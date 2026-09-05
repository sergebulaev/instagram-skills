# Instagram Post Audit

Run any caption (and its carousel slide text) through the 2026 Instagram ranking
checklist. Catches AI tells, format violations (first-125 hook, caption length,
hashtag sizing, emoji), reach suppressors (engagement bait, mixed media), and
structural weaknesses before publishing. This is the `ig-humanizer --mode audit`
workflow: detection only, no rewrite.

## When to use

- Before publishing a hand-written or AI-drafted caption or carousel
- When `ig-caption-writer` or `ig-carousel-planner` finishes a draft (auto-invoked)
- When a recent post underperformed and the user wants a post-mortem

## Input

- A caption, and for a carousel the slide text
- Optional: target audience, scheduled time, the surface (image / carousel / Reel)

## Output

- **Pass / Fail** header
- **Blockers** (must fix before publishing): em dash density over the cap,
  paragraphs at 3+ AI markers, reveal bridges, a sincerity announcement as
  the opener, engagement bait, a hook that spills past the fold, hashtag walls
- **Warnings** (ship-risky): staccato stacks, sincerity markers or hedges
  mid-caption (as the opener they are a blocker), missing referenced numbers,
  generic CTA
- **Suggested fixes** for each issue
- **Per-paragraph tell density** (markers, em dashes per 100 words,
  fragments, triads). No detector score: on caption-length text those are
  noise and the skill does not promise to beat them
- **Timing recommendation** given the audience

## Checks

### Blockers (auto-fail)

1. Em dash density above about 1 per 100 words (1-2 per caption; more than
   one on a carousel slide); en dash between clauses; double dash. A single em
   dash is not a blocker.
2. The hook needs the second line to make sense (the first 125 chars do not
   stand alone).
3. Caption over 2,200 chars.
4. 20-30 hashtags, or hashtags mid-sentence.
5. Engagement bait ("comment YES", "tag 3 friends", "double tap if you agree").
6. Opens with "In today's fast-paced world" or similar, a reveal bridge
   ("Here's the thing..", "Let's talk about..", "Stop X, start Y"), or a
   sincerity announcement ("real talk", "not gonna lie", "POV:" on something
   that is not a POV).
7. Ends with "What do you think?", "Thoughts?", or "Let that sink in." (a
   save/send prompt with a reason is fine).
8. Any paragraph with 3+ vocabulary / grammar markers, or any
   negative-parallelism / "The result?" reveal bridge (see
   `../references/scrub-rules.md`).
9. Carousel mixes images and video, or has more than 10 slides.
10. No media plan (Instagram rejects text-only posts).

### Warnings (flag with a suggested fix)

11. More than 5 hashtags, or an all-broad set a small account cannot rank in.
12. 4+ emoji, emoji sprinkled through every line, or the rocket/sparkles/fire
    signature run.
13. A paragraph that reads machine-flat (4+ sentences all the same length, no
    clause doing work). Flag that paragraph only; never suggest adding
    variance as a tactic. One-idea-per-line layout is fine.
13a. Staccato stacks ("Short. Punchy. Done.", "No X. No Y. Just Z."), one-word
    lines for drama, more than 2 standalone fragments, or a long/short/long/
    short seesaw.
14. No odd-precision number with a named referent anywhere the claim would
    allow one (a bare number does not clear this).
15. No named entity (person, brand, tool).
16. Stacked or perfectly parallel rule-of-three, a hollow triad without
    concrete items, or 3+ triads in the caption (one natural triad passes).
16a. Hedging stack ("perhaps", "it seems") or a sincerity marker / framed
    confession mid-caption ("real talk, this hurt: ..."); the same marker as
    the opener is blocker 6. A flat dated fact is fine.
16b. Over-scrubbed (only when auditing a humanizer rewrite with the original in hand to compare against; a fresh draft that never had an em dash or a triad is not over-scrubbed): uniformly flat tone, every em dash and triad gone from a
    long caption, the author's emoji or lowercase register gone, no reaction
    or opinion anywhere.
17. Carousel slide 1 is a bare title, not a promise + open loop.
18. The strongest carousel point is buried on the last body slide.
19. No clear primary goal: the draft chases saves, shares, comments, and follows
    all at once. Pick one (see `../../../references/hook-formulas.md`
    "Engagement-goal split").
20. CTA is generic or there are three competing CTAs.

### Info (neutral notes)

21. Suggested posting window given the audience.
22. Surface recommendation (single image vs carousel vs Reel) given the material.
23. Save/send opportunity: if the draft is a list/framework/how-to, note that it
    should be structured to maximize saves; if it is a contrarian/myth payoff,
    structure it to maximize sends.

## Steps

1. Detect the surface: single image, carousel, or Reel.
2. Measure the caption: char count, where the first 125 chars cut, hashtag count
   and sizing, emoji count, em dashes per 100 words.
3. Run the blocker checks. If any fail, return **FAIL** with specific fixes;
   optionally offer to hand off to `ig-humanizer` for an auto-rewrite.
4. If no blockers, run the warnings.
5. Report per-paragraph tell density. Do not estimate a detector score.
6. Return the structured report with a timing note and a media reminder.

## Related

- `ig-humanizer` - proportional rewrite if the audit fails
- `ig-caption-writer` / `ig-carousel-planner` - regenerate using a proven formula
