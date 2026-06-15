# Maturity, sunset & supersede rules — the rules the Action computes by

> The curator (`pattern-library-curate`) **reads** these rules; it never applies them.
> Maturity is a `COUNT(*)` over the real adoption ledger, computed by the
> **pattern-lifecycle Action** and materialised in `generated/pattern-maturity.json`.
> Validity is a human ratification with evidence. Supersede is a chain edit, never a
> delete. This file documents the *same* rules the Action computes by, so the curator
> proposes **within** them rather than around them.
>
> Source of truth: `.github/workflows/pattern-lifecycle.yml`.

## 1. Maturity ladder — computed, never asserted

Maturity is derived from the **adoption count** in `adoptions/ledger.jsonl` (the
append-only record), tallied by the Action:

| `adopted_count` | computed `maturity` |
|---|---|
| 0 | `experimental` (adopted by zero — shown honestly) |
| 1–2 | `emerging` |
| 3+ | `battle-tested` |

The arithmetic, verbatim from the Action:

```python
def maturity_for(adopted_count: int) -> str:
    if adopted_count >= 3:
        return "battle-tested"
    if adopted_count >= 1:
        return "emerging"
    return "experimental"
```

What counts toward `adopted_count`: any ledger row whose `disposition` **starts with
`adopted`** (`adopted-clean`, `adopted-with-overrides`). What does **not** count:

- **`overridden-out`** rows — a team that evaluated and *declined* is real signal, but
  not an adoption. These are surfaced honestly **alongside** the tally, never folded into
  it and never suppressed.
- **`rejected`** rows — likewise signal, not adoption.

The curator **reads** `maturity` and `adopted_count` from `generated/pattern-maturity.json`
and quotes them. It **never** decides a maturity itself, and `maturity` is **forbidden as
a frontmatter input** (the lint rejects an author-set maturity).

## 2. Sunset & review-due — date arithmetic against today

The curator derives these flags deterministically (date math only, against today's
date), reading the human-owned frontmatter dates:

- **past-sunset** — `sunset_on` (schema name: `sunset_at`; the Action tolerates both) is
  in the past. The Action opens a sunset-flag issue; the curator proposes the human-facing
  curation (deprecate + `superseded_by`, or extend the window with fresh evidence).
- **review-due** — `review_by` is in the past, **or** `validated_on` +
  `validity_check_months` (default **12** when unset) is in the past — whichever the
  pattern declares. The Action opens a revalidation issue; the curator drafts the ask.
- **zero-adoption** — `adopted_count == 0` in the maturity file (adopted-by-0, shown
  honestly — absence is data).
- **declining / declined** — any `overridden-out` / `rejected` rows present, or
  `adopted-with-overrides` outweighing `adopted-clean`.

Revalidation is a **human ratification with evidence attached** — the curator drafts an
*issue* asking the owner to re-confirm validity (a recent engagement that used the pattern
as built) or to sunset it. The curator **never** writes `validated_by` / `validated_on` /
`review_by` itself (an agent-set `validated_*` fails the lint).

## 3. Supersede chains — deprecate, never delete

When a pattern is replaced:

- On the **predecessor**: set `status: deprecated` (or `superseded`) and
  `superseded_by: <successor-key>`.
- On the **successor**: set `supersedes: <predecessor-key>` (the back-reference).

**Never delete a pattern that has *any* adoption rows.** A pattern with rows in the ledger
is the historical record of real engagements — deleting it erases provenance the next
architect needs. The DELETE INVARIANT is enforced by the Action: a removed pattern file
with recorded adoptions is flagged ("must be deprecated, not deleted; restore it and set
`approval_status: deprecated` + `superseded_by`").

**Broken-chain flags** the curator detects in Step 1 (and proposes a minimal fix for):

- a `superseded_by` pointing at a `pattern_key` with no file;
- a `supersedes` with no matching predecessor;
- a pattern marked `status: superseded` / `deprecated` whose `superseded_by` is empty;
- a successor that does not back-reference via `supersedes`.

## 4. Non-adoption is surfaced, never hidden

`adopted-by-0` is shown as `adopted-by-0`. `overridden-out` / `rejected` reasons —
**why teams declined** — are quoted from `adoptions/ledger.jsonl` alongside the adoption
tally, never suppressed to make the shelf look busy. Absence and decline are both data.

## The posture

- **Read; never assert.** Maturity comes from the file. If you find yourself *deciding* a
  maturity, you have left the curator's role.
- **Propose; never dispose.** Every output is a PR draft (chain / status edit) or an issue
  draft (revalidation / zero-adoption review). A human reviews and merges. Nothing gates.
- **Cite the computed fact.** Each proposal points at the exact motivator — a
  maturity-file count, a frontmatter date, or a ledger reason — verifiable in one glance.
- **Prefer fewer proposals.** Surface what is genuinely stale, broken, or unadopted; leave
  the healthy shelf alone.
