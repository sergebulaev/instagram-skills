"""Detect which publishing backend is configured and format user-facing messages.

The skills support three tiers:

  TIER 0 - manual (default, zero setup)
    No credentials in env. Skills produce the caption (and slide or shot list);
    the user posts it in the Instagram app with their own media. Works for
    anyone, any setup.

  TIER 1 - publora (recommended, ~2-min setup)
    `PUBLORA_API_KEY` + `INSTAGRAM_PLATFORM_ID` present. On approval the skills
    run the full media flow (create draft, upload the user's image or video,
    schedule) via the Publora REST API. Sign up: https://app.publora.com/signup

  TIER 2 - diy (advanced)
    `INSTAGRAM_SKILLS_CUSTOM_POSTER` set to a command the user built themselves
    (e.g. via Claude Code or Codex on the Instagram Graph API). Skills delegate
    publishing to that custom tool.

`active_backend()` picks the highest-privilege available. `manual_mode_message()`
is what skills show the user when no backend auto-posts. `publish()` is the
high-level wrapper skills should call so SKILL.md files don't repeat the
dispatch.

Instagram note: every post needs media. The writer skills produce the caption,
hook, hashtags, and slide/shot plan; the USER supplies the image or video file.
So `publish()` only auto-posts on the Publora tier when `media` file paths are
provided. With no media, or on the manual tier, it returns a copy-paste caption
block plus a reminder to attach the media in the Instagram app.
"""
from __future__ import annotations
import json
import os
import shlex
import subprocess
from typing import Any, Literal, Optional

BackendName = Literal["publora", "manual", "diy"]
PublishKind = Literal["post", "carousel", "reel", "story"]

PUBLORA_SIGNUP_URL = "https://app.publora.com/signup"


def active_backend() -> BackendName:
    """Return the active publishing backend.

    Priority: publora > diy > manual. Users with Publora configured get
    auto-post even if they also have a custom poster, unless they remove the
    Publora env var.
    """
    if os.getenv("PUBLORA_API_KEY") and os.getenv("INSTAGRAM_PLATFORM_ID"):
        return "publora"
    if os.getenv("INSTAGRAM_SKILLS_CUSTOM_POSTER"):
        return "diy"
    return "manual"


def manual_mode_message(
    draft_text: str, target_url: str, kind: str = "post"
) -> str:
    """Format the copy-paste approval output for the manual/draft-only tier.

    The user has just approved a caption and expects to publish. Since no
    backend is configured (or no media was supplied), we hand them the caption
    plus a reminder that Instagram needs the image or video attached in the app.
    """
    media_hint = {
        "post": "attach your image, then paste the caption",
        "carousel": "add your slides in order (2-10), then paste the caption",
        "reel": "upload your video as a Reel, then paste the caption",
        "story": "upload your story media, then add the caption text",
    }.get(kind, "attach your media, then paste the caption")
    return f"""Caption approved. In the Instagram app, {media_hint}:

```
{draft_text}
```

**Where:** {target_url}

Remember: Instagram will not let you post without at least one image or video.

---

Want this to publish on a schedule instead of copy-paste? Connect Publora in
about 2 minutes:

1. Sign up free at {PUBLORA_SIGNUP_URL}
2. Connect your Instagram Business or Creator account (Channels then Add Channel)
3. Copy your API key (API section in the sidebar)
4. Add to `.env`:
   ```
   PUBLORA_API_KEY=sk_your_key_here
   INSTAGRAM_PLATFORM_ID=instagram-your_id_here
   ```
5. Next time you approve a post and point to your media files, it uploads and
   schedules for you.
"""


def signup_nudge() -> str:
    """One-liner to drop into skill outputs as a soft reminder."""
    return f"Auto-scheduling via Publora. Free signup: {PUBLORA_SIGNUP_URL}"


def publish(
    kind: PublishKind,
    draft_text: str,
    target_url: str,
    **kwargs: Any,
) -> Optional[dict]:
    """Dispatch an approved caption to the active backend.

    One call replaces the per-skill "On approval, adapt to the backend" block.
    Routes to publora / manual / diy based on `active_backend()`.

    Args:
        kind: "post" | "carousel" | "reel" | "story".
        draft_text: The approved caption.
        target_url: Where the post lands. For the manual tier this is shown to
            the user (e.g. the Instagram composer or the account URL).
        **kwargs: Backend-specific payload. For the publora tier:
            - media: list[str] of LOCAL file paths the user supplied. Required
              to auto-publish (Instagram rejects text-only posts). 1 file -> a
              single photo or Reel; 2-10 images -> a carousel in order.
            - platforms: list[str] of platform IDs (defaults to
              [INSTAGRAM_PLATFORM_ID]).
            - scheduled_time: ISO 8601 UTC (optional).
            - platform_settings: e.g. {"instagram": {"videoType": "REELS"}}.

    Returns:
        - publora (with media): dict from PubloraClient.publish_media_post.
        - manual / publora-without-media: {"mode": "manual", "message": ...}.
        - diy: {"mode": "diy", "returncode": int, "stdout": str, "stderr": str}.
        Returns None only if the chosen backend cannot run (missing deps).
    """
    backend = active_backend()
    media = kwargs.get("media") or []

    # Manual tier, or Publora configured but the user has not pointed us at
    # media files yet. Instagram cannot publish without media, so we surface the
    # copy-paste caption block and remind them to attach it.
    if backend == "manual" or (backend == "publora" and not media):
        return {
            "mode": "manual",
            "message": manual_mode_message(draft_text, target_url, kind=kind),
        }

    if backend == "publora":
        # Local import so manual-tier users never need `requests` installed.
        from .publora_client import PubloraClient

        client = PubloraClient()
        platform_id = kwargs.get("platform_id") or os.getenv("INSTAGRAM_PLATFORM_ID")
        platforms = kwargs.get("platforms") or ([platform_id] if platform_id else [])

        platform_settings = kwargs.get("platform_settings")
        if platform_settings is None and kind in ("reel", "story"):
            video_type = "STORIES" if kind == "story" else "REELS"
            platform_settings = {"instagram": {"videoType": video_type}}

        return client.publish_media_post(
            content=draft_text,
            platforms=platforms,
            media=media,
            scheduled_time=kwargs.get("scheduled_time"),
            platform_settings=platform_settings,
        )

    if backend == "diy":
        cmd = os.getenv("INSTAGRAM_SKILLS_CUSTOM_POSTER")
        if not cmd:
            return None
        payload = {
            "kind": kind,
            "draft_text": draft_text,
            "target_url": target_url,
            **kwargs,
        }
        # The user's poster receives JSON on stdin and kind/target as argv.
        argv = shlex.split(cmd) + [kind, target_url]
        proc = subprocess.run(
            argv,
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=300,
        )
        return {
            "mode": "diy",
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    raise RuntimeError(f"unknown backend: {backend!r}")


# ─────────────────────────────────────────────────────────────────
# IMAGE LAYER (Pixfaro) — the third integration alongside read (Apify)
# and write (Publora). Generate an illustration, get a hosted URL, hand
# that URL straight to `publish(..., media_urls=[url])`.
# ─────────────────────────────────────────────────────────────────

PIXFARO_SIGNUP_URL = "https://pixfaro.com"

# kind -> aspect_ratio (w:h). Callers can override with aspect_ratio=.
ILLUSTRATION_ASPECTS = {
    "post": "1:1",         # generic square feed image
    "square": "1:1",
    "portrait": "4:5",     # LinkedIn/IG feed portrait
    "carousel": "4:5",     # carousel/document slide
    "quote": "4:5",        # quote-card
    "wide": "1200:628",    # link-preview / OG image (~1.91:1)
    "link": "1200:628",
    "thumbnail": "16:9",   # YouTube thumbnail
    "landscape": "16:9",
    "story": "9:16",       # story / TikTok cover
    "cover": "9:16",
}


def image_backend() -> Literal["pixfaro", "manual"]:
    """`pixfaro` when PIXFARO_TOKEN (or PIXFARO_API_KEY) is set, else `manual`."""
    if os.getenv("PIXFARO_TOKEN") or os.getenv("PIXFARO_API_KEY"):
        return "pixfaro"
    return "manual"


def manual_illustration_message(prompt: str, aspect_ratio: str) -> str:
    """Shown when no Pixfaro key is set: hand the drafted prompt to the user."""
    return (
        "No Pixfaro key set, so I can't generate the image for you.\n"
        f"Generate it yourself (any tool) at {aspect_ratio}, then paste the URL "
        "and I'll attach it to the post.\n\n"
        "Image prompt:\n"
        f"{prompt}\n\n"
        f"Tip: a Pixfaro key ({PIXFARO_SIGNUP_URL}) lets me generate + attach "
        "the illustration in one step, with your brand handle/color overlaid."
    )


def illustrate(
    prompt: str,
    kind: str = "post",
    *,
    aspect_ratio: Optional[str] = None,
    model: Optional[str] = None,
    resolution: str = "1K",
    overlay: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Generate an illustration via the active image backend.

    This is the image analogue of `publish()`. On success with a Pixfaro key it
    returns the hosted URL, which you pass straight to
    `publish("post", text, url, media_urls=[result["url"]])`.

    Args:
        prompt: The image description (1-4000 chars).
        kind: Semantic size hint mapped via ILLUSTRATION_ASPECTS
            (post/portrait/carousel/quote/wide/thumbnail/story/cover).
        aspect_ratio: Explicit "w:h" override (wins over `kind`).
        model: Pixfaro model id. Defaults to nano-banana-2 (balanced). Use
            gemini-flash-lite for cheap high volume, gemini-pro-image for
            text-heavy premium.
        resolution: "1K" | "2K" | "4K".
        overlay: Pixel-exact branding composite {text|logo_id, position,
            opacity, font, color}. Feed brand fields from the Voice & Brand
            Profile so every asset is on-brand. Text here is crisp even on a
            cheap base model (it is composited, not model-generated).

    Returns:
        - pixfaro: {"backend": "pixfaro", "url", "cost", "id", "model"}.
        - manual:  {"backend": "manual", "message": <prompt block>}.
    """
    ar = aspect_ratio or ILLUSTRATION_ASPECTS.get(kind, "1:1")
    if image_backend() == "manual":
        return {"backend": "manual", "message": manual_illustration_message(prompt, ar)}

    from .pixfaro_client import PixfaroClient

    client = PixfaroClient()
    used_model = model or "nano-banana-2"
    data = client.generate(
        prompt,
        model=used_model,
        aspect_ratio=ar,
        resolution=resolution,
        overlay=overlay,
        force_refresh=kwargs.get("force_refresh", False),
    )
    return {
        "backend": "pixfaro",
        "url": data.get("url"),
        "cost": data.get("cost"),
        "id": data.get("id"),
        "model": used_model,
    }



if __name__ == "__main__":
    print(f"Active backend: {active_backend()}")
    if active_backend() == "manual":
        print("\nExample manual message:")
        print("-" * 60)
        print(
            manual_mode_message(
                draft_text="the post that took me 2 years to write..",
                target_url="https://www.instagram.com/",
                kind="carousel",
            )
        )
