---
name: classify-requirements
description: Annotate each requirement with layer / stated_as (need|solution|constraint|symptom) / quantified / value_outcome and a need-shaped rewrite only when solution-shaped. Use after requirements exist, to surface solutioneering, unmeasurability and value-orphans before the red-team. Idempotent and advisory.
when_to_use: after requirements exist, to surface solutioneering, unmeasurability and value-orphans before the red-team
output_kinds: [proposal]
deterministic_fallback: the keyword/precedence tables as an optional backstop
suggested_tier: sonnet
---

# classify-requirements — annotate the shape of each requirement

## Purpose

Describe the *shape* of each requirement so a human can see it at a glance. For every requirement you emit five fields: `layer`, `stated_as`, `quantified`, `value_outcome`, and a `suggested_rewrite` (only when the requirement is solution-shaped).

This skill is **advisory and non-destructive**. It describes; it never decides. It does **not** change a requirement's status, source, version, ID, or wording. It only attaches annotations alongside the existing text. A human reads the annotations and chooses what to act on.

The point is to make three failure modes jump off the page *before* the red-team runs:

- **Solutioneering** — a requirement that names a mechanism/product instead of the underlying need (`stated_as = solution`).
- **Unmeasurability** — a requirement with no number/target, so you can't tell when it's met (`quantified = false`).
- **Value-orphans** — a requirement that serves no nameable business outcome (`value_outcome = null`).

## When to use

After requirements exist (captured, elicited, or derived) and before the red-team pass. Run it whenever the requirement set changes and you want a quick read on its shape. Re-run freely — it is idempotent.

## Inputs

The user supplies, as markdown or plain context:

- **Project title** — one line.
- **Project context** — a short paragraph of what the project is and what it's for. This grounds the `value_outcome` inference and the business-vs-technical `layer` call.
- **Requirements to classify** — a list, each row carrying a stable identifier and the requirement text. Reference each row by its real identifier; do not renumber, merge, skip, or duplicate.

Example input block:

```
PROJECT TITLE: Field-service scheduling uplift
PROJECT CONTEXT: Dispatchers hand-build daily routes in a spreadsheet; the
business wants faster, more consistent scheduling and an audit trail of changes.

REQUIREMENTS:
  7  | The system shall use Power Automate to route approval requests.
  8  | A dispatcher must be able to publish a day's routes in under 30 seconds.
  9  | The current process is too slow and dispatchers complain.
 10  | Customer data must remain within the AU region.
```

## The method

The LLM reasoning step **is** the method. The deterministic keyword/precedence tables (Step 5) are an optional backstop for offline runs and a sanity check — not the primary classifier. Run the steps in order, per requirement.

### Step 1 — `layer`: business or technical

Exactly one of `business` or `technical`.

- `technical` when the text names a technical concern, mechanism, or system tier (a database, an API tier, encryption, a framework, a data store, TLS, schema/migration, etc.).
- `business` otherwise — the default.

### Step 2 — `stated_as`: need | solution | constraint | symptom

Exactly one of these four. When more than one could apply, resolve by this precedence (highest wins):

> **solution > constraint > symptom > need**

One-line definitions:

- **solution** — names an implementation, mechanism, or product. This is solutioneering: the *how* has leaked into the requirement.
- **constraint** — a boundary, prohibition, residency, or compliance rule ("must not…", "shall remain within…", data sovereignty, a regional boundary).
- **symptom** — describes a problem with no target or condition ("is slow", "users complain", "hard to use"). A pain, not a requirement.
- **need** — a clean statement of the underlying need. The default when none of the above fire.

Apply the precedence literally: if the text is *both* a constraint and a symptom, it is a constraint. If it names a mechanism *and* states a boundary, it is a solution.

### Step 3 — `quantified`: boolean

`true` when the text carries a number paired with a unit or target (`500 ms`, `99.9%`, `30 seconds`, `80% coverage`, `1000 users`, `5 days`). `false` when there is no measurable figure. A bare number with no unit/target does not count.

This flags unmeasurability: a `need`-shaped requirement with `quantified = false` is a candidate for a hard acceptance question at red-team.

### Step 4 — `value_outcome` and `suggested_rewrite`

- **`value_outcome`** — a SHORT display label (**≤ 4 words**) naming the business outcome the requirement serves, grounded in the project context (e.g. "Faster onboarding", "Regulatory compliance", "Audit trail"). Use `null` when no business outcome can be inferred — that is a value-orphan and is itself a useful signal.
- **`suggested_rewrite`** — a need-shaped rewrite that strips the mechanism and restates the underlying need. Provide this **only when `stated_as = solution`**. In every other case it MUST be `null`. The rewrite is a suggestion for the human; it does not overwrite the original text.

### Step 5 — Deterministic backstop (optional, NOT the primary method)

For offline runs, regression tests, or a quick cross-check, a pure keyword/precedence pass produces the same fields with no model call. It is a coarse fallback — the LLM step above is the real classifier. The tables and the exact precedence are in **`references/stated-as-precedence.md`**. Spine of the backstop:

1. `layer = technical` if any tech keyword appears, else `business`.
2. `stated_as` by first match in precedence order: solution keywords → constraint keywords → symptom keywords → else `need`.
3. `quantified = true` if a digit co-occurs with a unit/consequence token (`ms`, `%`, `days`, `users`, `GB`, `TLS 1.`, `99.`).
4. `value_outcome` = first outcome keyword hit, else `null`.
5. `suggested_rewrite` = a per-keyword rewrite when `stated_as = solution`, else a generic need-shaped fallback; `null` otherwise.

Where the backstop and the LLM disagree, prefer the LLM and note the divergence — a disagreement usually means an edge case worth a human glance.

## Idempotency

The same requirement text classifies the same way every time. Classification is a function of the text (plus stable project context), with no dependence on run order, prior runs, or other requirements in the batch. Re-running over an unchanged set yields identical annotations, so it is safe to run on every change.

## Output format

Return one classification per requirement id, in the input order, plus a short human-readable digest. Use only the controlled values above; never invent new ones.

### Machine-readable block

```json
{
  "classifications": [
    {
      "requirement_id": 7,
      "layer": "technical",
      "stated_as": "solution",
      "quantified": false,
      "value_outcome": "Auditable approvals",
      "suggested_rewrite": "The system shall route approval requests for review and capture an auditable record — let the design phase choose the orchestration mechanism."
    },
    {
      "requirement_id": 8,
      "layer": "business",
      "stated_as": "need",
      "quantified": true,
      "value_outcome": "Faster scheduling",
      "suggested_rewrite": null
    },
    {
      "requirement_id": 9,
      "layer": "business",
      "stated_as": "symptom",
      "quantified": false,
      "value_outcome": "Faster scheduling",
      "suggested_rewrite": null
    },
    {
      "requirement_id": 10,
      "layer": "business",
      "stated_as": "constraint",
      "quantified": false,
      "value_outcome": "Data sovereignty",
      "suggested_rewrite": null
    }
  ]
}
```

### Human digest

A compact table the user actually reads, followed by the flags that matter.

```
| id | layer     | stated_as  | quantified | value_outcome      |
|----|-----------|------------|------------|--------------------|
| 7  | technical | solution   | no         | Auditable approvals|
| 8  | business  | need       | yes        | Faster scheduling  |
| 9  | business  | symptom    | no         | Faster scheduling  |
| 10 | business  | constraint | no         | Data sovereignty   |

Flags for the red-team:
- Solutioneering (1): #7 names Power Automate. Suggested need-shaped rewrite above.
- Unmeasurable needs (0): none — all need-shaped items carry a target.
- Symptoms (1): #9 is a pain, not a requirement; derive the real need.
- Value-orphans (0): every requirement maps to a stated outcome.
```

## Notes / anti-patterns

- **Advisory only.** Never mutate status, source, version, id, or the requirement text. Emit annotations beside the text; the human decides.
- **One row per id.** Exactly one classification per input id. Do not skip, merge, duplicate, or renumber.
- **Controlled values only.** `layer ∈ {business, technical}`; `stated_as ∈ {need, solution, constraint, symptom}`. No new categories, no compound values.
- **`suggested_rewrite` is gated.** It is non-null **iff** `stated_as = solution`. A non-null rewrite on a non-solution row is a bug.
- **Respect the precedence.** `solution > constraint > symptom > need`. Don't pick the "nicest" label — pick the highest one that applies.
- **Keep `value_outcome` ≤ 4 words.** It is a display label, not a sentence. If you can't name an outcome in four words, it is probably `null` — and that null is the signal.
- **The LLM is the method.** The keyword tables are a backstop, not the source of truth. Don't downgrade to substring matching just because it's deterministic; use it to cross-check.
- **Don't over-flag `technical`.** A business outcome phrased with one incidental tech noun is still `business`. `technical` is for requirements whose substance is a technical concern.
