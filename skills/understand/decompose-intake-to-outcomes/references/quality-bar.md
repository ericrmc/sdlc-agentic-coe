# Quality bar — outcomes & derived requirements

The standard every item must meet before it is handed back for ratification.
Advisory, not enforced — but if an item fails a test, rewrite or strike it.

## The five tests (every requirement)

Run each requirement through all five. A pass requires all five.

### 1. Atomic
One capability or constraint per requirement — **not a bundle**.

- Fail: *"The system shall sync data, notify the technician, and log the
  reconciliation."* (three requirements)
- Pass: *"The system shall reconcile locally-recorded changes to the system of
  record when connectivity is restored."*

Test: can you imagine accepting one half and rejecting the other? If yes, split.

### 2. Verifiable
Phrased so a tester can confirm it is met. A functional requirement earns a
Given/When/Then; a non-functional requirement names a **measurable target**.

- Fail: *"The system shall handle errors gracefully."* (what does "gracefully"
  mean to a tester?)
- Pass: *"GIVEN a failed reconciliation, WHEN connectivity returns, THEN the
  technician is shown the specific job that failed and a retry action."*

Test: could two testers disagree on whether it passed? If yes, sharpen it.

### 3. Free of solution detail (no-HOW)
State **WHAT** is required, never **HOW** to build it. No technology, framework,
storage engine, cloud, or implementation choice. This is the most-violated
test — be ruthless.

- Fail: *"The system shall cache jobs in IndexedDB via a service worker."*
- Pass: *"The system shall make assigned jobs viewable and editable without
  network connectivity."*

Test: does the words name something that would appear in an architecture
diagram or a `package.json`? If yes, it is HOW — strip it. The HOW belongs to
the downstream project, guided by the component-pattern skills.

### 4. Grounded in the intake
Traceable to something the intake text actually says or directly implies. **Do
not invent scope.**

- Fail: adding a "multi-language support" requirement to an intake that never
  mentions language or locale.
- Pass: a requirement whose rationale can quote or paraphrase the intake.

Test: can you point to the sentence in the intake that demands this? If not, it
is invention — note it as an open question, not a requirement.

### 5. No orphan, by construction
Every requirement carries a `derives_from: BO-N` that names one of the emitted
outcomes. The key is a flat `REQ-<n>`; the parent tie lives only in
`derives_from`. The skeleton makes a parentless requirement structurally
impossible; don't hand-edit one in.

- Fail: a `REQ-<n>` block with no `derives_from`, or one pointing at a `BO-N`
  that isn't in the outcomes list.
- Pass: every `REQ-<n>` cites a `BO-N` in `derives_from`.

Test: does removing the parent outcome cleanly remove this requirement? If the
requirement would survive orphaned, the trace is wrong.

## The outcome test (every outcome)

Outcomes have one extra test on top of grounded-in-intake:

### Benefit, not mechanism
An outcome is a **benefit or capability statement** the business wants — never a
solution. If it could be a line in an architecture, it is not an outcome.

- Fail: *"Use a Postgres cache."* / *"Deploy on Databricks."* / *"Build a
  React SPA."*
- Pass: *"Technicians complete jobs with no connectivity."* / *"Completions are
  auditable."*

Plus: a short (<= 4 word) display label, and a count in the **3-6** range — a
range, not a quota. Fewer strong outcomes beat more invented ones.

## Quick checklist (paste into a PR review)

```
Outcomes (3-6):
  [ ] each is a benefit, not a mechanism
  [ ] each has a <= 4-word label
  [ ] each is grounded in the intake (no invented scope)

Each requirement:
  [ ] atomic (one capability/constraint)
  [ ] verifiable (GWT for F, measurable target for NF)
  [ ] no-HOW (no tech/framework/implementation)
  [ ] grounded in the intake
  [ ] has a derives_from: BO-N parent (no orphan)
  [ ] F/NF marked correctly
  [ ] strong functional reqs carry Given/When/Then
```
