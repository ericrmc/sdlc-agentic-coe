<!-- GENERATED FILE — DO NOT EDIT.
     Built by skills/_scripts/concat_skills.py from the sources listed below.
     Edit the source skill/pattern files and re-run the concat-patterns Action.
     This file is marked linguist-generated in .gitattributes. -->

# Solution Design — combined author + reconcile loop

> Generated bundle. Built 2026-06-16 by `skills/_scripts/concat_skills.py`.

The end-to-end solution-architecture authoring method in one file. Start with the synthesise-solution-architecture skill (read the codebase + context, then author the document as the frozen-8 sections), keep the frozen-8 section reference alongside it so every section has a precise target, and close with reconcile-design-vs-requirements to check the authored design back against the requirement set. Advisory throughout — reconcile reports drift, it does not block.

## Bundled sources

- `skills/architect/synthesise-solution-architecture/SKILL.md`
- `references/frozen-8-sections.md`
- `skills/architect/reconcile-design-vs-requirements/SKILL.md`


---

## Source: `skills/architect/synthesise-solution-architecture/SKILL.md`

<details><summary>frontmatter</summary>

```yaml
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
```

</details>

## Synthesise solution architecture

Author the durable solution-design document for a project as a fixed set of eight independently-versioned markdown sections, each grounded only in its own slice of the project's material.

### Purpose

Write the living **solution-design document** — not as one monolithic doc, but as a **fixed set of eight independently-versioned markdown sections**. Read the codebase plus the project's recorded outcomes, requirements, pattern, decisions, estimate, and open risks, then write each section grounded *only* in its own slice of that material.

The output is a **proposal**: a faithful synthesis a human reviews, edits, and re-runs. It issues no verdict and approves nothing. It is "here is the design, written down honestly, with traceability intact."

The discipline that makes it trustworthy is mechanical, not stylistic:

- The section set is **frozen** (the same eight, in the same order, every time). A frozen set is what makes a later *reconcile* deterministic — every check has a precise target, every downstream projection knows exactly what it reads.
- **Each fact lives in exactly one section.** A pattern's NFRs render in `quality_nfrs` and nowhere else. If a fact could plausibly go in two sections, the frozen layout already decided which one — follow it.
- **Keys are preserved verbatim.** Every requirement / outcome key shown in the material (backtick-quoted `REQ-1`, `REQ-7`, `BO-1`) is carried through unchanged so traceability survives the synthesis.
- **Thin material is stated plainly, never padded.** A sparse project produces honest "nothing recorded yet" lines, not invented content.

### When to use

Use this once a direction is **locked in** — outcomes accepted, a pattern chosen, decisions made, an estimate produced (or honestly absent). This is the durable design everyone then builds against.

Do **not** use it to explore options or to decide direction (that is earlier work). And do not treat its output as an approval — it is advisory synthesis, light by design. Re-run it whenever the underlying material changes; regeneration is cheap and non-destructive (the old version is kept).

### Inputs

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

### Grounding (quoted)

This skill reads the codebase plus the project's outcomes, requirements, decisions, and
acceptance criteria, so it carries the no-fabrication keystone — see
`skills/_contract/grounding-no-absent-input`. The existing "ground every claim in the provided
material; add no facts of your own; thin material is stated plainly, never padded" discipline
is one **instance** of this contract.

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

### The frozen-8 sections

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

### The method

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

#### The deterministic base and the model step

The work has two clearly separated halves — keep them separate:

- **DETERMINISTIC STEP — render the 8-section skeleton.** Mechanically produce the eight titled sections in frozen order. No judgement, no model call, no randomness. This is the floor you can always ship.
- **MODEL STEP — generate each section body.** For each `section_key`, run the section's grounding prompt (`references/section-prompts/<section_key>.md`) against that section's slice to author the body. This is the only place reasoning enters, and it is fenced inside one section's material at a time.

### Composing other skills

This skill is the **composition root** for two reusable mechanics:

- **`skills/_contract/parallel-agents`** — fan out **one parallel agent per section**. Each agent gets exactly one section's slice and its grounding prompt, authors that one body, and returns it. Because each fact lives in one section and each section is grounded only in its own slice, the eight authoring jobs are genuinely independent and parallelise cleanly. Reassemble the returned bodies into the frozen order.
- **`skills/_contract/explore-one-area-at-a-time`** — the **`section_key` is the routing edge**. It is the stable identifier that says which slice of the assembled graph an agent sees and which section it writes. Routing by `section_key` is what keeps each agent inside its lane and stops facts leaking across section boundaries.

> **Multi-agent option (advisory).** This step deepens with independent parallel agents: launch one sub-agent per section, at most 4 at a time, each a separate sub-agent. A failed sub-agent returns nothing and is never fatal — the deterministic base stands; merge what succeeded. (Claude Code: use the Task tool / subagents. Other tools: launch parallel model calls; or a matrix-strategy CI job.) Never required — it adds coverage and cuts single-pass bias. See `skills/_contract/parallel-agents`.

Ship a **grounding prompt per section** in `references/section-prompts/` (eight files, named by `section_key`). Each is a thin specialisation of the shared authoring prompt, naming the one section, its title, and the slice it is grounded in. The shared template's invariant clause — *"This is the ONLY source material. Do NOT invent … If the material for this section is empty or thin, say so plainly … Preserve every backtick-quoted key verbatim … Plain professional house style, no product / codenames"* — is repeated in every one.

### Output format

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

### Notes / anti-patterns

- **Do not reorder, merge, drop, or add sections.** The frozen eight in fixed order is the contract. A "this project doesn't need decisions" instinct is wrong — render the section with its honest empty line.
- **Do not let a fact appear twice.** The classic leak is rendering the pattern's NFRs in both `application_architecture` and `quality_nfrs`. Section 4 is identity / topology / provenance only; NFRs are section 5's alone. Duplication makes a later "is this addressed?" check ambiguous.
- **Do not fabricate to fill space.** Thin material is a true fact about the project. "No comparators were confirmed" is a better section than an invented comparator. Add no facts not in the material.
- **Do not rename or paraphrase keys.** `REQ-1` stays `REQ-1`, backticked. The whole value of the document is the preserved thread from outcome to requirement to acceptance criterion.
- **Do not assemble per-section.** Read and reshape the graph once; route slices to sections. Re-reading per section is how facts and keys drift between sections.
- **Do not editorialise or import codenames.** Plain solution-architect prose, grounded strictly in the slice. No product names or internal jargon in any rendered string.
- **Do not treat the output as approval.** This is advisory synthesis. It proposes the written design; it blocks nothing and signs off nothing. If something is unresolved, it belongs in section 8 — surfaced, not tidied away.
- **Prefer the deterministic floor over a bad guess.** If the model step is unavailable or a slice is unclear, ship the skeleton with honest empty lines. A correct, sparse document beats a confident, invented one.


---

## Source: `references/frozen-8-sections.md`

## The frozen-8 solution-architecture sections

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

### The frozen set, in order

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

### The two rules that make this work

These are the only two invariants you must hold. Everything else above is guidance.

#### Rule 1 — Each fact lives in exactly one section

A given fact is rendered in **one** section and no other. The clearest case: the pattern's NFRs render
**only** in `quality_nfrs` (section 5), never also in `application_architecture` (section 4). Section 4
carries the pattern's identity, summary, topology, placement, and provenance — and deliberately stops
short of its NFRs, leaving every NFR to section 5.

Why it matters: it keeps the reconcile checks meaningful. There is exactly **one** place an NFR is
supposed to appear, so the reconcile "is this NFR addressed?" check has a single, unambiguous target.
If the same fact appeared in two sections, a reconcile check could not tell "covered" from "duplicated
in the wrong place", and the as-built diff would double-count. One fact, one home.

#### Rule 2 — Frozen order makes reconcile deterministic

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

### Practical notes for the architecture skills

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

### See also

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


---

## Source: `skills/architect/reconcile-design-vs-requirements/SKILL.md`

<details><summary>frontmatter</summary>

```yaml
name: reconcile-design-vs-requirements
description: Advisory review of a solution-architecture doc against its source-of-truth requirements/outcomes/NFRs — five checks plus a semantic drift pass; every finding is a question; under git the stale-section check reads diff/blame; never blocks merge.
one_liner: Find where a design doc has drifted from its requirements.
aliases: [design drift check, design vs requirements review, requirements traceability, design coverage check, stale design sections, does the design still match, design consistency review]
when_to_use: checking a design doc still reflects its requirements after either side changed
output_kinds: [question, halt]
deterministic_fallback: the five deterministic checks (exact-token mismatches)
suggested_tier: frontier
neighbours: |
  Before: architect/synthesise-solution-architecture (authors the design doc this checks).
  After: architect/import-external-design (merge an external design back onto the doc).
```

</details>

## Reconcile design vs requirements

Find where a solution-architecture doc has drifted from its requirements, and surface
each drift as a question for a human to resolve.

### Purpose

A solution-architecture doc is a set of markdown **sections**. Its **source of truth** is
the project's requirements: business **outcomes**, the technical requirements derived from
them, the **non-functional requirements (NFRs)**, and the **acceptance criteria**. Over a
project's life either side moves — an outcome is added, a section is edited, an NFR is
inherited from a new pattern — and the two quietly drift apart.

This skill reads the design sections against the source of truth and surfaces **drift, gaps,
and contradictions as questions a human resolves**. Run it after either side changes.

One absolute rule:

> **PROPOSE and QUESTION. NEVER issue a verdict, a status, or a pass/fail.**

Every finding is phrased as an observation or a question ("... Is it addressed?", "Should it
be re-parented or retired?"). It never says "FAIL", never sets a status, never blocks a merge.
The human reading the findings decides what to do. This is advisory tooling.

The method has two layers that stay distinct:

- A **deterministic step** — five exact-token checks. Cheap, repeatable, no model, no
  judgement. These catch literal mismatches (an outcome key that appears in no section body,
  a requirement with no acceptance criterion).
- A **semantic step** — one reasoning pass that catches the **paraphrase / contradiction
  drift** the deterministic checks miss by construction (an outcome covered only by a
  reworded paragraph, an NFR addressed under different wording, two sections that contradict
  each other). The token checks only see literal matches, so this layer is where the real
  value is.

Run the deterministic step first; it is the floor and the fallback. Run the semantic step on
top; it is the reason a reviewer was asked.

### When to use

- A design doc has been written or regenerated and you want to confirm it still reflects its
  requirements.
- A requirement, outcome, or NFR changed and you want to know which sections went stale.
- A section was hand-edited and you want to check the edit did not drift from the source of
  truth.
- Before a handover / review, as an advisory worklist of "things a human should confirm".

Do **not** use it as a merge gate. Findings inform; they do not block.

### Inputs

The user supplies (paste, attach, or point at files):

1. **The design sections** — *Required.* The markdown solution-architecture doc, ideally with
   stable `section_key`s (e.g. `background_context`, `requirements_acceptance`,
   `application_architecture`, `quality_nfrs`, `key_decisions`, `estimate_plan`,
   `open_questions`). If the doc is one file, split it on its top-level headings; each heading
   is a section. *If absent/unreadable/empty: HALT and ask where the design doc is (per
   `_shared/grounding.md`); never invent a section to reconcile.* Readable forms: a markdown
   file, a docs folder, or a pasted block.
2. **The source of truth** — *Required (at least one of outcomes / requirements / NFRs
   present).* It is the requirements the design is checked against:
   - **Business outcomes** — each with a `req_key` and its text.
   - **Derived requirements** — each with a `req_key`, its text, and its acceptance-criteria
     count (or the criteria themselves).
   - **NFRs** — each with a `req_key` (where it has one) and its text; plus any NFRs the
     adopted pattern attaches.

   *If the entire source of truth is absent: HALT and ask where the
   outcomes / requirements / NFRs live (per `_shared/grounding.md`); never invent a `req_key`
   or a requirement to check the design against. There is nothing to reconcile a design with
   no source of truth.*
3. **Orphan signal** — *Optional.* Any requirement already flagged as deriving from no current
   outcome. *If absent: skip the `orphaned_requirement` check; never fabricate an orphan flag.*
4. **Under git** — *Optional (but preferred).* The repository, so the staleness check can read
   `git diff` / `git blame` instead of a stored snapshot. See the `section_stale` note below.
   *If absent: the `section_stale` check degrades to "cannot determine from git" — never
   invent a commit sha or an edit date.*

If a `req_key` or `section_key` is supplied, use it **verbatim** in findings. Never invent a
key that does not appear in the inputs — this is the no-fabrication keystone applied to keys
(see `skills/_contract/grounding-no-absent-input`).

### Grounding (quoted)

This skill reasons over requirements, outcomes, NFRs, acceptance criteria, and design
sections, so it carries the no-fabrication keystone — see
`skills/_contract/grounding-no-absent-input`. The existing "reason only about the supplied
material; never invent a `req_key` / `section_key` that is not in the inputs verbatim"
discipline is one **instance** of this contract.

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

### The method as numbered steps

#### Step 0 — Locate / verify the required inputs (deterministic, pre-model)

Before running any check, confirm the Required inputs are present as a file-level fact: the
**design sections** and **at least one** of the source-of-truth kinds (outcomes /
requirements / NFRs). This is mechanical — absent / unreadable / empty — never a judgement on
"is there enough to reconcile."

- **Design sections absent/unreadable/empty** → emit the clean HALT below and stop.
- **The entire source of truth absent** → HALT and ask where the outcomes / requirements /
  NFRs live. (A design with no requirements to check against has nothing to reconcile — that
  is a halt, not an empty "no drift found" result.)

```
HALT — required input missing.

I can't reconcile a design against its requirements without both the design doc and the
source-of-truth requirements, and I won't invent either. Point me at the missing side and
I'll surface the drift — nothing is assumed until then.

I can read any of: a markdown file · a docs folder · an xlsx/csv path · a GitHub Project
(owner + number) · the rows pasted directly here. Which one, and where?
```

#### Step 1 — DETERMINISTIC: the five exact-token checks

Run these first. They are pure functions of the text — no model, no judgement, repeatable.
Each check sets a specific `check_kind` and, where it has one, a `req_key` and/or
`section_key`. Use **exactly** these five `check_kind` values and no others.

The full definitions live in `references/five-checks.md`; the summary:

1. **`outcome_no_design_coverage`** — an outcome's `req_key` appears as a literal token in
   **no** current section body. Set `req_key` = the outcome's key; `section_key` = null.
   (A freshly generated doc covers every outcome by construction, so in practice this is an
   *edit-drift guard*: it fires when a later edit dropped the reference.)

2. **`requirement_no_acceptance_criterion`** — a derived requirement has **zero** acceptance
   criteria. Set `req_key` = the requirement's key; `section_key` = `requirements_acceptance`.

3. **`nfr_unaddressed`** — a pattern NFR or an NF requirement is **not reflected** in the
   `quality_nfrs` section body: either its literal `req_key` is absent, or (for free-text
   NFRs) it has fewer than two keyword tokens overlapping the section body. Set `req_key` =
   the NFR's key (null for a free-text pattern NFR); `section_key` = `quality_nfrs`.

4. **`orphaned_requirement`** — a requirement flagged as deriving from no current outcome
   (`applies_status='orphaned'`). Set `req_key` = the requirement's key; `section_key` = null.

5. **`section_stale`** — a section whose source data has changed since it was generated.
   Set `section_key` = the section's key; `req_key` = null.

   **Under git, this check reads `git diff` / `git blame`, not a stored snapshot.** Version
   control answers the question "did the data this section was built from change after the
   section was last written?" directly:
   - `git log -1 --format=%cI -- <section-file>` → when the section was last touched.
   - `git log -1 --format=%cI -- <requirements-source>` → when the source of truth last
     changed.
   - If the source moved **after** the section, the section is a candidate for `section_stale`.
   - `git blame` on the changed source lines shows *what* changed, to put in the question.

   State this in the output when you raise a `section_stale` finding ("the requirements file
   was last changed in commit `<sha>` after this section was last edited").

Emit one finding per tension. Every message must read as a question.

#### Step 2 — LLM: the semantic drift pass

The deterministic step only sees literal tokens, so it is blind to meaning. This step is one
reasoning pass over the same material, looking for the drift the tokens miss. Reason about
**only the supplied material** — do not invent scope.

Look specifically for:

- **An outcome covered only by paraphrase** — the outcome's *intent* is clearly addressed in
  a section, but its `req_key` never appears, so the deterministic `outcome_no_design_coverage`
  check would false-fire (or, conversely, the key appears but the section's content actually
  addresses a *different* intent). Surface it as a question: "Outcome X seems to be covered by
  the second paragraph of Application architecture, but its key is not cited there — is X
  genuinely addressed, or is that paragraph about something else?"
- **An NFR addressed under different wording** — e.g. the NFR says "availability" and the
  quality section talks about "uptime and failover" without the word "availability". The
  token check sees no overlap and flags `nfr_unaddressed`; semantically it *is* addressed.
  Surface the reconciliation as a question.
- **A requirement with no genuinely testable criterion** — it has an acceptance criterion on
  paper, but the criterion is not actually testable ("works well"). The token check is
  satisfied; the meaning is not.
- **A contradiction between two sections** — two sections that, read together, cannot both be
  true (one section says data stays on-prem, another describes a cloud-hosted store). The
  deterministic step has no cross-section comparison; this is the semantic pass's job.
  Surface it as a `section_stale` finding against the section that contradicts the source of
  truth or the other section.

Use the **same five `check_kind` values** for semantic findings. Phrase every one as a
question. Only reference `req_key`/`section_key` values that appear verbatim in the inputs. If
everything is consistent, return no findings.

#### Step 3 — Apply dismissal memory (do not re-nag)

If the user supplies a list of previously **dismissed** findings, do not re-raise any whose
identity matches. **Identity is the tuple `(check_kind, req_key, section_key, message)`.**
Because the message is derived from stable handles (keys and item ids), not from free text, it
stays stable across a wording edit and stays distinct between two items that share a handle. A
finding the human already dismissed against unchanged evidence is **not resurrected**. If the
underlying evidence changed (the message now reads differently because the data changed), it is
a new finding and may be raised.

#### Step 4 — Assemble the worklist

Collect all deterministic + semantic findings, drop the dismissed ones, and present them as
the output below. Order them deterministic-first (they are the firm floor), then semantic
(they need a human eye). Nothing here is a verdict; it is a worklist of questions.

### Output format

Return a markdown worklist. Each finding is a question with its `check_kind`, the key(s) it
points at, and a short evidence note. Group by check, deterministic before semantic. Never a
status, never a pass/fail, never a merge verdict.

Concrete template:

```markdown
## Reconcile findings — <doc / project name>

_Advisory only. Every item is a question for a human to resolve, not a verdict._
_Deterministic checks: N · Semantic observations: M · Dismissed (unchanged): K_

### Deterministic findings

- **[outcome_no_design_coverage]** `req_key: BO-3`
  Business outcome BO-3 ("reduce onboarding time to under a day") is not referenced in any
  current design section. Should the sections be regenerated or updated to cover it?
  _Evidence: token "BO-3" absent from all section bodies._

- **[requirement_no_acceptance_criterion]** `req_key: REQ-12` · `section_key: requirements_acceptance`
  Requirement REQ-12 has no acceptance criterion. How will it be tested?
  _Evidence: acceptance-criteria count = 0._

- **[nfr_unaddressed]** `req_key: REQ-9` · `section_key: quality_nfrs`
  Requirement REQ-9 (classify: nfr, kind=availability) does not appear to be reflected in the
  Quality attributes section. Is it addressed?
  _Evidence: no keyword overlap between the requirement text and the quality_nfrs body._

- **[section_stale]** `section_key: application_architecture`
  The requirements source was last changed in commit `a1b2c3d` (2026-06-12), after this
  section was last edited (2026-05-30). Should this section be regenerated to reflect the
  current requirements?
  _Evidence: `git log` shows source changed after section; `git blame` attributes the change
  to the data-placement requirement._

### Semantic observations

- **[nfr_unaddressed]** `req_key: REQ-9` · `section_key: quality_nfrs`
  Requirement REQ-9 (classify: nfr, kind=availability) asks for "availability", and the
  Quality section discusses "uptime targets and failover" without using that word — so the
  token check above may be a false alarm. Is REQ-9 genuinely addressed by that wording?
  _Evidence: paraphrase, not literal match._

- **[section_stale]** `section_key: application_architecture`
  Application architecture states data stays on-prem, while Key decisions records a chosen
  cloud-hosted store. These two sections appear to contradict each other — which is current?
  _Evidence: cross-section contradiction; no deterministic check compares sections._
```

If everything reconciles, say so plainly — "No drift, gaps, or contradictions found against
the supplied source of truth." — and return an empty findings list. An empty result is an
honest, valid outcome.

### Notes / anti-patterns

- **Never a verdict.** The single hard rule. No "PASS", no "FAIL", no status column, no
  "blocks merge". If a sentence could be read as a ruling, rewrite it as a question. The human
  owns the disposition.
- **Advisory only.** This skill produces a worklist. It must not be wired to fail a CI
  job or block a PR. (A CI job *may* run it and post the findings as a non-blocking comment.)
- **Deterministic floor first.** Always run the five token checks even when an LLM is
  available — they are the repeatable fallback and they make the semantic pass cheaper by
  pre-flagging the literal misses. If no model is available at all, the deterministic five are
  the whole skill.
- **Don't invent scope.** Reason only about the supplied outcomes/requirements/NFRs/sections.
  Never reference a `req_key` or `section_key` that is not in the inputs verbatim. (An absent
  *required* input HALTs and asks rather than being invented — see
  `skills/_contract/grounding-no-absent-input`.)
- **Stale = git, not a snapshot.** Under version control the staleness question is answered by
  `git diff` / `git log` / `git blame` comparing when the section vs the source last changed.
  Cite the commit; do not keep a separate snapshot of the source data.
- **Respect dismissal memory.** Key it on `(check_kind, req_key, section_key, message)`. Don't
  re-nag a human about evidence they already looked at and dismissed and which has not changed.
  Derive the message from stable handles so the key survives a harmless rewording.
- **One fact, one place.** The checks assume each fact has exactly one home (an NFR is
  expected in `quality_nfrs`, nowhere else). If the doc duplicates a fact across sections, the
  `nfr_unaddressed` / coverage checks get noisier — note it, don't silently dedup.
- **Semantic pass is where the value is.** A reviewer is not needed to grep for a token. Spend
  the model budget on paraphrase coverage and cross-section contradiction — the things a
  token check structurally cannot see.

See `references/five-checks.md` for the verbatim definitions of the five deterministic checks.
