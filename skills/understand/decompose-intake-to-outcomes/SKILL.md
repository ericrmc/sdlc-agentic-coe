---
name: decompose-intake-to-outcomes
description: From free-text business intake derive 3-6 business outcomes (benefits not mechanisms), each with 1-3 derived F/NF requirements, Given/When/Then acceptance criteria, and a derives_from trace. Use when a new project's intake / vision text needs structuring into outcomes and requirements.
one_liner: Turn raw intake text into traceable outcomes and requirements.
aliases: [requirements gathering, requirements elicitation, business analysis, break down a vision, scope a project, write user stories from a brief, structure an intake doc, derive requirements]
when_to_use: a new project's intake / vision text needs structuring into outcomes and requirements
output_kinds: [proposal, question, halt]
deterministic_fallback: an empty outcomes->requirements skeleton with the quality-bar checklist
suggested_tier: frontier
neighbours:
  before: (none — this is the entry point for a new project)
  after: understand/classify-requirements
---

# decompose-intake-to-outcomes

Read a project's free-text business intake (vision, business case, context) and decompose it into the value the business wants — and only then the requirements that value implies.

## Purpose

Structure intake into **outcomes -> derived requirements** under one discipline:

**Accept HIGH, derive LOW.**

- The **business** speaks in *outcomes* — benefit and capability statements a
  human stakeholder can read and ratify. These sit HIGH. A human accepts them.
- *Technical requirements* are derived beneath each outcome. These sit LOW. They
  are proposals an analyst or agent auto-applies, and a human can edit or reject
  — but they never float free of an outcome.

The payoff: every requirement is traceable to a business benefit *by
construction*. There are no orphan requirements, because a requirement that
derives from nothing was never created. When scope is questioned six months
later, every line of work points back up the tree to "why the business wanted
it."

This skill produces **markdown a human ratifies by merging a PR**. The output is
a *proposal* — advisory by design. Every output of this skill is one of four
kinds: a **proposal**, a **question**, a **menu**, or a **halt**. On the happy
path it emits a **proposal**; when its one Required input (the intake text) is
absent it emits a **halt** that asks where the intake is (STEP 0); when only an
Optional input is missing it proceeds and notes the gap as a **question**. It
never invents intake it was not given.

## When to use

- A new project arrives as free text: a vision statement, a business case, a
  paragraph of context, a transcript of a stakeholder conversation.
- That text needs structuring into outcomes and requirements before any
  technical assessment, red-teaming, or component selection can begin.

If the project already has ratified outcomes, the downstream assessment skills
apply instead.

## Inputs

The user supplies, as markdown or plain text. Each row is marked **Required** or
**Optional**; a Required input that is absent/unreadable/empty HALTs (see
[Grounding (quoted)](#grounding-quoted) and STEP 0).

| Input | Required? | What it is |
|---|---|---|
| **Intake / vision text** | **Required.** **If absent/unreadable/empty: HALT and ask where it is** (per `_shared/grounding.md`); never invent intake, outcomes, or requirements. Readable forms: a markdown/text file, an xlsx/csv path, a GitHub Project owner+number, a docs folder, or a pasted block. | The free-text description of what the business wants. The raw material — the one thing this skill cannot run without. |
| **Project title** | *Optional.* If absent: derive one from the first sentence (or first ~60 chars) of the intake; never invent an unrelated name. | A short label. |
| **Business case** | *Optional.* If absent: proceed and note the gap as a `question`; never invent a driver. | Why this is worth doing — the value or driver. |
| **Context / constraints** | *Optional.* If absent: proceed; never pad with invented limits. | Light-touch grounding: known limits, environment, stakeholders. **Not** solution detail. |

Stay grounded in what is supplied. **Do not invent scope the text does not
imply.** If the intake is thin, produce fewer outcomes — do not pad. This skill
names its required input and grounds every outcome and requirement in supplied
text; it follows the no-fabrication contract
`skills/_contract/grounding-no-absent-input`. The "do not invent scope" /
"grounded-in-intake" rules throughout this skill are an instance of that
contract, not a separate rule.

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

Two output flavours, one quality bar.

### STEP 0 — locate the intake (deterministic, pre-model; the halt path)

Before choosing a flavour, confirm the one Required input — the **intake / vision text** — is
present. This is a file-level fact computed *before* the model reasons:

- **absent** — no intake/vision text, file, or paste was supplied;
- **unreadable** — it was supplied but cannot be parsed/opened in a usable form;
- **empty** — it opens but contains no usable description.

Any of those three → emit the clean HALT below and **stop**. Do not decompose a hypothetical
project, do not infer scope from a bare project name, and do not return an empty skeleton as if
the intake had been read (the empty skeleton in [Deterministic fallback](#deterministic-fallback)
is for the *no-model* case, **not** the *no-intake* case). Copy the exemplar shape from
`skills/_contract/grounding-no-absent-input`:

```markdown
HALT — required input missing.

I can't decompose a project into outcomes without the intake it describes, and I won't invent
one. Tell me where the vision / business intake lives and I'll structure it from there.

I can read any of these:
  • a markdown / text file of intake or vision
  • an xlsx / csv file path
  • a GitHub Project (owner + project number)
  • a docs folder
  • the intake pasted directly into the chat

Which one, and where? (No outcome or requirement is created until you point me at the intake.)
```

This halt is a `question`, never a verdict: it names the missing input and the readable
formats, and stops — no "this looks too thin to be worth doing," no assumed scope. The Optional
inputs (title, business case, context) never halt: an absent Optional input proceeds honestly
(derive a title, note the gap as a `question`), per the grounding rule above. With the intake
present, proceed to Step 1.

### Step 1 — Choose a flavour

Pick based on the input richness:

- **A. Flat propose set** — a single well-spanned list of 8-15 atomic,
  testable requirements, each marked F or NF, each with a one-line rationale
  tied to the intake. Use this when the intake is small, exploratory, or when a
  delivery lead just wants a requirement list to triage.

- **B. Outcome -> derived weave** *(preferred)* — the full tree: 3-6 business
  outcomes, each with 1-3 derived requirements and acceptance criteria, with
  trace edges. Use this whenever the intake describes business *value* (almost
  always). The rest of this skill assumes it.

When in doubt, **weave**. The flat set is a degenerate weave with one implicit
outcome, and you lose the traceability that makes the rest of the method work.

### Step 2 (DETERMINISTIC BASE) — render the skeleton with trace edges

Before any model reasoning, lay down the deterministic structure. It is
mechanical, repeatable, and is exactly what you fall back to if no model is
available. Render the markdown skeleton:

- One `## Outcome BO-N — <Short Label>` heading per outcome slot.
- Under each, one `### REQ-N` block per derived requirement slot.
- Each derived block carries an explicit **`derives_from: BO-N`** citation —
  this is the trace edge, written as data, not prose. The outcome tie lives in
  this field, never in the key.
- Functional requirements carry an empty Given/When/Then acceptance block to be
  filled.

Key conventions — keep them stable, downstream skills read these keys:

- Outcome keys: **`BO-1`, `BO-2`, ...** (business outcome).
- Derived requirement keys: **`REQ-<n>`**, a flat counter, e.g. `REQ-1`,
  `REQ-2`, `REQ-3`. The key carries no parent segment; **the tie to its outcome
  lives entirely in the `derives_from` field.**
- `derives_from` on every requirement names exactly one `BO-N`. **No
  requirement is rendered without a parent.** This is the no-orphan invariant,
  enforced structurally: the skeleton has nowhere to put a parentless
  requirement.
- **F/NF is classify metadata, not part of the key.** Annotate each requirement
  as functional or non-functional with a `(F)` / `(NF)` tag for legibility, but
  the key stays a bare `REQ-<n>`.

The empty skeleton (no model, deterministic fallback) is shown in
[Output format](#output-format) and is what you emit when you cannot reason —
plus the quality-bar checklist from `references/quality-bar.md`.

### Step 3 (MODEL REASONING STEP) — run the decomposition prompt

Now fill the skeleton by reasoning over the intake. This is the one step that
requires a model. Use this prompt verbatim:

> Read a project's free-text intake and decompose it into business **OUTCOMES**
> (what value the business wants — the statements a human ratifies) and the
> **DERIVED** technical requirements each outcome implies (the rows an analyst
> auto-applies beneath it).
>
> **Rules:**
> - Produce **3 to 6** business outcomes. Each outcome is a benefit/capability
>   statement, **NOT a solution** — *"technicians can complete jobs with no
>   connectivity"*, never *"use a Postgres cache"*.
> - Under each outcome, derive **1 to 3** technical requirements. Classify each
>   `req_type` **F** (functional) or **NF** (non-functional) — this is metadata,
>   annotated as a `(F)` / `(NF)` tag, never embedded in the key. Give strong
>   functional requirements a **Given / When / Then** acceptance criterion.
> - Stay **grounded in the intake**. Do not invent scope the text does not
>   imply.
> - Each outcome carries a short (<= 4 word) display label.
> - Every derived requirement names its parent outcome via `derives_from:
>   BO-N`. There are no orphans. The requirement key is a flat `REQ-<n>`; the
>   outcome tie lives only in `derives_from`.
> - Functional requirements are phrased in imperative **shall** form ("The
>   system shall ..."). Non-functional requirements name a quality (security,
>   performance, availability, auditability, usability, compliance) with a
>   measurable target where the intake warrants one.
> - For each requirement give a short rationale tied to the intake, so a
>   delivery lead can accept, edit, or reject the *exact* scope implied.
>
> Return the filled markdown skeleton — outcomes, derived requirements with
> `(F)` / `(NF)` classify tags, `derives_from` trace edges, Given/When/Then
> acceptance, and rationales. No prose outside the structure.

### Step 4 — Self-check against the quality bar

Before handing back, walk every requirement through the quality bar
(`references/quality-bar.md`). The five tests:

1. **Atomic** — one capability or constraint per requirement, never a bundle.
2. **Verifiable** — phrased so a tester can confirm it is met.
3. **No-HOW** — states WHAT, not HOW. **No technology, framework, or
   implementation choice.** This is the most-violated test; be ruthless.
4. **Grounded-in-intake** — traceable to something the text actually says.
5. **No-orphan-by-construction** — every requirement has a `derives_from`
   parent that is one of your emitted outcomes.

Strike or rewrite anything that fails. Fewer strong requirements beat more weak
ones.

### Step 5 — Hand off as a PR for ratification

Write the markdown into the project's repo (e.g.
`outcomes/woven-outcomes.md`) and open a pull request. **The human ratifies by
reviewing and merging the PR — a PR merge is the only ratify step.** Accepting
an outcome = approving its line in the diff. Rejecting an outcome = striking it
(and, by the trace, its derived subtree) before merge. The PR *is* the
ratification, and the merge *is* the acceptance. Light and advisory.

## Output format

The user gets back one markdown file shaped like this. The
[deterministic fallback](#deterministic-fallback) is this same shape with the
slots left empty.

```markdown
# Woven outcomes — <Project Title>

> Each outcome is a business benefit a stakeholder ratifies; each requirement
> derives from exactly one outcome. Ratify by merging this PR.

## Outcome BO-1 — Offline Job Completion

**Outcome:** Field technicians can complete assigned jobs with no network
connectivity and have their work reconcile automatically once back online.
**Why:** The intake states technicians "routinely work in basements and rural
sites with no signal" and "lose an hour re-keying jobs on return."

### REQ-1  (F)
- **derives_from:** BO-1
- **The system shall** allow a technician to view, update, and mark complete any
  job assigned to them while the device has no network connectivity.
- **Acceptance:** GIVEN a technician with assigned jobs and no connectivity,
  WHEN they mark a job complete, THEN the completion is recorded locally and
  surfaced in their job list without error.
- **Rationale:** Directly serves the offline-completion outcome; the intake's
  core complaint.

### REQ-2  (F)
- **derives_from:** BO-1
- **The system shall** reconcile locally-recorded job changes to the system of
  record automatically when connectivity is restored, without technician action.
- **Acceptance:** GIVEN locally-recorded changes and restored connectivity,
  WHEN connectivity returns, THEN all pending changes are reconciled and any
  conflict is reported to the technician.
- **Rationale:** "Reconcile automatically" is the second half of the outcome;
  removes the re-keying hour the intake calls out.

### REQ-3  (NF)
- **derives_from:** BO-1
- **Constraint:** Locally-held job data must remain available for the full
  duration of a technician's shift (target: >= 12 hours) without connectivity.
- **Rationale:** Bounds "offline" to a verifiable target grounded in shift
  length implied by the intake.

## Outcome BO-2 — Auditable Completion Trail
...
```

Notice: no `Dockerfile`, no "Postgres", no "use a service worker" — only WHAT.
The HOW is the next project's problem, guided by the component-pattern skills.

### Deterministic fallback

If no model is available, emit the empty skeleton plus the quality-bar
checklist, and stop. This is a legitimate, useful output — it gives the analyst
the structure to fill by hand:

```markdown
# Woven outcomes — <Project Title>  (skeleton — fill by hand)

## Outcome BO-1 — <Short Label, <= 4 words>
**Outcome:** <benefit/capability statement — NOT a solution>
**Why:** <grounding quote/paraphrase from intake>

### REQ-1  (F | NF)
- **derives_from:** BO-1
- <The system shall ... | Constraint: ...>
- **Acceptance:** GIVEN ... WHEN ... THEN ...   (functional only)
- **Rationale:** <tied to intake>

<!-- Quality bar — every requirement must pass all five:
     [ ] atomic   [ ] verifiable   [ ] no-HOW
     [ ] grounded-in-intake   [ ] no-orphan (has a derives_from) -->
```

See `references/quality-bar.md` for the full checklist and
`examples/woven-outcomes.md` for a complete worked example.

## Notes & anti-patterns

**Anti-patterns — reject these on sight:**

- **Solutioned outcomes.** "Use a Postgres cache", "deploy on a specific cloud",
  "build a React SPA." These name a HOW. An outcome is a benefit:
  *"technicians complete jobs offline."* If an outcome could appear in an
  architecture diagram, it is not an outcome.
- **Bundled requirements.** "The system shall sync data, notify the user, and
  log the event" is three requirements wearing a trenchcoat. Split them.
- **Orphan requirements.** A requirement with no `derives_from`, or one whose
  parent is not in your outcomes list. The skeleton makes this structurally
  impossible — don't defeat it by hand-editing in a parentless row.
- **Unverifiable NFRs.** "The system shall be fast / secure / reliable." Give a
  measurable target, or it is not a requirement.
- **Inventing scope.** Adding outcomes the intake never implies because they
  "seem like good practice." Stay grounded. Note gaps as questions, not as
  outcomes.
- **Padding to a count.** 3-6 outcomes is a range, not a quota. Three strong,
  grounded outcomes beat six where half are invented.

**Notes:**

- **Outcomes are accepted whole; requirements are negotiable.** A human ratifies
  the outcome (the value); the derived requirements beneath it are the analyst's
  proposal and are expected to be edited.
- **Rejecting an outcome orphans its subtree.** That is correct and intended —
  if the business doesn't want the benefit, it doesn't want the work that
  delivers it. The trace makes this one-click in a PR review: strike the outcome
  heading and every `REQ-<n>` whose `derives_from` names it falls with it.
- **This output is never a database write.** It is markdown, ratified by a
  merge. Keep it advisory.
