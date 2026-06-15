# SDLC Agentic Centre of Excellence

A portable, GitHub-native library of advisory agent skills for the early software lifecycle — from a business vision to a build-ready solution design and on through phases and releases. Each skill is self-contained markdown (steps + YAML frontmatter) an agent reads and runs inside any LLM workflow, backed by a PR-reviewed library of reusable component **patterns** and the **capabilities** that bridge a plain-language need to a proven component.

Read this as the agent who will use it. You author the patterns, capabilities, and skill changes and open the PR; a human reviewer ratifies it by merging.

## Start here

| To do this | Read |
| --- | --- |
| Enter the library — be walked through an engagement, or add to it | [`ENTRYPOINT.md`](ENTRYPOINT.md) (→ `meta/navigator` to use, `meta/author-a-skill` to contribute) |
| Pick your starting point and wire up your tool | [`GETTING-STARTED.md`](GETTING-STARTED.md) |
| See every skill and the end-to-end flow | [`skills/MAP.md`](skills/MAP.md) |
| Resolve a need ("a data warehouse", "run our agents in prod") to a component | [`capabilities/INDEX.md`](capabilities/INDEX.md) |
| Run a leadership-altitude portfolio view across projects | [`docs/portfolio-github-projects.md`](docs/portfolio-github-projects.md) |

## Skill categories

| Category | What it does |
| --- | --- |
| [`ingest`](skills/ingest/) | Lift a structured-but-messy source (spreadsheet, ticket board, docs folder, export) into traceable requirement markdown with provenance — or HALT for it, never invent. |
| [`understand`](skills/understand/) | Turn a raw vision or intake into structured outcomes, requirements, NFR coverage, and the capability each requirement fulfils. |
| [`challenge`](skills/challenge/) | Pressure-test a requirement set: conflicts, gaps, gold-plating, risks, assumptions, roadblocks, necessity. |
| [`architect`](skills/architect/) | Choose a solution shape and author the design: recommend patterns, explore options, propagate NFRs, validate, synthesise. |
| [`panel`](skills/panel/) | Multi-voice deliberation and review: convene a panel, synthesise it, record dissent, run design and a11y review. |
| [`deliver`](skills/deliver/) | Plan the lifecycle and hand off the build: feature intake, phases, releases, waves, cutover, triage, testing/build/design scaffolds, estimate. |
| [`library`](skills/library/) | Author and curate the reusable assets: component patterns, capabilities, portfolio health, governance checklist. |
| [`meta`](skills/meta/) | Skills about using and extending the library: `navigator` (the front door — walks an engagement stage by stage) and `author-a-skill` (the contribution wizard). |

## How a skill behaves

- Every output is one of exactly four kinds — **proposal**, **question**, **menu**, or **halt**. Never emit a verdict, status, score, or approval; the human decides.
- A skill runs with no model at all as a deterministic base, then deepens with a single model step (provider-agnostic tier hint: `frontier` | `mid` | `light`).
- The output format and template travel inside each `SKILL.md`. Read one folder plus the project files — never the whole repo.

## Automation (GitHub Actions)

When you author a pattern, capability, or skill change and open a PR, the pipeline validates it for you and posts a pass/fail summary the human reviewer reads. Nothing here blocks a merge — every Action is advisory; CODEOWNERS is the only structural gate.

| Action | Trigger | What it does for you |
| --- | --- | --- |
| `validate-patterns` | PR touching `patterns/**` | Lints pattern frontmatter against the schema; sticky PR comment lists any field you left wrong or missing. |
| `validate-capabilities` | PR touching `capabilities/**` | Lints capability frontmatter (need-statement, aliases, governance NFRs, fulfilment confidence) so a candidate enters clean. |
| `validate-skill-frontmatter` | PR touching `skills/**`, `patterns/**`, `capabilities/**`, `references/**` | Runs the target-rule lint (no output kind outside the closed four; no agent-set `approval_status`) plus the map-link, references, and capability-index checks. |
| `concat-patterns` | push to `main`; PR labelled `build:combined` | Combines related patterns and skills into `generated/` bundles so an agent can load one file instead of many. |
| `pattern-lifecycle` | weekly schedule; on demand | Recomputes pattern maturity from the adoption ledger and opens revalidation/sunset issues. Never deletes a pattern that has adoptions. |
| `portfolio-rollup` | weekday schedule; on demand | Writes an advisory RAG verdict per project to the org Project board. See [`docs/portfolio-github-projects.md`](docs/portfolio-github-projects.md). |
| `check-shared-stub-drift` | PR touching `skills/**` | Flags when a quoted shared convention has drifted from its canonical copy. |

Each Action is a thin runner of a script under `skills/_scripts/` that you can also run locally before opening the PR.

## Patterns and capabilities

A **pattern** is one markdown file (`patterns/<category>/<key>.md`) capturing a proven solution shape — its frontmatter carries the intent, topology, attached NFRs, and the `evidence[]` proving it was built. It may also carry `reference_implementations[]`: a forward pointer to a working artefact (an IaC repo, app, notebook, scaffold, module, or pipeline) an agent can clone or scaffold from. That field is **advisory only** — it never relaxes the promotion gate, which still runs through `evidence[]`; an agent may propose a candidate entry but a CODEOWNER confirms the URL and sets `last_verified`. A **capability** (`capabilities/<domain>/<slug>.md`) names a plain-language need and the proven-or-candidate patterns that fulfil it — the bridge a requirement crosses via `fulfils_capability: CAP-…`. See [`DESIGN.md`](DESIGN.md) for the full field shapes.

## Governance in one line

Advisory by construction: a human PR merge is the only act that ratifies anything (**propose → ratify**). Patterns and capabilities carry one structural human review — a CODEOWNERS architect must approve every change. No persisted scores, no per-person metrics.

See [`DESIGN.md`](DESIGN.md) for the architecture and [`CONTRIBUTING.md`](CONTRIBUTING.md) to author or PR a skill, pattern, or capability.
