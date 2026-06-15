<!--
  Skill PR — review checklist.
  Selected via the URL query: ?template=skill.md
  Use this template when the PR adds or changes a SKILL.md (a portable agent skill).
  For component patterns use ?template=pattern.md instead.

  This is the HUMAN read. A separate, advisory GitHub Action
  (`validate-skill-frontmatter`) checks the *shape* mechanically and
  (`check-shared-stub-drift`) pins any quoted shared block to skills/_shared/.
  CI comments and fails its own check to prompt a fix — it never blocks the merge.
  The call is always a human's. Keep it light.
-->

## What this skill does

<!-- One or two sentences. What does it derive/structure/surface, and WHEN should someone reach for it? -->



## Skills touched

<!-- List every SKILL.md added or changed, by path. -->

- `skills/`

---

## Reviewer checklist (the human read)

> The `validate-skill-frontmatter` Action checks most of these mechanically and leaves an advisory comment.
> This list is where a human confirms the *intent* the lint can't see. Tick what you have actually read and agree with;
> leave a note next to anything you waived and why. An unchecked box is a conversation, not a block.

### The target rule — agents target the model, the record, or the blind spot, never the judgment

- [ ] **`output_kinds` are a subset of `{proposal, question, menu, halt}`** (the target rule). No fifth kind. No `status`, `verdict`, `colour`, `ranking`, `score`, `feasibility`, `disposition`, or assessment-of-a-person has crept in under a different name.
- [ ] Every example output in the body is genuinely one of those four kinds — nothing that reads like a decision a human could rubber-stamp. If an output looks like a verdict, it has targeted the *judgment*; it should hand the human a typed thing to rule on instead.
- [ ] Where the skill quotes the canonical rule, it pastes the **"Target rule (quoted)"** block from `skills/_shared/target-rule.md` verbatim, markers included.

### The deterministic spine — the LLM is enrichment, never a dependency

- [ ] **A deterministic, no-LLM fallback is named** in the `deterministic_fallback:` frontmatter field — concrete (split / regex / template / skeleton), one line, honest about depth. Not "best-effort heuristics."
- [ ] The body actually implements that fallback: a reader could delete the model step and still get a draft a reviewer would accept. The spine may be shallow; it may not be empty or a fiction.
- [ ] The spine and the model step are **separate numbered steps**, and there is a **merge step** that keeps the spine's output when the model is absent, errors, times out, returns junk, or violates the skill's vocabulary. The model path degrades; it is never fatal.
- [ ] The LLM reasoning step is still present and pulls its weight (this is a *companion* to the spine, not a replacement for it) — the skill keeps the deterministic spine **and** the real reasoning step the method needs.

### Provider-agnostic — tier hints only

- [ ] **No model ids are hard-coded.** Model selection names a **tier** (`opus` / `sonnet` / `haiku`) or defers to the caller — never a concrete id, never a vendor, anywhere in the frontmatter or body.
- [ ] The one-line model swap honours the fixed precedence (global pin → per-call override → skill default tier), so deepening the skill is editing one word, not rewriting it.

### Survives extraction — the method works without GitHub

- [ ] **Any GitHub-native step is marked optional** so the method survives extraction. A reader running this skill in a bare terminal, a plain prompt, or another LLM workflow gets a complete result; Actions / Projects / PR mechanics are a *convenience layer*, never load-bearing.
- [ ] No step *requires* a repo, a runner, or a CI secret to produce its primary artefact.

### No drift in shared stubs

- [ ] **Any quoted shared stub matches `skills/_shared/`** (the `check-shared-stub-drift` drift guard will check). Quoted copies of `target-rule`, `deterministic-fallback`, `dismissal-memory`, `trace-edge`, `frozen-8-sections`, or `propose-ratify` are byte-for-byte identical to the canonical source — markers included.
- [ ] If a shared rule genuinely needed to change, it was changed **in `skills/_shared/` first**, then re-quoted into every skill in *this same PR* — never edited in place in a quoted copy.

### Light and advisory — no enforcement gates

- [ ] The skill introduces **no enforcement gate** — no state-machine, no required approval, no version-bound blocker, no acceptance-rate metric. It proposes, questions, offers a menu, or halts; the human decides.
- [ ] Frontmatter is complete and sane: `name:` is kebab-case; `description:` is one line that says **WHEN** to use the skill (not just what it is); `output_kinds:` and `deterministic_fallback:` are both present.
- [ ] The skill reads cleanly **on its own** — Purpose, When to use, Inputs, numbered Steps, Output format with a concrete template/example, and Notes/anti-patterns. Someone who has never seen this repo could run it from this one file.

---

## Evidence / dogfood

<!--
  How do you know it works? Optional but encouraged:
  - a run against a real intake / project, with the markdown it produced
  - the no-LLM spine output (proof the fallback isn't a fiction)
  - a link to the validate-skill-frontmatter / check-shared-stub-drift check runs on this PR
-->



## Notes for the reviewer

<!-- Anything you waived, any box you left unchecked on purpose, any open question. The honest "here's what I'm unsure about" is the most useful thing in this box. -->
