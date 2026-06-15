---
name: comparator-grounded-estimate
description: Produce a comparator-anchored effort estimate — point value + low/high range + confidence + basis_note citing only relied-on comparator ids; widen when comparators are few, tighten when many agree; ships documentation-only until a real effort-actual table exists.
when_to_use: sizing effort for phase/release planning when a comparator dataset is available
output_kinds: [proposal]
deterministic_fallback: the mean-of-confirmed-actuals +/- range method
suggested_tier: sonnet
---

# comparator-grounded-estimate

> **SHIPS UNWIRED — READ THIS FIRST.**
> This skill is **documentation-only** until your organisation seeds a real
> effort-actual comparators dataset (confirmed past projects whose ACTUAL effort
> in person-days is known). With no dataset, the only honest output is an
> *ungrounded placeholder* with an empty basis — **never a fabricated number**.
>
> The sharpest documented failure in the parent system was a generative
> comparator agent inventing plausible past projects with fake effort numbers,
> feeding them into real estimate math, and stamping the result
> `confidence: high`. The discipline that prevents it is simple: an estimate is
> grounded **only** in confirmed historical actuals you can point to by id. Seed
> the comparators table (`references/comparators.template.csv` is the empty
> schema), confirm rows by a human, then wire the LLM step. Not before.

## Purpose

A comparator-anchored effort estimate for a phase, release, or wave: a single
point value (person-days) plus a low/high range that brackets it, a confidence
band, and a basis note that cites **only** the comparator ids actually relied on.
The estimate anchors on the ACTUAL effort of confirmed historical comparators —
real past projects whose effort is known — and treats those actuals as the
primary evidence. The range encodes uncertainty structurally: **widen it when
comparators are few, scattered, or only loosely similar; tighten it when many
close comparators agree.** When there are no comparators, the estimate is an
honest placeholder with an empty basis, and the note says so plainly.

This is a **proposal**, not a verdict. A human ratifies the estimate before it
drives any planning. The skill never asserts a "correct" number — it shows its
work (which comparators, why this confidence) so a human can accept, adjust, or
reject it.

## When to use

- Sizing effort for **phase / release / wave planning** (this skill feeds
  `describe-phases-releases-waves`), once you have a vision → derived
  requirements → assessed components view of the project.
- **Only when a comparators dataset is present.** If the dataset is empty, use
  the skill to produce the explicit ungrounded-placeholder output (so the gap is
  visible in planning) — do not improvise a number.

**Do NOT use it** to manufacture a number to satisfy a deadline, to estimate
from gut feel dressed up as evidence, or to invent comparators. No dataset, no
grounded estimate — that is the whole point.

## Inputs

The user supplies, as markdown / context:

1. **The thing being estimated** — a `title` and a `description` of the phase,
   release, or scope of work. Enough detail to judge similarity to past work.
2. **Confirmed comparators** — the rows from your seeded comparators dataset,
   each carrying at minimum: an `id` (integer, cited verbatim), a `name`, and an
   `actual_effort_days` (the known historical actual). Optionally a short
   similarity/notes field. See `references/comparators.template.csv` for the
   schema. **Only confirmed rows count** — a comparator without a human-confirmed
   actual is not evidence.

If the comparators list is empty or absent, the skill still runs — it returns the
ungrounded-placeholder result.

## The method (numbered steps)

The spine is deterministic; the LLM step refines it but never replaces the
evidentiary anchor.

### Step 1 — Gather confirmed comparators

Collect only comparators with a **confirmed actual_effort_days**. Discard any
row without one — it is not evidence, and using it would launder a guess into a
citation. Note each row's `id` (you will cite these verbatim) and its
`actual_effort_days`.

### Step 2 — Deterministic anchor (the spine, runs with no LLM)

This is the `deterministic_fallback` and it always runs first — it is the
honest floor under any LLM refinement.

- **If there are confirmed comparators:**
  - `point = mean(actual_effort_days of the relied-on confirmed comparators)`
  - `low / high = point − range / point + range`, where `range` reflects spread:
    a reasonable default is the larger of (a) the sample standard deviation of
    the relied-on actuals, or (b) a floor fraction of the point (e.g. ±25%) so a
    single-comparator estimate is never falsely precise. **Widen** the range
    when comparators are few, scattered, or loosely similar; **tighten** it when
    many close comparators agree.
  - Clamp `low` at 0 (effort is non-negative).
- **If there are NO confirmed comparators:**
  - Return an **ungrounded placeholder**: empty `basis_comparator_ids`, and a
    `basis_note` stating plainly that the estimate is an ungrounded placeholder
    with no comparators. Do **not** fabricate a point value — leave it null/blank
    or mark it explicitly as a placeholder. Stop here; the LLM step does not run.

This deterministic mean-of-confirmed-actuals ± range is publishable on its own.
It is what you ship while the LLM step is unwired.

### Step 3 — Pick confidence (deterministic heuristic, LLM may refine)

- `high` — many close comparators that agree tightly.
- `medium` — a few comparators, or some spread.
- `low` — one or two comparators, or wide divergence among them.
- (no comparators → not a confidence band at all; it is an ungrounded
  placeholder, said plainly.)

### Step 4 — LLM refinement (ONLY when a comparators dataset is present)

When confirmed comparators exist, an LLM may refine the anchor — choosing *which*
comparators are genuinely similar (and therefore relied upon), adjusting the
point within the comparator envelope, and shaping the range and confidence. The
LLM **must not** invent comparators, ids, or figures not in the supplied list,
and **must not** widen confidence beyond what the agreement of the cited
comparators supports.

Use this prompt (provider-agnostic — runnable in any LLM workflow that reads
markdown). It is lifted from the parent system's `estimate.md` template, which is
the canonical wording:

```
You are a delivery estimator on an internal managed-services delivery team.
Produce a single effort estimate (in person-days) for the project below,
grounded in the CONFIRMED historical comparators provided. These comparators are
past projects whose ACTUAL effort is known — treat their actuals as your primary
evidence and do not invent projects, ids, or figures that are not listed.

PROJECT: <title>

DESCRIPTION:
<description>

CONFIRMED COMPARATORS (each line: [id] name — actual_effort_days person-days):
<comparators_block>

Estimate the effort as a point value plus a low/high range that brackets it.
Anchor the point value on the comparators' actual effort; widen the range when
comparators are few, scattered, or only loosely similar, and tighten it when many
close comparators agree.

Set "confidence" to exactly one of: "low", "medium", "high" — higher when more
comparators agree closely, lower when there are few or divergent comparators.

In "basis_comparator_ids", list ONLY the integer ids of comparators above that you
actually relied on (drawn verbatim from the [id] values). If the list of
comparators is empty, return an empty array and say so plainly in "basis_note".

In "basis_note", state in one or two sentences how the estimate was derived (which
comparators, why this confidence). If there are no comparators, the note must say
the estimate is an ungrounded placeholder.

Return ONLY a JSON object of exactly this shape, no prose, no markdown fence:
{
  "effort_days": 40.0,
  "low_days": 30.0,
  "high_days": 50.0,
  "confidence": "medium",
  "basis_comparator_ids": [12, 34],
  "basis_note": "Anchored on the mean actual effort of the two closest comparators ..."
}
```

### Step 5 — Sanity-check against the spine, then propose

Compare the LLM result against the Step 2 deterministic anchor. If the LLM point
sits outside the envelope of the cited comparators' actuals, or its
`basis_comparator_ids` contain any id not in the supplied list, **reject it and
fall back to the deterministic estimate** — the spine wins. Confirm `low ≤ point
≤ high`. Then render the output below as a proposal for a human to ratify.

## Output format

Return this markdown. Use the JSON object only where you need the machine-shaped
record (the parent system stored exactly these fields); the surrounding markdown
is what a human reads.

```markdown
## Effort estimate — <title>

| Field        | Value                              |
|--------------|------------------------------------|
| Point        | <effort_days> person-days          |
| Range        | <low_days> – <high_days> person-days |
| Confidence   | <low \| medium \| high>            |
| Relied on    | comparators <id, id, …> (verbatim) |

**Basis:** <one or two sentences: which comparators, why this confidence, how the
point and range were derived>

<!-- machine record (matches the parent system's stored shape) -->
```json
{
  "effort_days": 40.0,
  "low_days": 30.0,
  "high_days": 50.0,
  "confidence": "medium",
  "basis_comparator_ids": [12, 34],
  "basis_note": "Anchored on the mean actual effort of comparators 12 and 34, the two closest by scope; tightened range because both agree within a few days."
}
```

> Proposal only — ratify before this drives planning. Reject or send back and the
> estimate carries no weight.
```

### Concrete example — grounded

Inputs: a "Customer self-service portal" phase; confirmed comparators
`[12] Members area rebuild — 38d`, `[34] Claims self-service — 44d`,
`[51] Internal admin console — 90d` (judged only loosely similar).

```markdown
## Effort estimate — Customer self-service portal

| Field        | Value                              |
|--------------|------------------------------------|
| Point        | 41 person-days                     |
| Range        | 35 – 50 person-days                |
| Confidence   | medium                             |
| Relied on    | comparators 12, 34                 |

**Basis:** Anchored on the mean actual effort of comparators 12 and 34 (38d and
44d), the two closest self-service builds. Comparator 51 was excluded as only
loosely similar (internal, no customer auth), which is why it does not appear in
the relied-on ids. Range kept moderate (35–50) because only two comparators
agree; not tightened further.
```
```json
{
  "effort_days": 41.0,
  "low_days": 35.0,
  "high_days": 50.0,
  "confidence": "medium",
  "basis_comparator_ids": [12, 34],
  "basis_note": "Mean of comparators 12 (38d) and 34 (44d), the two closest self-service builds; 51 excluded as only loosely similar; medium confidence on two agreeing comparators."
}
```

### Concrete example — ungrounded (no comparators)

When the comparators list is empty, this is the **only** correct output:

```markdown
## Effort estimate — Customer self-service portal

| Field        | Value                              |
|--------------|------------------------------------|
| Point        | — (ungrounded placeholder)         |
| Range        | —                                  |
| Confidence   | n/a — no comparators               |
| Relied on    | none                               |

**Basis:** This is an ungrounded placeholder: there are no confirmed comparators
to anchor on, so no point value is given. Seed and confirm an effort-actual
comparators dataset to produce a grounded estimate.
```
```json
{
  "effort_days": null,
  "low_days": null,
  "high_days": null,
  "confidence": null,
  "basis_comparator_ids": [],
  "basis_note": "Ungrounded placeholder — no confirmed comparators; no number fabricated."
}
```

## Notes / anti-patterns

- **Never fabricate a number.** No comparators → ungrounded placeholder with an
  empty basis. A made-up point value stamped with confidence is the exact
  failure this skill exists to prevent.
- **Cite only what you relied on, verbatim.** `basis_comparator_ids` lists ids
  drawn exactly from the supplied list — never an id not present, never a
  comparator you did not actually use to anchor.
- **The deterministic spine wins ties.** If the LLM result drifts outside the
  cited comparators' envelope or cites an unknown id, fall back to the
  mean-of-confirmed-actuals ± range. The LLM refines; it does not override the
  evidence.
- **Range is honesty, not decoration.** Few/scattered/loose → wide. Many/close/
  agreeing → tight. A suspiciously narrow range off one comparator is false
  precision.
- **Confirmed only.** A comparator without a human-confirmed actual is not
  evidence. Similarity is judged against real scope, not keyword overlap.
- **Advisory, not a gate.** This produces a proposal a human ratifies. It does
  not block, approve, or enforce. It feeds `describe-phases-releases-waves` as an
  input to planning, nothing more.
- **Stays unwired by design** until a real effort-actual table exists. Shipping
  the deterministic spine + the honest-placeholder behaviour first, and wiring
  the LLM step last, is itself the safeguard — it guarantees there is a grounded
  floor before any model narrates over it.
