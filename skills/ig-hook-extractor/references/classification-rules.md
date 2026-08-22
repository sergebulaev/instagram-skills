# Hook Classification Rules (Instagram)

Feature extraction and scoring heuristics `ig-hook-extractor` uses to map a post
to one of the 10 formulas in `../../../references/hook-formulas.md`.

## Step 1: detect the surface

| Signal | Surface |
|---|---|
| One photo + a caption | single image (look at IG1-IG4) |
| 2-10 stacked images, swipe dots | carousel (look at IG5-IG8) |
| Video, vertical, audio | Reel (look at IG9-IG10) |

The URL helps: `/reel/` is a Reel; `/p/` is a single image or a carousel (the
caret/dots in the app distinguish them, so ask the user).

## Step 2: extract hook features

### Caption hooks (first ~125 chars)

| Feature in the first line | Formula |
|---|---|
| An odd-precision number + a "steal this / here is how" promise | IG1 Number-First Result |
| A flat claim that contradicts common advice | IG2 Contrarian Truth |
| A specific shared moment, no setup, no number | IG3 Relatable Cold-Open |
| A first-person time marker + an admitted cost or surprise | IG4 Mini-Story Confession |

### Carousel hooks (slide 1 + structure)

| Feature | Formula |
|---|---|
| Slide 1 promises N numbered items; body is one item per slide | IG5 Listicle |
| Slide 1 shows an "after"; slide 2 the "before"; body is steps | IG6 Before/After |
| Body slides pair "Myth:" with "Truth:" | IG7 Myth-Buster |
| Slide 1 names a framework; last slide summarizes it on one slide | IG8 Steal-This Framework |

### Reel hooks (first 1-3 seconds)

| Feature | Formula |
|---|---|
| A pattern interrupt / open-loop on-screen text, no slow intro | IG9 Pattern-Interrupt |
| "How I {result} in {timeframe}" + labeled steps | IG10 How-I Teardown |

## Step 3: score confidence

- **High (0.8+):** the hook matches one formula's skeleton cleanly and the body
  follows its structure.
- **Medium (0.5-0.8):** the hook fits but the body is loose, or two formulas
  overlap (common: IG1 and IG10 both use a result + steps). Return the top 2.
- **Low (under 0.5):** no clean match. Describe the structure literally and
  suggest the closest formula as a starting point.

When two fit, the tiebreaker is the **primary goal** (below) and the surface: a
caption-only result is IG1, the same result as a Reel with steps is IG10.

## Step 4: name the primary goal

Infer what the original optimized for from its structure and close:

| Close / structure | Likely goal |
|---|---|
| "save this", a list, a framework, a how-to | saves |
| "send this to..", a contrarian or myth payoff | shares |
| a relatable moment, a question, a confession | comments |
| proof of transformation, "follow for.." | follows |

## Step 5: build the blank template

Copy the matched formula's skeleton from `hook-formulas.md`, keep its slot
structure, and relabel the slots to the user's topic. Strip any AI tells the
original had (do not propagate em dashes or a 30-hashtag block into the template).

## Step 6: audit the source

Flag, so the user does not copy them:
- em dashes / en dashes
- AI vocabulary (leverage, fundamentally, delve, elevate)
- 20-30 hashtags crammed at the top
- engagement bait ("comment YES", "tag 3 friends")
- a hook that only makes sense after the "more" fold
