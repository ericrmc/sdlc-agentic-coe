---
name: ingest-source-to-requirements
description: Read a structured-but-messy requirements source (xlsx/csv, a pinned GitHub Project snapshot, a docs folder, an exported SharePoint file, or a pasted block) via the deterministic readers, and emit one per-requirement markdown block in the canonical shape (REQ-<n>, derives_from, **The system shall**, GIVEN/WHEN/THEN, **Rationale:**) with a verbatim source_ref and a locator. HALT if the source is unstated or unreadable; never invent a requirement, key, number, or acceptance criterion; lift an acceptance criterion only when a source locator backs it. Delegate controlled-vocab metadata to classify-requirements.
one_liner: Turn a structured-but-messy source into traceable requirement markdown — or HALT for the source, never invent it.
aliases: [ingest requirements, import a backlog, read an xlsx of requirements, load requirements from a spreadsheet, pull from a github project, ingest a docs folder, requirements from a CSV, structured intake, parse a requirements export, source to requirements]
when_to_use: a structured-but-messy requirements source exists (a spreadsheet, a ticket board, a docs folder, an exported document) and needs lifting into the canonical per-requirement markdown shape with provenance, before any classification or red-teaming
output_kinds: [proposal, question, halt]
deterministic_fallback: the deterministic readers in skills/ingest/_scripts/ (block-extraction with a per-block locator + sha256; the extract-evidence prototype is the zero-dependency reference) yield a one-row-per-block skeleton with no model; degrade to "paste the rows" when no reader is wired for the source format
suggested_tier: frontier
tier_reason: lifting messy real-world rows into clean traceable requirements, judging which blocks are requirements vs noise, and stamping provenance that downstream skills trust is high-stakes synthesis; the read itself is deterministic, the map-to-requirement is the model step
neighbours:
  before: skills/ingest/stage-and-fingerprint (vault the original + fingerprint it before reading; re-ingest matches on its source_ref)
  after: skills/understand/classify-requirements (owns the controlled-vocab metadata — layer / stated_as / quantified / solution_shaped — this skill delegates, never inlines)
---

# ingest-source-to-requirements — lift a messy source into canonical requirement markdown

A new project rarely arrives as free text. More often the requirements already live somewhere
structured-but-messy: a stakeholder's spreadsheet, a Jira/GitHub board, a folder of docs, an
exported SharePoint page. `decompose-intake-to-outcomes` handles the free-text case;
`classify-requirements` annotates requirements that already exist. **Nothing else ingests a
structured source** — that is this skill's job.

It does **two** things and keeps them separate:

1. **A deterministic read** (no model) that turns the source into blocks, each carrying a
   **locator** (where in the source it came from) and a **sha256** (so a re-read can prove
   the block is unchanged). This is the readers in `skills/ingest/_scripts/`.
2. **A model map** that turns each block into a per-requirement markdown block in the canonical
   shape — minting a local `REQ-<n>` while preserving the source's own identifier verbatim as a
   `source_ref`. This is the one step that needs a model.

Everything it emits is a **proposal a human ratifies by merging a PR** — advisory by design. Its
two other outputs are a **question** (an optional input is missing, or a delta needs a human call)
and a **halt** (a required input — the source itself — is absent or unreadable). Those are the
only output kinds: proposal, question, halt.

> **The discipline in one line:** read the source, or HALT for it — never invent it; lift an
> acceptance criterion only when a locator backs it — never synthesise one.

## When to use

- A project's requirements already exist in a structured-but-messy artefact and you want them in
  the canonical markdown shape, with provenance, before classifying or red-teaming them.
- You have an xlsx/csv path, a **pinned** GitHub Project snapshot, a docs folder, an exported
  SharePoint file, or rows pasted into the chat.

Do **not** use this for free-text intake (that is `decompose-intake-to-outcomes`) or to annotate
requirements that are already canonical (that is `classify-requirements`). Do not use it to author
a *new* requirement the source does not contain — this skill only lifts what is there.

## Inputs

| Input | Required | What it is — and the if-absent behaviour |
|---|---|---|
| **The source** | **Required.** | The artefact the requirements live in. If absent (the user has not said *where* the requirements are): **HALT and ask where they live** (per `_shared/grounding.md`), offering the readable forms below; never invent a source or its rows. If present but **unreadable / unsupported**: **HALT — not empty** (see STEP 1); an "I cannot read this" is a different output from "I read nothing." |
| **Target file / key scheme** | *Optional.* | The accepted-requirements file whose key scheme the minted keys should match. If absent: proceed, mint a fresh `REQ-<n>` counter, and surface a `question` asking which file these should land in; never assume a scheme — read it from the target file when one is given (per `_shared/req-key-conventions.md`). |
| **Source origin / export metadata** | *Optional.* | `received_from`, and for stale-prone sources an `exported_at` / snapshot timestamp. If absent: record it as `unknown` and carry a soft `staleness-unverified` caveat; never fabricate a timestamp. |

Readable forms (offer these in the halt): an **xlsx / csv** file path · a **GitHub Project**
(owner + project number, **as a pinned timestamped snapshot**, not a live read) · a **docs folder**
(markdown / text) · an **exported SharePoint file** (never a live fetch) · the **rows pasted**
into the chat.

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

## The method (numbered steps)

### STEP 0 — locate the source; HALT if unstated (deterministic, pre-model)

Before any model reasoning, establish that there **is** a source and that you can name it. This
is a file-level fact, not a judgement: a path was given / a project snapshot was pinned / a folder
was named / rows were pasted. If none of those is true — the user has not said *where the
requirements live* — emit the clean halt and **stop**:

```markdown
HALT — required input missing.

I can't ingest requirements without the source they live in, and I won't invent one. Tell me
where the requirements are and I'll read them from there.

I can read any of these:
  • an xlsx / csv file path
  • a GitHub Project (owner + project number) — as a pinned, timestamped snapshot, not a live board
  • a docs folder (markdown / text)
  • an exported SharePoint file (an export, not a live link)
  • the rows pasted directly into the chat

Which one, and where? (Once you point me at it, I'll read it and propose the requirements —
nothing is assumed until then.)
```

The halt **names the missing input, offers the readable forms, and stops.** It carries no finding,
no assumption, no count, no feasibility verdict — those would break the rule (see the ❌
counter-example in `skills/_contract/grounding-no-absent-input/SKILL.md`).

**Source-trust branches (resolved at STEP 0, before any read):**

- **SharePoint** — never live-fetch (an auth + stale-doc hazard). **HALT asking for a local
  export**, then stamp its origin and `exported_at` (or `unknown`). SharePoint support is
  *optional*; the halt is the whole of it.
- **GitHub Project** — require a **pinned, timestamped snapshot**, not a live `gh project
  item-list` read. A live board is exactly as stale-prone as a SharePoint doc — a field rename
  silently remaps "acceptance." If only a live board is on offer, ask for the pinned snapshot
  first; the same export discipline applies.
- **CSV / any format with no wired reader** — if the format is unreadable or unsupported, this is
  resolved at STEP 1 as a **HALT — not empty**, never an empty result.

### STEP 1 — read the source to blocks (deterministic; HALT-not-empty on unreadable OR read-as-empty)

Run the deterministic reader in `skills/ingest/_scripts/` for the source format. It turns the
source into **blocks** — one per spreadsheet row, ticket, paragraph, or text line — each carrying:

- a **locator** — the navigable position inside the **original**, in the **exact form the reader
  emits** (these are the only forms; copy them verbatim, never a paraphrase like `sheet:` or
  `item:#`):
  - **xlsx** — `Sheet!A1` (a single-cell row) or `Sheet!A1:F1` (a multi-cell row), where `Sheet`
    is the worksheet's own name. A single cell inside a row resolves as `Sheet!C1`.
  - **csv / tsv** — `csv!A1` or `csv!A2:C2` — the sheet name is the literal token `csv`, the row
    number is 1-based over the file (the header is row 1).
  - **docx** — `para:N`, where `N` is the 1-based count over emitted paragraphs **and** table
    rows in body order (a table row's cells join with ` — `).
  - **text / markdown** — `line:N`, where `N` is the 1-based line number in the file.
  - **GitHub Project snapshot** — `item:<num>` (the row), `item:<num>!fields` (the header), or
    `item:<num>:<field>` (one field), where `<num>` is the item's content number, **no `#`**
    (e.g. `item:231`, `item:231:status`).
  so an acceptance criterion can be proven to come from a real place;
- a **sha256** of the block's source bytes, so `reingest-delta` can prove later whether the block
  changed.

This needs **no model** and yields a usable skeleton on its own. The zero-dependency reference for
this read is the `extract-evidence` prototype (stdlib-only: OOXML is `zipfile` + `xml.etree`; PDF
via `pdftotext` with pinned flags; deterministic — same bytes in, byte-identical blocks out, no
clock, no network, no model). The readers wrap that behaviour; they are a **deterministic fallback,
never a hard read-time dependency** — if no reader is wired for the format, **degrade to "paste the
rows."**

> **HALT — not empty (unreadable).** If the source exists but cannot be read (unsupported format,
> corrupt file, a live board offered where a snapshot is required), the reader returns a projection
> with `status="skipped"` and a `reason`. Emit a **halt that says "I cannot read this"** carrying
> that reason and asking for a readable form. **Never return an empty result.** "I read nothing"
> and "I cannot read this" are different outputs — a silent-empty ingest reads downstream as *the
> source had nothing in it*, which is a trust failure.

> **HALT — read as empty (readable-but-empty).** The reader can also come back `status="ok"` with
> **zero blocks** — a CSV that decoded but held no rows, a workbook whose only sheet is blank, a
> docs folder with no text, an export with no content, a paste of only whitespace, or a GitHub
> snapshot whose `items` list is empty. **This is the silent-empty failure the grounding rule
> forbids, and it is THIS skill's call, not the reader's.** A readable-but-empty read MUST **HALT**,
> never proceed to STEP 2 and emit an empty requirement set. Name *which* source read as empty and
> ask for a non-empty one (the right sheet, a wider range, the folder that actually holds the
> docs). Concretely: **if `proj["blocks"]` is empty for any reason** — `status="skipped"` (the
> unreadable case above) **or** `status="ok"` with no blocks (this case) — **halt; never carry an
> empty block set into the model step.** An empty requirement set is never a valid output of this
> skill.
>
> ```markdown
> HALT — the source read as empty.
>
> I read <source> at <locator/sheet/folder you pointed me at> and it parsed cleanly, but it held
> no rows/paragraphs/items I could lift a requirement from. I won't emit an empty requirement set,
> and I won't invent one to fill the gap.
>
> Point me at a non-empty source — e.g. the sheet/tab the requirements are actually on, a wider
> cell range, the folder that holds the docs, or the rows pasted directly — and I'll read it.
> ```

### STEP 2 — map each block to a per-requirement markdown block (the model step)

For each block that **is** a requirement (skip headings, totals, notes — a block the model judges
not to be a requirement is dropped, never reshaped into a fake one), emit one canonical
per-requirement markdown block. **Read the target file's key scheme first** (per the req-key
convention); if no target file was given, mint a fresh `REQ-<n>` counter and flag it in STEP 5.

Each emitted block carries, by construction:

- a minted local key `REQ-<n>` (or the target scheme's prefix), and a **`source_ref:`** = the
  source's **own identifier, verbatim** (its ticket id, its row label, its heading). Re-ingest
  matches on `source_ref`, never on the minted key. If the source row has no identifier of its
  own, `source_ref` is the locator itself — never a fabricated id.
- a **`derives_from:`** to the outcome the requirement serves **only when the source states one**;
  if the source carries no outcome link, leave `derives_from` as an explicit `null` and surface it
  in STEP 5 as a value-orphan `question` — **never invent a `BO-<n>` to fill it.**
- the requirement text in canonical form: **The system shall …** (functional) or
  **Constraint: …** (non-functional). Lift the source wording; tighten phrasing, never add scope.
- the **acceptance criteria — lifted with their locator, or marked structurally absent.** This is
  the load-bearing distinction:
  - If the source has an acceptance field/column/section for this block, lift it as
    **`Acceptance:` GIVEN … WHEN … THEN …** and append its locator **in the reader's exact form**
    (e.g. `(source: Reqs!E7)` for the AC cell of an xlsx row, `(source: item:231:body)` for a
    GitHub field, `(source: line:42)` for a text line). A lifted AC **carries its source locator.**
  - If the source has **no** acceptance content for this block, emit
    **`Acceptance: — (absent in source; not synthesised)`**. An AC with no locator is an
    **absent-AC flag, never a silently-present one.** This makes lifted-vs-fabricated a
    **structural distinction (locator present or absent), not a model promise** — you can grep for
    a missing locator.
- a **`Rationale:`** — one line, grounded in the source (paraphrase or quote what the source row
  says about *why*). If the source gives no rationale, write `Rationale: — (none stated in source)`
  rather than inventing one.

### STEP 3 — stamp the source line (provenance travels in the markdown)

Append a single **Source** line to each requirement block so provenance travels *in* the artefact,
not in a side-channel that dies at ingest:

```
**Source:** <vault-filename> · sha256:<block-hash> · <locator> · received_at:<ISO> ·
received_from:<origin|unknown> · exported_at:<ISO|unknown> · <staleness-unverified?>
```

`received_at` is the ingest time; `received_from` and `exported_at` come from the optional origin
metadata (or `unknown`). A stale-prone or unknown-export source carries a soft
`staleness-unverified` caveat here — **never a hard exclusion**, and never a fabricated timestamp.
This is the field that lets `classify-requirements` re-surface a 6-month-old row's staleness
downstream instead of laundering it into a clean-looking requirement.

### STEP 4 — delegate the controlled-vocab metadata (do NOT inline the enums)

The shape metadata — `layer`, `stated_as` (need|solution|constraint|symptom), `quantified`, and
the solution-shaped flag — is **owned by `classify-requirements`.** Do **not** inline its enums
here. Hand the emitted requirement blocks to `classify-requirements` and let it annotate them.

Rationale: the drift check guards *marked prose blocks* (the byte-stable stubs), **not enum lists**.
Inlining `classify`'s closed sets here would duplicate them where nothing pins them in step, so they
would silently drift. One owner, cited — never a private copy.

### STEP 5 — propose a PR; surface the gaps as questions

Write the requirement blocks into the project's repo (e.g.
`requirements/ingested-<source>.md`) and open a pull request — **the human ratifies by merging.**
Alongside the proposal, surface as **questions** (never silent fills):

- every block with `derives_from: null` (a value-orphan — *which outcome does this serve?*);
- every block with an **absent AC** (*the source states no acceptance for this — confirm or add one*);
- any block dropped as "not a requirement" (*confirm it was noise, not a missed requirement*);
- if no target file was given: *which file should these land in, and whose key scheme do they take?*

## Output format

One markdown file of per-requirement blocks, each in this shape. The
[deterministic fallback](#deterministic-fallback) is this same shape with the text slots empty and
only the locator + sha256 + `source_ref` filled by the reader.

```markdown
# Ingested requirements — <source name>

> Lifted from <source> on <date>. Each block cites its source verbatim. Ratify by merging this PR.
> Shape metadata (layer / stated_as / quantified) is delegated to classify-requirements.

## REQ-1  (F)
- **source_ref:** JIRA-4821          <!-- the source's OWN id, verbatim -->
- **derives_from:** BO-2             <!-- only when the source states the outcome; else null + a question -->
- **The system shall** allow a dispatcher to publish a day's routes without re-keying.
- **Acceptance:** GIVEN a built route set, WHEN the dispatcher publishes, THEN every stop is
  pushed to the technician app within 30 seconds.  *(source: Reqs!E12)*
- **Rationale:** Source row notes "dispatchers lose an hour re-keying" — the publish path removes it.
- **Source:** intake-2026-06.xlsx · sha256:9f2a… · Reqs!B12 · received_at:2026-06-16T09:00Z ·
  received_from:client-PMO · exported_at:2026-06-10T00:00Z

## REQ-2  (NF)
- **source_ref:** row-13
- **derives_from:** null              <!-- surfaced as a value-orphan question in STEP 5 -->
- **Constraint:** Customer data must remain within the AU region.
- **Acceptance:** — (absent in source; not synthesised)   <!-- NO locator = structurally absent -->
- **Rationale:** — (none stated in source)
- **Source:** intake-2026-06.xlsx · sha256:c1d8… · Reqs!B13 · received_at:2026-06-16T09:00Z ·
  received_from:client-PMO · exported_at:unknown · staleness-unverified
```

### Deterministic fallback

If no model is available, run the reader and emit the **skeleton only** — one block per source
block, with `source_ref`, locator, sha256, and the empty `The system shall …` / `Acceptance:` /
`Rationale:` slots — then stop. This is a legitimate, useful output: it gives an analyst the
structure and the provenance to fill the requirement text by hand, and nothing in it is invented.
If no reader is wired for the source format, the fallback is **"paste the rows"** — never a
fabricated read, never an empty result.

## Notes & anti-patterns

**Anti-patterns — reject these on sight:**

- **Inventing a source.** No path, no snapshot, no folder, no paste → HALT (STEP 0). Never reason
  from a project *name* to a plausible requirement set.
- **Silent-empty on an unreadable source.** "I read nothing" must never stand in for "I cannot read
  this." Unreadable/unsupported → HALT — not empty (STEP 1).
- **Silent-empty on a readable-but-empty source.** A clean read that yields **zero blocks** (an empty
  sheet/CSV/folder/snapshot, a whitespace-only paste) must HALT too — never proceed to STEP 2 and
  emit an empty requirement set. If `proj["blocks"]` is empty for any reason, halt and ask for a
  non-empty source (STEP 1). An empty requirement set is never a valid output.
- **Synthesising an acceptance criterion.** An AC with no source locator is an **absent-AC flag**.
  Never write a GIVEN/WHEN/THEN the source does not contain — that is the single most damaging
  fabrication this skill could make, because it reads downstream as a tested commitment.
- **Inventing a `derives_from`.** A requirement with no stated outcome carries `derives_from: null`
  and a value-orphan question — never a manufactured `BO-<n>`.
- **Minting a key and losing the source id.** Always preserve the source's own identifier as
  `source_ref`; re-ingest de-dups on it, not on the minted `REQ-<n>` (which renumbers across
  schemes).
- **A live GitHub board or live SharePoint fetch.** Both are stale-prone; require a pinned
  snapshot / a local export. A field rename silently remaps a column otherwise.
- **Inlining classify's enums.** `layer` / `stated_as` / `quantified` are delegated, never copied.

**Notes:**

- **Read deterministically, map with a model.** The locator + sha256 read is mechanical and is the
  fallback; the row-to-requirement map is the one model step. Keeping them separate is what makes
  lifted-vs-fabricated a *structural* fact (locator present or absent).
- **Provenance must propagate.** The `Source` line travels in the markdown, and
  `classify-requirements` re-surfaces a stale source as a `question` downstream — so a six-month-old
  Excel row cannot launder into a clean requirement two skills later.
- **Advisory, never a gate.** The proposal is markdown ratified by a merge. The halt stops *this
  run* and asks; it blocks nothing downstream. (See `skills/_contract/propose-ratify-rhythm`.)
- **Reuse, do not re-author.** Wrap the deterministic readers in `skills/ingest/_scripts/` (the
  `extract-evidence` prototype is the zero-dependency reference) by name and behaviour. Author fresh
  only: the row-to-requirement prompt (STEP 2), the source-line format (STEP 3), and the SharePoint
  halt branch (STEP 0). A CSV adapter is a change in the separate assistant repo — out of scope here.
