---
name: portfolio-phase-health
description: Compute a per-project advisory RAG health verdict at phase granularity, derived-on-read (no persisted score) — worst-of over a transparent named checklist with reasons naming every failing check; advisory facts ride alongside but don't drive v1; never a per-person/throughput metric; degrades safely. Use when producing the phase-level portfolio view for the org GitHub Project.
when_to_use: producing the phase-level portfolio view for the org GitHub Project
output_kinds: [proposal]
deterministic_fallback: the worst-of checklist computation with reasons[]
suggested_tier: sonnet
---

# portfolio-phase-health — derived-on-read advisory RAG per project phase

## Purpose

Compute and publish, for every downstream project in the portfolio, a single
**advisory RAG verdict** (`red` / `amber` / `green`) at **phase granularity**, and write it
onto the org-level GitHub Project board.

Three properties make this a *Centre-of-Excellence* signal rather than a management dashboard:

- **Derived-on-read, never persisted as a score.** The verdict is recomputed every time the
  portfolio-rollup runs from the project's *live* signals (its GitHub Project items, its phase
  label, its open advisory checks). There is no committed `health: amber` field anywhere to drift,
  go stale, or be gamed. If you delete the rollup output and re-run, you get the same answer because
  it is a pure projection of current state.
- **Transparent, never a black-box grade.** The verdict is the **worst-of** a small, fixed,
  *named* checklist. Every failing check is listed by name in `reasons[]`. A reader can always answer
  "why is this project amber?" by reading one line. There is no weighting, no composite number,
  no model judging the team.
- **Advisory only.** It gates nothing, blocks no merge, fails no Action. It is a lens for a
  practice lead skimming the portfolio, not an approval state-machine. (This is the deliberate
  drop from the legacy app: the bespoke tool had governance gates; the CoE keeps the *signal* and
  discards the *enforcement*.)

This skill is the portable version of the legacy `project_health()` derived-on-read RAG that ran in
the `/portfolio` endpoint (`backend/app/routers/_helpers.py:project_health`). The method is
preserved; the substrate moved from a Postgres read to GitHub Project items.

## When to use

- The **portfolio-rollup GitHub Action** invokes this to (re)stamp every project card's health field
  on the org board.
- A **practice lead** runs it ad hoc to get a "needs-attention-first" ordering of the portfolio.
- Any time you want a phase-aware, auditable health read **without** standing up a scoring service.

Do **not** use it to rank people, measure throughput, or compute acceptance rates — that is an
explicit anti-pattern (see Notes).

## Inputs

You (or the calling Action) supply, per project:

1. **Project handle** — the downstream project's own GitHub Project (each downstream delivery gets
   its OWN GitHub Project, guided by these skills; this portfolio view rolls them up at PHASE level,
   never down to individual requirements).
2. **Phase** — the project's current delivery-lifecycle phase, one of
   **`prototype` / `mvp` / `pilot` / `production`** (the axis below). Typically a single-select field
   or label on the project card.
3. **Advisory signals** — the same signals the `advisory-governance-checklist` skill reads, surfaced
   as machine-readable facts on the project (issue labels, a `health-inputs.json` checked into the
   project repo, or Action step outputs). Each is OPTIONAL; a missing signal degrades to its safe
   default and is never treated as a failure.

Concretely the v1 checklist consumes:

| Signal | Source on the project | Default if absent |
|---|---|---|
| `phase` | project field / label | `prototype` |
| `gate_sent_back` | label `gate:sent-back` present | `false` |
| `open_required_checks` | count of open issues labelled `advisory-check:required` | `0` |
| `record_complete` | label `record:complete` (or solution-design doc present) at `production` | treated complete unless explicitly `record:incomplete` |
| `drafted_decisions` | count of open issues labelled `decision:drafted` | `0` |
| `open_reconcile_proposals` | count of open issues labelled `design-drift` | `0` |

And these **advisory facts** (surfaced, never scored — see Step 4):

| Fact | Source | Default |
|---|---|---|
| `open_critical_risks` | open issues labelled `risk:high-high` | `0` |
| `open_roadblocks` | open issues labelled `roadblock` | `0` |
| `has_pii` | any item labelled `data:pii` or `data:special-category` | `false` |
| `has_automated_decision` | any item labelled `ai:automated-decision` | `false` |

## The method (numbered steps)

### Step 1 — Resolve the phase axis (delivery lifecycle)

Read the project's phase. The axis is the **delivery lifecycle**, ordered:

```
prototype  <  mvp  <  pilot  <  production
```

Hold the index. Several checks are **phase-gated**: a check that only matters once a project is
shipping (e.g. "record incomplete") must not fire on a `prototype`. Mirror the legacy state-index
guard (`_state_idx` / `si >= _state_idx("…")`): a check applies only at or beyond the phase where its
bar is meaningful. Map the phase to a numeric index `pi` for the comparisons below.

### Step 2 — Gather the signals, each degrading safely

Pull every signal in the Inputs tables. Wrap **each** read so a missing label, an empty project, or
a flaky API call yields the **safe default**, never an exception. The portfolio view must NEVER fail
because one project is malformed — a project you cannot read is reported, not crashed over. (Legacy
discipline: every fact fetch in `_health_facts` / `project_health` is in its own `try/except` that
falls back to a benign default.)

### Step 3 — DETERMINISTIC STEP: the worst-of checklist with `reasons[]`

This is the spine. It is a **transparent boolean evaluation**, identical in spirit to the legacy
`verdict = "red" if red else "amber" if amber else "green"`. No weighting, no score, no LLM.

Evaluate each named check. Append a human-readable string to `red[]` or `amber[]` when it fires.

**RED checks (bars the practice already treats as must-fix):**

- `gate_sent_back` is true → `"Advisory gate sent back"`
- `pi >= phase_index("pilot")` **and** `open_required_checks > 0`
  → `"{open_required_checks} required advisory check(s) open"`

**AMBER checks (drift / incompleteness worth a glance):**

- phase is `production` **and** `record_complete` is false
  → `"Record incomplete at production"`
- `pi >= phase_index("mvp")` **and** `drafted_decisions > 0`
  → `"{drafted_decisions} decision(s) still drafted"`
- `open_reconcile_proposals > 0`
  → `"Design drift (reconcile proposals open)"`

Then take the **worst level present**:

```
verdict = "red"   if red
          "amber" if amber
          "green" otherwise

reasons = red + amber          # EVERY failing check, named, in severity order
```

`green` is the *absence of evidence of a problem*, not a certificate of quality. State it that way.

> **Why worst-of and not an average?** Averaging hides the one red check behind four green ones.
> Worst-of with an itemised `reasons[]` is auditable: the verdict and its justification are the same
> object. A reader never has to trust a number — they read the list.

### Step 4 — Advisory facts ride ALONGSIDE (they do NOT drive the v1 verdict)

Compute `open_critical_risks`, `open_roadblocks`, `has_pii`, `has_automated_decision` and attach them
to the row. **They do not change `verdict` in v1.** They are surfaced so a lead can scan exposure
(e.g. "which production projects touch PII?") and so the org can later, deliberately, ratify one of
them into a verdict-driving bar. Until that ratification, a project with PII and an automated decision
can still be `green` — and the facts make the exposure visible regardless.

This is the deliberate v1 conservatism: **the verdict uses only bars the practice already agrees on.**
Promoting a fact to a driver is an org decision, not a default.

### Step 5 — Derived-on-read publication (nothing persisted as a committed score)

Write `verdict` + `reasons` + facts onto the org GitHub Project card for the project (a single-select
RAG field + a short body/comment listing reasons). This write is **output, not state**: it is fully
recomputed on the next rollup. Do not commit the verdict into any project repo, do not store it as a
field the project itself edits, and do not let a stale value survive a re-run. If the inputs change,
the next rollup changes the card; nothing reconciles because nothing was the source of truth except
the live signals.

**Consistency invariant:** this skill reads the **same signals** as `advisory-governance-checklist`.
By construction the two can never disagree — the portfolio RAG is a roll-up *of* the per-project
advisory checklist, not a parallel opinion. If you add a check here, add the matching signal there
(and vice versa) so they stay one source.

### Step 6 — LLM STEP (optional, narrative only)

**None is required — this skill is deterministic.** Steps 1–5 fully determine the verdict and reasons.

Optionally, you may add **one narrative line** per amber/red project to make the board skimmable —
a plain-language paraphrase of `reasons[]`, e.g.:

> _"Amber: pilot has 2 decisions still drafted and design drift to reconcile — no required checks open."_

Constraints on the optional narrative:
- It **paraphrases** `reasons[]`; it never introduces a judgement not in the deterministic list.
- It **cannot change** `verdict` or add/remove a reason.
- If the LLM is unavailable, omit it — the deterministic verdict + `reasons[]` stand alone (this is the
  `deterministic_fallback`).

## Output format

Return one proposal block: a per-project row plus a rollup table for the board. Concrete template:

```markdown
## Portfolio phase health — derived-on-read (rollup @ 2026-06-15)

Advisory only. Verdict = worst-of a named checklist; reasons list every failing check.
Facts ride alongside and do NOT drive the v1 verdict. No persisted score.

| Project | Phase | Verdict | Reasons (every failing check) | Facts (advisory) |
|---|---|:---:|---|---|
| billing-ledger | production | 🔴 red | 1 required advisory check(s) open | risks:1 · roadblocks:0 · PII · auto-decision |
| onboarding-flow | mvp | 🟠 amber | 2 decision(s) still drafted; Design drift (reconcile proposals open) | risks:0 · roadblocks:1 |
| pattern-catalog | pilot | 🟢 green | — | risks:0 · roadblocks:0 |

### billing-ledger — 🔴 red
- **Phase:** production
- **Reasons:**
  - 1 required advisory check(s) open
- **Advisory facts (not scored):** open critical risks: 1 · open roadblocks: 0 · has PII: yes · automated decision: yes
- _Narrative (optional):_ Red at production — one required advisory check still open; touches PII with an automated decision, worth a privacy glance.
```

Per-project JSON the rollup Action writes to the card (machine-readable, regenerated each run):

```json
{
  "project": "billing-ledger",
  "phase": "production",
  "verdict": "red",
  "reasons": ["1 required advisory check(s) open"],
  "facts": {
    "open_critical_risks": 1,
    "open_roadblocks": 0,
    "has_pii": true,
    "has_automated_decision": true
  },
  "derived_on_read": true,
  "computed_at": "2026-06-15T00:00:00Z"
}
```

Default ordering for a practice lead: **red, then amber, then green** (needs-attention first) —
mirroring the legacy practice-lead default sort.

## Notes / anti-patterns

- **Never a per-person, throughput, velocity, or acceptance-rate metric.** This is a hard scope guard
  carried over verbatim from the legacy `/portfolio` ("NO per-person metrics"). The verdict describes
  a *project's conformance to the method*, never a team's or person's output. If a proposed check needs
  who-did-what, it is out of scope.
- **No persisted score.** If you ever find yourself storing the verdict as the source of truth, you've
  reintroduced drift. The only durable artefacts are the *signals*; the verdict is always recomputed.
- **`green` ≠ "good".** It means "no failing check in the current set". Say so on the board so nobody
  reads it as a quality stamp.
- **Worst-of, not weighted.** Resist requests for a 0–100 health score. The whole value here is that
  the verdict and its justification are the same auditable list.
- **Facts don't silently become drivers.** Promoting `has_pii` (etc.) into a red/amber bar is an
  explicit org ratification, not a code default. Until then it is surfaced, never scored.
- **Degrade, never crash.** A malformed or unreadable project is reported with whatever signals are
  readable and safe defaults for the rest — the portfolio view stays up.
- **Phase-gate the checks.** Don't fire "record incomplete" on a prototype or "required checks open"
  before pilot. The phase index exists precisely so early-lifecycle projects aren't penalised for
  not yet having shipping-stage artefacts.
- **Stay advisory.** No Action should `exit 1` on a red verdict. This skill informs; it does not gate.

See `references/rag-checklist.md` for the exact named checklist, the phase-gate rules, and the
worst-of resolution table.
