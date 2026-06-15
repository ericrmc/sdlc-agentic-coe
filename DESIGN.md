# DESIGN — SDLC Agentic Centre of Excellence

A portable, GitHub-native library of advisory agent skills plus a PR-reviewed pattern and capability library,
covering early SDLC from a raw intake to a delivery plan. Every skill is self-contained markdown: an agent runs
it in any LLM workflow that reads markdown, with zero repo dependency.

Read this as the agent who authors and runs this material: you populate the patterns, capabilities, and skill
edits and open the PR; the human reviews and ratifies by merging. Front doors: **ENTRYPOINT.md** (the thin
pointer naming the two `meta/` skills — `meta/navigator` to USE the library, `meta/author-a-skill` to extend it),
**GETTING-STARTED.md** (persona table + fast end-to-end pass), **skills/MAP.md** (category table + end-to-end
flow), **capabilities/INDEX.md** (need-first lookup).

---

## 1. Layers

| Layer | Holds | Property |
|---|---|---|
| Method | `skills/`, `patterns/`, `capabilities/`, `nfrs/`, `references/` | Provider-agnostic markdown; the high-IP reasoning. |
| Mechanics | `.github/`, `generated/`, `skills/_scripts/` | GitHub does three jobs only: validate frontmatter on PR, concatenate related files into bundles, project derived-on-read facts. Each Action is a thin runner of a script that also runs locally. |
| Governance | conventions | A PR merge is the only ratify. CODEOWNERS makes a human architect's review structurally required to merge a pattern or capability. Everything else is advisory. |

```
sdlc-agentic-coe/
├── skills/                 the product — self-contained SKILL.md folders, grouped by category
│   ├── MAP.md              the index (category table + end-to-end flow + project-seed bash)
│   ├── _contract/          authoring conventions every skill obeys
│   ├── _shared/            one canonical copy of each shared convention; skills quote it (drift-guarded)
│   └── _scripts/           plain validators/concatenators the Actions run
├── patterns/               PR-reviewed component patterns (one .md each) + _schema/
├── capabilities/           PR-reviewed needs that bridge requirements → patterns + _schema/ + INDEX.md
├── nfrs/ references/       closed vocabularies the skills cite
├── projects/               optional per-engagement folder template (markdown SoT + adoption ledger)
├── docs/                   operating notes (portfolio-github-projects.md, etc.)
├── generated/              Action output only — never hand-edit
└── .github/                Actions, issue templates, CODEOWNERS
```

---

## 2. Core invariants

Hold these when you author or run anything here.

| Invariant | Statement |
|---|---|
| Four output kinds | Every output is exactly one of `proposal \| question \| menu \| halt` — never a status, verdict, score, colour, ranking, or disposition. Outputs cannot self-approve, so the library needs no enforcement. |
| Propose → ratify | Human supplies → agent proposes → human ratifies/edits/overrides. The only ratify act is a human merging the PR. |
| Deterministic base + model step | Every skill names a no-LLM path (checklist/regex/skeleton) plus a one-line model swap, so it produces a usable scaffold with no model wired. |
| Accept-high / derive-low | Humans accept the few commitments (outcomes, solution shape, contested calls); agents derive everything beneath, each item threaded by a `derives_from` key citation (a markdown link). A rejected outcome visibly orphans its subtree. |
| Projections, not persistence | Rollups, RAG verdicts, release notes, maturity tallies are recomputed on read or in an Action, never stored as a field that can rot. "Is this section stale?" is answered by `git diff`/`blame`. |
| Provider-agnostic tiers | No model ids anywhere; `suggested_tier` carries `frontier \| mid \| light` only, mapped by the running harness. |
| Anti-fatigue | Delta-since-last-green; untouched = defer; dismissal-memory re-arms only on changed evidence; no acceptance-rate / throughput / per-person metric anywhere. |

The target-rule lint enforces invariant 1 on PR (advisory): a skill declaring an output kind outside the
closed set, or a pattern carrying an agent-set `approval_status`, fails the check.

---

## 3. The eight categories

| Category | Purpose | Skills |
|---|---|---|
| **ingest** | Read an external source into staged requirements: fingerprint each row, propose on first read, diff on re-read. | ingest-source-to-requirements · stage-and-fingerprint · reingest-delta |
| **understand** | Structure a raw intake into outcomes, derived requirements, NFR coverage, and the capability each requirement fulfils. | decompose-intake-to-outcomes · classify-requirements · nfr-coverage-check · derive-capabilities |
| **challenge** | Adversarially pressure-test a requirement set. | red-team-requirements · surface-risks-and-assumptions · enumerate-roadblocks · necessity-check |
| **architect** | Choose a solution shape and author the design. | recommend-component-patterns · surface-solution-options · propagate-pattern-nfrs · validate-solution-vs-requirements · surface-open-decisions · synthesise-solution-architecture · reconcile-design-vs-requirements · import-external-design · reconcile-as-built |
| **panel** | Multi-voice deliberation and review. | convene-a-panel · synthesise-panel · red-team-and-dissent · design-review-findings · frontend-a11y-review |
| **deliver** | Plan the delivery lifecycle and hand off the build. | intake-feature-change · describe-phases-releases-waves · help-implement-a-wave · triage-backlog-and-defer · scope-reconcile-check · scaffold-then-handoff · testing-brief-scaffold · build-agent-brief-scaffold · design-studio-brief-scaffold · comparator-grounded-estimate |
| **library** | Author and curate the reusable assets; see the portfolio. | author-component-pattern · author-capability · pattern-library-curate · portfolio-phase-health · advisory-governance-checklist |
| **meta** | Skills about using and extending the library — the front door, not a stage. | navigator · author-a-skill |

`skills/MAP.md` shows these as a category table and an end-to-end flow (ingest → understand → challenge →
architect → panel → deliver, with library as a side-store and capabilities as the requirements→components
bridge): a map, not a track. **meta** sits outside that line: `meta/navigator` is how an agent *enters* the flow
(it asks what you want and walks the engagement one stage at a time, routing only to skills that exist on disk
and halting between stages for the human to ratify — its deterministic fallback is the GETTING-STARTED persona
table plus the MAP category table); `meta/author-a-skill` is the off-ramp for contributing a new skill, pattern,
or capability. `ENTRYPOINT.md` (repo root) is the thin pointer naming both. Conventions live in
`skills/_contract/` (target-rule-output-kinds · propose-ratify-rhythm · explore-one-area-at-a-time ·
parallel-agents · grounding-no-absent-input).

---

## 4. Automation (GitHub Actions)

You author a pattern, capability, or skill change and open a PR; the pipeline validates it and posts a pass/fail
summary the reviewer reads. Before opening the PR, run the matching `skills/_scripts/` script locally and paste
the result. Everything below is advisory — no Action blocks a merge; CODEOWNERS is the only structural gate.

| Action | Trigger | What it does for you |
|---|---|---|
| `validate-patterns` | PR touching `patterns/**` | Lints pattern frontmatter against `patterns/_schema/`; sticky PR comment lists any field left wrong or missing. |
| `validate-capabilities` | PR touching `capabilities/**` | Lints capability frontmatter (need-statement, ≥2 aliases, governance NFRs over the closed 11 kinds, fulfilment confidence) so a candidate enters clean. |
| `validate-skill-frontmatter` | PR touching `skills/**`, `patterns/**`, `capabilities/**`, `references/**` | Target-rule lint (no output kind outside the closed four; no agent-set `approval_status`, verified by blame) plus map-link, references, and capability-index checks. |
| `concat-patterns` | push to `main`; PR labelled `build:combined` | Combines related patterns and skills into `generated/` bundles so an agent loads one file instead of many. On a labelled PR it uploads the bundle as an artefact; on `main` it commits the rebuilt bundles. |
| `pattern-lifecycle` | weekly schedule; on demand | Recomputes `maturity` and `adoption_count` from the adoption ledger, opens revalidation issues when `validity_check_months` elapses, flags pattern past `sunset_at`. Never deletes a pattern that has adoptions. |
| `portfolio-rollup` | weekday schedule; on demand | Writes an advisory RAG verdict + `Reasons` per project to the org Project board (`docs/portfolio-github-projects.md`). Recomputed each run; the cell caches a derived value, never a stored score. |
| `check-shared-stub-drift` | PR touching `skills/**` | Flags when a quoted `skills/_shared/` convention drifted from its canonical copy. |

Each Action runs a thin step over a script in `skills/_scripts/` (`lint_pattern_frontmatter.py`,
`lint_skill_target_rule.py`, `lint_map_links.py`, `lint_skill_references.py`, `concat_skills.py`). Run any of
them locally to self-check before the PR.

---

## 5. Multi-agent option

Ten reasoning-heavy skills carry an advisory note: deepen the step by launching one sub-agent per
persona / section / objection / candidate, at most 4 concurrent, each independent. A failed sub-agent
returns nothing and is never fatal — the deterministic base stands, merge what succeeded. The convention is
defined once in `skills/_contract/parallel-agents` (one model seam with a tier hint, parallel calls capped at
4) and quoted from a drift-guarded `skills/_shared/` stub. Never required; it adds coverage and cuts
single-pass bias.

---

## 6. Pattern lifecycle

A pattern is one markdown file at `patterns/<category>/<pattern_key>.md`; its YAML frontmatter is the schema.

| Field group | Fields |
|---|---|
| Required | `pattern_key` (stable, cite-able), `name`, `category` (`deployment\|integration\|data`), `intent` ("use WHEN … so that …"), `deployment_topology`, `data_placement`, `summary`, `approval_status` (`candidate\|provisional\|approved\|deprecated`, **human-only**), `valid_from`, `attached_nfrs[]` each `{kind, statement, acceptance_criterion}` |
| Conditional | `approved_by` + `approved_at` + ≥1 `evidence[]` `{title,url}` when status ∈ {provisional, approved}; `superseded_by` when deprecated |
| Optional | `validity_check_months` (default 12), `sunset_at`, `supersedes`, `constraints[]` `{statement, enforced: hard\|soft}`, `fulfils: [CAP-…]` back-ref, `reference_implementations[]` `{kind: iac\|app\|notebook\|scaffold\|module\|pipeline, url, provisions, repo_path?, scaffold_cmd?, last_verified?, notes?}` — a forward pointer to a working artefact an agent clones/scaffolds from |
| Computed (Action-owned, in `generated/`, never hand-write) | `maturity` (battle-tested\|emerging\|experimental from adoption count), `adoption_count` |

Closed NFR kinds (11): `security, availability, performance, data-residency, observability, resilience,
cost, compliance, scalability, data-governance, operations`. Shared by patterns and capabilities.

**`reference_implementations[]` vs `evidence[]`** — they answer different questions. `evidence[]` is
retrospective ("was this BUILT?") and is REQUIRED from `provisional` up; it is the only thing the promotion
gate reads. `reference_implementations[]` is a forward pointer ("what working artefact do I clone or scaffold
from?") and is **advisory only** — additive, optional, validates without it, and **never relaxes the gate**. A
reference implementation that *is* a real build is also listed under `evidence` (and *that* entry promotes the
pattern, through the existing door — zero new gate logic). An agent may propose a candidate entry but never
blesses one: a CODEOWNER confirms the URL and sets `last_verified`. `lint_pattern_frontmatter.py` validates the
`kind` enum and an advisory `last_verified` staleness note, and adds nothing to the promotion rules.

**Loop:** propose (`new-pattern` issue → PR at `candidate`) → validate (advisory schema lint) → ratify (a human
architect merges via CODEOWNERS branch protection; `approval_status: approved` is written in the human commit,
verified by blame) → compute (Action tallies maturity). Leave `approval_status: candidate` when you author —
the reviewer moves it; you never set it.

**Validity / sunset / supersede.** `valid_from` + `validity_check_months` open a `pattern-revalidation` issue when
the cadence elapses. Past `sunset_at` the pattern is flagged and `recommend-component-patterns` stops proposing
it. Never delete a pattern with adoptions: deprecate and set `superseded_by` so citations never dangle.

**Adoption provenance.** A downstream project appends one line to `adoptions/ledger.jsonl`:
`{pattern_key, repo, disposition (adopted-clean\|adopted-with-overrides\|overridden-out), at, override_reason?}`.
"Used in N engagements" is that tally; absent = adopted-by-0, shown honestly.

---

## 7. Capability lifecycle (the requirements → components bridge)

A capability is one markdown file at `capabilities/<domain>/<slug>.md` naming a need in plain language. It is
the named middle term: `OUTCOME ← requirement (fulfils_capability: CAP-…) ← capability (fulfilled_by: PAT-…) ← pattern`.

| Field group | Fields |
|---|---|
| Required | `capability_key` (`^CAP-`), `name`, `capability_domain` (`data\|compute\|integration\|runtime\|experience\|governance`), `summary`, `need_statement` (technology-free, "a system needs … so that …"), `aliases[]` (≥2 lay synonyms — feed `INDEX.md`), `governance_nfrs[]` (the floor any fulfilling pattern must meet, over the closed 11 kinds), `approval_status`, `valid_from` |
| Conditional / optional | `approved_by`, `approved_at`, `superseded_by`, `validity_check_months`, `fulfilled_by[]` |
| `fulfilled_by[]` entry | `{pattern_key, confidence (proven\|candidate), note, evidence?:[{title,url}], open_questions?:[…]}` — `pattern_key` required when `confidence: proven`, optional when `candidate` |

**Proven vs candidate** lives entirely in `fulfilled_by[].confidence`: a proven fulfilment carries build
evidence; a candidate carries the spike questions that gate promotion. Promotion candidate → proven is a human
PR that attaches evidence and flips confidence — you never flip it. Author through the `new-capability` issue
form → candidate PR → CODEOWNERS architect promotes; `capabilities/INDEX.md` is the alias-searchable lookup
whose linter fails advisory if an alias is missing or an entry points at a missing key.

| Seed | Domain | Fulfilment |
|---|---|---|
| CAP-OLAP (analytical/BI store) | data | `PAT-LAKEHOUSE-DELTA` — proven (NFRs meet the governance floor) |
| CAP-OLTP (transactional system-of-record) | data | `PAT-WEBAPP-PG` — proven (managed-Postgres tier); Lakebase recorded as a future candidate |
| CAP-AGENT-RUNTIME (host LLM agents in prod) | runtime | candidate-only: AWS AgentCore, Databricks Agent Bricks, Microsoft Foundry — spikes owed |

---

## 8. Model tiers + per-skill frontmatter

| Tier | When |
|---|---|
| `frontier` | High-stakes synthesis or adversarial judgement that shapes a human commitment (red-team-requirements, recommend-component-patterns, synthesise-solution-architecture). |
| `mid` | One bounded structured pass over given facts (classify, propagate, scaffold, reconcile a single dimension). |
| `light` | Mechanical / navigational / templating only (MAP.md, the `_contract` convention docs). |

Each skill carries `suggested_tier` + a one-line `tier_reason`; the harness maps the tier to a model, and you
may override to a cheaper tier any time. Per-skill frontmatter also carries: `one_liner` (≤12 words, cold-reader
purpose) · `aliases` (synonyms for findability) · `output_kinds` (⊆ the closed four) · `deterministic_fallback` ·
`neighbours` (2-line before/after linkage so a copied-out skill keeps its place) · `audience` (the role it serves).

---

## 9. Honest trade-offs

- **PR-is-ratify is a forced fit for in-session iteration.** Intra-session work happens on the working branch
  with no ceremony; the merge ratifies a logical unit. "A human always disposes" is review culture, not code.
- **Advisory CI can let a malformed pattern merge if a reviewer ignores a red check.** CODEOWNERS is the backstop
  for patterns/capabilities; `validate-patterns` may be flipped to required for `patterns/**` only.
- **Maturity depends on downstream projects appending their adoption line.** If they don't, the tally
  under-counts; an org-repo scan upgrade is deferred.
- **No vector index** — skills read pattern/capability files directly. Fine for tens of files; a known ceiling
  that needs an index Action at hundreds.
- **Duplication is the price of zero-dependency portability.** Shared conventions are quoted into each skill;
  `check-shared-stub-drift` guards in-repo copies, but a skill copied out loses that guard.
- **Large surface area.** The category map, the `GETTING-STARTED.md` persona table, and `meta/navigator` (which
  reads both and walks an engagement stage by stage) mitigate discovery cost; a "core 10" subset could be marked
  for a lighter first adoption.
