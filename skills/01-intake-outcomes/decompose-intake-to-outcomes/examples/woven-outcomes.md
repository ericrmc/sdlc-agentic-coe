# Example — woven outcomes (few-shot)

A complete worked example. Use it as a few-shot reference: this is the shape,
density, and discipline a good weave produces. The intake is deliberately
modest (a few sentences) — note how the outcomes stay grounded and how no
requirement names a technology.

---

## The intake (input)

> **Project:** Field Service Mobile
>
> Our field technicians service equipment at customer sites, many of which are
> in basements, plant rooms, and rural areas with no mobile signal. Today they
> carry paper job sheets and re-key everything into the back-office system when
> they return — typically losing the best part of an hour per technician per
> day, and we regularly find jobs keyed days late or not at all. Customers have
> started asking for proof a job was actually completed and when. The
> operations manager needs to see, by the end of each day, which jobs are still
> open. Whatever we build has to be usable one-handed on a phone while the other
> hand is holding a tool, by technicians who are not especially tech-confident.

---

## The weave (output)

```markdown
# Woven outcomes — Field Service Mobile

> Derived from intake by the Weaver. Each outcome is a business benefit a
> stakeholder ratifies; each requirement derives from exactly one outcome.
> Ratify by merging this PR.

## Outcome BO-1 — Offline Job Completion
**Outcome:** Technicians can complete assigned jobs at a customer site with no
mobile signal, and have that work captured without re-keying later.
**Why:** Intake — sites "in basements, plant rooms, and rural areas with no
mobile signal"; technicians "re-key everything ... losing the best part of an
hour."

### TR-1.1  (F)
- **derives_from:** BO-1
- The system shall allow a technician to view, update, and mark complete any
  job assigned to them while the device has no network connectivity.
- **Acceptance:** GIVEN a technician with assigned jobs and no connectivity,
  WHEN they mark a job complete, THEN the completion is recorded on the device
  and shown in their job list without error.
- **Rationale:** The core complaint — work must be capturable at the no-signal
  site, not re-keyed on return.

### TR-1.2  (F)
- **derives_from:** BO-1
- The system shall transfer job updates recorded offline to the back-office
  system automatically once connectivity is restored, without technician action.
- **Acceptance:** GIVEN job updates recorded offline and restored connectivity,
  WHEN connectivity returns, THEN every pending update reaches the back office
  and any that cannot is reported to the technician.
- **Rationale:** Removes the "keyed days late or not at all" failure; the
  reconcile half of the offline outcome.

### TR-1.3  (NF)
- **derives_from:** BO-1
- Offline-held job data must remain available without connectivity for at least
  a full working shift (target: >= 12 hours).
- **Rationale:** Bounds "offline" to a verifiable target grounded in a day's
  work implied by the intake.

## Outcome BO-2 — Proof Of Completion
**Outcome:** The business can show a customer that a specific job was completed
and exactly when.
**Why:** Intake — "customers have started asking for proof a job was actually
completed and when."

### TR-2.1  (F)
- **derives_from:** BO-2
- The system shall record, for each completed job, the time of completion and
  the identity of the technician who completed it.
- **Acceptance:** GIVEN a completed job, WHEN its record is retrieved, THEN it
  shows the completion timestamp and the completing technician.
- **Rationale:** The minimum factual basis for "proof a job was completed and
  when."

### TR-2.2  (NF)
- **derives_from:** BO-2
- A recorded job completion must not be silently altered or deleted; any change
  must be attributable and recoverable.
- **Rationale:** "Proof" is only proof if the record is trustworthy; serves the
  auditability the customer demand implies.

## Outcome BO-3 — End-Of-Day Visibility
**Outcome:** The operations manager can see, by the end of each day, which jobs
remain open.
**Why:** Intake — "the operations manager needs to see, by the end of each day,
which jobs are still open."

### TR-3.1  (F)
- **derives_from:** BO-3
- The system shall present, on demand, the set of jobs that are not yet marked
  complete, distinguishable from completed jobs.
- **Acceptance:** GIVEN a mix of open and completed jobs, WHEN the operations
  manager views the day's jobs, THEN open jobs are listed and clearly separated
  from completed ones.
- **Rationale:** Directly the manager's stated need.

### TR-3.2  (NF)
- **derives_from:** BO-3
- A job completed offline must appear as open to the operations manager only
  until it reconciles, and as completed within a bounded window after
  connectivity returns (target: <= 5 minutes).
- **Rationale:** Reconciles BO-3's visibility with BO-1's offline capture so the
  manager is not misled by in-flight work.

## Outcome BO-4 — One-Handed Field Usability
**Outcome:** A technician can operate the tool one-handed on a phone, at a site,
without being especially tech-confident.
**Why:** Intake — "usable one-handed on a phone while the other hand is holding
a tool, by technicians who are not especially tech-confident."

### TR-4.1  (NF)
- **derives_from:** BO-4
- Every action required to view and complete a job must be operable one-handed
  on a phone-sized screen, with touch targets and flows that pass an
  established mobile-accessibility bar.
- **Rationale:** The stated usability constraint; left measurable against an
  accessibility standard rather than a framework.

### TR-4.2  (NF)
- **derives_from:** BO-4
- A technician must be able to complete a job in a number of steps a
  first-time, non-technical user can perform without training (target:
  validated by unmoderated task success >= 90% with field technicians).
- **Rationale:** Operationalises "not especially tech-confident" as a testable
  target.
```

---

## What to notice

- **Four outcomes, in range (3-6), all benefits.** Not one names a technology.
  "Offline job completion," not "a sync engine."
- **Every requirement traces up.** `TR-2.1` -> `BO-2` -> the customer's
  proof demand in the intake. Strike `BO-2` and `TR-2.*` falls with it.
- **NFRs carry targets.** ">= 12 hours", "<= 5 minutes", ">= 90% task success" —
  not "fast" or "easy".
- **No-HOW held throughout.** TR-4.1 says "pass an established
  mobile-accessibility bar" — a WHAT — and leaves the standard and the
  implementation to the downstream a11y / design-review skill and the
  component-pattern library.
- **The cross-outcome tension is captured, not hidden.** TR-3.2 names the
  reconcile window so BO-1's offline capture doesn't quietly break BO-3's
  visibility — surfaced as a requirement for the red-team skill to pick up.
