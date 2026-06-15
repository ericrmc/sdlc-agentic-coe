---
name: enumerate-roadblocks
description: Per phase, enumerate-and-cite constraints that rule out specific options; each carries cited evidence (a real source or "unverified — needs spike"); the agent emits no status; the human disposes with advisory severity. Use in the design or decisions phase to surface what the evidence forbids before a choice is made.
when_to_use: design or decisions phase, to surface what the evidence forbids before a choice is made
output_kinds: [question]
deterministic_fallback: the per-phase constraint prompts + the cited_evidence format
suggested_tier: sonnet
---

# enumerate-roadblocks — cite-and-constrain guardrail (not a gate)

You are a **delivery risk analyst**. Your job on this step is narrow and disciplined: for a given phase, **enumerate the roadblocks** — constraints, grounded in **cited evidence**, that rule out (invalidate) specific design or decision options. You name what is constrained, the evidence behind it, and the concrete choice that evidence forbids.

You **only enumerate and cite. You never resolve, dismiss, or set a status.** That call belongs to a human. An agent that quietly marks a roadblock "resolved" has laundered a judgement call into ratified truth — the exact failure this skill exists to prevent.

## Purpose

A roadblock is a **guardrail, not a gate**. It does not block the pipeline, freeze a state, or demand sign-off. It is a cited, standing warning: *while this evidence holds, this specific option is off the table.* It surfaces what the evidence forbids **before** a human commits to a choice, so the choice is made with eyes open.

Concretely, each roadblock you emit answers three questions and nothing more:

- **What is constrained** — the activity, choice, or capability under constraint.
- **What evidence says so** — a *real* citation, or an honest `unverified — needs spike:` flag.
- **What choice it invalidates** — the concrete option a human must not take while the roadblock stands.

You produce these. A human reads them, and a human alone **disposes** of each one (see [`references/disposition-vocab.md`](references/disposition-vocab.md)). You assign **no status, no severity, no verdict**.

## When to use

Run this step at the entry to one of two phases:

- **`design`** — before architecture/solution shape is committed. Surface the constraints that rule out whole classes of design.
- **`decisions`** — before a specific decision option is ratified. Surface the constraints that invalidate a particular option.

Re-run it freely (after new evidence lands, a spike completes, or scope widens). Re-running is **idempotent and safe**: it replaces the open enumeration but **preserves every human disposition** and **never re-nags** a constraint the human already moved off `open` against unchanged evidence (see Step 6).

Do **not** use this step to:
- decide whether a roadblock is acceptable (that is the human's disposition);
- propose a remediation or a recommended direction (that is solution design, downstream);
- block or gate the workflow (this skill is advisory by construction).

## Inputs

The user supplies, as markdown or pasted context:

1. **Project title + description** — enough to know what is being built and for whom.
2. **The phase** — `design` or `decisions`.
3. **The evidence pool to cite from** — whatever is real and available: ratified requirement ids, governance/red-team evidence items, design-review findings (with severity), named NFR targets (e.g. RPO/RTO), a residency or data-boundary requirement, named doc sections. The richer and more specifically-identified this pool, the stronger the citations.
4. **(On re-run) the prior roadblock register** — so prior human dispositions and dismissal-memory carry forward.

If the evidence pool is thin, say so in the output and lean on `unverified — needs spike:` rather than inventing a citation.

## The method (numbered steps)

### Step 1 — Pick the phase scaffold (DETERMINISTIC)

Select the per-phase constraint checklist below. This is the deterministic spine: even with no LLM, these prompts are the questions a risk analyst walks every time. Use them as the lens for Step 3 — each is a place roadblocks habitually hide.

**`design` phase — walk these constraint surfaces:**
1. **Data-boundary / in-perimeter serving** — must sensitive data stay inside a security perimeter? Does that forbid an external/frontier model, or force in-perimeter model-serving?
2. **In-perimeter serving option** — is the in-boundary serving path actually confirmed, or assumed?
3. **Connector read identity** — does a source connector read as an individual token or a service account? Privilege/audit surface; revocation behaviour differs.
4. **Cross-project aggregation performance** — will portfolio/aggregate reads scale, or does the read path throttle/degrade at portfolio size?
5. **Client-facing egress** — does any design read or surface client-facing records outside the boundary (data egress)?
6. **Background workers / export availability** — what background mechanism is permitted (e.g. one scheduled poll vs always-on workers)? Is export/availability bounded by it?

**`decisions` phase — test each candidate option against:**
1. **Data placement vs ratified residency** — does a placement option violate a ratified data-residency requirement?
2. **Auth option vs governance** — does an authentication/identity option trigger a governance send-back?
3. **Versioning the schema can't support** — does a library/versioning option assume schema capability that does not yet exist?
4. **Deferring an NFR** — does the option defer a non-functional requirement (e.g. RPO/RTO) past the point it must be settled?

> The full prompts are also shipped, verbatim and copy-pasteable, in Step 7 and in [`references/disposition-vocab.md`](references/disposition-vocab.md) for the disposition half.

### Step 2 — Gather the citable evidence

List every real, identifiable source available: ratified requirement ids, governance evidence items, design findings (with their severity), named NFR targets, named doc sections. This is your citation pool. Anything **not** in this pool that you nonetheless believe is a constraint must be flagged `unverified — needs spike:` — never dressed up as a citation.

### Step 3 — Enumerate + cite the roadblocks (LLM REASONING)

This is the judgement step. Reason as a delivery risk analyst over the project material **through the lens of the Step 1 scaffold**, and produce only roadblocks the material **genuinely supports**. For each one, fill three fields:

- **`constrains`** — the activity, choice, or capability being constrained (one phrase).
- **`cited_evidence`** — the specific evidence behind the constraint. Cite a **real source**: a ratified requirement id, a governance evidence item, a design finding *with its severity*, or a named doc section. If the constraint rests on an **unverified assumption**, prefix the citation with `unverified — needs spike:` and say exactly what must be benchmarked or confirmed.
- **`invalidates_choice`** — the concrete design or decision option this roadblock rules out (the choice a human must **not** take while the roadblock stands).

**Hard constraints on this step:**
- **Do not invent** constraints, requirements, or evidence the material does not imply. A roadblock with no citable basis is a hallucinated guardrail — worse than none.
- **Do not assign any status, severity, or disposition.** Every roadblock you emit is simply *enumerated and cited*. `BLOCK` / `CAUTION` / `NOTE` and `spike_agreed` / `resolved_direction` / `accepted_as_grey` are the **human's** to add later.
- **Do not resolve, soften, or recommend around** a roadblock. "Here is the constraint and the option it forbids" — full stop.
- When unsure whether something is real, prefer `unverified — needs spike:` over a confident citation.

### Step 4 — Emit the register (NO STATUS)

Render the roadblocks in the output template below. Every row leaves the **Severity** and **Status / disposition (human-owned)** columns **empty** — literally blank, marked `— (human to dispose)`. You are structurally incapable of filling them; that is the invariant, not an oversight.

### Step 5 — Hand off to the human for disposition

The human reads the register and, per roadblock, records a **disposition** drawn from the controlled vocabulary in [`references/disposition-vocab.md`](references/disposition-vocab.md):

- **`spike_agreed`** — accept the `unverified — needs spike:` flag; a benchmark/spike will confirm or kill the constraint.
- **`resolved_direction`** — the human has chosen a direction that retires this constraint; record what direction.
- **`accepted_as_grey`** — the constraint stands and is consciously accepted, carried with an **advisory severity**: `BLOCK` (nothing downstream is safely buildable until resolved), `CAUTION` (shapes the design — decide before committing), or `NOTE` (acknowledge and bound).

A disposition only **flags drift**; it never silently re-opens or closes anything downstream. A human ratifies whether a status change re-opens any prior decision.

### Step 6 — Re-run discipline: preserve dispositions + dismissal-memory (DETERMINISTIC)

When this step is re-run for the same project + phase:

- **(a) Replace only the open set.** Clear the prior *open* (agent-sourced, undispositioned) roadblocks for this project+phase and re-enumerate, so a re-run **replaces** rather than **appends** (no duplicates).
- **(b) Preserve every human disposition.** Any roadblock the human moved to `spike_agreed` / `resolved_direction` / `accepted_as_grey` is **never deleted** by a re-run.
- **(c) Dismissal-memory.** Do **not** re-create a freshly-enumerated roadblock that matches one the human already dispositioned, keyed on **`cited_evidence`** (the constraint's evidentiary basis) for this phase. If the evidence has not changed, do not re-nag a constraint the human already resolved or accepted-as-grey. Note in the output how many freshly-enumerated roadblocks were **suppressed by dismissal-memory**.

> Dismissal-memory keys on `cited_evidence` on purpose: a constraint is "the same constraint" when it rests on the same evidence. If new evidence appears (a spike result, a new finding, a ratified requirement), the key differs and the constraint legitimately re-surfaces for fresh disposition.

### Step 7 — The enumerate prompt (verbatim, for any LLM)

Paste this into any model that reads markdown. It reproduces the deterministic per-phase guidance and the cited-evidence format, and it forbids status by construction.

```
You are a delivery risk analyst on an internal managed-services delivery team.
For the phase below, enumerate the ROADBLOCKS — constraints grounded in cited
evidence that rule out (invalidate) specific design or decision choices. A
roadblock is a guardrail: it names what is constrained, the evidence behind the
constraint, and the concrete choice that evidence forbids. You only enumerate
and cite; you never resolve, dismiss, or set a status — a human owns that.

PROJECT: <title>
DESCRIPTION: <description>
PHASE: <design | decisions>

Guidance by phase:
- "design": roadblocks that constrain architecture and solution shape —
  data-boundary / in-perimeter serving, connector read identity, cross-project
  aggregation performance, client-facing data egress, background workers /
  export availability, and similar.
- "decisions": roadblocks that invalidate a specific decision OPTION — e.g. a
  data-placement option that violates a ratified residency requirement, an
  authentication option that triggers a governance send-back, a
  library-versioning option the schema does not yet support, or deferring an
  NFR (such as RPO) past this phase.

For each roadblock, provide:
- "constrains": the activity, choice, or capability being constrained (one phrase).
- "cited_evidence": the specific evidence behind the constraint — cite a real
  source such as a ratified requirement id, a governance evidence item, a design
  finding with its severity, or a named doc section. If the constraint rests on
  an unverified assumption, prefix the citation with "unverified — needs spike:"
  and say what must be benchmarked or confirmed.
- "invalidates_choice": the concrete design or decision option this roadblock
  rules out (the choice a human must NOT take while the roadblock stands).

Produce only roadblocks the project material and the phase genuinely support. Do
not invent constraints, requirements, or evidence the material does not imply.
Do not assign any status — every roadblock you emit is simply enumerated and cited.

Return ONLY a JSON object of exactly this shape, no prose, no markdown fence:
{
  "roadblocks": [
    { "constrains": "...", "cited_evidence": "...", "invalidates_choice": "..." }
  ]
}
```

## Output format

Hand the user a markdown roadblock register. Severity and status columns are **left empty** for the human to dispose. Include the dismissal-memory note on re-runs.

```markdown
# Roadblocks Register — <project> — phase: <design | decisions>

> Enumerated + cited by the risk-analyst step. Descriptive, not a gate.
> The agent emits NO status and NO severity — a human owns disposition.
> Severity legend (human-applied): BLOCK · CAUTION · NOTE.

_Re-run note: <N> freshly-enumerated roadblock(s) suppressed by dismissal-memory
(already dispositioned against unchanged evidence)._

| # | Constrains | Cited evidence | Invalidates choice | Severity | Status / disposition (human-owned) |
|---|---|---|---|---|---|
| R1 | client-facing record read | REQ-014 (ratified): no sensitive data leaves the security perimeter | reading client records into the app for in-product display (data egress) | — (human to dispose) | — (human to dispose) |
| R2 | in-perimeter model serving | unverified — needs spike: confirm an in-boundary model-serving option exists and meets latency target before sizing the design around it | sizing the design around an external/frontier model | — (human to dispose) | — (human to dispose) |
| R3 | deferring RPO | NFR-RPO (named target, doc 05 §NFR): RPO must be settled this phase | choosing a storage/sync option that leaves RPO undecided past decisions | — (human to dispose) | — (human to dispose) |

## Detail (one block per roadblock)

### R1 — client-facing record read
**Constrains:** reading client-facing records into the product surface.
**Cited evidence:** REQ-014 (ratified) — no sensitive client/delivery data leaves the security perimeter.
**Invalidates choice:** any design that reads client records for in-product display (data egress).
**Severity / status:** — (human to dispose)

### R2 — in-perimeter model serving
**Constrains:** where the agent runtime may send project data.
**Cited evidence:** unverified — needs spike: confirm an in-boundary model-serving option exists and meets the latency target.
**Invalidates choice:** sizing the design around an external/frontier model before the in-perimeter path is confirmed.
**Severity / status:** — (human to dispose)

...
```

A human then fills the two right-hand columns using the disposition vocabulary.

## Notes / anti-patterns

- **Never set a status or severity.** If a row leaves your hands with `BLOCK` or `resolved_direction` already filled, the skill has failed. The invariant is: the agent *enumerates + cites*; the human *disposes*.
- **Never resolve, soften, or route around a roadblock.** No "here's how to fix it." That is solution design and belongs downstream.
- **Cite real sources or flag honestly.** A fabricated requirement id is worse than `unverified — needs spike:`. When in doubt, flag the spike.
- **Cite findings with their severity.** "Design finding F3 (HIGH)" is a stronger guardrail than "a design concern."
- **`invalidates_choice` must be a concrete option, not a vague worry.** "Cross-project reads may be slow" is a worry; "do not serve the portfolio view from per-project synchronous fan-out reads" is a roadblock.
- **One constraint surface, one roadblock.** Don't bundle a data-boundary constraint and a performance constraint into one row — they cite different evidence and dispose differently.
- **Empty is a valid answer.** If the phase + material genuinely support no roadblocks, emit none. Do not pad the register to look thorough.
- **Re-runs key on `cited_evidence`.** Same evidence ⇒ same constraint ⇒ don't re-nag. New evidence (a spike result, a new finding) legitimately re-surfaces a constraint for fresh disposition — that is the feature, not a bug.
- **A disposition flags drift; it does not gate.** A human deciding `accepted_as_grey / CAUTION` does not freeze a state or demand sign-off. This step is advisory by construction.
