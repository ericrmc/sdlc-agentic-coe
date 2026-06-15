#!/usr/bin/env python3
"""csvreader.py — CSV / TSV projection (stdlib csv only).

This is the GAP filled: the xlsx reader handles workbooks, but a tabular source
exported as plain CSV had no projection. This reader mirrors the xlsx block shape
exactly, so a CSV row and a worksheet row map to a requirement the same way and a
downstream skill needs no special case.

extract(data) -> (blocks, adapter). Deterministic: stdlib csv.reader with sniffed-
then-defaulted dialect, one block per row, A1-style cell references derived from
column position (column 1 -> A, 27 -> AA, the spreadsheet convention), so a cell
locator reads the way an operator reads a spreadsheet. Values are kept VERBATIM —
nothing is coerced, evaluated, or reinterpreted (a leading-zero code, a date-like
string, a formula-looking string all survive byte-for-byte).

Never raises for a content problem: a CSV that the parser cannot make any rows
from comes back as a ProjectionError (the dispatcher skips it -> the ingest skill
HALTs). An empty-but-readable file is an honest empty block list, distinct from a
skip.

LOCATORS (the xlsx convention, with a row-anchored sheet name "csv"):

    csv!A1            a single-cell row (rare; a one-column CSV).
    csv!A2:C2         a multi-cell data row; the block carries a cells map
                     {"A2": value, ...} so a single-cell locator (csv!B2)
                     resolves to the bare value via projection.find_span.

The header row, when present, is row 1 (csv!A1:...): it is the FIRST cells-bearing
block, the same "first block is the header" convention the xlsx and GitHub Project
readers share. Row numbers are 1-based over the original file rows, so a locator
points at the line an operator would scroll to.
"""

import csv
import io

from . import projection

ProjectionError = projection.ProjectionError

ADAPTER = "csv"
SHEET = "csv"
# Guard a pathological single-cell line from blowing memory; a CSV row with more
# columns than this is almost certainly not a requirements export.
_MAX_COLS = 16384


def extract(data):
    """One block per non-empty row, cells serialised ref=value verbatim. Mirrors
    the xlsx reader's block shape so a CSV and a worksheet ingest identically."""
    if isinstance(data, bytes):
        text = data.decode("utf-8-sig", "replace")
    else:
        text = data
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip():
        # readable, but nothing in it: honest empty, NOT a skip.
        return [], ADAPTER
    dialect = _sniff(text)
    try:
        reader = csv.reader(io.StringIO(text), dialect)
        rows = list(reader)
    except csv.Error as exc:
        raise ProjectionError("CSV does not parse (%s)" % exc)
    blocks = []
    for r, row in enumerate(rows, 1):
        cells = {}
        for col, raw in enumerate(row):
            if col >= _MAX_COLS:
                break
            val = raw.rstrip("\n")
            if val == "":
                continue
            cells["%s%d" % (_letters(col), r)] = val
        if not cells:
            continue
        refs = list(cells)
        loc = ("%s!%s" % (SHEET, refs[0]) if len(refs) == 1
               else "%s!%s:%s" % (SHEET, refs[0], refs[-1]))
        text_repr = "; ".join("%s=%s" % (ref, v) for ref, v in cells.items())
        blocks.append({"locator": loc, "text": text_repr, "cells": cells})
    if not blocks:
        # Parser ran but produced no usable cells from a non-blank file — the
        # source is not the tabular shape it claimed. Skip, do not pretend empty.
        raise ProjectionError(
            "no non-empty rows parsed from a non-blank CSV — the delimiter may be "
            "wrong or the file is not tabular; stage a clean export or paste rows")
    return blocks, ADAPTER


def _sniff(text):
    """A stable dialect for the file. csv.Sniffer when it is confident, else a
    deterministic default keyed off the first line's delimiter counts (TAB over
    comma over semicolon over pipe), never a guess that varies run to run."""
    sample = "\n".join(text.split("\n", 20)[:20])
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t;|")
    except csv.Error:
        first = text.split("\n", 1)[0]
        for delim in ("\t", ",", ";", "|"):
            if delim in first:
                class _D(csv.excel):
                    delimiter = delim
                return _D
        return csv.excel


def _letters(i):
    """0 -> A, 25 -> Z, 26 -> AA — spreadsheet column letters."""
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(ord("A") + r) + s
    return s
