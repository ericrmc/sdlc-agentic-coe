# Per-engagement project folder (template)

This is the **optional, thin folder** you copy when you want to run a project *inside this
Centre-of-Excellence repo* — for a quick spike, a study, or when a project has no repo of its own yet.

**Most downstream projects do not use this.** The normal path is: each downstream project gets its
**own repo and its own GitHub Project board** (for the portfolio view of its *phases*), and pulls the
[skills](../../skills/) and [patterns](../../patterns/) from here. Use this folder only when keeping
the artefacts here is genuinely simpler than standing up a repo.

Everything here is **plain markdown, and the markdown is the source of truth.** There is no database,
no app, no orchestration engine. The skills read these files and write back to them. A human reviews and
edits them directly. That is the whole mechanism.

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

The **frozen eight sections** — the design everyone builds against. The set is fixed (not
per-project configurable); freezing it is what lets the review and reconcile skills target precise
sections. In order:

1. **Background & context** — why the project exists and what success means, in the sponsor's words.
2. **Business architecture** — the accepted business outcomes and the commitments they represent.
3. **Requirements & acceptance criteria** — every derived requirement threaded to its outcome, each
   with its testable acceptance criteria.
4. **Application & solution shape** — the adopted pattern as the solution shape: identity, topology,
   data placement, provenance.
5. **Quality attributes & NFRs** — the non-functional standards the build must hold, mostly inherited
   from the adopted pattern.
6. **Key decisions & trade-offs** — the genuinely contested calls, what was chosen and why, including
   compromises accepted (the detail lives in `decisions/`; this is the summary).
7. **Estimate & delivery plan** — sized effort and confidence for the build, with its evidential
   basis, and the phases/releases/waves.
8. **Open questions & risks** — what is unresolved or carried as a known risk (cross-references
   `RAID.md`).

Each fact lives in **one** section (an NFR appears in section 5, not also in section 4) — that keeps
reviews meaningful, since there is exactly one place a thing is supposed to be. This file is generated
and refined by the solution-architecture skill reading your codebase plus the files in this folder;
edit it freely afterwards — it is just markdown.

### `decisions/` — one ADR per decision

One Architecture Decision Record markdown file per genuinely contested call, numbered
(`0001-<slug>.md`, `0002-<slug>.md`, …). An ADR records the **question, the choice, the rationale, and
the compromises accepted**. Section 6 of the architecture is the digest; these are the full record.
Keeping decisions as first-class files (not buried in the design prose) is deliberate — contested
calls are easy to lose and expensive to relitigate.

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
not to, because Y" lines live, with a date and a link back to the decision or comment that settled
them. The point is that a future reader can see what was deliberately ruled out, so it is not silently
re-proposed (or silently re-built) six months later. Preserving the "why not" is as load-bearing as
preserving the "why".

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

- **Requirements never go on the portfolio Project board.** Requirements live **here** (or in the
  downstream project's own repo). The GitHub Project board shows only **phases** — Prototype, MVP,
  Pilot, Production, and ongoing Releases — as the portfolio-level view. The board answers "where is
  each project in its lifecycle"; this folder answers "what is the project, in detail". Keep the two
  separate: pushing requirements onto the board recreates the heavyweight tracker we are deliberately
  leaving behind.

- **No gates, no approvals, no orchestration engine.** This folder is a set of living documents, not a
  workflow with enforced transitions. The skills propose and question; a human decides and edits.
  Nothing here blocks anything — it is all light and advisory by design.
