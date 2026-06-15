# Few-shot: `conflicting` vs a scoped prohibition

The single most trust-destroying mistake the critic can make is flagging a **false**
conflict. The frequent culprit is a **scoped prohibition** — a "must not …" that applies
only to a *subset*, mistaken for a blanket opposite. This few-shot teaches the guard.

A negated clause is **scoped** (and therefore NOT a conflict) when it carries a
scope/condition marker: *containing, when, unless, except, older than, raw, only, if*.

---

## DO flag — true blanket opposite

```
#8  The system must purge audit logs after 30 days.
#14 The system must not purge audit logs.
```

Same subject (audit logs). One mandates purging; the other forbids purging — with **no
scope marker** on the prohibition. These cannot both hold. Emit:

```json
{
  "kind": "conflicting",
  "message": "Requirements #8 and #14 are direct opposites — #8 requires purging audit logs after 30 days; #14 forbids purging audit logs. Which holds, or do they apply to different scopes?",
  "suggested_action": "Reconcile the two (pick the binding rule or scope each). The agent does not choose a winner.",
  "requirement_id": 8,
  "contests_id": 14
}
```

Note: `requirement_id` is the LOWER id (8); `contests_id` is the higher (14). The message
poses the question and names both ids; it does not say which one wins.

---

## Do NOT flag — scoped prohibition

```
#8  Retain logs for 90 days.
#14 The system must not retain logs CONTAINING card numbers.
```

The prohibition in #14 is scoped by **"containing card numbers"** — it forbids retaining
a *subset* of logs (those with PAN data), not logs in general. Both can hold
simultaneously: retain logs for 90 days, but scrub/exclude card numbers from them. This
is a real-world data-protection pattern, not a contradiction. **Emit nothing** for this
pair.

---

## More scoped cases that must stay silent

| pair | why it is NOT a conflict |
|------|--------------------------|
| "Retain events 1 year" vs "must not retain raw events **older than** 30 days" | scoped by time window (`older than`) — different subsets |
| "Cache responses" vs "must not cache **when** the user is unauthenticated" | scoped by condition (`when`) |
| "Log all requests" vs "must not log request bodies **except** for errors" | scoped by exception (`except`) |
| "Store uploads" vs "must not store uploads **unless** virus-scanned" | scoped by precondition (`unless`) |

---

## Contrast cases that DO flag

| pair | why it IS a conflict |
|------|----------------------|
| "p95 latency ≤ 200 ms" vs "p95 latency ≤ 2 s" on the same endpoint | contradictory quantified targets, same subject |
| "Deploy on-prem only" vs "Deploy cloud-only" | mutually-exclusive constraint pair |
| "Availability ≥ 99.99%" vs "Availability ≥ 99.0%" for the same service | different percentage targets, same subject |
| "Must purge PII on request" vs "must not delete any user record" (same subject, unscoped) | literal opposite on a shared subject |

---

## The rule, distilled

1. Same subject? If not — never a conflict.
2. Does the negated/contested clause carry a scope marker (*containing, when, unless,
   except, older than, raw, only, if*)? If yes — **scoped**, stay silent.
3. Hard signal (contradictory numbers / exclusive pair / unscoped negation)? Only then
   flag — and **pose** the disambiguation, naming both ids, never choosing a winner.

When in doubt, prefer silence. Precision over recall — a false conflict corrodes trust.
