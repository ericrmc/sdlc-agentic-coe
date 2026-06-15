"""Deterministic, stdlib-only source readers for the ingest skill group.

A PROJECTION is a regenerable cache of locator-addressed text blocks lifted from a
structured source by deterministic parsing — no model, no network. These readers
are what the ingest skills call to turn a messy-but-structured source (a workbook,
a CSV, a docx, a GitHub Project snapshot) into a usable, citable skeleton before
any model reasons over it.

The package layout:

    projection.py   the dispatcher + resolution helpers (build, find_span,
                    block_source_ref, serialise, text_of). Routes a file by
                    extension to the right reader; returns a status="skipped"
                    projection (never raises) on any content problem.
    textual.py      plain text / markdown -> line:N blocks.
    csvreader.py    CSV / TSV -> tabular blocks (mirrors the xlsx shape).
    ooxml.py        docx / xlsx -> para:N / Sheet!A1 blocks (stdlib zip + xml).
    ghproject.py    a saved `gh project item-list --format json` snapshot ->
                    item:<num> blocks, with a normalized content-hash for
                    no-change re-ingest de-dup.

See README.md for the contract every reader honours.
"""
