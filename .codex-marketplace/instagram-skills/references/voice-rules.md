# Voice Rules for Instagram

These are the canonical voice rules for the whole bundle. Every skill inherits
them. Skill-local "Hard rules" sections only add format-specific overrides
(caption length, slide counts, hashtag sizing) and point back here.

## Hard rules

1. **Em dashes (`—`) capped at about 1 per 100 words** (1-2 per caption, at
   most 1 per carousel slide). The character is no longer a tell (2026 models
   use fewer than humans, and 29% of human captions in our corpus contain one);
   the density is. Replace the excess with a comma, colon, parentheses or a
   line break, never a period. No en dashes (`–`) between clauses, no double
   dashes (`--`).
2. **Use `..` or a line break** as a soft pause when you would reach for a
   second em dash. Reads human and matches how people actually caption on
   Instagram.
3. **Capitalize personal names, company names, product names** (Stripe, Canva,
   Figma). Lowercase a brand name and it reads as careless.
4. **Sentence starts can be lowercase.** Lowercase openers are native to the
   Instagram caption register. Names inside are always capitalized.
5. **Specific numbers beat adjectives.** "saved 11 hours a week" beats "saved
   tons of time". "$4,200 in 30 days" beats "made good money".
6. **One idea per caption.** A caption that argues three points reads as a blog
   post. Pick the one that earns the save.
7. **Don't hard-sell.** Instagram buries overtly promotional captions. Teach or
   tell a story, then point to the next step once.

## Vocabulary markers (density-scored)

Count these per paragraph. One is English; two is borderline (flag it in the report, leave the words);
three in one paragraph reads as AI and the whole paragraph gets rewritten (see `ig-humanizer` V3).
The durable 2026 set (significant, crucial, notably, particularly,
comprehensive, insights, robust, leverage, foster, landscape, nuanced,
streamline, elevate, empower) counts alongside the older corporate words:
- leverage, utilize, facilitate, streamline, robust, seamless, delve, navigate,
  unlock, harness, foster, cultivate, elevate, empower, dive in
- fundamentally, essentially, ultimately, crucially, notably
- landscape, ecosystem, paradigm, realm, tapestry, journey

## Always forbidden (single hit, regardless of density)

These are scrubbed on sight. They are reveal bridges, negative parallelism,
dead phrases or performed sincerity, not vocabulary:
- "It's not just X, it's Y"
- "In today's fast-paced world", "in the digital age"
- "game-changer", "deep dive", "level up", "next level", "must-have"
- "link in bio" used as filler (only when there is a real link and a real reason)
- Sincerity announcements as an opener or pivot: "let me be honest", "I'll be
  real", "honestly?", "real talk", "not gonna lie", "unpopular opinion:" on a
  take that is actually popular. State the fact flat instead.

## Instagram-native style

- **The first line is the whole job.** Instagram hides everything after ~125
  characters behind "more". If line 1 does not earn the tap, the rest is unread.
- **Line breaks are punctuation.** White space between short lines controls
  pacing and makes a caption skimmable. A wall of text gets scrolled past.
- **Emoji are part of the register, used with restraint.** 0-3 in a caption,
  placed to break up text or mark a list, never sprinkled. A caption dusted with
  12 emoji reads as a spam account or AI.
- **Hashtags are sizing, not volume.** 3-5 well-sized tags beat 30 random ones
  in 2026 (see `hashtag-strategy.md`). Put them at the end of the caption or in
  the first comment, never mid-sentence.

## Length

- **Caption cap: 2,200 characters.** Only the first ~125 show before "more", so
  front-load the hook. Most strong captions land between 150 and 1,500 chars;
  long is fine when it teaches or tells a story worth the scroll.
- **A carousel caption can be short** because the slides carry the payload. A
  single-image post leans harder on the caption.
- **Reels caption: keep it tight.** The video is the hook; the caption adds
  context and the save/share reason in a line or two.

## Structure

- **Front-load the hook** into the first line (before the fold). State the
  payoff, the tension, or the number up front.
- **End on a landing, not a dead prompt.** "What do you think?" is dead. A
  specific question, a save prompt that names the reason ("save this for your
  next launch"), or a sharp closing line all beat it.
- **Carousels:** slide 1 is the hook, the last slide is the payoff plus the
  save/follow ask. See `hook-formulas.md` and the carousel planner.

## Anti-patterns

- Caption that restates the obvious ("Marketing is so important these days").
- Generic engagement bait ("double tap if you agree", "comment YES").
- Overused openers: "Let's talk about..", "Here's the thing..", "POV:" on
  something that is not a POV.
- Stacked or hollow rule of three ("faster, cheaper, better"); one natural
  triple with concrete items is fine.
- A first line that needs line 2 to make sense (the fold eats it).
- 20+ hashtags stuffed at the top of the caption.
- ALL CAPS lines for intensity. Carry intensity with word choice.

## Algorithmic note

Instagram's 2026 ranking leans on **sends per reach** (shares to friends and to
your own story) and **saves** as the strongest signals that content is worth
spreading, ahead of likes. Before posting, check: does this give a viewer a
reason to send it to one specific friend, or to save it for later? If it only
earns a passive like, sharpen it.
