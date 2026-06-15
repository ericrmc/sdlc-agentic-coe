---
name: sdlc-spine
description: Umbrella TOC that orders the de-enforced FORGE stages, points at the real nested skill(s) that serve each, and seeds a downstream project's own GitHub Project. Start here.
when_to_use: starting any engagement, or deciding which skill to reach for next
output_kinds: [menu]
deterministic_fallback: the static ordered stage list + the gh project create snippet
suggested_tier: haiku
---

# sdlc-spine — the Centre-of-Excellence table of contents

## Purpose

This is the **front door and the map** for the whole skill library — nothing more.
It orders the fourteen stages of our delivery method, points at the one skill that
serves each stage, and seeds a downstream project's own GitHub Project so the team
can run its phases on a board.

It **enforces nothing.** There is no state machine here, no gate that blocks an
advance, no "you cannot proceed until…". The original platform had a nine-state
machine (`state_machine.py`) that returned `409` when a gate wasn't met; **we lifted
the *method* out of that and left the *enforcement* behind on purpose.** Every stage
below is advisory. A human merges a PR when they judge the work is ready; that merge
is the only "gate," and it is a human one.

> **Deleting this skill breaks no other skill.** It is pure navigation. Every sibling
> skill stands alone and is runnable on its own. This file just tells you *which one*
> to reach for, and *in what order they usually help*. Lose it and you lose the map,
> not the territory.

## When to use

- You are **starting any engagement** and want to know where to begin.
- You finished a stage and are **deciding which skill to reach for next.**
- You need to **seed a downstream project's GitHub Project** (the deterministic step).
- You have a **free-text engagement description** and want a proposed run-order menu
  (the LLM step).

## Inputs (what you supply)

- For navigation: nothing — just read the journey table below.
- For seeding: a project name (and optionally the GitHub owner/org).
- For the menu step: a paragraph or two of free text describing the engagement —
  the messy reality, pasted from an email, a call note, a one-line ask. Anything.

---

## The contract every sibling obeys

Two short rules. Every skill in this library obeys both. They are the de-enforced
descendants of the original platform's hardest-won invariants (the TARGET RULE and
the propose→ratify rhythm — see [`_contract/`](../_contract/) for the full statements
and the lint they imply).

### 1. The TARGET RULE — target the model, the record, or the blind spot, never the judgment

> Every skill's output is one of exactly four kinds: **proposal, question, menu, or
> halt.** Never a status, a verdict, a colour, a ranking-as-judgment, a feasibility
> stamp, a queue disposition, or an assessment of a person.

A skill may *propose* a requirement, *ask* "necessary for which outcome?", offer a
*menu* of options, or *halt* and say it cannot proceed. It may never say "approved,"
"this is gold-plated," "ranked #1," or "this person's design is weak." The human
holds every judgment. This is what lets the library be richly agent-driven without
collapsing into rubber-stamp review.

### 2. The propose→ratify rhythm

> The skill (or its agent) **proposes**; a **human ratifies** by merging the PR (or
> editing, or declining). The skill never crosses that gate on its own.

```
  agent PROPOSES  ──►  artifact lands as a PR / a markdown draft
        │
        │  (human edits / overrides / widens the space → re-propose)
        ▼
  human RATIFIES  ──►  merge the PR — the ONLY thing that makes it "real"
```

In the original app the agent "never crossed a ratification gate" and a `409` enforced
it. Here, **nothing enforces it but the rhythm itself**: the propose step writes a
draft or opens a PR, and the human's merge is the ratify step. The mechanic is the
same; the enforcement is gone. That is the whole pivot in one picture.

---

## The 14-stage journey

Read top to bottom. This is the order delivery usually wants — but it is a **map, not
a track**: skip, loop back, or re-enter any stage. Each row names the stage, the
skill(s) that serve it, what **auto-applies** (runs without you accepting it
item-by-item), and the **human gate** (almost always: *none — a human merges the PR*).

The "Skill(s)" column gives the **real on-disk path** under `skills/`. Click
straight to that `SKILL.md` — these are the live, nested paths, not stage slugs.

| # | Stage | Skill(s) that serve it (real path) | What auto-applies | Human gate |
|---|---|---|---|---|
| 1 | **Intake** | `skills/01-intake-outcomes/decompose-intake-to-outcomes` | Project skeleton + a new-project-intake issue drafted from the free text | none — a human merges the PR |
| 2 | **Outcomes** | `skills/01-intake-outcomes/decompose-intake-to-outcomes` + `skills/01-intake-outcomes/classify-requirements` | Technical requirements + classifications derived beneath each business outcome, each traced `derives_from` its outcome | **accept the business outcomes** (the few real commitments) |
| 3 | **Review** | `skills/02-review/red-team-requirements` (adversarial) + `skills/02-review/surface-risks-and-assumptions` + `skills/02-review/enumerate-roadblocks` | Nothing — every cue is a *question* naming its target, dismissible | none — a zero-note review is a legitimate, non-failing outcome |
| 4 | **Solution patterns** | `skills/03-solution/recommend-component-patterns` + `skills/03-solution/propagate-pattern-nfrs` | On adopt, the pattern's `attached_nfrs` flow in as derived requirements | **adopt the pattern** (the solution shape — a real commitment) |
| 5 | **Solution options** | `skills/03-solution/surface-solution-options` | Nothing structural — candidates are a *menu*; "do nothing" always present | **narrow to the chosen shape** |
| 6 | **Validation** | `skills/03-solution/validate-solution-vs-requirements` | Compromise *flags* (computed): "your 'instant confirm' degrades to ≤2s" | **accept or reject each compromise** (contested calls) |
| 7 | **Necessity check** | `skills/03-solution/necessity-check` (anti-gold-plating) | Nothing — the flag is computed; the skill *asks*, never asserts | **the human decides** keep-or-cut (zero cuts is legitimate) |
| 8 | **Technical / design review** | `skills/04-review-and-panel/design-review-findings` | Nothing — assembles the delta + impact view for inspection | none — a comment-only review; accepting nothing is legitimate |
| 8b | **Design review · WCAG/a11y** | `skills/04-review-and-panel/frontend-a11y-review` | Nothing — emits citation-bearing a11y findings against WCAG 2.2 AA | none — a comment-only review; accepting nothing is legitimate |
| 9 | **NFRs** | `skills/01-intake-outcomes/nfr-coverage-check` (the NFR catalogue check) | NFRs inherited from an adopted pattern; the rest proposed against the catalogue | **accept the NFR set** (or defer; untouched = defer) |
| 10 | **Convene panel** | `skills/04-review-and-panel/convene-a-panel` + `skills/04-review-and-panel/synthesise-panel` + `skills/04-review-and-panel/red-team-and-dissent` + `skills/04-review-and-panel/surface-open-decisions` | Synthesis lands as *proposals* + a dissent register; nothing decided | **the human picks** from the synthesised menu |
| 11 | **Solution architecture** | `skills/05-solution-architecture/synthesise-solution-architecture` (+ `skills/05-solution-architecture/reconcile-design-vs-requirements`, `skills/05-solution-architecture/import-external-design`, `skills/05-solution-architecture/reconcile-as-built`) | A sectioned, versioned design doc drafted section-by-section from the codebase | **accept the design** (or request a section regenerate) |
| 12 | **Phases: MVP / Pilot / Production** | `skills/07-lifecycle/describe-phases-releases-waves` + `skills/07-lifecycle/help-implement-a-wave` (+ `skills/07-lifecycle/triage-backlog-and-defer`, `skills/07-lifecycle/scope-reconcile-check`) | Phase stamps + a light UAT checklist per phase | none — a human merges the phase entry |
| 13 | **Releases** | `skills/07-lifecycle/describe-phases-releases-waves` | Release notes projected from the add/change/remove req deltas, each traced | none — a human merges the release PR |
| 14 | **Pattern-library promotion** | `skills/08-pattern-library/author-component-pattern` + `skills/08-pattern-library/pattern-library-curate` | Net-new designs *flagged* eligible; cold patterns *flagged* as a curation smell | **an architect merges the pattern PR** (with evidence, dates, sunset metadata) |

**Portfolio (cross-cutting, not a numbered stage).** Above the per-project
journey sits the org-wide view: `skills/09-portfolio/portfolio-phase-health`
(derived-on-read RAG health per project) and
`skills/09-portfolio/advisory-governance-checklist` (the light, advisory
governance pass). These read *across* projects rather than advancing one.

**How to read the gate column.** "none — a human merges the PR" means the skill
produces an artifact and stops; the human's normal review-and-merge *is* the gate.
A named gate ("accept the business outcomes") flags the **few** points that are
genuine human commitments — the inversion the method is built on: **humans accept
HIGH (outcomes, solution shape, contested calls); the skills derive LOW** (technical
requirements, NFRs, classifications) and auto-apply it, every derived row traced back
to the outcome it serves.

**Order is load-bearing but not enforced.** The sequence —
Intake → Outcomes → Review → Solution patterns → Solution options → Validation →
Necessity check → Technical/design review → NFRs → Convene panel → Solution
architecture → Phases → Releases → Pattern-library promotion — is the path delivery
usually takes. You may, and often will, loop: a panel (10) can re-open outcomes (2);
a release (13) re-enters the whole front half under a new direction. Nothing stops you.

---

## The method — numbered steps

### STEP A · Orient (always do this first)

Read the journey table. Find where the engagement is. If it hasn't started, you are at
Intake; if outcomes exist but no solution is chosen, you are around stage 4–5; and so
on. Name the current stage in one line and point at the one skill that serves it.

### STEP B · Seed a downstream project (DETERMINISTIC)

This is a deterministic step — **no LLM judgment**. Each downstream project gets its
**own** GitHub Project, guided by these skills but owned by that team. The board tracks
the project's **PHASES**, not its requirements. Requirements live as **markdown in the
downstream repo**, threaded by `derives_from`, **never on the board.**

Run this exactly (substitute the owner and title):

```bash
#!/usr/bin/env bash
# Seed a downstream project: its OWN GitHub Project, 4 phase columns, 1 intake issue.
# Requirements never live on the board — they live as markdown in the repo.
set -euo pipefail

OWNER="your-org-or-user"          # e.g. an org login or @me
TITLE="Acme Returns Portal"       # the downstream project's name
REPO="your-org/acme-returns"      # the downstream repo (for the intake issue)

# 1) Create the project's OWN GitHub Project (Projects v2, org- or user-scoped).
PROJECT_URL=$(gh project create --owner "$OWNER" --title "$TITLE" --format json | jq -r '.url')
PROJECT_NUMBER=$(gh project list --owner "$OWNER" --format json \
  | jq -r --arg t "$TITLE" '.projects[] | select(.title==$t) | .number')
echo "Created project #$PROJECT_NUMBER → $PROJECT_URL"

# 2) Add the FOUR phase columns as a single-select "Phase" field.
#    The board tracks PHASES (maturity), not requirements.
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" \
  --name "Phase" --data-type SINGLE_SELECT \
  --single-select-options "Prototype,MVP,Pilot,Production"

# 3) Open the new-project-intake issue in the downstream REPO (not on the board).
#    This is where Intake (stage 1) begins; requirements will be authored as
#    markdown in this repo and traced — never as cards on the board.
gh issue create --repo "$REPO" \
  --title "Project intake: $TITLE" \
  --label "intake" \
  --body "$(cat <<'EOF'
## New-project intake

Paste the messy reality of this engagement below — anything you already have
(an email, a call note, a one-line ask). The Outcomes skill (stage 2) reads this
and derives structure beneath the business outcomes you accept.

### What should this project deliver?
<!-- free text — the front door is the act of typing -->

### Phases live on the GitHub Project board; requirements live here as markdown.
- Board: tracks Prototype / MVP / Pilot / Production only.
- This repo: `requirements/` markdown, each requirement traced `derives_from` an outcome.

Guided by the CoE skill library — this project owns its own board and its own pace.
EOF
)"

echo "Seeded. Board tracks phases; intake issue opened in $REPO for the requirements."
```

> If `gh project` commands prompt for a scope, run `gh auth refresh -s project,read:project`
> once. The four columns are **Prototype / MVP / Pilot / Production** — the delivery
> maturity ladder, the same four the method uses at stage 12.

### STEP C · Propose a run-order (THE LLM STEP)

Given the free-text engagement description, **return a MENU** proposing which stages
and skills to run, in what order, and *why* — tailored to what the text actually
contains. This is the one reasoning step in this skill.

Hard rules for this step (the TARGET RULE applies to you, too):

- It is a **menu**, never a verdict. Propose; do not decide.
- **Never rank stages as a judgment** ("stage 4 is most important"). Order them only
  as *"this usually helps before that."*
- If the text already implies a stage is irrelevant, say so plainly and offer to skip
  it — don't pad the menu to look thorough.
- One bright thing at a time: lead with the single best next move, then list the rest.
- If you cannot tell what the engagement is, **halt** and ask one orienting question
  rather than guessing.

Reason like this: read the text → spot which stages it gives you raw material for
(does it name outcomes? a technology? a known pattern? a hard constraint?) → propose
the smallest sensible path through the stages that turns this text into a governed,
buildable design, and say why each stage earns its place for *this* engagement.

---

## Output format

Return a short, calm markdown menu. Lead with one bright next move. Template:

Always name skills by their **real nested path** (the full `skills/<bucket>/<skill>`
form shown in the journey table), so a reader can click straight to the `SKILL.md`.
In the template below, `BUCKET/LEAF` stands in for that real path.

```markdown
## Suggested path for: <one-line restatement of the engagement>

**Start here →** `BUCKET/LEAF` — <one line: why this is the best first move *here*>.

Then, in the order that usually helps:

1. `BUCKET/LEAF` (<Stage name>) — <why this stage earns its place for *this* text>.
2. `BUCKET/LEAF` (<Stage name>) — <why>.
3. …

**Probably skip / defer:**
- `BUCKET/LEAF` (<Stage>) — <why it doesn't apply to what you described>.

**Open question (halt):** <the one thing I'd need to know to tighten this> —
or proceed with the path above and we'll learn it at Intake.

_This is a proposal, not a plan of record. Re-run me any time the picture changes._
```

### Worked example

Input free text:

> "Client wants a returns portal for their warehouse staff. Must be WCAG AA. They
> mentioned they already use our standard 'event-sourced ledger' pattern elsewhere
> and want to reuse it. Tight timeline — three weeks to a pilot."

A good menu output:

```markdown
## Suggested path for: a WCAG-AA returns portal reusing the event-sourced ledger pattern, 3 weeks to pilot

**Start here →** `skills/01-intake-outcomes/decompose-intake-to-outcomes` — capture the
messy reality and open the intake issue; the pattern reuse and the a11y constraint are
strong signals worth recording verbatim.

Then, in the order that usually helps:

1. `skills/01-intake-outcomes/decompose-intake-to-outcomes` (Outcomes) — the ask is
   concrete; derive technical requirements beneath the "staff can process returns"
   outcome so everything downstream traces back.
2. `skills/03-solution/recommend-component-patterns` (Solution patterns) — they named an
   *approved pattern* to reuse; this is the fast path. Adopting it flows its NFRs in for
   free — pull this forward, ahead of options.
3. `skills/04-review-and-panel/frontend-a11y-review` (Design review · WCAG/a11y) — "must
   be WCAG AA" is a named constraint; run the a11y lens early so it shapes the design,
   not patches it late.
4. `skills/01-intake-outcomes/nfr-coverage-check` (NFRs) — confirm the pattern's
   inherited NFRs cover the tight timeline and the a11y target; propose any gaps against
   the catalogue.
5. `skills/07-lifecycle/describe-phases-releases-waves` (Phases) — three weeks to *pilot*
   means MVP→Pilot is the near horizon; seed those columns and a light UAT checklist.

**Probably skip / defer:**
- `skills/03-solution/surface-solution-options` (Solution options) — they already chose a
  pattern, so the "nothing fits, explore rivals" stage likely doesn't apply. Re-enter
  only if the pattern fails validation.

**Open question (halt):** is the event-sourced ledger pattern *approved* and current
in our library (in-date, not superseded)? If not, stage 4 becomes stage 5 — we explore
instead of adopt. Otherwise proceed with the path above.

_This is a proposal, not a plan of record. Re-run me any time the picture changes._
```

Notice: it pulls the pattern stage *forward* because the text earned it, pulls a11y
*forward* because it's a named constraint, proposes skipping options with a reason,
and halts on the one fact that would flip the path — all menu, no verdict.

---

## Notes / anti-patterns

- **This skill enforces nothing.** If you find yourself writing "you cannot advance
  until…", stop — that's the old state machine talking. The pivot dropped the
  `409`-style gates on purpose. Advisory only.
- **Don't put requirements on the GitHub Project board.** The board is for **phases**
  (Prototype/MVP/Pilot/Production). Requirements are markdown in the downstream repo,
  traced by `derives_from`. Mixing the two recreates the "flat wall of cards accepted
  one box at a time" the method exists to avoid.
- **Don't rank stages as a judgment.** Ordering is "usually helps before"; it is never
  "this stage matters more than that one." Stage order is a map, not a scoreboard.
- **Don't pad the menu.** A three-step path that fits the engagement beats a
  fourteen-step path that looks complete. One bright thing at a time.
- **Don't seed the board with the LLM step.** Seeding (STEP B) is deterministic `gh`
  commands — same input, same output, no reasoning. Keep it that way so it's
  reproducible and reviewable.
- **Each downstream project owns its own board and its own pace.** These skills guide;
  they don't drive. A team can ignore a stage, loop a stage, or run them out of order.
- **When in doubt, take the obvious default and state it in one line** rather than
  asking. Only `halt` when you genuinely can't tell what the engagement is.
- **Provider-agnostic.** Nothing here needs a specific model or runtime — it's markdown
  any LLM workflow can read, plus one bash block any shell with `gh` + `jq` can run.
