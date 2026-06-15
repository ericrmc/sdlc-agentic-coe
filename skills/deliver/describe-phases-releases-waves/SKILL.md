---
name: describe-phases-releases-waves
description: Lay out a project's life past 'built' — UAT-gated maturity phases (Prototype->MVP->Pilot->Production with a light advisory checklist) then releases (add/change/remove/patch deltas, each traced to one outcome, null-trace = scope-creep signal); emit a deterministic release-notes projection grouped by change_kind.
one_liner: Plan a project's maturity phases and traced release stream.
aliases: [release planning, delivery phases, rollout plan, release notes, roadmap phases, change log, MVP to production, scope creep check]
when_to_use: planning a project's delivery lifecycle and release stream past the prototype
output_kinds: [proposal, menu]
deterministic_fallback: the four-phase ladder + the change_kind release-notes grouping
suggested_tier: frontier
neighbours: Comes after architect/reconcile-as-built (the design is settled against reality). Comes before deliver/help-implement-a-wave (planning one wave's cutover).
---

# describe-phases-releases-waves — phases, releases, and the delta model

## 1. Purpose

Lay out a project's life past 'built': its maturity phases and its ongoing stream of releases.

A project's life does not stop at the first prototype. After it is built it moves through **maturity
phases** — and then never stops changing: a stream of new features, revisions, retirements, and patches.

This skill structures that whole life so two questions are always answerable:

- **Where is this project in its maturity?** (Prototype → MVP → Pilot → Production)
- **What changed, and why, release over release?** — the thing a ticket pile can never tell you.

It does so with **one load-bearing insight**:

> **A phase, a release, and a migration are all the same shape: a scoped, versioned, traced DELTA over one
> source of truth.** They are not parallel universes. A phase is a labelled checkpoint over the design. A
> release is a named envelope of requirement deltas. Each delta carries a `change_kind` and a trace to the
> **one** outcome it serves. Nothing is ever deleted — `remove` is a retirement pointer, `change` supersedes.

Everything here is **light and advisory**. No transition is blocked. The maturity phases become the
**columns of the downstream GitHub Project**; the releases become a deterministic, traceable record readable
top to bottom. The acceptance checklist is a checklist a human signs off — not a wall the work has to climb.

## When to use

Use this when a project is past its prototype and you need to plan its delivery lifecycle and its ongoing
release stream:

- standing up the **phase columns** for a downstream project's GitHub Project board,
- turning a **backlog / pile of tickets** into a scoped, traced release,
- producing **release notes** that cite which outcome each change served,
- deciding whether a proposed change is real scope or quiet **scope creep**.

Do **not** use this to author solution design — a release holds no design. It points at requirements and
outcomes that already exist. With no outcomes yet, run the requirements/outcomes skills first; a release with
nothing to trace to is all creep.

## Inputs (what the user supplies)

Paste or point the skill at:

1. **The accepted outcomes** — each with a stable key (e.g. `BO-2`, `REQ-7`) and one line of text. These
   are the *only* things a change may trace to. May be sparse — that is fine and honest.
2. **The backlog** — a pasted list of desired changes / tickets / one-liners. One item per line. (A direct
   Jira/GitHub ingest is a future seam; today the list is pasted.)
3. **Optionally, the current phase** — which maturity milestone this release belongs to, if any.
4. **Optionally, acceptance criteria** per outcome — for the UAT checklist projection.

No codebase or design doc is needed. This skill works entirely off keys, outcome text, and the backlog.

## The method as numbered STEPS

The method has a **deterministic base** (Steps 1, 4, 6 — runnable with no model at all) and **one model
reasoning step** (Step 5 — the classify-and-trace judgement). Preserve both.

### STEP 1 — Lay out the four-phase ladder (DETERMINISTIC)

Establish the maturity phases. These are fixed and ordered; a project may **skip** one (seq is the real order
it entered, not the canonical 1-2-3-4). Each carries a **light advisory UAT acceptance checklist** and a
human **sign-off** — and nothing more. The checklist is read, ticked, and signed; it never blocks.

| Phase | What it is | Light acceptance check |
|---|---|---|
| **Prototype** | Throwaway, to see and feel. | quick look — does it demo the idea? |
| **MVP** | The first real, narrow slice in users' hands. | UAT checklist + sign-off |
| **Pilot** | A controlled rollout to a limited cohort. | UAT checklist + sign-off |
| **Production** | General availability. | UAT checklist + go-live sign-off |

> **These four phases are exactly the columns of the downstream GitHub Project.** Each downstream project gets
> its own GitHub Project; this skill names the columns and what "done enough to move right" means in each. The
> board tracks *phases*, never individual requirements.

The UAT checklist is advisory: for each outcome the phase covers, one line — *"Outcome `BO-2` (auditors can
self-serve evidence): covered by REQ-7, REQ-9 — observed working?"* — with a checkbox and a place for a human
name + date. A human ticks and signs. Capture `pass`, `pass with conditions` (note the conditions), or `send
back` (note the findings). None of these are enforced; they are a record.

### STEP 2 — Pointer-snapshot the design at phase entry (DETERMINISTIC, advisory)

When a phase is entered, record **which version of the design was current** — a pointer, never a copy. In a
GitHub-native setup this is just the commit SHA (or the doc tag) the phase entered against. "Show me the
design as it was at MVP entry" becomes a `git` query, not a duplicated document. Cheap, honest, no drift.

### STEP 3 — Open a release as a named envelope (DETERMINISTIC)

A release is a **named, versioned envelope** with: a stable key (`REL-3`), a title, and a one-line **intent**
("why this release"). It belongs to at most one phase. It holds **no design** — only a set of deltas.
Replanning a release makes a new version of it; the old version is kept, never overwritten.

### STEP 4 — Classify every backlog item by `change_kind` (DETERMINISTIC)

For each backlog line, pick exactly one `change_kind` by the item's **intent** (not just its wording). The
deterministic verb heuristic — the fallback runnable with no model — is, in priority order (first match wins,
because `remove` is the strongest signal):

| `change_kind` | Trigger verbs (heuristic) | Means |
|---|---|---|
| `remove` | remove, drop, retire, delete, deprecate | retire existing scope — a **pointer**, never a delete |
| `patch` | fix, patch, hotfix, bug, correct | fix a defect — **no scope change** |
| `change` | change, update, revise, tighten, rework, modify | supersede existing behaviour (new version) |
| `add` | add, introduce, build, ship, support, enable, create | new capability (default for an unqualified line) |

An unqualified line defaults to `add`. See `references/change-kinds.md` for what each kind does to the
underlying requirement graph and why nothing is ever deleted.

### STEP 5 — Trace each item to the ONE outcome it serves (THE MODEL REASONING STEP)

This is the judgement call and the heart of the method. For each item, set `derives_from` to the
key of the **one** accepted outcome the change genuinely serves — copied **exactly** from the supplied
outcomes. The rules:

- Use the outcome the change *serves*, not the one it merely mentions.
- Copy the key **exactly**. Never invent a key. Never force a weak match.
- **An honest `null` is better than a false trace.** If no accepted outcome backs the item, set the trace to
  `null`. **That null IS the deliberate scope-creep signal** — it is not a failure, it is the method working.
  It says, in writing: *"this is work with no outcome behind it; trace it or drop it."*

The deterministic fallback (Step 4's sibling) is a token-overlap match: require at least two shared meaningful
tokens between the item and an outcome's text to claim a trace, else `null`. A frontier-tier model does this
far better — it reads intent, not keywords — but the fallback keeps the skill runnable with no model.

Write a one-or-two-sentence **rationale** per item: when traced, name the outcome and why it serves it; when
null, say plainly that no accepted outcome backs it, so it reads as scope creep until a trace is set.

> **Propose, never dispose.** This step *proposes*. It issues no verdict, no status, no approval. A human
> accepts or rejects each proposed change. Keep that line bright: the output is a menu of proposals, not a
> decision.

### STEP 6 — Project the release notes, grouped by `change_kind` (DETERMINISTIC)

The release notes are a **pure projection** of the accepted changes — nothing hand-authored, nothing left to
drift. Group by `change_kind` under fixed headings, and cite every line's key and traced outcome:

```
add    → ## Added
change → ## Changed
patch  → ## Fixed
remove → ## Removed
```

Every byte comes from fields that already exist (key, kind, trace, rationale), so this runs with no model.
See `references/release-notes-projection.md` for the exact deterministic projection algorithm and the heading
order.

The persuasive **narrative / comms-deck** version of the notes is a separate, optional model pass on top —
the structured projection here is the reliable floor that is always correct.

## Output format

The user gets back two markdown artefacts: **(A)** a phase ladder for the GitHub Project columns, and **(B)** a
release proposal + its notes projection. Concrete templates:

### (A) Phase ladder — the downstream GitHub Project columns

```markdown
## Maturity phases (GitHub Project columns)

| seq | Phase | Entered against | Light acceptance check |
|----:|-------|-----------------|------------------------|
| 1 | Prototype  | (commit/tag)  | demo'd the idea — signed off: <name>, <date> |
| 2 | MVP        | a1b2c3d       | UAT checklist below — sign-off pending |
| 3 | Pilot      | —             | not yet entered |
| 4 | Production | —             | not yet entered |

### MVP — UAT acceptance checklist (advisory)
- [ ] Outcome **BO-2** (auditors can self-serve evidence): covered by REQ-7, REQ-9 — observed working?
- [ ] Outcome **BO-4** (approvals are traceable): covered by REQ-11 — observed working?
- Sign-off: ______________  Date: __________  Outcome (advisory): accepted / accepted-with-follow-ups / not-yet
- Conditions / findings: ______________________________________________
```

### (B) Release proposal — the traced delta menu

```markdown
## REL-3 — Q3 audit & export improvements
Intent: give auditors self-serve evidence without raising a ticket.

| change_kind | item | traces to | status |
|-------------|------|-----------|--------|
| add    | CSV export on the approvals dashboard | BO-2 | proposed |
| change | tighten the audit-log retention to 7y | BO-4 | proposed |
| patch  | fix timezone drift in audit timestamps | _null — scope creep_ | proposed |
| remove | retire the legacy XML export | BO-2 | proposed |

> The `patch` line has **no outcome behind it**. That null is the deliberate scope-creep flag:
> trace it to an outcome or drop it before this release ships.
```

### (B continued) Release notes — the deterministic projection

```markdown
# REL-3 — Q3 audit & export improvements

give auditors self-serve evidence without raising a ticket.

## Added
- **CSV export on the approvals dashboard** — traces to BO-2: the self-serve mechanism for BO-2.

## Changed
- **Audit-log retention → 7y** — traces to BO-4: keeps approvals traceable for the full audit window.

## Fixed
- **Timezone drift in audit timestamps** — no outcome (scope creep): trace before shipping.

## Removed
- **Legacy XML export** — traces to BO-2: superseded by the new CSV export.
```

## Notes / anti-patterns

- **Do not invent a trace.** A forced weak match is worse than an honest null. The null is a feature: it is
  how scope creep becomes visible. Suppressing it defeats the whole method.
- **Do not delete.** `remove` is a retirement pointer; `change` supersedes with a new version. History is
  always preserved — "what was this before REL-3?" must stay answerable.
- **One outcome per delta.** If an item genuinely serves two outcomes, it is probably two items. Forcing
  many-to-one traces makes the release notes lie.
- **Keep it advisory.** The UAT checklist is signed, not enforced; the phase ladder is a board, not a
  blocker. If work gets blocked on a disposition, the method's light posture has been lost.
- **Phases are columns, not requirements.** The downstream GitHub Project tracks phases. Do not push
  individual requirements onto that board — each downstream project owns its own finer-grained tracking.
- **Classify by intent, not keyword.** "Improve the export" is a `change`, not an `add`, even though it has
  no `change` verb. The verb heuristic is the floor; a frontier-tier read does better.
- **Release notes are a projection, never hand-authored.** If someone edits the notes by hand, they will
  drift from the deltas. Regenerate them from the accepted changes every time.

## References

- `references/change-kinds.md` — the four `change_kind`s, what each does to the requirement graph, and why
  nothing is ever deleted.
- `references/release-notes-projection.md` — the exact deterministic release-notes projection: heading order,
  grouping, and the per-line trace citation.
