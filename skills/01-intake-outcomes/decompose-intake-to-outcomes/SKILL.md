---
name: decompose-intake-to-outcomes
description: The front door — from free-text business intake derive 3-6 business outcomes (benefits not mechanisms), each with 1-3 derived F/NF requirements, Given/When/Then acceptance criteria, and a derives_from trace. Use when a new project's intake / vision text needs structuring into outcomes and requirements.
when_to_use: a new project's intake / vision text needs structuring into outcomes and requirements
output_kinds: [proposal]
deterministic_fallback: an empty outcomes->requirements skeleton with the quality-bar checklist
suggested_tier: opus
---

# decompose-intake-to-outcomes

> The front door of the method. You are the **Weaver**: you read a project's
> free-text business intake (vision, business case, context) and decompose it
> into the value the business wants — and only then the requirements that value
> implies.

## Purpose

This is FORGE stages 1-2: **intake -> outcomes -> derived requirements**. It
exists to enforce one discipline that everything downstream depends on:

**Accept HIGH, derive LOW.**

- The **business** speaks in *outcomes* — benefit and capability statements a
  human stakeholder can read and ratify. These sit HIGH. A human accepts them.
- The **method** derives *technical requirements* beneath each outcome. These
  sit LOW. They are proposals an analyst or agent auto-applies, and a human can
  edit or reject — but they never float free of an outcome.

The payoff: every requirement is traceable to a business benefit *by
construction*. There are no orphan requirements, because a requirement that
derives from nothing was never created. When scope is questioned six months
later, every line of work points back up the tree to "why the business wanted
it."

This skill produces **markdown a human ratifies by merging a PR**. It never
writes a database row, never enforces a gate, and never advances a state
machine. The output is a *proposal* — advisory by design.

## When to use

- A new project arrives as free text: a vision statement, a business case, a
  paragraph of context, a transcript of a stakeholder conversation.
- You need that text structured into outcomes and requirements before any
  technical assessment, red-teaming, or component selection can begin.

If the project already has ratified outcomes, you don't need this skill — you
need the downstream assessment skills.

## Inputs

The user supplies, as markdown or plain text:

| Input | Required | What it is |
|---|---|---|
| **Intake / vision text** | yes | The free-text description of what the business wants. The raw material. |
| **Project title** | optional | A short label. If absent, derive one from the first sentence (or first ~60 chars) of the intake. |
| **Business case** | optional | Why this is worth doing — the value or driver. |
| **Context / constraints** | optional | Light-touch grounding: known limits, environment, stakeholders. **Not** solution detail. |

Stay grounded in what is supplied. **Do not invent scope the text does not
imply.** If the intake is thin, produce fewer outcomes — do not pad.

## The method (numbered steps)

This method is carried verbatim from the original delivery workbench's two
prompts: the flat `propose_requirements` analyst and the richer `weave`
decomposer. Two flavours, one quality bar.

### Step 1 — Choose a flavour

There are two flavours of output. Pick based on the input richness:

- **A. Flat propose set** — a single well-spanned list of 8-15 atomic,
  testable requirements, each marked F or NF, each with a one-line rationale
  tied to the intake. Use this when the intake is small, exploratory, or when a
  delivery lead just wants a requirement list to triage. This is the
  `propose_requirements` behaviour.

- **B. Outcome -> derived "weave"** *(preferred)* — the full tree: 3-6 business
  outcomes, each with 1-3 derived requirements and acceptance criteria, with
  trace edges. Use this whenever the intake describes business *value* (almost
  always). This is the `weave` behaviour and the rest of this skill assumes it.

When in doubt, **weave**. The flat set is a degenerate weave with one implicit
outcome, and you lose the traceability that makes the rest of the method work.

### Step 2 (DETERMINISTIC SPINE) — render the skeleton with trace edges

Before any LLM reasoning, lay down the deterministic structure. This is the
*spine* — it is mechanical, repeatable, and is exactly what you fall back to if
no model is available. Render the markdown skeleton:

- One `## Outcome BO-N — <Short Label>` heading per outcome slot.
- Under each, one `### TR-N.M` block per derived requirement slot.
- Each derived block carries an explicit **`derives_from: BO-N`** citation —
  this is the trace edge, written as data, not prose.
- Functional requirements carry an empty Given/When/Then acceptance block to be
  filled.

Key conventions (carried from the source seams — keep them stable, downstream
skills read these keys):

- Outcome keys: **`BO-1`, `BO-2`, ...** (business outcome).
- Derived requirement keys: **`TR-<outcome#>.<n>`**, e.g. `TR-1.1`, `TR-1.2`,
  `TR-2.1`. The first number ties the requirement to its outcome; this *is* the
  trace, made legible.
- `derives_from` on every requirement names exactly one `BO-N`. **No
  requirement is rendered without a parent.** This is the no-orphan invariant,
  enforced structurally: the skeleton has nowhere to put a parentless
  requirement.

The empty skeleton (no model, deterministic fallback) is shown in
[Output format](#output-format) and is what you emit when you cannot reason —
plus the quality-bar checklist from `references/quality-bar.md`.

### Step 3 (LLM REASONING STEP) — run the weave prompt

Now fill the skeleton by reasoning over the intake. This is the one step that
requires a model. Use this prompt verbatim (it is the original Weaver,
re-targeted to emit markdown instead of JSON):

> You are the **Weaver**. You read a project's free-text intake and decompose
> it into business **OUTCOMES** (what value the business wants — the statements
> a human ratifies) and the **DERIVED** technical requirements each outcome
> implies (the rows an analyst auto-applies beneath it).
>
> **Rules:**
> - Produce **3 to 6** business outcomes. Each outcome is a benefit/capability
>   statement, **NOT a solution** — *"technicians can complete jobs with no
>   connectivity"*, never *"use a Postgres cache"*.
> - Under each outcome, derive **1 to 3** technical requirements. Mark each
>   `req_type` **F** (functional) or **NF** (non-functional). Give strong
>   functional requirements a **Given / When / Then** acceptance criterion.
> - Stay **grounded in the intake**. Do not invent scope the text does not
>   imply.
> - `value_outcome` is a short (<= 4 word) display label for the outcome.
> - Every derived requirement names its parent outcome via `derives_from:
>   BO-N`. There are no orphans.
> - Functional requirements are phrased in imperative **shall** form ("The
>   system shall ..."). Non-functional requirements name a quality (security,
>   performance, availability, auditability, usability, compliance) with a
>   measurable target where the intake warrants one.
> - For each requirement give a short rationale tied to the intake, so a
>   delivery lead can accept, edit, or reject the *exact* scope implied.
>
> Return the filled markdown skeleton — outcomes, derived requirements with F/NF
> marks, `derives_from` trace edges, Given/When/Then acceptance, and rationales.
> No prose outside the structure.

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
reviewing and merging.** Accepting an outcome = approving its line in the diff.
Rejecting an outcome = striking it (and, by the trace, its derived subtree)
before merge. There is no gate, no state machine, no disposition record — the
PR *is* the ratification, and the merge *is* the acceptance. Light and
advisory.

## Output format

The user gets back one markdown file shaped like this. The
[deterministic fallback](#deterministic-fallback) is this same shape with the
slots left empty.

```markdown
# Woven outcomes — <Project Title>

> Derived from intake by the Weaver. Each outcome is a business benefit a
> stakeholder ratifies; each requirement derives from exactly one outcome.
> Ratify by merging this PR.

## Outcome BO-1 — Offline Job Completion

**Outcome:** Field technicians can complete assigned jobs with no network
connectivity and have their work reconcile automatically once back online.
**Why:** The intake states technicians "routinely work in basements and rural
sites with no signal" and "lose an hour re-keying jobs on return."

### TR-1.1  (F)
- **derives_from:** BO-1
- **The system shall** allow a technician to view, update, and mark complete any
  job assigned to them while the device has no network connectivity.
- **Acceptance:** GIVEN a technician with assigned jobs and no connectivity,
  WHEN they mark a job complete, THEN the completion is recorded locally and
  surfaced in their job list without error.
- **Rationale:** Directly serves the offline-completion outcome; the intake's
  core complaint.

### TR-1.2  (F)
- **derives_from:** BO-1
- **The system shall** reconcile locally-recorded job changes to the system of
  record automatically when connectivity is restored, without technician action.
- **Acceptance:** GIVEN locally-recorded changes and restored connectivity,
  WHEN connectivity returns, THEN all pending changes are reconciled and any
  conflict is reported to the technician.
- **Rationale:** "Reconcile automatically" is the second half of the outcome;
  removes the re-keying hour the intake calls out.

### TR-1.3  (NF)
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

### TR-1.1  (F | NF)
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

- **Solutioned outcomes.** "Use a Postgres cache", "deploy on Databricks",
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
  heading and its `TR-N.*` block falls with it.
- **This output is never a row write.** It is markdown, ratified by a merge.
  Keep it advisory. No gate, no state machine, no governance disposition lives
  in this skill.
