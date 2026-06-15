# _shared/req-key-conventions.md — the canonical req-key scheme

> **This file is the single source of truth for REQ-KEY NAMING.**
> Skills do not import it; they **quote the block below verbatim** into their own body.
> The `check-shared-stub-drift` GitHub Action (advisory, on every PR touching
> `skills/**`) diffs each skill's quoted copy against this file and fails the check
> if a single byte drifts. **Keep the canonical block byte-stable.** If the scheme
> must change, change it *here first*, then re-quote into every skill in the same PR
> — never edit a quoted copy in place.

A key is a short, human-readable, project-stable citation target — not a database id.
One scheme, used by every skill that reads or writes a requirement, outcome, decision,
capability, or pattern. The key names *what a thing is*; every link to another thing
lives in a **field**, never inside the key.

---

## The canonical block (quote this verbatim)

<!-- BEGIN req-key-conventions (byte-stable; do not edit a quoted copy — edit _shared/req-key-conventions.md) -->

**REQ-KEY SCHEME — one prefix per kind; parentage lives in fields, never in the key.**

| Key | Kind | Notes |
|---|---|---|
| `BO-<n>` | Business outcome | `BO-1`, `BO-2`, … one integer counter per project. |
| `REQ-<n>` | Requirement | Functional **or** non-functional. F/NF is `classify` metadata, **never part of the key**. |
| `CAP-<SLUG>` | Capability | Upper-kebab slug, e.g. `CAP-OLAP`. Established under `capabilities/`. |
| `PAT-<SLUG>` | Component pattern | Upper-kebab slug, e.g. `PAT-WEBAPP-PG`. Established under `patterns/`. |
| `DEC-<n>` | Decision | A contested call, an ADR, a recorded dissent. |
| `AC-<REQ>.<n>` | Acceptance criterion | **Optional child key**, e.g. `AC-REQ-7.1`. Use only when an AC needs its own citation target; otherwise an AC is just a line under its requirement. |

A key is plain text, optionally rendered as a markdown link to the file/anchor that
defines it. It needs no database, no id, no schema. Keys are **stable for the life of
the project** — renaming or renumbering one silently breaks every field that cites it.

**THE ONE NORMALISATION RULE.** Read the key scheme **from the target file; never assume
one.** When a source uses some other prefix (`OUT-`, `TR-`, `F-`, `NF-`, `O-`, `R-`, `D-`,
a bare integer, …), normalise on write to the scheme above — outcome → `BO-`, requirement
(F or NF) → `REQ-`, decision → `DEC-`, capability → `CAP-`, pattern → `PAT-` — **and
preserve the source's own identifier verbatim as a `source_ref` field**, so a re-read
matches on `source_ref` and not on a minted key that renumbers across schemes.

**TRACE VIA FIELDS, NEVER IN THE KEY.** All parentage and relationship is a field on the
artefact, naming the **stable key** of the thing it points at:

- `derives_from:` — the upstream node this artefact serves (the single trace edge). This is
  the **one** parentage field: an outcome's capability, a requirement's outcome, a derived
  NFR's pattern. (There is no separate `derives_from_outcome_key`; it is `derives_from`.)
- `fulfils_capability:` — the `CAP-<SLUG>` a requirement fulfils.
- `fulfilled_by:` — the `PAT-<SLUG>`(s) a capability is fulfilled by.
- `supersedes:` / `superseded_by:` — version succession between two keys of the same kind.
- `contests:` — the key this artefact contests (a conflict, a dissent).

`derives_from` is a **citation, never a verdict** — it records *what serves what*; it never
asserts a thing is necessary, sufficient, good, or done. Those are human calls.

<!-- END req-key-conventions -->

---

## How to quote it

In any `SKILL.md` (or artefact template) that mints, reads, or traces a key, paste the
block between the `BEGIN`/`END` markers above — markers included — into a section titled
**"Req-key scheme (quoted)"**. Do not reword, reorder, re-case, or re-punctuate it; the
drift check compares bytes between the markers.

```markdown
## Req-key scheme (quoted)

<!-- BEGIN req-key-conventions (byte-stable; do not edit a quoted copy — edit _shared/req-key-conventions.md) -->
...paste the canonical block exactly...
<!-- END req-key-conventions -->
```

## Two hard rules, restated for the skill author

1. **Read the scheme from the target file; never assume one.** A halt that fires on
   "no `BO-` keys" must compute *file-absent / unreadable / zero-keys-of-any-recognised-
   scheme* before the model runs — never argue a project out of its own valid keys.
2. **Preserve the source identifier as `source_ref`.** Minting a local `REQ-<n>` is fine;
   losing what the source called it is not. Re-ingest de-dups on `source_ref`, never on the
   minted key.

## Relationship to the rest of the library

- The **edge** these keys are cited across — `derives_from`, walkable both ways — is
  `skills/_shared/trace-edge.md`. That stub and this one use the **same** prefixes; they
  are kept in step by hand and by the drift check.
- The **rhythm** keys live inside — propose → ratify-by-merge — is
  `skills/_shared/propose-ratify.md`.
- The **output discipline** that keeps a key a citation and never a verdict is
  `skills/_shared/target-rule.md`. Every output is one of exactly four kinds —
  **proposal, question, menu, or halt** — and an agent proposes while a human ratifies.

Keep it light. One prefix per kind, one normalisation rule, every link in a field — that
is the whole scheme.
