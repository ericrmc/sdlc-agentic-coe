---
name: synthesise-solution-architecture
description: Read the codebase plus the project's outcomes/requirements/decisions and author a solution-architecture doc as the fixed frozen-8 sections; assemble the graph slice once, ground only in it, preserve keys verbatim, each fact in exactly one section. Use when authoring the durable solution design once a direction is locked in.
when_to_use: authoring the durable solution design once a direction is locked in
output_kinds: [proposal]
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

Write the living **solution-design document** — not as one monolithic doc, but as a **fixed set of eight independently-versioned markdown sections**. Read the codebase plus the project's recorded outcomes, requirements, pattern, decisions, estimate, and open risks, then write each section grounded *only* in its own slice of that material.

The output is a **proposal**: a faithful synthesis a human reviews, edits, and re-runs. It issues no verdict and approves nothing. It is "here is the design, written down honestly, with traceability intact."

The discipline that makes it trustworthy is mechanical, not stylistic:

- The section set is **frozen** (the same eight, in the same order, every time). A frozen set is what makes a later *reconcile* deterministic — every check has a precise target, every downstream projection knows exactly what it reads.
- **Each fact lives in exactly one section.** A pattern's NFRs render in `quality_nfrs` and nowhere else. If a fact could plausibly go in two sections, the frozen layout already decided which one — follow it.
- **Keys are preserved verbatim.** Every requirement / outcome key shown in the material (backtick-quoted `F-1`, `NF-2`, `O-1`) is carried through unchanged so traceability survives the synthesis.
- **Thin material is stated plainly, never padded.** A sparse project produces honest "nothing recorded yet" lines, not invented content.

## When to use

Use this once a direction is **locked in** — outcomes accepted, a pattern chosen, decisions made, an estimate produced (or honestly absent). This is the durable design everyone then builds against.

Do **not** use it to explore options or to decide direction (that is earlier work). And do not treat its output as an approval — it is advisory synthesis, light by design. Re-run it whenever the underlying material changes; regeneration is cheap and non-destructive (the old version is kept).

## Inputs

The user (or the orchestrator) supplies a **project-graph slice** — the assembled facts for the project. Read whatever of the codebase is relevant to ground the architecture, plus these recorded rows:

- **Project framing** — title, description / intake text, and any vision / business-case / context grounding.
- **Outcomes** — accepted business outcomes (with their `req_key`, status, and value label), plus any deferred / still-being-settled outcomes.
- **Requirements** — derived requirements threaded to their outcome, each with `req_key`, type (functional / NF), and its acceptance criteria. NF requirements are called out separately.
- **Pattern** — the adopted solution pattern (name, summary, deployment topology, data placement) and its attached NFRs; plus any pattern override (chosen alternative + reason) and the recommendation's rationale.
- **Decisions** — the ratified, genuinely-contested calls (question, choice, rationale).
- **Estimate** — sized effort (point + low/high range + confidence + basis) and the comparator rows cited as evidence — or honest absence.
- **Open items** — orphaned requirements, deferred outcomes, the pattern override, open roadblocks, open requirement challenges, recorded space-expansions, and live risks & assumptions.

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

The layout is a **hybrid of Background & context + BDAT** (Business / Data / Application / Technology), deliberately bent so each section maps onto data the project already holds. Two departures from textbook BDAT: NFRs and decisions are pulled out into their own first-class sections (they are the keystone — NFRs flow from the pattern, decisions are the contested calls — so burying them inside "Technology" would hide them); and an estimate section and an open-questions section are appended (both are durable and produced upstream).

Note the **single-home rule made concrete**: the adopted pattern's identity, topology, and provenance belong to section 4 (`application_architecture`); the same pattern's *NFRs* belong to section 5 (`quality_nfrs`) and must not also appear in section 4. Keeping each fact in one place is exactly what lets a later "is this NFR addressed?" reconcile check have one unambiguous target.

## The method

This is the contract for authoring. Honour every clause.

1. **Assemble the project-graph slice ONCE.** Read the project and reshape it into a single assembled context up front — outcomes grouped, children grouped under their parent, acceptance criteria grouped per requirement, the settled pattern with its attached NFRs, ratified decisions, the estimate, comparators, orphans, open roadblocks / challenges, space-expansions, and live register items. Read whatever of the codebase grounds the architecture *now*, not section by section. One read per source, plain data, no re-reads mid-author. One assembly, then route slices of it to sections.

2. **Render the deterministic skeleton first.** Lay down all eight sections, in the frozen order, with their canonical titles, *before* authoring any prose. This skeleton is the deterministic fallback: even with zero material it is a complete, honest document of eight sections each saying "nothing recorded yet."

3. **Author each section grounded ONLY in its slice.** For each section, the assembled material routed to it is the **only** source. Do not pull a decision into the requirements section, or a pattern NFR into the application-shape section. The frozen layout already routed every fact; follow the routing.

4. **Preserve every requirement / outcome key verbatim.** Carry every backtick-quoted key (`F-1`, `NF-2`, `O-1`, …) through unchanged. Traceability is the point — a renamed or dropped key silently breaks the thread from outcome to requirement to acceptance criterion.

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

> **Multi-agent option (advisory).** This step deepens with independent parallel agents: launch one sub-agent per section, at most 4 at a time, each a separate sub-agent. A failed sub-agent returns nothing and is never fatal — the deterministic base stands; merge what succeeded. (Claude Code: use the Task tool / subagents. Other tools: launch parallel model calls; or a matrix-strategy CI job.) Never required — it adds coverage and cuts single-pass bias. See `skills/_contract/parallel-agents`.

Ship a **grounding prompt per section** in `references/section-prompts/` (eight files, named by `section_key`). Each is a thin specialisation of the shared authoring prompt, naming the one section, its title, and the slice it is grounded in. The shared template's invariant clause — *"This is the ONLY source material. Do NOT invent … If the material for this section is empty or thin, say so plainly … Preserve every backtick-quoted key verbatim … Plain professional house style, no product / codenames"* — is repeated in every one.

## Output format

The user gets back a single markdown document: the eight frozen sections, in order, each a titled block. For a real project each section carries its grounded prose; for a sparse project the empty sections carry an honest reason line. Below is the **skeleton template** (the deterministic fallback) — with one populated section shown so the shape is concrete.

```markdown
# Solution design — <project title>

## 1. Background & context

## Why <project title> exists

<project description, or: _No intake description was recorded._>

### Targeted outcomes
- `O-1` — _faster onboarding_ — New analysts are productive within one day.
- `O-2` — _lower support load_ — Tier-1 tickets fall by a third.

### Outcomes still being settled
_every outcome is accepted_

## 2. Business architecture

_nothing recorded yet — no outcomes have been woven for this project._

## 3. Requirements & acceptance criteria

### `O-1` — New analysts are productive within one day
- `F-1` Guided first-run walkthrough.
    - _AC:_ A new user completes setup without contacting support.
- `NF-1` First-run loads in under two seconds on a standard laptop.
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
- `NF-1` First-run loads in under two seconds on a standard laptop.
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

- **Do not reorder, merge, drop, or add sections.** The frozen eight in fixed order is the contract. A "this project doesn't need decisions" instinct is wrong — render the section with its honest empty line.
- **Do not let a fact appear twice.** The classic leak is rendering the pattern's NFRs in both `application_architecture` and `quality_nfrs`. Section 4 is identity / topology / provenance only; NFRs are section 5's alone. Duplication makes a later "is this addressed?" check ambiguous.
- **Do not fabricate to fill space.** Thin material is a true fact about the project. "No comparators were confirmed" is a better section than an invented comparator. Add no facts not in the material.
- **Do not rename or paraphrase keys.** `F-1` stays `F-1`, backticked. The whole value of the document is the preserved thread from outcome to requirement to acceptance criterion.
- **Do not assemble per-section.** Read and reshape the graph once; route slices to sections. Re-reading per section is how facts and keys drift between sections.
- **Do not editorialise or import codenames.** Plain solution-architect prose, grounded strictly in the slice. No product names or internal jargon in any rendered string.
- **Do not treat the output as approval.** This is advisory synthesis. It proposes the written design; it blocks nothing and signs off nothing. If something is unresolved, it belongs in section 8 — surfaced, not tidied away.
- **Prefer the deterministic floor over a bad guess.** If the model step is unavailable or a slice is unclear, ship the skeleton with honest empty lines. A correct, sparse document beats a confident, invented one.
