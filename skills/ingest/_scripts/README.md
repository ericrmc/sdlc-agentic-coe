# ingest/_scripts — deterministic source readers

These are the **deterministic extractors the `ingest/` skills call** to turn a
structured-but-messy source into a usable, citable skeleton *before any model
reasons over it*. They are not skills and not a product — they are the
no-model floor the ingest skills degrade to, and the locator machinery that lets a
minted requirement be walked back to the exact span it came from.

## The contract every reader honours

1. **Deterministic.** Stdlib only — no third-party package, no network, no clock,
   no formula evaluation. Run a reader twice on the same bytes and the blocks are
   byte-identical. (`projection.serialise` sorts keys so a re-extract diffs clean.)
2. **A projection is a cache, never authoritative.** The file the operator staged
   is the source of truth. A projection only holds locator-addressed text blocks
   that point *back* into that file. It is regenerable and disposable.
3. **Skip, never raise; halt, never empty.** A reader never raises for a content
   problem. An unsupported format, an unreadable container, a payload that is not
   what its extension claims — each comes back as a projection dict with
   `status="skipped"` and a human-readable `reason`. The calling ingest skill
   turns a *skipped* projection into a **HALT** ("I cannot read this source"),
   which is a deliberately different output from an **empty block list** ("the
   source was readable and had nothing"). A silent-empty ingest reads as "the
   source had nothing" and is a silent-proceed failure — these readers refuse it.
4. **Structural provenance, not a promise.** Every block carries a `locator`. A
   minted requirement stamps that locator plus the sha256 of the block text as its
   verbatim `source_ref` (`projection.block_source_ref`), so a re-ingest matches on
   *what the source actually said at that locator*, not on a minted key that
   renumbers across schemes. See `skills/_shared/req-key-conventions.md`.

## The block shape

Every block is `{"locator": str, "text": str}`. A tabular block also carries
`{"cells": {ref: value}}` so a single-cell locator resolves to the bare value via
`projection.find_span`. By convention the **first cells-bearing block of a sheet /
table is its header row** — the same convention across the xlsx, csv, and GitHub
Project readers, so a downstream skill needs no per-source special case.

| Reader | Source | Locator forms |
|---|---|---|
| `textual.py` | `.md` `.markdown` `.txt` `.log` | `line:N` |
| `csvreader.py` | `.csv` `.tsv` | `csv!A1`, `csv!A2:C2` (header = row 1) |
| `ooxml.py` | `.docx` | `para:N` |
| `ooxml.py` | `.xlsx` | `Sheet!A1`, `Sheet!A1:F1` |
| `ghproject.py` | saved `gh project item-list --format json` | `item:<num>`, `item:<num>!fields`, `item:<num>:<field>` |

## How an ingest skill calls them

```python
from skills.ingest._scripts import projection, ghproject

# a file on disk (xlsx / csv / docx / md):
proj = projection.build("/path/to/backlog.xlsx")
if proj["status"] != "ok":
    HALT(proj["reason"])              # "I cannot read this", not "it was empty"
for block in proj["blocks"]:
    ref = projection.block_source_ref(block)   # {"locator", "sha256"}
    # map block -> a per-requirement markdown block, stamp ref as source_ref,
    # reading the TARGET FILE's key scheme (never assume one) per
    # _shared/req-key-conventions.md

# a saved GitHub Project snapshot (a pinned, timestamped JSON, NOT a live read):
proj = ghproject.build(open("snapshot.json", "rb").read())
# proj["normalized_hash"] is the no-change de-dup key; proj["warnings"] carries
# any collision caveats (advisory, never a halt).
```

## Run them directly

```sh
python3 -m skills.ingest._scripts.projection /path/to/source.xlsx
python3 -m skills.ingest._scripts.ghproject  /path/to/snapshot.json
```

Both print the serialised projection JSON to stdout. A `status="skipped"`
projection still prints (with its `reason`) — that is the halt signal, surfaced,
not swallowed.

## Scope notes

- **GitHub Project is a snapshot, not a live read.** Run against a saved JSON the
  operator captured. A live board is as stale-prone as any other export (a field
  rename silently remaps "acceptance"); the same export discipline applies.
- **Staleness and origin stamping** (export timestamp, received-from, snapshot
  age) are the *ingest skill's* job, written into the per-requirement markdown.
  These readers only supply the locator + content hash they are built on.
- These readers are **portable**: drop the `_scripts/` package into any cloned
  repo and the ingest skills are runnable with no install step.
