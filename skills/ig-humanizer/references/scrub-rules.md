# Scrub Rules (Instagram, V3, 2026-09)

Tiered catalogs the humanizer applies. Load this file when actually executing a
scrub. Two tiers: forensic (always on) and strict (default on), plus the
Instagram-format scrubs. V3: vocabulary is scored by **density per
paragraph**, not deleted per word. Em dashes are **capped** at about 1 per 100
words, not banned (29% of human captions use one). Forced rhythm is a tell,
not a fix. See SKILL.md "What changed in V3" for the evidence.

## Contents

- Density scoring (how every vocabulary rule is applied)
- FORENSIC tier (always on)
- STRICT tier (default on)
- Instagram-format scrubs (always apply)
- Pass 2 - Rhythm (anti-uniformity guard only)
- Pass 3 - Forbidden insertions (sincerity markers, hedges)
- Preserve these (user voice, do not scrub)

---

## Density scoring (how every vocabulary rule is applied)

The cluster principle: readers spot AI text from clusters of markers, not from
any single word. One "notably" in a paragraph is English. "Notably",
"comprehensive" and a nominalisation in the same paragraph is a signature.

```python
def score_paragraph(paragraph: str, markers: dict) -> dict:
    """Count marker hits per paragraph (or per carousel slide). Returns hits and the action to take."""
    hits = []
    for name, pattern in markers.items():
        for m in re.finditer(pattern, paragraph, flags=re.I):
            hits.append((name, m.group(0)))
    n = len(hits)
    always = [h for h in hits if h[0] in ("reveal_bridge", "neg_parallel", "sincerity_marker")]
    if n >= 3:
        action = "REWRITE_PARAGRAPH"   # 3+ markers = signal. Rewrite the paragraph, not word-by-word.
    elif always:
        action = "REPLACE"             # a reveal bridge / negative parallelism / sincerity marker is always scrubbed,
                                       # even when it shares the paragraph with one ordinary marker (checked BEFORE n == 2)
    elif n == 2:
        action = "FLAG_ONLY"           # 2 = borderline. Report it, leave the words: the audit allows 0-2 per unit.
    else:
        action = "LEAVE"               # a single common word is not a verdict
    return {"hits": hits, "count": n, "action": action}
```

Rules of application:
- Score forensic markers separately: one hit = delete, no density threshold.
- Caption-level counts also matter for two patterns: triads (3+ per caption =
  scrub down to the first natural one; one or two natural triads pass, the
  same threshold the audit uses) and standalone fragments (3+ per caption =
  merge back, see Pass 2).
- Never replace a word with a synonym from the same list. "Leverage" to
  "harness" is not a fix.
- When you rewrite a paragraph, rewrite it in the author's register
  (lowercase casual stays lowercase casual, their emoji stay), not in "plain"
  register. Plainness at uniform temperature is itself a fingerprint.

---

## FORENSIC tier (always on)

Real model leakage no human types. Delete or flag on sight.

| Pattern | Action |
|---|---|
| `oaicite`, `contentReference`, `turn0search0`, `attached_file`, `grok_card` | delete the marker |
| "As of my last update", "As of my knowledge cutoff", "I cannot browse" | delete the disclaimer line |
| `[Your Name]`, `[Brand]`, `[insert X here]`, `YYYY-MM-DD` template blanks | flag, ask the user to fill |
| Em dashes above the cap (see below) | replace the excess with a comma, colon, parentheses, or a rewrite; never a period |

### Em dash cap (about 1 per 100 words)

The character is not a tell: GPT-5.4 emits 1.43 em dashes per 1,000 words,
below the human 3.23, and 29% of human Instagram captions in our corpus use
one. A caption's em dash is never a tell on its own; a blanket ban
over-sterilises captions and zero dashes across a long caption is the tell of
someone trying to look human. What is still forensic is the old GPT-4 glue
habit: 3+ in a short caption.

```python
def em_dash_excess(text: str) -> int:
    """Return how many em dashes exceed the cap (~1 per 100 words, floor 1, ceiling 2 per caption).
    0 = leave every em dash alone. A carousel slide counts as its own unit with a cap of 1."""
    words = len(text.split())
    cap = max(1, min(2, round(words / 100)))
    return max(0, text.count("—") - cap)

# Replacement order for the EXCESS ones (keep the one doing the most work, usually the first):
#   1. comma            if the dash joins a clause to the main sentence
#   2. colon            if the dash introduces a reveal, a list, or a consequence
#   3. parentheses      if the dash pair wraps an aside
#   4. line break       Instagram-native: the aside gets its own line
#   5. rewrite          if none of the above reads naturally
# NEVER a period. "X. Y." from a split dash creates fragment stacking, which is a worse tell than the dash.
```

---

## STRICT tier (default on)

What expert human readers cite when they spot AI text (vocabulary 53%,
sentence structure 36%). All vocabulary and grammar lists go through
`score_paragraph()`; reveal bridges, negative parallelism and sincerity
markers are scrubbed on a single hit.

### Punctuation

- Curly quotes -> straight quotes.
- `--` -> a comma or a line break (not a period: a period here stacks fragments).
- En dash (`–`) between clauses -> a comma. Number ranges (7-9) stay.
- Em dashes are handled by `em_dash_excess()` above, not stripped.

### Vocabulary: durable 2026 markers (density-scored)

The 2023-24 list (delve, tapestry, realm) is decaying because humans now avoid
those words. The durable markers are common words LLMs over-select at 2-5x the
human rate across 2026 frontier models. They are ordinary English, so one per
paragraph is fine. Three in a paragraph is a signature.

| Marker | Preferred replacement when the paragraph is over threshold |
|---|---|
| significant | a number ("31% more saves", not "significant growth"; ask if none exists) |
| crucial | delete, or "the" |
| notably, particularly | delete |
| comprehensive, holistic | full |
| insight(s) | say what was learned |
| robust | solid (keep if a term of art) |
| leverage | use |
| foster | build |
| landscape | field |
| nuanced | specific |
| multifaceted | delete |
| streamline | simplify |
| elevate | lift |
| empower | help |
| utilize, harness | use |
| facilitate | help |
| unlock | open up |
| navigate (figurative) | handle |
| dive in / dive into | get into |
| seamless | smooth |
| ecosystem | space |

Filler adverbs (each counts as one marker; delete when over threshold):
fundamentally, essentially, ultimately, crucially, notably, particularly,
arguably, certainly, definitely, undoubtedly.

### Grammar markers (density-scored; the 2026 structural signature)

```python
GRAMMAR_MARKERS = {
    # Present-participial clause openers: 5.3x the human rate.
    # "Leveraging our data, we..." / "Building on this, ..." / lowercase-casual "leveraging our data, we..."
    "ing_opener": r"(?m)^[\s>*\-]*[A-Za-z][a-z]+ing\b[^.]{0,60},",
    # Nominalisations: verb-turned-noun that hides the actor. "the implementation of"
    "nominalisation": r"\bthe (\w+(?:tion|sion|ment|ance|ence|ization|isation)) of\b",
    # Stacked abstract nouns
    "abstract_stack": r"\b(alignment|transformation|optimization|innovation|efficiency|scalability|synergy)\b.{0,40}\b(alignment|transformation|optimization|innovation|efficiency|scalability|synergy)\b",
}
# Fix for ing_opener: put the actor first. "Leveraging our data, we cut churn" -> "we cut churn with our data."
# Fix for nominalisation: use the verb. "the implementation of the new flow" -> "when we shipped the new flow"
```

### 2026 model-idiom layer (density-scored)

Phrases that were human caption idiom in 2024 and are model idiom in 2026.
Each counts as one marker; "let that sink in" and "that's the real story" are
scrubbed on a single hit as closers.

```python
IDIOM_LAYER_2026 = [
    r"\bquietly\b",                          # "quietly shipped"
    r"(?m)^\w+ matters\.$",                  # "consistency matters." as a line
    r"\bcompound(s|ing)?\b",
    r"\ba signal\b|\bthe signal\b",
    r"\bthe work\b",
    r"\bbuilt different\b",
    r"\bload-bearing\b",
    r"\bdoing the heavy lifting\b",
    r"\blet that sink in\b",
    r"\bthat's the real story\b",
    r"\bmain character energy\b",
    r"\bsoft launch(ing)?\b(?! a product)",  # as a mood, not a product launch
]
```

### Reveal bridges (single hit = replace)

```python
REVEAL_BRIDGES = [
    (r"(?im)^the (result|outcome|answer|lesson|catch|kicker|truth)\?\s*", ""),   # "The result?"
    (r"(?i)\bit'?s not \w[^,.]{0,40}, it'?s \b", None),                          # "It's not X, it's Y" (rewrite as paired declaratives)
    (r"(?i)^stop \w[^,.]{0,40}\. start \b|^stop \w[^,.]{0,40}, start \b", None),  # "Stop X, start Y"
    (r"(?im)^here'?s (what|how|why|the thing)\b[^:.\n]{0,40}[:.]\s*", ""),      # "Here's what/how", "Here's the thing.."
    (r"(?im)^(plot twist|spoiler|the twist)[:?]\s*", ""),
    (r"(?im)^let'?s talk about\b[^.\n]{0,40}[.:]\s*", ""),                      # "Let's talk about.." opener
]
# Fix: delete the bridge and let the next sentence stand. It was the point anyway.
# Named 2026 tells on every reader list; measured reach-negative on LinkedIn (vendor data).
```

### Negative parallelism (single hit = rewrite)

Strip the "not X, but Y" / "it isn't about X, it's about Y" constructions and
every sibling form ("The question isn't X, it's Y", "This isn't X. This is
Y."). Rewrite as paired declaratives, not by auto-substitution, and flag for
the user since meaning preservation needs judgement. Zero human captions in
our corpus use one.

### Rule of three (strict at density; one natural triad is allowed)

Tricolon runs at 2x the expert-human rate across 2026 models. 23% of human
captions in our corpus contain one, so the tell is the stacked or perfectly
parallel triad, the hollow one, and the repeat, not the form.

```python
NO_NO_JUST = r"\b(no \w+)[,.] (no \w+)[,.] ((?:just|only) \w+)"   # "No X. No Y. Just Z." / "no X, no Y, just Z"

def detect_triads(text: str) -> list:
    patterns = [
        r"(\w+), (\w+),? and (\w+)",                       # word triplets
        r"(\w+ \w+), (\w+ \w+),? and (\w+ \w+)",           # short-phrase triplets
        r"(?m)^(\w+)\. (\w+)\. (\w+)\.$",                  # "Simple. Effective. Easy." (also a Pass 2 staccato hit)
        NO_NO_JUST,                                        # staged construction, never a natural triad (also a Pass 2 hit)
    ]
    return [m for p in patterns for m in re.finditer(p, text, flags=re.I)]

HOLLOW_ADJECTIVES = {"dynamic", "vibrant", "innovative", "faster", "cheaper", "better", "simple",
                     "effective", "easy", "bold", "clear", "focused", "scalable", "powerful", "aesthetic"}
ABSTRACT_NOUNS = {"growth", "impact", "value", "alignment", "innovation", "efficiency", "results", "success",
                  "clarity", "freedom", "scale", "momentum", "consistency", "mindset", "strategy", "vision"}

def hollow(t: "re.Match", text: str) -> bool:
    """A triad is hollow when its items are interchangeable: every item is an abstract adjective or an
    abstract noun, and none carries a receipt (a proper name, a number, a $ or %). Equal word counts are
    NOT a tell on their own: "Stripe invoices, Vercel logs, and GitHub alerts" is a natural concrete triad.
    Capitalization alone is never a receipt: a capital that opens a sentence ("Simple, effective, and easy",
    "Simple. Effective. Easy.") is sentence case, not a name. A name is a capital that does NOT open a sentence."""
    def opens_sentence(pos: int) -> bool:
        return re.search(r"(?:^|[.!?\n])\s*$", text[:pos]) is not None
    def has_receipt() -> bool:
        for g in range(1, t.lastindex + 1):
            pos = t.start(g)
            for w in t.group(g).split():
                if re.search(r"[0-9$%]", w):
                    return True
                if w[:1].isupper() and not opens_sentence(pos):
                    return True
                pos += len(w) + 1
        return False
    items = t.groups()
    all_abstract = all(x.lower().strip() in HOLLOW_ADJECTIVES or x.lower().strip() in ABSTRACT_NOUNS
                       or x.lower().split()[-1] in ABSTRACT_NOUNS for x in items)
    return (not has_receipt()) and all_abstract

def triad_action(triads: list, text: str) -> list:
    """Call once per caption with that caption's triads (from detect_triads(text)). Scrub any hollow triad on
    sight. Natural (concrete, non-interchangeable) triads are a density call, on the SAME threshold the audit
    uses: one or two pass; at 3+ triads in the caption scrub down to the FIRST natural one. Rewrite mode is
    never harsher than audit mode. Threads are not pooled: the threshold is per caption."""
    actions = []
    over_density = len(triads) >= 3
    kept_one = False
    for t in triads:
        staged = t.re.pattern == NO_NO_JUST          # "no X, no Y, just Z" is a staged tell in either punctuation, always rewritten
        if hollow(t, text) or staged or (over_density and kept_one):
            actions.append((t, "REWRITE_AS_TWO_OR_FOUR"))   # 2 items, or 4 with one that breaks the pattern
        else:
            actions.append((t, "LEAVE"))
            kept_one = True
    return actions
```

### Dead phrases (delete or rewrite)

- "in today's fast-paced world", "in the digital age", "in the age of AI"
- "at the end of the day"
- "game-changer", "deep dive", "level up", "next level", "must-have", "paradigm shift"
- "the world of {thing}"
- "the hard truth is" / "the uncomfortable reality is"

### Dead closers (rewrite to a landing or a specific ask)

- "What do you think?"
- "Thoughts?"
- "Double tap if you agree."
- "Tag 3 friends who need this."
- "Comment YES below."
- "Let that sink in."
- A one-word closing line ("Still.")

A save or send prompt that names a reason ("save this before your next
post") is not a dead closer; it is the CTA Instagram rewards.

### Emoji storms

- 4+ emoji in a caption, or emoji on every line: cut to 0-3 placed with intent.
- The 2024-25 AI emoji signature (rocket, sparkles, fire, 100, raised hands in
  a row) is scrubbed on a single hit as a set.
- The author's own 1-3 intentional emoji are voice and stay (see Preserve).

## Instagram-format scrubs (always apply)

- A hook that needs line 2 to make sense: rewrite so the first 125 chars stand
  alone.
- 6+ hashtags, or any mid-sentence: cut to a 3-5 sized set at the end or in the
  first comment (see `../../../references/hashtag-strategy.md`).
- A bare carousel slide-1 title: rewrite to a promise + open loop.
- A caption over 2,200 chars: tighten.
- On-image slide text: at most one em dash per slide, and only if it does real
  work; slides are short.

---

## Pass 2 - Rhythm (anti-uniformity guard only)

Replaces V2's "BREAK (force burstiness)". Detectors do not score burstiness
(GPTZero dropped it in 2023). Captions are mid-length, and on the platforms
where we have engagement data sentence-length variance is either neutral or a
negative (LinkedIn null; Threads uniform wins), so rhythm is not a reach
lever here. What readers do notice is machine-flat uniformity (structure =
36% of expert judgments) and, worse, staged variance: mechanical long/short
alternation is a learnable humanizer fingerprint. So: fix rhythm only where it
reads machine-flat, remove manufactured variance everywhere, never add
variance as a tactic.

```python
STACCATO_TELLS = [
    r"(?m)^\w+\.$",                                              # one-word line for drama: "Still." "Exactly."
    r"(?m)^(\w+\. ){2,}\w+\.$",                                  # "Short. Punchy. Done." / "Simple. Effective. Easy."
    r"(?i)\bno \w+\. no \w+\. (just|only) \w+",                  # "No X. No Y. Just Z."
    r"(?i)\ball (of )?the \w+\. none of the \w+",                # "All the X. None of the Y."
    r"(?im)^the (result|outcome|answer|lesson|catch|kicker|truth)\?",  # "The result?" reveal (also a strict reveal bridge)
    r"(?i)\b(why|how|what happened)\? (because|simple|easy)\b",  # pseudo-Socratic Q&A
    r"(?i)\b(that's it|that's all|that's the post|full stop|period)\.$",
]

def is_standalone_fragment(s: str) -> bool:
    """A fragment is a short line with no subject + finite verb: "Still.", "Exactly.", "No excuses.",
    "Every single time." A short complete sentence ("It worked.", "Sales rose.") is not a fragment and
    never counts toward the cap; short is not the tell, fragment-for-drama is."""
    return len(s.split()) < 4 and not has_subject_and_verb(s)

def restore_rhythm(text: str) -> str:
    """V3. Remove staged variance; un-flatten only what reads machine-flat. Never manufacture variance."""
    paragraphs = split_paragraphs(text)
    fragments_seen = 0

    for i, p in enumerate(paragraphs):
        # 1. Kill staged rhythm first. Merge staccato runs into one full sentence with a real clause.
        for pat in STACCATO_TELLS:
            if re.search(pat, p):
                p = merge_into_sentence(p, pat)     # "No filters. No presets. Just light." -> "no filters or presets, just the light from the window."

        sents = split_sentences(p)
        lengths = [len(s.split()) for s in sents]

        # 2. Cap standalone fragments at 2 per CAPTION, not per paragraph. Only true fragments count;
        #    "It worked. Sales rose. Customers returned." is three short sentences, not three fragments.
        for j, s in enumerate(sents):
            if is_standalone_fragment(s):
                fragments_seen += 1
                if fragments_seen > 2:
                    sents[j] = attach_to_neighbor(sents, j)   # fold into the previous sentence with a comma or colon

        # 3. Un-flatten ONLY a machine-flat paragraph: 4+ sentences, every one within +-3 words of the
        #    mean, no subordinate clause anywhere. Then extend the ONE sentence that carries the most
        #    content by joining it to its natural neighbour with a clause that does work (because / which /
        #    when / after), not a comma splice. Once per paragraph, and only if the result reads like the
        #    author. A paragraph with one long and one short sentence is already fine.
        if len(sents) >= 4 and all(abs(n - mean(lengths)) <= 3 for n in lengths) and not any(has_working_clause(s) for s in sents):
            k = max(range(len(sents)), key=lambda j: lengths[j])
            j = k + 1 if k + 1 < len(sents) else k - 1
            sents[k] = join_with_clause(sents[k], sents[j])
            del sents[j]                              # the absorbed neighbour is removed so nothing appears twice

        # 4. Never long/short/long/short. If the paragraph now alternates (4+ sentences flipping between
        #    short <8 words and long >=16 words), fold the SECOND short sentence into the sentence before it.
        #    The seesaw is the humanizer fingerprint.
        lengths = [len(s.split()) for s in sents]
        if len(lengths) >= 4 and all((lengths[k] < 8) != (lengths[k + 1] < 8) for k in range(len(lengths) - 1)) \
                and all(n < 8 or n >= 16 for n in lengths):
            k = [j for j, n in enumerate(lengths) if n < 8][1]
            sents[k - 1] = join_with_clause(sents[k - 1], sents[k])
            del sents[k]

        # 5. One-idea-per-line captions (each paragraph one sentence) and carousel slides: leave rhythm alone entirely.

        paragraphs[i] = rejoin_keeping_breaks(p, sents)   # re-attach the paragraph's own single line breaks; the pass edits sentences, never breaks

    return "\n\n".join(paragraphs)
```

Layout vs rhythm: one-sentence lines with blank lines between them are
Instagram's native caption layout and are **not** touched by this pass. "I
grew an account from 0 to 10k in 4 months." on its own line is layout.
"Still." on its own line is fragment-for-drama. The pass edits sentences,
never the line breaks.

## Pass 3 - Forbidden insertions (sincerity markers, hedges)

Pass 3 adds concreteness only (a referenced odd-precision number, a named
entity, a flat dated fact). It never adds these, and Pass 1 strict removes them
when the draft already has them as an opener or pivot:

```python
SINCERITY_MARKERS = [
    # Anchored to a line start OR a sentence boundary, so a same-line pivot ("The launch failed. Real talk, this hurt.") is caught too.
    r"(?im)(?:^|(?<=[.!?]\s))(let me be (honest|real|direct|clear)|i'?ll be (honest|real|direct)|honestly\?|honest (caveat|version|answer)|the honest (version|answer|truth) is|to be (direct|honest|fair|transparent)|real talk|full transparency|can i be (honest|vulnerable)|i'?ll say the quiet part|not gonna lie|ngl|unpopular opinion|storytime)[:,.]?\s*",
    r"(?im)(?:^|(?<=[.!?]\s))pov:\s*(?!.*\b(you|your)\b)",   # "POV:" on something that is not a point of view
    r"(?i)\b(i (might|may|could) be wrong,? but|perhaps|it seems (to me )?that|in my humble opinion|i think it'?s fair to say)\b",  # inserted hedges: only scrub if NOT in the author's voice samples
]
# Fix: delete the marker and keep the sentence that follows. If the sentence that follows is not
# a specific fact, the marker was doing the work of vulnerability. Ask the author for the fact.
# Evidence: performed hesitancy 2x more common in LLM than expert human text; "false vulnerability"
# is a named 2026 tell. The rule is: never manufacture one, and never wrap a fact in one.
```

## Preserve these (user voice, do not scrub)

- Lowercase-casual register if that is how the user captions
- `..` as a soft pause and single line breaks as beats
- One or two sentence fragments used intentionally ("every time.") - the cap
  is 2 per caption, not 0
- One em dash per ~100 words. Do not push the count to zero; 29% of human
  captions have one and zero across a long caption is below the human baseline
- One natural rule-of-three with concrete, non-interchangeable items (23% of
  human captions have one)
- One genuinely long sentence per paragraph, even if a style guide would split it
- The author's 1-3 intentional emoji
- Contractions (don't, it's, you're)
- Specific numbers with referents and named entities (add MORE, never remove)
- First-person sensory details
- The author's reactions and opinions, including a blunt one. Flat tone across
  a whole caption is a humanizer fingerprint
- A single common-word marker in a paragraph ("notably", "robust" as a term
  of art). One is not a verdict
- Their actual story. Never invent a detail to make a caption land
