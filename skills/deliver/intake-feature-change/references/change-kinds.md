# Change kinds — pointer (do NOT re-author here)

The `change_kind` taxonomy this skill classifies a feature ask into is **owned by
`describe-phases-releases-waves`**, not re-authored here. This file is a thin
pointer so the citation resolves locally; the source of truth is:

> `skills/deliver/describe-phases-releases-waves/references/change-kinds.md`

Read that file for the full definitions. The summary below is a non-authoritative
reminder only — if it ever disagrees with the source, the source wins.

## The four kinds (reminder — source of truth is describe-phases)

| `change_kind` | Intent | Effect on the requirement graph |
|---|---|---|
| `add` | new capability the project did not have | creates a new requirement row, traced to one outcome |
| `change` | revise existing behaviour | supersedes the existing requirement (new version + `supersedes` pointer) |
| `remove` | retire / drop existing scope | marks the requirement retired with a pointer — **never a delete** |
| `patch` | fix a defect | no scope change; the item exists for the record only |

## The verb heuristic (the deterministic floor — first match wins)

In priority order, because `remove` is the strongest signal and `add` is the default:

1. `remove`, `drop`, `retire`, `delete`, `deprecate` → **remove**
2. `fix`, `patch`, `hotfix`, `bug`, `correct` → **patch**
3. `change`, `update`, `revise`, `tighten`, `rework`, `modify` → **change**
4. `add`, `introduce`, `build`, `ship`, `support`, `enable`, `create` → **add**
5. (no verb matched) → **add**

Classify by the ask's **intent**, not its words — "improve the export" is a `change`,
not an `add`. The verb list is the floor a no-model run uses; a frontier read does better.

Nothing is ever deleted: `remove` writes a retirement pointer, `change` supersedes.
For why that matters and what each kind does downstream, read the source file above.
