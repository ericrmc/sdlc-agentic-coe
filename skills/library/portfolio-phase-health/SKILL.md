---
name: portfolio-phase-health
description: Compute a per-project advisory RAG health verdict at phase granularity, derived-on-read (no persisted score) — worst-of over a transparent named checklist with reasons naming every failing check; advisory facts ride alongside but don't drive v1; never a per-person/throughput metric; degrades safely. Use when producing the phase-level portfolio view for the org GitHub Project.
when_to_use: producing the phase-level portfolio view for the org GitHub Project
output_kinds: [proposal, halt]
deterministic_fallback: the worst-of checklist computation with reasons[]
one_liner: Derived-on-read advisory RAG health per project phase.
aliases: [project health, portfolio dashboard, RAG status, red amber green, project rollup, delivery health, portfolio view, traffic-light status]
suggested_tier: mid
neighbours: |
  Before: library/pattern-library-curate (curates the reusable assets this view sits beside).
  After: library/advisory-governance-checklist (the per-project checklist this rolls up; both read the same signals).
---

# portfolio-phase-health — derived-on-read advisory RAG per project phase

## Purpose

Compute and publish, for every downstream project in the portfolio, a single
**advisory RAG verdict** (`red` / `amber` / `green`) at **phase granularity**, and write it
onto the org-level GitHub Project board.

Three properties make this a portfolio signal rather than a management dashboard:

- **Derived-on-read, never persisted as a score.** The verdict is recomputed every time the
  portfolio-rollup runs from the project's *live* signals (its GitHub Project items, its phase
  label, its open advisory checks). There is no committed `health: amber` field anywhere to drift,
  go stale, or be gamed. If you delete the rollup output and re-run, you get the same answer because
  it is a pure projection of current state.
- **Transparent, never a black-box grade.** The verdict is the **worst-of** a small, fixed,
  *named* checklist. Every failing check is listed by name in `reasons[]`. A reader can always answer
  "why is this project amber?" by reading one line. There is no weighting, no composite number,
  no model judging the team.
- **Advisory only.** The verdict blocks no merge and fails no Action. It is a lens for a
  practice lead skimming the portfolio, not an approval mechanism.

## When to use

- The **portfolio-rollup GitHub Action** invokes this to (re)stamp every project card's health field
  on the org board.
- A **practice lead** runs it ad hoc to get a "needs-attention-first" ordering of the portfolio.
- Any time you want a phase-aware, auditable health read **without** standing up a scoring service.

Do **not** use it to rank people, measure throughput, or compute acceptance rates — that is an
explicit anti-pattern (see Notes).

## Inputs

You (or the calling Action) supply, per project. Each row is marked Required or Optional; the
*if-absent* notes cite the grounding contract (`skills/_contract/grounding-no-absent-input`,
rule in `skills/_shared/grounding.md`).

1. **Project handle** — *Required.* The downstream project's own GitHub Project (each downstream
   delivery gets its OWN GitHub Project; this portfolio view rolls them up at PHASE level, never
   down to individual requirements). If **no project is named at all** — the handle is absent,
   unreadable, or empty — HALT and ask which project(s) to roll up (per `_shared/grounding.md`);
   never invent a project name or fabricate a verdict for a project that was not supplied.
   Readable forms: a GitHub Project owner+number, an org/project list, or the handle pasted in.
   (Note the asymmetry below: a project you *were* pointed at but **cannot read** is reported with
   safe defaults, not halted — "degrade, never crash". The halt is only for "you named no project
   at all", where there is nothing to roll up and a verdict would be invented.)
2. **Phase** — *Optional (defaults to `prototype`).* The project's current delivery-lifecycle
   phase, one of **`prototype` / `mvp` / `pilot` / `production`** (the axis below); typically a
   single-select field or label on the project card. If absent: default to `prototype` (the most
   conservative phase — it gates off the shipping-stage checks); never invent a later phase.
3. **Advisory signals** — *Optional.* The same signals the `advisory-governance-checklist` skill
   reads, surfaced as machine-readable facts on the project (issue labels, a `health-inputs.json`
   checked into the project repo, or Action step outputs). Each is OPTIONAL; a missing signal
   degrades to its safe default (per the table below) and is never treated as a failure, and a
   default is never padded with an invented count.

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

## Grounding (quoted)

This skill reasons over a project's live inputs (its GitHub Project items, phase, and advisory
signals), so it obeys the no-fabrication keystone — `skills/_contract/grounding-no-absent-input`.
The **project handle is the one required input**: name no project and there is nothing to roll up,
so the skill HALTs and asks rather than inventing a verdict. Every *other* input is optional and
degrades to a documented safe default — that degrade is **not** a halt (see the asymmetry note in
Inputs). The quoted rule below travels in this skill's own bytes (drift-pinned by the
`check-shared-stub-drift` Action).

<!-- BEGIN grounding (byte-stable; do not edit a quoted copy — edit _shared/grounding.md) -->

**GROUNDING RULE — name the required inputs; an absent required input HALTs and asks, never assumes.**

A skill **names its required inputs** up front (its Inputs section marks each row Required or
Optional). Then:

- **A required input that is absent, unreadable, or empty becomes a `halt`.** The halt asks
  the user *where the input is*, offering the formats ingestion can read (an xlsx/csv path, a
  GitHub Project owner+number, a docs folder, or a pasted block). It then **stops and waits.**
  It never assumes, invents, or reasons over a hypothetical — no invented id, key, number, NFR,
  requirement, acceptance criterion, file path, or source row.
- **Partial input is named, not patched.** When some required inputs are present and others are
  not, the skill **names exactly what is missing and asks for it** — it never silently proceeds
  on the part it has, and it never back-fills the gap with a plausible-looking guess.
- **An absent *optional* input proceeds honestly.** It is surfaced as a `question` or recorded
  as an explicit null — never padded with invented content to look complete.

**"I read nothing" and "I cannot read this" are different outputs.** An unreadable or
unsupported source HALTs (it asks for a readable form); it never returns an empty result, because
a silent-empty reads downstream as "the source had nothing in it" — a silent-proceed failure.

**A halt is a question, never a verdict.** A halt names the missing input and asks where it is.
It never smuggles a finding, an assumption, or a disposition for a human to rubber-stamp — no
"I halt because this is infeasible / too risky / out of scope." Those are JUDGMENTs the human
owns. The halt carries only: *what is required, what is missing, and the formats it can be read
from.*

<!-- END grounding -->

> **The grounding asymmetry that makes this skill's halt narrow.** "Name no project" (the required
> input is absent) HALTs — there is nothing to compute and a verdict would be invented. "A named
> project I cannot read cleanly" does **not** halt — it is reported with safe defaults per Step 2's
> degrade-never-crash guard, because the project *was* supplied. The portfolio view never crashes
> over one malformed project; it crashes over being told to roll up *nothing at all*.

---

## The method (numbered steps)

### Step 0 — Verify a project was named (deterministic, pre-model)

Before resolving any phase or signal, check the **project handle** as a file-level fact. If at
least one project handle was supplied, proceed to Step 1 (and let Step 2 degrade-not-crash on any
project you cannot read cleanly). If **no** project was named at all — the handle is absent,
unreadable, or empty — emit the clean HALT below and stop. Do **not** invent a project name, and
never compute a RAG colour for a project that was never supplied — there is nothing to roll up.

```markdown
HALT — required input missing.

I can't run **portfolio-phase-health** without a project to roll up, and I won't invent one.
No project handle was supplied, so there is nothing to compute a verdict against.

Tell me which project(s) to include and I'll roll up each one's live signals. I can read:
  • a GitHub Project (owner + project number)
  • an org / project list to enumerate
  • the project handle(s) pasted directly into the chat

Which project(s)? (Nothing is assumed until you name one. Once a project is named, I report it
even if some of its signals are unreadable — those degrade to safe defaults, they don't stop me.)
```

This is a `halt`, never a verdict — it names the missing input (the project handle) and asks for
it. It carries no health colour, no "this looks red", no disposition; those are computed only once
a real project is supplied.

### Step 1 — Resolve the phase axis (delivery lifecycle)

Read the project's phase. The axis is the **delivery lifecycle**, ordered:

```
prototype  <  mvp  <  pilot  <  production
```

Hold the index. Several checks are **phase-gated**: a check that only matters once a project is
shipping (e.g. "record incomplete") must not fire on a `prototype`. A check applies only at or
beyond the phase where its bar is meaningful. Map the phase to a numeric index `pi` for the
comparisons below.

### Step 2 — Gather the signals, each degrading safely

Pull every signal in the Inputs tables. Wrap **each** read so a missing label, an empty project, or
a flaky API call yields the **safe default**, never an exception. The portfolio view must NEVER fail
because one project is malformed — a project you cannot read is reported, not crashed over. Each
fact fetch sits in its own guard that falls back to a benign default.

### Step 3 — DETERMINISTIC STEP: the worst-of checklist with `reasons[]`

This is the deterministic base. It is a **transparent boolean evaluation** —
`verdict = "red" if red else "amber" if amber else "green"`. No weighting, no score, no model.

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

Then take the **worst level present:**

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

### Step 6 — MODEL STEP (optional, narrative only)

**None is required — this skill is deterministic.** Steps 1–5 fully determine the verdict and reasons.

Optionally, you may add **one narrative line** per amber/red project to make the board skimmable —
a plain-language paraphrase of `reasons[]`, e.g.:

> _"Amber: pilot has 2 decisions still drafted and design drift to reconcile — no required checks open."_

Constraints on the optional narrative:
- It **paraphrases** `reasons[]`; it never introduces a judgement not in the deterministic list.
- It **cannot change** `verdict` or add/remove a reason.
- If the model is unavailable, omit it — the deterministic verdict + `reasons[]` stand alone (this is the
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

Default ordering for a practice lead: **red, then amber, then green** (needs-attention first).

## Notes / anti-patterns

- **Never a per-person, throughput, velocity, or acceptance-rate metric.** This is a hard scope guard.
  The verdict describes a *project's conformance to the method*, never a team's or person's output. If
  a proposed check needs who-did-what, it is out of scope.
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
- **Stay advisory.** No Action should `exit 1` on a red verdict. This skill informs; it does not block.
- **Halt on "no project named"; degrade on "project unreadable".** Per the grounding contract
  (`skills/_contract/grounding-no-absent-input`), the *required* input is the project handle —
  absent it, Step 0 HALTs and asks rather than inventing a verdict. Every other input is optional
  and degrades to a safe default (Step 2). Keep the two distinct: never crash over one malformed
  project (degrade it), and never invent a verdict when **no** project was supplied (halt).

See `references/rag-checklist.md` for the exact named checklist, the phase-gate rules, and the
worst-of resolution table.
