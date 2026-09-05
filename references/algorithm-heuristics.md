# 2026 Instagram Posting Heuristics

Synthesized from Instagram's public ranking statements (Adam Mosseri's creator
posts), the 2023-2026 algorithm explainers, and observed creator data. Numbers
marked "reported" are community-measured, not officially confirmed. Instagram
ranks each surface (Feed, Reels, Explore, Stories) with its own model, but the
signals below generalize.

## Contents

- Signal weights (relative reach impact)
- The first 30-60 minutes
- Reach suppressors (avoid)
- Reach amplifiers
- Format and media limits (via the publishing API)
- Carousels
- Reels
- Stories
- Timing
- Saves and sends are the underrated levers
- Pre-publish checklist

## Signal weights (relative reach impact)

Instagram scores predicted engagement, and the engagement types are not equal.
Reported relative weights from creator testing and platform statements:

| Signal | Relative weight | Note |
|---|---|---|
| **Send / share** (to a friend in DM, or reshare to story) | highest positive | "sends per reach" is the metric the algorithm leans on hardest in 2026 |
| **Save** | high | the "I will come back to this" signal; drives reach for how-tos, lists, frameworks |
| **Comment** (esp. with author reply back) | high | a real conversation is a strong quality signal |
| **Reel watch time / completion / rewatch** | high (Reels) | for video, retention and rewatch decide the push |
| **Profile visit then follow** | high | the growth signal; payoff content earns it |
| **Like** | low | cheap affirmation, light reach |
| **Negative: "not interested", unfollow, hide, report** | heavy penalty | one report outweighs many likes |

Takeaway: optimize for **sends, saves, and comments**, not likes. The single
most useful question before posting: would a viewer send this to one specific
friend, or save it to use later?

## The first 30-60 minutes

- The opening window sets the trajectory. Early saves, sends, and comments tell
  the ranker to widen distribution to non-followers via Explore and the Reels
  feed.
- **Reply to early comments fast.** Author replies pull more comments and signal
  an active conversation.
- A Reel that holds retention through the first 3 seconds in the opening test
  earns a wider push.

## Reach suppressors (avoid)

- **Engagement bait** ("comment YES", "tag 3 friends", "double tap if") is
  explicitly downranked.
- **Reposted/recycled video with another app's watermark** (a visible logo from
  a different platform) is suppressed in Reels.
- **All-hashtag captions** (20-30 tags crammed at the top) read as spam in 2026
  and do not help reach. Sized 3-5 tags is the current guidance.
- **Aspect ratios outside 4:5 to 1.91:1** get cropped, which hurts a carousel or
  a feed image.
- **High hide/unfollow/report rate** collapses distribution fast.
- **Mixed media in one carousel** is rejected by the API outright.

## Reach amplifiers

- **Sends are the lever.** A post built to be sent to a friend (a relatable
  truth, a useful list, a "you need to see this") out-reaches a like-bait post.
- **Saves compound.** Save-bait formats (lists, frameworks, how-tos, before/
  after) keep earning reach for days as Explore surfaces them.
- **Reels with strong retention** get pushed to non-followers the hardest of any
  format in 2026. Original audio and on-screen text both help.
- **Carousels get a second look:** a viewer who does not swipe may see slide 2
  on a re-surface, so Instagram sometimes re-shows carousels, giving them a
  longer tail.
- **Replying to your own comments and DMs** in the first hour keeps the
  conversation signal alive.

## Format and media limits (via the publishing API)

| Item | Limit |
|---|---|
| Caption | 2,200 chars (first ~125 visible before "more") |
| Hashtags | 30 max per post (but 3-5 sized tags is the 2026 practice) |
| Carousel items | 2-10 (API; the native app allows 20) |
| Image formats | JPEG, PNG, WebP (WebP auto-converts to JPEG) |
| Image max size | 8 MB |
| Reel duration | up to 3 min (180s) via API; 5-90s are eligible for the Reels tab |
| Reel/video max size | 300 MB |
| Carousel video | up to 60s per clip |
| Mixed media in a carousel | not allowed (all images or all video) |
| Aspect ratio | 4:5 (portrait) to 1.91:1 (landscape); portrait 4:5 fills the feed |
| Rate limit | ~50 posts / 24h (some accounts report 25) |

- **Media is required on every post.** Instagram rejects text-only posts. The
  writer skills produce the caption; the user supplies the image or video.
- A single image posts as a photo; 2-10 images post as a carousel; a single
  video posts as a Reel by default (or a Story via `videoType: "STORIES"`).

## Carousels

- **Slide 1 is the entire funnel.** It must promise a payoff and open a loop, or
  the viewer never swipes. Everything else only matters if slide 1 earns the
  swipe.
- **Front-load value.** Swipe-through decays with depth, so the strongest item
  goes on slide 2 or 3, not saved for slide 10.
- **Optimal length: 6-10 slides** for a teaching or list carousel. Each slide
  should make one point and stand alone.
- **The last slide earns the save and the follow.** Close with a one-slide
  summary (the saveable artifact) plus a single clear ask.
- **Design for the 4:5 frame.** Portrait fills more screen and holds attention.

## Reels

- **The first 1-3 seconds decide reach.** Open with a pattern interrupt, an
  on-screen text hook, and the point. No "hey guys, welcome back".
- **Retention and rewatch are the goal.** A loop-able ending (the last frame
  flows into the first) lifts rewatch.
- **On-screen text** lets silent viewers get the hook and improves completion.
- **Original or trending audio** helps, but the hook and retention matter more.
- No visible watermark from another video app.

## Stories

- **Stories do not drive reach** to non-followers; they deepen the relationship
  with existing followers and keep you top-of-mind.
- A **reshare of your feed post to your story** is a send-equivalent signal and
  pushes the original to followers who missed it.
- Interactive stickers (poll, question, quiz) earn the taps that keep you in the
  front of the story tray.

## Timing

| Audience | Best windows (local) |
|---|---|
| US creators / consumers | weekdays 11 AM-1 PM and 7-9 PM, plus Sun evening |
| B2B / founders | Tue-Thu mid-morning and lunch |
| Global mixed | post when your specific audience is online (check your insights) |

- Consistency beats raw frequency. 3-5 high-quality posts a week with a
  steady cadence outperforms a daily dump of filler.
- Reels can be posted more often than carousels without fatigue, because each
  reaches a fresh non-follower audience.

## Saves and sends are the underrated levers

- A **save** means the viewer intends to return: it rewards lists, frameworks,
  how-tos, and before/after content. Design save-bait deliberately (IG5, IG8,
  IG10, IG1, IG6).
- A **send** means the viewer thought of a specific person: it rewards relatable
  truths, myth-busters, and contrarian takes (IG2, IG7, IG3, IG9).
- Both spread reach far more than a like. The hook-formulas goal tags map every
  formula to saves, shares, comments, or follows.

## Pre-publish checklist

- [ ] First 125 chars of the caption stop the scroll on their own.
- [ ] Em dashes (`—`) at or under about one per 100 words (never swap one for a period); no en dashes (`–`) between clauses or double dashes (`--`).
- [ ] No AI vocabulary cluster (3+ markers in one paragraph: leverage, fundamentally, significant, etc.).
- [ ] At least one odd-precision number with a named referent where the claim allows it.
- [ ] 3-5 sized hashtags (not 30), at the end or in the first comment.
- [ ] 0-3 emoji, placed with intent, none sprinkled.
- [ ] Carousel slide 1 promises and opens a loop; the last slide pays off + asks.
- [ ] Media supplied and within limits (JPEG/PNG/WebP, no mixed media, 2-10 slides).
- [ ] Close is a landing or a specific save/send ask, not "what do you think?".
- [ ] A clear primary goal (saves / shares / comments / follows), not all at once.
