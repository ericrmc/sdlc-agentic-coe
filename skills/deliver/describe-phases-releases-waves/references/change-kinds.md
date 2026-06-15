# Change kinds — the four-way delta classification

Every release item — and every phase and migration, since they are the same shape — is a **scoped, versioned,
traced delta** over one source of truth. The `change_kind` says what *kind* of delta it is. There are exactly
four, and the rule that governs all of them is: **nothing is ever deleted.** Retirement is a pointer; revision
supersedes.

## The four kinds

| `change_kind` | Intent | What it does to the requirement graph |
|---|---|---|
| **`add`** | A new capability the project did not have. | Creates a **new requirement** row, traced (`derives_from`) to the outcome it serves. The release item is the audit envelope around that creation. |
| **`change`** | Revise existing behaviour. | **Supersedes** the existing requirement: a new version, with a `supersedes` pointer back to the old one. The old version is retained, marked superseded. |
| **`remove`** | Retire / drop existing scope. | Marks the requirement **retired** with a pointer to the release that retired it (e.g. `retired_in_release = REL-3`). **Never a delete.** The trace edge survives so history stays answerable. |
| **`patch`** | Fix a defect. | **No scope change.** No requirement is created, superseded, or retired. The item exists for the release record and the notes only. Its trace may still point at the outcome whose quality it preserves. |

## Classifying by intent (the verb heuristic is only the floor)

The deterministic fallback picks a kind by scanning for trigger verbs, in priority order — `remove` first
because it is the strongest signal, `add` last as the default:

1. `remove`, `drop`, `retire`, `delete`, `deprecate` → **remove**
2. `fix`, `patch`, `hotfix`, `bug`, `correct` → **patch**
3. `change`, `update`, `revise`, `tighten`, `rework`, `modify` → **change**
4. `add`, `introduce`, `build`, `ship`, `support`, `enable`, `create` → **add**
5. (no verb matched) → **add**

This is a floor, not a ceiling. **Classify by the item's intent, not its words.** "Improve the CSV export"
carries no `change` verb but is plainly a `change`, not an `add`. A capable model reads the intent; the verb
list keeps the skill runnable when no model is available.

## Why nothing is ever deleted

A delete loses the answer to "what was this, and why did it go away?" — the exact question a release record
exists to answer. So:

- **`remove`** writes a *retirement pointer*, not a `DELETE`. The requirement row stays; it is marked retired
  by a named release. You can always reconstruct what the project looked like before that release.
- **`change`** writes a *new version with a supersedes link*, not an in-place edit. The prior version stays.
- Outcomes affected by a removal stay visible. If a `remove` retires the **only** requirement under an
  outcome, that outcome now has no coverage — surface it (see the scope-creep / dropped-requirement checks),
  do not silently orphan it.

## The trace edge and the null signal

Independently of its kind, **every delta carries a trace** (`derives_from_outcome_key`) to the **one** outcome
it serves — copied exactly from the accepted outcomes, never invented.

A delta with a **null trace is not an error**. It is the deliberate **scope-creep signal**: work with no
recorded outcome behind it. The honest null is the point. An `add` or `change` with a null trace says, in
writing, *"trace this to an outcome or drop it before shipping."* A `patch` may legitimately carry a null (a
defect fix that preserves no specific outcome) — but even then, naming the outcome whose quality it preserves
is better than a bare null.
