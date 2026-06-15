# The frozen-8 solution-architecture sections

> Canonical reference. This is the discoverability mirror of `skills/_shared/frozen-8-sections.md`.
> If the two ever disagree, the `_shared` copy is the one the skills load — fix this one to match.
>
> Cited by the architecture skills:
> `architect/synthesise-solution-architecture`, `architect/reconcile-design-vs-requirements`,
> `architect/reconcile-as-built`, and `architect/import-external-design`.

A solution architecture here is **not one free-form document**. It is a fixed
set of **eight sections**, each its own markdown block, written in a **fixed order**. The set is
**frozen** — it is not per-project configurable, and you do not add, drop, rename, or re-order
sections per project. Freezing it is the whole point: it is what makes generation, reconcile, and the
as-built diff deterministic. Every check has a precise target, and every projection knows exactly what
it reads.

The structure is a **hybrid of "Background & context" + BDAT** (Business / Data / Application /
Technology architecture), deliberately bent so each section maps onto information you actually hold.
Two departures from textbook BDAT, on purpose:

- **NFRs and decisions are pulled out into their own first-class sections.** They are the keystones —
  NFRs flow from the adopted pattern, decisions are the contested calls — so burying them inside
  "Technology" would hide them.
- **An estimate section and an open-questions section are appended.** Both are durable and produced by
  earlier steps in the method, so they belong in the source of truth.

(Pure BDAT under-serves the material; pure Conceptual/Logical/Physical over-serves it — these projects
hold almost no physical-tier data and deployment/infra is usually out of scope.)

---

## The frozen set, in order

The `section_key` is the **stable identifier**. It is what the reconcile and as-built skills match on,
and it never changes. Always emit all eight, always in this order.

| # | `section_key` | Title | Purpose | Generated from (the real inputs) |
|---|---|---|---|---|
| 1 | `background_context` | Background & context | Why the project exists and what success means, in the sponsor's own words. | Project title + description; the **outcomes** (the `outcome`-altitude requirements, each with its value-outcome label); outcomes still being settled flagged separately. |
| 2 | `business_architecture` | Business architecture | The accepted business outcomes and the commitments they represent. | The **outcomes** with their status and key; an "has orphaned requirements" signal where an outcome's subtree no longer applies. |
| 3 | `requirements_acceptance` | Requirements & acceptance criteria | Every derived requirement threaded back to its outcome, each with its testable acceptance criteria. | The **derived requirements** (key, type, applies-status) grouped under their parent outcome; the **acceptance criteria** per requirement. |
| 4 | `application_architecture` | Application & solution shape | The adopted pattern as the solution shape: identity, topology, data placement, and provenance (why it was recommended). | The **settled pattern** (name, summary, deployment topology, data placement); any **pattern override** (the alternative chosen instead, and why); the recommendation's rationale. |
| 5 | `quality_nfrs` | Quality attributes & NFRs | The non-functional standards the build must hold — mostly inherited from the pattern. | The pattern's **attached NFRs**; the propagated **NF requirements** with their acceptance criteria. |
| 6 | `key_decisions` | Key decisions & trade-offs | The genuinely contested calls — what was chosen, why, and which compromises were accepted. | The **ratified decisions** (question, choice, rationale); the **pattern override** as an accepted trade-off. |
| 7 | `estimate_plan` | Estimate & delivery plan | Sized effort and confidence for the real build, with its evidential basis. | The current/accepted **estimate** (effort, low/high range, confidence, basis note); the **confirmed comparators** cited as basis. |
| 8 | `open_questions` | Open questions & risks | What is unresolved or carried as a known risk — never tidied away. | **Orphaned** requirements; **deferred** outcomes; the **pattern override**; open **roadblocks**; open requirement **challenges**; recorded **space expansions**; the live **risks & assumptions** register. |

A blank slot is fine. A section with nothing to say still renders — with a plain reason line ("no
outcomes have been woven yet", "no decisions have been ratified yet"), never an empty heading and
never a fabricated entry. An empty estimate or decision section is honest; it is not a gap.

---

## The two rules that make this work

These are the only two invariants you must hold. Everything else above is guidance.

### Rule 1 — Each fact lives in exactly one section

A given fact is rendered in **one** section and no other. The clearest case: the pattern's NFRs render
**only** in `quality_nfrs` (section 5), never also in `application_architecture` (section 4). Section 4
carries the pattern's identity, summary, topology, placement, and provenance — and deliberately stops
short of its NFRs, leaving every NFR to section 5.

Why it matters: it keeps the reconcile checks meaningful. There is exactly **one** place an NFR is
supposed to appear, so the reconcile "is this NFR addressed?" check has a single, unambiguous target.
If the same fact appeared in two sections, a reconcile check could not tell "covered" from "duplicated
in the wrong place", and the as-built diff would double-count. One fact, one home.

### Rule 2 — Frozen order makes reconcile deterministic

The eight `section_key`s and their order are **frozen** — the same for every project, decided once,
not configurable. This is what lets the downstream skills be deterministic rather than guesswork:

- **Reconcile** reads a known set of sections in a known order and points each check at a known
  `section_key`. "Is this outcome covered somewhere in the design?" / "Is this NFR reflected in
  `quality_nfrs`?" are answerable precisely because the target is fixed.
- **The as-built diff** matches each as-designed section to an as-built block by `section_key`, then
  reports `match` / `gap` / `addition` / `difference`. Stable keys make the matching stable.
- **Projections** (exec summary, estimate, architecture diagram) each read a known subset of sections,
  so they regenerate cleanly and never drift from the source.

If sections were per-project configurable, none of these could be written once and reused — every
project would need its own check wiring. Freezing the order is the cheap discipline that buys
deterministic, reusable downstream tooling.

---

## Practical notes for the architecture skills

- **Always render all eight, in order.** Do not collapse, skip, merge, or re-order. A sparse project
  produces eight sections, some with reason lines.
- **No internal jargon in section bodies.** Plain, professional headings. Section 8's title is always
  "Open questions & risks".
- **Keep section 4 NFR-free.** When you describe the adopted pattern, resist listing its NFRs there —
  that is section 5's job (Rule 1).
- **Record what each section was generated from.** When you (or an Action) regenerate a section, note
  the inputs it was built from (which outcomes, which requirements, which pattern, which estimate).
  The reconcile skill uses that note to spot a section that was generated from data which has since
  changed — the "is this section stale?" question. (Light and advisory: it is a prompt to regenerate,
  not a block.)
- **Proposals, not verdicts.** Reconcile and the as-built diff phrase findings as questions a human
  resolves ("Is this addressed?", "Should this be re-parented or retired?"). They never stamp a
  pass/fail. The frozen-8 structure exists to make those questions precise — not to enforce anything.

## See also

- `skills/architect/synthesise-solution-architecture/SKILL.md` — reads the project
  material and writes these eight sections.
- `skills/architect/reconcile-design-vs-requirements/SKILL.md` — checks the eight
  sections against the requirements; surfaces drift, gaps, and contradictions as proposals.
- `skills/architect/reconcile-as-built/SKILL.md` — diffs a submitted as-built
  document against these eight as-designed sections.
- `skills/architect/import-external-design/SKILL.md` — merges an external solution
  design onto these eight sections as the authoritative source of truth.
- The estimate projection is derived from a known subset of these sections by
  `skills/deliver/comparator-grounded-estimate/SKILL.md`.
