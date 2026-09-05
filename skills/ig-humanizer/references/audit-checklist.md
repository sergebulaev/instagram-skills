# Pre-Publish Audit Checklist (Instagram)

The thresholds the `--mode audit` pass applies. Mirror of the root
`references/algorithm-heuristics.md` checklist, with the humanizer's blocker
distinctions. V3 (2026-09): AI tells are scored by density per paragraph; em
dashes are capped at about 1 per 100 words, not banned (29% of human captions
use one); forced rhythm is a tell.

## Blockers (auto-fail)

- [ ] Em dashes (`—`) at or under about 1 per 100 words (1-2 per caption; at
      most one per carousel slide). A single em dash is never a blocker. No en
      dash (`–`) between clauses, no double dash (`--`).
- [ ] The first 125 chars stand alone as a hook (the "more" fold cuts the rest).
- [ ] Caption within 2,200 chars.
- [ ] 3-5 sized hashtags, not 20-30, never mid-sentence.
- [ ] No engagement bait ("comment YES", "tag 3 friends", "double tap if").
- [ ] No "In today's fast-paced world" or equivalent opener; no reveal-bridge
      opener ("Here's the thing..", "Let's talk about..", "Stop X, start Y");
      no sincerity announcement opener ("real talk", "not gonna lie", "POV:"
      on something that is not a POV).
- [ ] No "What do you think?" / "Thoughts?" / "Let that sink in." dead closer
      (a save or send prompt with a reason is fine and wanted).
- [ ] No paragraph with 3+ vocabulary / grammar markers (one marker per
      paragraph is fine); no "It's not X, it's Y" negative parallelism; no
      "The result?" reveal bridge.
- [ ] Carousel: all images or all video (no mixed media), 2-10 slides.
- [ ] A media plan exists (Instagram rejects text-only posts).

## Warnings (flag with fix)

- [ ] Hashtag set is sized (2-3 niche, 1-2 mid, 0-1 broad), not all-broad.
- [ ] 0-3 emoji, placed with intent, none sprinkled; no rocket/sparkles/fire
      signature run.
- [ ] No paragraph reads machine-flat (4+ sentences all the same length, no
      clause doing work). Flag that paragraph only; never suggest adding
      variance as a tactic. One-idea-per-line layout is fine.
- [ ] No staccato stacks ("Short. Punchy. Done.", "No X. No Y. Just Z."),
      no one-word lines for drama, at most 2 standalone fragments in the
      caption, no long/short/long/short seesaw.
- [ ] At least one odd-precision number WITH a named referent where the claim
      allows (a bare number does not clear this).
- [ ] At least one named entity.
- [ ] At most one natural rule-of-three; no stacked or perfectly parallel
      triads, no hollow triads without concrete items, never 3+ in a caption.
- [ ] No hedging stack ("perhaps", "it seems", "I might be wrong but") and no
      framed confession ("real talk, this hurt: ..."). A flat dated fact is
      fine.
- [ ] Only when auditing a humanizer rewrite with the original in hand, not a fresh draft: not over-scrubbed, i.e. the author's tone, reactions, lowercase register, one
      em dash, one natural triad and their intentional emoji survived.
- [ ] Carousel slide 1 promises + opens a loop, not a bare title.
- [ ] Strongest carousel point is front-loaded (slide 2-3), not buried last.
- [ ] One clear primary goal (saves / shares / comments / follows).
- [ ] One CTA, not three; it names a reason.

## Thresholds quick reference

| Metric | Limit |
|---|---|
| Caption | 2,200 chars (hook in first ~125) |
| Hashtags | 3-5 sized (30 is the hard cap but spammy) |
| Emoji per caption | 0-3 |
| Em dashes | about 1 per 100 words (1-2 per caption; 1 per slide) |
| Vocabulary / grammar markers per paragraph | 0-2 |
| Standalone fragments | 2 per caption |
| Carousel slides | 2-10 |
| Reel duration | up to 3 min; 5-90s for the Reels tab |
| Aspect ratio | 4:5 to 1.91:1 |

## Scoring

- Any blocker -> **FAIL**, return fixes, offer auto-rewrite via `ig-humanizer`.
- No blockers, any warnings -> **PASS with warnings**, list each with a fix.
- Clean -> **PASS**, add the timing note, the surface sanity check, and the
  media reminder.
- Report per-paragraph tell density (markers, em dashes per 100 words,
  fragments, triads). Do not estimate a detector score: on caption-length
  text those are noise and this skill does not promise to beat them.
