---
name: classify-requirements
description: Annotate each requirement with layer / stated_as (need|solution|constraint|symptom) / quantified / value_outcome / source_staleness and a need-shaped rewrite only when solution-shaped. Use after requirements exist, to surface solutioneering, unmeasurability, value-orphans and stale upstream sources. Idempotent and advisory.
one_liner: Tag each requirement's shape to surface solutioneering and unmeasurability.
aliases: [classify requirements, requirement shape, requirement triage, solutioneering check, measurable requirement check, need vs solution, requirement quality, tag requirements]
when_to_use: after requirements exist, to surface solutioneering, unmeasurability and value-orphans
output_kinds: [proposal, question, halt]
deterministic_fallback: the keyword/precedence tables as an optional backstop
suggested_tier: mid
neighbours: |
  before: understand/decompose-intake-to-outcomes (produces the requirements this annotates)
  after: understand/nfr-coverage-check, then challenge/red-team-requirements (act on the flags raised here)
---

# classify-requirements — annotate the shape of each requirement

Describe the *shape* of each requirement so a human can see it at a glance. For every requirement, emit six fields: `layer`, `stated_as`, `quantified`, `value_outcome`, a `suggested_rewrite` (only when the requirement is solution-shaped), and a **derived-on-read `source_staleness`** that re-surfaces an upstream source's age/unverified-export caveat at this first analysis hop (computed from the requirement's own provenance, never invented).

This skill is **advisory and non-destructive**. It describes; it never decides. It does **not** change a requirement's status, source, version, ID, or wording. It only attaches annotations alongside the existing text. A human reads the annotations and chooses what to act on.

Each requirement is cited as `REQ-<n>` — the canonical requirement key. Functional vs non-functional is **`layer`/`stated_as` classify metadata, never part of the key**: there is no `F-`/`NF-` key. This skill is the canonical home of that functional/non-functional distinction, and it lives in the `layer` field, not in the identifier. The machine-readable block may keep a bare integer `requirement_id` as a stable internal index, but the citation key a human sees is always `REQ-<n>`.

The point is to make three failure modes jump off the page:

- **Solutioneering** — a requirement that names a mechanism/product instead of the underlying need (`stated_as = solution`).
- **Unmeasurability** — a requirement with no number/target, so you can't tell when it's met (`quantified = false`).
- **Value-orphans** — a requirement that serves no nameable business outcome (`value_outcome = null`).
- **Stale provenance** — a requirement carried forward from a source whose snapshot is old or whose export age is unverified (`source_staleness` is a non-`current` value). This is the caveat that ingestion stamped onto the requirement's provenance; classify re-surfaces it here, at the first hop, as a `question` — so a six-month-old exported row does not launder into a clean-looking requirement downstream.

## When to use

After requirements exist (captured, elicited, or derived) and before an adversarial requirement review. Run it whenever the requirement set changes and a quick read on its shape is wanted. Re-run freely — it is idempotent.

## Inputs

The user supplies, as markdown or plain context. Each row is marked **Required** or
**Optional**; a Required input that is absent/unreadable/empty HALTs (see
[Grounding (quoted)](#grounding-quoted) and STEP 0).

- **Requirements to classify** — *Required.* A list, each row carrying its `REQ-<n>` key
  (or a bare integer index that maps to one) and the requirement text. Reference each row
  by its real key; do not renumber, merge, skip, or duplicate. **If absent/unreadable/empty:
  HALT and ask where the requirement set is** (per `_shared/grounding.md`); never invent a
  requirement, key, or text. Readable forms: a markdown file, an xlsx/csv path, a GitHub
  Project owner+number, a docs folder, or rows pasted into the chat.
- **Project context** — *Optional.* A short paragraph of what the project is and what it's
  for. This grounds the `value_outcome` inference and the business-vs-technical `layer`
  call. If absent: proceed and surface the gap as a `question` (more `value_outcome = null`
  is the honest result); never pad it with an invented context.
- **Project title** — *Optional.* One line. If absent: proceed with an explicit null /
  placeholder label; never invent a project name.
- **Per-requirement provenance** — *Optional.* The `source_ref` / `received_at` /
  `exported_at` / `snapshot` fields ingestion stamps onto a requirement (see
  `skills/ingest/`). Used only to derive `source_staleness` (STEP 4b). If absent:
  `source_staleness = unknown` — recorded as an explicit null, never inferred from the text.

This skill **names its required inputs and grounds every annotation in supplied text**; it
follows the no-fabrication contract `skills/_contract/grounding-no-absent-input`. The
pre-existing "never invent" / "cite only real keys" rules below are an instance of that
contract, not a separate rule.

## Grounding (quoted)

<!-- BEGIN grounding (byte-stable; do not edit a quoted copy — edit _shared/grounding.md) -->

**GROUNDING RULE — name the required inputs; an absent required input HALTs and asks, never assumes.**

A skill **names its required inputs** up front (its Inputs section marks each row Required or
Optional). Then:

- **A required input that is absent, unreadable, or empty becomes a `halt`.** The halt asks
  the user *where the input is*, offering the formats ingestion can read (an xlsx/csv path, a
  GitHub Project owner+number, a docs folder, or a pasted block). It then **stops and waits.**
  It never assumes, invents, or reasons over a hypothetical — no invented id, key, number, NFR,
  requirement, acceptance criterion, file path, or source row.
- **Partial input is named, not patched.** When some required inputs are present and others are
  not, the skill **names exactly what is missing and asks for it** — it never silently proceeds
  on the part it has, and it never back-fills the gap with a plausible-looking guess.
- **An absent *optional* input proceeds honestly.** It is surfaced as a `question` or recorded
  as an explicit null — never padded with invented content to look complete.

**"I read nothing" and "I cannot read this" are different outputs.** An unreadable or
unsupported source HALTs (it asks for a readable form); it never returns an empty result, because
a silent-empty reads downstream as "the source had nothing in it" — a silent-proceed failure.

**A halt is a question, never a verdict.** A halt names the missing input and asks where it is.
It never smuggles a finding, an assumption, or a disposition for a human to rubber-stamp — no
"I halt because this is infeasible / too risky / out of scope." Those are JUDGMENTs the human
owns. The halt carries only: *what is required, what is missing, and the formats it can be read
from.*

<!-- END grounding -->

Example input block:

```
PROJECT TITLE: Field-service scheduling uplift
PROJECT CONTEXT: Dispatchers hand-build daily routes in a spreadsheet; the
business wants faster, more consistent scheduling and an audit trail of changes.

REQUIREMENTS:
  REQ-7   | The system shall use Power Automate to route approval requests.
  REQ-8   | A dispatcher must be able to publish a day's routes in under 30 seconds.
  REQ-9   | The current process is too slow and dispatchers complain.
  REQ-10  | Customer data must remain within the AU region.
```

## The method

The model reasoning step **is** the method. The deterministic keyword/precedence tables (Step 5) are an optional backstop for offline runs and a sanity check — not the primary classifier. Run the steps in order, per requirement.

### STEP 0 — locate the requirement set (deterministic, pre-model; the halt path)

Before any classification, confirm the one Required input — the **requirement set** — is
present. This is a file-level fact computed *before* the model reasons:

- **absent** — no requirements file/source/paste was supplied;
- **unreadable** — it was supplied but cannot be parsed/opened in a usable form;
- **empty** — it opens but contains zero requirement rows.

Any of those three → emit the clean HALT below and **stop**. Do not classify a hypothetical
set, and do not return an empty classification (a silent-empty reads downstream as "there were
no requirements," which is a silent-proceed failure). Copy the exemplar shape from
`skills/_contract/grounding-no-absent-input`:

```markdown
HALT — required input missing.

I can't classify requirements without the requirement set, and I won't invent one. Tell me
where the requirements live and I'll classify each row exactly as written.

I can read any of these:
  • a markdown file of requirements
  • an xlsx / csv file path
  • a GitHub Project (owner + project number)
  • a docs folder
  • the rows pasted directly into the chat

Which one, and where? (Nothing is classified until you point me at it.)
```

This halt is a `question`, never a verdict: it names the missing input and the readable
formats, and stops — it carries no finding, no "this set looks too thin," no assumption. The
Optional inputs (project context/title, provenance) never halt: an absent Optional input
proceeds honestly (a `question` or an explicit null), per the grounding rule above. With the
requirement set present, proceed to Step 1.

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

This flags unmeasurability: a `need`-shaped requirement with `quantified = false` is a candidate for a hard acceptance question in adversarial review.

### Step 4 — `value_outcome` and `suggested_rewrite`

- **`value_outcome`** — a SHORT display label (**≤ 4 words**) naming the business outcome the requirement serves, grounded in the project context (e.g. "Faster onboarding", "Regulatory compliance", "Audit trail"). Use `null` when no business outcome can be inferred — that is a value-orphan and is itself a useful signal.
- **`suggested_rewrite`** — a need-shaped rewrite that strips the mechanism and restates the underlying need. Provide this **only when `stated_as = solution`**. In every other case it MUST be `null`. The rewrite is a suggestion for the human; it does not overwrite the original text.

### Step 4b — `source_staleness`: derived-on-read, never invented

`source_staleness` re-surfaces — at this first analysis hop — a caveat that ingestion already
stamped onto the requirement's **provenance** (see `skills/ingest/`). It is **derived on read**
from the provenance fields the requirement carries (`received_at`, `exported_at` / `snapshot`,
`staleness-unverified`), **not** a fresh judgement and **never** inferred from the requirement
text. There is no persisted staleness score and no scheduler — the field is computed each time
classify runs, from whatever provenance is present *now*.

Emit exactly one controlled value per requirement:

- `current` — the requirement carries provenance with a recent, verified snapshot/export.
- `stale` — the provenance shows an old snapshot, or ingestion stamped a `staleness-unverified`
  caveat (e.g. a SharePoint export with `exported_at: unknown`, or a GitHub board read without a
  pinned snapshot).
- `unknown` — **the default and the honest null.** The requirement carries no provenance to
  derive from (an Optional input that was absent). This is an explicit null, never a guess.

This field is **advisory and read-only**, exactly like the others: it surfaces, it does not
decide. A non-`current` value is reported as a `question` in the digest ("this row came from a
source that may be out of date — re-verify before relying on it"), **never** as a verdict,
score, or a flip of the requirement's status. Resolving staleness (re-export, re-ingest) is a
separate human action; classify only makes the caveat visible so it does not die at ingest.

> Why here: the downstream consumers (`nfr-coverage-check`, `challenge/red-team-requirements`,
> `architect/recommend-component-patterns`) read requirement *text* only. Without this re-surface,
> a stale Excel row would launder into a clean-looking requirement two skills later. Classify is
> the first hop, so the caveat re-appears here.

### Step 5 — Deterministic backstop (optional, NOT the primary method)

For offline runs, regression tests, or a quick cross-check, a pure keyword/precedence pass produces the same fields with no model call. It is a coarse fallback — the model step above is the real classifier. The tables and the exact precedence are in **`references/stated-as-precedence.md`**. Outline of the backstop:

1. `layer = technical` if any tech keyword appears, else `business`.
2. `stated_as` by first match in precedence order: solution keywords → constraint keywords → symptom keywords → else `need`.
3. `quantified = true` if a digit co-occurs with a unit/consequence token (`ms`, `%`, `days`, `users`, `GB`, `TLS 1.`, `99.`).
4. `value_outcome` = first outcome keyword hit, else `null`.
5. `suggested_rewrite` = a per-keyword rewrite when `stated_as = solution`, else a generic need-shaped fallback; `null` otherwise.
6. `source_staleness` = read straight from provenance: `stale` if a `staleness-unverified` caveat or an old/`unknown` snapshot is present, `current` if a recent verified snapshot is present, else `unknown`. This is a lookup, not a keyword pass — never derived from requirement text.

Where the backstop and the model disagree, prefer the model and note the divergence — a disagreement usually means an edge case worth a human glance.

## Idempotency

The same requirement text classifies the same way every time. The five shape fields (`layer`, `stated_as`, `quantified`, `value_outcome`, `suggested_rewrite`) are a function of the text (plus stable project context), with no dependence on run order, prior runs, or other requirements in the batch. `source_staleness` is **derived-on-read** — a pure function of the requirement's provenance *at read time* — so it carries no stored state either; it changes only when the underlying provenance changes (a re-export, a re-ingest), never on a re-run over identical inputs. Re-running over an unchanged set with unchanged provenance yields identical annotations, so it is safe to run on every change.

## Output format

Return one classification per requirement, in the input order, plus a short human-readable digest. Use only the controlled values above; never invent new ones. The machine-readable block keys each row by its `requirement_id` integer as a stable internal index; everything a human reads cites the canonical `REQ-<n>` key (where `<n>` is that same index).

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
      "suggested_rewrite": "The system shall route approval requests for review and capture an auditable record — let the design phase choose the orchestration mechanism.",
      "source_staleness": "stale"
    },
    {
      "requirement_id": 8,
      "layer": "business",
      "stated_as": "need",
      "quantified": true,
      "value_outcome": "Faster scheduling",
      "suggested_rewrite": null,
      "source_staleness": "current"
    },
    {
      "requirement_id": 9,
      "layer": "business",
      "stated_as": "symptom",
      "quantified": false,
      "value_outcome": "Faster scheduling",
      "suggested_rewrite": null,
      "source_staleness": "unknown"
    },
    {
      "requirement_id": 10,
      "layer": "business",
      "stated_as": "constraint",
      "quantified": false,
      "value_outcome": "Data sovereignty",
      "suggested_rewrite": null,
      "source_staleness": "unknown"
    }
  ]
}
```

### Human digest

A compact table the user actually reads, followed by the flags that matter.

```
| key    | layer     | stated_as  | quantified | value_outcome      | source     |
|--------|-----------|------------|------------|--------------------|------------|
| REQ-7  | technical | solution   | no         | Auditable approvals| stale ⚠    |
| REQ-8  | business  | need       | yes        | Faster scheduling  | current    |
| REQ-9  | business  | symptom    | no         | Faster scheduling  | unknown    |
| REQ-10 | business  | constraint | no         | Data sovereignty   | unknown    |

Flags for adversarial review:
- Solutioneering (1): REQ-7 names a named product. Suggested need-shaped rewrite above.
- Unmeasurable needs (0): none — all need-shaped items carry a target.
- Symptoms (1): REQ-9 is a pain, not a requirement; derive the real need.
- Value-orphans (0): every requirement maps to a stated outcome.
- Stale provenance (1): REQ-7 came from a source whose export age is unverified —
  re-verify before relying on it (a question for the human, not a verdict). The
  `unknown` rows carry no provenance to judge.
```

## Notes / anti-patterns

- **Advisory only.** Never mutate status, source, version, id, or the requirement text. Emit annotations beside the text; the human decides.
- **One row per requirement.** Exactly one classification per input `REQ-<n>` (or its integer index). Do not skip, merge, duplicate, or renumber.
- **Controlled values only.** `layer ∈ {business, technical}`; `stated_as ∈ {need, solution, constraint, symptom}`; `source_staleness ∈ {current, stale, unknown}`. No new categories, no compound values.
- **`source_staleness` is derived, never invented.** Read it from the requirement's provenance fields; if there is no provenance, it is `unknown` (the honest null), never guessed from the text. A non-`current` value surfaces as a `question`, never a verdict or a status change.
- **`suggested_rewrite` is gated.** It is non-null **iff** `stated_as = solution`. A non-null rewrite on a non-solution row is a bug.
- **Respect the precedence.** `solution > constraint > symptom > need`. Don't pick the "nicest" label — pick the highest one that applies.
- **Keep `value_outcome` ≤ 4 words.** It is a display label, not a sentence. If you can't name an outcome in four words, it is probably `null` — and that null is the signal.
- **The model step is the method.** The keyword tables are a backstop, not the source of truth. Don't downgrade to substring matching just because it's deterministic; use it to cross-check.
- **Don't over-flag `technical`.** A business outcome phrased with one incidental tech noun is still `business`. `technical` is for requirements whose substance is a technical concern.
