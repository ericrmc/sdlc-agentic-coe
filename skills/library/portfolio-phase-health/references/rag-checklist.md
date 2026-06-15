# RAG checklist — the deterministic base for `portfolio-phase-health`

This is the exact, named checklist. It is a **transparent boolean evaluation**, not a score.
The verdict is the **worst level** of any check that fires; `reasons[]` is every firing check, named.
Advisory facts are surfaced but do **not** drive the v1 verdict.

The verdict is derived-on-read (no persisted score). The phase axis is the delivery lifecycle; every
signal read degrades safely to a benign default.

---

## Phase axis (delivery lifecycle)

```
prototype (0)  <  mvp (1)  <  pilot (2)  <  production (3)
```

A check tagged with a **min-phase** only applies when the project's phase index is **at or beyond** it.
Below the min-phase the check is skipped (it cannot fire). Missing phase → default `prototype` (0).

---

## The named checks

### RED (bars the practice already treats as must-fix)

| Check name | Min-phase | Fires when | `reasons[]` string |
|---|---|---|---|
| `gate_sent_back` | prototype (always) | the advisory gate was sent back | `Advisory gate sent back` |
| `required_checks_open` | pilot | `open_required_checks > 0` | `{n} required advisory check(s) open` |

### AMBER (drift / incompleteness worth a glance)

| Check name | Min-phase | Fires when | `reasons[]` string |
|---|---|---|---|
| `record_incomplete` | production | `record_complete` is false | `Record incomplete at production` |
| `decisions_drafted` | mvp | `drafted_decisions > 0` | `{n} decision(s) still drafted` |
| `design_drift` | prototype (always) | `open_reconcile_proposals > 0` | `Design drift (reconcile proposals open)` |

### GREEN

No RED and no AMBER check fired. Means **"no failing check in the current set"** — not a quality
certificate. `reasons[]` is empty.

---

## Worst-of resolution

```
red[]   = [ every fired RED check's string ]
amber[] = [ every fired AMBER check's string ]

verdict =
    "red"    if len(red)   > 0
    "amber"  elif len(amber) > 0
    "green"  else

reasons = red + amber          # severity order: reds first, then ambers
```

| `red[]` | `amber[]` | verdict |
|:---:|:---:|:---:|
| non-empty | (any) | 🔴 red |
| empty | non-empty | 🟠 amber |
| empty | empty | 🟢 green |

No averaging. No weighting. No composite number. The verdict and its justification are the same object.

---

## Advisory facts (surfaced, NOT scored in v1)

Computed and attached to every row regardless of verdict. They do **not** change `verdict`.
Each degrades to its default on any read failure.

| Fact | Computed from | Default |
|---|---|---|
| `open_critical_risks` | count of open risks where likelihood = `high` **and** impact = `high` | `0` |
| `open_roadblocks` | count of open roadblocks | `0` |
| `has_pii` | any requirement/decision tagged `data_class ∈ {pii, special_category}` | `false` |
| `has_automated_decision` | any requirement/decision tagged `ai_use = automated_decision` | `false` |

Source enums, for label/field mapping:

- `data_class ∈ { public, internal, confidential, pii, special_category }`
- `ai_use ∈ { none, llm_generation, llm_assisted, automated_decision }`
- `likelihood, impact ∈ { low, medium, high }`

**Promotion rule:** moving any fact into a verdict-driving RED/AMBER check is an explicit org
ratification, never a code default. Until then: surfaced, never scored.

---

## Degrade-safely rule

Wrap **every** signal read so a missing label / empty project / flaky API yields the safe default
above — never an exception. The portfolio view must never fail because one project is malformed:
a project you cannot fully read is reported with whatever is readable, not crashed over.

---

## Consistency invariant

These checks read the **same signals** as `advisory-governance-checklist`. The portfolio RAG is a
roll-up *of* that per-project checklist, not a second opinion. Add a check here ⇒ add the matching
signal there (and vice versa), so the two can never disagree.

---

## Worked examples

**production project, one required check open, touches PII:**
- RED `required_checks_open` fires (phase ≥ pilot, `open_required_checks=1`) → `red[] = ["1 required advisory check(s) open"]`
- facts: `open_critical_risks` (e.g. 1), `has_pii=true`, `has_automated_decision=true`
- **verdict = red**, reasons = `["1 required advisory check(s) open"]`, facts attached (do not change verdict)

**mvp project, 2 drafted decisions, design drift, no required checks:**
- AMBER `decisions_drafted` fires (phase ≥ mvp) and AMBER `design_drift` fires
- **verdict = amber**, reasons = `["2 decision(s) still drafted", "Design drift (reconcile proposals open)"]`

**prototype project, 2 drafted decisions but no design drift:**
- `decisions_drafted` is min-phase `mvp` → **skipped** at prototype; nothing fires
- **verdict = green**, reasons = `[]` (early-lifecycle is not penalised for not-yet-due artefacts)

**production project, record marked incomplete, high-high risk open:**
- AMBER `record_incomplete` fires → **verdict = amber**
- fact `open_critical_risks=1` attached but does NOT escalate to red in v1 (surfaced, not scored)
