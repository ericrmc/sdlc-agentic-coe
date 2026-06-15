# RAID Register — Project: «PROJECT NAME»

> **Advisory: does not block.** This register grounds the plan; it never blocks a phase or
> demands a sign-off. The agent proposes every item as `open`; a **human disposes** using
> the kind-validated closeout vocabulary below. It **coexists with roadblocks** — a
> roadblock becomes a register risk only by a human's one-way promotion, never an
> automatic twin.

## Kinds and their legal closeouts

| kind | what it is | live state | legal closeouts |
|------|-----------|-----------|-----------------|
| **assumption** | something taken-true the plan depends on | `open` | `validated` · `invalidated` |
| **risk** | something that *might* happen (likelihood × impact + mitigation) | `open` | `mitigated` · `avoided` · `accepted` · `realised` |
| **tech_debt** | a durable carried-forward concern from design/review | `open` | `accepted` · `remediated` · `wont_fix` |

A closeout that is illegal for the item's kind is rejected (you cannot mark an assumption
`mitigated`). Closing out **never deletes the row** — the table is the history. A **fired**
closeout (`assumption → invalidated`, `risk → realised`) is a rework signal: re-check
everything that depended on the item.

## Revisit cadence (derived on read — no scheduler)

```
next_review_at = last_reviewed_at + review_cadence_days
due_for_review = (cadence set) AND (status == open) AND (now >= next_review_at)
```

- **Re-review** = "I looked, it still holds" → set `last reviewed` = today, **status unchanged**.
- **Closeout** = "this bet resolved" → change `status` + add the disposed note/date.
- A **new widening fact retires an assumption**: a human marks it `invalidated`, and the
  next derive run proposes the corrected one.

## Register

> Newest first. `id` prefixes (`A-` assumption, `R-` risk, `T-` tech_debt) are a reading
> aid, not a key. Risk fields (likelihood/impact/mitigation) live in the statement or
> category cell and stay blank for assumptions. An open item shows `—` under *disposed*.

| id | kind | title | statement | category | status | cadence (d) | last reviewed | source | disposed (note · date) |
|----|------|-------|-----------|----------|--------|-------------|---------------|--------|------------------------|
| A-1 | assumption | «short label» | «one or two sentences: what is assumed and what depends on it» | «e.g. market-scan / license-cost / resource-availability» | open | 90 | 2026-06-15 | agent | — |
| R-1 | risk | «short label» | «what might happen + impact» | likelihood: «low/med/high» / impact: «low/med/high» — mitigation: «…» | open | 30 | 2026-06-15 | human | — |
| T-1 | tech_debt | «short label» | «the carried-forward concern» | «e.g. design-debt» | open | — | — | human (promoted from reconcile) | — |

<!--
ADD A ROW per kept item from a derive run. The derive step proposes ASSUMPTIONS as
`status: open, source: agent`. Risks usually arrive by human promotion of a roadblock;
tech_debt by human promotion of a design/review finding.

DEDUPE before adding: pass every existing row (open AND closed) into the derive prompt
(semantic dedupe) and run the exact-match backstop (normalise title/statement: lowercase +
collapse whitespace; drop a verbatim repeat of any existing title or statement). Exact-match
only — do NOT add a fuzzy filter; the model owns semantic dedupe.

DISPOSE (human only): change `status` to a closeout legal for the kind, fill the disposed
cell with a one-line note + ISO date. Never delete the row.
-->
