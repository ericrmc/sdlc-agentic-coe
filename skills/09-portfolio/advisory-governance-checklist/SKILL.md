---
name: advisory-governance-checklist
description: The governance-lite replacement for hard gates — prefill evidence against advisory lenses (pattern_compliance / security / nfr / approval), the human reviews only the delta-since-last-green, untouched defaults to defer, no disposition is binding, and no acceptance-rate metric is ever recorded. Use it at a governance / technical-review checkpoint that you want reframed as advisory lenses rather than required dispositions.
when_to_use: a governance/technical-review checkpoint, reframed as advisory lenses not required dispositions
output_kinds: [proposal, question]
deterministic_fallback: the four-lens evidence-prefill checklist
suggested_tier: sonnet
---

# Advisory Governance Checklist

The governance-LITE replacement for hard gates. Where a heavyweight process puts a
state-machine gate, a disposition machine, and a version-bound approval in the way of
shipping, this skill puts **four advisory lenses** and a human glance at **what changed**.
It keeps light governance *honest* — every concern still gets evidence prefilled against it
— without ever enforcing, blocking, or rubber-stamping.

It is the de-enforced descendant of a real governance gate. In the original app the gate
gathered facts (`build_gate_ctx`), an agent prefilled evidence against a fixed check set
(`pattern_compliance`, `security`, `nfr`, `approval`), and then a human had to dispose each
check `pass` / `pass-with-conditions` / `send-back` before a version-bound state-machine
gate would let the project advance. **This skill keeps the evidence prefill and the four
lenses. It strips the disposition machine, the state transition, and the version binding
entirely.** Nothing here gates anything. The output is a PR-checklist comment a human reads.

---

## Purpose

Replace hard gates with advisory lenses that keep light governance honest.

- **Hard gate (dropped):** a required disposition per check, a state-machine transition that
  refuses to advance until every required check is `pass`/`pass-with-conditions`, a
  `reopened_reason = 'governance_send_back'` that demotes the project, and a per-version
  binding so a re-prefill is forced after any change.
- **Advisory lens (kept):** the same four concern areas, each with evidence prefilled by an
  agent and cited to its source, rendered as a checklist a reviewer skims. The reviewer's
  attention is the scarce resource — so they are shown only **what changed since the last
  time this looked clean**, and an untouched lens is recorded as `defer`, never `approve`.

The whole point: an executive who sees agents auto-applying technical work asks "how do I
know it's not making things up?" The honest answer is evidence-cited lenses plus a human who
actually looked at the delta — not a green checkmark a tired reviewer clicked at 11pm. **A
gate optimised for throughput is worse than no gate**, because it launders machine output as
human-validated provenance. This skill is engineered so that failure mode is structurally
impossible: there is no disposition to rubber-stamp and no metric that rewards stamping.

---

## When to use

Use at any governance / technical-review checkpoint that you want reframed as **advisory
lenses, not required dispositions** — typically once a solution shape and its NFRs have
settled and you are about to hand off to build, or whenever you want a defensible
"we looked at this" record without a blocking approval workflow.

Do **not** use this to enforce. If you need something to actually block (a legal hold, a
hard residency boundary), that is a *constraint* on the work, not a governance lens — model
it as a roadblock and let the work fail validation against it. This skill only ever advises.

---

## Inputs

The user supplies whatever project context they have as markdown / notes. The richer the
context, the better the evidence prefill, but every lens degrades safely to "no evidence
found — defer". Useful inputs:

- **The settled solution shape / pattern** and its attached NFRs (drives `pattern_compliance`).
- **Decisions** that are settled — data placement, auth method, encryption, integration
  (drives `security`).
- **Non-functional requirements** and any design findings against them — response time,
  availability, residency, RPO/RTO (drives `nfr`).
- **The completeness facts** — requirements accepted vs open, comparators confirmed, pattern
  adopted, decisions settled, estimate accepted (drives `approval`).
- **The previous checklist** (the last "green" snapshot), if one exists — so this run can
  compute the **delta since last green**. If there is no prior snapshot, the whole checklist
  is the delta (first review).
- **A dismissal log** (optional) — lenses/cues the human already dismissed, and the evidence
  fingerprint they dismissed against, so a dismissed cue does not re-nag until its evidence
  changes.

---

## The method — STEPS

The spine is deterministic; exactly one step is LLM reasoning. Both are preserved from the
source: the deterministic four-lens prefill skeleton, and the agent's evidence-prefill.

### Step 1 — Assemble the advisory inputs (deterministic)

Gather the facts the lenses read, the way `build_gate_ctx` did — but **as advisory inputs
only**. Collect, do not judge:

- settled pattern + its `attached_nfrs`; whether an override was recorded
- confirmed comparators and whether they share the chosen topology
- settled decisions (data placement, auth, encryption, integration)
- accepted NFRs and any open design findings against them
- requirement status counts (accepted vs still open), pattern adopted y/n, estimate accepted y/n

> There is **no** disposition machinery here. We are not computing `open_required_checks` to
> block a transition. We are only assembling what the lenses will cite.

### Step 2 — Compute the delta since last green (deterministic, anti-fatigue)

If a previous "green" checklist snapshot exists, diff the current inputs against it. The
review **opens on only what changed**: new evidence, changed evidence, evidence that
disappeared. Everything unchanged is folded away (shown as "unchanged since last green —
deferred", not re-surfaced for re-judgement). If there is no prior snapshot, every lens is
in the delta (first pass). This is the single most important anti-fatigue move: a reviewer
who must re-read 40 unchanged rows every time will stop reading.

### Step 3 — Apply dismissal-memory (deterministic, anti-fatigue)

For each cue/lens, compute an evidence **fingerprint** (e.g. a hash of the cited values). If
the human previously dismissed this cue, suppress it **unless the fingerprint changed**. A
dismissed cue re-arms *only* when its underlying evidence changes — never on a timer, never
on re-run. This is the fix for the unconditional-re-nag bug: dismissal without memory trains
the reviewer to ignore the channel, which destroys it.

### Step 4 — Prefill evidence per lens (LLM reasoning step)

This is the one model step. For **each** of the four fixed lenses, prefill the **evidence**
— a short list of `{ label, value, ref }` rows that cite the inputs. The lenses are:

| Lens | The concern it carries |
|---|---|
| `pattern_compliance` | Does the chosen shape match an approved pattern? Override recorded? Attached NFRs reviewed? Design review status? |
| `security` | Data placement / residency, auth method, encryption in transit & at rest, RBAC, secret rotation — with findings flagged at their real severity. |
| `nfr` | Response time, availability, residency, RPO/RTO, topology availability model — each tied to an accepted requirement or named as an open finding. |
| `approval` | The completeness picture: requirements accepted, comparators confirmed, pattern settled, decisions settled, estimate accepted, prior lenses' notes. |

**The hard rule of this step:** prefill **evidence only — never a disposition.** Do not write
`pass`, `pass-with-conditions`, `send-back`, `approve`, `reject`, a RAG colour, a score, a
recommendation, or a "probably-approve" hint. State the facts and cite them. Where a fact is
missing or weak, say so plainly and name it as an open note for the human — that is evidence,
not a verdict. The disposition belongs to the human and to no one else; here, there isn't even
a disposition field to fill.

### Step 5 — Render as an advisory PR-checklist comment (deterministic)

Emit the checklist as a markdown PR comment (template below). Each lens is a section with its
prefilled evidence and an explicit **DEFER** default. There is no "approve all" affordance, no
recommended disposition, no required tick. The human reads the delta, optionally jots a note
or dismisses a cue, and moves on. Untouched stays `defer`.

---

## Output format

A markdown PR-checklist comment. Concrete template:

```markdown
## Advisory governance lenses — review the delta only

> These are advisory lenses, not gates. Nothing here blocks the merge. Untouched lenses are
> **deferred**, never approved. No disposition is binding. No reviewer metric is recorded.

**Delta since last green:** 2 lenses changed · 2 unchanged (folded away, deferred)
_First review? Then every lens is in the delta below._

---

### Lens: `security` — CHANGED since last green
Evidence prefilled by agent (cite-and-state only; no disposition):
- **Data placement** — In-region managed Postgres; PII stays within the regional boundary.
  _ref: decision: data_placement (settled)_
- **Encryption at rest** — Provider-managed; **key-rotation policy not yet documented.**
  _ref: design finding (high)_  ← *open note for the human*
- **RBAC (API ↔ data store)** — not fully specified in the design draft.
  _ref: design finding (medium)_  ← *open note for the human*

Default: **DEFER.** [ ] I looked · note: _____________________ · [dismiss key-rotation cue]

---

### Lens: `nfr` — CHANGED since last green
- **Availability** — 99.9% monthly; consistent with the pattern's attached NFR.
  _ref: requirement (accepted); pattern.attached_nfrs_
- **RPO** — **not yet stated.** _ref: design finding (high)_  ← *open note for the human*

Default: **DEFER.** [ ] I looked · note: _____________________

---

### Lens: `pattern_compliance` — unchanged since last green → **deferred** (folded)
### Lens: `approval` — unchanged since last green → **deferred** (folded)

_Expand the folded lenses only if you want to; their evidence has not changed._
```

The output is **proposal** (the prefilled evidence) and **question** (the open notes the
human may act on) — never a verdict. If you have no inputs at all for a lens, render it as
"no evidence found — deferred"; an honest empty lens is correct, padding it is not.

---

## Notes / anti-patterns

**The guardrails ARE the product, not the brakes.** The four mechanics below are what make a
governance-lite checklist trustworthy enough to replace a hard gate. Strip them and you have
a rubber stamp.

- **Delta-since-last-green is mandatory.** Re-surfacing unchanged rows for re-judgement every
  run is the fatigue that kills the channel. Open the review on what changed; fold the rest.
- **Untouched defaults to DEFER — never auto-approve.** Closing the checklist with a lens
  untouched records `deferred`. The "38 drafts at 11pm, approve-all" path must be impossible,
  because approve-all launders machine output as human-validated provenance — *worse than no
  gate at all.*
- **No disposition is binding.** There is deliberately no `pass`/`send-back` field and no
  state transition behind it. The checklist informs; it does not gate. If something must
  truly block, model it as a constraint/roadblock the work fails against — not as a lens.
- **No 'probably-approve' lane, no recommended disposition.** The agent prefills evidence; it
  never nudges the human toward an outcome. Suggesting the disposition is the same failure as
  enforcing it — it just enforces socially instead of mechanically.
- **No acceptance-rate, throughput, or per-person metric is EVER recorded.** No reviewer
  velocity, no approval rate, no "lenses cleared per hour", nowhere. A gate optimised for
  throughput is worse than no gate. The absence of the metric is a feature; never add it
  "just for visibility".
- **Dismissible cues carry dismissal-memory.** A dismissed cue re-arms only when its evidence
  fingerprint changes — never on a timer, never on re-run. An un-dismissible cue trains the
  reviewer to ignore the whole channel.
- **Evidence only at the LLM step.** The model states and cites facts. The moment it writes a
  disposition, a colour, a score, or a recommendation, it has stopped advising and started
  pretending to be the human reviewer. Keep it to `{ label, value, ref }`.
- **Lens, not person.** A lens flags a missing *concern* (no documented key-rotation), never a
  missing or under-performing *person*. Never assess a reviewer.
- **Light by default.** If in doubt, advise and defer. This skill's job is to make sure
  nothing important went unlooked-at — not to stop the work.
