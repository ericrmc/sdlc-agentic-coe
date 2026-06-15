# Portfolio as GitHub Projects — phase-level guidance

This is the guidance for running the **portfolio** view on top of GitHub Projects. It is the lightweight,
GitHub-native replacement for the bespoke app's `/portfolio` overview: a leadership-altitude scan of where
each downstream project sits in its delivery lifecycle, with an advisory RAG verdict to flag what needs a
practice lead's attention.

It is deliberately **light and advisory**. Nothing here is a gate. The board does not block a project from
moving, it does not approve anything, and it holds no enforcement state. It is a *render of facts* that live
elsewhere — a place to look, not a place that decides.

---

## 1. The altitude rule — phases only, never requirements

> The portfolio operates at **PHASE granularity, full stop.**

The only columns the portfolio ever has are the four delivery-lifecycle maturity phases:

| Column | What it means |
|---|---|
| **Prototype** | Throwaway, to see and feel. Not in users' hands. |
| **MVP** | The first real, narrow slice in users' hands. |
| **Pilot** | A controlled rollout to a limited cohort. |
| **Production** | General availability and the ongoing release stream. |

These are the maturity phases from the `describe-phases-releases-waves` skill (the same Prototype → MVP →
Pilot → Production ladder the bespoke app's delivery-lifecycle model used). A project occupies exactly one
column at a time — the latest phase it has *entered* (a project may skip a phase; the column is the real
current phase, not a fixed sequence step).

**The portfolio NEVER goes below phase level.** It does not list requirements, outcomes, acceptance criteria,
release items, NFRs, patterns, or tasks. There are no sub-issues, no checklists of requirements, no
per-requirement status on this board. The instant you find yourself wanting a "requirements" column or a
card per requirement, you have left the portfolio's altitude — stop.

Those things live as **markdown in each downstream project's own repo**, and (where the team wants a working
board) in *that project's own* GitHub Project. The portfolio rolls up phases; it never reaches down into the
requirement-level detail that each project governs for itself with the skills in this CoE.

Why the hard line: the bespoke app learned that a portfolio that drills into requirements becomes a second
system of record that immediately drifts from the source markdown. Keeping the portfolio at phase altitude
means there is **nothing to drift** — the detail has exactly one home (the project repo), and the portfolio
only ever shows the one fact a leader actually scans for: *what phase is each thing in, and is any of it in
trouble.*

---

## 2. One Project per downstream repo

Each downstream project gets its **own** GitHub Project, with **its own four phase columns**. This is the
project's working board — the team that owns the repo drives it. The four columns are the same Prototype /
MVP / Pilot / Production phases, so every project speaks the same lifecycle language.

The per-project board is seeded once, by the `sdlc-spine` skill / setup script, when the downstream project
is stood up:

```bash
# Create the project's own board (run from / against the downstream repo's owner)
gh project create --owner "$OWNER" --title "$PROJECT_NAME — delivery"

# Capture the number it printed, then add the four phase columns as a single-select field.
# (The four phase options ARE the board's status lanes.)
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" \
  --name "Phase" --data-type SINGLE_SELECT \
  --single-select-options "Prototype,MVP,Pilot,Production"
```

That is the whole seed: a board and the four phase options. Everything else about how that team runs day to
day — their issues, their PRs, their own labels — is **theirs**, not the CoE's business. The CoE's only
contract with a per-project board is that it carries those four phase options, because that is what the
org-level rollup reads.

A downstream project's *requirement* and *release* detail stays as markdown in its repo (authored and kept
current with the CoE skills). The per-project board is for the **work**; the markdown is the **record**.

---

## 3. The org-level Project — the practice lead's needs-attention view

Above the per-project boards sits **one** org-level GitHub Project: the portfolio. It has **one card per
downstream project** (not per phase, not per requirement). Each card rolls up:

- **Phase** — the single current maturity phase that project sits in (Prototype / MVP / Pilot / Production),
  shown as the board's column.
- **Advisory RAG verdict** — `green` / `amber` / `red`, in a single-select field.
- **Reasons** — a short text field naming *every* failing check behind the verdict (e.g. "2 required
  checks open; design drift open"). The verdict is never a black box; the reasons field always says why.

The practice lead's default view is **"needs attention"**: filter to `RAG = red OR amber`, sort red first.
That is the entire leadership ergonomic — open the org board, see the handful of projects that are amber or
red and exactly *why*, and go ask about those. A green project needs no attention and takes no space in the
lead's head.

This mirrors the bespoke app's `/portfolio` exactly: one row per project, the current phase, and a
derived-on-read `standing` verdict with `reasons`. We are reproducing that read in GitHub-native fields, not
re-inventing it.

A suggested saved view setup:

```bash
# Single-select for the verdict; a text field for the reasons.
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --name "RAG" --data-type SINGLE_SELECT --single-select-options "green,amber,red"
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --name "Reasons" --data-type TEXT
# (Then save a board view filtered `RAG:amber,red` — the practice lead's home view.)
```

---

## 4. How the RAG gets onto the board

The verdict is computed by the **`portfolio-rollup` Action** (a scheduled GitHub Actions workflow). For each
downstream project it recomputes **portfolio-phase-health** and writes the result into that project's `RAG`
and `Reasons` fields on the org board.

The model is lifted straight from the bespoke app's `project_health` projection, and the discipline carries
over verbatim:

- **It is a render of derived-on-read facts, never a stored score.** The Action *recomputes* the verdict
  every run from the live signals in each project's repo (its markdown record, its open advisory flags, its
  reconcile/drift notes) and overwrites the board field. The board cell is a *cache of a derived value*, not
  a number anyone edits or that accrues history. There is nothing to drift because the truth is recomputed,
  not stored.
- **The verdict is the worst level across a small fixed check set** — a transparent boolean conjunction, the
  same `red if any red else amber if any amber else green` rule the bespoke `project_health` used. It is
  never a weighted grade or a score out of 100.
- **`Reasons` names every failing check.** If a project is amber, the reasons field lists each amber check;
  if red, each red one. The field is the audit of the verdict.
- **Every check degrades safely.** A project whose repo is missing a signal the rollup looks for is treated
  as "no finding," not an error — the rollup never fails a project's verdict because a file was absent, and
  the board never breaks on one bad repo.

### The latency trade-off, stated plainly

Because the rollup runs **on a schedule** (say, hourly or on each downstream `main` push via
`repository_dispatch`), the RAG on the board is **as fresh as the last run, and no fresher.** If a project
goes red at 10:05 and the rollup runs at the top of each hour, the board shows red at 11:00, not 10:05.

That staleness window is the price of *not* storing a score and *not* coupling the org board live to every
repo. We accept it on purpose: this is a leadership *scanning* surface, not an operational alarm. Anyone who
needs the truth-this-second reads the project's own markdown record and its own board — that is always live.
The org board trades a scheduled lag for a single, cheap, drift-free rollup. State the schedule openly in the
board's description so no one mistakes an hour-old green for a real-time guarantee.

A sketch of the rollup's per-project logic (deterministic; the same shape as the bespoke `project_health`):

```text
for each downstream project:
    reasons_red   = []
    reasons_amber = []

    # RED — bars the org has chosen to treat as "must look now"
    if record shows a governance/review send-back open:        reasons_red.append("review sent back")
    if required advisory checks for the current phase are open: reasons_red.append("N checks open")

    # AMBER — drift / incompleteness, worth a glance not an alarm
    if phase == Production and the record is incomplete:        reasons_amber.append("record incomplete")
    if decisions still in draft:                                reasons_amber.append("N decisions drafted")
    if reconcile/design-drift notes are open:                   reasons_amber.append("design drift open")

    verdict  = "red" if reasons_red else "amber" if reasons_amber else "green"
    reasons  = reasons_red + reasons_amber
    write verdict + reasons to the org board's RAG / Reasons fields for this project
```

Keep the check set small and only include bars the org actually stands behind. Advisory exposure facts
(critical risks open, PII present, automated-decision present) can ride along as extra board fields for
scanning, but — exactly as in the bespoke app — they are **surfaced facts, not verdict drivers**, until the
org explicitly ratifies them as bars. The RAG stays a small, defensible, explainable conjunction.

---

## 5. What is NEVER on the board

The portfolio carries **no per-person, throughput, or acceptance-rate metric.** None of:

- velocity, story points, burndown, cycle time, or any throughput number;
- per-author commit / PR / review counts, or any per-person leaderboard;
- a pattern acceptance-rate, a "% of proposals accepted," or any approval-rate figure;
- any field that ranks or scores an individual.

This is a deliberate scope guard, inherited from the bespoke app (its `/portfolio` route is explicitly
documented "NO per-person metrics"). The portfolio answers *"what phase is each project in, and is any of it
in trouble"* — a project-health question — and nothing else. The moment a column or field starts measuring
*people* or *pace*, it has stopped being a phase portfolio and become a performance-management tool, which
this surface must never be. If someone asks for a velocity or acceptance-rate column, the answer is no — that
data, if it's wanted at all, belongs in a different tool owned by a different conversation.

---

## 6. How to set it up

A practical, copy-pasteable setup. Run with the `gh` CLI authenticated and the `project` scope granted
(`gh auth refresh -s project,read:project`).

**a. Org-level portfolio board (once for the whole CoE):**

```bash
ORG="your-org"

# 1. Create the single org portfolio board.
gh project create --owner "$ORG" --title "Delivery Portfolio"
#   -> note the project number it prints; call it $ORG_PROJECT_NUMBER

# 2. Phase column (the altitude rule — these four options ARE the columns).
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --name "Phase" --data-type SINGLE_SELECT \
  --single-select-options "Prototype,MVP,Pilot,Production"

# 3. The advisory RAG verdict + its reasons.
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --name "RAG" --data-type SINGLE_SELECT --single-select-options "green,amber,red"
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --name "Reasons" --data-type TEXT

# 4. (Optional, advisory facts only — never verdict drivers, never per-person.)
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --name "Open critical risks" --data-type NUMBER
gh project field-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --name "PII present" --data-type SINGLE_SELECT --single-select-options "yes,no"
```

Then, in the board UI, save a view filtered to `RAG: amber, red`, sorted red-first, and make it the
practice lead's default — the "needs attention" view.

**b. Per-project board (once per downstream project, by `sdlc-spine` at setup):**

```bash
OWNER="your-org"        # or the team/user that owns the downstream repo
NAME="Acme Onboarding"  # the downstream project's name

gh project create --owner "$OWNER" --title "$NAME — delivery"
#   -> note $PROJECT_NUMBER
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" \
  --name "Phase" --data-type SINGLE_SELECT \
  --single-select-options "Prototype,MVP,Pilot,Production"

# Add one card on the ORG board for this project (the portfolio's one-card-per-project rule).
gh project item-create "$ORG_PROJECT_NUMBER" --owner "$ORG" \
  --title "$NAME"
# (Then set its Phase = the project's current maturity phase.)
```

**c. The rollup:**

Install the `portfolio-rollup` GitHub Actions workflow (in this CoE's `.github/workflows/`). Give it a
schedule (`on: schedule: - cron: "0 * * * *"` for hourly) and/or a `repository_dispatch` trigger so a
downstream `main` push can poke it. It iterates the downstream projects, recomputes each verdict per section
4, and writes `RAG` + `Reasons` onto the org board via `gh project item-edit`. That workflow's frontmatter
and validation are its own file; this document is the *what and why* of the board it feeds.

---

## In one line

The portfolio is **one org board, one card per project, four phase columns, an advisory recomputed RAG with
reasons, no per-person metrics, and nothing below phase level** — a place to look, never a gate.
