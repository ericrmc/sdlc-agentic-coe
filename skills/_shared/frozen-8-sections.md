# The frozen-8 solution-architecture sections

> **Canonical source of truth.** This is the one place the eight solution-architecture
> section keys, their order, their purpose, and what each is built from are defined.
> Any skill that touches the solution-architecture document quotes **this** list and does
> not invent, rename, reorder, add, or drop sections. If `references/frozen-8-sections.md`
> exists, it points here rather than restating the list.

## Who relies on this

All read the same eight keys in the same order; keeping the list in one file keeps them
consistent:

- **`synthesise-solution-architecture`** — writes the eight sections from the real material.
- **`reconcile-design-vs-requirements`** — checks each against requirements/outcomes, raising questions.
- **`import-external-design`** — merges an external design onto these eight in the same shape.
- **`reconcile-as-built`** — diffs an as-built write-up against these eight as-designed.

## Why the set is frozen

Fixed at eight, fixed order, not per-project configurable — that is what makes everything
downstream deterministic (a precise reconcile target, a known landing place for each imported
fact, a stable as-built comparator). The shape is a bent BDAT after Background & context, with
NFRs and key decisions pulled into their own first-class sections and an estimate/plan plus
open-questions appended; deployment/infrastructure is deliberately out of scope.

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

1. **Each fact lives in exactly one section** (the table's "Built from" column is the home).
   Pattern NFRs render in `quality_nfrs` only; pattern identity/summary/provenance in
   `application_architecture` only — single-home is what makes "is this NFR addressed?" a real
   signal. Place each fact once; do not repeat for emphasis.

2. **Every section always renders — emptiness is stated, not skipped.** A thin section carries
   a plain reason line ("no decisions ratified yet"), which is honest output, not a gap. Never
   drop a section, never fabricate to fill one.

3. **Fixed order, fixed names, fixed count.** Always eight, always these keys, always this
   order — no localised titles, no merged sections, no ninth. Anything with no home here goes
   into `open_questions` as a carried item.

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
inline, **stop and link here instead.** The failure this prevents is four skills each carrying
a slightly-different copy that then disagrees on a key spelling or ordering and quietly breaks
reconcile. Before relying on a consuming skill's copy, confirm its keys match the code block
above byte-for-byte and in order; if not, fix the skill — this file is the authority.
