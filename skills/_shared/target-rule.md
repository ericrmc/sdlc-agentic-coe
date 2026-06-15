# _shared/target-rule.md — the canonical TARGET RULE

> **This file is the single source of truth for the TARGET RULE.**
> Skills do not import it; they **quote the block below verbatim** into their own body.
> `skills/_scripts/check_shared_stub_drift.py` (run by the `check-shared-stub-drift`
> GitHub Action on every PR) diffs each skill's quoted copy against this file and
> fails the check if a single byte drifts. **Keep the canonical block byte-stable.**
> If the rule must change, change it *here first*, then re-quote into every skill in
> the same PR — never edit a quoted copy in place.

---

## The canonical block (quote this verbatim)

<!-- BEGIN target-rule (byte-stable; do not edit a quoted copy — edit _shared/target-rule.md) -->

**TARGET RULE — agents target the model, the record, or the blind spot, never the judgment.**

Every agent output is exactly one of four kinds:

- `proposal` — a derived or structured thing to accept, edit, or reject.
- `question` — a named tension and the assumption beneath it, for a human to rule on.
- `menu` — N un-ranked, equal options; "do nothing" is always one of them.
- `halt` — a stop; the agent waits for a human.

An agent output is **never** any of these (the forbidden-output list):

- a **status**
- a **verdict**
- a **colour**
- a **ranking**
- a **score**
- a **feasibility** call
- a **disposition**
- an **assessment of a person**

The three legal targets, and the one illegal one:

- **MODEL** — keep a cheap model on rails (decompose, classify, structure, trace).
- **RECORD** — structure something for defensibility and reuse (assemble, retrieve, cite).
- **BLIND SPOT** — coverage and de-biasing rituals (surface a conflict, name an adjacency, ask "which assumption gives?").
- **JUDGMENT** — the human's call: good-enough, feasible, approved, who's at fault, what colour, what ranks first. The agent **never** targets this; it hands the human a typed thing to rule on.

If an output reads like a decision someone could rubber-stamp, it has targeted the JUDGMENT. Reshape it into a `proposal`, a `question`, a `menu`, or a `halt`, and hand the call to the human.

<!-- END target-rule -->

---

## How to quote it

In any `SKILL.md` (or pattern doc) that needs the rule, paste the block between the
`BEGIN`/`END` markers above — markers included — into a section titled
**"Target rule (quoted)"**. Do not reword, reorder, re-case, or re-punctuate it; the
drift check compares bytes between the markers.

```markdown
## Target rule (quoted)

<!-- BEGIN target-rule (byte-stable; do not edit a quoted copy — edit _shared/target-rule.md) -->
...paste the canonical block exactly...
<!-- END target-rule -->
```

A skill's own frontmatter still declares its `output_kinds:` (a subset of
`[proposal, question, menu, halt]`); the quoted block is the shared *prose* every
skill shares so the discipline reads identically everywhere.

## Why a quoted copy and not an import

This is a markdown library meant to run in **any** LLM workflow that can read a file —
Claude Code, a plain prompt, a CI step. There is no import mechanism to rely on at
read time, and a skill that references a rule it does not contain ships broken when
copied alone. So each skill carries the rule **in its own bytes**, and the drift check
keeps the copies honest without a runtime dependency. The trade is deliberate:
redundancy on disk, zero coupling at use time, one canonical source for edits.

## Relationship to the rest of the library

- The **full rationale** — why the four-kinds rule is *safe* without enforcement, the
  forbidden-output catalogue with concrete ❌ examples, and the frontmatter contract —
  lives in `skills/_contract/target-rule-output-kinds/SKILL.md`. That file *explains*;
  this file is the *byte-stable quotable*. The wording here is the subset both agree on.
- The **lint** that checks `output_kinds:` against the closed enum and greps for
  forbidden-output tells is `skills/_scripts/lint_skill_target_rule.py`
  (`validate-skill-frontmatter` Action).
- The **drift check** that pins quoted copies to this file is
  `skills/_scripts/check_shared_stub_drift.py` (`check-shared-stub-drift` Action).
- Both Actions are **advisory CI**: they comment and fail the check to prompt a human
  fix. Neither blocks a downstream project. Consistent with the library's keep-it-light
  stance — the machine catches the *shape*; a human still owns every call.
