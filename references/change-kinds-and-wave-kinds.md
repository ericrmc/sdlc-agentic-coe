# Change kinds & wave kinds — release verbs and migration waves

A small, closed-list reference the lifecycle skills cite by name. Two vocabularies live
here: the **four release change kinds** (the verbs that describe a delta) and the **six
ordered migration wave kinds** (the backbone of a cutover). Keep both lists closed — if a
new word seems needed, it almost always maps onto one of these.

> **The load-bearing insight.** A *phase*, a *release*, and a *migration wave* are all the
> same shape: a **scoped, versioned, traced DELTA over one source of truth**. None of them
> is a parallel universe with its own design document — each points at the canonical
> requirements/sections and moves a version of them forward. Two rules follow, and they are
> the whole reason this file exists:
>
> 1. **Every delta carries a `change_kind`** (what kind of move this is), and
> 2. **Every delta carries a trace to the ONE outcome it serves.**
>
> **A null trace IS the scope-creep signal.** It is not a bug to be cleaned up before
> review — it is the most useful thing a delta can tell you. An add or a change with no
> outcome behind it is work nobody asked for; surface it, ask "which outcome, or drop it?",
> and let a human answer. Do not invent a trace to make the null go away. An honest null
> beats a false trace every time.

---

## Part 1 — The four release `change_kind`s

Every release item, deferred feature, and backlog entry resolves to exactly **one** of
these four verbs. Classify by the item's **intent**, not just its wording — "improve the
export" is a `change`, even though it contains no literal "change".

| `change_kind` | One line | Verb heuristics (what to listen for) | Versioning effect |
|---|---|---|---|
| **`add`** | A new capability that did not exist | "add", "support", "enable", "introduce", "allow", "create", "new" | Inserts a new requirement, traced to its outcome |
| **`change`** | Revise existing behaviour; **supersedes** | "change", "improve", "extend", "revise", "update", "enhance", "refactor", "rename" | Supersedes the existing requirement (new version, old kept) |
| **`remove`** | Retire / drop existing scope | "remove", "retire", "deprecate", "drop", "sunset", "decommission", "delete" | A **retirement pointer**, never a hard delete; history preserved |
| **`patch`** | Fix a defect; **no scope change** | "fix", "correct", "repair", "resolve", "hotfix", "bug" | No requirement change; the record + notes only |

### Notes on each verb

- **`add` — new capability.** On acceptance this creates a new requirement row, derived
  from (and traced to) the outcome it serves. An `add` whose trace is null is the textbook
  scope-creep case: new work, no outcome. Flag it; don't silently accept it.

- **`change` — revise existing behaviour, supersedes.** This is the verb people under-use,
  because "improve / extend / enhance" don't *sound* like "change". They are. A `change`
  **supersedes** the prior requirement: the old version is retained (superseded), a new
  version becomes current. Nothing is lost; the chain records "what it used to say".

- **`remove` — a retirement pointer, not a delete.** Retiring scope is a *pointer*
  (`retired_in_release_id` and friends), never a destructive delete. History stays
  queryable. The important second-order effect: a `remove` that retires the **only**
  requirement under an outcome strands that outcome — surface it ("is the outcome being
  dropped too, or does it need new work?"). That is the `release-dropped-requirement`
  signal, the mirror image of scope creep.

- **`patch` — fix a defect, no scope change.** A patch changes no requirement and moves no
  section. It exists for the record and the release notes. Its trace, when set, points at
  the outcome whose *quality* it preserves (the export still serves BO-2; the patch keeps
  it working). A patch is the one verb where a null trace is unremarkable — it fixes
  something, it doesn't reshape scope.

### Anti-patterns (classification smells)

- **Forcing a trace to dodge the null.** The null is the signal. Inventing `BO-2` to avoid
  an awkward conversation is the worst outcome — it launders scope creep into "governed".
- **Calling everything `change`.** If it didn't exist before, it's `add`. If it's a bug,
  it's `patch`. Reserve `change` for "this behaviour existed and now behaves differently".
- **Using `remove` to mean delete.** Removal is retirement. If you find yourself wanting to
  erase history, you've reached for the wrong verb.
- **Bundling a patch into a `change`.** A defect fix that also quietly extends behaviour is
  two items, two verbs. Split them so the release notes tell the truth.

---

## Part 2 — The six ordered migration `wave_kind`s

A migration (a cutover from a current system to a target) is a **delta too** — the same
shape, expressed as an ordered sequence of waves. The order is canonical and load-bearing;
later waves depend on earlier ones. Each wave traces a real target design section where one
exists, and carries a **back-out plan** and **go/no-go criteria** that a human owns.

> The lifecycle skills PLAN and STATE a cutover; they never RUN it. A skill names the
> back-out plan and the validation criteria — it does not execute them.

| # | `wave_kind` | What it does | Traces (preferred section) | Back-out plan | Go/no-go criteria |
|---|---|---|---|---|---|
| 1 | **`schema`** | Stand up the target structure | `application_architecture` | Tear down the new structure; the source stays system of record | Target structure created and reachable; live system untouched |
| 2 | **`data`** | Migrate the data to the target | `application_architecture` | Halt the load, leave source unchanged; load is re-runnable (idempotent) | Row counts reconcile source↔target; sampled records match; no data loss |
| 3 | **`cutover`** | Cut traffic over to the target | `application_architecture` | Repoint traffic to the source (kept warm until decommission) | Health checks green; key journeys pass; errors within budget |
| 4 | **`config`** | Apply environment & integration config | `key_decisions` | Restore the prior configuration snapshot | Integrations connect; secrets resolve; config matches agreed decisions |
| 5 | **`validation`** | Validate against acceptance criteria | `requirements_acceptance` | Not applicable — validation is read-only | Acceptance criteria for migrated outcomes pass; stakeholders sign off |
| 6 | **`decommission`** | Decommission the source system | *(none — no section behind it)* | Re-provision the source from backup within the retention window | Source idle for the agreed soak period; backups retained; access revoked |

### Why this order, and why it's closed

- **The order encodes dependency.** You cannot migrate `data` before the `schema` exists;
  you cannot `cutover` before the data is there; you cannot `decommission` before
  `validation` signs off. The sequence is the dependency graph drawn straight.
- **A wave is emitted whether or not its section exists.** When the preferred section is
  present, the wave traces it. When it is absent, the trace is **null** — an honest "no
  design behind this yet" signal, the migration sibling of the null-trace scope-creep
  signal above. Same discipline, same meaning: a null is information, not an error.
- **`validation`'s back-out is "not applicable"** by design — validation is read-only, so
  there is nothing to roll back. Stating that explicitly is part of an honest runbook.
- **`decommission` is last and deliberately unhurried.** A retention window, a soak period,
  retained backups — the same "retire by pointer, never destroy" instinct as the `remove`
  change kind. Removal (of a requirement) and decommission (of a system) are the same idea
  at two altitudes.

### Anti-patterns (sequencing smells)

- **Reordering the waves.** If your plan needs `data` before `schema`, the plan is wrong,
  not the list. The order is the safety property.
- **Skipping `validation`.** Cutting over and decommissioning without an acceptance gate is
  how a migration silently loses data. Validation is the wave that earns the decommission.
- **Treating `decommission` as a delete.** Re-provisionable-from-backup within a retention
  window is the bar. If the source can't be restored, you decommissioned too early.
- **Inventing a seventh wave.** "Comms", "training", "monitoring" are activities *within*
  these waves (often within `config` and `validation`), not new wave kinds.

---

## How the skills use this file

These two closed lists are the shared vocabulary the lifecycle skills lean on:

- **`describe-phases-releases-waves`** — uses both lists to structure a delivery roadmap:
  phases as maturity milestones, releases tagged with `change_kind`s, migrations expressed
  as the six ordered waves.
- **`help-implement-a-wave`** — walks one migration `wave_kind` at a time, naming its
  back-out plan and go/no-go criteria from the table above before doing the work.
- **`triage-backlog-and-defer`** — classifies each backlog item into one of the four
  `change_kind`s and traces it to an outcome (or emits an honest null).
- **`scope-reconcile-check`** — reads the trace on every delta and surfaces the nulls: an
  `add`/`change` with no outcome (scope creep), a `remove` that strands an outcome (dropped
  requirement), a wave with no section behind it (undesigned step).

The single sentence to carry into every one of them: **a delta with a `change_kind` and a
trace to one outcome is governed; a delta with a null trace is the conversation worth
having.**
