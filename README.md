<p align="center">
  <img src="assets/hero.png" alt="Instagram marketing skills for Claude Code and Codex, open source MIT licensed" width="900" />
</p>

# Instagram Marketing Skills for Claude Code and Codex

<p align="center">
  <img src="https://img.shields.io/github/v/release/sergebulaev/instagram-skills?color=111827&label=release" alt="Latest release">
  <img src="https://img.shields.io/badge/Claude_Code-Compatible-D97757?logo=anthropic&logoColor=white" alt="Claude Code Compatible">
  <img src="https://img.shields.io/badge/Codex-Compatible-111827" alt="Codex Compatible">
  <img src="https://img.shields.io/badge/Claude-Skills-8A63D2" alt="Claude Skills">
  <img src="https://img.shields.io/badge/License-MIT-22C55E.svg" alt="MIT License">
  <img src="https://img.shields.io/github/stars/sergebulaev/instagram-skills?style=social" alt="GitHub stars">
  <img src="https://img.shields.io/badge/PRs-welcome-F59E0B.svg" alt="PRs Welcome">
</p>

> **Part of the [linkedin-skills](https://github.com/sergebulaev/linkedin-skills) family (400+ stars).** Same voice engine and approve-before-publish flow, now for Instagram. Also available for [X](https://github.com/sergebulaev/x-skills) · [YouTube](https://github.com/sergebulaev/youtube-skills) · [TikTok](https://github.com/sergebulaev/tiktok-skills) · [Threads](https://github.com/sergebulaev/threads-skills) · [Facebook](https://github.com/sergebulaev/facebook-skills).

**9 skills that turn Claude Code and Codex into your Instagram content team.** They write captions and Reels hooks in your voice, size hashtags, plan carousels and a full week of content, read your niche from real data, and optimize your profile. Every draft gets the AI tells stripped and waits for your approval before anything publishes. You supply the image or video; the skills write the words. No coding required.

Once installed, just ask Claude Code or Codex things like:

- "Write a caption for this Reel about [topic]"
- "Plan a week of Instagram posts for my [niche]"
- "What's working in my niche right now?" (reads real data via Apify)
- "Rewrite this caption so it doesn't sound like AI"

The right skill activates automatically. Then you review and approve.

## Install

Pick whichever way you use Claude Code or Codex:

### Codex CLI

```bash
codex plugin marketplace add sergebulaev/instagram-skills
codex plugin add instagram-skills@instagram-skills
```

To test a local clone before publishing changes:

```bash
git clone https://github.com/sergebulaev/instagram-skills.git
cd instagram-skills
codex plugin marketplace add .
codex plugin add instagram-skills@instagram-skills
```

### claude.ai (web)

1. Open https://claude.ai/code
2. Go to **Skills** in the sidebar
3. Click **Add from GitHub**
4. Paste: `sergebulaev/instagram-skills`
5. Done. The skills activate automatically when you ask about Instagram.

### Claude Desktop (Mac / Windows)

1. Open Claude Desktop
2. Open **Settings** (gear icon)
3. Go to **Skills**
4. Click **Add from GitHub**
5. Paste: `sergebulaev/instagram-skills`
6. Done. Start a new conversation and ask Claude to write a caption.

### Claude Code (CLI / VS Code / JetBrains)

```
/plugin marketplace add sergebulaev/instagram-skills
/plugin install instagram-skills@instagram-skills
```

Or clone the repo and open it as your working directory:

```bash
git clone https://github.com/sergebulaev/instagram-skills.git
cd instagram-skills
```

### OpenClaw

1. Open your OpenClaw working directory
2. Clone the skills into it:
   ```bash
   git clone https://github.com/sergebulaev/instagram-skills.git
   ```
3. In OpenClaw settings, add this to your system prompt:
   ```
   You have Instagram marketing skills in ./instagram-skills/.
   For any Instagram task, read the relevant skills/*/SKILL.md first.
   Use lib/url_parser.py for URL parsing and lib/publora_client.py for publishing.
   ```
4. Done. Ask OpenClaw to write a Instagram post.

### Hermes Agent

Hermes Agent (Nous Research) follows the agentskills.io open standard and loads `skills/*/SKILL.md` directly. Clone the bundle into your Hermes skills folder:

```bash
git clone https://github.com/sergebulaev/instagram-skills.git ~/.hermes/skills/instagram-skills
```

Coming from OpenClaw? `hermes claw migrate` imports these skills automatically. Then call `/<skill-name>` from any of your Hermes chat surfaces.

### Any agent (skills CLI)

One command that works across Claude Code, Codex, Cursor, and any other agent that reads SKILL.md files:

```bash
npx skills add sergebulaev/instagram-skills
```

> **Found this useful? [Star the repo](https://github.com/sergebulaev/instagram-skills).** Curated Claude Code and Codex directories rank and gate by star count, so a star is what makes these skills findable for the next person. It is the only thing we ask. No signup, no email.

## What you can do

Once installed, just ask Claude Code or Codex for help with Instagram. The right skill activates automatically.

**Write a caption:**
> "Write me an Instagram caption about how I cut my editing time from 6 hours to 47 minutes. Hook in the first line."

**Plan a carousel:**
> "Turn my notes into a 10-slide carousel on portfolio mistakes for junior designers."

**Reverse-engineer a viral Reel:**
> "What hook does this Reel use? https://www.instagram.com/reel/C9_aBcDeF/ (I'll paste the first 3 seconds)"

**Size your hashtags:**
> "Give me 5 hashtags for this post, sized so my 2k account can actually rank."

**Check a draft before posting:**
> "Audit this caption for AI tells and the first-125-char hook: [paste your text]"

**Plan your week:**
> "Plan a week of Instagram content. I'm launching a design course for junior designers."

Every skill shows you a draft first and waits for your OK. Nothing gets posted without your approval.

## The 9 skills

| Skill | What it does |
|---|---|
| **Caption Writer** | Drafts a caption with the hook in the first 125 chars, a skimmable body, and one CTA, using a 2026 hook formula picked by goal: saves, shares, comments, or follows |
| **Carousel Planner** | Plans a carousel slide by slide (up to 10): a hook slide that opens a loop, value slides front-loaded, and a payoff slide that earns the save and the follow |
| **Hook Extractor** | Reverse-engineers the hook from any viral Reel or carousel. Maps it to one of the 10 Instagram formulas and returns a blank template you can fill |
| **Hashtag Strategist** | Builds a sized 3-5 hashtag set (niche / mid / broad) you can actually rank in, matched to the post. The 2026 reality, not the 30-tag wall |
| **Humanizer** | Removes the AI tells human readers react to: 2026 AI vocabulary scored by paragraph density, reveal bridges, staccato fragment stacks, stacked triads, performed sincerity, emoji storms; caps em dashes at about one per 100 words instead of banning them (29% of human captions use one). Does not promise to beat detectors (no edit reliably does). Bundles a `--mode audit` pre-publish check |
| **Content Planner** | Creates a weekly plan with a Reels / carousel / story mix, per-day hooks, posting times, a saves-and-shares goal, and a goal-mix balance check |
| **Repurposer** | Turns a LinkedIn post, blog, YouTube script, or X thread into a native Instagram carousel or caption: re-hooked before the 125-char fold, off-platform artifacts stripped, never a copy-paste |
| **Profile Optimizer** | Audits and rewrites the profile end-to-end: photo, searchable NAME field, bio (150 chars), goal-matched link, category label, highlights (covers, order, naming), the first-9 grid, and up to 3 pinned posts, with a scorecard and before/after rewrites |
| **Audience Insights** | Reads your niche and profile from real data via Apify: scans a hashtag for the posts traveling now (likes, comments, owner, format) and pulls follower/post/bio stats for any handle, yours or a competitor's. Instagram hides likers and commenters, so this is niche discovery plus profile stats, not an engager list |

## Media is required on every Instagram post

Instagram does not allow text-only posts. The skills write the caption, hook, hashtags, and slide or shot plan. **You supply the image or video.** When you connect Publora and point a skill at your media files, it runs the publish flow for you:

```
1. create a draft (no scheduled time)   -> postGroupId
2. upload each file to S3                (2-10 images for a carousel, in order)
3. schedule the post                     (status=scheduled + time)
```

That exact order matters: scheduling before the upload finishes races Instagram's scheduler against the media. The bundle's `lib/publora_client.publish_media_post(...)` does all three steps in one call.

## Optional: auto-post with Publora

By default, the skills draft the caption for you to post in the Instagram app with your own media. If you want Claude Code or Codex to upload your media and schedule the post directly, connect Publora. It takes about 2 minutes.

### What is Publora?

[Publora](https://publora.com) is a publishing API that handles the Instagram media flow (draft, upload, schedule) in one call, and can cross-post the same content to other networks.

### Setup (2 minutes)

**Step 1.** Sign up at https://app.publora.com/signup (free)

**Step 2.** Connect Instagram: click **Channels** in the left sidebar, then **Add Channel**, pick **Instagram**, authorize. You need a **Business or Creator** account (personal accounts are not supported).

**Step 3.** Find your Platform ID: go to **Channels**, click your Instagram account. The ID looks like `instagram-11223344`. Copy the whole thing including `instagram-`.

**Step 4.** Get your API key: click **Settings** (gear icon, bottom-left), then **API**, then **Create Key**. Copy the `sk_...` string.

**Step 5.** Create a file called `.env` in the instagram-skills folder:

```
PUBLORA_API_KEY=sk_paste_your_key_here
INSTAGRAM_PLATFORM_ID=instagram-paste_your_id_here
```

If you cloned the repo, copy the template instead:

```bash
cp .env.example .env
```

Then open `.env` and replace the placeholders with your real values.

**Step 6.** Install two small Python packages:

```bash
pip install requests python-dotenv
```

**Step 7.** Test it. Ask Claude Code or Codex:

> "Schedule a test Instagram post via Publora 24 hours from now with this image: [path]. Caption: 'testing the API connection, will cancel in dashboard'."

If Publora returns a `postGroupId`, you're set. Cancel the post in the Publora dashboard before the scheduled time. If you get HTTP 401, your API key is wrong. If you get an `Invalid platform ID format` error, your `INSTAGRAM_PLATFORM_ID` is wrong. See [Troubleshooting](#troubleshooting).

> **Note on media:** Instagram rejects text-only posts. If you do not point a skill at an image or video, it returns the caption as a copy-paste block plus a reminder to attach your media in the app.

## Optional: generate illustrations with Pixfaro

Instagram is visual-first. The Carousel Planner can generate carousel slides and quote-cards and attach them automatically when publishing. Without a key it drafts the image prompt and asks you to generate it yourself, so nothing breaks.

[Pixfaro](https://pixfaro.com) is a single image API over multiple models (from `flux-schnell` at $0.004 to `gpt-5-image`). It composites your handle, brand color, or logo onto the image as a **pixel-exact overlay**, so a cheap base model still renders crisp text on a carousel slide. Pull those brand fields from your [Voice & Brand Profile](references/voice-profile.md) (section 6) and every asset stays on-brand.

Setup: drop `PIXFARO_TOKEN=pf_live_...` into your `.env`. The thin client at `lib/pixfaro_client.py` and the wrappers `lib.illustrate(prompt, kind="carousel")` / `lib.refine(image_id, instruction)` return a hosted URL that flows straight into `lib.publish(..., media_urls=[url])`. `refine` edits a prior image by its id (cheaper than regenerating); results carry `cost`, `balance_after`, and a `premium` flag so the skills never quietly spend on a pricey model.

## Voice rules

Every skill follows these rules automatically:

1. Em dashes capped at about one per 100 words. The character stopped being a tell in 2026; the density is.
2. Capitalize names. Always. Lowercase a brand reads as careless.
3. No AI vocabulary clusters. One 2026 marker ("leverage", "significant", "elevate", "dive in") in a paragraph is English; three in one paragraph reads as AI and gets the paragraph rewritten.
4. Specific numbers beat adjectives. "47 minutes" beats "fast".
5. The hook lives in the first 125 chars (everything after is behind the "more" fold).
6. Hashtags are sizing, not volume: 3-5 sized tags, not 30. 0-3 emoji.

## Troubleshooting

| Problem | Fix |
|---|---|
| Skills don't activate when I ask about Instagram | Make sure you installed via the Skills panel, `/plugin install`, or `codex plugin add`. Try a new conversation. |
| "PUBLORA_API_KEY not set" | Your `.env` file is missing or in the wrong folder. It should be in the `instagram-skills/` root. |
| "401 Invalid API key" from Publora | Your API key is wrong or revoked. Go to Publora Settings > API > Create a new key. |
| "Invalid platform ID format" | Your `INSTAGRAM_PLATFORM_ID` is wrong. Go to Publora Channels and copy the full `instagram-...` string. |
| My post failed with "media required" | Instagram does not allow text-only posts. Point the skill at an image or video file. |
| My carousel was rejected | A carousel is 2-10 items, all images or all video. You cannot mix images and a video in one carousel. |
| Personal account won't connect | Instagram's API needs a Business or Creator account. Switch in the Instagram app settings, then reconnect. |
| `pip install` fails | Use a virtual environment: `python -m venv venv && source venv/bin/activate && pip install requests python-dotenv` |

## Cross-cutting references

- [`references/hook-formulas.md`](references/hook-formulas.md) - the 10 Instagram hook formulas with skeletons and goal tags
- [`references/algorithm-heuristics.md`](references/algorithm-heuristics.md) - 2026 Instagram ranking signals, timing, and limits
- [`references/hashtag-strategy.md`](references/hashtag-strategy.md) - the 2026 sized-hashtag model (3-5, not 30)
- [`references/media-workflow.md`](references/media-workflow.md) - the draft, upload, schedule media flow
- [`references/voice-rules.md`](references/voice-rules.md) - the canonical voice rules every skill inherits

---

<details>
<summary><b>For developers: runtime compatibility, URL parsing, and internals</b></summary>

## Runtime compatibility

```
instagram-skills/
  skills/             SKILL.md frontmatter; native to Claude Code and Codex, others read as markdown
  .codex-marketplace/ generated nested Codex package (run scripts/sync_codex_marketplace.py)
  lib/                pure Python, works in any agent runtime
  references/         pure markdown, works anywhere
  scripts/            pure Python CLI, works anywhere
```

| Runtime | Auto-discovers skills? | Setup |
|---|---|---|
| **Claude Code** (CLI, Desktop, Web, IDE) | Yes | Install via plugin or clone. Skills activate on matching prompts. |
| **Codex CLI** | Yes | `codex plugin marketplace add sergebulaev/instagram-skills` and `codex plugin add instagram-skills@instagram-skills`. |
| **Anthropic Managed Agents** (`/v1/agents`) | Yes | Pass skill files in the agent context. |
| **Cursor / Cline / Aider** | Manual | Read `SKILL.md` files as prompt context; import `lib/` as Python. |
| **LangChain / AutoGen** | No | Use `lib/` as a package; feed `references/` as prompt context. |

## Generic Python agent quickstart

```python
import sys; sys.path.insert(0, "path/to/instagram-skills")
from lib import parse_instagram_url, PubloraClient, publish

parsed = parse_instagram_url("https://www.instagram.com/reel/C9_aBcDeF/")
print(parsed["url_type"], parsed["shortcode"])  # reel C9_aBcDeF

# Write side (Publora) - the full Instagram media flow in one call
client = PubloraClient()  # reads PUBLORA_API_KEY from env
client.publish_media_post(
    content="the 3-step setup is below, steal it\n\n#niche #mid #broad",
    platforms=["instagram-11223344"],
    media=["slide1.jpg", "slide2.jpg", "slide3.jpg"],  # local paths, in order
    scheduled_time="2026-07-01T15:00:00.000Z",
)

# Or use the high-level wrapper that handles manual / Publora / diy routing
publish("carousel", draft_text="...", target_url="https://www.instagram.com/",
        media=["slide1.jpg", "slide2.jpg"], platforms=["instagram-11223344"])
```

## URL handling

`lib/url_parser.py` parses Instagram post, Reel, and profile URLs:

| URL fragment | Parsed |
|---|---|
| `instagram.com/p/SHORTCODE/` | `{shortcode, url_type: "post"}` |
| `instagram.com/reel/SHORTCODE/` | `{shortcode, url_type: "reel"}` |
| `instagram.com/USERNAME/` | `{username, url_type: "profile"}` |
| `instagram.com/stories/USER/ID/` | `{username, shortcode, url_type: "story"}` |

```bash
python lib/url_parser.py "https://www.instagram.com/p/C8xYz12abcd/"
```

## Why the publish flow is three steps

Instagram requires media, and uploading media to a pre-signed S3 URL is
asynchronous. If you create a post with a scheduled time set up front, the
scheduler can fire before the upload finishes, producing a failed or media-less
post. So the flow is always: create a draft, upload the media, then set the
schedule. `publish_media_post` enforces that order and cleans up the draft if any
step fails.

## Why there is no read layer by default

Instagram has no cheap, documented post-read actor wired into this bundle, so
`ig-hook-extractor` asks the user to paste the caption (and slide or Reel hook).
If you add an Apify Instagram actor later, gate it behind `APIFY_TOKEN` and keep
the paste fallback.

</details>

## References

- [Publora API docs](https://docs.publora.com) - endpoint reference for the publishing layer
- [Instagram Graph API content publishing](https://developers.facebook.com/docs/instagram-api/guides/content-publishing) - the platform API the publish layer builds on

## Who builds this

These skills come out of [Creative Content Crafts](https://cccrafts.ai), an engineering company. We build the machinery underneath a company's public voice: ICP parsing, engagement systems, content guardrails, and posting infrastructure. We do not sell the words themselves.

We call that layer **content engineering**. Writing collapsed to the price of a chat subscription. What stayed valuable is everything below it: pulling every post your market wrote this week, keeping a live list of the people who matter, engaging on it daily with judgment in the loop, and catching the risky drafts before the platform does.

This repo is the thin top layer of that stack, open-sourced. The engine underneath is what we build for clients.

## License

MIT. Powered by [Publora](https://publora.com).

## Related open-source skill bundles

Part of a family of AI social-media marketing skill bundles for Claude Code and Codex:

- [linkedin-skills](https://github.com/sergebulaev/linkedin-skills) - LinkedIn
- [x-skills](https://github.com/sergebulaev/x-skills) - X (Twitter)
- **instagram-skills - Instagram (this repo)**
- [youtube-skills](https://github.com/sergebulaev/youtube-skills) - YouTube
- [threads-skills](https://github.com/sergebulaev/threads-skills) - Threads
- [tiktok-skills](https://github.com/sergebulaev/tiktok-skills) - TikTok
- [facebook-skills](https://github.com/sergebulaev/facebook-skills) - Facebook Pages

Also: [Anthropic Skills repo](https://github.com/anthropics/skills), the `awesome-claude-skills` directory.
