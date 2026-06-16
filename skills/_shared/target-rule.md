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
`[proposal, question, menu, halt]`); the quoted block is the shared *prose* every skill shares.

## Pointers

- The full rationale — why four-kinds is safe without enforcement, the forbidden-output
  catalogue with ❌ examples, the frontmatter contract — lives in
  `skills/_contract/target-rule-output-kinds/SKILL.md`. That file explains; this is the
  byte-stable quotable.
- The lint for `output_kinds:` and forbidden-output tells — `skills/_scripts/lint_skill_target_rule.py`.
- Pinned to this file by `check-shared-stub-drift` (advisory CI).
