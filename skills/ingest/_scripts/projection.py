#!/usr/bin/env python3
"""projection.py — the deterministic projection dispatcher (stdlib only).

A PROJECTION is a regenerable cache: locator-addressed text blocks lifted from a
structured source (a workbook, a CSV, a docx, a GitHub Project snapshot) by
deterministic parsing — NO model, no network, no evaluation of formulas. Run it
twice on the same bytes and you get byte-identical blocks. It is NEVER
authoritative: the original file the operator staged is the source of truth; this
cache only points back into it via a locator.

A projection NEVER raises for a content problem. An unsupported format, an
unreadable container, a payload that is not what its extension claims — all come
back as a dict with status="skipped" and a human-readable reason. The ingest
skill that calls this turns a skipped projection into a HALT ("I cannot read this
source"), which is a DIFFERENT output from an empty result ("the source had
nothing"). Silent-empty is a silent-proceed failure; this module refuses it.

The ingest skills call build(path) to get blocks, then map each block to a
per-requirement markdown block, stamping the block's locator + sha256 as the
verbatim source_ref (see skills/_shared/req-key-conventions.md). The locator is
how a downstream reader walks a minted requirement back to the exact span it came
from.

LOCATOR FORMS, by format:

    line:N                  plain text / markdown / csv-as-text (N = 1-based line)
    row:N / row:N!A1        csv (N = 1-based data row; cell ref A1-style)
    Sheet!A1 / Sheet!A1:C1  xlsx (single cell, or a row's first:last cell)
    para:N                  docx (N counts emitted paragraphs / table rows)
    item:<num>              GitHub Project item (see ghproject.py)

Every block carries {"locator": str, "text": str} and may carry {"cells": {ref:
value}} for tabular blocks so a single-cell locator resolves to the bare value.
The first cells-bearing block of a sheet/table is that sheet's header row, by
convention — the same convention the xlsx and GitHub Project readers share.
"""

import hashlib
import json
from pathlib import Path

PROJECTION_VERSION = "1"

# Suffix -> internal format tag. Extension-driven, but every reader re-checks the
# actual bytes and skips gracefully when extension and content disagree.
FORMATS = {
    ".md": "text", ".markdown": "text", ".txt": "text", ".log": "text",
    ".csv": "csv", ".tsv": "csv",
    ".docx": "ooxml-docx", ".xlsx": "ooxml-xlsx",
}


class ProjectionError(Exception):
    """An extraction cannot proceed. build() catches this and returns a dict
    with status="skipped"; it is never allowed to escape build()."""


# Readers import ProjectionError + PROJECTION_VERSION from here, so these imports
# come AFTER both are defined. The relative form works when this module is loaded
# as part of the package (the intended `python3 -m skills.ingest._scripts.projection`
# or an `import` from a calling skill). When the file is run as a bare script
# (`python3 skills/ingest/_scripts/projection.py <file>`) it has no parent package,
# so the relative import would ImportError at load time — before build() ever runs.
# That bare-script form is part of the contract (the self-check invokes it), so we
# bootstrap the package: put the repo root on sys.path and re-import each reader
# under its absolute package name. The readers' own `from . import projection`
# then resolves to THIS already-loaded module (it is registered in sys.modules under
# the package name below), so ProjectionError stays a single shared class and
# build()'s `except ProjectionError` keeps catching what the readers raise.
try:
    from . import csvreader, ooxml, textual  # noqa: E402
except ImportError:
    import os as _os
    import sys as _sys

    _PKG = "skills.ingest._scripts"
    _root = _os.path.dirname(  # .../skills/ingest/_scripts -> repo root
        _os.path.dirname(_os.path.dirname(_os.path.dirname(
            _os.path.abspath(__file__)))))
    if _root not in _sys.path:
        _sys.path.insert(0, _root)
    # Register this running module under its package name so the readers'
    # `from . import projection` binds to it instead of loading a second copy
    # (a second copy would give ProjectionError a different identity).
    _sys.modules.setdefault(_PKG + ".projection", _sys.modules[__name__])
    __package__ = _PKG
    from skills.ingest._scripts import csvreader, ooxml, textual  # noqa: E402


def build(path):
    """Extract locator-addressed blocks from a file on disk.

    Returns a projection dict ready to serialise. NEVER raises for a content
    problem: an unsupported or unreadable file comes back status="skipped" with a
    reason; a file that does not exist comes back skipped too. The only thing the
    caller must do is check status before reading blocks — a skipped projection
    means HALT, not empty."""
    path = Path(path)
    proj = {
        "projection_version": PROJECTION_VERSION,
        "original": path.name,
        "format": None,
        "adapter": None,
        "status": "ok",
        "reason": None,
        "blocks": [],
    }
    if not path.is_file():
        proj["status"], proj["reason"] = "skipped", (
            "no file at %s — the source must be staged locally before ingest"
            % path)
        return proj
    fmt = FORMATS.get(path.suffix.lower())
    proj["format"] = fmt or (path.suffix.lower().lstrip(".") or "(none)")
    try:
        data = path.read_bytes()
    except OSError as exc:
        proj["status"], proj["reason"] = "skipped", (
            "cannot read %s (%s)" % (path, exc))
        return proj
    try:
        if fmt == "text":
            blocks, adapter = textual.extract(data)
        elif fmt == "csv":
            blocks, adapter = csvreader.extract(data)
        elif fmt in ("ooxml-docx", "ooxml-xlsx"):
            blocks, adapter = ooxml.extract(data, fmt.split("-", 1)[1])
        else:
            raise ProjectionError(
                "unsupported format %r — stage a supported source "
                "(.md/.txt/.csv/.tsv/.docx/.xlsx) or paste the rows directly"
                % (path.suffix.lower() or "(none)"))
    except ProjectionError as exc:
        proj["status"], proj["reason"] = "skipped", str(exc)
        return proj
    proj["adapter"], proj["blocks"] = adapter, blocks
    proj["content_hash"] = hashlib.sha256(data).hexdigest()
    return proj


def from_dict(proj):
    """Pass-through for an already-built projection dict (e.g. the GitHub Project
    reader's build()), so the resolution helpers below work uniformly across an
    on-disk file and an in-memory snapshot."""
    return proj


def serialise(proj):
    """Deterministic JSON for the projection cache. Sorted keys, so the same
    blocks serialise byte-identically run to run — a no-change re-extract diffs
    clean and a content_hash de-dup is meaningful."""
    return json.dumps(proj, ensure_ascii=False, indent=1, sort_keys=True)


def text_of(proj):
    """The joined block text — grep fodder / similarity input for a skill that
    wants the whole source as one string."""
    return "\n".join(b["text"] for b in proj.get("blocks", ()))


def find_span(proj, locator):
    """Exact span text for a locator against a built projection, or None.

    Exact block-locator match first; then single tabular cells found inside their
    row block's cells map (so Costs!B14 resolves even though the block locator is
    the whole row Costs!A14:F14). None when nothing matches — the caller decides
    whether a missing locator is a halt or a tolerable gap."""
    locator = (locator or "").strip()
    if not locator:
        return None
    for b in proj.get("blocks", ()):
        if b.get("locator") == locator:
            return b["text"]
    # single tabular cell (Sheet!A1 or row:N!A1) inside a row block's cells map
    if "!" in locator and ":" not in locator:
        prefix, _, ref = locator.partition("!")
        for b in proj.get("blocks", ()):
            cells = b.get("cells")
            loc = b.get("locator", "")
            if cells and ref in cells and loc.startswith(prefix + "!"):
                return cells[ref]
    return None


def block_source_ref(block):
    """The verbatim source_ref a minted requirement carries: the block's locator
    plus the sha256 of its own text, so a re-ingest matches on what the source
    actually said at that locator — not on a minted key that renumbers across
    schemes (see _shared/req-key-conventions.md). Pure function of the block."""
    text = block.get("text", "")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return {"locator": block.get("locator", ""), "sha256": digest}


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write("usage: projection.py <source-file>\n")
        raise SystemExit(2)
    print(serialise(build(sys.argv[1])))
