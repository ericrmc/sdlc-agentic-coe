---
name: surface-solution-options
description: When retrieval finds no approved match, populate 2-3 rival candidate solution shapes side-by-side with 'do nothing' always present; candidates are menus, never a ranked recommendation; on success, prompt to promote to the pattern library.
one_liner: Lay rival solution shapes side by side when no pattern fits.
aliases: [solution options, design alternatives, options analysis, trade study, candidate architectures, build vs buy, no pattern fits, explore the design space]
when_to_use: Pattern retrieval came back honest-empty — no approved pattern fits the solution shape with enough confidence to adopt. Reach here only after recommend-component-patterns finds nothing, to open the space with rival shapes before anyone commits.
output_kinds: [menu, question, halt]
deterministic_fallback: the side-by-side candidate columns skeleton with a mandatory 'do nothing' column
suggested_tier: frontier
neighbours: |
  Before: architect/recommend-component-patterns (run it first; reach here only when it returns honest-empty).
  After: architect/propagate-pattern-nfrs (once a shape is chosen and promoted) — or library/author-component-pattern to promote the chosen shape.
---

# surface-solution-options — rival shapes when nothing fits

Open the solution space when no approved pattern matches: lay 2-3 credible rival shapes side by side, with "do nothing" always present, and hand a `menu` to pick / merge / kill. Never crown a winner.

## Purpose

Runs only when `recommend-component-patterns` came back honest-empty — a legitimate,
non-failing outcome, not an error. The response is structured exploration, not invention:
surface distinct, credible rival shapes side by side so a human narrows the trade-space.
Output is markdown a human acts on (a table + questions) — no row write, no workflow advance.
The three safety disciplines (menu-not-recommendation, mandatory `Do nothing`, agent-populates/
human-disposes) are enforced at Step 2, Step 5, and the anti-patterns below.

## When to use

- `recommend-component-patterns` returned **honest-empty** — no approved pattern
  in the library matches the project's solution shape with enough confidence to
  adopt.
- The solution space is genuinely **novel for the organisation** (or novel enough
  that the proven shapes don't carry it) and needs exploring before anyone
  commits.

**Do not use this skill when retrieval did find a match.** Adopting an approved
pattern is the fast path and the prominent move; exploration is the fallback for
when the fast path is honestly unavailable. If you reach here while a decent
pattern exists, go back and adopt — don't explore your way around a governed
shape that already fits.

> **Multi-agent option (advisory).** Deepen by populating one rival shape per parallel
> sub-agent and merging what succeeds — never required, adds coverage. See
> `../../_contract/parallel-agents`.

## Inputs

The user supplies, as markdown or plain text:

| Input | Required | What it is |
|---|---|---|
| **Ratified outcomes + derived requirements** | **Required** | The project's `BO-N` outcomes and `REQ-N` requirements (each carrying `derives_from: BO-N` for the outcome it serves). This is what each candidate must serve and what you trace back to. *If absent/unreadable/empty: HALT and ask where the ratified outcomes + requirements live (per `_shared/grounding.md`); never invent an outcome or `REQ-N` to justify a shape.* |
| **The honest-empty signal** | **Required** | Confirmation that pattern retrieval found no adoptable approved pattern — ideally the near-misses it *did* surface and why each fell short, so candidates can deliberately diverge from them. *If absent: HALT and ask whether `recommend-component-patterns` actually returned honest-empty (per `_shared/grounding.md`) — exploration is strictly the no-fit fallback; never assume the library was empty. If a pattern in fact fits, go back and adopt it.* |
| **NFRs / constraints** | optional | Any attached NFRs already in play, plus hard constraints (data residency, runtime, latency targets). These bound the space and seed roadblocks. *If absent: proceed; never invent a constraint.* |
| **Known roadblocks register** | optional | Any existing roadblock output for the project. Exploration commonly *adds* to it; start from what's already known. *If absent: start a fresh roadblock list; never invent a prior one.* |
| **Space-expansion notes** | optional | Human corrections to a constraint the model was pretrained to assume — *"this runtime can run background tasks."* These **oblige re-proposal** (see Step 6). |

Stay grounded in the outcomes. **A candidate exists to serve named `BO-N`
outcomes** — if a shape doesn't trace to outcomes, it is a daydream, not a
candidate. Do not invent requirements the project never stated to justify a shape.
(This is the no-fabrication keystone applied to outcomes — see
`skills/_contract/grounding-no-absent-input`.)

## Grounding (quoted)

Carries the no-fabrication keystone (see `skills/_contract/grounding-no-absent-input`):

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

The base is deterministic (the columns skeleton); one step requires a model (the
even-handed population of rival shapes). The structure is mechanical and falls
back cleanly; the reasoning is the only place a model is needed, and it is bounded
by hard "no winner" rules.

### Step 0 — Locate / verify the required inputs (deterministic, pre-model)

Before exploring, confirm both Required inputs are present as a file-level fact: the
**ratified outcomes + derived requirements** (what every candidate must serve) and the
**honest-empty signal** (the reason exploration is happening at all). This is mechanical —
absent / unreadable / empty — never a judgement on "is the space novel enough."

- **Outcomes + requirements absent/unreadable/empty** → emit the clean HALT below and stop.
- **Honest-empty signal absent** → HALT and ask whether `recommend-component-patterns` really
  returned no adoptable pattern. Never assume the library was empty; if a pattern fits, go
  back and adopt it.

```
HALT — required input missing.

I can't open the solution space without the ratified outcomes + requirements every candidate
must serve, and I won't invent them. Point me at the outcomes / requirements and I'll lay
out rival shapes side by side — nothing is assumed until then.

I can read any of: a markdown file · an xlsx/csv path · a GitHub Project (owner + number)
· a docs folder · the rows pasted directly here. Which one, and where?
```

### Step 1 — Confirm you are actually here (honest-empty check, advisory)

Before exploring, confirm retrieval really returned honest-empty. If a credible
approved pattern exists, stop and adopt it — exploration is strictly the
no-fit fallback. Capture *why* retrieval came up empty (the near-misses and
their gaps); a good exploration deliberately spans away from the shapes that
*almost* fit, so the human sees real alternatives, not three flavours of the
same near-miss.

### Step 2 (DETERMINISTIC) — render the columns skeleton

Before any model reasoning, lay down the deterministic structure. This is the
base — mechanical, repeatable, and exactly what you fall back to if no model is
available. Render a side-by-side comparison **table** with one column per
candidate plus the mandatory status-quo column:

- **2-3 candidate columns**, codenamed **alphabetically** — `Candidate A`,
  `Candidate B`, `Candidate C` — so the order is the alphabet and carries **no
  preference signal**. Never name them "Recommended / Alternative / Fallback."
- **A `Do nothing` column, always last but co-equal.** Not "Option 0", not
  greyed out — a real column with the same rows filled in honestly (what the
  status quo costs, what it leaves unserved, what risk it carries).
- **A fixed set of comparison rows**, identical across every column so the shapes
  are read on the same axes:
  - **Shape in one line** — the architectural gist.
  - **Outcomes served** — which `BO-N` it serves well (cite ids), which it
    serves weakly or not at all.
  - **Key components** — the named pieces (kept deliberately light — WHAT, not a
    full design).
  - **Roadblocks hit** — `R#` ids this shape runs into (filled by Step 3, **no
    feasibility status**).
  - **What you'd trade** — the honest cost: effort shape, operational burden,
    lock-in, reversibility.
  - **Reversibility** — how cheaply you can back out if it's wrong (a status-quo
    column usually wins this row, and that's the point).

The empty skeleton (no model, deterministic fallback) is shown in
[Output format](#output-format) below — it is a legitimate, useful output that
gives an architect the axes to fill by hand.

### Step 3 (compose `enumerate-roadblocks`) — fill the roadblock row as cited facts

Exploration is where roadblocks surface — a candidate shape runs into a real
constraint (runtime, data residency, a maturity gap). **Do not invent a new
roadblock vocabulary here.** Compose the
[`enumerate-roadblocks`](../../challenge/enumerate-roadblocks/SKILL.md) skill:
each roadblock a candidate hits is **enumerated and cited** (what it is, what it
constrains, what it invalidates if it holds) and assigned an `R#` id that the
candidate's **Roadblocks hit** row references.

Carry the register's non-negotiable convention:

> The agent / analysis **enumerates and cites** a roadblock; **a human owns the
> `Status` field.** "spike-agreed", "resolved-direction", "accepted-as-grey" are
> feasibility *dispositions* — a human's call, **never the agent's.**

So a roadblock cell reads *"hits R3 (maturity of a sync component)"* — a **cited
fact**. It **never** reads *"Candidate B: infeasible"* or *"Candidate B:
feasible"*. An agent-proposed feasibility status is a recommendation in disguise
and is the single most tempting violation of this skill. The candidate carries
the *fact* it hits; the human carries the *verdict* on whether that's a stopper.

### Step 4 (DETERMINISTIC) — render the post-choice prompts (seed the fast path)

After the comparison table, render the two human-facing prompts that close the
loop — both as plain markdown, both human-owned:

1. **The narrowing `menu`** — *"Pick one, merge two, or kill all and do
   nothing."* This is the human decision point. The agent stops here; it does not
   pick.
2. **The promotion `question`** — *"If you chose a shape: promote it to the
   pattern library?"* On a chosen shape, this routes to
   [`author-component-pattern`](../../library/author-component-pattern/SKILL.md):
   the explored shape becomes a candidate pattern (PR-reviewed, evidence-bearing,
   dated, with validity/sunset metadata) so the next project retrieves it on the
   fast path. Every expensive explore seeds a future fast path — the whole reason
   exploration is worth its cost.

Neither prompt is pre-answered. The promotion prompt is offered, never assumed —
promotion is a human ratification (a person merges the PR) with evidence, not a
field the agent sets.

### Step 5 (MODEL REASONING STEP) — populate the rival shapes, grounded, no winner

Now fill the skeleton by reasoning over the project context. This is the one step
that requires a model. Use this prompt:

> The approved pattern library returned **no adoptable match** for this project,
> so there is no fast path — the job is to open the solution space, not to
> recommend a solution.
>
> You are given the project's ratified business outcomes (`BO-N`) and derived
> requirements (`REQ-N`, each tracing to its outcome via `derives_from: BO-N`),
> the near-misses retrieval surfaced (and why each fell short), any
> NFRs/constraints, and any known roadblocks.
>
> **Produce 2-3 genuinely distinct, credible candidate solution shapes**, plus a
> **`Do nothing`** column, filling every comparison row for each:
>
> - **Distinct** — span the trade-space; make different architectural bets (buy vs
>   build vs compose; sync vs scheduled-poll; centralise vs federate); deliberately
>   diverge from the near-misses retrieval already rejected.
> - **Credible** — each plausibly serves the named outcomes. Cite **which `BO-N`
>   each shape serves well and which it serves weakly or not at all.**
> - **Grounded** — stay inside what outcomes and constraints actually say. Name
>   light, real components (WHAT, not a full design). Do not invent requirements.
> - **Roadblock-honest** — name the roadblocks each shape hits as **cited facts with
>   `R#` ids** (what each constrains, what it invalidates if it holds). **Never**
>   emit a feasibility status — that disposition is the human's.
> - **`Do nothing` is a real column** — fill it honestly (what it leaves unserved,
>   costs to keep, risk it carries, usually-strong reversibility). Do not strawman it.
>
> **Hard constraints on your output:**
> - **No winner.** No ranking, no "recommended", no starred favourite, no order
>   that implies preference. Codename the candidates **alphabetically**; the
>   alphabet is the only order.
> - **No verdict.** You enumerate and cite; you never adjudicate feasibility,
>   quality, or which the human should choose.
> - **Even-handed tone** — laying out a map, not selling a route. Give every
>   column, including `Do nothing`, its fair best case and its honest worst case.
>
> Return the filled comparison table, the cited roadblock list, and the two
> closing prompts (narrow; promote-if-chosen). No prose outside the structure
> that pushes toward one option.

### Step 6 — Honour space-expansion and re-propose

If the human supplied (or supplies after seeing the map) a **space-expansion**
note — a correction to a constraint the model was pretrained to assume, e.g.
*"this runtime can run background tasks"* — you are **obliged to re-propose.**
The earlier exploration may have silently dropped a whole class of shape because
of a false constraint; widen the box and surface the candidates that now become
credible. The human widening the box is a first-class input, not noise — treat it
as a trigger to regenerate, not a comment to acknowledge.

### Step 7 — Hand off as a PR for the human to narrow

Write the markdown into the project's repo (e.g.
`solution/options/candidate-shapes.md`) and open a pull request. **The human
narrows by acting on the diff** — keep the chosen column, strike the rest, and
(if a shape was chosen) follow the promotion prompt into
`author-component-pattern`. There is no disposition record. The PR *is* the
surface where the human picks / merges / kills. Light and advisory.

## Output format

The user gets back one markdown file shaped like this. The
[deterministic fallback](#deterministic-fallback) is this same shape with the
candidate cells left empty.

```markdown
# Solution options — <Project Title>

> Pattern retrieval found **no adoptable approved pattern** — there is no fast
> path here, so the space was explored. Below are rival candidate shapes, side by
> side, with **do nothing** as a co-equal column. **These are a menu, not a
> recommendation** — pick one, merge two, or do nothing. Nothing here is ranked,
> and no column is preferred. Narrow by acting on this PR.

## Candidate shapes

| | **Candidate A** | **Candidate B** | **Do nothing** |
|---|---|---|---|
| **Shape** | Compose two existing internal services behind a thin sync API | Adopt a managed third-party service and integrate via webhook | Keep the current manual spreadsheet handoff |
| **Outcomes served** | Serves **BO-1, BO-2** well; **BO-3** weakly (no audit trail) | Serves **BO-1, BO-3** well; **BO-2** only if the vendor exposes the field | Serves **none** fully; BO-1 partially, by hand |
| **Key components** | Internal Svc-X, Svc-Y, a small sync API, a state table | Vendor SaaS, webhook receiver, a mapping layer | Existing spreadsheet + email |
| **Roadblocks hit** | hits **R3** (sync-component maturity — reliability) | hits **R2** (data egress to an external vendor) | hits **R-none**; the known-bad status quo |
| **What you'd trade** | Higher build effort, full control, no new vendor | Low build effort, recurring cost + vendor lock-in, egress review | Zero build, ongoing manual hours + error rate persist |
| **Reversibility** | Moderate — owned code, can re-shape | Low — data + workflow now live in a vendor | High — change nothing, change back anytime |

> See the cited roadblocks below. **Status of each roadblock is human-owned** —
> these cells state the *fact* a shape hits, never a feasibility verdict.

## Roadblocks surfaced (cited facts — status human-owned)

*(composed via `enumerate-roadblocks`)*

### R3 — Maturity of the sync component
- **Constrains:** the reliability of the sync API in **Candidate A**.
- **Invalidates if it holds:** any shape assuming low-latency, lossless sync.
- **Status (human-owned):** _unset — a human dispositions this._

### R2 — In-boundary data
- **Constrains:** what **Candidate B** may send to the external vendor.
- **Invalidates if it holds:** routing client data to an out-of-boundary SaaS.
- **Status (human-owned):** _unset — a human dispositions this._

## Narrow the space  (human decision)

- [ ] **Pick a shape** — keep one column, strike the rest in this PR.
- [ ] **Merge** — combine two shapes into a hybrid (describe the merge).
- [ ] **Kill all / do nothing** — a legitimate, non-failing choice.

## Promote to the pattern library?  (offered, not assumed)

> **If you chose a shape:** promote it so the next project fast-paths what this
> one explored. Routes to `author-component-pattern` — the shape becomes a
> PR-reviewed pattern carrying evidence, approved_at/validity_check_months/sunset_at metadata.
> Every expensive explore seeds a future fast path.
- [ ] Promote the chosen shape to a candidate pattern.
- [ ] Not yet — explore further / leave un-promoted.
```

### Deterministic fallback

If no model is available, emit the empty skeleton — the comparison table with the
fixed axes, a co-equal `Do nothing` column, and the two closing prompts — and
stop. This is a legitimate, useful output: it gives an architect the exact axes
to populate by hand, and it structurally **cannot** omit `Do nothing` or rank the
candidates.

```markdown
# Solution options — <Project Title>  (skeleton — fill by hand)

> No approved pattern matched. Rival shapes below are a **menu, not a
> recommendation**. **Do nothing** is mandatory and co-equal. No column is ranked.

| | **Candidate A** | **Candidate B** | **(Candidate C)** | **Do nothing** |
|---|---|---|---|---|
| **Shape** | | | | |
| **Outcomes served** | <which BO-N well / weakly> | | | <what stays unserved> |
| **Key components** | | | | <status quo pieces> |
| **Roadblocks hit** | <R# — fact, no verdict> | | | |
| **What you'd trade** | | | | <ongoing cost of status quo> |
| **Reversibility** | | | | <usually high> |

<!-- Quality bar — every candidate must pass all five:
     [ ] distinct (spans the trade-space, not 3 of one idea)
     [ ] grounded (serves named BO-N; cites which weakly)
     [ ] roadblocks are CITED FACTS with R# ids — NO feasibility status
     [ ] no winner — alphabetical codenames, no ranking, no star
     [ ] 'Do nothing' is a real, honestly-filled column -->

## Narrow the space (human decision): pick / merge / kill
## Promote to pattern library? (only if a shape was chosen) -> author-component-pattern
```

## Anti-patterns — reject these on sight

- **A feasibility status** — *"Candidate B: infeasible"*. The agent cites roadblock
  facts, never the verdict; the disposition is human-owned (Step 3). The single most
  tempting violation.
- **Dropping "do nothing"** — a menu of two build options has already decided
  something must be built. Always co-equal, honestly filled, never strawmanned.
- **A ranked menu** — best-first order, a "Recommended" label, or a starred favourite
  is a smuggled verdict, not a menu (see `../../_contract/target-rule-output-kinds`).
- **Three flavours of one idea** — candidates sharing one architectural bet are not
  exploration.
- **Hand-rolling roadblock vocabulary** instead of composing `enumerate-roadblocks`.
- **Skipping the promotion prompt on a win** — a fast path thrown away; the next
  project re-explores at senior cost.
