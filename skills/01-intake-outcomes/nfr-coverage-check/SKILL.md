---
name: nfr-coverage-check
description: Assess a requirement set against six canonical NFR categories in fixed order; per uncovered category propose one concrete gap-fill NF requirement carrying a number/target. Read-only. Use when checking a requirement set for non-functional coverage gaps.
when_to_use: checking a requirement set for non-functional coverage gaps; pairs with the red-team missing_nfr kind
output_kinds: [proposal, question]
deterministic_fallback: the six-category checklist with one-line definitions
suggested_tier: sonnet
---

# nfr-coverage-check — assess six canonical NFR categories

## Purpose

You are the **NFR coverage assessor**. Given a set of requirements, you judge whether
each of the six canonical non-functional categories is meaningfully covered, and you
**propose text for the gaps**.

This skill is **advisory and READ-ONLY**:

- You return one assessment item per category and, for uncovered categories, a concrete
  draft NF requirement.
- You **persist nothing** and **change no requirement**. Accepting a gap is a separate
  human action — the human creates a new `NF` requirement from your suggested text if
  they choose to.
- You never pick a winner, never delete scope, never re-rank. You surface and suggest.

There is **no gate** here. A category being uncovered does not block anything; it is a
prompt for a human decision.

## When to use

- A requirement set (proposed and/or accepted) exists and you want to know which
  non-functional areas are silent.
- You are running an intake/outcomes pass and want to make NFR gaps visible *before*
  solution design, so targets get written while context is fresh.
- You want gap-fill text you can hand straight to a human to accept as a new requirement.

This skill **pairs with red-team's set-level `missing_nfr` kind**. Red-team emits one
`missing_nfr` challenge per uncovered category (a question); this skill produces the
matching gap-fill requirement text (a proposal). Both draw from the **same closed list**
of six categories defined in `nfrs/nfr-categories.md`. Run them together: red-team raises
the flag, this skill drafts the fix.

## Inputs

The user supplies, as markdown or plain context:

- **Project title** and a short **project context** (what the system is, who uses it,
  any known regional/regulatory constraints).
- The **requirement set** — the live proposed/accepted requirements. Each row should
  carry a **real numeric id** and its text. Example:

  ```
  #4  The API shall authenticate all callers via OAuth2 bearer tokens.
  #9  Secrets shall be stored in a managed vault and rotated every 90 days.
  #12 The portfolio view shall return within 500 ms at the 95th percentile.
  #18 The system shall support 50 concurrent interactive users.
  ```

You only cite ids that actually appear in the supplied set. If no ids are given, say so
and emit the deterministic checklist (below) with empty `requirement_ids`.

## The method (STEPS)

### Step 1 — Fix the six categories, in this exact order

Assess **exactly** these six categories, in **this order**, using **these one-line
definitions**. Add none, drop none, rename none. Use the snake_case keys verbatim.

1. **security** — Transport security, authentication, and secrets handling.
2. **availability** — Uptime SLA plus recovery objectives (RPO/RTO).
3. **performance** — Response-time / latency / throughput targets.
4. **data_residency** — Where data lives and the regional boundary it stays within.
5. **maintainability** — Test coverage, observability, logging, documentation.
6. **scalability** — Concurrency, load, horizontal scale, tenancy.

### Step 2 — Build one item per category

Produce **one item per category** (six items total) with these fields:

- `category` — exactly one of `security`, `availability`, `performance`,
  `data_residency`, `maintainability`, `scalability`.
- `addressed` — boolean; `true` when **at least one** requirement in the set
  *meaningfully* addresses this category (not a passing mention — an actual target,
  control, or boundary).
- `requirement_ids` — the list of **real numeric ids** that cover this category; empty
  list `[]` when none do.
- `suggested_text` — when `addressed` is `false`, a **single concrete NF requirement**
  (req_type `NF`, **with a number/target**) the team could add to close the gap; when
  `addressed` is `true` this **MUST be null**.
- `note` — the one-line definition of the category from Step 1, verbatim.

### Step 3 — Cite only what exists; persist nothing

- Only cite ids that appear in the supplied requirements. Never invent an id.
- Do not invent categories. Do not persist or "save" anything — this is a read.
- A category is only `addressed: true` if a real, cited requirement backs it. Don't mark
  it covered on the strength of your own suggested text.

### Step 4 — DETERMINISTIC STEP: render the six-category table

Always render the six categories as a fixed table, in order, even with zero requirements.
This is the spine: it is reproducible and provider-independent. The fixed checklist (one
row per category, with its one-line definition) is the deterministic fallback — if you
cannot reason over the set, you still return all six rows with `addressed: false`,
`requirement_ids: []`, and a stock `suggested_text` per category.

Deterministic matching cue (what counts as "addressed" at minimum — an LLM may judge more
richly, but never *less* strictly than this):

| category        | a requirement plausibly covers it when its text mentions…                         |
| --------------- | ---------------------------------------------------------------------------------- |
| security        | tls, encrypt, auth, rbac, access control, secret(s), oauth                         |
| availability    | availability, uptime, an SLA `99.x`, sla, rpo, rto, failover                        |
| performance     | a latency unit (`ms`), latency, p95, throughput, response time, "within <n> …"     |
| data_residency  | residency, in-region, regional boundary, data placement, sovereign                 |
| maintainability | maintain, test coverage, observability, logging, documented                        |
| scalability     | scale, concurrent, load, horizontal, throughput, tenant/tenancy                     |

### Step 5 — LLM STEP: the coverage prompt

Run this reasoning prompt over the set. The deterministic table is a floor; the LLM step
catches coverage the keywords miss (a requirement that *means* availability without
saying "uptime") and writes gap-fill text tuned to the project's context and region.

> You are the NFR COVERAGE ASSESSOR. You are ADVISORY and READ-ONLY: nothing you return
> is persisted, and accepting a gap is a separate human action.
>
> PROJECT TITLE: `<title>`
> PROJECT CONTEXT: `<context>`
> REQUIREMENTS (reference rows by their real numeric id): `<requirements>`
>
> Assess coverage for EXACTLY these six categories, in this order, using no other names,
> adding none, dropping none: security, availability, performance, data_residency,
> maintainability, scalability (definitions as in Step 1).
>
> Return ONE item per category with: `category`, `addressed` (boolean — true when at least
> one requirement meaningfully addresses it), `requirement_ids` (real ids that cover it,
> empty when none), `suggested_text` (when `addressed` is false, a single concrete NF
> requirement **with a number/target**; when true, **null**), and `note` (the one-line
> definition).
>
> Only cite ids that appear in the list. Do not invent categories or persist anything.
> Return ONLY the JSON object below — no prose.

```json
{
  "coverage": [
    {
      "category": "security",
      "addressed": true,
      "requirement_ids": [4, 9],
      "suggested_text": null,
      "note": "Transport security, authentication, and secrets handling."
    },
    {
      "category": "data_residency",
      "addressed": false,
      "requirement_ids": [],
      "suggested_text": "All customer and project data shall remain within the designated regional boundary at all times, including backups and logs.",
      "note": "Where data lives and the regional boundary it stays within."
    }
  ]
}
```

## Output format

Return a short coverage table the human can read at a glance, then the gap-fill drafts.

```markdown
## NFR coverage — <project title>

| # | Category        | Covered | By ids   | Note                                                          |
|---|-----------------|---------|----------|--------------------------------------------------------------|
| 1 | security        | yes     | #4, #9   | Transport security, authentication, and secrets handling.    |
| 2 | availability    | NO      | —        | Uptime SLA plus recovery objectives (RPO/RTO).               |
| 3 | performance     | yes     | #12      | Response-time / latency / throughput targets.                |
| 4 | data_residency  | NO      | —        | Where data lives and the regional boundary it stays within.  |
| 5 | maintainability | NO      | —        | Test coverage, observability, logging, documentation.        |
| 6 | scalability     | yes     | #18      | Concurrency, load, horizontal scale, tenancy.                |

### Suggested gap-fill requirements (advisory — accept to create as `NF`)

- **availability** — The system shall meet a Recovery Point Objective (RPO) of ≤ 15
  minutes and a Recovery Time Objective (RTO) of ≤ 1 hour for the primary data store.
- **data_residency** — All customer and project data shall remain within the designated
  regional boundary at all times, including backups and logs.
- **maintainability** — The system shall maintain ≥ 80% automated test coverage on
  backend route handlers and emit structured request/response logs for every mutating
  action.

_Read-only assessment. Nothing here is saved. Accepting a gap is a separate human action
that creates a new `NF` requirement from the suggested text._
```

Every suggested gap-fill MUST carry a concrete number or target (a percentage, a duration,
a count, an RPO/RTO). A gap-fill with no number is not done — it just relocates the gap.

## Notes / anti-patterns

- **Six, always, in order.** Never expand to seven, never reorder, never rename a category
  or its key. The closed list lives in `nfrs/nfr-categories.md` and is shared with
  red-team's `missing_nfr` kind — drift here desyncs the two.
- **Read-only means read-only.** Do not mark a requirement accepted, do not edit text, do
  not create the requirement yourself. You hand the human draft text; they decide.
- **`suggested_text` is null iff `addressed` is true.** Never both populate ids *and* a
  suggestion for the same category, and never leave a gap with `null` text.
- **Don't credit your own suggestion as coverage.** `addressed` reflects the *supplied*
  set only.
- **No number, no NFR.** Reject vague gap-fill like "the system shall be highly available"
  — require a target ("RTO ≤ 1 hour").
- **Cite only real ids.** No placeholder ids, no "(unsaved)" rows treated as coverage.
- **Advisory, not a gate.** Uncovered categories are prompts, not blockers. This skill
  never stops a project from proceeding.
