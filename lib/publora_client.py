"""Thin Publora REST client for the Instagram Skills project.

Wraps the Publora API endpoints this bundle uses. As of 2026-06 Publora exposes
the pieces an Instagram publisher needs:
- POST /create-post              (create a draft or scheduled post group)
- POST /get-upload-url           (pre-signed S3 URL for one image or video)
- PUT  /update-post/:id          (set status="scheduled" + scheduledTime)
- DELETE /delete-post/:id         (remove a draft/scheduled group + its media)
- GET  /platform-connections     (list connected accounts + token health)

Instagram REQUIRES media on every post. A text-only Instagram post fails at
publish time. So the publish path is always a three-step flow:

    1. POST /create-post  with NO scheduledTime  -> draft + postGroupId
    2. POST /get-upload-url -> pre-signed URL, then PUT the file bytes to S3
       (repeat per image for a 2-10 item carousel)
    3. PUT /update-post/:postGroupId  status="scheduled" + scheduledTime

Creating a post with scheduledTime set up front races the scheduler against the
S3 upload, so the draft-first order is mandatory, not a style choice.

Base URL: https://api.publora.com/api/v1
Auth header: x-publora-key: sk_...  (NOT Bearer)
Content-Type: application/json. Server-to-server only (custom headers are not in
the CORS allowlist, so browser calls fail preflight).

Design note: this client is deliberately minimal. Skills call the high-level
`publish_media_post` for the full flow, after the user has approved a caption
rendered via `lib/approval.py` and supplied the media files. The Publora JSON
endpoints (create-post, get-upload-url, update-post, delete-post) retry on
transient 408/429/5xx via the shared retry decorator. The raw S3 PUT in
`put_to_s3` is NOT covered by that decorator: it talks to S3 with a pre-signed
URL, not a Publora JSON endpoint, and is left as a single attempt by design.
"""
from __future__ import annotations
import os
import time
import random
import mimetypes
from datetime import datetime, timezone
from typing import Any, Optional

import requests


def _utcnow_iso() -> str:
    """Current UTC time as an ISO 8601 string with a trailing `Z`, matching the
    `2026-03-01T14:00:00.000Z` form the rest of this client and the Publora docs
    use. Used as the implicit `scheduledTime` for a publish-now request: the
    create-post / update-post API treats a past-or-now time as immediate."""
    return (
        datetime.now(timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        + "Z"
    )


class PubloraError(RuntimeError):
    pass


RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504}


def _retry(attempts: int = 3, base_delay: float = 0.6):
    """Retry decorator for HTTP methods. Triggers on 408/429/5xx and on
    transient network errors. Exponential backoff with jitter."""

    def decorator(fn):
        def wrapper(*args, **kwargs):
            last_exc: Optional[Exception] = None
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except PubloraError as e:
                    msg = str(e)
                    retryable = any(f"HTTP {s}" in msg for s in RETRYABLE_STATUSES)
                    if not retryable or attempt == attempts - 1:
                        raise
                    last_exc = e
                except (requests.ConnectionError, requests.Timeout) as e:
                    if attempt == attempts - 1:
                        raise
                    last_exc = e
                time.sleep(base_delay * (2**attempt) + random.uniform(0, 0.25))
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator


# Platform IDs must match Publora's regex: /^[a-z]+-[a-zA-Z0-9_-]+$/
# For Instagram the prefix is `instagram-` (e.g. "instagram-11223344").
PLATFORM_ID_PREFIX = "instagram-"

# Content types Instagram accepts at publish time.
IMAGE_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
VIDEO_CONTENT_TYPES = {"video/mp4", "video/quicktime"}


# Explicit extension -> MIME map for the formats Publora/Instagram accept.
# Videos must be listed here so an unknown-to-`mimetypes` container (.mkv,
# .webm, .avi) is never mis-defaulted to image/jpeg, which would tag the upload
# as media_type "image" and break it. Keep image and video families explicit.
_EXT_CONTENT_TYPES = {
    # images
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    # videos
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".m4v": "video/x-m4v",
    ".webm": "video/webm",
    ".mkv": "video/x-matroska",
    ".avi": "video/x-msvideo",
}


def guess_content_type(file_name: str) -> str:
    """Resolve a MIME type from a file name, restricted to the formats Instagram
    accepts. Raises PubloraError on an unknown extension rather than blindly
    defaulting to image/jpeg, so a video container `mimetypes` does not know
    (.mkv, .webm, .avi) can never be mis-tagged as an image and break upload."""
    ext = os.path.splitext(file_name)[1].lower()
    if ext in _EXT_CONTENT_TYPES:
        return _EXT_CONTENT_TYPES[ext]
    # Last resort: trust the OS mime database only when it yields an
    # image/* or video/* type. Anything else (or no guess) is an error.
    guessed, _ = mimetypes.guess_type(file_name)
    if guessed and (guessed.startswith("image/") or guessed.startswith("video/")):
        return guessed
    raise PubloraError(
        f"Cannot determine an Instagram-supported content type for {file_name!r}"
        f" (extension {ext or '<none>'!r}). Pass content_type= explicitly or use"
        " a known image (.jpg/.jpeg/.png/.webp/.gif) or video"
        " (.mp4/.mov/.m4v/.webm/.mkv/.avi) file."
    )


class PubloraClient:
    BASE_URL = "https://api.publora.com/api/v1"

    def __init__(self, api_key: Optional[str] = None, timeout: float = 60.0):
        self.api_key = api_key or os.getenv("PUBLORA_API_KEY")
        if not self.api_key:
            raise PubloraError(
                "PUBLORA_API_KEY not set. Export it or pass api_key= explicitly."
            )
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "x-publora-key": self.api_key,
                "Content-Type": "application/json",
            }
        )

    # ---- Posts ------------------------------------------------------------

    def create_post(
        self,
        *,
        content: str,
        platforms: list[str],
        scheduled_time: Optional[str] = None,
        platform_settings: Optional[dict[str, Any]] = None,
        media_urls: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Create a post group (a draft by default).

        For Instagram, omit `scheduled_time` here on purpose: you want a draft
        so you can attach media first, then schedule via `update_post`. Passing
        a `scheduled_time` up front races the scheduler against the S3 upload.

        Args:
            content: The caption text. Instagram caps captions at 2,200 chars;
                only the first ~125 show before the "more" fold.
            platforms: List of platform connection IDs, e.g.
                ["instagram-11223344"]. Each must match /^[a-z]+-[a-zA-Z0-9_-]+$/.
            scheduled_time: ISO 8601 UTC datetime. Omit for a draft (the
                recommended first step for any media post).
            platform_settings: Optional per-platform object. For a Reel pass
                {"instagram": {"videoType": "REELS"}}; for a Story pass
                {"instagram": {"videoType": "STORIES"}}. REELS is the default.

        Returns:
            { "success": true, "postGroupId": "..." } on HTTP 200.
        """
        if not content or not content.strip():
            raise PubloraError("content is required (cannot be empty or whitespace)")
        if not platforms:
            raise PubloraError("at least one platform ID is required")
        payload: dict[str, Any] = {
            "content": content,
            "platforms": platforms,
        }
        if scheduled_time:
            payload["scheduledTime"] = scheduled_time
        if platform_settings:
            payload["platformSettings"] = platform_settings
        if media_urls:
            payload["mediaUrls"] = media_urls
        return self._post("/create-post", payload)

    # ---- Media flow -------------------------------------------------------

    def get_upload_url(
        self,
        *,
        file_name: str,
        content_type: str,
        post_group_id: str,
        media_type: str = "image",
    ) -> dict[str, Any]:
        """Request a pre-signed S3 upload URL for one media file.

        Args:
            file_name: e.g. "slide1.jpg". Publora sanitizes the name (spaces to
                underscores, special chars stripped).
            content_type: MIME type, e.g. "image/jpeg" or "video/mp4".
            post_group_id: The draft to attach this media to (from create_post).
            media_type: "image" or "video". Required by Publora: omitting it
                makes the S3 PutObject fail, so this client always sends it.

        Returns:
            { success, uploadUrl, fileUrl, mediaId }. `uploadUrl` is the
            pre-signed PUT target and expires in 1 hour.
        """
        if media_type not in ("image", "video"):
            raise PubloraError('media_type must be "image" or "video"')
        return self._post(
            "/get-upload-url",
            {
                "fileName": file_name,
                "contentType": content_type,
                "type": media_type,
                "postGroupId": post_group_id,
            },
        )

    def put_to_s3(self, upload_url: str, data: bytes, content_type: str) -> None:
        """PUT raw file bytes to the pre-signed S3 URL. No Publora auth header
        here (the signature is in the URL). Raises on a non-2xx response.

        Note: unlike the Publora JSON endpoints, this S3 PUT is a single attempt
        and is not wrapped by the shared `_retry` decorator. If it fails, the
        caller (`upload_media_file` / `publish_media_post`) deletes the draft so
        no broken media reference is left behind."""
        r = requests.put(
            upload_url,
            data=data,
            headers={"Content-Type": content_type},
            timeout=self.timeout,
        )
        if r.status_code >= 300:
            raise PubloraError(
                f"S3 upload failed HTTP {r.status_code}: {r.text[:300]}"
            )

    def update_post(
        self,
        post_group_id: str,
        *,
        status: str = "scheduled",
        scheduled_time: Optional[str] = None,
    ) -> dict[str, Any]:
        """Move a draft to scheduled (or publish-now by passing the current
        time). Call this only after every media file has finished uploading."""
        payload: dict[str, Any] = {"status": status}
        if scheduled_time:
            payload["scheduledTime"] = scheduled_time
        return self._put(f"/update-post/{post_group_id}", payload)

    def delete_post(self, post_group_id: str) -> dict[str, Any]:
        """Delete a draft/scheduled post group and all of its attached media.
        Use this to clean up an abandoned upload (a get-upload-url call whose
        S3 PUT failed leaves a broken media reference that blocks scheduling)."""
        return self._delete(f"/delete-post/{post_group_id}")

    def upload_media_file(
        self,
        post_group_id: str,
        path: str,
        *,
        content_type: Optional[str] = None,
    ) -> dict[str, Any]:
        """Upload one local file to a draft: get URL, read bytes, PUT to S3.

        Returns the get_upload_url response ({fileUrl, mediaId, ...}) so the
        caller can record what was attached.
        """
        file_name = os.path.basename(path)
        ctype = content_type or guess_content_type(file_name)
        media_type = "video" if ctype in VIDEO_CONTENT_TYPES or ctype.startswith(
            "video/"
        ) else "image"
        meta = self.get_upload_url(
            file_name=file_name,
            content_type=ctype,
            post_group_id=post_group_id,
            media_type=media_type,
        )
        with open(path, "rb") as f:
            self.put_to_s3(meta["uploadUrl"], f.read(), ctype)
        return meta

    def publish_media_post(
        self,
        *,
        content: str,
        platforms: list[str],
        media: list[str],
        scheduled_time: Optional[str] = None,
        platform_settings: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Run the full Instagram publish flow in one call.

        Steps: create a draft, upload each media file, then schedule.
        Instagram requires at least one media file; a 2-10 file list becomes a
        carousel (all images, no mixed media). On any failure after the draft
        is created, the draft is deleted so no broken group is left behind.

        Args:
            content: caption text (<= 2,200 chars).
            platforms: e.g. ["instagram-11223344"].
            media: ordered list of local file paths. 1 image -> single photo
                post; 1 video -> Reel (or Story via platform_settings);
                2-10 images -> carousel in this order.
            scheduled_time: ISO 8601 UTC. If omitted, the final update-post call
                sends the current UTC time, which Publora treats as immediate
                (a publish-now). The update never PUTs status="scheduled" with an
                absent scheduledTime, which the create-post API does not support.
            platform_settings: e.g. {"instagram": {"videoType": "REELS"}}.

        Returns:
            { "postGroupId": ..., "media": [<upload responses>],
              "scheduled": <update_post response> }.
        """
        if not media:
            raise PubloraError(
                "Instagram requires at least one media file. Text-only posts "
                "are rejected at publish time."
            )
        if len(media) > 10:
            raise PubloraError(
                "Instagram carousels allow at most 10 media items."
            )
        draft = self.create_post(
            content=content,
            platforms=platforms,
            platform_settings=platform_settings,
        )
        post_group_id = draft.get("postGroupId")
        if not post_group_id:
            raise PubloraError(f"create-post did not return a postGroupId: {draft}")
        # A draft only leaves draft state when update-post carries a
        # scheduledTime. For a publish-now request (scheduled_time is None) we
        # must still send a concrete time -- "now" -- because PUT
        # status="scheduled" with no scheduledTime is not a supported way to
        # publish. Publora treats a past/near time as immediate.
        effective_time = scheduled_time or _utcnow_iso()
        try:
            uploaded = [self.upload_media_file(post_group_id, p) for p in media]
            scheduled = self.update_post(
                post_group_id,
                status="scheduled",
                scheduled_time=effective_time,
            )
        except Exception:
            # Best-effort cleanup so an abandoned draft does not linger.
            try:
                self.delete_post(post_group_id)
            except Exception:
                pass
            raise
        return {
            "postGroupId": post_group_id,
            "media": uploaded,
            "scheduled": scheduled,
        }

    # ---- Connections (read) -----------------------------------------------

    def list_connections(self) -> list[dict[str, Any]]:
        """List connected social accounts with token health.

        Returns the `connections` array from GET /platform-connections. Each
        entry has platformId, username, displayName, tokenStatus, etc. Use it to
        confirm an Instagram account is connected and which `instagram-<id>` to
        pass to the publish flow.
        """
        r = self._session.get(
            self.BASE_URL + "/platform-connections", timeout=self.timeout
        )
        data = self._handle(r)
        return data.get("connections", [])

    def instagram_connections(self) -> list[dict[str, Any]]:
        """Convenience filter: only the connected Instagram accounts."""
        return [
            c
            for c in self.list_connections()
            if str(c.get("platformId", "")).startswith(PLATFORM_ID_PREFIX)
        ]

    # ---- Internals --------------------------------------------------------

    @_retry()
    def _post(self, path: str, json_body: dict[str, Any]) -> dict[str, Any]:
        r = self._session.post(
            self.BASE_URL + path, json=json_body, timeout=self.timeout
        )
        return self._handle(r)

    @_retry()
    def _put(self, path: str, json_body: dict[str, Any]) -> dict[str, Any]:
        r = self._session.put(
            self.BASE_URL + path, json=json_body, timeout=self.timeout
        )
        return self._handle(r)

    @_retry()
    def _delete(self, path: str) -> dict[str, Any]:
        r = self._session.delete(self.BASE_URL + path, timeout=self.timeout)
        return self._handle(r)

    @staticmethod
    def _handle(r: requests.Response) -> dict[str, Any]:
        if r.status_code >= 400:
            try:
                body = r.json()
            except Exception:
                body = {"error": r.text[:500]}
            raise PubloraError(f"HTTP {r.status_code}: {body}")
        return r.json()
