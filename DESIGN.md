# DESIGN — SDLC Agentic Centre of Excellence

> The portable, GitHub-native reference library that lifts the proven SDLC *method* out of the retired
> `sdlc-companion` app and drops the heavyweight enforcement. The method is the asset; GitHub carries the
> mechanics; everything is **light and advisory by construction.**

---

## 1. Why this exists (the pivot)

We built `sdlc-companion`: a three-tier app (FastAPI + raw-SQL + React) that ran a divisional early-SDLC
method end to end — derive requirements from a business vision, red-team them, retrieve approved solution
patterns, review the design, convene a battle-test panel, author a sectioned solution architecture, then
plan phases/releases/waves. The **method** was strong. The **app** is not something the business will
support: it carries a bespoke relational substrate, a 9-state workflow machine, governance-disposition
gates, role-gated UAT, and a React shell — all of which need an owner, a deploy target, and a maintenance
budget nobody has signed up for.

So we **pivot, not patch.** We lift the load-bearing reasoning out into a library of portable **agent
skills** (markdown + YAML frontmatter, runnable in Claude Code or any LLM workflow that reads markdown),
and we replace every dropped *app mechanism* with a **GitHub primitive** — and nothing more.

### What we KEEP (the method)
The full de-enforced FORGE spine, end to end:

> Intake → Outcomes → Review (adversarial + exploratory) → Solution patterns (retrieval) → Solution options
> → Validation → Necessity check → Technical/design review (incl. WCAG/a11y) → NFRs → Convene/battle-test
> panel → Solution architecture (read the codebase, synthesise the doc in sections) → Phases/MVP/Pilot/
> Production → Releases (add/change/remove/patch) → Pattern-library promotion.

Plus the per-stage reasoning, carried **verbatim** from the on-disk prompts (the 9-kind requirements
red-team, the 6-category NFR coverage check, retrieval-not-generation pattern recommendation, pattern-NFR
propagation, the balanced 5-lens panel, the frozen-8 architecture sections, reconcile-as-proposals,
phases/releases/waves), and the cross-cutting disciplines (provider-agnostic fan-out, dismissal-memory,
preserve-dissent, projections-not-persisted, anti-fatigue guardrails).

### What we DROP (the enforcement)
The state machine (`STATE_ORDER`/`can_advance`/`_GATES`/409s, the 9 hard states, agent-work-state
lockouts); governance disposition + send-back + version-bound gating; the role-gated UAT gate;
HOLD/blocking on requirement rows; auto-ratify/auto-transition; the entire relational schema and raw-SQL
repo layer; FastAPI transport/RBAC/audit-log plumbing; the agent Protocol/dataclass seam; concrete
backends and the Databricks deploy target; embedding/vector machinery; and the React/UI shells. In their
place: **markdown files in git, reviewed by humans in PRs, with derived facts recomputed by Actions and
never persisted.**

### The two bets that make "no gates" safe
1. **THE TARGET RULE.** Every skill's agent output is exactly one of `proposal | question | menu | halt` —
   never a status, verdict, colour, ranking, score, feasibility, or disposition. Agents target the *model*,
   the *record*, or the *blind spot*, never the *judgment*. Because outputs structurally **cannot
   self-approve**, the library needs no enforcement gate. (FORGE principle VI.)
2. **THE TARGET RULE IS LINTABLE.** A single Action reads every skill/pattern frontmatter on PR and fails
   the *check* (advisory by default) if a skill declares an output kind outside the closed set, or a pattern
   carries an agent-set `approval_status`. That one lint is the spine of the whole light-governance posture.

---

## 2. The architecture in one picture

```
sdlc-agentic-coe/                  one git repo = the Centre of Excellence
├── skills/                        THE PRODUCT — 36 self-contained, copy-pastable SKILL.md folders
│   ├── 00-sdlc-spine/             umbrella TOC: orders the 14 stages, seeds a downstream Project
│   ├── _contract/                 cross-cutting authoring contract loaded first by every skill
│   ├── 01-intake-outcomes/ … 09-portfolio/   FORGE stages as numbered folders (method = organising principle)
│   ├── _shared/                   ONE canonical copy of each shared convention; skills QUOTE it (drift-guarded)
│   └── _scripts/                  plain validators/concatenators — Actions are just runners of these
├── patterns/                      the PR-reviewed component-pattern LIBRARY (one .md per pattern)
│   └── _schema/                   the frontmatter JSON Schema + closed NFR-kind enum (travels with the repo)
├── nfrs/                          the closed NFR vocabularies the skills cite
├── references/                    the other closed enums (challenge-kinds, frozen-8, panel roster, waves…)
├── projects/                      OPTIONAL per-engagement folder template (markdown SoT, adoption ledger)
├── generated/                     Action OUTPUT only — never hand-edited (combined bundles, computed tallies)
└── .github/                       the THIN GitHub-native control plane (Actions, templates, CODEOWNERS)
```

Three layers, deliberately separated:

- **The method layer (`skills/`, `patterns/`, `nfrs/`, `references/`).** Portable, provider-agnostic, runs
  in any markdown-reading LLM with zero GitHub dependency. The high-IP reasoning lives here.
- **The mechanics layer (`.github/`, `generated/`).** GitHub does three jobs and only three: **validate**
  frontmatter + target-rule on PR; **concatenate** related skills/patterns into combined files; **project**
  derived-on-read facts (pattern maturity, portfolio RAG) into `generated/` artifacts and the Projects
  board. No Action ever fails a build to block a downstream project.
- **The governance posture (the conventions).** PR review *is* the ratify. CODEOWNERS makes a human
  architect's review *structurally necessary* to merge a pattern (branch protection, not code). Everything
  else is advisory: a cue, a question, a checkbox — never a 409.

### Design principles, inherited and de-enforced
- **Accept-high / derive-low.** Humans accept the few commitments (outcomes, solution shape, contested
  calls); agents derive everything beneath, each item threaded by a `derives_from` **req_key citation**
  (a markdown link, not a foreign key). A rejected outcome visibly orphans its subtree.
- **Propose → ratify rhythm.** Human supplies → agent PROPOSES → human ratifies/edits/overrides → advance.
  In a portable skill the checkpoint is *advisory guidance* ("a human should confirm X"); the canonical
  GitHub encoding is **the human merges the PR**.
- **Projections, not persistence.** Rollups, RAG verdicts, release notes, maturity tallies are pure
  functions of live files/rows — recomputed on read or in an Action, never stored as a field that can rot.
  The "has this section gone stale?" question is answered by `git diff`/`blame`, not a snapshot column.
- **Provider-agnostic by construction.** Every skill names a deterministic no-LLM path (a checklist/regex/
  skeleton) plus a one-line model swap. No model ids in the library; tier hints only, mapped by the running
  harness. Fan-out = "launch one independent agent per persona/section/area in parallel."
- **Anti-fatigue guardrails are mechanical.** Delta-since-last-green; untouched = defer; dismissal-memory
  (re-arm only on changed evidence); and **no acceptance-rate / throughput / per-person metric anywhere.**

---

## 3. The skill catalogue (36 skills)

Each skill is a directory containing `SKILL.md` (YAML frontmatter + method body) and, where useful,
`references/` (closed vocabularies, schemas, few-shot examples). Numbered folders mirror the FORGE stages
so discovery follows the method.

### `00-sdlc-spine`
- **sdlc-spine** — umbrella/TOC: names and orders the 14 stages, points at one skill per stage, embeds the
  propose→ratify rhythm + the TARGET RULE as the contract every sibling obeys; its "seed a project" step
  emits `gh project create` + four phase columns so each downstream repo gets its OWN Project. Enforces
  nothing.

### `_contract` (loaded first by every skill)
- **target-rule-output-kinds** — the invariant + the spec the `validate-skill-frontmatter` Action enforces:
  output is only `proposal|question|menu|halt`; no agent-set `approval_status`; no verdict/score/colour.
- **propose-ratify-rhythm** — the human-disposes rhythm, accept-high/derive-low, the de-enforcement mapping
  (ratify = a human note / PR-merge, HOLD/blocking → detection-only, send-back/version-bound dropped).
- **llm-fanout-orchestrator** — the provider-agnostic `ModelBackend.complete()` seam + deterministic
  fallback + parallel `run_structured_many`; the rule every skill obeys; framework-free (no LangGraph/SDK).
- **explore-one-area-at-a-time** — the fan-out meta-method: domains as lenses over one graph (BDAT /
  crosscutting / lifecycle), one narrowly-chartered agent per surfaced area, ≤4 concurrent, rolled back into
  one source of truth by `section_key`.

### `01-intake-outcomes`
- **decompose-intake-to-outcomes** — front door: free-text vision → 3-6 business OUTCOMES (benefits not
  mechanisms) each with 1-3 derived F/NF requirements, G/W/T acceptance criteria, a `derives_from` trace.
- **classify-requirements** — annotate layer / stated_as (need|solution|constraint|symptom) / quantified /
  value_outcome + a need-shaped rewrite only when solution-shaped. Covers "assess the shape of requirements".
- **nfr-coverage-check** — assess the set against six canonical categories (security, availability,
  performance, data_residency, maintainability, scalability); propose one gap-fill NF per uncovered category.

### `02-review`
- **red-team-requirements** — the highest-value salvaged IP: one dismissible challenge per genuine issue
  over the closed 9-kind taxonomy; conservative on conflicting/gold_plated; conflicting names BOTH ids.
- **surface-risks-and-assumptions** — the light RAID register: surface the small load-bearing assumption
  set, deduped against the existing register (open AND closed); agent proposes `open`, human disposes.
- **enumerate-roadblocks** — a guardrail, not a gate: enumerate-and-CITE constraints that rule out options;
  no agent status; human disposes with advisory BLOCK/CAUTION/NOTE; dismissal-memory on re-run.

### `03-solution`
- **recommend-component-patterns** — retrieval not generation: read project context + the approved pattern
  files and recommend ONLY genuine fits or NONE; never invent keys; honest-empty routes to options.
- **surface-solution-options** — when retrieval finds no fit: 2-3 rival shapes side-by-side, "do nothing"
  always a column; menus not rankings; on success prompts "promote to pattern library?".
- **propagate-pattern-nfrs** — on adopt, place each attached NFR against the outcome it best serves and emit
  it as a derived NF requirement traced to its parent (or pattern-level); never drop/merge/reword/add.
- **validate-solution-vs-requirements** — replay every requirement against the solution's enforced
  constraints; surface friction as met|compromised|unmet (computed, never a model verdict); walk each
  compromise UP to the outcome it dents.
- **necessity-check** — anti-gold-plating tripwire: "necessary for WHICH outcome?" naming both ids; flag
  never verdict; zero cuts is a legitimate outcome.

### `04-review-and-panel`
- **design-review-findings** — the general review engine: severity-tagged ({high|medium|low|info}),
  citation-bearing FINDINGS over a built-in architecture checklist (RPO/RTO, encryption-at-rest, RBAC,
  topology, secret rotation, unclassified integrations); validation harness (clamp/default/drop).
- **frontend-a11y-review** — WCAG 2.2 AA specialisation: a11y findings each citing a fixed success criterion
  from the shipped ref list (WCAG-1.4.3-contrast, WCAG-2.1.1-keyboard, WCAG-4.1.2-name-role-value, …).
- **surface-open-decisions** — the genuinely open ADR-style decisions (kinds data_placement|architecture|
  integration|other, always ≥1 data_placement), 2-3 options each with an honest buy/cost/break note.
- **convene-a-panel** — flagship battle-test: balanced 5-lens roster (explorer+solution_designer+pragmatic_
  engineer vs skeptic+minimalist), 4-7 grounded questions, one parallel contribution per (persona,question),
  balance + honesty rules; a genuine split becomes a human-owned decision.
- **synthesise-panel** — cluster a transcript by node+signal into four proposal categories (gaps, value,
  alternatives, risks); an affirmative-vs-adversarial split is NOT auto-resolved.
- **red-team-and-dissent** — the single strongest objection per emerging proposal; a declined objection
  becomes a durable DISSENT ("what we decided NOT to do, and why") feeding dismissal-memory.

### `05-solution-architecture`
- **synthesise-solution-architecture** — read the codebase + outcomes/requirements/decisions and author the
  FROZEN-8 sections; assemble the graph slice once; each fact in exactly one section; honest reason line
  when thin; frozen order makes downstream reconcile deterministic.
- **reconcile-design-vs-requirements** — five checks (outcome-no-coverage; req-no-AC; nfr-unaddressed;
  orphaned-req; section-stale-via-git-blame) + a semantic pass; every finding a question; dismissal-memory.
- **import-external-design** — merge an externally authored design onto the frozen-8; preserve/integrate/
  dedupe; bucket the unmappable; per-section candidate-vs-current diff before adopting.
- **reconcile-as-built** — diff an as-built doc against design + requirements + AC; four neutral observation
  kinds (match/difference/addition/gap); a gap means "confirm whether dropped", never FAIL.

### `06-handoff`
- **scaffold-then-handoff** — the shared convention: deterministic fact-grounded spine FIRST (open-questions
  lead, honest "None flagged." fallback, fenced paste-ready prompt), THEN an optional LLM enrich pass that
  keeps every fact / invents no scope, falling back to the spine on error.
- **testing-brief-scaffold** — a test charter from outcomes→requirements→AC: one "PROVE: <criterion>" per
  AC, a deterministic-browser-testing approach block, a fenced prompt for a testing agent; scaffold not store.
- **design-studio-brief-scaffold** — a paste-ready design/branding brief for an external studio: a fixed
  white-label brand baseline reused as constraints; returned assets re-enter as references, not binaries.
- **comparator-grounded-estimate** — point + low/high range + confidence + basis_note citing only relied-on
  comparator ids; ships documentation-only (no fabricated numbers) until a real effort-actual table exists.

### `07-lifecycle`
- **describe-phases-releases-waves** — UAT-gated maturity PHASES (Prototype→MVP→Pilot→Production, light
  advisory checklist) then RELEASES (add/change/remove/patch deltas, each traced to one outcome, null-trace =
  scope-creep signal); deterministic release-notes projection grouped by change_kind.
- **help-implement-a-wave** — plan-and-govern a cutover as the six ordered wave_kinds (schema→data→cutover→
  config→validation→decommission), each with back-out PLAN + go/no-go CRITERIA; a runbook scaffold; never runs.
- **triage-backlog-and-defer** — park/size/prioritise/promote/decline-with-memory; promote = an "add"
  release delta carrying the same trace; decline is remembered against unchanged evidence.
- **scope-reconcile-check** — three advisory drift QUESTIONS over a release delta (scope_creep; dropped_
  requirement; breaks_outcome); never a blocking gate; dismissal-memory.

### `08-pattern-library`
- **author-component-pattern** — author ONE pattern as markdown with CI-validated frontmatter (the full v1
  field set below); seeded from the six existing patterns; writes the file, the PR review ratifies it.
- **pattern-library-curate** — maintain lifecycle health by READING what the Actions computed: maturity from
  the real adoption ledger (never assert), past-sunset/validity flags, supersede chains (never delete a
  pattern with adoptions), non-adoption/override reasons surfaced honestly.

### `09-portfolio`
- **portfolio-phase-health** — a per-project ADVISORY RAG verdict at PHASE granularity, derived-on-read:
  worst-of over a transparent named checklist with `reasons`; advisory facts ride alongside but don't drive
  v1; never a per-person/throughput metric; degrades safely.
- **advisory-governance-checklist** — the governance-LITE replacement for hard gates: prefill evidence
  against advisory LENSES (pattern_compliance/security/nfr/approval); review only the delta-since-last-green;
  untouched = defer; no disposition binding; no acceptance-rate metric.

---

## 4. The GitHub-native mechanics

GitHub is a **thin carrier** that maps 1:1 onto every dropped app mechanism — and adds nothing.

### 4.1 PR review IS the ratify
The canonical propose→ratify mechanic, library-wide. An agent opens a PR proposing markdown; a human
ratifies by **merging** it (or edits in-thread, or closes = halt). No enforced state, no 409. The PR
template links the relevant FORGE stage and carries *advisory* ratify checkboxes (informational, never
required-to-merge). PR/issue/commit history IS the audit log that replaces the dropped `insert_event` table.

### 4.2 CODEOWNERS routing (the one real human gate)
`patterns/**` → `@architects`; `skills/**` → `@coe-maintainers`; `.github/**` + `_schema/**` → `@platform`.
With branch protection requiring CODEOWNERS review, **a human architect's review is structurally necessary
to merge a pattern** — expressed as branch protection, not application code. This is the single hard gate in
the whole CoE; everything downstream stays advisory.

### 4.3 Actions — three jobs, only three
| Action | Trigger | Job |
|---|---|---|
| `validate-patterns` | PR touching `patterns/**` | schema-lint frontmatter (required vs conditionally-required fields), closed NFR-kind enum, date sanity, the never-delete-with-adoptions invariant. Advisory check; CODEOWNERS is the gate. |
| `validate-skill-frontmatter` (target-rule lint) | PR touching `skills/**` | every skill declares `output_kinds ⊆ {proposal,question,menu,halt}` and a `deterministic_fallback`; no agent-set `approval_status` (verified by blame); no forbidden output in the body. The spine of light governance. |
| `concat-patterns` | label `build:combined` / merge to main | concatenate related fragments into combined skill/pattern files in `generated/` (linguist-generated, never hand-edited): patterns-by-category, the adversarial-review bundle, the solution-design bundle. The brief's named "combine into a larger skill file" Action. |
| `pattern-lifecycle` | scheduled (weekly) | compute maturity from the real adoption tally; open a `pattern-revalidation` issue when validity comes due; flag past-sunset; verify no deprecated-with-adoptions pattern was deleted. Writes `generated/pattern-maturity.json`. |
| `portfolio-rollup` | scheduled / dispatch | recompute each downstream project's phase-level RAG (worst-of + reasons) → `generated/portfolio-rollup.json` + the org Project board. Pure projection. |
| `check-shared-stub-drift` | PR | diff each skill's quoted shared stub against the canonical `skills/_shared/` copy; fail if drifted. The mitigation for portability-duplication. |

Every Action is a thin runner of a plain script in `skills/_scripts/` — the **same script runs locally with
no GitHub**, so the validators travel with the repo. No Action ever blocks a downstream project's progress.

### 4.4 GitHub Projects — phase-level portfolio
Each DOWNSTREAM project gets its OWN GitHub Project, seeded by `sdlc-spine`, whose columns are the delivery
PHASES (**Prototype / MVP / Pilot / Production**) — never down to requirements (those live as markdown in the
downstream repo). An org-level Project rolls per-project phase + advisory RAG up for the practice-lead's
needs-attention view. The board is a render of derived-on-read facts pushed by `portfolio-rollup`, never a
stored truth.

### 4.5 Issue templates
`new-project-intake` (free-text vision → kicks off decompose-intake-to-outcomes); `new-pattern` (forces
evidence-of-built + intent + NFR kinds before a PR opens); `pattern-revalidation` (opened by the lifecycle
Action); `dissent-record` ("what we decided NOT to do, and why" as a first-class revisitable object).

---

## 5. The pattern lifecycle (PR-reviewed, dated, validity-checked, sunset/supersede)

A component pattern is **one markdown file** at `patterns/<category>/<pattern_key>.md` whose YAML
frontmatter is the schema. It moves through a lifecycle reviewed by humans and carried by GitHub mechanics,
with zero blocking state machine.

### 5.1 The v1 frontmatter field set
**REQUIRED (CI-enforced shape, human-gated value):** `pattern_key` (stable, cite-able, survives rename),
`name`, `category` (closed: `deployment|integration|data`), `intent` ("use WHEN … so that …"),
`deployment_topology`, `data_placement`, `summary`, `approval_status`
(`candidate|provisional|approved|deprecated`, **human-only — an agent may never set it**), `valid_from`
(date), `attached_nfrs[]` each `{kind` (from the closed enum below)`, statement, acceptance_criterion}`.

**CONDITIONALLY REQUIRED:** `approved_by` + `approved_at` + at least one `evidence[]` entry when
`approval_status ∈ {provisional, approved}`; `superseded_by` when `approval_status = deprecated`.

**OPTIONAL:** `validity_check_months` (default 12), `sunset_at` (date), `supersedes` (pattern_key),
`constraints[]` each `{statement, enforced: hard|soft}` ("adopt me, give this up").

**COMPUTED — never hand-written (Action-owned, lives in `generated/` not the file):** `maturity`
(battle-tested|emerging|experimental from the adoption count), `adoption_count`.

### 5.2 The closed NFR-kind vocabulary (the 11 values)
`security, availability, performance, data-residency, observability, resilience, cost, compliance,
scalability, data-governance, operations`. Promoted from the open-ended seed strings to a fixed list so
`propagate-pattern-nfrs` and `nfr-coverage-check` stay deterministic. Enforced by `validate-patterns`.

### 5.3 The loop: propose → validate → human-ratify → compute
1. **PROPOSE.** `author-component-pattern` (or a human) opens a `new-pattern` issue, then a PR adding one
   `.md` at `approval_status: candidate`. The PR template forces the author to confirm evidence-of-built is
   attached, `approval_status` was NOT set by an agent, `valid_from`/sunset/validity are set, and
   `supersedes` is named if this replaces an existing pattern.
2. **VALIDATE (CI, advisory).** `validate-patterns` checks SHAPE only. Non-required by policy so it never
   silently blocks — the human review is the gate.
3. **RATIFY (human, structural).** `patterns/**` is CODEOWNERS-routed to `@architects` with branch
   protection. **The merge is the ratification.** `approval_status: approved` + `approved_by`/`approved_at`
   are written in the same human-authored commit the architect merges (the lint asserts the agent never
   wrote them, verified by blame). A pattern with zero evidence can only ever be `candidate`.
4. **COMPUTE (Action, derived-on-read).** `pattern-lifecycle` computes maturity from the real adoption tally
   and never lets a human assert it; `concat-patterns` rebuilds the by-category combined file.

### 5.4 Validity / sunset / supersede
- `valid_from` + `validity_check_months` → the lifecycle Action opens a `pattern-revalidation` issue when
  the cadence elapses; revalidation is a human PR that bumps `valid_from` or moves status to `deprecated`.
- `sunset_at` → past this the Action flags the pattern and `recommend-component-patterns` is told to stop
  proposing it (advisory; the file is **not** deleted).
- `supersedes`/`superseded_by` → the bidirectional deprecation chain. **NEVER delete a pattern that has
  adoptions**; deprecate it and set `superseded_by` so historical citations never dangle.

### 5.5 Adoption provenance (computed, never asserted)
A downstream project adopting a pattern appends one line to `adoptions/ledger.jsonl` via a small PR:
`{pattern_key, repo, disposition (adopted-clean|adopted-with-overrides|overridden-out), at, override_reason?}`.
"Used in N engagements" is that tally; `overridden-out` rows are kept as honest non-adoption signal;
absent = adopted-by-0, shown honestly. The seeded **API-gateway/BFF override** is the worked example of
recording WHY a recommended pattern was declined.

---

## 6. How a team adopts this

1. **Read `00-sdlc-spine`** for the recommended flow, then reach for one skill at a time. The library is
   advisory; run as many or as few stages as the engagement needs.
2. **Start a downstream project.** Run `sdlc-spine`'s "seed a project" step to create that project's OWN
   GitHub Project with the four phase columns. Requirements and design live as markdown in the downstream
   repo — never on the portfolio board.
3. **Use a skill.** Paste a `SKILL.md` (or a `generated/` combined bundle) into your LLM workflow. Each
   skill has a deterministic no-LLM floor and a one-line model swap, so it produces a usable scaffold even
   with no model wired.
4. **Ratify by merging.** When the agent proposes markdown (outcomes, a design section, a release delta),
   review the delta and merge the PR. That merge is the only act that advances anything.
5. **Adopt patterns; record adoptions.** `recommend-component-patterns` reads the approved library and
   recommends genuine fits. On adopt, `propagate-pattern-nfrs` carries the pattern's NFRs in as derived
   requirements, and you append one line to the adoption ledger.
6. **Contribute a pattern.** When an engagement builds something reusable, open a `new-pattern` issue with
   evidence-of-built, then a PR. An architect reviews and merges; the merge ratifies it.

A team can also **copy a single skill folder out of the repo** and run it standalone — the schema and
vocabularies travel with the skill. Outside the CoE the GitHub-native steps degrade to manual instructions
(each is marked "GitHub-native mechanic (optional)"), but the *method* survives extraction intact.

---

## 7. Resolved open questions (stated defaults)

These were genuinely open across the three proposals; the lead-architect calls, taken so the library is
coherent rather than asking:

1. **Pattern frontmatter is the rich shape** (§5.1), reconciling the built thin shape with the designed
   lifecycle metadata. NFR `kind` is a **closed 11-value list** (§5.2).
2. **Canonical ratify mechanic = PR-merge**, library-wide. One consistent "a human always disposes" posture.
3. **Combined-bundle Actions** target adversarial-review (red-team-requirements + design-review-findings +
   red-team-and-dissent), solution-design (the frozen-8 section authoring), and patterns-by-category;
   trigger = on-merge for category bundles, on-label for the review/design bundles.
4. **Adoption tally** = a central append-only `adoptions/ledger.jsonl`, tallied by the scheduled
   `pattern-lifecycle` Action (honest-but-manual). An org-repo scan is a deferred upgrade.
5. **`comparator-grounded-estimate` ships documentation-only** (no fabricated numbers) until the org seeds a
   real effort-actual comparator dataset.
6. **`frontend-a11y-review` targets WCAG 2.2 AA** with a fixed, citable success-criterion ref list.
7. **`suggested_tier` is an optional soft hint** in frontmatter; no concrete model-ids in the portable
   library — the running harness maps tier → id.
8. **Cross-PROJECT / cross-pattern overlap is OUT of v1.** The red-team `conflicting` kind covers
   within-project requirement conflict; cross-project overlap has no built equivalent to salvage and is
   flagged as the clearest scope gap for a later call.

---

## 8. Honest trade-offs

- **PR-is-ratify is a slightly forced fit for in-session iteration.** A designer iterating on outcomes
  doesn't want a PR per micro-edit. Mitigation: intra-session work happens in the working branch with no
  ceremony; the PR-merge ratifies a *logical unit*. The "human always disposes" guarantee is a convention
  enforced by review culture, not by code — weaker than the old state machine, by deliberate choice.
- **Advisory CI keeps the library light but a malformed pattern can be merged if a reviewer ignores a red
  check.** Hardening the checks to required would reintroduce a hard gate. We keep them advisory and lean on
  CODEOWNERS for patterns; the owner may flip `validate-patterns` to required for `patterns/**` only.
- **Maturity depends on downstream projects actually appending their adoption line.** If they don't, the
  tally under-counts. The org-repo scan upgrade needs org-wide tokens and is deferred.
- **No vector index** — `recommend-component-patterns` lets the LLM read pattern files directly. Fine for
  ~6-30 patterns; a known ceiling that needs a build-an-index Action at hundreds.
- **Duplication is the price of zero-dependency portability.** Shared conventions are quoted into each
  skill, not imported; `check-shared-stub-drift` guards the in-repo copies, but a skill copied *out* of the
  repo loses that guard.
- **Library surface area is large (36 skills).** The numbered-stage folders + the spine mitigate discovery
  cost; a "core 10" subset could be marked for a lighter first adoption.
