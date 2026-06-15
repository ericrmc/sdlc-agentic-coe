# Getting started

You are the agent. Each skill is one self-contained `SKILL.md` — its steps, vocabulary, and output format travel with it. Read one skill folder plus the project files and run it. Never load the whole repo. Every output you emit is a **proposal**, **question**, **menu**, or **halt**; a human ratifies by merging the PR.

Every analysis skill **HALTs rather than invents** when a required input is missing — it asks where the input is and stops, never fabricates a hypothetical requirement, key, number, or acceptance criterion (the keystone is `skills/_contract/grounding-no-absent-input/SKILL.md`).

## If you are an agent doing X, start here

Match the task you were handed to a starting point.

| If you are doing this for a… | Start at |
| --- | --- |
| **BA** whose requirements live in Excel / a GitHub Project / loose docs — lift them in with provenance | `skills/ingest/ingest-source-to-requirements/SKILL.md` |
| **BA** with a raw vision / intake doc — structure it into outcomes + requirements | `skills/understand/decompose-intake-to-outcomes/SKILL.md` |
| **BA** with requirements already — stress-test them before solutioning | `skills/challenge/red-team-requirements/SKILL.md` |
| **Architect** who knows the *need* but not the technology ("a data warehouse", "run our agents in prod") | `capabilities/INDEX.md` |
| **Architect** choosing technology — adopt a proven, governed pattern before building custom | `skills/architect/recommend-component-patterns/SKILL.md` (then `capabilities/INDEX.md` if nothing fits) |
| **Architect** authoring the design doc — produce the durable solution architecture | `skills/architect/synthesise-solution-architecture/SKILL.md` |
| **Lead** battle-testing a design — adversarial + affirmative review with recorded dissent | `skills/panel/convene-a-panel/SKILL.md` |
| **Delivery lead** planning the build — phases, releases, waves, hand-off | `skills/deliver/describe-phases-releases-waves/SKILL.md` |
| **Practice lead** wanting portfolio health across projects | `docs/portfolio-github-projects.md` |
| Anyone unsure where to start | `skills/MAP.md` |

**Need-first?** When the task names a need in plain words but not the technology, read `capabilities/INDEX.md`. It maps lay synonyms to a canonical capability and tells you whether a proven component already fulfils it or whether spikes are still owed.

## Point your agent at a skill

| Host | Wire-up |
| --- | --- |
| **Claude Code** | `git clone` the repo. Drop `skills/<category>/<skill>/` into `.claude/skills/`, or prompt: `read skills/challenge/red-team-requirements/SKILL.md and run it on requirements/`. |
| **Cursor** | Add the repo to the workspace, `@`-mention the `SKILL.md` path in chat, or paste a `generated/combined/*.md` bundle into a `.cursor/rules` file. |
| **Codex / generic CLI agent** | Feed `skills/<category>/<skill>/SKILL.md` (or a `generated/` bundle) into the prompt as context alongside the project files. |
| **Any markdown-reading LLM** | Paste the single `SKILL.md` into the chat. It is self-contained — no other file is required. |

## Model tiers

Each skill carries a `suggested_tier` — a provider-agnostic hint, never a model id. Map it to a model in the host harness.

| Tier | Use for |
| --- | --- |
| `frontier` | high-stakes synthesis, adversarial judgement, output that shapes a human commitment |
| `mid` | one bounded structured pass over given facts (classify, propagate, scaffold, reconcile) |
| `light` | mechanical, navigational, or templating work — no weighing |

Drop to a cheaper tier any time: every skill ships a deterministic base that runs with no model, so a lower tier degrades gracefully rather than breaking.

## Fast start (end-to-end)

A vision lands and you want it build-ready. One pass through the flow:

1. **Understand.** Run `skills/understand/decompose-intake-to-outcomes/SKILL.md` on the vision doc for structured outcomes, then `classify-requirements` and `nfr-coverage-check` to derive and check requirements.
2. **Challenge.** Run `skills/challenge/red-team-requirements/SKILL.md` over those requirements to surface conflicts, gaps, and gold-plating before any solutioning.
3. **Architect.** Name the need, look it up in `capabilities/INDEX.md`, then run `skills/architect/recommend-component-patterns/SKILL.md` to match a proven pattern (route to `surface-solution-options` when nothing fits). Author the design with `synthesise-solution-architecture`.
4. **Panel.** Battle-test the design with `skills/panel/convene-a-panel/SKILL.md`, recording dissent.
5. **Deliver.** Plan the build with `skills/deliver/describe-phases-releases-waves/SKILL.md` and hand off with the testing and design scaffolds under `skills/deliver/`.

Propose at every step; the human ratifies by merging. This is a map, not a track — enter at any node, loop back freely. See `skills/MAP.md` for the full set.
