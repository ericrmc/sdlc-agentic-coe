# The six-wave cutover skeleton

> The canonical cutover shape is **six waves in one fixed order**. This is the
> **deterministic spine** of `help-implement-a-wave` — identical for every migration,
> so emit it verbatim, then enrich each wave from the specific delta. Each wave carries a
> **default back-out PLAN** and **default go/no-go CRITERIA**; the planner states them, a
> specialist runs them. You **plan and govern; you never run the migration.**
>
> Grounded in the source app's `_SKELETON`
> (`backend/app/services/migration_agent.py`): same six `wave_kind`s, same fixed order,
> same default rollback/validation text, same "trace a real section or honest null"
> rule.

## The fixed order (load-bearing)

You stand up structure before you move data, move data before you cut traffic, configure
before you validate, validate before you decommission. **Do not drop, merge, or
re-sequence the six.** A near-empty wave (e.g. greenfield decommission) keeps its slot.

| # | `wave_kind` | What it does | Preferred traced section |
|---|-----------|--------------|--------------------------|
| 1 | `schema` | Stand up the target structure | `application_architecture` |
| 2 | `data` | Migrate the data to the target | `application_architecture` |
| 3 | `cutover` | Cut traffic over to the target | `application_architecture` |
| 4 | `config` | Apply environment & integration config | `key_decisions` |
| 5 | `validation` | Validate against the acceptance criteria | `requirements_acceptance` |
| 6 | `decommission` | Decommission the source system | (none — honest null) |

A wave is emitted **whether or not its preferred section exists.** When the section is
present, the wave traces it (`derives_from_section_key`); when it is absent, the wave
traces `null` — itself a useful signal ("there is no design behind this step yet — flag
it"). Never fabricate a section key to make a wave look grounded.

## Per-wave defaults (back-out PLAN + go/no-go CRITERIA)

The planner *states* these; it does **not execute** them. The source system stays the
system of record until decommission, so most back-outs are "stop, keep the source
untouched, repoint to it." `validation` is the honest exception — it is read-only, so
its back-out is "not applicable."

### 1 · `schema` — Stand up the target structure
- **Back-out PLAN:** Tear down the new structure; the source system stays the system of
  record.
- **Go/no-go CRITERIA:** Target structure created and reachable; the live system is
  untouched.

### 2 · `data` — Migrate the data to the target
- **Back-out PLAN:** Halt the load and keep the source data unchanged; the load is
  re-runnable (idempotent).
- **Go/no-go CRITERIA:** Row counts reconcile source vs target; sampled records match;
  no data loss.

### 3 · `cutover` — Cut traffic over to the target
- **Back-out PLAN:** Repoint traffic to the source system (kept warm until
  decommission).
- **Go/no-go CRITERIA:** Health checks green on the target; key journeys pass; errors
  within the budget.

### 4 · `config` — Apply environment & integration config
- **Back-out PLAN:** Restore the prior configuration snapshot.
- **Go/no-go CRITERIA:** Integrations connect; secrets resolve; config matches the
  approved decisions.

### 5 · `validation` — Validate against the acceptance criteria
- **Back-out PLAN:** Not applicable — validation is read-only.
- **Go/no-go CRITERIA:** Acceptance criteria for the migrated outcomes pass;
  stakeholders sign off.

### 6 · `decommission` — Decommission the source system
- **Back-out PLAN:** Re-provision the source from backup within the retention window.
- **Go/no-go CRITERIA:** Source idle for the agreed soak period; backups retained;
  access revoked.

## What every wave also carries (left for the human)

These slots the planner **cannot** know — leave them for the human to curate, and raise
a `question` rather than guessing:

- **`moves_from_ref`** — the current/source system this wave migrates from (the human
  names the system; the planner does not know it).
- **`depends_on_wave_seq`** — a cross-wave dependency *beyond* the natural order, only
  where a real constraint exists; default `null`.
- **`downtime_minutes`** — the expected interruption in minutes; default `null` (the
  human's budget to fill). The runbook sums these into a total stated downtime.

## The rules

- **The six waves and their order are fixed.** Do not invent a seventh wave, merge two,
  or reorder. A near-empty wave keeps its slot.
- **Honest null beats a fabricated trace.** When no design section backs a wave, trace
  `null` — a signal, not a failure to fill in.
- **Govern, never run.** The planner produces a scaffold; a specialist runs it. Never
  execute a wave, a back-out, or a validation against a live system.
- **Status is the human's.** Waves are emitted status-less. The planner never sets a wave
  validated / complete or moves the plan to accepted — disposition is a human act.
- **Light and advisory.** No gate, no state-machine that blocks. The value is the
  governed structure and the back-out / go/no-go text, not enforcement.
