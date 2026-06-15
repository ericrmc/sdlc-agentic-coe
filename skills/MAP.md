---
name: map
description: The index for the whole skill library — a category table of every skill with its one-line purpose and model tier, an end-to-end flow showing how the categories link, and a deterministic snippet to seed a downstream project's GitHub Project. Start here when unsure where to begin.
when_to_use: starting any engagement, or deciding which skill to reach for next
output_kinds: [menu]
one_liner: The index of every skill, the flow that links them, and a project seed.
aliases: [index, table of contents, where do I start, list of skills, library map, skill catalogue, navigation, what skills are there]
deterministic_fallback: the static category table + the gh project create snippet
suggested_tier: light
tier_reason: pure navigation plus a deterministic bash seed; no weighing
---

# Skill library — map

The index for the whole library. Two views below: a **category table** of every skill, and an **end-to-end flow** showing how the categories link. Read either; deleting this file breaks no skill — every skill stands alone and runs on its own.

New here? Start with [`GETTING-STARTED.md`](../GETTING-STARTED.md). Know the *need* but not the technology ("a data warehouse", "somewhere to run agents in production")? Go straight to [`capabilities/INDEX.md`](../capabilities/INDEX.md) — the need-first lookup that resolves a plain-language need to a proven component or the spikes still owed.

**Tier hints** are provider-agnostic: `frontier` (high-stakes synthesis and adversarial judgement), `mid` (one bounded structured pass), `light` (mechanical or navigational only). Map each to your own model; override with a cheaper tier any time.

---

## View 1 — category table

Eight categories. Each row is `category/skill — purpose — tier`. If you know your category, jump straight to its `SKILL.md`.

> **New here, or want to be walked through an engagement?** [`ENTRYPOINT.md`](../ENTRYPOINT.md) is the front door — it names the two `meta/` skills below: `meta/navigator` (USE the library, be walked stage by stage) and `meta/author-a-skill` (CONTRIBUTE to it). This table is the navigator's deterministic fallback — read it directly any time.

### Ingest — lift a structured-but-messy source into traceable requirement markdown (feeds understand)

| Skill | Purpose | Tier |
|---|---|---|
| `ingest/ingest-source-to-requirements` | Turn a structured-but-messy source into traceable requirement markdown — or HALT for the source, never invent it. | frontier |
| `ingest/stage-and-fingerprint` | Vault the original byte-untouched, fingerprint it, and propose whether it is new or a new version. | light |
| `ingest/reingest-delta` | Re-read a staged source, diff against the prior version, and surface only what changed — never silently overwrite. | mid |

### Understand — structure a raw ask into outcomes, requirements, and NFR coverage

| Skill | Purpose | Tier |
|---|---|---|
| `understand/decompose-intake-to-outcomes` | Turn raw intake text into traceable outcomes and requirements. | frontier |
| `understand/classify-requirements` | Tag each requirement's shape to surface solutioneering and unmeasurability. | mid |
| `understand/nfr-coverage-check` | Check a requirement set for gaps across six canonical NFR categories. | mid |
| `understand/derive-capabilities` | Tag each requirement with the capability it fulfils (`fulfils_capability: CAP-…`); route genuinely new needs to author-capability. | mid |

### Challenge — adversarially pressure-test a requirement set

| Skill | Purpose | Tier |
|---|---|---|
| `challenge/red-team-requirements` | Pressure-test a requirement set for conflicts, gaps, and gold-plating. | frontier |
| `challenge/surface-risks-and-assumptions` | Name the load-bearing bets a plan depends on. | mid |
| `challenge/enumerate-roadblocks` | Cite the constraints that rule out specific design or decision options. | mid |
| `challenge/necessity-check` | Ask whether a proposed component earns its keep against a named outcome. | mid |

### Architect — choose a solution shape and author the design

| Skill | Purpose | Tier |
|---|---|---|
| `architect/recommend-component-patterns` | Match project needs to proven library patterns, or honestly none. | frontier |
| `architect/surface-solution-options` | Lay rival solution shapes side by side when no pattern fits. | frontier |
| `architect/propagate-pattern-nfrs` | Trace an adopted pattern's NFRs onto the outcomes they serve. | mid |
| `architect/validate-solution-vs-requirements` | Replay requirements against a solution's constraints; surface the friction. | frontier |
| `architect/surface-open-decisions` | List the contested architecture calls a human must decide. | frontier |
| `architect/synthesise-solution-architecture` | Author the durable solution-design doc as eight fixed sections. | frontier |
| `architect/reconcile-design-vs-requirements` | Find where a design doc has drifted from its requirements. | frontier |
| `architect/import-external-design` | Merge an externally-authored design onto the fixed canonical sections. | frontier |
| `architect/reconcile-as-built` | Diff what was built against what was designed; flag divergences. | mid |

### Panel — multi-voice deliberation and review

| Skill | Purpose | Tier |
|---|---|---|
| `panel/convene-a-panel` | Battle-test a design with a balanced affirmative-plus-adversarial panel. | frontier |
| `panel/synthesise-panel` | Cluster a deliberation transcript into four proposal categories. | mid |
| `panel/red-team-and-dissent` | Raise the strongest objection per proposal; record declined ones as durable dissent. | frontier |
| `panel/design-review-findings` | Emit severity-tagged, cited findings over a design draft. | frontier |
| `panel/frontend-a11y-review` | Accessibility-review a UI against WCAG 2.2 AA, citing fixed criteria. | frontier |

### Deliver — plan the lifecycle and hand off the build

| Skill | Purpose | Tier |
|---|---|---|
| `deliver/intake-feature-change` | Front door for a feature on a project that already exists — ground the ask in the real requirements AND the real code, or HALT. | frontier |
| `deliver/describe-phases-releases-waves` | Plan a project's maturity phases and traced release stream. | frontier |
| `deliver/help-implement-a-wave` | Plan a migration cutover as six governed waves with back-out and go/no-go. | frontier |
| `deliver/triage-backlog-and-defer` | Park a raw backlog as traced, sized, prioritised items. | mid |
| `deliver/scope-reconcile-check` | Surface scope-drift questions over a proposed release delta. | mid |
| `deliver/scaffold-then-handoff` | Scaffold a fact-grounded handoff brief, then optionally enrich it. | mid |
| `deliver/testing-brief-scaffold` | Generate a traceable, paste-ready testing handoff brief. | mid |
| `deliver/build-agent-brief-scaffold` | Assemble a paste-ready build prompt for a downstream developer agent from a grounded feature analysis. | mid |
| `deliver/design-studio-brief-scaffold` | Assemble a paste-ready design and branding brief for an external studio. | mid |
| `deliver/comparator-grounded-estimate` | Size effort against confirmed past projects, never from guesswork. | mid |

### Library — author and curate the reusable assets, and see the portfolio

| Skill | Purpose | Tier |
|---|---|---|
| `library/author-component-pattern` | Capture one proven solution shape as a library pattern file. | frontier |
| `library/author-capability` | Name a need and its proven-or-candidate fulfilments as a library file. | frontier |
| `library/pattern-library-curate` | Keep the pattern shelf healthy by reading computed facts. | mid |
| `library/portfolio-phase-health` | Derived-on-read advisory RAG health per project phase. | mid |
| `library/advisory-governance-checklist` | Cited evidence against four advisory review lenses; a human reads only the delta. | mid |

### Meta — skills about using and extending the library (the front door)

| Skill | Purpose | Tier |
|---|---|---|
| `meta/navigator` | The library's front door for USING it — ask what you want, then walk the engagement one stage at a time, routing only to skills that exist. | light |
| `meta/author-a-skill` | The front door for CONTRIBUTING — classify a contribution (skill \| pattern \| capability), scaffold a SKILL.md or route to the right authoring skill. | mid |

> **`ENTRYPOINT.md`** (repo root) is the thin pointer that names these two `meta/` skills. `meta/navigator`'s deterministic fallback is this category table plus the `GETTING-STARTED.md` persona table — it reads them, never replaces them.

> **Conventions (cross-cutting, under `skills/_contract/`).** Every skill obeys two rules: every output is one of exactly four kinds — **proposal, question, menu, or halt** (`_contract/target-rule-output-kinds`), and the rhythm is **propose → ratify**: an agent proposes, a human ratifies by merging the PR (`_contract/propose-ratify-rhythm`). The no-fabrication keystone — an absent/unreadable/empty **required** input becomes a **HALT** that asks where it is, never an invented hypothetical — is `_contract/grounding-no-absent-input` (it carries the library's canonical HALT exemplar). Multi-call skills reuse one provider-agnostic convention for fan-out (`_contract/parallel-agents`) and one for scoping it (`_contract/explore-one-area-at-a-time`).

---

## View 2 — end-to-end flow

**This is a map, not a track — enter at any node, loop back freely.** The arrows show the order delivery usually wants, not a sequence anything enforces.

```
   ingest ──► understand ──► challenge ──► architect ──► panel ──► deliver
  (lift a     (outcomes &    (pressure-    (choose a     (battle-  (lifecycle
   messy       requirements)  test them)    shape &       test it)  & handoff)
   source)         │                        author the      ▲          │
                   │                        design) ────────┘          │
                   │                          ▲   │                     │
                   │           capabilities   │   │ reads patterns      │ writes
                   └─ requirement ──► CAP ────┘   ▼ & capabilities      ▼ patterns
                       (fulfils_capability)   ┌─────────────────────────────┐
                                              │   library  (side-store)      │
                                              │  patterns + capabilities +   │
                                              │  portfolio health            │
                                              └─────────────────────────────┘
```

- **ingest → understand** is the optional front door when requirements already live somewhere structured-but-messy (a spreadsheet, a ticket board, a docs folder, an export). `ingest` lifts that source into traceable requirement markdown — or HALTs for it, never invents — and hands the result to `understand`. Skip it when the ask arrives as free text (go straight to `understand/decompose-intake-to-outcomes`).
- **understand → challenge → architect → panel → deliver** is the main path. Loop back at will: a panel can re-open outcomes; a release can re-enter the whole front half under a new direction.
- **library is a side-store**, not a stage in the line. `architect` *reads* it (proven patterns and capabilities), `deliver` *writes* to it (promoting a shape worth reusing). It also holds the portfolio health view that sits *across* projects.
- **capabilities are the bridge** from a requirement to a component. A requirement in `understand` cites the capability it fulfils (`fulfils_capability: CAP-…`, emitted by `understand/derive-capabilities`); the capability names which proven pattern (a component in `library`) fulfils it, or the candidates and spikes still owed. This is why a need-first reader starts at [`capabilities/INDEX.md`](../capabilities/INDEX.md).
- **meta is the entry, not a stage.** [`ENTRYPOINT.md`](../ENTRYPOINT.md) → `meta/navigator` is how an agent *enters* this flow: it asks what you want and walks you stage to stage, halting between each for the human to ratify, only routing to skills that exist on disk. `meta/author-a-skill` is the off-ramp for adding a new skill, pattern, or capability rather than running one. Neither is a node in the line; they are how you get on and off it.

---

## Optional — propose a run-order for one engagement

Given free-text describing an engagement, this file can also **return a menu** proposing which skills to run, in what order, and why — tailored to what the text contains. Rules for that step: it is a **menu**, never a verdict; order skills only as "this usually helps before that", never as a ranking-of-importance; if the text implies a skill is irrelevant, say so and offer to skip it; lead with the single best next move; if you cannot tell what the engagement is, **halt** and ask one orienting question.

Output a short markdown menu: a `Start here →` line, then a numbered list in the order that usually helps with one reason each, a `Probably skip` block, and one `Open question (halt)` line. Close with: *This is a proposal, not a plan of record — re-run any time the picture changes.*

---

## Deterministic — seed a downstream project (no model step)

Each downstream project gets its **own** GitHub Project. The board tracks the project's **phases** — `Prototype / MVP / Pilot / Production` — never its requirements. Requirements live as **markdown in the downstream repo**, threaded by `derives_from`. Run this exactly (substitute owner and title):

```bash
#!/usr/bin/env bash
# Seed a downstream project: its OWN GitHub Project, 4 phase columns, 1 intake issue.
# Requirements never live on the board — they live as markdown in the repo.
set -euo pipefail

OWNER="your-org-or-user"          # an org login or @me
TITLE="Acme Returns Portal"       # the downstream project's name
REPO="your-org/acme-returns"      # the downstream repo (for the intake issue)

# 1) Create the project's OWN GitHub Project (Projects v2, org- or user-scoped).
PROJECT_URL=$(gh project create --owner "$OWNER" --title "$TITLE" --format json | jq -r '.url')
PROJECT_NUMBER=$(gh project list --owner "$OWNER" --format json \
  | jq -r --arg t "$TITLE" '.projects[] | select(.title==$t) | .number')
echo "Created project #$PROJECT_NUMBER -> $PROJECT_URL"

# 2) Add the FOUR phase columns as a single-select "Phase" field.
#    The board tracks PHASES (maturity), not requirements.
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" \
  --name "Phase" --data-type SINGLE_SELECT \
  --single-select-options "Prototype,MVP,Pilot,Production"

# 3) Open the new-project-intake issue in the downstream REPO (not on the board).
#    Requirements are authored as markdown in this repo and traced — never as cards.
gh issue create --repo "$REPO" \
  --title "Project intake: $TITLE" \
  --label "intake" \
  --body "$(cat <<'EOF'
## New-project intake

Paste the messy reality of this engagement below — anything you already have
(an email, a call note, a one-line ask). Run `understand/decompose-intake-to-outcomes`
on this text to derive structure beneath the business outcomes a human accepts.

### What should this project deliver?
<!-- free text -->

### Phases live on the GitHub Project board; requirements live here as markdown.
- Board: tracks Prototype / MVP / Pilot / Production only.
- This repo: `requirements/` markdown, each requirement traced `derives_from` an outcome.
EOF
)"

echo "Seeded. Board tracks phases; intake issue opened in $REPO for the requirements."
```

> If `gh project` commands prompt for a scope, run `gh auth refresh -s project,read:project` once. The four columns are the delivery maturity ladder used by `deliver/describe-phases-releases-waves`.

---

## How the human decision points work

Most skills produce an artifact and stop; a person's normal review-and-merge of the PR **is** the decision point — `propose → ratify`, where a human PR merge is the only ratify step. A few points are genuine human commitments worth naming: **accept the business outcomes**, **adopt a solution shape**, **accept or reject each compromise**, and **a human architect must review every pattern or capability change** (the one structural human review, enforced by CODEOWNERS on `patterns/**` and `capabilities/**`). The inversion the library runs on: humans accept HIGH (outcomes, shape, contested calls), skills derive LOW (technical requirements, NFRs, classifications) and trace every derived item back to the outcome it serves.

Nothing here needs a specific model or runtime — markdown any workflow can read, plus one bash block any shell with `gh` + `jq` can run.
