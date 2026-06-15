---
name: parallel-agents
description: The execution convention every multi-call skill reuses — a provider-agnostic model seam with a deterministic fallback and parallel fan-out, framework-free. Use it whenever a skill makes more than one model call (panel, per-section authoring, domain fan-out).
one_liner: Run many model calls in parallel over a deterministic base.
aliases:
  - parallel agents
  - fan out
  - run skills in parallel
  - concurrent model calls
  - batch model calls
  - deterministic fallback
  - thread pool of agents
when_to_use: any skill that runs more than one model call (panel, per-section authoring, domain fan-out)
output_kinds: [proposal]
deterministic_fallback: the deterministic base every fan-out wraps
suggested_tier: mid
neighbours: |
  Reused by, not run on its own. The multi-call skills that follow this convention
  include panel/convene-a-panel (one call per persona), architect/synthesise-solution-architecture
  (one call per design section), and challenge/red-team-requirements (one call per objection).
---

# Parallel agents

Run several model calls in parallel on top of a deterministic base, with no
framework. This is not a workflow to run on its own; it is the convention a skill
follows when it makes more than one model call — convene a panel, author N design
sections, assess M requirement domains at once. The whole convention is small: an
interface with one method, a deterministic stub behind it, and a capped parallel
fan-out over it. Nothing else.

It gives every multi-call skill one shared way to:

1. **Run with no model at all.** A deterministic path always produces a valid,
   useful result. A model can only add quality; it is never a hard dependency.
2. **Swap the model in one place.** Skills never name a provider, a CLI, or a
   model id — they call a model seam. The harness binds that seam; the skill does
   not change.
3. **Fan out in parallel, safely.** One independent call per persona / section /
   domain, capped small. A call that fails returns nothing and is never fatal.

## When to use

Use it for any skill that issues **more than one model call** — a panel (one call
per persona), per-section authoring (one call per design section), or a domain
fan-out (one call per requirement area, NFR category, or lens). A skill that makes
exactly one model call still uses the single-call half (`run_structured`) for the
deterministic-fallback guarantee, but not the fan-out half. A skill that makes zero
model calls does not need this convention.

## Inputs the skill author supplies

- **A deterministic base step** — the no-model path that already yields a valid
  result (a scaffold, a stub roster, a baseline draft).
- **A list of independent units** to fan out over (the personas, sections,
  domains). Each unit becomes one parallel call.
- **A prompt per unit**, rendered from the supplied context (the instructions
  handed to each parallel call).
- **A merge rule** — how a successful call deepens its base item, and what happens
  on nothing returned (the base item stands).

No model ids — only a **tier hint** (`frontier | mid | light`), which the harness
maps to a concrete model.

## The seam

Three shapes define the convention.

**1. `complete(prompt, model) -> str`** — one model completion. Provider-agnostic;
the only place that knows how a model is actually called. The harness binds one
backend at startup: a **deterministic-stub backend** (the fallback — a fixed,
structured reply with no network call, which is what makes "run with no model"
real), or a **live backend** (any real endpoint). Selecting it is a one-line
change, never an edit to a skill.

**2. `run_structured(key, vars, model=None) -> dict`** — the single call:
**render → call → parse JSON → raise-to-fallback-on-error.**

1. Render the registered prompt for `key` with `vars`.
2. Choose the model (global override → per-call `model` → the key's default tier).
3. `complete(prompt, model)`.
4. Parse a JSON **object** out of the reply (tolerating ```` ```json ```` fences
   and surrounding prose).
5. On *any* failure (render, call, or parse) raise one error type; the caller
   catches it and uses the deterministic stub.

**3. `run_structured_many(specs, model=None, max_workers=N) -> list[dict | None]`**
— the fan-out: N `run_structured` calls in parallel, results returned **in order**.
`specs` is `[(prompt_key, vars), ...]`, one per unit. **A failed call yields `None`
and is never fatal** — each is wrapped so an exception becomes `None`. If no model
is bound, every element is `None` and the base stands unchanged. Any request-scoped
context (a shared foreword, project scope) must be **passed into each parallel call
explicitly** — parallel calls do not inherit ambient context.

## The method as numbered steps

The deterministic base comes first; the model step layers on top, never the other
way around.

1. **Run the deterministic base** to get a valid baseline (scaffold / stub roster
   / baseline draft). This satisfies the user even if zero model calls succeed.
2. **Select the independent units.** Pick the items worth deepening. Skip items
   with no real signal (in a panel, contributions that merely *concur* are left
   verbatim — the honesty rule). Build one `spec = (prompt_key, vars)` per unit.
3. **Fan out in parallel** with `run_structured_many(specs, max_workers=N)`, **N
   capped small — `<= 4` concurrent** for an interactive markdown workflow (one
   independent call per persona/section/area, at most four at a time). Keep it
   `<= 4` so it stays legible and rate-limit-safe.
4. **Merge successes; let failures stand.** Zip results to base items: a usable
   dict *replaces* its base item with the deepened version; a `None` keeps the base
   item as-is. The list returned is **always valid** — the base plus what deepened.
5. **Report what deepened** (e.g. "deepened 4/6 contributions"). Transparency, not
   enforcement — advisory output.

The one rule, in one line:

> **A no-model deterministic path that always produces a valid result, plus a
> one-line model swap to deepen it — fanned out one independent call per unit,
> `<= 4` at a time, where a failed call is `None` and never fatal.**

## Worked example: a deliberation panel

1. **Base:** a no-model step produces a balanced roster of persona contributions
   and keeps the hard invariants (signal-binding, the honesty rule). Valid alone.
2. **Select:** skip contributions that merely concur or are not bound to a real
   signal — those stay verbatim. The rest each become one spec.
3. **Fan out:** one `("panel_contribution", {...})` spec per remaining
   contribution; each persona deepens its own argument in parallel.
4. **Merge:** a successful dict replaces that contribution's body; a `None` leaves
   the base contribution untouched.
5. **Stand on the base:** the result is always a valid list. With no model bound,
   every call is `None` and the base returns unchanged.

A red-team pass is the same shape over adversarial objections: one parallel call
per objection, deepened independently, the base standing for any that fail. Same
convention, different unit — that is the whole point.

## CI-native note (optional)

The same fan-out maps onto a **matrix-strategy Actions job** for headless CI: the
units become the matrix, each leg runs one unit, a failed leg is the `None` (let it
fail soft), and a merge step folds the legs that succeeded onto the base.

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
    if: always()                # merge whatever legs succeeded onto the base
    runs-on: ubuntu-latest
    steps:
      - run: ./merge-onto-base.sh
```

Interactive run and CI run are the same convention — `max_workers` in a parallel
fan-out, or `max-parallel` in a matrix.

## Output format

Return markdown that makes the fan-out legible and advisory:

```markdown
## <skill> result (deterministic base + N parallel calls)

**Base:** <one line — what the deterministic path produced>
**Fan-out:** deepened 4/6 units (2 calls returned nothing → base stands)

### <unit 1 — persona / section / domain>
<deepened content, or the verbatim base item if its call returned None>

### <unit 2>
...

> Advisory only. Every unit has a valid base; the model deepened what it could.
> Re-running may deepen more or fewer units — the base never regresses.
```

## Notes / anti-patterns

- **No model ids — tier hints only** (`frontier` / `mid` / `light`); the harness
  maps a tier to a concrete model in one place.
- **Deterministic base first, always.** If a skill's only path is "call the
  model," add a no-model base; the model deepens it, never replaces it.
- **A failed call is `None`, never an exception that aborts the batch.** Fail soft,
  merge the rest.
- **Cap concurrency** at `<= 4` (or `max-parallel: 4` in CI). Unbounded fan-out
  invites rate limits and illegible output.
- **Pass request context into each call explicitly** — parallel calls and matrix
  legs do not inherit ambient context.
- **Don't reach for a framework.** One interface, one stub, one capped fan-out.
- **Advisory, not enforcement.** The fan-out deepens and reports; it never blocks.
  It produces proposals; a human decides.

## References

- `references/model-seam.md` — the model seam / `run_structured` /
  `run_structured_many` shapes as **pseudocode**: a portable spec to copy into any
  harness, not an importable dependency.
