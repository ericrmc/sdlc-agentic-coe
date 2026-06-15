# FORGE Stages — the canonical 14-stage ordering (de-enforced)

> **What this is.** The advisory spine of the FORGE method: fourteen named stages in
> their natural order, each a *method label* a practitioner moves through, not a gate a
> machine enforces. This is the ordering the original bespoke platform encoded as a
> rigid 9-state machine. **We keep the ordering and the per-stage method; we drop the
> enforcement.** Nothing here blocks you. Skip a stage, loop back, run two at once —
> the spine is a map, not a turnstile.

Cited by **`sdlc-spine`** (the skill that walks a project through these stages).

---

## How to read this

- The stages are **ordered** because the method has a natural information flow — you
  cannot do a Necessity check before you have outcomes to check necessity *against*, and
  you cannot convene a panel on a solution architecture that does not yet exist. The
  order is real and load-bearing as *advice*.
- The stages are **advisory**. There is no state column, no `can_advance()`, no 409, no
  disposition that must be `pass` before the next stage opens. A stage is "done" when the
  practitioner judges it done. Loops (refine → reconcile back to outcomes) are first-class
  and expected, not exceptions the machine has to forgive.
- Each stage names **the skill(s) that serve it** so you can jump straight from "I'm at
  Solution patterns" to the markdown that runs that step.

---

## The 14 stages

The **Skill(s)** column gives the **real on-disk path** under `skills/` — the live,
nested skill directory that serves each stage. (The repo uses a 9-bucket nested
layout: `skills/01-intake-outcomes/…` through `skills/09-portfolio/…`. The 14 method
stages map onto those 9 buckets; several stages share a bucket, and a couple of
buckets host more than one stage's skills.)

| # | Stage | One line | Skill(s) that serve it (real path) |
|---|---|---|---|
| 1 | **Intake** | Capture the messy reality of the project in plain text; structure starts condensing. | `skills/01-intake-outcomes/decompose-intake-to-outcomes`, `skills/00-sdlc-spine` |
| 2 | **Outcomes** | Derive business outcomes (accept these) and the technical requirements beneath them (auto-derived, threaded by `derives_from`). | `skills/01-intake-outcomes/decompose-intake-to-outcomes`, `skills/01-intake-outcomes/classify-requirements` |
| 3 | **Review** | Adversarially challenge weak/conflicting requirements and surface risks, assumptions, and roadblocks you missed. | `skills/02-review/red-team-requirements`, `skills/02-review/surface-risks-and-assumptions`, `skills/02-review/enumerate-roadblocks` |
| 4 | **Solution patterns** | Retrieve approved patterns from the library; adopting one flows its governed NFRs in for free. | `skills/03-solution/recommend-component-patterns`, `skills/03-solution/propagate-pattern-nfrs` |
| 5 | **Solution options** | When nothing fits, explore rival candidate architectures side by side ("do nothing" always a column); narrow to a shape. | `skills/03-solution/surface-solution-options` |
| 6 | **Validation** | Replay every requirement against the chosen solution; surface the compromises it forces. | `skills/03-solution/validate-solution-vs-requirements` |
| 7 | **Necessity check** | For any specific component, ask "necessary for *which* outcome?" — the anti-gold-plating tripwire. | `skills/03-solution/necessity-check` |
| 8 | **Technical / design review** | Human technical review of the delta; design-quality lenses (WCAG/a11y, SRE, security) applied as reviewer lenses. | `skills/04-review-and-panel/design-review-findings`, `skills/04-review-and-panel/frontend-a11y-review` |
| 9 | **NFRs** | Confirm the non-functional requirements (inherited from adopted patterns + any project-specific ones) and their measurable targets. | `skills/01-intake-outcomes/nfr-coverage-check` |
| 10 | **Convene panel** | Battle-test the design with a multi-perspective panel (build/break/cost/ops lenses); record dissent as first-class. | `skills/04-review-and-panel/convene-a-panel`, `skills/04-review-and-panel/synthesise-panel`, `skills/04-review-and-panel/red-team-and-dissent`, `skills/04-review-and-panel/surface-open-decisions` |
| 11 | **Solution architecture** | Read the codebase and synthesise the source-of-truth design document, section by section. | `skills/05-solution-architecture/synthesise-solution-architecture`, `skills/05-solution-architecture/reconcile-design-vs-requirements`, `skills/05-solution-architecture/import-external-design`, `skills/05-solution-architecture/reconcile-as-built` |
| 12 | **Phases / MVP / Pilot / Production** | Lay out the delivery maturity ladder; each phase a labelled checkpoint over the same design, with its own (advisory) UAT. | `skills/07-lifecycle/describe-phases-releases-waves`, `skills/07-lifecycle/help-implement-a-wave`, `skills/07-lifecycle/triage-backlog-and-defer`, `skills/07-lifecycle/scope-reconcile-check` |
| 13 | **Releases** | Plan ongoing add/change/remove/patch releases as traced deltas to the source of truth — "what changed, and why, release over release". | `skills/07-lifecycle/describe-phases-releases-waves` |
| 14 | **Pattern-library promotion** | Promote a successful net-new design back into the approved library so the next project fast-tracks what this one explored. | `skills/08-pattern-library/author-component-pattern`, `skills/08-pattern-library/pattern-library-curate` |

> **Cross-cutting (not a numbered stage): Portfolio.** Above the per-project journey,
> `skills/09-portfolio/portfolio-phase-health` and
> `skills/09-portfolio/advisory-governance-checklist` read *across* projects (RAG health,
> the light advisory governance pass) rather than advancing one.
>
> The paths above are the **real, on-disk** skill directories. `skills/00-sdlc-spine` is
> the orchestrator that knows this whole ordering; the per-stage skills are the depth
> behind each label.

---

## The stages, in detail

### 1 — Intake
**Method:** Capture whatever already exists about the project — a brief, a Slack thread,
a half-formed idea — as plain text. No template to fill, no picker to choose from. The
front door *is* the act of typing context in. Enough context is a *threshold*, not a
submit button.
**Serves it:** `skills/01-intake-outcomes/decompose-intake-to-outcomes`, `skills/00-sdlc-spine`.

### 2 — Outcomes
**Method:** Decompose the intake into a short stack of **business outcomes** (the few
things that are genuine commitments — these are what a human accepts) and, beneath each,
the **technical requirements** that serve it. Technical requirements, classifications, and
NFRs are *derived and auto-applied*, never accepted one box at a time — but every derived
requirement is threaded by a `derives_from` edge back to the outcome it serves, so a
rejected outcome visibly orphans its subtree. This is the keystone: accept HIGH, derive
LOW.
**Serves it:** `skills/01-intake-outcomes/decompose-intake-to-outcomes`, `skills/01-intake-outcomes/classify-requirements`.

### 3 — Review
**Method:** Two passes in parallel. **Adversarial:** challenge weak, vague, or conflicting
requirements — surface the assumption beneath a conflict rather than just flagging it.
**Exploratory:** surface *adjacent* outcomes the intake implies but didn't state ("similar
engagements also needed an audit-trail export — add an outcome?"). Output is *cues, not
commands* — each a question naming its target, dismissible, with dismissal-memory so the
same note never re-prompts against unchanged evidence. **A review that yields zero notes
is a legitimate, non-failing outcome.**
**Serves it:** `skills/02-review/red-team-requirements`, `skills/02-review/surface-risks-and-assumptions`, `skills/02-review/enumerate-roadblocks`.

### 4 — Solution patterns
**Method:** The solution space is a **retrieval** over the firm's approved Pattern
Library, never a from-scratch generation. Rank the real, PR-validated patterns by computed
similarity to this project's outcomes; show provenance (where each was used before, what
adopters kept, what they overrode). **Adopting a pattern flows its `attached_nfrs` into the
project automatically** as derived requirements — the economic payoff. This is the fast
path and should be the most prominent move.
**Serves it:** `skills/03-solution/recommend-component-patterns`, `skills/03-solution/propagate-pattern-nfrs`.

### 5 — Solution options
**Method:** When retrieval returns no approved match, explore. Populate rival candidate
architectures side by side; **"do nothing" is always a column.** Narrow by pick / merge /
kill. Roadblocks the exploration hits are recorded as *cited facts* with human-owned
status (no agent-asserted feasibility verdict). On landing a shape, ask "promote to the
pattern library?" — every expensive explore should seed a future fast-track.
**Serves it:** `skills/03-solution/surface-solution-options`.

### 6 — Validation
**Method:** Replay every requirement back against the chosen solution's enforced
constraints. Satisfied requirements settle quietly; **compromises surface** — "the pattern
enforces async writes; your 'instant confirmation' outcome degrades to '≤2s'." Each
compromise walks the trace edge *upward* to the business outcome and capability it dents,
so nothing is silently dropped. The human accepts or rejects each compromise — these are
contested calls, genuinely human.
**Serves it:** `skills/03-solution/validate-solution-vs-requirements`.

### 7 — Necessity check
**Method:** Point at any specific component and ask the one question that prevents
over-engineering: *"necessary for which outcome?"* — computing over-reach relative to a
named outcome's NFRs and posing the question naming both ids ("Redis serves only
'sub-200ms search', already met by the adopted pattern — necessary, or cut?"). The method
never asserts "this is gold-plated"; it raises the flag and **the human decides.**
Answerable only because the trace edge exists. **Zero cuts is a legitimate outcome.**
**Serves it:** `skills/03-solution/necessity-check`.

### 8 — Technical / design review
**Method:** Human technical review of the **delta since last reviewed**. Design-quality
lenses — accessibility (WCAG/a11y), SRE/reliability, security — are *lenses a reviewer
adopts*, not provisioned seats or checkboxes. Order what's reviewed by deterministic
consequence, not by a suggested disposition. Record dissent as first-class. **A review
that accepts nothing is legitimate; no acceptance-rate metric exists.**
**Serves it:** `skills/04-review-and-panel/design-review-findings`, `skills/04-review-and-panel/frontend-a11y-review`.

### 9 — NFRs
**Method:** Confirm the non-functional requirements. Most arrive *inherited* — flowed in
when a pattern was adopted in Stage 4 — pre-approved and traced to that pattern. Add any
project-specific NFRs and pin each to a **measurable target** (latency, availability,
RPO/RTO, a11y conformance level, etc.). NFRs are derived-and-applied like other technical
requirements, but their *targets* are the kind of thing worth a human eye.
**Serves it:** `skills/01-intake-outcomes/nfr-coverage-check`.

### 10 — Convene panel
**Method:** Battle-test the design with a multi-perspective panel — distinct lenses
(builder, breaker, cost, ops/SRE, security) run over the same design and argue. Surface
failure modes, contested assumptions, and the calls the panel disagrees on. **Preserve
dissent:** what was decided *not* to do, and why, is recorded as a first-class node, not
smoothed away. The panel informs; the human still owns the decision.
**Serves it:** `skills/04-review-and-panel/convene-a-panel`, `skills/04-review-and-panel/synthesise-panel`, `skills/04-review-and-panel/red-team-and-dissent`, `skills/04-review-and-panel/surface-open-decisions`.

### 11 — Solution architecture
**Method:** Read the (existing or target) codebase and **synthesise the source-of-truth
design document, section by section.** This is the durable artefact from which every
downstream projection is derived — exec summary, diagrams, estimates, the build spec.
Change is controlled by re-version, not by re-authoring: a targeted edit regenerates only
the affected sections, which are then reconciled and re-accepted.
**Serves it:** `skills/05-solution-architecture/synthesise-solution-architecture`, `skills/05-solution-architecture/reconcile-design-vs-requirements`.

### 12 — Phases / MVP / Pilot / Production
**Method:** Lay out the delivery-maturity ladder past the design: **Prototype → MVP →
Pilot → Production.** Each phase is a *labelled checkpoint over the same design sections*
(by pointer, not a copy), with its own UAT. The UAT is an **advisory** acceptance gate —
agentic UAT (a browser harness pre-filling evidence) can assist, but a human is always the
ratifier. A project may skip phases; the order is the real sequence entered, not a forced
march.
**Serves it:** `skills/07-lifecycle/describe-phases-releases-waves`, `skills/07-lifecycle/help-implement-a-wave`.

### 13 — Releases
**Method:** Production is not the end. Plan the ongoing stream of releases — each a
**scoped, versioned delta** to the source of truth that *adds / changes / removes /
patches* requirements, every delta traced to the outcome it serves. A release holds no
design of its own; it points at requirements and drives the existing change-control loop
(targeted edit → regenerate affected sections → reconcile → accept → re-version). This
makes *"what changed, and why, release over release"* answerable — the thing a ticket pile
cannot tell you. Release notes and an exec summary are projections off the release record.
**Serves it:** `skills/07-lifecycle/describe-phases-releases-waves`.

### 14 — Pattern-library promotion
**Method:** Close the loop. When a project lands a successful **net-new** design (one that
wasn't an existing pattern in Stage 4), promote it into the approved Pattern Library —
PR-reviewed by a human, carrying the evidence/artefacts that it was actually built, with
dates, a validity check, and sunset/supersede metadata. The next delivery lead then
*fast-tracks* what this project explored. Promotion is an architect's deliberate
acceptance, never automatic.
**Serves it:** `skills/08-pattern-library/author-component-pattern`, `skills/08-pattern-library/pattern-library-curate`.

---

## The legacy 9-state machine — what we kept and what we dropped

The original bespoke platform encoded **this same ordering** as a rigid, enforced
finite-state machine. Its spine was nine states, with `can_advance()` gates that returned
a 409 if a stage's pre-conditions weren't met, and a constrained send-back routing rule:

```
draft
  → requirements_proposed
  → requirements_ratified
  → comparators_suggested
  → design_in_review
  → decisions_recorded
  → estimated
  → governance_checks
  → approved
```

Those nine states **are the same method as the fourteen stages above** — just collapsed
and, crucially, *enforced*. Mapping the legacy encoding onto the de-enforced spine:

| Legacy state | Enforced gate (what it blocked on) | FORGE stage(s) it encoded |
|---|---|---|
| `draft` | — (entry; advanced via `propose`) | **1 Intake** |
| `requirements_proposed` | — | **2 Outcomes** |
| `requirements_ratified` | explicit human advance | end of **2 Outcomes** / **3 Review** |
| `comparators_suggested` | "confirm ≥1 comparator" | **4 Solution patterns** / **5 Solution options** |
| `design_in_review` | "design must be reviewed *and* a pattern settled" | **6 Validation** + **7 Necessity** + **8 Technical/design review** |
| `decisions_recorded` | "ratify every drafted decision; ≥1 ratified" | **10 Convene panel** (decisions/dissent) |
| `estimated` | "accept the estimate" | folds into **11 Solution architecture** projections |
| `governance_checks` | "every required check disposed pass / pass-with-conditions" | the **approval gate** (dropped) |
| `approved` | — (terminal) | **11 Solution architecture** onward (**12–14** co-own it) |

**What we KEEP:** the *ordering* and the *per-stage method*. The information flow is real
— outcomes before patterns before validation before architecture before phases before
releases — and every stage's technique (derive-low/accept-high, retrieval-not-generation,
the necessity question, panel + dissent, section-by-section synthesis, traced release
deltas) carries over verbatim. The fourteen stages are simply the nine states *expanded*
to name the steps the machine had bundled together.

**What we DROP:** the *enforcement*. Specifically gone —

- **The state column and `STATE_ORDER`.** No project carries a `workflow_state`; there is
  no single position to advance.
- **`can_advance()` and the 409.** No gate condition blocks the next stage. "Confirm ≥1
  comparator", "the design must be reviewed", "ratify every drafted decision", "accept the
  estimate", "every required check disposed pass" — all become *advice the skill offers*,
  never a precondition a machine enforces.
- **Governance disposition as a gate.** `governance_checks` → `approved` was a
  state-machine-enforced approval gate. It is replaced by **light, advisory** review
  (Stage 8) and panel (Stage 10): you are *prompted* to review, never *prevented* from
  proceeding.
- **The constrained send-back routing.** `can_send_back()` allowed routing only to four
  "meaningful re-entry points" and only strictly backward. In the de-enforced spine you
  loop freely — refine → reconcile back to Outcomes, re-open architecture from a release —
  with no routing rule to satisfy.

The method survives; the turnstile does not. Where the legacy system said *"you may not
advance until…"*, the FORGE spine says *"the natural next step is… (here's the skill)"*.
Everything is light and advisory — a practitioner's map, run in any LLM workflow that can
read markdown.
