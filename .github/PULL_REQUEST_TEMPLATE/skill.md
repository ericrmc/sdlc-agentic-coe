<!--
  SKILL PULL REQUEST — filled by the authoring agent, ratified by a human.
  Select with ?template=skill.md. Use when the PR adds or changes a SKILL.md.
  For a component pattern use ?template=pattern.md; for anything else the default.

  AGENT: you authored the skill; populate every field below FROM THE FILE YOU WROTE.
  Three advisory Actions run on this PR — validate-skill-frontmatter (checks the target
  rule and frontmatter shape), check-shared-stub-drift (pins any quoted shared block to
  skills/_shared/), and skill-security-scan (static SkillSpector scan for injection /
  malicious patterns). They comment and may fail their own check; none blocks the merge.
  The human reviewer ratifies by merging.
-->

## What this skill does

- Skill file(s): `skills/<category>/<skill>/SKILL.md`
- One line — what it derives/structures/surfaces, and WHEN to reach for it:

## Agent self-certification

> AGENT: tick each box only after you have verified it against the file you wrote.
> These are honest self-checks the human reviewer relies on; they are not a gate. Note
> next to any box you leave unchecked why.

### Security scan (advisory)

- [ ] Ran `python3 security/skillspector/scan.py skills/<category>/<skill>` and reviewed any findings. A static finding is a prompt for review, not proof of malice (e.g. `Hidden Instructions` over-flags skills that discuss instruction-handling) — note below what was flagged and why it is safe.

### The target rule — target the model, the record, or the blind spot, never the judgment

- [ ] `output_kinds` is a subset of `{proposal, question, menu, halt}`. No fifth kind, and no `status` / `verdict` / `score` / `ranking` / `feasibility` / `disposition` / assessment-of-a-person renamed to slip in.
- [ ] Every example output in the body is genuinely one of those four kinds — nothing that reads like a decision a human could rubber-stamp.
- [ ] Where the skill quotes the canonical rule, it pastes the "Target rule (quoted)" block from `skills/_shared/target-rule.md` verbatim, markers included.

### The deterministic base — the model is enrichment, never a dependency

- [ ] `deterministic_fallback:` names a concrete no-model fallback (split / regex / template / skeleton), one line, honest about depth — not "best-effort heuristics".
- [ ] The body implements that fallback: delete the model step and a reviewer still gets a usable draft. The base may be shallow; it may not be a fiction.
- [ ] The deterministic base and the model step are separate numbered steps, and a merge step keeps the base's output when the model is absent, errors, times out, or violates the vocabulary.
- [ ] The model reasoning step is still present and pulls its weight — a companion to the base, not a replacement.

### Provider-agnostic — tier hints only

- [ ] No model ids are hard-coded anywhere. Model selection names a tier (`frontier` / `mid` / `light`) or defers to the caller — never a vendor or a concrete id.
- [ ] The model swap honours the precedence (global pin → per-call override → skill default tier): deepening the skill is editing one word.

### Survives extraction — the method works without GitHub

- [ ] Any GitHub-native step is marked optional; a reader running this in a bare terminal or another LLM workflow gets a complete result.
- [ ] No step requires a repo, runner, or CI secret to produce its primary artefact.

### No drift in shared stubs

- [ ] Any quoted shared stub (`target-rule`, `deterministic-fallback`, `dismissal-memory`, `trace-edge`, `frozen-8-sections`, `propose-ratify`) is byte-for-byte identical to `skills/_shared/`, markers included (`check-shared-stub-drift` will check).
- [ ] If a shared rule needed to change, it was changed in `skills/_shared/` first, then re-quoted into every skill in THIS PR — never edited in place in a quoted copy.

### Light, advisory, self-contained

- [ ] The skill introduces no enforcement — no blocking approval, no automated blocker, no acceptance-rate metric. It proposes, questions, offers a menu, or halts.
- [ ] Frontmatter is complete: `name:` kebab-case matching the directory; `description:` one line saying WHEN to use it; `output_kinds:` and `deterministic_fallback:` both present.
- [ ] The body reads cleanly on its own — Purpose, When to use, Inputs, numbered Steps, Output format with a concrete template, Notes/anti-patterns. Someone who has never seen this repo could run it from this one file.

## Lint results

> AGENT: run both and paste the output. They are advisory; paste even on failure and
> explain.

```
<!-- python3 skills/_scripts/lint_skill_target_rule.py skills/<category>/<skill>/SKILL.md
     plus the check-shared-stub-drift result if the skill quotes a shared stub -->
```

## Evidence / dogfood

> Optional but encouraged: a run against a real intake/project with the markdown it
> produced, or the no-model deterministic-base output (proof the fallback is not a
> fiction).

## Notes for the reviewing human

> Anything you waived, any box left unchecked on purpose, any open question. The honest
> "here is what I am unsure about" is the most useful line in this box.
