---
name: synthesise-solution-architecture
description: Read the codebase plus the project's outcomes/requirements/decisions and author a solution-architecture doc as the fixed frozen-8 sections; assemble the graph slice once, ground only in it, preserve keys verbatim, each fact in exactly one section. Use when authoring the durable solution design once a direction is locked in.
when_to_use: authoring the durable solution design once a direction is locked in
output_kinds: [proposal, halt]
deterministic_fallback: the frozen-8 section skeleton with an honest 'nothing recorded yet' per empty section
one_liner: Author the durable solution-design doc as eight fixed sections.
aliases: [solution design document, architecture document, design doc, write up the design, solution architecture, design write-up, architecture spec, document the design]
suggested_tier: frontier
neighbours: |
  Before: panel/frontend-a11y-review (design has been battle-tested and reviewed).
  After: architect/reconcile-design-vs-requirements (check the written design against the requirements as both change).
---

# Synthesise solution architecture

Author the durable solution-design document for a project as a fixed set of eight independently-versioned markdown sections, each grounded only in its own slice of the project's material.

## Purpose

A **proposal**, not a verdict: a faithful synthesis a human reviews, edits, and re-runs. Four mechanical disciplines make it trustworthy — frozen section set, each fact in exactly one section, keys preserved verbatim, thin material stated plainly. They are enforced by the frozen-8 table and method clauses below; this section only names them.

## When to use

Use this once a direction is **locked in** — outcomes accepted, a pattern chosen, decisions made, an estimate produced (or honestly absent). This is the durable design everyone then builds against.

Do **not** use it to explore options or to decide direction (that is earlier work). And do not treat its output as an approval — it is advisory synthesis, light by design. Re-run it whenever the underlying material changes; regeneration is cheap and non-destructive (the old version is kept).

## Inputs

The user (or the orchestrator) supplies a **project-graph slice** — the assembled facts for the project. Read whatever of the codebase is relevant to ground the architecture, plus these recorded rows:

- **Project framing + recorded rows (outcomes / requirements)** — *Required.* The title,
  description / intake text, any vision / business-case / context grounding, the accepted
  business outcomes (with their `req_key`, status, value label), and the derived requirements
  threaded to their outcome (each with `req_key`, type, acceptance criteria). NF requirements
  are called out separately. *If the project framing **and** the outcomes/requirements are all
  absent/unreadable/empty: HALT and ask where the project material lives (per
  `_shared/grounding.md`); never invent an outcome, a `req_key`, a requirement, or an
  acceptance criterion to fill a section.* Readable forms: a markdown file, an xlsx/csv path, a
  GitHub Project owner+number, a docs folder, or a pasted block.
- **Codebase** — *Optional.* Read whatever of it grounds the architecture sections. *If absent
  (e.g. a greenfield design before any code exists): proceed and ground the architecture in the
  recorded rows alone; never invent components, files, or a topology the material does not
  support.*
- **Pattern** — *Optional.* The adopted solution pattern (name, summary, deployment topology, data placement) and its attached NFRs; plus any pattern override (chosen alternative + reason) and the recommendation's rationale. *If absent: the application-shape and NFR sections say so plainly; never invent a pattern.*
- **Decisions** — *Optional.* The ratified, genuinely-contested calls (question, choice, rationale). *If absent: the decisions section carries its honest empty line.*
- **Estimate** — *Optional.* Sized effort (point + low/high range + confidence + basis) and the comparator rows cited as evidence — or honest absence. *If absent: the estimate section says no estimate was produced; never invent a number or a comparator.*
- **Open items** — *Optional.* Orphaned requirements, deferred outcomes, the pattern override, open roadblocks, open requirement challenges, recorded space-expansions, and live risks & assumptions. *If absent: the open-questions section is honestly empty.*

> **Thin-but-present material is the deterministic skeleton, NOT a halt.** A sparse project
> with framing + a couple of outcomes but no pattern, no decisions, and no estimate yields a
> complete eight-section document whose empty sections say "nothing recorded yet" (Step 2).
> What HALTs is an **entirely absent** required set — no framing *and* no
> outcomes/requirements — because there is then nothing to synthesise and the only way to fill
> the document would be to invent it.

## Grounding (quoted)

Carries the no-fabrication keystone (`skills/_contract/grounding-no-absent-input`).

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

If a slice is not pre-assembled, **assemble it once** at the start (see Step 1). Assembling it per-section is the anti-pattern that leaks facts across boundaries.

## The frozen-8 sections

These eight sections, **in this fixed order, with these stable keys**, are the whole document. The set is not per-project configurable — freezing it is what makes downstream reconcile deterministic. The full reference is in `../../_shared/frozen-8-sections.md`.

| # | `section_key` | Title | Purpose | Generated from (real rows) |
|---|---|---|---|---|
| 1 | `background_context` | Background & context | Why the project exists and what success means, in the sponsor's words. | project title / description; outcomes (with value label); deferred outcomes flagged. |
| 2 | `business_architecture` | Business architecture | The accepted business outcomes and the commitments they represent. | outcomes (status, `req_key`, value label); orphaned-subtree signal. |
| 3 | `requirements_acceptance` | Requirements & acceptance criteria | Every derived requirement threaded to its outcome, each with its testable acceptance criteria. | derived requirements (`req_key`, type, applies-status); acceptance criteria per requirement. |
| 4 | `application_architecture` | Application & solution shape | The adopted pattern as the solution shape: identity, topology, data placement, provenance. | settled pattern (name, summary, topology, data placement); pattern override; recommendation rationale. **Identity / summary / provenance only — no NFRs here.** |
| 5 | `quality_nfrs` | Quality attributes & NFRs | The non-functional standards the build must hold — mostly inherited from the pattern. | pattern's attached NFRs; propagated NF requirements (`req_type='NF'`) with their acceptance criteria. **The only home for NFRs.** |
| 6 | `key_decisions` | Key decisions & trade-offs | The genuinely contested calls, what was chosen, why — including compromises accepted. | ratified decisions (question, choice, rationale); pattern override (chosen alternative, reason). |
| 7 | `estimate_plan` | Estimate & delivery plan | Sized effort and confidence for the real build, with its evidential basis. | current / accepted estimate (effort, low / high, confidence, basis); confirmed comparator rows cited as basis. |
| 8 | `open_questions` | Open questions & risks | What is unresolved or carried as a known risk — never tidied away. | orphaned requirements; deferred outcomes; pattern override; open roadblocks; open requirement challenges; space-expansions; live risks & assumptions. |

The layout is a hybrid of Background & context + BDAT, bent so each section maps onto data the project already holds: NFRs and decisions are pulled out as first-class sections (rather than buried in Technology), and estimate + open-questions are appended. Single-home rule (method clause 5): the pattern's identity/topology/provenance is section 4's alone; its NFRs are section 5's alone.

## The method

This is the contract for authoring. Honour every clause.

0. **Locate / verify the required input first (deterministic, pre-model).** Before assembling
   anything, confirm the Required set is present as a file-level fact: the **project framing**
   and/or the **outcomes / requirements**. This is mechanical — absent / unreadable / empty —
   never a judgement on "is there enough recorded to write a design." If the framing *and* the
   outcomes/requirements are all absent, emit the clean HALT below and stop. (Thin-but-present
   material is **not** a halt — it is the skeleton path of step 2.)

   ```
   HALT — required input missing.

   I can't synthesise a solution design without the project's framing and its
   outcomes / requirements, and I won't invent them to fill the sections. Point me at the
   project material and I'll author the eight sections grounded only in it — nothing is
   assumed until then.

   I can read any of: a markdown file · an xlsx/csv path · a GitHub Project (owner + number)
   · a docs folder · the rows pasted directly here. Which one, and where?
   ```

1. **Assemble the project-graph slice ONCE.** Read the project and reshape it into a single assembled context up front — outcomes grouped, children grouped under their parent, acceptance criteria grouped per requirement, the settled pattern with its attached NFRs, ratified decisions, the estimate, comparators, orphans, open roadblocks / challenges, space-expansions, and live register items. Read whatever of the codebase grounds the architecture *now*, not section by section. One read per source, plain data, no re-reads mid-author. One assembly, then route slices of it to sections.

2. **Render the deterministic skeleton first.** Lay down all eight sections, in the frozen order, with their canonical titles, *before* authoring any prose. This skeleton is the deterministic fallback: even with zero material it is a complete, honest document of eight sections each saying "nothing recorded yet."

3. **Author each section grounded ONLY in its slice.** For each section, the assembled material routed to it is the **only** source. Do not pull a decision into the requirements section, or a pattern NFR into the application-shape section. The frozen layout already routed every fact; follow the routing.

4. **Preserve every requirement / outcome key verbatim.** Carry every backtick-quoted key (`REQ-1`, `REQ-7`, `BO-1`, …) through unchanged. Traceability is the point — a renamed or dropped key silently breaks the thread from outcome to requirement to acceptance criterion.

5. **Each fact in exactly one section.** A pattern's NFRs render only in `quality_nfrs`. The pattern's *identity* renders only in `application_architecture`. An override's *reason* can appear as a decision (section 6) and as an open trade-off (section 8) where the material genuinely carries both senses — but a plain fact has exactly one home. When in doubt, the table above is the tiebreak.

6. **When a section's material is thin, say so plainly.** If there are no decisions, the decisions section says "No decisions have been ratified yet." — it does not invent a decision. Empty estimate, empty comparators, no overrides, no risks: state the honest empty-line and move on. Fabrication is the cardinal failure here. Ground every claim in the provided material; add no facts of your own.

7. **Plain house style, no product / codenames.** Write as a faithful solution architect: clean professional markdown, a short heading per section then prose and / or lists, no editorialising beyond what the material supports, no product names or internal jargon. The open-questions section is titled "Open questions & risks".

8. **The frozen order is load-bearing.** Emit the eight in the canonical order above, always. The order is not cosmetic — it is what makes a downstream reconcile (and any combined export) deterministic. Do not reorder, drop, merge, or add sections.

### The deterministic base and the model step

The work has two clearly separated halves — keep them separate:

- **DETERMINISTIC STEP — render the 8-section skeleton.** Mechanically produce the eight titled sections in frozen order. No judgement, no model call, no randomness. This is the floor you can always ship.
- **MODEL STEP — generate each section body.** For each `section_key`, run the section's grounding prompt (`references/section-prompts/<section_key>.md`) against that section's slice to author the body. This is the only place reasoning enters, and it is fenced inside one section's material at a time.

## Composing other skills

This skill is the **composition root** for two reusable mechanics:

- **`skills/_contract/parallel-agents`** — fan out **one parallel agent per section**. Each agent gets exactly one section's slice and its grounding prompt, authors that one body, and returns it. Because each fact lives in one section and each section is grounded only in its own slice, the eight authoring jobs are genuinely independent and parallelise cleanly. Reassemble the returned bodies into the frozen order.
- **`skills/_contract/explore-one-area-at-a-time`** — the **`section_key` is the routing edge**. It is the stable identifier that says which slice of the assembled graph an agent sees and which section it writes. Routing by `section_key` is what keeps each agent inside its lane and stops facts leaking across section boundaries.

The per-section fan-out is advisory (never required — the deterministic base stands; merge what succeeded); for the agent count, failure handling, and runner mapping see `skills/_contract/parallel-agents`.

Ship a **grounding prompt per section** in `references/section-prompts/` (eight files, named by `section_key`). Each is a thin specialisation of the shared authoring prompt, naming the one section, its title, and the slice it is grounded in. The shared template's invariant clause — *"This is the ONLY source material. Do NOT invent … If the material for this section is empty or thin, say so plainly … Preserve every backtick-quoted key verbatim … Plain professional house style, no product / codenames"* — is repeated in every one.

## Output format

The user gets back a single markdown document: the eight frozen sections, in order, each a titled block. For a real project each section carries its grounded prose; for a sparse project the empty sections carry an honest reason line. Below is the **skeleton template** (the deterministic fallback) — with one populated section shown so the shape is concrete.

```markdown
# Solution design — <project title>

## 1. Background & context

## Why <project title> exists

<project description, or: _No intake description was recorded._>

### Targeted outcomes
- `BO-1` — _faster onboarding_ — New analysts are productive within one day.
- `BO-2` — _lower support load_ — Tier-1 tickets fall by a third.

### Outcomes still being settled
_every outcome is accepted_

## 2. Business architecture

_nothing recorded yet — no outcomes have been woven for this project._

## 3. Requirements & acceptance criteria

### `BO-1` — New analysts are productive within one day
- `REQ-1` Guided first-run walkthrough.
    - _AC:_ A new user completes setup without contacting support.
- `REQ-2` (NF) First-run loads in under two seconds on a standard laptop.
    - _AC:_ p95 first-paint < 2s measured on the reference device.

## 4. Application & solution shape

# Adopted pattern — <pattern name>

<pattern summary>

- **Deployment topology:** <topology>
- **Data placement:** <placement>

_Provenance: <recommendation rationale>_

## 5. Quality attributes & NFRs

### Governed NFRs (from the adopted pattern)
- **availability**: 99.9% monthly, business hours.

### Propagated non-functional requirements
- `REQ-2` First-run loads in under two seconds on a standard laptop.
    - _AC:_ p95 first-paint < 2s measured on the reference device.

## 6. Key decisions & trade-offs

### Ratified decisions
_No decisions have been ratified yet._

### Accepted trade-offs
_No pattern override was recorded._

## 7. Estimate & delivery plan

_No estimate has been produced yet. Confirm comparators and run the estimate to populate this section._

## 8. Open questions & risks

### Risks & assumptions
- **Assumption #4:** The reference device represents the slowest supported hardware.
- **Risk #7:** Third-party auth provider deprecation (likelihood medium, impact high).
```

Each section is **individually exportable** as `<section_key>.md`, and all eight join client-side into a single combined `SOLUTION-DESIGN.md` with the titles as headings. Re-running a section produces a **new version** that supersedes the old — never an in-place overwrite; the prior version is always retained. A hand edit follows the same path (a new version marked as edited). Record, alongside each generated section, a small snapshot of *which* rows it was generated from (ids / count / max version per source) — that snapshot is the baseline a later reconcile diffs against to flag a stale section. This is advisory bookkeeping, not a go/no-go gate.

## Notes / anti-patterns

- **Do not treat the output as approval.** This is advisory synthesis. It proposes the written design; it blocks nothing and signs off nothing. If something is unresolved, it belongs in section 8 — surfaced, not tidied away.
- **Prefer the deterministic floor over a bad guess.** If the model step is unavailable or a slice is unclear, ship the skeleton with honest empty lines. A correct, sparse document beats a confident, invented one.
