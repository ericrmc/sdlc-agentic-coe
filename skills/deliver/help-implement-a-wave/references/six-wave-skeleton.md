# The six-wave cutover skeleton

> The canonical cutover shape is **six waves in one fixed order**. This is the
> **deterministic base** of `help-implement-a-wave` — identical for every migration,
> so emit it verbatim, then enrich each wave from the specific delta. Each wave carries a
> **default back-out PLAN** and **default go/no-go CRITERIA**; the plan states them, a
> specialist runs them. Plan and govern; never run the migration.

## The fixed order (load-bearing)

Stand up structure before moving data, move data before cutting traffic, configure
before validating, validate before decommissioning. **Do not drop, merge, or
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

The plan *states* these; it does **not execute** them. The source system stays the
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

These slots cannot be known by the plan — leave them for the human to curate, and raise
a `question` rather than guessing:

- **`moves_from_ref`** — the current/source system this wave migrates from (the human
  names the system).
- **`depends_on_wave_seq`** — a cross-wave dependency *beyond* the natural order, only
  where a real constraint exists; default `null`.
- **`downtime_minutes`** — the expected interruption in minutes; default `null` (the
  human's budget to fill). The runbook sums these into a total stated downtime.

## The rules

- **The six waves and their order are fixed.** Do not invent a seventh wave, merge two,
  or reorder. A near-empty wave keeps its slot.
- **Honest null beats a fabricated trace.** When no design section backs a wave, trace
  `null` — a signal, not a failure to fill in.
- **Govern, never run.** The plan produces a scaffold; a specialist runs it. Never
  execute a wave, a back-out, or a validation against a live system.
- **Status is the human's.** Waves are emitted status-less. The plan never sets a wave
  validated / complete or moves itself to accepted — disposition is a human act.
- **Light and advisory.** The value is the governed structure and the back-out / go/no-go
  text. The only hard decision points are the per-wave go/no-go gates a human evaluates
  before proceeding.
```