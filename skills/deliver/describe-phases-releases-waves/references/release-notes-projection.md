# Release-notes projection — the deterministic algorithm

Release notes are a **pure projection** of a release's accepted changes. Nothing is hand-authored; nothing is
left to drift. Given the release record and its accepted change items, the projection is fully determined —
run it with no model and it is always correct. The persuasive narrative / comms-deck version is a separate,
optional model pass *on top of* this floor.

## Inputs

- The **release**: its key (`REL-3`), title, and one-line intent.
- Its **accepted changes**: each with a `change_kind`, a display key (`req_key`), a trace
  (`derives_from_outcome_key`, possibly null), and an optional one-line rationale.
- The **outcomes** (to resolve each trace key to its outcome for the citation).

## Heading order (fixed)

Group the changes by `change_kind` under these four headings, in this order. **Skip any group that is
empty** — do not emit an empty heading.

| `change_kind` | Heading |
|---|---|
| `add` | `## Added` |
| `change` | `## Changed` |
| `patch` | `## Fixed` |
| `remove` | `## Removed` |

## The algorithm

```
1. Emit the title line:        "# {rel_key} — {title}"   (trim a trailing " —" if title is empty)
2. If the release has an intent, emit a blank line then the intent paragraph.
3. For each (kind, heading) in the fixed order above:
     a. group = all accepted changes whose change_kind == kind
     b. if group is empty: skip this heading entirely
     c. emit a blank line, then the heading
     d. for each change in the group, emit one bullet:
          - **{req_key or "(no key)"}**{trace}{": " + rationale, if any}
        where {trace} is:
          - " — traces to {OUTCOME_KEY}"        when derives_from resolves to an outcome with a key
          - " — traces to a requirement"        when it derives from a requirement but not a keyed outcome
          - " — no outcome (scope creep)"        when the trace is null
4. End with a trailing newline.
```

## Worked example

Release `REL-3` "Q3 audit & export improvements", intent "give auditors self-serve evidence without raising a
ticket", with four accepted changes (one add → OUT-2, one change → OUT-4, one patch → null, one remove →
OUT-2) projects to:

```markdown
# REL-3 — Q3 audit & export improvements

give auditors self-serve evidence without raising a ticket.

## Added
- **REQ-21** — traces to OUT-2: the self-serve CSV export mechanism for OUT-2.

## Changed
- **REQ-11** — traces to OUT-4: extends audit-log retention to keep approvals traceable.

## Fixed
- **REQ-30** — no outcome (scope creep): timezone-drift fix; trace before shipping.

## Removed
- **REQ-4** — traces to OUT-2: legacy XML export, superseded by the new CSV export.
```

## Why this is deterministic, and why that matters

Every token comes from a field that already exists — the kind, the key, the trace, the rationale. No
judgement, no prose, no model. That means:

- The notes **cannot drift** from the deltas; regenerate them on every change and they stay true.
- The **null trace is preserved**, not smoothed over — "no outcome (scope creep)" appears in the notes
  themselves, so the scope-creep signal is visible to whoever reads them.
- Every line **cites its outcome**, so "what changed and why" is answerable line by line.

The narrative deck — persuasive prose for a stakeholder audience — is genuinely new synthesis and belongs to
an optional model pass. This deterministic projection is the reliable floor it builds on; if the model is
unavailable, the floor still ships.
