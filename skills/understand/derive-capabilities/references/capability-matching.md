# capability-matching — the deterministic backstop + the MATCHED/PROPOSED-NEW split

Companion to `derive-capabilities/SKILL.md`. The model step is the method; this is the
offline backstop and the sanity check, plus the worked split so a MATCHED tag is always
cited to a real `capabilities/INDEX.md` row and a PROPOSED-NEW need is always cited to its
requirement keys.

## The deterministic alias-match backstop (optional, NOT the primary matcher)

A pure lookup, no model call — for offline runs, regression tests, or a cross-check:

1. **Fix the legal set.** Read `capabilities/INDEX.md`. For each row, collect
   `(alias_phrase, CAP-key, fulfilment_state)`. This is the closed `CAP-` set — every
   MATCHED key must be one of these. (Mirror of `recommend-component-patterns` STEP 1.)
2. **Normalise each requirement's need.** Strip the mechanism to the underlying need
   (lower-case, drop vendor/product nouns). A requirement that names "Power Automate" or
   "Databricks" matches on the *need* phrasing ("approval routing", "analytics store"), not
   the product token.
3. **Match.** A requirement is MATCHED to a `CAP-key` when its normalised need contains, or
   is contained by, one of that capability's alias phrases. Record the `via_alias` that hit.
4. **UNMATCHED → PROPOSED-NEW.** A requirement whose need hits no alias is an UNMATCHED need;
   it drives a PROPOSED-NEW candidate (see grouping below). Never force a weak alias hit.
5. **AMBIGUOUS.** A requirement whose need hits **two or more** distinct `CAP-key`s is
   ambiguous → a `menu` row asking which (or neither), never an auto-pick.

Where the backstop and the model disagree, **prefer the model and note the divergence** — a
disagreement is usually an edge case worth a human glance.

## The same-need grouping rule (PROPOSED-NEW)

Two or more requirements that imply the **same** underlying need become **one** PROPOSED-NEW
candidate, cited by all their `req_key`s — not one candidate per requirement.

- Group by normalised need, not by wording: "a queue between services" and "an event bus for
  async messaging" are the same candidate.
- The recurrence flag is the count of distinct requirements citing the grouped need:
  - **1 requirement** → `single — confirm it recurs` (proposed-but-flagged, still listed).
  - **2+ requirements** → `recurs (N reqs)`.
- Every candidate carries its `req_key`(s) **by construction**: a need with no requirement
  behind it cannot be grouped, so it cannot appear in the menu. This is what makes
  "never invent a capability not grounded in a requirement" a structural fact, not a promise.

## Worked split — MATCHED vs PROPOSED-NEW

Input (grounded, classified requirements + `capabilities/INDEX.md` with rows
`CAP-OLAP`, `CAP-OLTP`, `CAP-AGENT-RUNTIME`):

```
REQ-7  | The application stores customer records in a relational database.
REQ-9  | The system reports on historical sales for dispatchers.
REQ-14 | We need to run our LLM agents in production.
REQ-22 | The system shall route approval requests and keep an audit trail.
REQ-31 | Services publish domain events for other services to consume.
```

Resolution against the fixed INDEX set:

| req_key | normalised need                | resolves to                  | outcome                              |
|---------|--------------------------------|------------------------------|--------------------------------------|
| REQ-7   | application database           | `CAP-OLTP` (alias hit)       | **MATCHED** — proven `PAT-WEBAPP-PG` |
| REQ-9   | reporting / analytics store    | `CAP-OLAP` (alias hit)       | **MATCHED** — proven `PAT-LAKEHOUSE-DELTA` |
| REQ-14  | run our agents in prod         | `CAP-AGENT-RUNTIME` (alias)  | **MATCHED-but-OPEN** — spikes owed   |
| REQ-22  | auditable approval routing     | no INDEX alias               | **PROPOSED-NEW** (with REQ-7? no — different need) |
| REQ-31  | event stream between services  | no INDEX alias               | **PROPOSED-NEW**                     |

Outputs:

- **MATCHED** (proposal, rides the requirement PR): `REQ-7 → CAP-OLTP`,
  `REQ-9 → CAP-OLAP`, `REQ-14 → CAP-AGENT-RUNTIME` (carry the OPEN state so
  `recommend-component-patterns` reaches honest-empty for REQ-14).
- **PROPOSED-NEW** (un-ranked menu, routed to `library/author-capability`):
  - **Workflow orchestration / auditable approval routing** — cited by REQ-22 —
    `single — confirm it recurs` (proposed key `CAP-WORKFLOW`, not yet real).
  - **Event stream between services** — cited by REQ-31 — `single — confirm it recurs`
    (proposed key `CAP-EVENT-STREAM`, not yet real).

Had a second requirement also needed approval routing, the two would collapse into **one**
PROPOSED-NEW candidate cited by both, flagged `recurs (2 reqs)`.

## The boundary, restated

- **MATCHED** keys are **real `capabilities/INDEX.md` rows** — never minted here.
- **PROPOSED-NEW** keys are **suggestions only**, always marked "(proposed — not yet a real
  key)"; they become real only if `library/author-capability` writes the file and a CODEOWNER
  ratifies.
- This skill **never** writes a capability file, sets `confidence`, or advances
  `approval_status`. It tags (MATCHED) or routes a stub (PROPOSED-NEW). The
  no-fabrication keystone lives in `skills/_contract/grounding-no-absent-input`.
