# Requirement Challenge Kinds — the closed 9-kind red-team vocabulary

This is the **definitive** vocabulary the requirements red-team uses. When a skill
or workflow red-teams a project's requirement set, every challenge it raises MUST
carry exactly one `kind` drawn from the nine values below — no others.

The `red-team-requirements` skill (`skills/challenge/red-team-requirements/`) cites
this file as its single source of truth. If that skill ships its own
`references/challenge-kinds.md`, that copy is a pointer back to **this** document.

This vocabulary is **advisory**. A challenge flags an issue and poses a question for
a human to triage; it never picks a winner, deletes scope, blocks acceptance, or
changes a requirement's status. A human decides every challenge.

---

## How a challenge is shaped

Each challenge a red-team pass produces is one object with:

- `kind` — exactly one of the nine values below.
- `message` — specific, references the real requirement id(s); never generic boilerplate.
- `suggested_action` — concrete and actionable (what to add / restate / reconcile), always leaving the verdict to the human.
- `requirement_id` — the real numeric id of the targeted requirement, OR `null` for a set-level challenge.
- `contests_id` — set **only** for a `conflicting` challenge (the partner requirement's id); omitted or `null` for every other kind.

Produce **one challenge per genuine issue**. Be conservative: a false `conflicting`
or false `gold_plated` corrodes trust — stay silent on mere ambiguity. Do not invent
requirements that are not in the set. Do not change status.

---

## The nine kinds (definitions)

Use each definition below as written. Do not paraphrase these when implementing a
red-team pass — they carry load-bearing guards (the both-ids rule, the
scoped-prohibition guard, the set-level NFR categories).

### 1. `vague`

> "vague" — references a control/term (e.g. CORS, an origin, a role) without naming the exact value, so it cannot be measured as written.

### 2. `unquantified`

> "unquantified" — a non-functional goal stated with NO number/target (e.g. "fast", "secure", "scalable").

### 3. `untestable`

> "untestable" — a subjective quality ("user-friendly", "intuitive", "seamless", "easy to use") with no observable acceptance criterion.

### 4. `solution_shaped`

> "solution_shaped" — names a mechanism/product/technology rather than the underlying need (solutioneering).

### 5. `orphan_value`

> "orphan_value" — no business outcome can be inferred; the requirement is not linked to value.

### 6. `conflicting`

> "conflicting" — two requirements genuinely contradict: contradictory quantified targets on the same subject, mutually-exclusive constraints (e.g. on-prem vs cloud-only), OR a LITERAL OPPOSITE / negation (one forbids what the other requires on the same subject, e.g. "must purge logs after 30 days" vs "must not purge logs"), OR heavy semantic overlap that is actually contested. Name BOTH ids: set `requirement_id` to the LOWER id and `contests_id` to the OTHER (higher) id. POSE the disambiguation question; NEVER choose a winner. Watch for SCOPED prohibitions that are NOT a true conflict (e.g. "must not retain logs CONTAINING card numbers" does not conflict with "retain logs 90 days") — do not flag those.

**The both-ids rule.** A `conflicting` challenge is the only kind that names two
requirements. Set `requirement_id` to the **lower** id and `contests_id` to the
**other (higher)** id. Every other kind omits `contests_id` or sets it `null`.

**The scoped-prohibition guard.** A prohibition that is *scoped* (forbids a narrow
case) does not conflict with a broad rule that permits the general case. "must not
retain logs CONTAINING card numbers" does **not** conflict with "retain logs 90
days" — do not flag those.

### 7. `gold_plated`

> "gold_plated" — reaches for extra scope ("nice to have", "ideally", "as well as", "stretch goal") with no business outcome to justify it. ASK whether the extra capability is required; do not drop scope.

### 8. `missing_nfr`

> "missing_nfr" — a SET-LEVEL gap: an entire NFR category is uncovered. Set `requirement_id` to null. Use ONLY these category names: security, availability, performance, data_residency, maintainability, scalability.

`missing_nfr` is **set-level**: it speaks to the requirement set as a whole, not a
single row, so `requirement_id` is `null`. The six — and only six — category names are:

| Category | Uncovered when nothing in the set addresses… |
|----------|----------------------------------------------|
| `security` | authn/authz, encryption, secrets, threat surface, audit |
| `availability` | uptime targets, failover, recovery, degraded modes |
| `performance` | latency/throughput targets, load behaviour |
| `data_residency` | where data physically lives / sovereignty constraints |
| `maintainability` | observability, supportability, operability, change cost |
| `scalability` | growth headroom, horizontal/vertical scaling limits |

### 9. `off_vision`

> "off_vision" — a requirement introduces a direction NOT reflected in the PROJECT VISION or the rest of the set — a possible UNINTENDED PIVOT by someone who cannot see the whole picture. ADVISORY only: flag it as a light steer to confirm against the north star; it never blocks acceptance. Only emit this when a vision is present and the drift is real.

---

## Shape examples

A non-functional goal with no target:

```json
{
  "kind": "unquantified",
  "message": "Requirement #12 states a non-functional goal with no number.",
  "suggested_action": "Add a target (e.g. p95 <= 500 ms) and the consequence of breach.",
  "requirement_id": 12
}
```

A true conflict — note **both** ids, lower as `requirement_id`:

```json
{
  "kind": "conflicting",
  "message": "Requirements #8 and #14 are direct opposites — #8 requires purging logs after 30 days; #14 forbids purging logs. Which holds, or do they apply to different scopes?",
  "suggested_action": "Reconcile the two (pick the binding rule or scope each). The agent does not choose a winner.",
  "requirement_id": 8,
  "contests_id": 14
}
```

A set-level NFR gap — `requirement_id` is `null`:

```json
{
  "kind": "missing_nfr",
  "message": "No requirement addresses DATA RESIDENCY.",
  "suggested_action": "Accept the suggested NFR in the coverage panel, or add your own.",
  "requirement_id": null
}
```

---

## Closed set — do not extend

These nine are the whole vocabulary. If a real issue does not fit one of them, that
is a signal to reconsider whether it is a requirements red-team finding at all (it
may belong to a different pass — design review, NFR catalogue, panel) rather than a
reason to invent a tenth kind. Keep the vocabulary closed so findings stay
comparable across projects and over time.
