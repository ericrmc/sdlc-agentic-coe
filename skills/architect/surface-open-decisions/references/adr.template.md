# Lightweight ADR template

> A lightweight **Architecture Decision Record**. An ADR is just a markdown file a human
> writes (or appends to a decisions log) once they have chosen one option off the
> `surface-open-decisions` menu. Recording the decision and its reasoning *is* the whole
> ceremony — no enforced disposition, no blocking step. The durable value is "we chose X
> over Y because Z", not a workflow that holds the project until someone signs off.
>
> The skill produces the *menu* of open decisions; the human's pen produces the decision.
> When the agent hands over a filled template, it leaves the **chosen option blank** for
> the human to complete.

A good ADR captures: the **question**, the **option chosen**, the **options rejected** (so
the road not taken is on record), and the **rationale** for the call.

---

```markdown
# ADR-<NNN>: <the open question, restated as a title>

- **Status:** Proposed | Accepted | Superseded by ADR-<NNN>
- **Date:** <YYYY-MM-DD>
- **Kind:** data_placement | architecture | integration | other
- **Deciders:** <names / roles>

## Context
<Why this decision is open now, and what it drives — drawn from the agent_rationale.
What changes downstream depending on which way this goes.>

## Options considered
| Option | Buys | Costs | Breaks |
|--------|------|-------|--------|
| <option A> | … | … | … |
| <option B> | … | … | … |

## Decision
<The option chosen. Filled in by the human, not the agent.>

## Rationale
<Why this option over the others. The road not taken stays on record above.>

## Consequences
<What now follows from this — new constraints, follow-on decisions, evidence to produce.>
```

---

## Notes

- **The `Status` field is ADR lifecycle, not a sign-off step.** `Proposed → Accepted →
  Superseded` is the standard life of an ADR record; it does **not** block a project or
  enforce a disposition. This is advisory.
- **One ADR per genuinely open decision.** The `kind` value comes from the four-bucket
  controlled vocabulary in `surface-open-decisions`: `data_placement`, `architecture`,
  `integration`, `other`.
- **The options table is even-handed.** Every option carries a buys / costs / breaks note —
  the same symmetry the menu demands. A one-sided option in the table is the tell that a
  winner was pre-picked.
- **The road not taken stays on record.** Listing the rejected options *above* the decision
  is the point — a future reader sees what was considered and why it lost, not just what
  won.
