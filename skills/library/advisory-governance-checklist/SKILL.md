---
name: advisory-governance-checklist
description: Prefill cited evidence against four advisory review lenses (pattern_compliance / security / nfr / approval), surface only the delta since the last clean snapshot, default every untouched lens to defer, and never record a disposition, score, or reviewer metric. Use at a governance / technical-review checkpoint you want framed as advisory lenses rather than required dispositions.
one_liner: Cited evidence against four advisory review lenses, human reads only the delta.
aliases: [governance checklist, technical review checkpoint, design sign-off, advisory review, compliance lens, pre-handoff review, evidence checklist]
when_to_use: a governance/technical-review checkpoint, framed as advisory lenses not required dispositions
output_kinds: [proposal, question, halt]
deterministic_fallback: the four-lens evidence-prefill checklist
suggested_tier: mid
tier_reason: one structured evidence-prefill pass over given facts; no adversarial weighing
neighbours: |
  Comes after library/portfolio-phase-health (portfolio health facts can feed the approval lens).
  Terminal: produces a review record, hands off to a human reviewer; no skill follows.
---

# Advisory Governance Checklist

Run a governance / technical-review checkpoint as **four advisory lenses** plus a human
glance at **what changed** — never as a blocking approval workflow.

Each concern gets evidence prefilled and cited to its source. The checklist informs; it
does not block, enforce, or rubber-stamp. The output is a PR-checklist comment a human reads.

---

## Purpose

Replace a blocking approval workflow with advisory lenses that keep light governance honest.

The four lenses are the same four concern areas a heavier review would carry, but with the
disposition machinery removed:

- **No required disposition per check.** There is no `pass` / `pass-with-conditions` /
  `send-back` field, and nothing refuses to advance until checks are dispositioned.
- **What is kept:** the four concern areas, each with evidence prefilled by an agent and
  cited to its source, rendered as a checklist a reviewer skims. The reviewer's attention is
  the scarce resource — so they are shown only **what changed since the last clean snapshot**,
  and an untouched lens is recorded as `defer`, never `approve`.

The motivating question: someone who sees agents auto-applying technical work asks "how do I
know it's not making things up?" The honest answer is evidence-cited lenses plus a human who
actually looked at the delta — not a green checkmark a tired reviewer clicked at 11pm.
**A review optimised for throughput is worse than no review**, because it launders machine
output as human-validated provenance. This design makes that failure mode structurally
impossible: there is no disposition to rubber-stamp and no metric that rewards stamping.

---

## When to use

Use at any governance / technical-review checkpoint to be framed as **advisory lenses, not
required dispositions** — typically once a solution shape and its NFRs have settled and a
build handoff is near, or whenever a defensible "this was looked at" record is wanted without
a blocking approval workflow.

Do **not** use this to enforce. If something must actually block (a legal hold, a hard
residency boundary), that is a *constraint* on the work, not a governance lens — model it as
a roadblock and let the work fail validation against it. This skill only ever advises.

---

## Inputs

The user supplies whatever project context they have as markdown / notes. The richer the
context, the better the evidence prefill, but every lens degrades safely to "no evidence
found — defer". Each row is marked Required or Optional; the *if-absent* notes cite the
grounding contract (`skills/_contract/grounding-no-absent-input`, rule in
`skills/_shared/grounding.md`).

- **The project context to review** — *Required (at least one of the four lens feeds below).*
  The lenses cite real project facts; an empty context has nothing to ground a review record
  against, so a review with **no** input for **any** lens HALTs and asks for the context
  (per `_shared/grounding.md`) — it never invents a solution, decision, NFR, requirement, or
  completeness fact to populate a lens. The four lens feeds are:
  - **The settled solution shape / pattern** and its attached NFRs (drives `pattern_compliance`).
  - **Decisions** that are settled — data placement, auth method, encryption, integration
    (drives `security`).
  - **Non-functional requirements** and any design findings against them — response time,
    availability, residency, RPO/RTO (drives `nfr`).
  - **The completeness facts** — requirements accepted vs open, comparators confirmed, pattern
    adopted, decisions settled, estimate accepted (drives `approval`).
  A *partial* context is the normal case, not a halt: when **some** lens feeds are present and
  others are not, the present lenses are prefilled from real evidence and each absent lens is
  rendered honestly as "no evidence found — deferred" (never padded with an invented fact).
  Only a context with **zero** evidence for **every** lens halts.
- **The previous checklist** (the last clean snapshot) — *Optional.* If absent: proceed and
  treat the whole checklist as the delta (first review); never invent a prior snapshot.
- **A dismissal log** — *Optional.* If absent: proceed with nothing suppressed; never invent
  a dismissal the human did not make.

Readable forms for the project context: a markdown file, an xlsx/csv path, a GitHub Project
owner+number, a docs folder, or a block pasted into the chat.

---

## Grounding (quoted)

This skill reasons over project inputs (NFRs, decisions, the settled solution, requirement
status), so it obeys the no-fabrication keystone — `skills/_contract/grounding-no-absent-input`.
An absent *required* input HALTs and asks; an absent *optional* input proceeds honestly. The
quoted rule below travels in this skill's own bytes (drift-pinned by the `check-shared-stub-drift`
Action).

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

> **Read this skill's halt narrowly.** The lens-level "no evidence found — defer" default is the
> *optional*-input path: a context that is present but thin still produces an honest review record.
> The halt fires only on the *required* input — a context with **zero** evidence for **every**
> lens, where there is nothing to review and a record would be pure invention. Degrade per lens;
> halt only when there is no project context at all.

---

## The method — STEPS

The base is deterministic; exactly one step is LLM reasoning: a deterministic four-lens
prefill skeleton plus the agent's evidence-prefill.

### Step 0 — Verify there is something to review (deterministic, pre-model)

Before any prefill, check input presence as a file-level fact. If there is project context for
**at least one** lens feed (a settled solution / pattern + NFRs, settled decisions, NFRs +
design findings, or completeness facts), proceed to Step 1. If there is **no** readable evidence
for **any** lens — the context is absent, unreadable, or empty — emit the clean HALT below and
stop. Do **not** manufacture a lens feed to "have something to review"; a review record grounded
in nothing is exactly the laundering this skill exists to prevent.

```markdown
HALT — required input missing.

I can't run **advisory-governance-checklist** without the project context the lenses cite, and
I won't invent one. There is no solution shape, decision, NFR, or completeness fact for me to
ground a single lens against — so any record I produced would be fabricated.

Point me at the context and I'll prefill the lenses from real evidence. I can read any of these:
  • a markdown file or docs folder (the solution shape, decisions, NFRs, design findings)
  • an xlsx / csv file path
  • a GitHub Project (owner + project number)
  • the facts pasted directly into the chat

Which one, and where? (Nothing is assumed until you point me at it. A partial context is fine —
present lenses are prefilled, absent lenses are deferred honestly; only a wholly empty context
stops here.)
```

This is a `halt`, never a verdict — it names the missing input and asks where it is. It carries
no "this looks unready / out of scope" disposition; that is a JUDGMENT the human owns.

### Step 1 — Assemble the advisory inputs (deterministic)

Gather the facts the lenses read, **as advisory inputs only**. Collect, do not judge:

- settled pattern + its `attached_nfrs`; whether an override was recorded
- confirmed comparators and whether they share the chosen topology
- settled decisions (data placement, auth, encryption, integration)
- accepted NFRs and any open design findings against them
- requirement status counts (accepted vs still open), pattern adopted y/n, estimate accepted y/n

> There is **no** disposition machinery here. This step does not compute a blocking set of
> open checks. It only assembles what the lenses will cite.

### Step 2 — Compute the delta since last clean (deterministic, anti-fatigue)

If a previous clean checklist snapshot exists, diff the current inputs against it. The
review **opens on only what changed**: new evidence, changed evidence, evidence that
disappeared. Everything unchanged is folded away (shown as "unchanged since last clean —
deferred", not re-surfaced for re-judgement). If there is no prior snapshot, every lens is
in the delta (first pass). This is the single most important anti-fatigue move: a reviewer
who must re-read 40 unchanged rows every time will stop reading.

### Step 3 — Apply dismissal-memory (deterministic, anti-fatigue)

For each cue/lens, compute an evidence **fingerprint** (e.g. a hash of the cited values). If
the human previously dismissed this cue, suppress it **unless the fingerprint changed**. A
dismissed cue re-arms *only* when its underlying evidence changes — never on a timer, never
on re-run. Dismissal without memory trains the reviewer to ignore the channel, which
destroys it.

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

> These are advisory lenses. Nothing here blocks the merge. Untouched lenses are
> **deferred**, never approved. No disposition is binding. No reviewer metric is recorded.

**Delta since last clean:** 2 lenses changed · 2 unchanged (folded away, deferred)
_First review? Then every lens is in the delta below._

---

### Lens: `security` — CHANGED since last clean
Evidence prefilled by agent (cite-and-state only; no disposition):
- **Data placement** — In-region managed relational store; PII stays within the regional boundary.
  _ref: decision: data_placement (settled)_
- **Encryption at rest** — Provider-managed; **key-rotation policy not yet documented.**
  _ref: design finding (high)_  ← *open note for the human*
- **RBAC (API ↔ data store)** — not fully specified in the design draft.
  _ref: design finding (medium)_  ← *open note for the human*

Default: **DEFER.** [ ] I looked · note: _____________________ · [dismiss key-rotation cue]

---

### Lens: `nfr` — CHANGED since last clean
- **Availability** — 99.9% monthly; consistent with the pattern's attached NFR.
  _ref: requirement (accepted); pattern.attached_nfrs_
- **RPO** — **not yet stated.** _ref: design finding (high)_  ← *open note for the human*

Default: **DEFER.** [ ] I looked · note: _____________________

---

### Lens: `pattern_compliance` — unchanged since last clean → **deferred** (folded)
### Lens: `approval` — unchanged since last clean → **deferred** (folded)

_Expand the folded lenses only if you want to; their evidence has not changed._
```

The output is **proposal** (the prefilled evidence) and **question** (the open notes the
human may act on) — never a verdict. If you have no inputs at all for a lens, render it as
"no evidence found — deferred"; an honest empty lens is correct, padding it is not.

---

## Notes / anti-patterns

**The guardrails ARE the product, not the brakes.** The four mechanics below are what make a
governance-lite checklist trustworthy. Strip them and you have a rubber stamp.

- **Delta-since-last-clean is mandatory.** Re-surfacing unchanged rows for re-judgement every
  run is the fatigue that kills the channel. Open the review on what changed; fold the rest.
- **Untouched defaults to DEFER — never auto-approve.** Closing the checklist with a lens
  untouched records `deferred`. The "38 drafts at 11pm, approve-all" path must be impossible,
  because approve-all launders machine output as human-validated provenance.
- **No disposition is binding.** There is deliberately no `pass`/`send-back` field and no
  transition behind it. The checklist informs; it does not block. If something must truly
  block, model it as a constraint/roadblock the work fails against — not as a lens.
- **No 'probably-approve' lane, no recommended disposition.** The agent prefills evidence; it
  never nudges the human toward an outcome. Suggesting the disposition is the same failure as
  enforcing it — it just enforces socially instead of mechanically.
- **No acceptance-rate, throughput, or per-person metric is EVER recorded.** No reviewer
  velocity, no approval rate, no "lenses cleared per hour", nowhere. The absence of the metric
  is a feature; never add it "just for visibility".
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
- **Halt on a wholly empty context; defer on a thin one.** Per the grounding contract
  (`skills/_contract/grounding-no-absent-input`), the *required* input is "context for at
  least one lens"; absent that, Step 0 HALTs and asks rather than inventing a lens feed. The
  *optional* per-lens evidence degrades to "no evidence found — deferred". Never collapse the
  two: a present-but-thin context is a deferred lens, not a halt; a wholly absent context is a
  halt, not a checklist of invented facts.
