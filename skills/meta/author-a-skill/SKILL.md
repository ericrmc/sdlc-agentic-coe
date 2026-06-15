---
name: author-a-skill
description: A wizard for a CONTRIBUTOR (an agent) adding to this library — classify the contribution as a skill, a pattern, or a capability, then either scaffold a new SKILL.md (a proposal) or route to the right authoring skill (library/author-component-pattern, library/author-capability). It wraps CONTRIBUTING.md and cites the templates; it never duplicates their content, and it states the one structural gate plainly (patterns and capabilities are CODEOWNERS-reviewed; skills are advisory). Use it when you want to ADD to the library rather than use it.
one_liner: A wizard that walks a contributor through adding a skill, pattern, or capability — citing CONTRIBUTING, never duplicating it.
aliases: [add a skill, contribute, new skill wizard, how do I add a pattern, author a capability, scaffold a skill, contribute to the library, write a new SKILL.md, add to the centre of excellence, contribution wizard]
when_to_use: you want to ADD to the library — a new skill, pattern, or capability — and want to be walked through the right path, the required frontmatter/fields, the templates to cite, and where the human review gate sits
output_kinds: [proposal, question, menu]
deterministic_fallback: read CONTRIBUTING.md top to bottom and follow its "Add a skill / Add a pattern / Add a capability" section directly, plus the matching template (skills via skill.md template, patterns/_TEMPLATE.md, the new-capability issue); the wizard only orders those steps and pre-fills the skill scaffold
suggested_tier: mid
tier_reason: one bounded pass — classify the contribution against three known kinds and scaffold or route accordingly; the rules and templates are fixed in CONTRIBUTING.md, so this weighs little and authors only a frontmatter skeleton
neighbours:
  before: skills/MAP.md (where the contributor sees the existing categories a new skill would slot into)
  after: skills/library/author-component-pattern (when the contribution is a pattern, this is the real authoring skill the wizard routes to; library/author-capability when it is a capability)
---

# author-a-skill — the contribution front door

You are an agent who wants to **add** to this library — a new skill, a new pattern, or a new
capability — and you want to be walked through the right path rather than reverse-engineer it
from the existing files. This wizard does that.

It is a thin guide over `CONTRIBUTING.md`. It **cites** that file and the templates; it does
**not** restate their rules or copy their field lists. When the rules change, they change in
`CONTRIBUTING.md` and this wizard still points at the same place — so it can never drift out of
sync with the contract it wraps.

> **It scaffolds or routes; the human ratifies.** Its outputs are a `proposal` (a scaffolded
> `SKILL.md` skeleton for a new skill), a `menu` (the path options, or the real authoring skill
> to hand off to), or a `question` (which kind is this, what is missing). It sets no `status`
> and blesses nothing — a maintainer merges the PR. For a pattern or capability it does not even
> write the file: it routes to the dedicated authoring skill, because `patterns/**` and
> `capabilities/**` carry a structural human review this wizard must not pretend to satisfy.

## Purpose

Turn "I want to contribute X" into the correct, in-contract next action — without the
contributor having to know the three contribution kinds, the required frontmatter, the templates,
and the one review gate in advance. It **classifies, then scaffolds or routes**, always citing
`CONTRIBUTING.md` as the authority.

## When to use

- You have an idea for a new **skill**, **pattern**, or **capability** and want the right path.
- You are unsure **which kind** your contribution is (a reusable instruction? a built component?
  a plain-language need?).
- You want the **frontmatter skeleton** for a new skill pre-filled so you can flesh it out.

Do **not** use it to *run* the library on an engagement — that is its sibling
`skills/meta/navigator`. This wizard is for adding to the library, not using it.

## Inputs

- **Contribution idea** — *Required.* A sentence or two on what you want to add and why. *If
  absent/unreadable/empty:* do not invent a contribution — ask what the contributor wants to add
  (surface it as a `question`; the same no-fabrication discipline as `_shared/grounding.md`,
  applied to a contribution rather than a project input). The wizard reasons over the
  *contribution idea*, never over a project's requirements, so it routes and scaffolds — it
  produces no project content.
- **The contract + templates** — *Optional (assumed present).* `CONTRIBUTING.md`,
  `skills/MAP.md`, the skill PR template, `patterns/_TEMPLATE.md`,
  `patterns/_schema/pattern.frontmatter.schema.json`, and `capabilities/INDEX.md`. The wizard
  cites these; it never duplicates their content.

## The three contribution kinds (the classification, per CONTRIBUTING.md)

`CONTRIBUTING.md` opens by naming exactly three things this repo holds. The wizard's first move
is to place the contribution in one of them — read CONTRIBUTING for the authoritative definition
of each; the one-liners below are only to disambiguate:

| Kind | It is… | Where it lives | Who ratifies |
|---|---|---|---|
| **skill** | a portable agent instruction (one self-contained `SKILL.md`) | `skills/<category>/<name>/SKILL.md` | **advisory** — a CODE maintainer merges; CI annotates |
| **pattern** | a component the firm has **actually built**, with governed NFRs + evidence | `patterns/<category>/<slug>.md` | **CODEOWNERS-gated** (`patterns/**`) — a human architect ratifies |
| **capability** | the technology-free **need** that resolves a requirement to a pattern | `capabilities/<domain>/<slug>.md` | **CODEOWNERS-gated** (`capabilities/**`) — a human architect ratifies |

> **The one structural gate, stated plainly (CONTRIBUTING.md "One structural human gate").**
> `CODEOWNERS` routes `patterns/**` and `capabilities/**` to the architect team; branch
> protection requires that review before merge. **Skills are advisory** — everything else is a
> CI annotation a human may merge over with a reason. This is why the wizard *scaffolds* a skill
> directly but *routes* a pattern or capability to its dedicated authoring skill: the gated kinds
> get the human review the gate exists for.

## The method

### STEP 0 — confirm there is a contribution to place

Check the one required input: is there a **contribution idea**? If not, ask for it as a
`question` — what do you want to add, and why? Do not assume the kind or invent a contribution.
Once you have it, classify it.

### STEP 1 — classify the contribution (skill | pattern | capability)

Place the idea in one of the three kinds above. If it is genuinely ambiguous (e.g. "a reusable
deployment thing" could be a *pattern* if it has been built, or a *capability* if it is the need
behind one), return a **menu** of the candidate kinds — each with the one question that decides
it (per the table: *has it been built with evidence?* → pattern; *is it a plain-language need?*
→ capability; *is it a portable instruction?* → skill) — and let the contributor pick. Never
guess the kind silently.

### STEP 2 — route or scaffold

- **It is a pattern** → route (a `menu`/`question`) to `skills/library/author-component-pattern`.
  Note the floor CONTRIBUTING names (the agent writes `approval_status: candidate`; a CODEOWNER
  architect ratifies past that with evidence). Do **not** scaffold the pattern file here — that
  skill owns the schema and the linter (`skills/_scripts/lint_pattern_frontmatter.py`).
- **It is a capability** → route to `skills/library/author-capability`, and remind the
  contributor to add its alias rows to `capabilities/INDEX.md`. The wizard does not write the
  capability file — it is `capabilities/**`-gated.
- **It is a skill** → **scaffold a `SKILL.md` skeleton** as a `proposal` (STEP 3). This is the
  gap the wizard fills directly; the other two kinds have dedicated authoring skills, a new
  skill does not.

### STEP 3 — scaffold the SKILL.md skeleton (the proposal, for a skill only)

Pre-fill the frontmatter the linters require, leaving the contributor to flesh out the body.
Cite CONTRIBUTING's "Add a skill" section and the skill PR template for the field meanings;
**do not re-explain them here.** The skeleton to propose:

```markdown
---
name: <kebab-case, matches the directory>
description: <one line saying WHEN to reach for this skill>
one_liner: <the single-sentence purpose>
aliases: [<lay synonym>, <lay synonym>, …]   # how a runner might ask for it
when_to_use: <the situation that should make an agent open this file>
output_kinds: [<a non-empty subset of: proposal, question, menu, halt>]
deterministic_fallback: <the no-model base this skill degrades to>
suggested_tier: <frontier | mid | light>   # never a model id
tier_reason: <one line: why that tier>
neighbours:
  before: <the skill that usually runs before this one + why>
  after: <the skill this hands off to + why>
---

# <name> — <one-line title>

## Purpose
## When to use
## Inputs            # mark each row Required / Optional
## Grounding (quoted) # REQUIRED if any input is Required — paste the byte-stable
                      #   block from skills/_shared/grounding.md verbatim, and wire a
                      #   STEP 0 halt; cite skills/_contract/grounding-no-absent-input
## The method        # numbered steps; deterministic base first, model step marked
## Output format      # which of proposal | question | menu | halt, and its shape
## Notes / contract compliance
```

Flag the **grounding obligation** as part of the proposal: *if the new skill reads or writes a
requirement (or any project input), it MUST mark that input Required, quote the grounding block,
cite `skills/_contract/grounding-no-absent-input`, and wire a STEP 0 halt* — per CONTRIBUTING and
the keystone contract. The wizard names this requirement; it does not relax it.

### STEP 4 — name the checks and the PR, then stop

Tell the contributor which advisory checks to run before opening the PR (citing CONTRIBUTING,
not re-deriving them):

- `python3 skills/_scripts/lint_skill_target_rule.py skills/<category>/<name>/SKILL.md`
  (output is one of `proposal | question | menu | halt`);
- `python3 skills/_scripts/lint_skill_grounding.py skills/<category>/<name>/SKILL.md`
  (stub cited + halt wired, if it has a Required input);
- the shared-stub-drift check (auto-discovers `skills/_shared/*.md`; runs in CI).

Then: open a PR with the skill template (`?template=skill.md`) and paste the check results. A
CODE maintainer reviews and ratifies by merging. The wizard **stops here** — it proposes the
scaffold and names the path; it never opens the gate or sets a status itself.

## Output format

Exactly one of three kinds:

- a **`proposal`** — the scaffolded `SKILL.md` skeleton (STEP 3), for a *skill* contribution;
- a **`menu`** — the candidate kinds when classification is ambiguous (STEP 1), or the routing
  options to a dedicated authoring skill (STEP 2);
- a **`question`** — what do you want to add (STEP 0), or which kind is this (STEP 1).

Never a `status`, `approval`, `score`, or `verdict`: the wizard scaffolds and routes; a human
ratifies by merging, and the gated kinds get their CODEOWNERS review.

## Notes / contract compliance

- **Wraps, never duplicates.** Every rule, field list, and template reference points at
  `CONTRIBUTING.md`, the templates, and the schema — the single sources of truth. If this wizard
  ever restates a rule, it has drifted; cite instead.
- **Altitude.** A meta-skill about *contributing*, not a project artefact. It produces a scaffold
  and routes; it sets no lifecycle field beyond what a skill author legitimately writes.
- **The gate is real and named.** `patterns/**` and `capabilities/**` are CODEOWNERS-reviewed;
  skills are advisory. The wizard routes the gated kinds to their authoring skills so the human
  review is not bypassed — it never writes a pattern or capability file itself.
- **Output discipline.** `proposal | question | menu` only — the closed kinds from
  `_shared/target-rule.md`. (No `halt`: an absent contribution idea is asked for as a `question`,
  since the wizard reasons over a contribution, not a grounded project input.)
- **Provider-agnostic.** Classifying a contribution and filling a frontmatter skeleton needs only
  a markdown-reading agent; the authority is the on-disk `CONTRIBUTING.md` and templates.
