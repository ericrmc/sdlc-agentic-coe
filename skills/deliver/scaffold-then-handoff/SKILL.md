---
name: scaffold-then-handoff
description: The shared convention the brief skills compose — build a deterministic, fact-grounded section base first (open-questions lead, an honest "None flagged." fallback in every section, a fenced paste-ready prompt for the downstream specialist), then run an optional model enrich pass that keeps every fact and invents no scope, falling back to the base on any error. Use when authoring any handoff brief for a downstream specialist (testing, design studio, build).
one_liner: Scaffold a fact-grounded handoff brief, then optionally enrich it.
aliases:
  - handoff brief
  - briefing template
  - work package handoff
  - delegate to a specialist
  - paste-ready prompt for an agent
  - package context for a downstream team
  - scaffold a brief
when_to_use: authoring any handoff brief for a downstream specialist (testing, design studio, build)
output_kinds: [proposal]
deterministic_fallback: the section base itself (the whole point)
suggested_tier: mid
neighbours: |
  Before: deliver/scope-reconcile-check (confirm scope is settled before packaging it).
  After: deliver/testing-brief-scaffold, deliver/design-studio-brief-scaffold,
  deliver/comparator-grounded-estimate (the brief skills that compose this convention).
---

# scaffold-then-handoff

Author a handoff brief for a downstream specialist: build the brief from facts
first, then optionally sharpen its prose.

This is a **convention doc**, not a brief skill. It supplies the shape, the
discipline, and the failure mode that the brief skills compose:
[`testing-brief-scaffold`](../testing-brief-scaffold/SKILL.md),
[`design-studio-brief-scaffold`](../design-studio-brief-scaffold/SKILL.md), and
[`comparator-grounded-estimate`](../comparator-grounded-estimate/SKILL.md). Read
this once, then read the specific brief skill — that one supplies the section
list; this one supplies the shape, the discipline, and the failure mode.

## Purpose

Scaffold a handoff brief and hand it off. Do not execute or store the
specialist's work.

A handoff brief is a structured package assembled from facts already on hand —
the project's outcomes, derived requirements, acceptance criteria, brand
baseline, panel synthesis — so a downstream specialist (a testing agent, a
design studio, a build agent) can pick up the work cold and run with it.

Two things this convention deliberately does **not** do:

- It does **not** do the specialist's job. The brief does not write the tests,
  render the mockups, or build the feature. It is the *brief* that lets someone
  (or some agent) do that work well.
- It does **not** store what comes back. Returned assets — test specs, reports,
  style guides, token sets, mockups, built code — re-enter as **references in the
  repo**, not as stored binaries. The brief points outward; the artefacts live
  where the work lives. When a specialist returns something, capture a pointer (a
  path, a PR link, a commit), never the blob.

## When to use

Use this convention whenever authoring a brief that hands work to a downstream
specialist:

- **Testing** → a deterministic test charter for a testing agent.
- **Design** → a brand-aligned design & branding brief for a design studio.
- **Build** → an implementation handoff for a build/coding agent.

A brief that fits none of those is still on safe ground: the base shape below
works for any "package context, someone else executes" handoff. Add a new brief
skill that names its own sections and composes this convention.

## Inputs

The user (or the composing brief skill) supplies project context as markdown or
structured facts. Typical inputs:

- **Project title + one-line intake / description.**
- **Accepted outcomes** (the business outcomes upstream agreed to pursue).
- **Derived requirements traced to those outcomes**, with **acceptance criteria**.
- **Anything orphaned** — requirements with no clear parent outcome, brand not
  yet captured, outcomes not yet accepted. These become open questions.
- **Optional panel / red-team synthesis** — if a deliberation panel or red-team
  pass shaped the work, its output folds into a dedicated input slot.

Not all of it is required. The convention's whole point is that a thin context
still produces a real, honest brief — see the "None flagged." rule below.

## The method (numbered steps)

The convention is two passes. **Step 1 always runs and is the deliverable on its
own. Step 2 is optional and never gets to lower the quality of Step 1.**

### Step 1 — Build the deterministic section base (the deliverable)

Assemble the brief from facts only. No model call, no network, no invention.
This is the contract:

1. **Open questions lead.** The first real section after the title/preamble is
   **always** "Open questions (read first)". The specialist must see what is
   uncertain *before* they see the plan. This is house style; do not bury it.

2. **Every section always renders — with an honest fallback.** Walk the full
   section list for the brief kind. A section never disappears because its data
   is empty. If there is nothing to say, the section still renders with a plain,
   honest line — `None flagged.` for open questions, or a one-line `_No X yet —
   do Y upstream to seed this._` note that tells the reader *why* it's empty and
   *what would fill it*. An empty-but-present section is information; a missing
   section is a silent hole.

3. **Include a fenced, paste-ready prompt for the specialist.** Near the end,
   emit a fenced code block (```) containing a prompt the user can paste
   straight into the downstream agent. It names the project, points at the brief
   above it, and states the discipline boundary (e.g. *"raise defects as
   findings — do not fix them"*, *"reuse the client's brand — do not
   re-derive it"*). Paste-ready means: no placeholders left to fill, no
   "[insert here]". If a fact is missing, the open-questions section carries it,
   not the prompt.

4. **Provide an optional input slot for the panel / red-team.** Reserve a
   section (e.g. "From the panel" / "From the red-team") that folds in
   deliberation or adversarial-review output when present, and renders an honest
   "_no panel convened yet — convene it to shape this brief, then regenerate_"
   note when absent. This is the seam where upstream deliberation reaches the
   specialist.

5. **Never raise.** Base assembly tolerates missing keys, wrong types, empty
   lists. A malformed input degrades to a "None flagged." line, never to a stack
   trace. The base is the safety net for everything downstream.

At the end of Step 1 there is a complete, fact-grounded, paste-ready brief. **If
no model is available, the work is done — ship the base.**

### Step 2 — Optional model enrich pass (prose only)

Hand the base to a model to sharpen the prose into a warmer, clearer brief.
This pass is a *prose enhancement*, not a re-authoring. Ground it hard:

1. **Feed the model the base as the source of truth.** The prompt's job is
   "improve and enrich this — keep its facts and structure," not "write a brief
   about this project." The base goes *into* the prompt as the scaffold to
   polish.

2. **Three non-negotiable instructions** to the enrich pass:
   - **Keep every fact.** Do not drop, alter, or contradict anything in the
     base. Same outcomes, same requirements, same acceptance criteria, same
     brand baseline.
   - **Invent no scope.** No new requirements, no new surfaces, no brand details
     that weren't captured, no acceptance criteria that weren't traced. If
     something is missing, it stays an open question — it does not get
     hallucinated into existence.
   - **Lead with open questions.** Preserve house style; the enriched brief still
     opens on what's uncertain.

3. **Fall back to the base on ANY error.** If the model call fails, times out,
   returns malformed output, or returns empty — return the Step-1 base
   unchanged. The enrich pass can only ever *improve*; it can never *block* or
   *degrade*. A caught exception is a quiet fallback, not a failure.

The net effect: with a model, the result is a polished brief grounded on the
base; without one (or on any model error) the result is the base, which was
already a complete, honest, paste-ready deliverable.

## Output format

A single markdown brief. The exact section list comes from the composing brief
skill; the **shape** is fixed by this convention:

```markdown
# <Kind> handoff — <Project title>

> One-line preamble: what this is, who it's for, and the
> scaffold-not-store boundary ("this scaffolds X — it does not run or store it").

## Open questions (read first)
- <specific, fact-derived question>            ← or, if none:
- None flagged. <one honest line confirming the next thing to check.>

## <Section A — the substance for this brief kind>
<rendered from facts; or an honest "_No X yet — do Y upstream to seed this._">

## <Section B — ...>
<... every section in the list renders, always ...>

## <Handoff / studio / build prompt — paste into the specialist>
```
<A complete, paste-ready prompt. Names the project, points at the brief
above, states the discipline boundary. No placeholders.>
```

## From the panel / red-team
<folded-in synthesis when present; or an honest "_none convened yet_" note.>
```

### Concrete example (testing brief, thin context)

A project with one accepted outcome, one derived requirement with two acceptance
criteria, and no panel yet — the base alone produces:

```markdown
# Testing handoff — Acme Returns Portal

> A scaffold assembled from project facts. Sharpen it, then hand this to a
> testing agent. This scaffolds testing — it does not run or store the tests.

## Open questions (read first)
- None flagged. Confirm the acceptance criteria below are complete + testable.

## What to prove (test charter)
### OUT-1 — Customers can self-serve a return without contacting support
- `REQ-3` (F) The portal accepts an order number and emails a prepaid label.
    - PROVE: A valid order number returns a downloadable label within 5s.
    - PROVE: An invalid order number shows a recoverable, specific error.

## Approach
- Framework: deterministic browser end-to-end (auto-waiting, headless).
- Determinism: run against seeded data; assert post-state, no fixed sleeps.
- Scaffold, not store: specs + reports live in the repo, not with the brief.

## Handoff prompt (paste into a testing agent)
```
Write and run deterministic end-to-end browser tests for Acme Returns Portal.
Prove each acceptance criterion in the test charter above. Use a seeded,
deterministic environment. Report pass/fail per charter item; raise product
defects as findings — do not fix them.
```

## From the panel
_No panel convened + synthesised yet. Convene the panel to shape this brief,
then regenerate._
```

That brief is shippable with zero model calls. The enrich pass would warm the
prose and tighten the prompt — it would not add a single requirement.

## Notes / anti-patterns

- **Anti-pattern: the enrich pass authors the brief.** If the model is doing the
  thinking and the base is an afterthought, the convention is inverted. The base
  is the deliverable; the model polishes.
- **Anti-pattern: a section vanishes when empty.** A missing section reads as
  "nothing to flag here" when the truth is "no data here." Render it with an
  honest fallback so the reader knows the difference.
- **Anti-pattern: placeholders in the paste-ready prompt.** A `[fill in scope]`
  in the fenced block means the prompt isn't paste-ready. Missing facts belong in
  open questions, never in the prompt.
- **Anti-pattern: storing what comes back.** Returned specs, reports, mockups,
  tokens, and code are references, not stored blobs. Capture a path / PR link /
  commit; let the artefact live where the work lives.
- **Anti-pattern: the enrich pass that can fail loudly.** Any model error must
  fall back to the base silently. The brief is never blocked by an enrichment
  that didn't land.
- **Anti-pattern: inventing scope to look complete.** A thin brief that honestly
  flags its gaps is worth more than a plump one with hallucinated requirements.
  Open questions are a feature, not an embarrassment.
- This is light and advisory. A brief carries no approval state and no blocking
  check. It is a starting point for a conversation with a specialist, not a
  contract that must pass review.
