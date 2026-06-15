# SDLC Agentic Centre of Excellence

A portable, GitHub-native library of **agent skills** that runs the proven early-SDLC method — from a
business vision to a build-ready solution design and on through phases and releases — as light, advisory
markdown you can drop into Claude Code or any LLM workflow.

No app to deploy. No state machine. No approval gates. The method is the asset; GitHub carries the
mechanics; a human always disposes.

---

## What this is

We retired a bespoke three-tier app that ran this method end to end, and lifted the load-bearing reasoning
out into **36 self-contained skills** (markdown + YAML frontmatter), a **PR-reviewed pattern library**, and a
**thin GitHub-native control plane** (Actions that validate and combine; Projects that show a phase-level
portfolio; PRs that *are* the ratification).

The whole library is **advisory by construction**. Every skill's output is one of exactly four kinds —
**proposal, question, menu, or halt** — never a verdict or a status. Because an agent's output structurally
cannot self-approve, the library needs no enforcement gate. That rule is **lintable**, and one GitHub Action
checks it on every PR. That is the entire light-governance posture.

## Why

The business will not support a bespoke app, but the *method* is valuable and reusable across every
downstream delivery. So we make the method portable: a reference Centre of Excellence a team adopts skill by
skill, contributes patterns back to, and runs against each new project's own GitHub repo and Project.

## The method (the FORGE spine, de-enforced)

> Intake → Outcomes → Review → Solution patterns (retrieval) → Solution options → Validation → Necessity
> check → Technical/design review (incl. WCAG/a11y) → NFRs → Convene a battle-test panel → Solution
> architecture (read the codebase, synthesise in sections) → Phases/MVP/Pilot/Production → Releases →
> Pattern-library promotion.

The ordering and the per-stage reasoning are kept verbatim from the original prompts. Only the *enforcement*
is dropped.

## Quick start (for a team)

1. **Browse the spine.** Open [`skills/00-sdlc-spine/SKILL.md`](skills/00-sdlc-spine/SKILL.md) — it orders
   the 14 stages and points at one skill per stage.
2. **Seed your project.** Run the spine's "seed a project" step to create your project's OWN GitHub Project
   with phase columns (Prototype / MVP / Pilot / Production). Your requirements and design live as markdown
   in *your* repo — never on the portfolio board.
3. **Run a skill.** Paste a `SKILL.md` (or a combined bundle from `generated/`) into your LLM workflow.
   Every skill works with no model at all (a deterministic scaffold) and deepens with a one-line model swap.
4. **Ratify by merging.** When a skill proposes markdown, review the delta and merge the PR. That merge is
   the ratification — the only act that advances anything.
5. **Adopt patterns.** `recommend-component-patterns` reads the approved library and recommends genuine
   fits; on adopt, the pattern's NFRs flow into your requirements for free. Append one line to
   `adoptions/ledger.jsonl` so the pattern's "used in N engagements" tally stays honest.
6. **Contribute back.** Built something reusable? Open a `new-pattern` issue with evidence, then a PR. An
   architect reviews and merges (CODEOWNERS makes that review structurally necessary). The merge ratifies it.

You can also copy a single skill folder out of this repo and run it anywhere — the schema and vocabularies
travel with it.

## Repo map

```
skills/                  THE PRODUCT — 36 copy-pastable SKILL.md folders, numbered by FORGE stage
  00-sdlc-spine/         umbrella TOC; seeds a downstream Project
  _contract/             the cross-cutting authoring contract (target rule, propose→ratify, fan-out, explore)
  01-intake-outcomes/    decompose / classify / nfr-coverage
  02-review/             red-team-requirements / risks-and-assumptions / roadblocks
  03-solution/           recommend-patterns / solution-options / propagate-nfrs / validate / necessity
  04-review-and-panel/   design-review / a11y / open-decisions / convene-panel / synthesise / red-team-dissent
  05-solution-architecture/  synthesise-architecture / reconcile-design / import-design / reconcile-as-built
  06-handoff/            scaffold-then-handoff / testing-brief / design-studio-brief / estimate
  07-lifecycle/          phases-releases-waves / implement-a-wave / triage-backlog / scope-reconcile
  08-pattern-library/    author-component-pattern / pattern-library-curate
  09-portfolio/          portfolio-phase-health / advisory-governance-checklist
  _shared/               ONE canonical copy of each shared convention; skills quote it (drift-guarded)
  _scripts/              plain validators/concatenators (Actions are just runners of these)
patterns/                the PR-reviewed component-pattern library (one .md per pattern)
  _schema/               the frontmatter JSON Schema + closed NFR-kind enum
nfrs/                     the NFR categories + kind vocabularies the skills cite
references/               the other closed enums (challenge-kinds, frozen-8, panel roster, waves, change-kinds)
projects/_TEMPLATE/       OPTIONAL per-engagement markdown SoT + adoption ledger
adoptions/ledger.jsonl    the append-only adoption provenance (PR-appended, never deleted)
generated/                Action OUTPUT only — never hand-edited
.github/                  the thin control plane (Actions, PR/issue templates, CODEOWNERS)
DESIGN.md                 the full architecture, skill catalogue, mechanics, pattern lifecycle
CONTRIBUTING.md           how to author/PR/validate a skill or a pattern; the review/evidence/sunset process
```

## The governance posture in one paragraph

There are no enforcement gates. PR review **is** the ratify. CODEOWNERS + branch protection make a human
architect's review structurally necessary to merge a *pattern* — the single hard gate, expressed in GitHub
config, not code. Everything else is a cue, a question, or a checkbox. Derived facts (pattern maturity, the
portfolio RAG verdict) are recomputed by Actions and never persisted as a field that can rot. No
acceptance-rate, throughput, or per-person metric exists anywhere.

See [`DESIGN.md`](DESIGN.md) for the complete architecture and [`CONTRIBUTING.md`](CONTRIBUTING.md) for the
pattern review/validation/evidence/sunset process.
