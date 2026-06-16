# Per-engagement project folder (template)

The **optional, thin in-repo folder** you copy for a spike, a study, or a project with no repo of its
own yet. Most downstream projects skip it — they get their own repo and GitHub Project board and pull the
[skills](../../skills/) and [patterns](../../patterns/) from here. Plain markdown is the source of truth:
the skills read and write these files, a human edits them directly, and nothing else is the mechanism.

---

## How to use it

1. Copy this `_TEMPLATE/` folder to `projects/<your-project-slug>/`.
2. Delete this README (or replace it with a one-line note on what the project is).
3. Fill in the files below as you move through the SDLC method — outcomes first, then the rest derive
   from them. Each [skill](../../skills/) tells you which file it reads and which it writes.

Nothing is mandatory and nothing is gated. A sparse project with only `OUTCOMES.md` filled in is a
perfectly valid state — it just means you are early. Fill a file when you have something real to put
in it; leave a plain "nothing yet" line otherwise (honest emptiness, never a fake placeholder).

---

## The layout

```
projects/<your-project-slug>/
  OUTCOMES.md              # accepted business outcomes + derived requirements (the root of everything)
  SOLUTION-ARCHITECTURE.md # the frozen-8 sections — the durable design everyone builds against
  decisions/             # one ADR markdown file per recorded decision
    0001-<slug>.md
    0002-<slug>.md
  DISSENT.md               # what we decided NOT to do, and why
  RAID.md                  # the light register: risks, assumptions, issues, dependencies
  adoptions.md             # which CoE patterns this project adopted (feeds the portfolio tally)
```

### `OUTCOMES.md` — the root

The accepted **business outcomes** (in the sponsor's words: why the project exists and what success
means) and the **derived requirements** that serve them. Each requirement carries a `derives_from`
citation back to the outcome it serves — that trace edge is what everything downstream hangs on. A
requirement with no `derives_from` is a scope-creep flag, on purpose; surface it, don't hide it.
Deferred outcomes stay visible and flagged, never tidied away. Each requirement also carries its
**acceptance criteria** (how it will be tested). This is the one file you should fill first; the
architecture, decisions, and RAID all derive from it.

### `SOLUTION-ARCHITECTURE.md` — the durable design

The **frozen eight sections** — fixed, not per-project configurable, so the review and reconcile skills
target precise sections. In order:

1. **Background & context** — why the project exists, in the sponsor's words.
2. **Business architecture** — the accepted outcomes and their commitments.
3. **Requirements & acceptance criteria** — each requirement threaded to its outcome, with testable AC.
4. **Application & solution shape** — the adopted pattern: identity, topology, data placement, provenance.
5. **Quality attributes & NFRs** — the non-functional standards, mostly inherited from the pattern.
6. **Key decisions & trade-offs** — the contested calls (digest of `decisions/`).
7. **Estimate & delivery plan** — sized effort + confidence, with phases/releases/waves.
8. **Open questions & risks** — what is unresolved (cross-references `RAID.md`).

Each fact lives in **one** section (an NFR appears in section 5, not also in section 4). The
solution-architecture skill generates this file from your codebase plus this folder; edit it freely
afterwards — it is just markdown.

### `decisions/` — one ADR per decision

One Architecture Decision Record markdown file per genuinely contested call, numbered
(`0001-<slug>.md`, `0002-<slug>.md`, …), recording the **question, the choice, the rationale, and the
compromises accepted**. Section 6 of the architecture is the digest; these are the full record.

Minimal ADR shape:

```markdown
# ADR 0001: <the decision in a phrase>

- **Status:** accepted | superseded by ADR-NNNN
- **Date:** YYYY-MM-DD

## Context
What forced a choice. The constraints and the competing options.

## Decision
What we chose.

## Consequences
What this buys us, what it costs us, the compromise we accepted.
```

### `DISSENT.md` — what we decided NOT to do

A durable record of the paths **not taken** and **why** — the dissent register. The red-team / panel
skills surface objections and rejected options; this is where the surviving "we considered X and chose
not to, because Y" lines live, each with a date and a link to the decision or comment that settled it,
so a ruled-out path is not silently re-proposed six months later.

### `RAID.md` — the light register

One light, advisory register for **Risks, Assumptions, Issues, and Dependencies**. Each entry is a
short line with a kind tag, an owner, and a status. This is **advisory, never blocking** — it informs
the open-questions section of the architecture and gives the team a worklist; it does not gate
anything. Keep it as one flat file; do not build a tracker.

```markdown
| kind        | item                                          | owner | status   | note                          |
|-------------|-----------------------------------------------|-------|----------|-------------------------------|
| risk        | comparator data is thin, estimate is soft     | EM    | open     | revisit after MVP actuals     |
| assumption  | downstream team owns the prod GitHub Project  | EM    | holding  | confirm in kickoff            |
| issue       | auth pattern has an open WCAG warning          | —     | open     | see patterns/, attached NFR   |
| dependency  | release cadence depends on the platform team  | —     | watching | quarterly                     |
```

### `adoptions.md` — which patterns this project adopted

A simple list of which CoE [patterns](../../patterns/) this project **adopted**, by pattern `id`,
with the date adopted and a one-line note on how. This feeds the **portfolio adoption tally** (which
patterns are actually being used across projects, and where). Adopting a pattern means you inherit its
attached NFRs into section 5 of your architecture — note any you are deliberately not taking.

```markdown
# Patterns adopted by <project>

- `pattern-id-here` — adopted 2026-06-15 — used for the API edge; inherited its rate-limit + WCAG NFRs.
- `another-pattern-id` — adopted 2026-06-15 — data placement; took all attached NFRs.
```

---

## What does NOT live here

- **Requirements never go on the portfolio Project board** — the board shows only phases; this folder
  holds the detail. See [`../../docs/portfolio-github-projects.md`](../../docs/portfolio-github-projects.md) for that boundary.
- **No gates, no approvals, no orchestration engine** — living documents, not a workflow with enforced
  transitions. The skills propose; a human decides and edits.
