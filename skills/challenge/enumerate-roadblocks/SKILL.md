---
name: enumerate-roadblocks
description: Per phase, enumerate-and-cite constraints that rule out specific options; each carries cited evidence (a real source or "unverified — needs spike"); the agent emits no status; the human disposes with advisory severity. Use in the design or decisions phase to surface what the evidence forbids before a choice is made.
one_liner: Cite the constraints that rule out specific design or decision options.
aliases: [blockers, constraints, showstoppers, dealbreakers, what rules this out, hard limits, deal breakers, off the table]
when_to_use: design or decisions phase, to surface what the evidence forbids before a choice is made
output_kinds: [question, halt]
deterministic_fallback: the per-phase constraint prompts + the cited_evidence format
suggested_tier: mid
neighbours: |
  Before: challenge/surface-risks-and-assumptions (open-ended risk/assumption pass).
  After: challenge/necessity-check (is a proposed component actually needed?).
---

# enumerate-roadblocks

Enumerate the roadblocks for a given phase: constraints, grounded in **cited evidence**, that rule out specific design or decision options. Name what is constrained, the evidence behind it, and the concrete choice that evidence forbids.

This step **only enumerates and cites. It never resolves, dismisses, or sets a status.** That call belongs to a human. An agent that quietly marks a roadblock "resolved" launders a judgement call into ratified truth — the exact failure this skill exists to prevent.

## What a roadblock is

A roadblock is advisory. It does not block the pipeline or demand sign-off. It is a cited, standing warning: *while this evidence holds, this specific option is off the table.* It surfaces what the evidence forbids **before** a human commits to a choice, so the choice is made with eyes open.

Each roadblock answers three questions and nothing more — `constrains` / `cited_evidence` / `invalidates_choice`, specified in Step 3. This step produces these; a human alone **disposes** of each one (see [`references/disposition-vocab.md`](references/disposition-vocab.md)). The agent assigns **no status, no severity, no verdict**.

## When to use

Run this step at the entry to one of two phases:

- **`design`** — before architecture/solution shape is committed. Surface the constraints that rule out whole classes of design.
- **`decisions`** — before a specific decision option is ratified. Surface the constraints that invalidate a particular option.

Re-run it freely (after new evidence lands, a spike completes, or scope widens). Re-running is **idempotent and safe**: it replaces the open enumeration but **preserves every human disposition** and **never re-nags** a constraint the human already moved off `open` against unchanged evidence (see Step 6).

Do **not** use this step to:
- decide whether a roadblock is acceptable (that is the human's disposition);
- propose a remediation or a recommended direction (that is solution design, downstream);
- block the workflow (this skill is advisory by construction).

## Inputs

The user supplies, as markdown or pasted context:

1. **Project title + description** — *Required.* Enough to know what is being built and for whom. If absent/unreadable/empty: HALT and ask where it is (per `_shared/grounding.md`); never invent a project to reason over. Readable forms: a markdown file, an xlsx/csv path, a GitHub Project owner+number, a docs folder, or a pasted block.
2. **The phase** — *Required.* `design` or `decisions` — it selects the constraint scaffold (Step 1). If absent: HALT and ask which phase (per `_shared/grounding.md`); never guess the phase, because the wrong scaffold enumerates the wrong constraints.
3. **The evidence pool to cite from** — *Required.* Whatever is real and available: ratified requirement ids, governance/red-team evidence items, design-review findings (with severity), named NFR targets (e.g. RPO/RTO), a residency or data-boundary requirement, named doc sections. If absent/unreadable/empty: HALT and ask where the evidence lives (per `_shared/grounding.md`); never invent a citation. The richer and more specifically-identified this pool, the stronger the citations. (A *thin-but-present* pool is not absent — proceed and lean on `unverified — needs spike:`; see below.)
4. **The prior roadblock register** — *Optional* (re-run only). If absent: this is a first run — proceed with an empty prior set. When present, prior human dispositions and dismissal-memory carry forward (Step 6).

No-fabrication discipline is the contract `skills/_contract/grounding-no-absent-input`; the "do not invent a citation" rule in Step 3 is an instance of it.

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

## The method (numbered steps)

### Step 0 — Locate and verify the required inputs (DETERMINISTIC, pre-model)

Before any reasoning, check the three required inputs as file-level facts: a project title + description, a phase (`design` or `decisions`), and an evidence pool. Any one **absent, unreadable, or empty** → emit the clean halt below and **stop**. This is mechanical, never a judgement on whether the material "looks like enough"; a *thin-but-present* evidence pool is not absent and does not halt.

```
HALT — required input missing.

I can't enumerate roadblocks without the project material and the evidence to cite
from, and I won't invent either. Tell me where they live and I'll pick up from there.

I'm missing: <name each absent input — e.g. the evidence pool / the phase>.

I can read any of these:
  • a markdown file
  • an xlsx / csv file path
  • a GitHub Project (owner + project number)
  • a docs folder (markdown / text)
  • the material pasted directly into the chat

Which one, and where? (And which phase — design or decisions? Once you point me at it,
I'll enumerate + cite the roadblocks — nothing is assumed or invented until then.)
```

The halt copies the canonical exemplar in `skills/_contract/grounding-no-absent-input` (partial input → name exactly what is missing, never run on the part you have).

### Step 1 — Pick the phase scaffold (DETERMINISTIC)

Select the per-phase constraint checklist below. This is the deterministic base: even with no LLM, these prompts are the questions to walk every time. Use them as the lens for Step 3 — each is a place roadblocks habitually hide.

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

This is the judgement step. Reason over the project material **through the lens of the Step 1 scaffold**, and produce only roadblocks the material **genuinely supports**. For each one, fill three fields:

- **`constrains`** — the activity, choice, or capability being constrained (one phrase).
- **`cited_evidence`** — the specific evidence behind the constraint. Cite a **real source**: a ratified requirement id, a governance evidence item, a design finding *with its severity*, or a named doc section. If the constraint rests on an **unverified assumption**, prefix the citation with `unverified — needs spike:` and say exactly what must be benchmarked or confirmed.
- **`invalidates_choice`** — the concrete design or decision option this roadblock rules out (the choice a human must **not** take while the roadblock stands).

**Hard constraints on this step:**
- **Do not invent** constraints, requirements, or evidence the material does not imply. A roadblock with no citable basis is a hallucinated guardrail — worse than none.
- **Do not assign any status, severity, or disposition.** Every roadblock is simply *enumerated and cited*. `BLOCK` / `CAUTION` / `NOTE` and `spike_agreed` / `resolved_direction` / `accepted_as_grey` are the **human's** to add later.
- **Do not resolve, soften, or recommend around** a roadblock. "Here is the constraint and the option it forbids" — full stop.
- When unsure whether something is real, prefer `unverified — needs spike:` over a confident citation.

### Step 4 — Emit the register (NO STATUS)

Render the roadblocks in the output template below. Every row leaves the **Severity** and **Status / disposition (human-owned)** columns **empty** — literally blank, marked `— (human to dispose)`. The agent is structurally incapable of filling them; that is the invariant, not an oversight.

### Step 5 — Hand off to the human for disposition

The human reads the register and, per roadblock, records a **disposition** drawn from the controlled vocabulary — `spike_agreed` / `resolved_direction` / `accepted_as_grey`, with the advisory severity `BLOCK` / `CAUTION` / `NOTE` carried only on `accepted_as_grey` — defined in [`references/disposition-vocab.md`](references/disposition-vocab.md). A disposition only **flags drift**; it never silently re-opens or closes anything downstream.

### Step 6 — Re-run discipline: preserve dispositions + dismissal-memory (DETERMINISTIC)

When this step is re-run for the same project + phase:

- **(a) Replace only the open set.** Clear the prior *open* (agent-sourced, undispositioned) roadblocks for this project+phase and re-enumerate, so a re-run **replaces** rather than **appends** (no duplicates).
- **(b) Preserve every human disposition.** Any roadblock the human moved to `spike_agreed` / `resolved_direction` / `accepted_as_grey` is **never deleted** by a re-run.
- **(c) Dismissal-memory.** Do **not** re-create a freshly-enumerated roadblock that matches one the human already dispositioned, keyed on **`cited_evidence`** for this phase — a constraint is "the same constraint" when it rests on the same evidence, so unchanged evidence does not re-nag, but new evidence (a spike result, a new finding, a ratified requirement) changes the key and legitimately re-surfaces it for fresh disposition. Note in the output how many freshly-enumerated roadblocks were **suppressed by dismissal-memory**.

### Step 7 — The enumerate prompt (verbatim, for any LLM)

Paste this into any model that reads markdown. It reproduces the deterministic per-phase guidance and the cited-evidence format, and it forbids status by construction.

```
For the phase below, enumerate the ROADBLOCKS — constraints grounded in cited
evidence that rule out (invalidate) specific design or decision choices. A
roadblock names what is constrained, the evidence behind the constraint, and the
concrete choice that evidence forbids. Only enumerate and cite; never resolve,
dismiss, or set a status — a human owns that.

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
Do not assign any status — every roadblock is simply enumerated and cited.

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

> Enumerated + cited by this step. Descriptive and advisory.
> The agent emits NO status and NO severity — a human owns disposition.
> Severity legend (human-applied): BLOCK · CAUTION · NOTE.

_Re-run note: <N> freshly-enumerated roadblock(s) suppressed by dismissal-memory
(already dispositioned against unchanged evidence)._

| # | Constrains | Cited evidence | Invalidates choice | Severity | Status / disposition (human-owned) |
|---|---|---|---|---|---|
| R1 | client-facing record read | REQ-014 (ratified): no sensitive data leaves the security perimeter | reading client records into the app for in-product display (data egress) | — (human to dispose) | — (human to dispose) |
| R2 | in-perimeter model serving | unverified — needs spike: confirm an in-boundary model-serving option exists and meets latency target before sizing the design around it | sizing the design around an external/frontier model | — (human to dispose) | — (human to dispose) |
| R3 | deferring RPO | NFR-RPO (named target): RPO must be settled this phase | choosing a storage/sync option that leaves RPO undecided past decisions | — (human to dispose) | — (human to dispose) |

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

(Status/resolution/citation discipline lives in Step 3; re-run keying in Step 6. These add only what the steps do not already enforce.)

- **Cite findings with their severity.** "Design finding F3 (HIGH)" is a stronger guardrail than "a design concern."
- **`invalidates_choice` must be a concrete option, not a vague worry.** "Cross-project reads may be slow" is a worry; "do not serve the portfolio view from per-project synchronous fan-out reads" is a roadblock.
- **One constraint surface, one roadblock.** Don't bundle a data-boundary constraint and a performance constraint into one row — they cite different evidence and dispose differently.
- **Empty is a valid answer.** If the phase + material genuinely support no roadblocks, emit none. Do not pad the register to look thorough.
