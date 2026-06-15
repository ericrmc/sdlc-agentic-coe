# Portfolio as GitHub Projects

Run a leadership-altitude portfolio view on top of GitHub Projects: one card per downstream project, the phase it sits in, and an advisory red/amber/green verdict flagging what needs attention. Advisory only — it renders facts that live elsewhere; it never blocks, approves, or holds enforcement state.

New here? Start at `GETTING-STARTED.md`, then `skills/MAP.md`. Need-first lookup: `capabilities/INDEX.md`.

## Rules

| Rule | Detail |
|---|---|
| Phase granularity only | The board never goes below phase level. No requirements, outcomes, NFRs, patterns, release items, tasks, sub-issues, or per-requirement status. |
| One card per project | The org board holds exactly one card per downstream project — not per phase, not per requirement. |
| Detail lives in the repo | Requirements and releases stay as markdown in each downstream repo, threaded by `derives_from`. The board rolls up phases; it never copies that detail (nothing to drift). |
| No per-person or pace metrics | No velocity, story points, burndown, cycle time, commit/PR/review counts, acceptance rate, or any per-person field. This is a project-health view, never performance management. |

## The four phase columns

A project occupies exactly one column — the latest phase it has entered (phases may be skipped).

| Column | Meaning |
|---|---|
| Prototype | Throwaway, to see and feel. Not in users' hands. |
| MVP | First real, narrow slice in users' hands. |
| Pilot | Controlled rollout to a limited cohort. |
| Production | General availability and the ongoing release stream. |

These are the maturity phases defined in `skills/deliver/describe-phases-releases-waves`.

## Two boards

| Board | Owner | Holds |
|---|---|---|
| Per-project board (one per repo) | The team that owns the repo | The four phase columns as a `Phase` single-select; the team's own issues, PRs, and labels. The only contract: it carries the four phase options, because the org rollup reads them. |
| Org portfolio board (one for the whole CoE) | The practice lead | One card per project, each with `Phase`, an advisory `RAG` verdict, and a `Reasons` field naming every failing check. |

Practice lead's default view: filter `RAG: amber, red`, sort red first — the "needs attention" home view. A green project takes no space.

## The RAG verdict

Computed by a scheduled `portfolio-rollup` GitHub Action, written into each card's `RAG` and `Reasons` fields. The logic matches `skills/library/portfolio-phase-health`.

- Recomputed every run from live repo signals (markdown record, open advisory flags, drift notes) and overwritten. The cell is a cache of a derived value, never a stored or edited score.
- Verdict is the worst level across a small fixed check set: `red if any red else amber if any amber else green`. Never a weighted grade.
- `Reasons` names every failing check — the audit of the verdict.
- Degrades safely: a missing signal is "no finding," never an error. One bad repo never breaks the board.

Latency: the board is as fresh as the last run, no fresher. State the schedule in the board description so an hour-old green is not mistaken for a real-time guarantee. Anyone needing truth-this-second reads the project's own repo and board.

Advisory exposure facts (open critical risks, PII present, automated-decision present) may ride along as extra board fields for scanning, but are surfaced facts, not verdict drivers, until the org ratifies them as bars.

```text
for each downstream project:
    red, amber = [], []
    if a governance/review send-back is open:            red.append("review sent back")
    if required checks for the current phase are open:    red.append("N checks open")
    if phase == Production and the record is incomplete:  amber.append("record incomplete")
    if decisions remain in draft:                         amber.append("N decisions drafted")
    if design-drift notes are open:                       amber.append("design drift open")
    verdict  = "red" if red else "amber" if amber else "green"
    write verdict + (red + amber) to the org board's RAG / Reasons fields
```

## Setup

Authenticate `gh` with the project scope: `gh auth refresh -s project,read:project`.

Org portfolio board (once):

```bash
ORG="your-org"
gh project create --owner "$ORG" --title "Delivery Portfolio"   # note the printed number -> $ORG_PROJECT_NUMBER
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --name "Phase" --data-type SINGLE_SELECT --single-select-options "Prototype,MVP,Pilot,Production"
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --name "RAG" --data-type SINGLE_SELECT --single-select-options "green,amber,red"
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" --name "Reasons" --data-type TEXT
# Optional advisory facts only (never verdict drivers, never per-person):
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" --name "Open critical risks" --data-type NUMBER
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --name "PII present" --data-type SINGLE_SELECT --single-select-options "yes,no"
```

Then save a board view filtered `RAG: amber, red`, sorted red-first, as the practice lead's default.

Per-project board (once per downstream project, at setup — the seed block in `skills/MAP.md`):

```bash
OWNER="your-org"; NAME="Acme Onboarding"
gh project create --owner "$OWNER" --title "$NAME — delivery"   # note -> $PROJECT_NUMBER
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" \
  --name "Phase" --data-type SINGLE_SELECT --single-select-options "Prototype,MVP,Pilot,Production"
gh project item-create "$ORG_PROJECT_NUMBER" --owner "$ORG" --title "$NAME"   # one org-board card; set its Phase
```

The rollup: install the `portfolio-rollup` workflow in `.github/workflows/`. Give it a schedule (`cron: "0 * * * *"`) and/or a `repository_dispatch` trigger so a downstream `main` push can poke it. It iterates the projects, recomputes each verdict, and writes `RAG` + `Reasons` via `gh project item-edit`.
