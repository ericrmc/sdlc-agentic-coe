---
name: llm-fanout-orchestrator
description: The reference execution convention every multi-call skill reuses — a provider-agnostic ModelBackend seam with a deterministic fallback and parallel fan-out; framework-free. Use it whenever a skill makes more than one model call (panel, per-section authoring, domain fan-out).
when_to_use: any skill that runs more than one model call (panel, per-section authoring, domain fan-out)
output_kinds: [proposal]
deterministic_fallback: the deterministic-stub base every fan-out wraps
suggested_tier: sonnet
---

# llm-fanout-orchestrator

The portability keystone of this Centre of Excellence. Every other skill in the
library that makes more than one model call — convene a panel, author N design
sections, assess M requirement domains in parallel — describes its work in terms
of the small execution convention defined here. This skill is not a workflow you
run on its own; it is the **contract** that lets the rest of the library run the
same way in Claude Code, in a plain Python harness, or as a headless CI job, with
no framework lock-in.

It is deliberately **framework-free**. There is no LangGraph, no Agent SDK, no
graph-compiler, no hidden runtime. The whole convention is: an interface with one
method, a deterministic stub behind it, and a thread-pool fan-out over it. That is
the entire balance — a *real* multi-call engine without importing anyone's
orchestration framework.

## Purpose

Give every multi-call skill ONE shared way to:

1. **Run with no LLM at all.** There is always a deterministic path that produces
   a valid, useful result. Turning the model on can only *add* quality; it can
   never be a hard dependency.
2. **Swap the model in one line.** Skills never name a provider, a CLI, or a model
   id. They call a `ModelBackend` seam. The running harness binds that seam — dev
   to one backend, production to another — and nothing in the library changes.
3. **Fan out in parallel, safely.** Launch one independent call per
   persona / section / domain at once, capped at a small concurrency. A call that
   fails returns `None` and is *never* fatal to the batch.

## When to use

- You are authoring or running a skill that issues **more than one model call**.
- Typical shapes: a deliberation **panel** (one call per persona), **per-section
  authoring** (one call per solution-design section), a **domain fan-out** (one
  call per requirement area / NFR category / persona lens).
- If a skill makes exactly one model call, it still uses the single-call half of
  this contract (`run_structured`) for the deterministic-fallback guarantee, but
  it does not need the fan-out half.

If a skill makes **zero** model calls (pure deterministic transform), it does not
need this skill at all.

## Inputs

The skill author supplies, in their own SKILL.md:

- **A deterministic base step** — the no-LLM path that already yields a valid
  result (a scaffold, a stub roster, a baseline draft). This is the spine.
- **A list of independent units of work** — the things to fan out over (the
  personas, the sections, the domains). Each unit becomes one parallel call.
- **A prompt per unit** — rendered from the supplied context. In a markdown
  workflow this is just "the instructions you hand each parallel agent."
- **A merge rule** — how a successful call *deepens* its corresponding base item,
  and what happens when a call returns `None` (answer: the base item stands).

No model ids. No provider names. Only a **tier hint** (opus / sonnet / haiku),
which the harness maps to a concrete model.

## The seam

Three things define the contract. They mirror the real implementation in
`backend/app/services/llm_runtime.py` from the app this library was lifted out of.

### 1. `ModelBackend.complete(prompt, model) -> str`

One model completion: a prompt string and a model/tier hint go in, reply text
comes out. Provider-agnostic — it is the *only* place that knows how a model is
actually called.

The harness picks ONE concrete backend at startup:

- A **deterministic-stub backend** (the fallback): returns a fixed, structured
  reply with no network call. This is what makes "run with no LLM" real — the seam
  is always satisfiable.
- A **live backend**: in the source app, a `ClaudeCliBackend` that shells out to
  an authenticated `claude` CLI in headless print mode; the production seam was a
  documented `InBoundaryBackend` reached over HTTP inside the perimeter. Either
  way, **selecting it is a one-line change** (an env var), never an edit to any
  skill or orchestrator.

### 2. `run_structured(key, vars, model=None) -> dict`

The single-call entry point: **render → call → parse JSON → raise-to-fallback-on-
error**.

1. Render the registered prompt for `key` with `vars`.
2. Choose the model (global override → per-call `model` → the key's default tier).
3. `complete(prompt, model)`.
4. Parse a JSON **object** out of the reply (tolerating ```` ```json ```` fences
   and surrounding prose).
5. On *any* failure (render, call, or parse) raise a single error type
   (`ClaudeCliError` in the source) — the caller catches it and uses the
   deterministic stub. Enabling the model can only add quality.

### 3. `run_structured_many(specs, model=None, max_workers=N) -> list[dict | None]`

The fan-out: run N `run_structured` calls **in parallel** over a
`ThreadPoolExecutor`, results returned **in order**.

- `specs` is `[(prompt_key, vars), ...]` — one entry per unit of work.
- **A failed call yields `None` and is NEVER fatal to the batch.** Each worker
  wraps its call in try/except; an exception becomes `None`, logged, never raised.
- If the bridge is off entirely, *every* element is `None` and the deterministic
  base stands unchanged.
- Any request-scoped context (in the source, a project-vision "foreword" carried
  in a `ContextVar`) must be **explicitly propagated into the worker threads** —
  thread pools do not inherit context automatically.

> Worth stating plainly: the whole thing is one interface, one stub, and a
> `ThreadPoolExecutor`. That is the framework. There is intentionally nothing else.

## The method as numbered STEPS

This is the spine every multi-call skill preserves — **the deterministic base
first, the LLM reasoning step layered on top, never the other way around.**

1. **Run the deterministic base.** Call the skill's no-LLM step to get a valid
   baseline result (the scaffold / stub roster / baseline draft). This already
   satisfies the user even if zero model calls succeed.
2. **Select the independent units.** Walk the base and pick the items worth
   deepening with a real model call. Skip items that carry no real signal (in the
   panel, contributions that merely *concur* are left verbatim — the honesty
   rule). Build one `spec = (prompt_key, vars)` per selected unit.
3. **Fan out in parallel.** Call `run_structured_many(specs, max_workers=N)` with
   **N capped small — `<= 4` concurrent** for an interactive markdown workflow
   ("launch one independent agent per persona/section/area in parallel, at most
   four at a time"). The source app used a larger pool server-side; for portable,
   human-facing fan-outs keep it `<= 4` so it stays legible and rate-limit-safe.
4. **Merge successes; let failures stand.** Zip results back to their base items.
   For each result that is a usable dict, *replace* that base item with the
   deepened version. For each `None`, keep the base item as-is. The list returned
   is **always valid**: the deterministic base, plus whatever the fan-out deepened.
5. **Report what deepened.** Note how many of N calls succeeded (e.g. "deepened
   4/6 contributions"). Transparency, not enforcement — this is advisory output.

The one rule every skill obeys, in one line:

> **A no-LLM deterministic path that always produces a valid result, plus a
> one-line model swap to deepen it — fanned out one independent call per unit,
> `<= 4` at a time, where a failed call is `None` and never fatal.**

## The worked example: the deliberation orchestrator

The reference implementation is the panel orchestrator
(`backend/app/services/deliberation_orchestrator.py`). It is the canonical shape
to copy.

1. **Deterministic base.** It wraps a deterministic `run_panel` stub that already
   produces a balanced roster of persona contributions and keeps the hard
   invariants (signal-binding, the honesty rule). This base is valid on its own.
2. **Select units.** It walks the base contributions and **skips any that
   `concurs` or are not bound to a real graph node** — those stay verbatim (the
   honesty rule: no-signal contributions are not "deepened" into invented
   content). The rest each become one spec.
3. **Fan out.** It builds one `("panel_contribution", {...})` spec per remaining
   contribution and calls `run_structured_many(specs)`. Each persona deepens *its
   own* argument independently and in parallel.
4. **Merge.** For each successful dict it `replace`s that contribution's body with
   the model-deepened `body_md` / `stance_summary`; a `None` leaves the base
   contribution untouched.
5. **Stand on the base.** Because `run_structured_many` never raises, the
   orchestrator always returns a valid list — the deterministic base plus whatever
   the fan-out deepened. With the bridge off, every call is `None` and the base is
   returned unchanged.

The red-team pass (`red_team`) is the same shape over adversarial objections: one
parallel `red_team_challenge` call per objection, each deepened independently, the
base standing for any that fail. **Same convention, different unit.** That is the
whole point — every multi-call skill is this shape with a different unit of work.

## GitHub-native note (optional)

The same fan-out maps cleanly onto a **matrix-strategy Actions job** when a skill
runs headless in CI. The list of units becomes the matrix; each matrix leg runs
one unit; a failed leg is the `None` of the fan-out — let it fail soft and merge
the legs that succeeded.

```yaml
# Illustrative — one parallel leg per unit, capped, fail-soft.
jobs:
  fanout:
    strategy:
      fail-fast: false          # a failed leg is the `None` — never fatal to the batch
      max-parallel: 4           # the <= 4 concurrency cap, in CI form
      matrix:
        unit: [persona-a, persona-b, persona-c, persona-d]
    runs-on: ubuntu-latest
    steps:
      - run: ./run-skill-unit.sh "${{ matrix.unit }}"   # one run_structured per unit
  merge:
    needs: fanout
    if: always()                # merge whatever legs succeeded onto the deterministic base
    runs-on: ubuntu-latest
    steps:
      - run: ./merge-onto-base.sh
```

Interactive run and CI run are the **same convention** — `max_workers` in a thread
pool, or `max-parallel` in a matrix. The skill author writes the unit and the
merge once; the harness chooses how to fan out.

## Output format

A skill that follows this contract returns, to the user, markdown that makes the
fan-out legible and advisory:

```markdown
## <skill> result (deterministic base + N parallel calls)

**Base:** <one line — what the deterministic path produced>
**Fan-out:** deepened 4/6 units (2 calls returned nothing → base stands)

### <unit 1 — e.g. persona / section / domain>
<deepened content, or the verbatim base item if its call returned None>

### <unit 2>
...

> Advisory only. Every unit has a valid base; the model deepened what it could.
> Re-running may deepen more or fewer units — the base never regresses.
```

Concrete shape, from the panel:

```markdown
## Panel deliberation (deterministic roster + 5 parallel persona calls)

**Base:** balanced roster of 6 signal-bound contributions
**Fan-out:** deepened 4/5 (the security persona's call returned nothing → its base stance stands)

### Reliability persona — challenges
<model-deepened argument grounded in the bound node>

### Security persona — concurs
<verbatim base contribution; skipped by the honesty rule, not sent to a model>
```

## Notes / anti-patterns

- **No model ids in the library — tier hints only.** Skills say `opus` /
  `sonnet` / `haiku`; the harness maps a tier to a concrete model in exactly one
  place. Never hard-code `claude-…` (or any provider's id) in a skill.
- **Deterministic base first, always.** If you find yourself writing a skill whose
  only path is "call the model," stop — add the no-LLM base. The model *deepens*
  the base; it is never the sole source of a valid result.
- **A failed call is `None`, never an exception that aborts the batch.** Do not let
  one slow or rate-limited unit sink the other N-1. Fail soft, merge the rest.
- **Cap concurrency.** `<= 4` parallel for interactive/markdown fan-outs (a small
  thread pool, or `max-parallel: 4` in CI). Unbounded fan-out invites rate limits
  and illegible output.
- **Propagate request context into workers explicitly.** Thread pools and matrix
  legs do not inherit ambient context (the vision foreword, project scope) — pass
  it into each unit yourself.
- **Don't reach for a framework.** This convention exists precisely so skills do
  *not* depend on LangGraph or an Agent SDK. One interface, one stub, one thread
  pool. Keep it that way.
- **Advisory, not a gate.** The fan-out's job is to deepen and report, never to
  block. It produces proposals; a human decides.

## References

- `references/modelbackend-seam.md` — the `ModelBackend` / `run_structured` /
  `run_structured_many` seam as **PSEUDOCODE** (a portable spec to copy into any
  harness, not an importable binary dependency).
- Source grounding (the app this was lifted from):
  `backend/app/services/llm_runtime.py` (the seam),
  `backend/app/services/deliberation_orchestrator.py` (the worked example),
  `backend/app/prompts/registry.py` (tier-not-id model selection).
