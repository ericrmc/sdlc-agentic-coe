---
name: stage-and-fingerprint
description: Vault an incoming requirements source byte-untouched, sha256 it for de-dup, record provenance (received_at, received_from, content_hash, source_ref), and propose an identity binding — is this a brand-new source, or a new version of one already staged? Advisory; proposes the binding, never decides it.
one_liner: Vault the original byte-untouched, fingerprint it, and propose whether it is new or a new version.
aliases: [stage a source, fingerprint a file, sha256 de-dup, record provenance, is this a new version, vault the original, content hash, source identity binding, dedupe an upload]
when_to_use: a requirements source has arrived and must be vaulted with provenance before it is read, and you need to know whether it is new or a new version of an already-staged source
output_kinds: [proposal, question]
deterministic_fallback: the staging readers in skills/ingest/_scripts/ (byte-copy to the vault + sha256 + a name/key match against prior staged sources) produce the provenance record and the candidate identity binding with no model
suggested_tier: light
tier_reason: hashing and a name/key match are deterministic file facts; the only soft call is proposing the identity binding when the name changed but the content overlaps, and even that is proposed for a human, never decided
neighbours:
  before: (none — this is the front door; a source is staged here before it is read)
  after: skills/ingest/ingest-source-to-requirements (reads the staged original) and skills/ingest/reingest-delta (when the binding says this is a new version of an existing source)
---

# stage-and-fingerprint — vault the original, fingerprint it, propose its identity

Before a source is read, it is **staged**: the incoming bytes are copied untouched into a vault,
hashed, and given a provenance record. This is the cheap, deterministic front door that makes
everything downstream trustworthy — `ingest-source-to-requirements` reads the *vaulted* copy (not a
volatile upload), and `reingest-delta` can prove later whether the source changed, because the
fingerprint is on record.

It also answers one identity question up front: **is this a brand-new source, or a new version of
one already staged?** The answer routes the next step — a new source goes to ingest; a new version
goes to re-ingest-delta. The skill **proposes** the binding; a human ratifies it.

Everything it emits is a **proposal a human ratifies by merging** (the provenance record + the
identity binding), or a **question** when the binding is genuinely ambiguous. Those are the only
output kinds here: proposal, question. (It has no `halt`: by the time a source is being staged, the
source is in hand — the absent-source halt is `ingest-source-to-requirements`' STEP 0.)

## When to use

- A requirements source has arrived (an upload, an export, a pasted block written to a file) and
  must be vaulted with provenance **before** it is read.
- You want to know whether it duplicates or supersedes something already staged, so the next step
  routes correctly.

Do not use this to read or interpret the source — that is `ingest-source-to-requirements`. This
skill touches the bytes only to copy and hash them; it never parses them into requirements.

## Inputs

| Input | Required | What it is — and the if-absent behaviour |
|---|---|---|
| **The incoming source bytes** | **Required.** | The file/export/paste to vault. If absent: there is nothing to stage; defer to `ingest-source-to-requirements`' STEP 0 halt (per `_shared/grounding.md`), which asks where the source is. Never vault or hash a hypothetical. |
| **Origin metadata** | *Optional.* | `received_from` (who/where it came from) and, for stale-prone sources, `exported_at`. If absent: record `unknown`; never fabricate an origin or a timestamp. |
| **Prior staged sources** | *Optional.* | The vault's existing records, for the identity match. If absent (first source): the binding is trivially "new"; never invent a prior version to bind against. |

## Grounding (quoted)

<!-- BEGIN grounding (byte-stable; do not edit a quoted copy — edit _shared/grounding.md) -->

**GROUNDING RULE — name the required inputs; an absent required input HALTs and asks, never assumes.**

A skill **names its required inputs** up front (its Inputs section marks each row Required or
Optional). Then:

- **A required input that is absent, unreadable, or empty becomes a `halt`.** The halt asks
  the user *where the input is*, offering the formats ingestion can read (an xlsx/csv path, a
  GitHub Project owner+number, a docs folder, or a pasted block). It then **stops and waits.**
  It never assumes, invents, or reasons over a hypothetical — no invented id, key, number, NFR,
  requirement, acceptance criterion, file path, or source row.
- **Partial input is named, not patched.** When some required inputs are present and others are
  not, the skill **names exactly what is missing and asks for it** — it never silently proceeds
  on the part it has, and it never back-fills the gap with a plausible-looking guess.
- **An absent *optional* input proceeds honestly.** It is surfaced as a `question` or recorded
  as an explicit null — never padded with invented content to look complete.

**"I read nothing" and "I cannot read this" are different outputs.** An unreadable or
unsupported source HALTs (it asks for a readable form); it never returns an empty result, because
a silent-empty reads downstream as "the source had nothing in it" — a silent-proceed failure.

**A halt is a question, never a verdict.** A halt names the missing input and asks where it is.
It never smuggles a finding, an assumption, or a disposition for a human to rubber-stamp — no
"I halt because this is infeasible / too risky / out of scope." Those are JUDGMENTs the human
owns. The halt carries only: *what is required, what is missing, and the formats it can be read
from.*

<!-- END grounding -->

> This skill's required input (the source bytes) being absent is the absent-source case the
> grounding rule covers; here it defers to `ingest-source-to-requirements`' STEP 0 halt rather than
> re-emitting one, because staging is downstream of "where is the source?".

## Req-key scheme (quoted)

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

> Staging cares about the **`source_ref`** rule above: the source's own identifier is preserved
> verbatim, so a re-staged file binds to its prior version by `source_ref` + content hash, never by
> a minted key that renumbers across schemes.

## The method (numbered steps)

### STEP 1 — vault the original, byte-untouched (deterministic)

Copy the incoming bytes into the vault **unmodified** — no re-encoding, no normalisation, no
trimming. The vaulted copy is the **source of record**; every locator and every later diff is
relative to it. Record the vault filename. (The `extract-evidence` prototype's discipline holds
here: the original binary is the source of record, and its sha256 is the provenance root every
emitted record carries.)

### STEP 2 — fingerprint it (deterministic, the de-dup key)

Compute the **sha256** of the vaulted bytes — the `content_hash`. This is the exact-duplicate key:

- **content_hash already in the vault** → this is a **byte-identical re-submission.** Propose
  binding it to the existing staged source as a no-op (same bytes, nothing to re-ingest) and say so;
  do not stage a second copy.
- **content_hash new** → a genuinely new set of bytes. Continue to STEP 3.

### STEP 3 — record provenance (deterministic)

Write the provenance record. Every field is observed or `unknown` — none is inferred:

```
staged_as:     <vault-filename>
content_hash:  sha256:<hex>
source_ref:    <the source's own identifier, verbatim — its filename, board name, or doc title>
received_at:   <ISO timestamp — when it was staged>
received_from: <origin | unknown>
exported_at:   <ISO | unknown>     # for stale-prone sources
```

`source_ref` is the source's **own** name/id, preserved verbatim per the req-key convention — it is
the key the version match keys off, not a minted requirement key.

### STEP 4 — propose the identity binding (the one soft call)

Match this source against the prior staged records to answer: **new source, or new version of an
existing one?** Use deterministic signals first, the model only to break a genuine tie:

- **Same `content_hash`** → identical bytes (handled in STEP 2): **no-op re-submission.**
- **Same `source_ref`, different `content_hash`** → **new version of an existing source.** Propose
  the binding `supersedes: <prior staged record>` and route to `reingest-delta`.
- **New `source_ref` and `content_hash`, but a strong name/key overlap with a prior source** (e.g.
  the file was renamed) → **ambiguous.** Surface a **question**: *"This looks like it may be a new
  version of `<prior>` (renamed) — bind as a new version, or stage as new?"* Never silently bind a
  renamed file; never silently fork a versioned one.
- **New `source_ref`, no overlap** → **brand-new source.** Propose staging it fresh and routing to
  `ingest-source-to-requirements`.

The binding is **proposed, never decided.** A wrong auto-bind either drops a real new version
(under-count) or forks one source into two (duplicate requirements under two keys) — both are
exactly the failure the `source_ref` rule exists to prevent, so the human ratifies the binding.

### STEP 5 — hand off

Open the provenance record + the proposed binding as a PR. On ratification, route:

- **new source** → `ingest-source-to-requirements` (read the vaulted copy);
- **new version** → `reingest-delta` (diff against the prior version);
- **no-op re-submission** → stop; nothing to ingest.

## Output format

A small provenance + binding record a human ratifies by merging.

```markdown
# Staged source — <vault-filename>

**content_hash:** sha256:9f2a4c…
**source_ref:** intake-requirements.xlsx
**received_at:** 2026-06-16T09:00Z
**received_from:** client-PMO
**exported_at:** 2026-06-10T00:00Z

## Proposed identity binding
- **Verdict (proposed):** new version of an existing source.
- **Supersedes:** staged/intake-requirements.2026-05.xlsx (source_ref match; content_hash differs).
- **Route:** reingest-delta (diff against the prior version).
- **Confidence basis:** identical `source_ref`, changed `content_hash` — deterministic, not a guess.
```

When the binding is ambiguous (a renamed file), the record instead carries a **question** naming
both candidates and asking the human to choose — never an auto-bind.

### Deterministic fallback

The staging readers in `skills/ingest/_scripts/` produce the entire record with no model: byte-copy
to the vault, sha256, and a `source_ref` + name match against prior records. The only place a model
helps is breaking the renamed-file tie in STEP 4 — and even there the output is a **question**, so
the deterministic fallback (surface the ambiguity, ask) is the safe default.

## Notes & anti-patterns

**Anti-patterns — reject these on sight:**

- **Mutating the original.** The vaulted copy is byte-untouched. Re-encoding, trimming, or
  normalising it breaks every downstream locator and every future diff.
- **De-duping on the minted key.** De-dup is on `content_hash` (exact) and `source_ref` (identity),
  never on a minted `REQ-<n>` — which renumbers across schemes and would silently fork a source.
- **Silently binding a renamed file.** A name change with no `source_ref` match is a **question**,
  not an auto-bind. Auto-binding wrong either drops a version or forks one.
- **Fabricating provenance.** `received_from` / `exported_at` are observed or `unknown` — never a
  plausible-looking guess.
- **Deciding the binding.** The skill proposes; a human ratifies. The binding routes the next step,
  so a wrong silent call propagates.

**Notes:**

- **Cheap and deterministic by design.** Copy, hash, match, propose. The hash *is* the de-dup; the
  `source_ref` *is* the identity. The model is a tie-breaker, not the method.
- **This is the front door, not the reader.** It vaults and fingerprints; it never parses the source
  into requirements. That is `ingest-source-to-requirements`, reading the copy this skill vaulted.
- **Advisory, never a gate.** The provenance record and the binding are a proposal ratified by a
  merge; nothing here blocks. (See `skills/_contract/propose-ratify-rhythm`.)
