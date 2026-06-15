---
name: surface-solution-options
description: When retrieval finds no approved match, populate 2-3 rival candidate solution shapes side-by-side with 'do nothing' always present; candidates are menus, never a ranked recommendation; on success, prompt to promote to the pattern library.
when_to_use: recommend-component-patterns returned honest-empty and the space needs exploring
output_kinds: [menu, question]
deterministic_fallback: the side-by-side candidate columns skeleton with a mandatory 'do nothing' column
suggested_tier: opus
---

# surface-solution-options — rival shapes when nothing fits

> FORGE **Stage 5 — Solution options** (`docs/06` §3). You are the **Explorer**.
> Retrieval over the approved Pattern Library came back honest-empty — there is
> no fast-track. The job now is not to *recommend* a solution; it is to **open
> the space** so a human can narrow it. You lay 2-3 credible rival shapes side by
> side, with **"do nothing" always present as a column**, and hand the human a
> `menu` to pick / merge / kill. You never crown a winner.

## Purpose

This skill runs **only when the fast path failed**. Stage 4
(`recommend-component-patterns`) ran a real retrieval over the firm's approved
patterns and returned nothing adoptable — no governed shape carries the project's
shape, so its NFRs cannot flow in for free. That is the honest-empty signal, and
it is a legitimate, non-failing outcome, not an error.

When that happens the platform does **not** fall back to "the agent invents the
answer." It falls back to **structured exploration**: surface a small set of
genuinely distinct, credible candidate solution shapes, side by side, so the
human can see the trade-space and *narrow* it themselves. The discipline that
makes this safe is the same one that governs the whole library:

- **Candidates are a `menu`, never a ranked recommendation.** N un-ranked, equal
  options, alphabetical codenames so order carries no signal, no starred
  favourite, no "preferred" badge. The moment order implies preference it has
  become a verdict (see `_contract/target-rule-output-kinds`).
- **"Do nothing" is always a column.** The status quo is a real, often
  underrated option. A menu that omits it has already pre-decided that *something*
  must be built — which is itself a smuggled recommendation.
- **The agent populates; the human disposes.** Pick one, merge two, kill the
  rest — that is the human's call. The agent's whole job is to make the space
  legible, cited, and even-handed.

The economic payoff sits at the end: **every expensive explore seeds a future
fast-track.** When the human lands on a shape, this skill prompts *"Promote to
pattern library?"* — so the next delivery lead who hits this same shape retrieves
it as an approved pattern in Stage 4 and never has to explore it again.

This skill produces **markdown a human acts on** — a comparison table and a set
of questions. It writes no database row, enforces no gate, advances no state
machine. Light and advisory by design.

## When to use

- `recommend-component-patterns` (Stage 4) returned **honest-empty** — no
  approved pattern in the library matches the project's solution shape with
  enough confidence to adopt.
- The solution space is genuinely **novel for the firm** (or novel enough that
  the proven shapes don't carry it) and needs exploring before anyone commits.

**Do not use this skill when retrieval *did* find a match.** Adopting an approved
pattern is the fast path and the prominent move; exploration is the fallback you
reach for only when the fast path is honestly unavailable. If you find yourself
reaching here while a decent pattern exists, go back and adopt — don't explore
your way around a governed shape that already fits.

## Inputs

The user supplies, as markdown or plain text:

| Input | Required | What it is |
|---|---|---|
| **Ratified outcomes + derived requirements** | yes | The project's `BO-N` outcomes and `TR-N.M` requirements (the output of `decompose-intake-to-outcomes`). This is what each candidate must serve and what you trace back to. |
| **The honest-empty signal** | yes | Confirmation that Stage 4 retrieval found no adoptable approved pattern — ideally the near-misses it *did* surface and why each fell short, so candidates can deliberately diverge from them. |
| **NFRs / constraints** | optional | Any attached NFRs already in play, plus hard constraints (data residency, runtime, latency targets). These bound the space and seed roadblocks. |
| **Known roadblocks register** | optional | Any existing `enumerate-roadblocks` output for the project. Exploration commonly *adds* to it; start from what's already known. |
| **Space-expansion notes** | optional | Human corrections to the box you were pretrained out of — *"Databricks Apps **can** run background tasks."* These **oblige re-proposal** (see Step 6). |

Stay grounded in the outcomes. **A candidate exists to serve named `BO-N`
outcomes** — if a shape doesn't trace to outcomes, it is a daydream, not a
candidate. Do not invent requirements the project never stated to justify a shape.

## The method (numbered steps)

The spine is deterministic (the columns skeleton); one step requires a model (the
even-handed population of rival shapes). This split is the contract: the
structure is mechanical and falls back cleanly; the reasoning is the only place a
model is needed, and it is bounded by hard "no winner" rules.

### Step 1 — Confirm you are actually here (honest-empty gate, advisory)

Before exploring, confirm Stage 4 really returned honest-empty. If a credible
approved pattern exists, stop and adopt it — exploration is strictly the
no-fit fallback. Capture *why* retrieval came up empty (the near-misses and
their gaps); a good exploration deliberately spans away from the shapes that
*almost* fit, so the human sees real alternatives, not three flavours of the
same near-miss.

### Step 2 (DETERMINISTIC SPINE) — render the columns skeleton

Before any LLM reasoning, lay down the deterministic structure. This is the
*spine* — mechanical, repeatable, and exactly what you fall back to if no model
is available. Render a side-by-side comparison **table** with one column per
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
[`enumerate-roadblocks`](../enumerate-roadblocks/SKILL.md) skill: each roadblock
a candidate hits is **enumerated and cited** (what it is, what it constrains,
what it invalidates if it holds) and assigned an `R#` id that the candidate's
**Roadblocks hit** row references.

Carry the register's non-negotiable convention verbatim (it is the same one in
`docs/02-roadblocks-register.md`):

> The agent / analysis **enumerates and cites** a roadblock; **a human owns the
> `Status` field.** "spike-agreed", "resolved-direction", "accepted-as-grey" are
> feasibility *dispositions* — a human's call, **never the agent's.**

So a roadblock cell reads *"hits R3 (Lakebase maturity)"* — a **cited fact**. It
**never** reads *"Candidate B: infeasible"* or *"Candidate B: feasible"*. An
agent-proposed feasibility status is a recommendation in disguise and is the
single most tempting violation of this skill. The candidate carries the *fact* it
hits; the human carries the *verdict* on whether that's a stopper.

### Step 4 (DETERMINISTIC) — render the post-choice prompts (seed the fast-track)

After the comparison table, render the two human-facing prompts that close the
loop — both as plain markdown, both human-owned:

1. **The narrowing `menu`** — *"Pick one, merge two, or kill all and do
   nothing."* This is the human gate of Stage 5. The agent stops here; it does
   not pick.
2. **The promotion `question`** — *"If you chose a shape: promote it to the
   pattern library?"* On a chosen shape, this routes to
   [`author-component-pattern`](../author-component-pattern/SKILL.md): the
   explored shape becomes a candidate pattern (PR-reviewed, evidence-bearing,
   dated, with validity/sunset metadata) so the next project retrieves it on the
   fast path. **Every expensive explore seeds a future fast-track** — this is the
   line in `docs/06` §3 Stage 5, and it is the whole reason exploration is worth
   its cost.

Neither prompt is pre-answered. The promotion prompt is offered, never assumed —
promotion is a human ratification with evidence, not a field the agent sets.

### Step 5 (LLM REASONING STEP) — populate the rival shapes, grounded, no winner

Now fill the skeleton by reasoning over the project context. This is the one step
that requires a model. Use this prompt verbatim:

> You are the **Explorer**. The firm's approved Pattern Library returned **no
> adoptable match** for this project, so there is no fast path — your job is to
> open the solution space, not to recommend a solution.
>
> You are given the project's ratified business outcomes (`BO-N`) and derived
> requirements (`TR-N.M`), the near-misses retrieval surfaced (and why each fell
> short), any NFRs/constraints, and any known roadblocks.
>
> **Produce 2-3 genuinely distinct, credible candidate solution shapes**, plus a
> **`Do nothing`** column, filling every comparison row for each:
>
> - **Distinct** — the candidates must span the trade-space, not offer three
>   flavours of one idea. Deliberately diverge from the near-misses retrieval
>   already rejected. Make different architectural bets (e.g. buy vs build vs
>   compose; sync vs scheduled-poll; centralise vs federate) so the human sees a
>   real choice.
> - **Credible** — each must plausibly serve the named outcomes. Cite **which
>   `BO-N` each shape serves well and which it serves weakly or not at all** — be
>   honest about every column's blind spots, including the strong ones.
> - **Grounded** — stay inside what the outcomes and constraints actually say.
>   Name light, real components (WHAT, not a full design). Do not invent
>   requirements to justify a shape.
> - **Roadblock-honest** — for each shape, name the roadblocks it hits as **cited
>   facts with `R#` ids**. State what each roadblock constrains and what it
>   invalidates if it holds. **Never** emit a feasibility status
>   ("feasible/infeasible") — that disposition is the human's.
> - **`Do nothing` is a real column** — fill it honestly: what the status quo
>   leaves unserved, what it costs to keep, what risk it carries, and (usually)
>   its strong reversibility. Do not strawman it.
>
> **Hard constraints on your output:**
> - **No winner.** No ranking, no "recommended", no starred favourite, no order
>   that implies preference. Codename the candidates **alphabetically**; the
>   alphabet is the only order.
> - **No verdict.** You enumerate and cite; you never adjudicate feasibility,
>   quality, or which the human should choose.
> - **Even-handed tone** — an explorer laying out a map, not an advocate selling
>   a route. Give every column, including `Do nothing`, its fair best case and
>   its honest worst case.
>
> Return the filled comparison table, the cited roadblock list, and the two
> closing prompts (narrow; promote-if-chosen). No prose outside the structure
> that pushes toward one option.

### Step 6 — Honour space-expansion and re-propose

If the human supplied (or supplies after seeing the map) a **space-expansion**
note — a correction to a constraint you were pretrained to assume, e.g.
*"Databricks Apps **can** run background tasks"* — you are **obliged to
re-propose.** The earlier exploration may have silently dropped a whole class of
shape because of a false constraint; widen the box and surface the candidates
that now become credible. The human widening the box is a first-class input, not
noise — treat it as a trigger to regenerate, not a comment to acknowledge.

### Step 7 — Hand off as a PR for the human to narrow

Write the markdown into the project's repo (e.g.
`solution/options/candidate-shapes.md`) and open a pull request. **The human
narrows by acting on the diff** — keep the chosen column, strike the rest, and
(if a shape was chosen) follow the promotion prompt into
`author-component-pattern`. There is no gate, no state machine, no disposition
record. The PR *is* the surface where the human picks / merges / kills. Light and
advisory.

## Output format

The user gets back one markdown file shaped like this. The
[deterministic fallback](#deterministic-fallback) is this same shape with the
candidate cells left empty.

```markdown
# Solution options — <Project Title>

> Stage 4 retrieval found **no adoptable approved pattern** — there is no
> fast-track here, so we explored the space. Below are rival candidate shapes,
> side by side, with **do nothing** as a co-equal column. **These are a menu, not
> a recommendation** — pick one, merge two, or do nothing. Nothing here is
> ranked, and no column is preferred. Narrow by acting on this PR.

## Candidate shapes

| | **Candidate A** | **Candidate B** | **Do nothing** |
|---|---|---|---|
| **Shape** | Compose two existing internal services behind a thin sync API | Adopt a managed third-party service and integrate via webhook | Keep the current manual spreadsheet handoff |
| **Outcomes served** | Serves **BO-1, BO-2** well; **BO-3** weakly (no audit trail) | Serves **BO-1, BO-3** well; **BO-2** only if the vendor exposes the field | Serves **none** fully; BO-1 partially, by hand |
| **Key components** | Internal Svc-X, Svc-Y, a small sync API, a state table | Vendor SaaS, webhook receiver, a mapping layer | Existing spreadsheet + email |
| **Roadblocks hit** | hits **R3** (Lakebase maturity — sync reliability) | hits **R2** (in-boundary LLM / data egress to vendor) | hits **R-none**; the known-bad status quo |
| **What you'd trade** | Higher build effort, full control, no new vendor | Low build effort, recurring cost + vendor lock-in, egress review | Zero build, ongoing manual hours + error rate persist |
| **Reversibility** | Moderate — owned code, can re-shape | Low — data + workflow now live in a vendor | High — change nothing, change back anytime |

> See the cited roadblocks below. **Status of each roadblock is human-owned** —
> these cells state the *fact* a shape hits, never a feasibility verdict.

## Roadblocks surfaced (cited facts — status human-owned)

*(composed via `enumerate-roadblocks`)*

### R3 — Lakebase maturity / Postgres→Delta sync
- **Constrains:** the reliability of the sync API in **Candidate A**.
- **Invalidates if it holds:** any shape assuming low-latency, lossless sync.
- **Status (human-owned):** _unset — a human dispositions this._

### R2 — In-boundary data
- **Constrains:** what **Candidate B** may send to the external vendor.
- **Invalidates if it holds:** routing client data to an out-of-boundary SaaS.
- **Status (human-owned):** _unset — a human dispositions this._

## Narrow the space  (human gate)

- [ ] **Pick a shape** — keep one column, strike the rest in this PR.
- [ ] **Merge** — combine two shapes into a hybrid (describe the merge).
- [ ] **Kill all / do nothing** — a legitimate, non-failing choice.

## Promote to the pattern library?  (offered, not assumed)

> **If you chose a shape:** promote it so the next project fast-tracks what this
> one explored. Routes to `author-component-pattern` — the shape becomes a
> PR-reviewed pattern carrying evidence, validated_on/review_by/sunset metadata.
> Every expensive explore seeds a future fast-track.
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

<!-- Explorer quality bar — every candidate must pass all five:
     [ ] distinct (spans the trade-space, not 3 of one idea)
     [ ] grounded (serves named BO-N; cites which weakly)
     [ ] roadblocks are CITED FACTS with R# ids — NO feasibility status
     [ ] no winner — alphabetical codenames, no ranking, no star
     [ ] 'Do nothing' is a real, honestly-filled column -->

## Narrow the space (human gate): pick / merge / kill
## Promote to pattern library? (only if a shape was chosen) -> author-component-pattern
```

## Notes & anti-patterns

**Anti-patterns — reject these on sight:**

- **A ranked menu.** Columns ordered best-first, or one labelled "Recommended" /
  "Preferred" / "Option 1 (best)", or a starred favourite. A real `menu` is
  un-ranked and equal — **alphabetical codenames so order carries no signal.** The
  moment order implies preference it is a verdict, not a menu. (`recommendation`
  is not a fifth output kind; it is the smuggled verdict — see
  `_contract/target-rule-output-kinds`.)
- **Dropping "do nothing".** A menu of two build options with no status-quo
  column has already decided *something must be built.* The status quo is a real,
  co-equal option — and on the reversibility axis it usually wins. Always include
  it; fill it honestly; never strawman it.
- **A feasibility status.** *"Candidate B: infeasible"* / *"Candidate A:
  feasible."* The agent **cites the roadblocks a shape hits** as facts; the
  feasibility *disposition* is human-owned. This is the single most tempting
  violation of this skill — the roadblock row carries the fact, never the verdict.
- **Three flavours of one idea.** Candidates that all make the same architectural
  bet are not exploration — they are one option wearing three hats. Make the bets
  genuinely diverge (buy/build/compose, sync/poll, centralise/federate), and
  deliberately span away from the near-misses retrieval already rejected.
- **Inventing requirements to justify a shape.** Padding the outcomes so a
  pet architecture looks necessary. Stay grounded in the ratified `BO-N`; a
  candidate serves the outcomes that exist, or it is not a candidate.
- **Inventing a new roadblock vocabulary.** Don't hand-roll roadblock prose here;
  compose `enumerate-roadblocks` so the register stays one shape, with
  human-owned status, across the whole method.
- **Skipping the promotion prompt on a win.** A chosen-and-not-promoted shape is
  a fast-track thrown away — the next project re-explores the same space at senior
  cost. Always offer promotion (never *assume* it). It is the economic point of
  paying for exploration.

**Notes:**

- **Honest-empty is the trigger, not a failure.** Reaching this skill means
  Stage 4 retrieval did its job and told the truth: no governed shape fits.
  Exploration is the designed response, not a degraded one.
- **The agent populates; the human narrows.** Pick / merge / kill is the human
  gate of Stage 5. The agent's contribution is a legible, cited, even-handed map —
  it stops at the menu and waits.
- **Space-expansion obliges re-proposal.** When a human widens the box you were
  pretrained out of, that is a regenerate trigger, not a comment to nod at. The
  most valuable candidate is often the one a false constraint hid.
- **This output is never a row write.** It is markdown — a comparison and a set
  of questions — narrowed by a human acting on a PR. No gate, no state machine, no
  feasibility disposition lives in this skill. Light and advisory.
