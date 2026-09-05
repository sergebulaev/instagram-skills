# Carousel Slide Architecture

Per-formula slide spines and the on-image text rules `ig-carousel-planner` uses.
A carousel is 2-10 slides (API limit; the native app allows 20). Design for the
portrait 4:5 frame, which fills the most screen.

## The universal spine

| Slide | Role | On-image text |
|---|---|---|
| 1 (hook) | promise + open loop | one big idea, 6-12 words, a number if it fits |
| 2 | strongest value | the best single point, front-loaded |
| 3 to N-1 | one point each | short, stands alone, readable in 2 seconds |
| N (payoff) | saveable summary + one ask | the recap on one slide, then save/follow |

Swipe-through decays with depth, so the order of value matters more than the
count. Put the best point on slide 2 or 3, never on slide 10.

## On-image text rules

- **One idea per slide.** If a slide needs two thoughts, split it.
- **Readable in 2 seconds.** Big text, few words. The slide is a billboard, not
  a paragraph. Detail goes in the caption.
- **Number the slides** when the format is a list (slide 2 = "1.", etc.) so the
  open loop ("most miss #4") pays off.
- **Visual consistency.** Same font, same margins, same accent color across
  slides so it reads as one set.
- **Em dashes capped at one per slide** in on-image text, and only when it
  does real work (a slide rarely needs one). The character is not a tell in
  2026; a slide glued together by dashes is. Replace the excess with a colon
  or a line break, never a period.

## IG5 - Listicle Carousel (goal: saves)

```
Slide 1: {N} {things} that {payoff}. (most miss #{k})
Slide 2: 1. {item} + one concrete example
Slide 3: 2. {item} + example
...
Slide N-1: {N}. {item} + example
Slide N: the list recapped on one slide + "save this so you use it"
```

Put the most surprising item at position 1 or 2 in the list, not last.

## IG6 - Before/After Transformation (goal: saves, follows)

```
Slide 1: {the after, with a number or a striking visual}
Slide 2: where it started (the before) - the open loop is the gap
Slide 3 to N-1: the exact steps, one per slide
Slide N: the result restated + "follow for the full {topic} system"
```

The before/after gap between slides 1 and 2 is the swipe driver. Steps must be
concrete enough to do tomorrow.

## IG7 - Myth-Buster (goal: shares)

```
Slide 1: {N} {topic} myths costing you {specific loss}
Slide 2 to N-1: "Myth: {belief}" then "Truth: {what works}"
Slide N: the reframe in one line + "send this to someone who still believes #1"
```

The send prompt on the last slide is the whole point; myth-busters get sent.

## IG8 - Steal-This Framework (goal: saves)

```
Slide 1: the {named} framework I use to {result}
Slide 2 to N-1: one part of the framework per slide, with the why
Slide N: the whole framework on one slide (the save-bait artifact) + save prompt
```

The single-slide summary is what people save. Make it self-contained.

## Slide count guidance

| Content | Slides |
|---|---|
| A tight list or framework | 6-8 |
| A richer teaching set or transformation | 8-10 |
| Fewer than 4 real points | post as a single image instead |

Never pad to 10. A 5-point idea is a 5-point carousel (7 slides with hook and
payoff), not a padded 10.

## Caption pairing

The caption can be short for a carousel because the slides carry the payload. It
should: restate the hook for the "more" fold, add one line of context, carry the
CTA, and hold the 3-5 sized hashtags. See `../../references/hashtag-strategy.md`.
