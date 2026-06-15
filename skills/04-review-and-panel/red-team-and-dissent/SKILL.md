---
name: red-team-and-dissent
description: From one or N persona lenses raise the single strongest objection to each emerging proposal (never a verdict, never kills it); a declined objection becomes a durable dissent record feeding dismissal-memory.
when_to_use: adversarially stress-testing a proposal, or recording what was decided NOT to do and why
output_kinds: [question, proposal]
deterministic_fallback: the single-objection template + the dissent register template
suggested_tier: opus
compose_with:
  - 03-requirements/llm-fanout-orchestrator   # fan one lens out over N
references:
  - references/dissent-register.template.md
---

# Red-team and Preserve-Dissent

Adversarial pass + durable memory of what you decided **not** to do.

This skill does two jobs that belong together:

1. **Red-team** — from a named persona lens, raise the **one** thing most likely to
   make an emerging proposal the wrong call. Hard-hitting, specific, grounded — but
   it **never** delivers a verdict and **never** kills the proposal.
2. **Preserve-dissent** — when a human *declines* an objection (keeps the proposal),
   the objection doesn't evaporate. It becomes a durable **dissent record**: a titled
   "what we decided NOT to do, and why" with a human-owned reason and provenance back
   to the objection. The register is revisitable and feeds **dismissal-memory** so the
   same idea is not silently re-proposed later.

The call **always** stays with the human. The agent surfaces; the human disposes.

---

## Purpose

A panel or a fan-out generates *proposals* — a requirement, a decision, a roadblock, a
gap to close, a shape of the solution. Most of them are fine. A few are quietly wrong:
they over-reach, under-deliver, or carry a hidden risk that nobody named out loud.

The red-team's job is to name that risk **once, at full strength**, per proposal — and
then get out of the way. It is not a gate. It does not have a kill switch. It produces
exactly one artefact per proposal: the strongest single objection, framed so a human
can decide in seconds whether to **keep** the proposal or **record a dissent**.

When the human keeps the proposal *over* an objection, that objection is the most
valuable thing in the room — it's the "we considered this and chose the other way"
that future-you (and future contributors) will desperately want. So we capture it.

---

## When to use

- You have one or more **emerging proposals** (from a panel, a fan-out, a brainstorm,
  or your own design pass) and you want them stress-tested before they harden.
- You are about to record **what the project decided NOT to do** and the durable WHY,
  so it can be cited and is not re-litigated by accident.
- You want **dismissal-memory**: a future proposal that matches a recorded dissent
  should surface that prior decision instead of arriving fresh.

Do **not** use this skill to *approve* anything. It has no "pass". A clean red-team
pass means "no strong objection surfaced" — not "this is blessed".

---

## Inputs (what you supply)

| Input | Required | Shape |
|---|---|---|
| `proposal(s)` | yes | Free-text or markdown. One proposal, or a list. Each carries: a one-line statement + enough grounding (facts, source) to object against. |
| `proposal_kind` | per proposal | One of `requirement \| decision \| roadblock \| gap \| solution-shape \| feature`. Drives the objection framing. |
| `lens(es)` | optional | One persona kind, or N. Defaults to `skeptic` then `minimalist`, alternating (see below). |
| `grounding` | recommended | The facts the objection must keep — the proposal's source, prior context, any objection-so-far to *deepen*. |

You don't need a database, a panel, or any state machine. A proposal pasted into a
prompt is enough.

### The persona lenses

These are the same lenses the source platform seats, each a deliberate slant:

| Lens | Slant | Objects when… |
|---|---|---|
| `skeptic` | Red-teams the requirements | conflicting / unquantified / untestable / vague claims; unresolved tensions |
| `minimalist` | Argues for less | scope reaches beyond the captured outcome (gold-plating / over-reach) |
| `pragmatic_engineer` | Argues buildability | no acceptance criteria, missing NFR coverage, open roadblocks |
| `solution_designer` | Argues the shape | a pattern was overridden without a holding reason; a section is thin/stale |
| `explorer` | Argues for wider | orphaned value or an unexplored domain the proposal walks past |

The two **default adversarial voices** are `skeptic` and `minimalist` — alternate them
across a batch of proposals so you don't hear the same objection in the same voice
twice in a row. The others are available when the proposal is clearly in their domain.

---

## The method

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

If there are **zero** proposals, stop and say so. The honest empty case is a result,
not a gap — do **not** invent an objection to have something to say.

Assign each surviving proposal a stable `proposal_ref` (`gap-0`, `req-0`, `decision-0`,
`roadblock-0`, …) and alternate the lens across the batch (`skeptic`, `minimalist`,
`skeptic`, …). This is fully deterministic — no model needed to get this far.

### Step 2 — LLM: raise the single strongest objection per proposal

For each proposal, run the red-team prompt below from its assigned lens. This is the
**verbatim method** from the source platform's `red_team_challenge.md`:

> You are the RED TEAM on a design deliberation, speaking from the **{persona_kind}**
> lens. Raise the single STRONGEST objection to the EMERGING proposal below — the one
> thing most likely to make it the wrong call. Be specific and hard-hitting. But you
> NEVER deliver a verdict and you NEVER kill the proposal: you surface the objection so
> a human can decide whether to keep the proposal or record it as a dissent (what we
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
- **Keep the proposal's facts.** You are deepening an objection, not re-describing the
  proposal or arguing a different point.
- **End by leaving the call to the human.** The last sentence of `body_md` hands the
  decision back: keep it, or record a dissent. No "therefore we should not…".
- **No verdict, no score, no kill.** "Wrong call" is a hypothesis you're surfacing, not
  a ruling you're issuing.

### Step 3 — Composable: one lens, or fan out over N

- **One lens:** run Step 2 once, with the assigned persona. Done.
- **N lenses (no panel machinery):** to hear several voices on the *same* proposal, run
  Step 2 once per lens and collect the objections. Use the
  **`llm-fanout-orchestrator`** skill to issue the calls in parallel — one model call
  per (proposal × lens) — then gather. You do **not** need a convened panel, a roster,
  or any session state to do this; the fan-out is just N independent red-team prompts.

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
materialise a **dissent record** using `references/dissent-register.template.md`. The
shape (lifted from the source platform's dissent register) is:

```yaml
title:        # one line — what we decided NOT to do
kind:         # feature | requirement | solution | proposal | other
source:       # agent  -> recorded from a red-team objection (provenance below)
              # human  -> a standalone dissent a human added directly
reason:       # the durable WHY — HUMAN-OWNED, editable, the human owns every word
status:       # recorded  (default) | revisited  (re-opened for reconsideration)
provenance:   # only when source=agent
  objection_summary:  # the stance_summary that triggered this
  objection_lens:     # which persona raised it
  proposal_ref:       # the ref from Step 1 (decision-0, req-0, …)
recorded_on:  # ISO date
```

Then append the record to the project's **dissent register** (one markdown file or a
GitHub Issue using the dissent-record issue template — see Notes). Two properties make
the register trustworthy, both inherited from the source:

- **The human owns the WHY.** The `reason` (and `title`) are editable forever. The
  *provenance* — which objection, which lens, which proposal — is **immutable** once
  recorded. Snapshot semantics: editing the reason never reaches back and mutates the
  original objection.
- **Never write-only.** A record can be **revisited** — flip `status: recorded →
  revisited` to re-open a declined item for reconsideration. The record, its WHY, and
  its discussion thread are **preserved** across the flip. Decision history is kept,
  not erased.

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

You return two markdown artefacts.

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

When you fan out N lenses on one proposal, list the objections under the same proposal
header, sharpest first, with the agreeing lenses noted.

### B. A recorded dissent — from `references/dissent-register.template.md`

```markdown
## Dissent: Do not co-locate rule evaluation on the read path

- **kind:** solution
- **source:** agent
- **status:** recorded
- **recorded_on:** 2026-06-15

**Why (human-owned):**
We accept the read-path latency cost for v1 to ship the rules feature without standing
up a queue. We will revisit if p95 regresses past the NFR target in staging.

**Provenance (immutable):**
- objection_lens: solution_designer
- proposal_ref: decision-0
- objection_summary: "rule evaluation on the read path spends the read-latency headroom"
```

---

## Notes / anti-patterns

- **No verdict, ever.** If your output contains "we should not", "rejected",
  "blocked", a score, or a pass/fail — you've stopped red-teaming and started gating.
  The strongest objection is a *hypothesis about why this could be wrong*, handed to a
  human. That's the whole contract.
- **One objection, full strength.** A list of five mild concerns is weaker than one
  sharp one. If you genuinely have two strong, *distinct* objections, that's a signal
  the proposal is two proposals — say so rather than diluting.
- **Keep the proposal's facts.** Deepen the objection; don't re-litigate a different
  point or restate the proposal back. You're given "the objection so far" to *sharpen*,
  not replace.
- **The honest empty case is a result.** Zero proposals → zero objections. A lens with
  no real signal says "no strong objection from this lens" and proposes nothing. Never
  manufacture an objection to look diligent.
- **The human owns the WHY; the agent owns the provenance.** When recording a dissent,
  the reason/title are the human's words (editable forever); the link back to the
  objection, lens, and proposal_ref is immutable. Don't let an edit silently rewrite
  what was originally objected to.
- **The register is never write-only.** Always offer *revisit* — a recorded "no" must
  be re-openable. Preserving dissent is about keeping the decision *and the ability to
  change it*, not freezing it.
- **Check dismissal-memory before surfacing.** A new proposal that matches a recorded
  dissent should arrive *with* its prior dissent attached, not fresh. Silently
  re-proposing a settled "no" is the failure this skill exists to prevent.
- **Light and advisory.** This skill enforces nothing. It produces objections and
  records; disposition, ordering, and re-opening are all human moves. There is no state
  machine to satisfy and no approval to grant.

### GitHub-native mechanics (optional)

- **Dissent register as Issues:** use a **dissent-record issue template** so each
  recorded dissent is a GitHub Issue. `source`/`kind`/`status` become labels
  (`status:recorded`, `status:revisited`); the immutable provenance goes in a fenced
  block in the issue body; the human-owned WHY is the editable description; discussion
  threads naturally as issue comments. "Revisit" = re-open the issue (or flip the
  status label).
- **Dismissal-memory as a check:** a lightweight Action on PRs/issues can grep new
  proposal text against open `status:recorded` dissent issues and post an advisory
  comment ("this resembles dissent #123") — advisory only, never a required check.
