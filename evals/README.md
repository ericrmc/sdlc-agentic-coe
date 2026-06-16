# Entrypoint evals

Does a cold agent, pointed only at this repo, **orient itself and run a skill correctly?**
Each case feeds a prompt to an agent harness (read-only) and grades the agent's answer with
**deterministic assertions — no judge model, no API key.** It catches what a linter cannot:
a rename that breaks navigation, a tightening pass that drops a grounding `halt`, a skill
whose output format drifts.

These tests **invoke a real agent harness** (which needs its own install + auth), so this is a
**local / on-demand** suite a maintainer runs — not a per-PR Action. (The harness-agnostic
design is itself what's under test.)

## Run

```bash
python3 evals/run.py                  # all cases, claude -p
python3 evals/run.py --harness codex  # codex exec
python3 evals/run.py --case orientation
python3 evals/run.py --list
```

Harnesses (read-only, run in the repo root):
- `claude` — `claude -p --allowedTools Read Glob Grep` (needs Claude Code + its auth)
- `codex`  — `codex exec --sandbox read-only -o <file>` (needs Codex + its auth)
- `cmd`    — `$EVAL_HARNESS_CMD` reads the prompt on stdin, prints the answer (any other harness)

Transcripts land in `evals/results/<harness>/` and a `report.json` (git-ignored). The runner
exits non-zero if any case fails.

## Cases

| id | category | checks |
|---|---|---|
| `orientation` | navigation | finds ENTRYPOINT, names both front doors, routes the BA persona to `decompose-intake-to-outcomes` |
| `routing-architect` | navigation | a need-first architect is routed to `capabilities/INDEX.md` + `recommend-component-patterns` |
| `apply-decompose` | skill-execution | navigates to the skill and produces its exact output shape (BO-/REQ- keys, `derives_from`, GIVEN/WHEN/THEN, a measurable NFR) |
| `grounding-halt` | grounding | **negative** — given no input, the agent HALTs and asks, never fabricates (the regression that catches a broken grounding stub) |

## Add a case

Drop two files in `cases/`:
- `<id>.prompt.md` — the prompt the agent receives.
- `<id>.json` — `{ id, category, description, allowed_tools?, assert }`. The `assert` block:
  `contains` (all present, case-insensitive), `contains_any` (≥1 present), `not_contains`
  (none present), `regex` (all match, case-insensitive + dotall). Assert on the skill's
  **output-format invariants** (keys, edges, the halt), not exact wording — wording drifts,
  invariants are the contract.

Grading is deterministic by design (reproducible, key-free). A richer LLM-as-judge layer for
rubric scoring is a possible future add-on, kept optional for the same reason the SkillSpector
semantic layer is (it would need a model).
