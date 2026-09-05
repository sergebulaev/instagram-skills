# Hashtag Sourcing Tactics

How `ig-hashtag-strategist` finds and sizes candidate tags. Pairs with the full
model in `../../../references/hashtag-strategy.md`.

## Finding niche tags (the workhorses)

Niche tags (under 50k posts) are where a small or mid account ranks and stays
visible for hours. Sources:

- **Combine two words:** topic + audience (`#notionforfreelancers`), topic +
  format (`#carouseldesign`), topic + style (`#uglyfoodphotography`).
- **Community names:** what the people in your exact world call themselves
  (`#bootstrappedsaas`, `#filmphotographycommunity`).
- **The creators you admire:** the smaller tags they actually rank in (not the
  giant ones in their first line).
- **Instagram search autocomplete:** type the topic and read the suggested tags
  with their post counts; the ones under ~50k are your niche slots.

## Finding mid tags (the extenders)

Mid tags (50k-500k) name a recognizable sub-topic: `#contentstrategy`,
`#indiehacker`, `#filmphotography`. They extend reach to a warm audience without
being unwinnable. One or two per post.

## The broad slot (optional)

Broad tags (500k+) are single common words: `#marketing`, `#fitness`, `#food`.
They rank for minutes, so treat them as a category label. Use at most one, and
only if it genuinely fits. Skip it rather than force it.

## Sizing without the API

The publishing API does not expose tag post counts. Size by:

1. **Specificity heuristic:** the more specific and combined, the more niche. A
   single common word is broad.
2. **In-app verification:** tell the user to check the count Instagram shows in
   search for the borderline tags.

## Tags to drop on sight

- Engagement-farm tags: `#follow4follow`, `#like4like`, `#followforfollowback`.
- Anything that cycles through flagged/banned status (generic spammy tags).
- Popular-but-off-topic tags. A mismatch trains the recommendation engine to
  show the post to the wrong audience, which lowers engagement rate and reach.

## Rotation

Do not reuse one 5-tag block on every post. Identical sets across many posts read
as automation. Rotate the niche tags to match each post's specific topic; the mid
and broad slots can stay more stable within a content pillar.
