# The frozen-8 solution-architecture sections

> **Canonical source of truth.** This is the one place the eight solution-architecture
> section keys, their order, their purpose, and what each is built from are defined.
> Any skill that touches the solution-architecture document quotes **this** list and does
> not invent, rename, reorder, add, or drop sections. If `references/frozen-8-sections.md`
> exists, it points here rather than restating the list.

## Who relies on this

These skills all read the same eight keys in the same order. Keeping the list in one file
is what keeps them consistent — a section a generator emits, a reconcile check looks for,
and an import re-homes must all mean the same thing.

- **`synthesise-solution-architecture`** — writes the eight sections from the project's
  real material.
- **`reconcile-design-vs-requirements`** — checks each section against requirements/outcomes
  and raises *questions* (never verdicts) about drift, gaps, and orphans.
- **`import-external-design`** — takes an externally-authored design (markdown) and merges it
  onto these eight sections so it becomes authoritative in the same shape.
- **`reconcile-as-built`** — diffs an as-built write-up against these eight as-designed
  sections to surface matches, gaps, additions, and drift.

## Why the set is frozen

The set is **fixed at eight, in a fixed order, and not per-project configurable.** Freezing
it is what makes everything downstream deterministic: every reconcile check has a precise
target, every import knows exactly where each fact lands, and every as-built diff has a
stable thing to compare against. If the set could drift per project, none of those could be
written once and reused.

The shape is a deliberate hybrid: **Background & context, then a bent BDAT** (Business /
Application architecture), with **two textbook departures** — NFRs and key decisions are
pulled out into their **own first-class sections** rather than buried inside "Technology"
(they are the keystone outputs of the method, so hiding them would defeat the point), and an
**estimate/plan** section plus an **open-questions** section are appended (both are durable,
both fall out of work already done). Deployment/infrastructure is intentionally **out of
scope** — there is no physical-tier section.

---

## The canonical set (fixed order)

| # | `section_key` | Title | One-line purpose | Built from |
|---|---|---|---|---|
| 1 | `background_context` | Background & context | Why the project exists and what success means, in the sponsor's own words. | Project title + description; the targeted business outcomes; any outcomes still being settled, flagged as deferred. |
| 2 | `business_architecture` | Business architecture | The accepted business outcomes and the commitments they represent. | The outcomes (status, key, value statement); a flag where an outcome has orphaned requirements hanging off it. |
| 3 | `requirements_acceptance` | Requirements & acceptance criteria | Every derived requirement threaded to its outcome, each with its testable acceptance criteria. | The derived requirements (key, type, parent outcome) and the acceptance criteria attached to each. |
| 4 | `application_architecture` | Application & solution shape | The adopted pattern *as* the solution shape: identity, topology, data placement, and why it was chosen. | The settled component/solution pattern (name, summary, deployment topology, data placement); the selection rationale; any pattern override. NFRs are **not** rendered here — they live in §5. |
| 5 | `quality_nfrs` | Quality attributes & NFRs | The non-functional standards the build must hold — mostly inherited from the adopted pattern. | The pattern's attached NFRs; any propagated non-functional requirements with their acceptance criteria. |
| 6 | `key_decisions` | Key decisions & trade-offs | The genuinely contested calls — what was chosen, why, and the compromises accepted. | The ratified decisions (question, choice, rationale); any pattern override recorded as an accepted trade-off. |
| 7 | `estimate_plan` | Estimate & delivery plan | Sized effort and confidence for the real build, with its evidential basis. | The current/accepted estimate (effort, low/high range, confidence, basis); the confirmed comparators cited as evidence. |
| 8 | `open_questions` | Open questions & risks | What is unresolved or carried as a known risk — never tidied away. | Orphaned requirements; deferred outcomes; pattern overrides; open roadblocks; open requirement challenges; live risks and assumptions; recorded scope expansions. |

The keys, copy-paste exact and in order:

```
background_context
business_architecture
requirements_acceptance
application_architecture
quality_nfrs
key_decisions
estimate_plan
open_questions
```

---

## The rules every consuming skill honours

These three rules are the contract. Break one and a downstream skill silently misbehaves.

1. **Each fact lives in exactly one section.** The pattern's NFRs render in `quality_nfrs`
   and **nowhere else** — not also in `application_architecture`. The pattern's *identity,
   summary, and provenance* render in `application_architecture` and not in `quality_nfrs`.
   This single-home rule is what makes a reconcile check like "is this NFR addressed?"
   answerable: there is exactly one place an NFR is supposed to appear, so its absence there
   is a real signal rather than noise. When synthesising or importing, place each fact once
   and resist the urge to repeat it for emphasis.

2. **Every section always renders — emptiness is stated, not skipped.** A sparse project does
   not yield a missing section; it yields a section whose body carries a plain reason line
   ("no decisions have been ratified yet", "no estimate has been produced yet", "every outcome
   is accepted"). An empty estimate section is **honest output, not a gap**. Never drop a
   section because its inputs are thin, and never fabricate content to fill it.

3. **Fixed order, fixed names, fixed count.** Always eight, always these keys, always this
   order. Do not localise the titles, do not merge two sections, do not add a ninth. If a
   project genuinely needs something that has no home here, it belongs in `open_questions`
   as a carried item — not as a new section.

---

## Mapping for `import-external-design` and `reconcile-as-built`

External and as-built documents will use **their own headings**. Map each of their headings
onto a frozen key, in this rough priority:

1. **Exact title match** (case-insensitive) against the titles in the table above.
2. **Section-key keyword overlap** — e.g. a heading containing "non-functional", "NFR",
   "quality", "performance", "security" maps to `quality_nfrs`; "decision", "trade-off",
   "ADR" maps to `key_decisions`; "estimate", "effort", "timeline", "plan" maps to
   `estimate_plan`; "risk", "open question", "assumption", "TBD" maps to `open_questions`.
3. **No match** — a foreign heading that maps to no frozen key is an **addition** (surface it
   as "the design adds X beyond the eight sections — fold it in or leave it out?"); a frozen
   section with no incoming match is a **gap** ("nothing in the external doc covers
   `key_decisions` — confirm whether that is intentional"). Surface both as **questions**,
   never as pass/fail.

This keeps the import and the as-built diff anchored to the same eight targets that
`synthesise-solution-architecture` produces — so the as-designed and the as-built are
genuinely comparable.

---

## Drift guard

If you are editing a consuming skill and find yourself about to hard-code the section list
inline, **stop and link here instead.** The failure mode this file prevents is four skills
each carrying their own slightly-different copy of the eight sections, which then disagree
about a key spelling or an ordering and quietly break reconcile.

Quick self-check before relying on the list:

- All eight keys present, spelled exactly as in the code block above? ✔
- In the order `background_context → … → open_questions`? ✔
- NFRs homed only in `quality_nfrs`; pattern identity only in `application_architecture`? ✔
- Every section accounted for, even the empty ones? ✔

If any check fails in a consuming skill, fix the skill to match this file — this file is the
authority.

---

*Light and advisory by design. Nothing here blocks a project; it is a shared vocabulary so
the solution-architecture skills speak the same eight words.*
