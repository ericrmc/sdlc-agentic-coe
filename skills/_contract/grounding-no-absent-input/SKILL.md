---
name: grounding-no-absent-input
description: The no-fabrication keystone — a skill names its REQUIRED inputs; an absent/unreadable/empty required input becomes a HALT that asks where it is (offering the formats ingestion reads) and stops, never an invented hypothetical. Carries the library's canonical HALT exemplar. Use it when authoring any skill that reads or writes a requirement, or to decide whether an output should be a halt.
one_liner: An absent required input HALTs and asks where it is — never an invented hypothetical.
aliases: [no fabrication, grounding contract, halt on missing input, do not invent, ask don't assume, absent input halt, halt not empty, never hallucinate an input, where is the source, halt exemplar]
when_to_use: authoring or reviewing any skill that reads or writes a requirement; deciding whether a missing input should halt; needing the canonical shape of a halt
output_kinds: [halt, question]
deterministic_fallback: the quoted grounding block + the ✅/❌ halt exemplar pair as a checklist — name the required inputs, and if a required one is absent, copy the clean halt verbatim
suggested_tier: light
tier_reason: convention doc — input-presence is a deterministic check (file absent/unreadable/empty), no weighing and no model call in its critical path
neighbours:
  before: skills/_contract/target-rule-output-kinds (halt is one of the four legal output kinds this rule defines)
  after: skills/_contract/propose-ratify-rhythm (a human supplies the missing input the halt asked for, then the agent re-runs and proposes)
---

# grounding-no-absent-input — the no-fabrication keystone

Make the absence of a required input a **typed `halt`**, not a silent guess. This is the one
contract that stops a richly agent-driven library from producing a clean-looking proposal
grounded in nothing — an invented requirement, a hallucinated source row, a plausible NFR no one
ever stated. Where a skill and this file disagree, this file wins; open a PR against this file
rather than forking the rule.

It is **mostly deterministic.** Whether a required input is present is a file-level fact
(absent / unreadable / empty), computable before any model runs. The deterministic fallback is
this whole document: name the required inputs, check them, and if a required one is missing, copy
the clean halt below verbatim.

## Purpose

State, once and quotably, the rule every analysis and ingest skill obeys:

> **A skill names its REQUIRED inputs. If a required input is absent, unreadable, or empty, the
> skill HALTs and asks the user where it is — offering the formats ingestion can read — and stops.
> It never assumes, invents, or reasons over a hypothetical. Partial input is named, not patched.**

This is load-bearing for a second reason: **the library's halt-first skills (ingest, the author
skills, the panel skills, and more) all converge on one halt shape.** `halt` is legal per the
TARGET RULE, and a growing set of skills wire a working halt path; left unanchored, each would
phrase its halt differently and some would drift into smuggling a verdict. This file carries the
**canonical halt exemplar** — a clean halt paired with a WRONG counter-example — as the single
reference every halt copies, so every halt looks the same and none of them smuggle a verdict.

## When to use

- **Authoring any skill that reads or writes a requirement** (outcome, decision, capability,
  pattern, acceptance criterion). Mark its Inputs Required/Optional, quote the grounding block,
  and wire a halt path for the Required ones.
- **Authoring any halt-first skill** (it cannot do its job without a specific input — ingest a
  source, change a live feature, navigate a real engagement). Copy the clean halt exemplar below.
- **Reviewing a PR** that adds such a skill: check it against the exemplar — a real halt step, a
  halt that *asks and stops* and does not carry a finding.

Do not use this to introduce enforcement. A halt is an advisory output kind: it stops *this run*
and asks; the human supplies the input and re-runs. Nothing downstream is blocked.

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

## The method — wire the halt before the model reasons

### STEP 0 — name and check the required inputs (deterministic, pre-model)

List the skill's inputs and mark each **Required** or **Optional**. For each Required input,
compute presence as a file-level fact *before* any model step:

- **absent** — the path/source was never supplied, or does not exist;
- **unreadable** — it exists but cannot be parsed/opened in a form the skill can use;
- **empty** — it opens but contains zero usable rows / keys / content.

Any of those three on a Required input → emit the clean halt (below) and **stop**. All Required
inputs present → proceed. This check is mechanical; it is **never** a model judgement on "does
this look like enough to work with" (that is the verdict the rule forbids).

### STEP 1 — on a present-but-partial set, name what's missing and ask

If some Required inputs are present and others are not, do **not** run on the partial set. Emit a
halt (or a `question` when only an Optional input is missing) that **names each missing input by
role** and asks for it. Never patch the gap with an invented value to "keep going."

### STEP 2 — proceed only when grounded

With every Required input present and read, the skill runs its real method and emits its normal
`proposal` / `question` / `menu`. The halt path is the off-ramp, not the destination.

## The canonical HALT exemplar

This is the **reference shape** every halt-first skill copies. It has two halves: the clean halt
to emulate (✅) and the verdict-smuggling halt to reject (❌). The difference between them is the
entire discipline.

### ✅ Clean halt — names the missing input, offers the readable formats, stops

```markdown
HALT — required input missing.

I can't run **ingest-source-to-requirements** without the source it reads from, and I won't
invent one. Tell me where the requirements live and I'll pick up from there.

I can read any of these:
  • an xlsx / csv file path
  • a GitHub Project (owner + project number)
  • a docs folder (markdown / text)
  • the rows pasted directly into the chat

Which one, and where? (Once you point me at it, I'll read it and propose the requirements —
nothing is assumed until then.)
```

Why it is clean: it names the **one required input that is missing** (the source), it offers the
**formats ingestion can read**, and it **stops and asks** — carrying no finding, no assumption, no
disposition. There is not a single invented requirement, key, or number in it. It is a `question`
wearing the `halt` shape: *what is required, what is missing, and how to supply it.*

### ❌ WRONG — a halt that smuggles a verdict / an assumption (do NOT do this)

```markdown
HALT — I'm stopping because this looks infeasible.

There's no requirements file, but based on the project name this is clearly a CRUD app, so I'll
assume the usual: REQ-1 user login, REQ-2 a dashboard, REQ-3 an admin role, with a 99.9% uptime
NFR. Given that, the effort is about 4–8 days and the data-residency requirement is probably the
real blocker — I'd halt the project here until that's resolved.
```

Why it is WRONG — it breaks the rule on **every** count:

- **It invents the missing input.** `REQ-1`/`REQ-2`/`REQ-3`, the uptime NFR, and the residency
  requirement were never supplied. The halt fabricated the very thing it claimed it lacked.
- **It smuggles a verdict.** "looks infeasible", "the real blocker", "I'd halt the project" are
  JUDGMENTs the human owns — a feasibility disposition dressed as a halt.
- **It smuggles a number.** "about 4–8 days" is a score the skill has no grounding to emit.
- **It assumes from a name.** "clearly a CRUD app" reasons over a hypothetical instead of asking.

The fix is always the same: throw all of it away and emit the **clean halt** — name the missing
input, offer the readable formats, ask where it is, and stop. A halt that contains a finding is
not a halt; it is a verdict with an apology attached.

## How every analysis skill references this contract

Each skill that reads or writes a requirement does **three** additive things:

1. **Marks its Inputs Required / Optional**, with a one-line *if-absent* note on every Required
   row that cites this contract — e.g. *"Required. If absent/unreadable/empty: HALT and ask where
   it is (per `_shared/grounding.md`); never invent."*
2. **Quotes the grounding block** verbatim (everything between the `BEGIN grounding` and
   `END grounding` HTML-comment markers shown above) in a section titled **"Grounding (quoted)"**,
   so the rule travels in the skill's own bytes and the drift check pins it.
3. **Wires a halt path** — a real STEP 0 (locate / verify inputs) that emits the clean halt when a
   Required input is missing. Declaring `halt` in `output_kinds` without a halt step in the body is
   exactly the gap the lint warns on.

The existing no-fabrication prose in `classify-requirements`, `decompose-intake-to-outcomes`, and
`recommend-component-patterns` ("never invent a `pattern_key`… the set of legal keys is fixed
before reasoning") becomes an **instance of this contract** rather than a private restatement —
each cites this file instead of re-deriving the rule.

## Output format

Applying this contract yields, for the authoring agent:

1. **The Inputs section**, every row marked Required/Optional with an *if-absent* note on the
   Required ones.
2. **The quoted grounding block**, pasted verbatim under "Grounding (quoted)".
3. **A STEP 0 halt path**, copied from the ✅ clean halt exemplar above and adapted to the skill's
   own required inputs and readable formats.

At runtime, the skill emits one of exactly two grounding-related outputs:

- a **`halt`** (a missing Required input) — the clean shape above; or
- a **`question`** (only an Optional input is missing, and the run can honestly proceed with an
  explicit null) — naming the gap, never padding it.

## Notes / contract compliance

- **Rhythm:** human supplies the missing input → agent re-runs and proposes (opens a PR) → human
  ratifies by merging. The halt does not advance anything; it waits.
  (See `skills/_contract/propose-ratify-rhythm`.)
- **Altitude:** this is a *contract* (a rule every skill obeys), not a project artefact. It
  produces nothing to ratify; it shapes how other skills behave.
- **A halt is a `question`, never a verdict.** The TARGET RULE
  (`skills/_contract/target-rule-output-kinds`) lists `halt` as one of the four legal kinds and
  forbids a halt that carries a status, feasibility verdict, score, or disposition — exactly the
  ❌ counter-example above.
- **The lint is honest about its reach.** `skills/_scripts/lint_skill_grounding.py` checks that a
  Required-input skill **cites** this stub and that a `halt`-declaring skill **wires** a halt path.
  It does **not** and **cannot** catch a model inventing an input mid-run — that is runtime
  behaviour. The safeguard is this rule plus the exemplar; the lint catches the documentation miss
  and the halt-not-wired miss, nothing more. Claiming otherwise would be false confidence about
  the safeguard itself.
- **Provider-agnostic.** The presence check is plain file I/O; the halt is plain markdown. The
  contract holds in any agent harness, any LLM workflow that reads markdown, or for a human with no
  agent at all — because the load-bearing move is "name the inputs and stop if a required one is
  missing," which needs no model.
