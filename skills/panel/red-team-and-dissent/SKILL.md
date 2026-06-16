---
name: red-team-and-dissent
description: From one or N persona lenses raise the single strongest objection to each emerging proposal (never a verdict, never kills it); a declined objection becomes a durable dissent record feeding dismissal-memory.
one_liner: Raise the strongest objection per proposal; record declined ones as durable dissent.
aliases:
  - devils advocate
  - play devil's advocate
  - poke holes
  - challenge a proposal
  - decision log of what was rejected
  - record why a proposal was declined
  - dissent register
  - objection log
when_to_use: adversarially stress-testing a proposal, or recording what was decided NOT to do and why
output_kinds: [question, proposal, halt]
deterministic_fallback: the single-objection template + the dissent register template
suggested_tier: frontier
tier_reason: adversarial judgement plus a durable human-facing dissent record is high-stakes.
neighbours:
  before: panel/synthesise-panel — supplies the proposals a synthesised review surfaces
  after: panel/design-review-findings — turns surviving proposals into concrete findings
compose_with:
  - skills/_contract/parallel-agents   # fan one lens out over N
references:
  - references/dissent-register.template.md
---

# Red-team and Preserve-Dissent

Two jobs that belong together: from a persona lens raise the **one** strongest objection
to each emerging proposal (never a verdict, never a kill); when a human *declines* an
objection, capture it as a durable **dissent record** that feeds dismissal-memory. The
call always stays with the human — the agent surfaces, the human disposes.

> Fan one lens out over N independent agents per `skills/_contract/parallel-agents`
> (advisory; the deterministic base stands if a sub-agent fails). See Step 3.

---

## When to use

- There are one or more **emerging proposals** (from a panel, a fan-out, a brainstorm,
  or a design pass) and they need stress-testing before they harden.
- The project is about to record **what was decided NOT to do** and the durable WHY,
  so it can be cited and is not re-litigated by accident.
- **Dismissal-memory** is wanted: a future proposal that matches a recorded dissent
  should surface that prior decision instead of arriving fresh.

Do **not** use this skill to *approve* anything. It has no "pass". A clean red-team
pass means "no strong objection surfaced" — not "this is blessed".

---

## Inputs (what you supply)

| Input | Required | Shape |
|---|---|---|
| `proposal(s)` | **yes** | Free-text or markdown. One proposal, or a list. Each carries: a one-line statement + enough grounding (facts, source) to object against. *If absent/unreadable/empty:* HALT and ask for the proposal(s) (per `skills/_shared/grounding.md` / `skills/_contract/grounding-no-absent-input`); never invent a proposal to red-team. See Step 0. |
| `proposal_kind` | per proposal | One of `requirement \| decision \| roadblock \| gap \| solution-shape \| feature`. Drives the objection framing. *If absent on a proposal:* infer it from the proposal's shape (Step 1), never default silently to a kind that changes the framing. |
| `lens(es)` | optional | One persona kind, or N. Defaults to `skeptic` then `minimalist`, alternating (see below). *If absent:* use the default adversarial voices; never invent a domain expert the proposal doesn't call for. |
| `grounding` | recommended (optional) | The facts the objection must keep — the proposal's source, prior context, any objection-so-far to *deepen*. *If absent:* object only from the proposal's own stated facts; never back-fill grounding the human did not supply. |

No database, panel, or session state is needed. A proposal pasted into a prompt is
enough. (Two empty cases — no proposals at all vs. proposals that hold no genuine
proposal — are handled at the Step 0 / Step 1 boundary.)

## Grounding (quoted)

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

Per `skills/_contract/grounding-no-absent-input`, the missing-proposal halt (Step 0) asks
where the proposals are — never a disposition dressed as a stop.

### The persona lenses

Each lens is a deliberate slant. Pick the one whose domain the proposal sits in, or
alternate the two default adversarial voices across a batch.

| Lens | Slant | Objects when… |
|---|---|---|
| `skeptic` | Red-teams the requirements | conflicting / unquantified / untestable / vague claims; unresolved tensions |
| `minimalist` | Argues for less | scope reaches beyond the captured outcome (gold-plating / over-reach) |
| `pragmatic_engineer` | Argues buildability | no acceptance criteria, missing NFR coverage, open roadblocks |
| `solution_designer` | Argues the shape | a pattern was overridden without a holding reason; a section is thin/stale |
| `explorer` | Argues for wider | orphaned value or an unexplored domain the proposal walks past |

The two **default adversarial voices** are `skeptic` and `minimalist` — alternate them
across a batch of proposals so the same objection is not heard in the same voice twice
in a row. The others are available when the proposal is clearly in their domain.

---

## The method

### Step 0 — DETERMINISTIC: verify proposals were supplied (the grounding halt)

Before identifying emerging proposals, confirm the `proposal(s)` input was actually
supplied — a file-level fact (absent / unreadable / empty), computed **before** any model
reasoning. If **nothing** was supplied to red-team, emit the clean HALT below and **stop** —
do not invent a proposal to object to.

```markdown
HALT — required input missing.

I can't red-team without a proposal to object to, and I won't invent one. Tell me what to
stress-test and I'll raise the single strongest objection per proposal.

I can read any of these:
  • one or more proposals pasted directly (a requirement, decision, roadblock, gap, solution-shape, feature)
  • the synthesis output of panel/synthesise-panel (its four proposal categories)
  • a markdown brief or design pass to pull the emerging proposals from

What should I red-team? (No objection is raised until you give me a real proposal.)
```

This is distinct from Step 1's empty case: a HALT means *no input arrived*; the Step 1
empty case means *input arrived but held no genuine proposal*. If proposals were supplied,
proceed to Step 1.

### Step 1 — DETERMINISTIC: identify the emerging proposals (no model)

Walk the input and pick out only the things that are genuinely **proposals**. A
statement that merely *concurs* or *objects-to-something-else* is not an emerging
proposal — skip it. The four signal shapes that ARE proposals (and the kind each maps
to) are:

| The proposal is a… | …if it | objection kind |
|---|---|---|
| `gap` | flags a missing thing to close | `gap` |
| `requirement` | proposes adding a requirement / carrying value | `requirement` |
| `decision` | proposes an alternative to weigh | `decision` |
| `roadblock` | raises a risk that constrains the build | `roadblock` |

If the supplied input held genuine content but **zero** of it is an emerging proposal,
stop and say so — *the honest empty case* (the Step 0 boundary above). It is a result,
not a gap — do **not** invent an objection to have something to say.

Assign each surviving proposal a stable `proposal_ref` (`gap-0`, `req-0`, `decision-0`,
`roadblock-0`, …) and alternate the lens across the batch (`skeptic`, `minimalist`,
`skeptic`, …). This is fully deterministic — no model needed to get this far.

### Step 2 — LLM: raise the single strongest objection per proposal

For each proposal, run the red-team prompt below from its assigned lens:

> You are the RED TEAM on a design deliberation, speaking from the **{persona_kind}**
> lens. Raise the single STRONGEST objection to the EMERGING proposal below — the one
> thing most likely to make it the wrong call. Be specific and hard-hitting. But you
> NEVER deliver a verdict and you NEVER kill the proposal: you surface the objection so
> a human can decide whether to keep the proposal or record it as a dissent (what was
> decided NOT to do, and why).
>
> **PROPOSAL KIND:** {proposal_kind}
>
> **THE EMERGING PROPOSAL + the objection so far** (deepen this — keep its facts):
> {grounding}
>
> Return ONLY a JSON object of exactly this shape, no prose, no fence:
> ```json
> {
>   "stance_summary": "one sharp sentence — your strongest single objection",
>   "body_md": "2-4 sentences making the objection concrete and grounded, ending by leaving the call to the human"
> }
> ```

Rules that make this a red-team and not a reviewer:

- **One** objection per proposal. Not three. The strongest single one.
- **Keep the proposal's facts.** This is deepening an objection, not re-describing the
  proposal or arguing a different point.
- **End by leaving the call to the human.** The last sentence of `body_md` hands the
  decision back: keep it, or record a dissent. No "therefore we should not…".
- **No verdict, no score, no kill.** "Wrong call" is a hypothesis being surfaced, not a
  ruling being issued.

### Step 3 — Composable: one lens, or fan out over N

- **One lens:** run Step 2 once, with the assigned persona. Done.
- **N lenses (no panel machinery):** to hear several voices on the *same* proposal, run
  Step 2 once per lens and collect the objections. Issue the calls in parallel — one
  model call per (proposal × lens) — then gather, following the convention in
  `skills/_contract/parallel-agents`. No convened panel, roster, or session state is
  needed; the fan-out is just N independent red-team prompts.

Deduplicate honestly: if two lenses raise effectively the same objection, keep the
sharper wording and note both lenses agreed — don't pad the list to look thorough.

### Step 4 — Human disposes: keep, or record a dissent (DETERMINISTIC)

Present each objection to the human with exactly two dispositions:

- **Keep the proposal** (objection acknowledged, proposal stands) → if the human keeps
  it *over* a real objection, offer to **record a dissent** capturing the objection so
  the decision is durable.
- **Record a dissent** (the project will NOT do this) → write a dissent record (Step 5).

Either way the human owns the outcome. The agent never auto-disposes.

### Step 5 — DETERMINISTIC: a declined objection becomes a durable dissent record

When the human declines a proposal (or keeps one but wants the objection on record),
materialise a **dissent record** per `references/dissent-register.template.md` — that
file owns the full record shape, the two trustworthiness properties (human owns the WHY /
never write-only), the append-to-register and GitHub-Issue mechanics, and a rendered
example. The fields the red-team supplies into it are `reason` (human-owned WHY),
`proposal_kind` → `kind`, and the immutable provenance triple
`objection_summary` / `objection_lens` / `proposal_ref` (from Step 1).

### Step 6 — dismissal-memory: don't silently re-propose a dissent

Before a *new* proposal is surfaced, check it against the dissent register. If it
matches a `recorded` dissent (same idea, same kind), do **not** present it fresh —
surface the prior dissent instead:

> ⤺ This looks like **{dissent.title}**, which was recorded as a dissent on
> {recorded_on} because: *{reason}*. Re-open it (set status → revisited) to
> reconsider, or leave it.

This is the whole point of preserving dissent: the project stops re-litigating settled
"no"s by accident, while keeping the door open to deliberately re-open any of them.

---

## Output format

Two markdown artefacts are returned.

### A. The objection(s) — one block per proposal

```markdown
### Red-team objection — `decision-0` (solution-shape)
**Lens:** solution_designer · **Disposition:** ⬚ keep proposal ⬚ record dissent

**Strongest objection:** Putting the rules engine behind the same sync HTTP path as
reads makes a 200ms rule evaluation a tail-latency tax on every page load.

The proposal reuses the existing request handler for rule evaluation, but rules fan
out to 3–5 downstream lookups; under the captured p95 target that path is already at
budget, so co-locating evaluation there spends the headroom the NFR set reserves for
reads. An async/queued evaluation keeps the read path clean at real cost to rule
freshness. Whether that trade is acceptable is the call to make here, not mine.
```

> Note: `body_md` is 2–4 sentences and its **last sentence hands the call back to the
> human**. There is no recommendation line, no score, no "verdict".

When N lenses are fanned out on one proposal, list the objections under the same
proposal header, sharpest first, with the agreeing lenses noted.

### B. A recorded dissent

Rendered per `references/dissent-register.template.md` (see its "Rendered example") when
the human disposes via Step 5.

---

## Notes / anti-patterns

- **Output a literal verdict-string and you've stopped red-teaming.** "we should not",
  "rejected", "blocked", a score, a pass/fail — the strongest objection is a *hypothesis*
  handed to a human (the no-verdict rule is enforced in Step 2).
- **One objection, full strength.** A list of five mild concerns is weaker than one
  sharp one. If there genuinely are two strong, *distinct* objections, that's a signal
  the proposal is two proposals — say so rather than diluting.
- **Light and advisory.** This skill enforces nothing; disposition, ordering, and
  re-opening are all human moves. There is no approval to grant.

(The dissent-record / dismissal-memory mechanics, including the GitHub-Issue rendering,
live in `references/dissent-register.template.md`.)
