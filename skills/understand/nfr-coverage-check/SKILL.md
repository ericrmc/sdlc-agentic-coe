---
name: nfr-coverage-check
description: Assess a requirement set against six canonical NFR categories in fixed order; per uncovered category propose one concrete gap-fill non-functional requirement carrying a number/target. Read-only. Use when checking a requirement set for non-functional coverage gaps.
one_liner: Check a requirement set for gaps across six canonical NFR categories.
aliases: [nfr coverage, non-functional requirements check, quality attribute gaps, missing nfrs, nfr gap analysis, performance security availability check, non-functional coverage]
when_to_use: checking a requirement set for non-functional coverage gaps
output_kinds: [proposal, question]
deterministic_fallback: the six-category checklist with one-line definitions
suggested_tier: mid
neighbours: |
  before: understand/classify-requirements (flags unquantified requirements this then checks for category coverage)
  after: challenge/red-team-requirements (raises a missing_nfr challenge per uncovered category; this drafts the matching fix)
---

# nfr-coverage-check — assess six canonical NFR categories

## Purpose

Assess a requirement set for non-functional coverage gaps and draft text to fill them.
Given a set of requirements, judge whether each of the six canonical non-functional
categories is meaningfully covered, and **propose text for the gaps**.

This skill is **advisory and read-only**:

- Return one assessment item per category and, for uncovered categories, a concrete
  draft non-functional requirement.
- Persist nothing and change no requirement. Accepting a gap is a separate human action:
  the human creates a new `REQ-<n>` (classified non-functional) from the suggested text
  if they choose to. Functional vs non-functional is classify metadata, never part of the
  key — there is no `NF-` key.
- Never pick a winner, never delete scope, never re-rank. Surface and suggest.

An uncovered category does not block anything; it is a prompt for a human decision.

## When to use

- A requirement set (proposed and/or accepted) exists and you want to know which
  non-functional areas are silent.
- You want NFR gaps visible *before* solution design, so targets get written while
  context is fresh.
- You want gap-fill text to hand straight to a human to accept as a new requirement.

This skill is the proposal half of a pair. `challenge/red-team-requirements` emits one
`missing_nfr` challenge (a question) per uncovered category; this skill produces the
matching gap-fill requirement text (a proposal). Both draw from the **same closed list**
of six categories in `nfrs/nfr-categories.md` — one raises the flag, the other drafts the
fix.

## Inputs

The user supplies, as markdown or plain context:

- **Project title** and a short **project context** (what the system is, who uses it,
  any known regional/regulatory constraints).
- The **requirement set** — the live proposed/accepted requirements. Each row should
  carry its `REQ-<n>` key (or a bare integer index that maps to one) and its text.
  Example:

  ```
  REQ-4   The API shall authenticate all callers via OAuth2 bearer tokens.
  REQ-9   Secrets shall be stored in a managed vault and rotated every 90 days.
  REQ-12  The portfolio view shall return within 500 ms at the 95th percentile.
  REQ-18  The system shall support 50 concurrent interactive users.
  ```

Cite only keys that actually appear in the supplied set. If none are given, say so
and emit the deterministic checklist (below) with empty `requirement_ids`. The
machine-readable block may keep bare integer ids as a stable internal index; the
citation key a human reads is always `REQ-<n>`.

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
- `requirement_ids` — the list of **real integer indices** (each citing a `REQ-<n>` key)
  that cover this category; empty list `[]` when none do.
- `suggested_text` — when `addressed` is `false`, a **single concrete non-functional
  requirement** (classified non-functional, **with a number/target**) the team could add
  as a new `REQ-<n>` to close the gap; when `addressed` is `true` this **MUST be null**.
- `note` — the one-line definition of the category from Step 1, verbatim.

### Step 3 — Cite only what exists; persist nothing

- Only cite `REQ-<n>` keys (or their indices) that appear in the supplied requirements. Never invent one.
- Do not invent categories. Do not persist or "save" anything — this is a read.
- A category is only `addressed: true` if a real, cited requirement backs it. Don't mark
  it covered on the strength of your own suggested text.

### Step 4 — DETERMINISTIC STEP: render the six-category table

Always render the six categories as a fixed table, in order, even with zero requirements.
This is the deterministic base: reproducible and provider-agnostic. The fixed checklist
(one row per category, with its one-line definition) is the deterministic fallback — if
the set cannot be reasoned over, still return all six rows with `addressed: false`,
`requirement_ids: []`, and a stock `suggested_text` per category.

Deterministic matching cue (what counts as "addressed" at minimum — the model step may
judge more richly, but never *less* strictly than this):

| category        | a requirement plausibly covers it when its text mentions…                         |
| --------------- | ---------------------------------------------------------------------------------- |
| security        | tls, encrypt, auth, rbac, access control, secret(s), oauth                         |
| availability    | availability, uptime, an SLA `99.x`, sla, rpo, rto, failover                        |
| performance     | a latency unit (`ms`), latency, p95, throughput, response time, "within <n> …"     |
| data_residency  | residency, in-region, regional boundary, data placement, sovereign                 |
| maintainability | maintain, test coverage, observability, logging, documented                        |
| scalability     | scale, concurrent, load, horizontal, throughput, tenant/tenancy                     |

### Step 5 — MODEL STEP: the coverage prompt

Run this reasoning prompt over the set. The deterministic table is a floor; the model
step catches coverage the keywords miss (a requirement that *means* availability without
saying "uptime") and writes gap-fill text tuned to the project's context and region.

> Assess NFR coverage. This pass is ADVISORY and READ-ONLY: nothing returned is
> persisted, and accepting a gap is a separate human action.
>
> PROJECT TITLE: `<title>`
> PROJECT CONTEXT: `<context>`
> REQUIREMENTS (reference rows by their `REQ-<n>` key / integer index): `<requirements>`
>
> Assess coverage for EXACTLY these six categories, in this order, using no other names,
> adding none, dropping none: security, availability, performance, data_residency,
> maintainability, scalability (definitions as in Step 1).
>
> Return ONE item per category with: `category`, `addressed` (boolean — true when at least
> one requirement meaningfully addresses it), `requirement_ids` (the integer indices —
> each a `REQ-<n>` citation — that cover it, empty when none), `suggested_text` (when
> `addressed` is false, a single concrete non-functional requirement **with a
> number/target**, draftable as a new `REQ-<n>`; when true, **null**), and `note` (the
> one-line definition).
>
> Only cite keys that appear in the list. Do not invent categories or persist anything.
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

| # | Category        | Covered | By key          | Note                                                          |
|---|-----------------|---------|-----------------|--------------------------------------------------------------|
| 1 | security        | yes     | REQ-4, REQ-9    | Transport security, authentication, and secrets handling.    |
| 2 | availability    | NO      | —               | Uptime SLA plus recovery objectives (RPO/RTO).               |
| 3 | performance     | yes     | REQ-12          | Response-time / latency / throughput targets.                |
| 4 | data_residency  | NO      | —               | Where data lives and the regional boundary it stays within.  |
| 5 | maintainability | NO      | —               | Test coverage, observability, logging, documentation.        |
| 6 | scalability     | yes     | REQ-18          | Concurrency, load, horizontal scale, tenancy.                |

### Suggested gap-fill requirements (advisory — accept to create as a new non-functional `REQ-<n>`)

- **availability** — The system shall meet a Recovery Point Objective (RPO) of ≤ 15
  minutes and a Recovery Time Objective (RTO) of ≤ 1 hour for the primary data store.
- **data_residency** — All customer and project data shall remain within the designated
  regional boundary at all times, including backups and logs.
- **maintainability** — The system shall maintain ≥ 80% automated test coverage on
  backend route handlers and emit structured request/response logs for every mutating
  action.

_Read-only assessment. Nothing here is saved. Accepting a gap is a separate human action
that creates a new non-functional `REQ-<n>` from the suggested text._
```

Every suggested gap-fill MUST carry a concrete number or target (a percentage, a duration,
a count, an RPO/RTO). A gap-fill with no number is not done — it just relocates the gap.

## Notes / anti-patterns

- **Six, always, in order.** Never expand to seven, never reorder, never rename a category
  or its key. The closed list lives in `nfrs/nfr-categories.md`; keep it in sync with the
  `missing_nfr` kind in `challenge/red-team-requirements`, which draws the same list.
- **Read-only means read-only.** Do not mark a requirement accepted, do not edit text, do
  not create the requirement yourself. You hand the human draft text; they decide.
- **`suggested_text` is null iff `addressed` is true.** Never both populate
  `requirement_ids` *and* a suggestion for the same category, and never leave a gap with
  `null` text.
- **Don't credit your own suggestion as coverage.** `addressed` reflects the *supplied*
  set only.
- **No number, no NFR.** Reject vague gap-fill like "the system shall be highly available"
  — require a target ("RTO ≤ 1 hour").
- **Cite only real `REQ-<n>` keys.** No placeholder keys, no "(unsaved)" rows treated as coverage.
- **Advisory, not a gate.** Uncovered categories are prompts, not blockers. This skill
  never stops a project from proceeding.
