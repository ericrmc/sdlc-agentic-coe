---
name: intake-feature-change
description: Add a feature to a project that already exists — a conversational front door that grounds an in-flight ask in BOTH the current accepted requirements AND real code access (a two-precondition HALT before any reasoning), classifies it into change_kind deltas, traces each delta to one accepted outcome (a null trace is the scope-creep signal), recommends an implementation grounded in real files, defaults the effort estimate to "— (ungrounded)", and optionally emits a developer-agent prompt. Never a feasibility verdict; never code-blind.
when_to_use: adding or changing a feature on an existing project that has accepted requirements and a reachable codebase
output_kinds: [proposal, question, halt]
deterministic_fallback: the change_kind verb heuristic + a grep/heading-scan of the real codebase to fix the touched-file set, with the estimate left as "— (ungrounded)"
one_liner: Ground a feature change in the real requirements and the real code, then propose how to build it.
aliases: [add a feature, feature request, change request, enhancement intake, new feature on an existing app, modify the app, in-flight change, feature delta, how should we build this]
suggested_tier: frontier
neighbours: |
  Before: deliver/describe-phases-releases-waves (the accepted delta re-enters there as one traced release item) and understand/decompose-intake-to-outcomes (run this first if the project has no accepted requirements yet).
  After: deliver/comparator-grounded-estimate (compose it to size the change), deliver/build-agent-brief-scaffold (emit the developer-agent prompt), deliver/help-implement-a-wave (when the change touches a live system and needs a governed cutover).
---

# intake-feature-change

Add a feature to a thing that **already exists**. This is the "in-flight ask"
front door — distinct from `decompose-intake-to-outcomes` (greenfield, from raw
text) and `describe-phases-releases-waves` (a whole release stream from a pasted
backlog). It takes **one feature ask** against a **live project + codebase**,
grounds it in the real requirements and the real code, and proposes how to build
it — never code-blind, never a feasibility verdict.

> **Grounding-in-real-files is this skill's reason to exist.** `describe-phases`
> can plan a delta off keys and outcome text alone. This skill goes further: it
> reads the actual code, fixes the set of touched files from disk before it
> reasons, and ties the change to the acceptance criteria it really affects. If it
> cannot read both the current requirements and the code, it has no advantage over
> `describe-phases` — so it **halts** rather than degrade to a code-blind guess.

## When to use

- A stakeholder wants to **add or change a feature** on a project that is already
  built and already has accepted requirements.
- You need the change **grounded in the real codebase** — which files it touches,
  which acceptance criteria it moves — not just sketched against keys.
- The change must **trace to an accepted outcome**, or be surfaced as scope creep.

Do **not** use this for a greenfield project with no accepted requirements yet
(run `decompose-intake-to-outcomes` first — the STEP 0 halt will say so), and do
**not** use it to plan a whole backlog at once (that is `describe-phases`).

## Inputs

Supplied as markdown / context / paths:

1. **The feature ask** — *Required.* One in-flight change, in a sentence or two
   ("add CSV export to the approvals dashboard"). If absent/unreadable/empty:
   HALT and ask what the change is (per `_shared/grounding.md`); never invent a
   feature to intake. Readable forms: a pasted block, a markdown file, or a
   GitHub Project owner+number.
2. **The current accepted requirements** — *Required.* The project's accepted
   outcomes + requirements, each with a stable key of whatever scheme the file
   uses (`BO-`/`REQ-`/`OUT-`/`F-`… — **read the scheme from the file, never assume
   one**, per `_shared/req-key-conventions.md`). These are the only things a delta
   may trace to. If absent/unreadable/empty (the file is missing, or has zero keys
   of any recognised scheme): HALT and ask where they live, naming
   `decompose-intake-to-outcomes` as the skill that produces them (per
   `_shared/grounding.md`); never invent an outcome, a key, or a requirement.
   Readable forms: a markdown file, an xlsx/csv path, a GitHub Project
   owner+number, a docs folder, or a pasted block.
3. **Code access** — *Required.* A reachable path to the project's repository /
   working tree on disk (or a checked-out clone). This is what makes the
   recommendation grounded rather than code-blind. If absent/unreadable (no path
   supplied, or the path does not exist / cannot be read): HALT and ask for the
   repo path (per `_shared/grounding.md`); never invent a file, a module, or a
   call site. A description of the code is **not** code access — the skill reads
   files, it does not take the human's word for what they contain.
4. **Acceptance criteria per requirement** — *Optional.* Improves the trace and
   the impact read. If absent: proceed and surface affected-AC gaps as a
   `question`; never invent a criterion.
5. **A comparators dataset** — *Optional.* Confirmed past projects with known
   actual effort, for sizing (see `comparator-grounded-estimate`). If absent:
   the estimate column stays **`— (ungrounded)`** and the gap is surfaced — never
   a fabricated number.

> **Two of the Required inputs are the whole point — and BOTH are checked before
> any reasoning.** The current requirements AND code access are a *two-precondition*
> halt (STEP 0). Either one absent is an honest halt, because the skill's value is
> grounding an implementation in real files; degrading to a code-blind guess would
> make it a worse `describe-phases`, not a better one.

This skill reads a requirement, an acceptance criterion, and a real codebase, so
it follows the GROUNDING contract — an absent **Required** input HALTs and asks;
it is never invented or silently proceeded over. See
`skills/_contract/grounding-no-absent-input`.

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

## The method (numbered STEPS)

The method has a **deterministic base** (STEP 0 presence check, STEP 1 verb
heuristic, STEP 2 grep/heading-scan that fixes the touched-file set) and **model
reasoning** (STEP 3 trace, STEP 4 implementation proposal). The base is runnable
with no model and never invents files or keys.

### STEP 0 — the two-precondition HALT (DETERMINISTIC, pre-model)

Before any reasoning, confirm **both** load-bearing Required inputs are present as
a file-level fact — the **current accepted requirements** AND **code access** —
*computed before the model runs*. This is mechanical, never a model judgement on
"is this enough to plan with":

- **requirements absent** — the file is missing/unreadable, OR it contains zero
  keys of any recognised scheme (`BO-`/`REQ-`/`OUT-`/`F-`/`CAP-`/… per
  `_shared/req-key-conventions.md`). A valid `BO-*` project must NOT halt — the
  check is *zero keys of any scheme*, not "no `O-*` keys";
- **code access absent** — no repo path was supplied, OR the path does not exist /
  cannot be read on disk. A prose *description* of the code does not satisfy this.

Either one absent → emit the clean halt below and **stop**, naming the exact next
skill or missing input. Do **not** proceed on the half you have, and do **not**
degrade to a code-blind guess.

```markdown
HALT — required input missing.

I can't ground a feature change without BOTH the current accepted requirements AND
real code access, and I won't guess at either. I'm missing: <the accepted
requirements | code access (a repo path) | both>.

- If the accepted requirements are missing, point me at them — or, if this project
  has none yet, it isn't a feature *change*: run `decompose-intake-to-outcomes` to
  establish outcomes first, then come back.
- If code access is missing, give me a reachable repo path — a description of the
  code is not code access; I read the files, I don't take it on faith.

I can read requirements from any of these:
  • a markdown file path
  • an xlsx / csv file path
  • a GitHub Project (owner + project number)
  • a docs folder (markdown / text)
  • the rows pasted directly into the chat

Which one, and where is the repo? (Nothing is intaken until I can read both — I
will not propose an implementation blind to the real code.)
```

The halt names the missing input and stops; it carries no delta, no touched file,
no estimate, and no feasibility call. With both present, proceed to STEP 1.

### STEP 1 — classify the ask into `change_kind` deltas (DETERMINISTIC)

Split the ask into one or more deltas and assign each exactly one `change_kind`
using the verb heuristic — `remove > patch > change > add`, first match wins,
unqualified defaults to `add`. **Cite, never re-author** the taxonomy: see
[`references/change-kinds.md`](references/change-kinds.md), a pointer to the
canonical definitions owned by `describe-phases-releases-waves`. Classify by
**intent**, not wording ("improve the export" is a `change`, not an `add`).

### STEP 2 — fix the touched-file set from the real code (DETERMINISTIC floor, model deepens)

Read-only pass over the codebase. Run a **deterministic grep / heading-scan /
set-overlap floor** (the `reconcile-as-built` primitive — portable, no tool
lock-in, no hallucination) to **fix the legal set of touched files before the
model reasons** — the exact retrieve-don't-generate move `recommend-component-patterns`
uses for pattern keys: the set of candidate files is drawn from disk, and the
model only *deepens* it, never invents it. **Every file named must exist on disk.**

- Grep the ask's nouns/verbs and the requirement text against the tree; collect
  the files, headings, and symbols that actually match.
- Optionally fan out per area with `explore-one-area-at-a-time` +
  `parallel-agents` for a large tree — one area per agent, read-only.
- The model may add a file only if it can point at the on-disk evidence (an
  import edge, a call site) for it. A file with no on-disk anchor is dropped, not
  guessed.

This pass is **read-only, always.** It opens no write, runs no migration, touches
no live system.

### STEP 3 — trace each delta to ONE accepted outcome (MODEL; the null is the signal)

For each delta, set `derives_from` to the key of the **one** accepted outcome it
genuinely serves — copied **exactly** from the supplied requirements, in the
file's own scheme (reuse `describe-phases` STEP 5). The rules:

- Use the outcome the change *serves*, not one it merely mentions. Copy the key
  exactly; never invent a key; never force a weak match.
- **A `null` trace is the deliberate scope-creep signal, surfaced as a `question`
  — never a forced weak match.** The null is not a failure: it says, in writing,
  *"this change has no accepted outcome behind it; trace it or drop it."* Ask the
  human which outcome it serves, or whether this is genuinely new scope that needs
  an outcome accepted first.

### STEP 4 — recommend an implementation as a PROPOSAL (MODEL; never a verdict)

Compose the recommendation from the real files (STEP 2) and the affected
acceptance criteria. It is a **proposal** a human ratifies — it issues no status,
no score, and no feasibility call. Where a roadblock exists, **enumerate and cite
the roadblocks** the change hits (reuse `enumerate-roadblocks`) and hand the call
to the human. A feasibility disposition is forbidden here; ruling the change in or
out is a JUDGMENT the human owns (per `_contract/target-rule-output-kinds`).
State, per delta:

- the `change_kind` and its one traced outcome (or the null + its question);
- the real files/areas it touches (from STEP 2, every one on disk);
- the acceptance criteria it affects (or a `question` where AC is absent);
- a one-line implementation sketch grounded in those files — *how*, not *whether*.

### STEP 5 — size the change (COMPOSE `comparator-grounded-estimate`)

Compose `comparator-grounded-estimate` to size each delta. **That skill ships
unwired** — documentation-only until a real effort-actual comparators table
exists. So the estimate column **defaults to `— (ungrounded)`**, and a real
number appears **only when a comparators dataset is wired**. Never show a
fabricated `4–8d (med)`-style number as the default; an ungrounded placeholder is
the honest output, and the absence of the dataset is surfaced, not papered over.

### STEP 6 — (OPTIONAL) emit a developer-agent prompt (DELEGATE to `build-agent-brief-scaffold`)

When the human wants to hand the build off, delegate to
`build-agent-brief-scaffold`, passing this skill's analysis: the traced delta +
`derives_from` + the real impacted files + the affected acceptance criteria + the
discipline boundary (read-only analysis ends here; the developer agent builds).
Returned code re-enters as **references** (a PR link / a commit), never stored.

## Output format

Return a single markdown proposal. Concrete template:

```markdown
## Feature change intake — <the ask, in one line>

> Grounded in the current accepted requirements and the real codebase
> (`<repo path>`). A proposal a human ratifies — no feasibility call, no status.

### Open questions (read first)
- `<delta>` has no accepted outcome behind it — trace it or confirm it is new scope.
- _(or)_ None flagged. Confirm the deltas + traces below.

### Proposed deltas

| change_kind | delta | traces to | touches (real files) | affects AC | estimate |
|-------------|-------|-----------|----------------------|------------|----------|
| add    | CSV export on the approvals dashboard | BO-2 | `app/dashboard/export.py`, `app/routes.py` | AC-2.1 | — (ungrounded) |
| change | widen the audit retention to 7y       | BO-4 | `app/audit/retention.py`                    | AC-4.3 | — (ungrounded) |
| patch  | fix timezone drift in audit timestamps | _null — scope creep_ | `app/audit/ts.py` | — | — (ungrounded) |

> The `patch` line traces to **null** — that is the deliberate scope-creep flag,
> surfaced as the open question above: trace it to an outcome or drop it.
> Estimates are `— (ungrounded)` because no comparators dataset is wired; seed and
> confirm one (`comparator-grounded-estimate`) to ground a number.

### Implementation sketch (per delta, grounded in real files)
- **CSV export (add → BO-2):** add an `export_csv` handler in
  `app/dashboard/export.py`, route it in `app/routes.py`; affects AC-2.1
  (self-serve evidence). How, not whether — a human owns the go/no-go.

### Roadblocks the change hits (enumerated + cited, not adjudicated)
- The 7y retention delta hits the storage-cost cap noted in `app/audit/retention.py`
  — enumerated for the human to weigh; the call is theirs.
- _(or)_ None surfaced.

### Hand off to build? (optional)
Run `build-agent-brief-scaffold` with this analysis to get a paste-ready
developer-agent prompt. Returned code re-enters as a PR/commit reference.
```

## Notes / anti-patterns

- **Never code-blind.** The two-precondition halt is the core of this skill. No
  current requirements OR no code access → halt and ask. Degrading to a guess off
  the requirements alone makes this a worse `describe-phases`, not a better one.
  (This is this skill's instance of the library GROUNDING rule —
  `skills/_contract/grounding-no-absent-input`.)
- **Read the key scheme from the file; never assume one.** A valid `BO-*` project
  must not spuriously halt on "no `O-*` keys." The presence check is *zero keys of
  any recognised scheme*, per `_shared/req-key-conventions.md`.
- **Fix the file set before reasoning.** STEP 2 draws the touched files from disk;
  the model deepens, never invents. Every file named exists on disk — the same
  retrieve-don't-generate discipline `recommend-component-patterns` uses for keys.
- **Read-only always.** This skill plans a change; it never makes one. It opens no
  write, runs no migration, touches no live system. When the change needs a
  governed cutover, hand off to `help-implement-a-wave`.
- **The null trace is a feature.** A delta with no accepted outcome is surfaced as
  a `question`, never force-matched. Suppressing the null hides scope creep.
- **Propose, never dispose.** STEP 4 recommends an implementation — *how*. It
  issues no status, no score, and no feasibility call; it enumerates and cites the
  roadblocks and hands the go/no-go to the human (per
  `_contract/target-rule-output-kinds`).
- **The estimate defaults to ungrounded.** `— (ungrounded)` is the honest default;
  a real number appears only when a comparators dataset is wired. A made-up
  person-day figure is the exact failure `comparator-grounded-estimate` exists to
  prevent.
- **Light and advisory.** The intake is a proposal a human ratifies and re-enters
  as one traced release item in `describe-phases-releases-waves`. It blocks
  nothing.

## References

- [`references/change-kinds.md`](references/change-kinds.md) — a pointer to the
  canonical `change_kind` taxonomy (owned by `describe-phases-releases-waves`);
  this skill cites it, never re-authors it.
