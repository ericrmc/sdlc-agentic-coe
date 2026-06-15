# Challenge kinds — the closed vocabulary

`kind` MUST be exactly one of these **nine** values. No others. A challenge that does
not fit a kind is probably not a challenge — resist inventing a tenth.

Each entry gives the precise definition and the `requirement_id` / `contests_id` rule.

| kind | definition | `requirement_id` | `contests_id` |
|------|------------|------------------|---------------|
| `vague` | References a control/term (e.g. CORS, an origin, a role) without naming the exact value, so it cannot be measured as written. | the targeted id | — |
| `unquantified` | A non-functional goal stated with NO number/target (e.g. "fast", "secure", "scalable"). | the targeted id | — |
| `untestable` | A subjective quality ("user-friendly", "intuitive", "seamless", "easy to use") with no observable acceptance criterion. | the targeted id | — |
| `solution_shaped` | Names a mechanism/product/technology rather than the underlying need (solutioneering). | the targeted id | — |
| `orphan_value` | No business outcome can be inferred; the requirement is not linked to value. | the targeted id | — |
| `conflicting` | Two requirements genuinely contradict (see below). POSE the disambiguation; NEVER choose a winner. | the **LOWER** id of the pair | the **OTHER (higher)** id |
| `gold_plated` | Reaches for extra scope ("nice to have", "ideally", "as well as", "stretch goal") with no business outcome to justify it. ASK whether the extra capability is required; do not drop scope. | the targeted id | — |
| `missing_nfr` | A SET-LEVEL gap: an entire NFR category is uncovered. | **null** | — |
| `off_vision` | A requirement introduces a direction NOT reflected in the project vision or the rest of the set — a possible unintended pivot. ADVISORY only; never blocks. | the targeted id | — |

## `conflicting` — the full definition

Two requirements genuinely contradict when:

- they state **contradictory quantified targets on the same subject** (two different time
  magnitudes normalised to a common unit, or two different percentages), OR
- they assert **mutually-exclusive constraints** — a known hard-opposite pair such as
  on-prem vs cloud-only, multi-region vs single-region, synchronous vs asynchronous,
  stateless vs stateful, offline vs always-online, OR
- one is a **literal opposite / negation** of the other — it forbids what the other
  requires on the same subject (e.g. *"must purge logs after 30 days"* vs *"must not purge
  logs"*), OR
- they have **heavy semantic overlap that is actually contested** (advisory / softer
  signal — surface as "may be duplicative or contested", do not assert a hard conflict).

Rules for `conflicting`:

- **Name BOTH ids.** `requirement_id` = the LOWER id, `contests_id` = the OTHER (higher)
  id. This makes the challenge stable under input reordering.
- **Shared subject required.** Only flag requirements about the same thing (content-word
  overlap; stop-words and high-frequency project vocabulary excluded).
- **Scoped-prohibition guard.** A prohibition qualified by *containing / when / unless /
  except / older than / raw / only / if* is **scoped**, not a blanket opposite — do NOT
  flag it. See `../examples/conflicting-vs-scoped.md`.
- **Pose, never choose.** Ask *"Which requirement holds — or do they apply to different
  scopes?"* and leave the verdict to the human.
- **Precision over recall.** A false conflict corrodes trust. Fire only on a hard signal;
  stay silent on mere ambiguity.

## `missing_nfr` — the six categories (set-level)

`missing_nfr` is the only kind with a **null** `requirement_id`. Use ONLY these category
names — one challenge per uncovered category, at most:

| category | covers |
|----------|--------|
| `security` | authn/authz, encryption, secrets, audit, threat surface |
| `availability` | uptime targets, failover, recovery (RTO/RPO) |
| `performance` | latency, throughput, resource budgets |
| `data_residency` | where data may live/transit; jurisdictional constraints |
| `maintainability` | observability, change cost, documentation, supportability |
| `scalability` | growth in load/users/data without redesign |
