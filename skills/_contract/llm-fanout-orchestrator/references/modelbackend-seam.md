# The ModelBackend seam — portable PSEUDOCODE

> The `ModelBackend` / `run_structured` / `run_structured_many` seam as a **portable
> spec to copy into any harness** — *not* an importable binary dependency. This is the
> contract every multi-call skill reuses: one interface, one deterministic stub, a
> thread-pool fan-out. There is intentionally nothing else — no LangGraph, no Agent SDK,
> no graph-compiler.
>
> Grounded in the real implementation it was lifted from:
> `backend/app/services/llm_runtime.py` (the seam),
> `backend/app/services/deliberation_orchestrator.py` (the worked example),
> `backend/app/prompts/registry.py` (tier-not-id model selection).

## 1. `ModelBackend.complete(prompt, model) -> str`

One model completion: a prompt string and a model/tier hint go in, reply text comes out.
Provider-agnostic — the **only** place that knows how a model is actually called.

```python
class ModelBackend:
    """One model completion: prompt + model id → text reply. Provider-agnostic."""
    name = "abstract"
    def complete(self, prompt: str, model: str) -> str:
        raise NotImplementedError
```

The harness picks **one** concrete backend at startup (a one-line / one-env-var change —
never an edit to any skill or orchestrator):

- **Deterministic-stub backend (the fallback).** Returns a fixed, structured reply with
  no network call. This is what makes "run with no LLM" real — the seam is always
  satisfiable.
- **Live backend.** In the source app, a `ClaudeCliBackend` that shells out to an
  authenticated `claude` CLI in headless print mode, tamed into a clean completion
  endpoint (a `--system-prompt` override so it is *not* the agentic Claude Code,
  user-only settings, no MCP, a neutral cwd). The documented production seam is an
  `InBoundaryBackend` reached over HTTP inside the perimeter.

```python
def select_backend() -> ModelBackend:
    # one env var chooses the backend; nothing else in the library changes
    name = env("LLM_BACKEND", default="claude-cli").lower()
    if name in ("in-boundary", "prod"):
        return InBoundaryBackend()
    if name in ("stub", "deterministic"):
        return DeterministicStubBackend()
    return ClaudeCliBackend()
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

Model selection precedence (tier alias `opus|sonnet|haiku` accepted anywhere a model is):

1. a hard **global override** env (pin everything to one model),
2. the per-call `model` argument,
3. the registry's **per-key tier** (the default mix).

**No model ids in the library — tier hints only.** The harness maps a tier to a concrete
model in exactly one place.

## 3. `run_structured_many(specs, model=None, max_workers=N) -> list[dict | None]`

The fan-out: run N `run_structured` calls **in parallel** over a thread pool, results
returned **in order**.

```python
def run_structured_many(specs, model=None, max_workers=N) -> list[dict | None]:
    # specs = [(prompt_key, vars), ...] — one entry per unit of work
    if not specs:
        return []
    fw = FOREWORD.get()                     # request-scoped context to propagate
    results = [None] * len(specs)
    def one(idx):
        token = FOREWORD.set(fw)            # ContextVars do NOT auto-inherit across a pool — set explicitly
        try:
            key, vars = specs[idx]
            results[idx] = run_structured(key, vars, model=model)
        except Exception:                   # a failed call is None, NEVER fatal to the batch
            results[idx] = None
        finally:
            FOREWORD.reset(token)
    workers = max(1, min(max_workers, len(specs)))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(one, range(len(specs))))
    return results
```

- **A failed call yields `None` and is never fatal.** Each worker wraps its call in
  try/except; an exception becomes `None`, logged, never raised.
- **If the bridge is off entirely, *every* element is `None`** and the deterministic base
  stands unchanged.
- **Propagate request-scoped context into the workers explicitly** (in the source, a
  project-vision "foreword" carried in a `ContextVar`) — thread pools do not inherit it.
- **Cap concurrency.** `<= 4` for an interactive/markdown fan-out; the source app used a
  larger pool server-side (`max_workers=8`). Keep human-facing fan-outs small so they
  stay legible and rate-limit-safe.

## The one rule, in one line

> A no-LLM deterministic path that always produces a valid result, plus a one-line model
> swap to deepen it — fanned out one independent call per unit, `<= 4` at a time, where a
> failed call is `None` and never fatal.

## CI form (the same convention)

The fan-out maps cleanly onto a **matrix-strategy Actions job**: the units become the
matrix, `max-parallel: 4` is the cap, `fail-fast: false` is the `None` (a failed leg
never sinks the batch), and an `if: always()` merge step folds the legs that succeeded
onto the deterministic base. Interactive run and CI run are the same convention —
`max_workers` in a thread pool, or `max-parallel` in a matrix.

## Anti-patterns

- **Don't reach for a framework.** This convention exists precisely so skills do *not*
  depend on LangGraph or an Agent SDK. One interface, one stub, one thread pool.
- **Deterministic base first, always.** The model *deepens* the base; it is never the
  sole source of a valid result.
- **No `claude-…` (or any provider id) hard-coded in a skill** — tier hints only.
- **Advisory, not a gate.** The fan-out deepens and reports; it never blocks.

> This is **pseudocode**, a spec to copy — not an importable binary dependency. A harness
> in Claude Code, in plain Python, or as a headless CI job each implements these three
> shapes its own way; the *contract* is what every skill in the library relies on.
