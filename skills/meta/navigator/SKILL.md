---
name: navigator
description: The universal entry point for an agent USING this library. Ask the runner what they want, route to the right skill group, and walk the engagement one stage at a time — ingest → understand → challenge → derive-capabilities → recommend-component-patterns → architect → panel → deliver — looping at each stage until the human is satisfied, then advancing. It routes only to skills that actually exist on disk; it never authors project content and never decides satisfaction. Use it when you do not yet know which skill to reach for, or want to be walked through an engagement.
one_liner: The library's front door — asks what you want, then walks the engagement one stage at a time, routing only to skills that exist.
aliases: [where do I start, walk me through it, guide me, entry point, route me to a skill, which skill next, take me through the flow, navigate the library, start an engagement, what do I run first]
when_to_use: you are an agent handed an engagement and unsure which skill to run, want a tailored start-here + ordered run, or want to be walked stage by stage with a re-run/advance prompt between each
output_kinds: [menu, question, halt]
deterministic_fallback: the static GETTING-STARTED persona table ("If you are an agent doing X, start here") + the skills/MAP.md category table and end-to-end flow — read them directly and pick the row that matches the engagement; the navigator is their engagement-aware reader, never their replacement
suggested_tier: light
tier_reason: pure routing and sequencing over a fixed skill graph — it reads each skill's description/when_to_use/neighbours and orders "this usually helps before that"; it weighs nothing about the project and authors no project content
neighbours:
  before: skills/MAP.md (the static index the navigator reads and complements — the category table and flow are the source of truth; the navigator is their dynamic, engagement-aware reader)
  after: skills/meta/author-a-skill (the sibling meta-skill — when the runner wants to ADD to the library rather than use it, route there)
---

# navigator — the library's front door

You are an agent that was handed an engagement and does not yet know which skill to reach
for. This skill is the **front door**: it asks what you want, points you at the right place,
and then **walks the engagement one stage at a time**, looping at each stage until the human
is satisfied and only then advancing.

It does exactly two jobs and nothing else:

1. **Route.** Read the engagement description, the static index in `skills/MAP.md`, and each
   skill's `description` / `when_to_use` / `aliases` / `neighbours`, then return a tailored
   **menu**: a single best next move, an ordered run for the rest, and what to probably skip.
2. **Walk.** Hand off to one stage skill, then ask whether the human ratified that stage and
   whether to advance or re-run. It walks; it never drives.

> **It routes; it never authors.** Every output is a `menu` (skills to run), a `question`
> (which way to go), or a `halt` (it cannot tell what the engagement even is). It emits **no
> `proposal`** — it never produces a requirement, a design, a finding, or any project content.
> That is the downstream skill's job, on the downstream skill's own grounding.

> **It carries NO grounding state between stages.** The navigator does not hold or pass along
> the project's requirements, keys, or outputs. Each stage skill **re-grounds itself** from the
> real project files and **halts on its own** if its input is missing. The navigator's only
> input is *what the engagement is* — enough to route. This is deliberate: a router that
> smuggled stale project state forward would let a downstream skill reason over something it
> never actually read. See the seam note under "What the navigator does NOT do."

## Purpose

Give an agent one place to start. Most skills assume you already know you want them; this one
assumes you do **not**, and turns "here is an engagement, what now?" into an ordered run over
the **real** skills in the library — never an invented one.

## When to use

- You were handed an engagement (an email, a vision doc, a spreadsheet of requirements, a
  request to add a feature) and do not know which `SKILL.md` to open.
- You want a tailored **start-here + ordered run**, not the whole static table.
- You want to be **walked** through the flow stage by stage, ratifying each before the next.

Do **not** use it to author anything — it routes. When you know the skill, open that skill
directly. When you want to *contribute* to the library (add a skill, pattern, or capability),
its sibling `skills/meta/author-a-skill` is the front door instead.

## Inputs

- **Engagement description** — *Required.* What this engagement is, in any form: a one-line
  ask, an email, a call note, a pasted vision, or just "I have a spreadsheet of requirements at
  `<path>`." *If absent/unreadable/empty:* HALT and ask what the engagement is (per
  `_shared/grounding.md`); never guess the engagement from a repo name or invent a journey.
  This is the **only** input the navigator needs — it routes on it, it does not reason over the
  project's content.
- **The live skill library** — *Optional (assumed present).* `skills/MAP.md`, the skill folders,
  and `capabilities/INDEX.md`. The navigator routes only to paths that resolve here; where a
  journey stage has no skill yet, it says so honestly rather than inventing one.

## Grounding (quoted)

The navigator's required input is the engagement description — *what the runner wants*. It does
not read project requirements, so it never fabricates one; the rule below still governs its one
required input (it asks what the engagement is rather than assuming it) and is the rule **every
stage it routes to** re-applies to its own inputs.

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

## The journey (mapped onto skills that ACTUALLY exist)

The library's usual delivery order, with the **real** skill each stage routes to. Where a stage
has **no skill yet**, that is stated plainly — the navigator names the honest gap, it never
invents a skill to fill it.

| Stage | What it does | Routes to (real path) |
|---|---|---|
| **ingest** | lift a structured-but-messy source into traceable requirement markdown | `skills/ingest/ingest-source-to-requirements` (+ `stage-and-fingerprint`, `reingest-delta`) |
| **understand** | structure a raw ask into outcomes, requirements, NFR coverage | `skills/understand/decompose-intake-to-outcomes`, `classify-requirements`, `nfr-coverage-check` |
| **challenge** | adversarially pressure-test the requirement set | `skills/challenge/red-team-requirements`, `surface-risks-and-assumptions`, `enumerate-roadblocks`, `necessity-check` |
| **derive-capabilities** | tag each requirement with the capability it fulfils | `skills/understand/derive-capabilities` **if present** — else degrade (see rule below) |
| **recommend-component-patterns** | match needs to proven library patterns, or honestly none | `skills/architect/recommend-component-patterns` + `capabilities/INDEX.md` |
| **architect** | choose a shape and author the design | `skills/architect/surface-solution-options`, `synthesise-solution-architecture`, `validate-solution-vs-requirements`, `surface-open-decisions`, … |
| **panel** | multi-voice deliberation and recorded dissent | `skills/panel/convene-a-panel`, `synthesise-panel`, `red-team-and-dissent`, `design-review-findings` |
| **deliver** | plan the lifecycle and hand off the build | `skills/deliver/describe-phases-releases-waves`, `help-implement-a-wave`, `scaffold-then-handoff`, `testing-brief-scaffold`, … |

**Degrade rule for derive-capabilities (verify on disk before you route — do not assume either
way).** Check whether `skills/understand/derive-capabilities/SKILL.md` exists on disk *at the
moment you route*:

- **If it exists** — route the capability step to it (it emits the `fulfils_capability: CAP-…`
  tag per requirement), then on to `recommend-component-patterns`.
- **If it does NOT exist** — **degrade the stage honestly**: say "derive-capabilities is not yet
  a skill," and route the runner straight to `skills/architect/recommend-component-patterns` plus
  the need-first lookup `capabilities/INDEX.md`. Do **not** invent a derive-capabilities path;
  name the gap and route around it.

The check is the durable part — this skill never hardcodes "present" or "absent," because the
library grows; it reads disk and routes to what is actually there.

A **prototype-markdown** step (turn an accepted shape into a throwaway prototype) is likewise
**not yet a skill** — if the runner asks for it, say so plainly and route them to the nearest
real neighbour (`scaffold-then-handoff` for a build hand-off brief), never a fabricated path.

## The method

### STEP 0 — confirm there is an engagement to route (deterministic, pre-model)

Check the one required input: is there an **engagement description**? If it is absent,
unreadable, or empty — **emit the clean halt and stop.** Do not guess the engagement from a
directory name, and do not assume a journey. This is mechanical, before any routing.

```markdown
HALT — I don't know what this engagement is yet, and I won't guess one.

I'm the navigator: I route you to the right skill and walk you through the flow. To do that I
need to know what you're working on. Tell me in any form and I'll take it from there:
  • a one-line ask, an email, or a call note
  • a vision / intake doc (a path or pasted)
  • "I have a spreadsheet / GitHub Project / docs folder of requirements at <where>"
  • or just the goal in a sentence

What's the engagement? (Once you tell me, I'll point you at the best first skill — nothing is
assumed until then.)
```

### STEP 1 — read the engagement and route (a menu, never a ranking)

With an engagement in hand, read it against `skills/MAP.md` and each candidate skill's
`description` / `when_to_use` / `aliases`. Return a **menu**:

- a single `Start here →` line (the best next move for *this* engagement);
- a numbered **ordered run** of the stages that usually help, each with one reason, ordered
  only as "this usually helps before that" — **never** a ranking of importance and **never**
  marked best-first;
- a `Probably skip` block for stages the engagement makes irrelevant (with the reason);
- one `Open question` line if anything about the engagement is genuinely ambiguous.

Routing cues (map the engagement onto the real front doors):

- requirements already live in a **spreadsheet / board / docs folder / export** →
  `skills/ingest/ingest-source-to-requirements`.
- a **raw vision / intake** as free text → `skills/understand/decompose-intake-to-outcomes`.
- requirements **already structured**, ready to stress-test → `skills/challenge/red-team-requirements`.
- knows the **need** but not the technology → `capabilities/INDEX.md`, then
  `skills/architect/recommend-component-patterns`.
- a **design to battle-test** → `skills/panel/convene-a-panel`.
- **planning the build** → `skills/deliver/describe-phases-releases-waves`.
- wants to **add to the library** (a skill / pattern / capability) → route to the sibling
  `skills/meta/author-a-skill`.

Close the menu with: *This is a proposal of where to start, not a plan of record — re-run the
navigator any time the picture changes.*

### STEP 2 — walk the engagement one stage at a time

After the runner picks a stage, hand off to its skill and let that skill run on **its own
grounding** (it re-reads the real project files and halts itself if its input is missing — the
navigator passes no project content forward). When the stage's skill returns, ask a `question`:

> *Has a human ratified this stage (merged its PR / accepted its outcome)? Re-run this stage,
> or advance to the next?*

- **Re-run** — loop on the same stage (the runner edits inputs and runs the skill again).
- **Advance** — move to the next stage in the journey and route to its skill (applying the
  derive-capabilities degrade rule when you reach that stage).

The navigator **never decides the human is satisfied** — that is a JUDGMENT the human owns. It
asks; the human's answer is what advances the walk. The loop is the library's existing
`propose → ratify` rhythm (`_shared/propose-ratify.md`): the agent proposes via the stage skill,
the human ratifies by merging the PR, and only then does the navigator offer to advance.

### STEP 3 — re-enter freely

The journey is a **map, not a track**. A panel can re-open outcomes; a new release can re-enter
the whole front half. At any point the runner can ask the navigator to re-route from scratch —
it re-reads the (possibly changed) engagement and returns a fresh menu. It loops at a stage
until the human advances, and it lets the human jump backwards whenever the picture changes.

## Output format

Exactly one of three kinds, every time:

- a **`halt`** — STEP 0, when there is no engagement to route (the clean shape above);
- a **`menu`** — STEP 1, the tailored start-here + ordered run + probably-skip + open question;
- a **`question`** — STEP 2, the ratified-this-stage? / re-run-or-advance? prompt between stages.

Never a `proposal`: the navigator produces no project content. Never a ranking, a verdict, a
score, or a "best" choice — the menu is an equal, un-ranked set of "this usually helps before
that," and *do nothing / stop here* is always a legitimate option.

## What the navigator does NOT do

- **It does not author project content.** No requirements, no design, no findings, no plan. It
  routes to the skill that does.
- **It does not decide satisfaction.** It asks whether the human ratified a stage; it never
  rules a stage "done" or a design "good."
- **It does not rank or score skills.** The ordered run is "usually helps before," not a
  ranking of importance.
- **It does not invent a skill.** Where a journey stage has no skill (`derive-capabilities`, a
  prototype-markdown step), it names the gap and routes to the nearest real neighbour.
- **It does not carry grounding forward.** It holds no project state between stages. The
  **key-scheme seam** — e.g. `decompose-intake-to-outcomes` emits `BO-*`/`TR-*` while a later
  skill expects its own keys — is reconciled by each skill reading the target file's scheme per
  `_shared/req-key-conventions.md` ("read the key scheme from the target file; never assume
  one"), **not** by the navigator normalising anything. The navigator never touches a key.
- **It does not replace the static index.** `skills/MAP.md` and `GETTING-STARTED.md` remain the
  single source of truth; the navigator is their engagement-aware reader. Deleting the navigator
  loses no information — the tables still route by hand.

## Notes / contract compliance

- **Altitude.** This is a meta-skill (a skill *about using* the library), not a project
  artefact. It produces nothing to ratify — it shapes where the runner goes next.
- **Deterministic base.** With no model, fall back to the GETTING-STARTED persona table and the
  MAP category table: match the engagement to a row by hand and open that skill. The model step
  only tailors the order to the specific engagement.
- **Output discipline.** `menu | question | halt` only — the closed kinds from
  `_shared/target-rule.md`. A halt here is a `question` (what is the engagement?), never a
  verdict on it.
- **Provider-agnostic.** Reading descriptions and ordering stages needs only a markdown-reading
  agent; the routing graph is the on-disk `neighbours:` edges plus `MAP.md`, no tool assumed.
