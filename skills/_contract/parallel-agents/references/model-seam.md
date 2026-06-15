# The model seam — portable pseudocode

> The model seam / `run_structured` / `run_structured_many` shapes as a **portable
> spec to copy into any harness** — *not* an importable dependency. This is the
> convention every multi-call skill reuses: one interface, one deterministic stub, a
> capped parallel fan-out. There is intentionally nothing else — no graph compiler,
> no orchestration framework.

## 1. `complete(prompt, model) -> str`

One model completion: a prompt string and a model/tier hint go in, reply text comes out.
Provider-agnostic — the **only** place that knows how a model is actually called.

```python
class ModelSeam:
    """One model completion: prompt + model id → text reply. Provider-agnostic."""
    name = "abstract"
    def complete(self, prompt: str, model: str) -> str:
        raise NotImplementedError
```

The harness picks **one** concrete backend at startup (a one-line / one-env-var change —
never an edit to a skill):

- **Deterministic-stub backend (the fallback).** Returns a fixed, structured reply with
  no network call. This is what makes "run with no model" real — the seam is always
  satisfiable.
- **Live backend.** Any real model endpoint, bound behind the same seam.

```python
def select_backend():
    # one env var chooses the backend; nothing else in the library changes
    name = env("MODEL_BACKEND", default="live").lower()
    if name in ("stub", "deterministic"):
        return DeterministicStubBackend()
    return LiveBackend()
```

## 2. `run_structured(key, vars, model=None) -> dict`

The single-call entry point: **render → call → parse JSON → raise-to-fallback-on-error.**

```python
def run_structured(key, variables, model=None) -> dict:
    prompt = registry.render(key, **variables)          # 1. render the registered prompt
    chosen = choose_model(key, model)                   # 2. global override → per-call → key's tier
    text   = complete(prompt, chosen)                   # 3. the one model call
    return parse_json_object(text)                      # 4. lift a JSON object out (tolerates ```json fences + prose)
    # 5. ON ANY FAILURE (render / call / parse) raise ONE error type;
    #    the caller catches it and uses the deterministic stub.
```

Model selection precedence (tier alias `frontier|mid|light` accepted anywhere a model is):

1. a hard **global override** env (pin everything to one model),
2. the per-call `model` argument,
3. the registry's **per-key tier** (the default mix).

**No model ids — tier hints only.** The harness maps a tier to a concrete model in exactly
one place.

## 3. `run_structured_many(specs, model=None, max_workers=N) -> list[dict | None]`

The fan-out: run N `run_structured` calls **in parallel**, results returned **in order**.

```python
def run_structured_many(specs, model=None, max_workers=N) -> list[dict | None]:
    # specs = [(prompt_key, vars), ...] — one entry per unit of work
    if not specs:
        return []
    foreword = current_context()            # request-scoped context to propagate
    results = [None] * len(specs)
    def one(idx):
        with bind_context(foreword):        # parallel calls do NOT auto-inherit context — pass it explicitly
            try:
                key, vars = specs[idx]
                results[idx] = run_structured(key, vars, model=model)
            except Exception:               # a failed call is None, NEVER fatal to the batch
                results[idx] = None
    workers = max(1, min(max_workers, len(specs)))
    run_in_parallel(one, range(len(specs)), max_workers=workers)
    return results
```

- **A failed call yields `None` and is never fatal.** Each call is wrapped so an exception
  becomes `None`, logged, never raised.
- **If no model is bound at all, *every* element is `None`** and the deterministic base
  stands unchanged.
- **Pass request-scoped context into each parallel call explicitly** (for example a shared
  foreword) — parallel calls do not inherit it.
- **Cap concurrency.** `<= 4` for an interactive/markdown fan-out. Keep human-facing
  fan-outs small so they stay legible and rate-limit-safe.

## The one rule, in one line

> A no-model deterministic path that always produces a valid result, plus a one-line model
> swap to deepen it — fanned out one independent call per unit, `<= 4` at a time, where a
> failed call is `None` and never fatal.

## CI form (the same convention)

The fan-out maps cleanly onto a **matrix-strategy Actions job**: the units become the
matrix, `max-parallel: 4` is the cap, `fail-fast: false` is the `None` (a failed leg
never sinks the batch), and an `if: always()` merge step folds the legs that succeeded
onto the deterministic base. Interactive run and CI run are the same convention —
`max_workers` in a parallel fan-out, or `max-parallel` in a matrix.

## Anti-patterns

- **Don't reach for a framework.** This convention exists precisely so skills do *not*
  depend on one. One interface, one stub, one capped fan-out.
- **Deterministic base first, always.** The model *deepens* the base; it is never the
  sole source of a valid result.
- **No provider model id hard-coded in a skill** — tier hints only.
- **Advisory, not enforcement.** The fan-out deepens and reports; it never blocks.

> This is **pseudocode**, a spec to copy — not an importable dependency. A harness in an
> interactive agent, in plain code, or as a headless CI job each implements these three
> shapes its own way; the *convention* is what every multi-call skill relies on.
