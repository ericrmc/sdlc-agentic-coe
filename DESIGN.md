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
| Four output kinds | Every output is exactly one of `proposal \| question \| menu \| halt` — never a status, verdict, score, colour, ranking, or disposition. |
| Propose → ratify | Human supplies → agent proposes → human ratifies/edits/overrides. The only ratify act is a human merging the PR. |
| Deterministic base + model step | Every skill names a no-LLM path (checklist/regex/skeleton) plus a one-line model swap. |
| Accept-high / derive-low | Humans accept the few commitments (outcomes, solution shape, contested calls); agents derive everything beneath, each item threaded by a `derives_from` key citation (a markdown link). A rejected outcome visibly orphans its subtree. |
| Projections, not persistence | Rollups, RAG verdicts, release notes, maturity tallies are recomputed on read or in an Action, never stored as a field that can rot. |
| Provider-agnostic tiers | No model ids anywhere; `suggested_tier` carries `frontier \| mid \| light` only, mapped by the running harness. |
| Anti-fatigue | Delta-since-last-green; untouched = defer; dismissal-memory re-arms only on changed evidence; no acceptance-rate / throughput / per-person metric anywhere. |

The target-rule lint enforces invariant 1 on PR (advisory): a skill declaring an output kind outside the
closed set, or a pattern carrying an agent-set `approval_status`, fails the check. RATIONALE.md §2 records why
each invariant is load-bearing; ADR.md holds the per-decision record.

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
(see its SKILL and GETTING-STARTED.md for the behaviour; its deterministic fallback is the GETTING-STARTED
persona table plus the MAP category table); `meta/author-a-skill` is the off-ramp for contributing a new skill,
pattern, or capability. `ENTRYPOINT.md` (repo root) is the thin pointer naming both. Conventions live in
`skills/_contract/` (target-rule-output-kinds · propose-ratify-rhythm · explore-one-area-at-a-time ·
parallel-agents · grounding-no-absent-input).

---

## 4. Automation (GitHub Actions)

The seven Actions, their triggers, and what each does are tabled in [README.md](README.md#automation-github-actions);
everything is advisory and CODEOWNERS is the only structural gate. The architecture-relevant fact: each Action is
a thin runner of a script in `skills/_scripts/` (`lint_pattern_frontmatter.py`, `lint_skill_target_rule.py`,
`lint_map_links.py`, `lint_skill_references.py`, `concat_skills.py`) — run any locally to self-check before the PR.

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

**`reference_implementations[]` vs `evidence[]`** — `evidence[]` is retrospective ("was this BUILT?"), REQUIRED
from `provisional` up, and the only thing the promotion gate reads; `reference_implementations[]` is an advisory
forward pointer ("what artefact do I clone or scaffold from?") that never relaxes the gate (an agent proposes a
candidate entry, a CODEOWNER confirms the URL). The full distinction is on the schema's
`reference_implementations` field description; ADR-0014 records why it stays out of the gate.

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

[RATIONALE.md §5](RATIONALE.md) holds these in full with their ADR pointers. In brief:

- PR-is-ratify is a forced fit for in-session iteration (§2.2, ADR-0004).
- Advisory CI can let a malformed pattern merge past an ignored red check; CODEOWNERS is the backstop (§2.3, ADR-0002).
- Computed maturity under-counts if downstream projects don't append their adoption line; an org-repo scan is deferred (ADR-0013).
- No vector index — fine for tens of files, a known ceiling at hundreds.
- Duplication is the price of zero-dependency portability; `check-shared-stub-drift` guards in-repo copies only (ADR-0010).
- Large surface area, mitigated by the map + persona table + `meta/navigator`, not eliminated.
