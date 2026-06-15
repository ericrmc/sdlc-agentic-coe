<!--
  Default PR template for the SDLC Agentic Centre of Excellence.

  Premise: there is no separate approval gate, no state machine, no governance
  disposition. Merging this PR IS the ratification. The PR / issue / commit
  history IS the audit trail. The checkboxes below are ADVISORY — they help the
  disposing human think, and they leave a durable record of what was considered.
  None of them blocks the merge. Leave them unticked if they don't apply.
-->

## 1. Which FORGE stage / skill does this serve?

<!-- Link the skill or stage this PR's proposal came out of, e.g. derive-requirements, recommend-components, design-review, convene-panel, solution-architecture, phases-releases. Paste the path or URL. -->

- Stage / skill: <!-- e.g. skills/derive-requirements/SKILL.md -->
- Related issue / project item: <!-- # or link -->

## 2. What the agent proposed

<!-- One line. What did the assistant draft? (requirements, a pattern recommendation, a design finding, an estimate, a section of the architecture doc, ...) -->

>

## 3. Who is disposing

<!-- The human accepting this. Propose -> accept: the agent drafts, you decide. -->

- Disposing human: @
- Role (advisory label): <!-- author / reviewer / architecture / practice-lead -->

## 4. Advisory ratify checks (informational — NEVER required to merge)

> These are a thinking aid, not a gate. Tick what you checked; skip what doesn't apply.
> An unticked box never blocks the merge — it just records that this one wasn't relevant or wasn't reviewed.

- [ ] The **outcomes / derived requirements still trace cleanly** — each new requirement points back to a business outcome, and nothing downstream contradicts what it claims to serve.
- [ ] **Open questions are surfaced, not tidied away** — uncertainties, "unverified — needs spike", and dissent are written down rather than smoothed over.
- [ ] The **target rule held** — the agent's proposal carries **no verdict / status / approval** of its own (no "passed", no "approved", no self-ratified state). The human decides; the agent only drafts.
- [ ] **Findings are framed as findings, not rulings** — design-review / red-team / panel output reads as evidence and options, not as a decision already made.
- [ ] If a **component pattern** is touched: it is **human PR-reviewed**, carries **evidence/artefacts of having been built**, and its **dates + validity-check + sunset/supersede** metadata are present and current.
- [ ] **No heavyweight gate snuck in** — this change stays light and advisory (no state-machine enforcement, no version-bound approval gate, no governance disposition object).

## 5. Merging this PR IS the ratification

<!--
  There is no separate sign-off step after this. When you merge:
    - the merge itself is the human acceptance (propose -> accept, completed),
    - the PR thread + commits + linked issue ARE the record of truth and the audit trail,
    - anything you decided NOT to do belongs in the PR discussion or a linked note, so the
      "why not" survives.

  No checkbox above blocks this merge. If something needs more thought, that's a comment
  or a follow-up issue — not a gate.
-->

By merging, the disposing human accepts the agent's proposal as drafted (or as amended in-thread). The conversation here is the durable "what we decided, and what we decided not to do, and why."
