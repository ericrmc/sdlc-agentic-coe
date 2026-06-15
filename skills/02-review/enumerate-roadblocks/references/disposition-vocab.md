# Roadblock disposition vocabulary (human-owned)

> The risk-analyst step **enumerates and cites** roadblocks. It assigns **no status and no severity**. Everything in this file is the **human's** to apply. A disposition only *flags drift* — it never silently re-opens or closes anything downstream; a human ratifies whether a change re-opens a prior decision.
>
> This is a **guardrail, not a gate.** No disposition freezes a workflow state, demands sign-off, or blocks the pipeline. The vocabulary exists so a human can record a deliberate, citable call against a cited constraint.

## The disposition values

A human moves each enumerated roadblock off `open` to exactly one of:

### `spike_agreed`
Use when the roadblock's evidence is flagged `unverified — needs spike:`. The human accepts that a benchmark/spike is required and **agrees to run it**. The constraint stands until the spike confirms or kills it.
- **Record:** what the spike must measure or confirm, and (optionally) who/when.
- **Effect:** the constraint remains live; the option it invalidates stays off the table until the spike result lands. When the spike completes, re-run enumeration — new evidence changes the `cited_evidence` key, so the constraint legitimately re-surfaces for fresh disposition.

### `resolved_direction`
Use when the human has **chosen a direction** that retires the constraint. The roadblock is no longer live because a decision removed its basis.
- **Record:** the direction taken (e.g. "in-perimeter model serving confirmed via X; R2 retired").
- **Effect:** the invalidated choice may now be reconsidered in light of the chosen direction. The disposition is preserved across re-runs and not re-nagged.

### `accepted_as_grey`
Use when the constraint **stands and is consciously accepted** as a known grey area — carried forward deliberately rather than resolved. This is the honest "we know, and we are proceeding with eyes open" disposition.
- **Must carry an advisory severity** (below).
- **Record:** why it is acceptable to proceed and what bounds the acceptance.
- **Effect:** the constraint is visible and accepted, not hidden. No silent drop — an accepted-as-grey roadblock stays in the register.

## Advisory severity (only on `accepted_as_grey`)

Severity is **advisory**, never enforcing. It communicates how much weight a standing, accepted constraint should carry — it does not block anything.

| Severity | Meaning |
|---|---|
| **BLOCK** | Nothing downstream is safely buildable until this is resolved. Keep it light, but treat as the top thing to clear. |
| **CAUTION** | Shapes the design — decide before committing to the invalidated choice. |
| **NOTE** | Acknowledge and bound. Low weight; carry it forward consciously. |

## Re-run / dismissal-memory contract

When enumeration is re-run for the same project + phase:

1. **Replace only the open set.** Undispositioned (`open`, agent-sourced) roadblocks are cleared and re-enumerated — re-run **replaces**, never appends.
2. **Preserve every human disposition.** `spike_agreed` / `resolved_direction` / `accepted_as_grey` roadblocks are **never deleted** by a re-run.
3. **Dismissal-memory keyed on `cited_evidence`.** Do not re-create a freshly-enumerated roadblock that matches one already dispositioned for this phase, keyed on its **cited evidence**. Same evidence ⇒ same constraint ⇒ no re-nag. New evidence (a spike result, a new finding, a newly-ratified requirement) changes the key, so the constraint re-surfaces for fresh disposition — by design.

## What a human must NOT delegate to the agent

- Setting any status or severity.
- Deciding a roadblock is "resolved," "acceptable," or "not a real constraint."
- Re-firing or closing a downstream decision because a roadblock changed.

The agent can name the constraint and cite the evidence. Only a human can say what to do about it.
