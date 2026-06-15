#!/usr/bin/env python3
"""ooxml.py — docx / xlsx text projection (stdlib zipfile + xml.etree only).

A .docx or .xlsx is a ZIP of XML parts. This reader walks the parts deterministic-
ally and emits locator-addressed blocks. No third-party library, no network, no
formula evaluation — a cell that holds a formula contributes its STORED lexical
value (the last computed result Excel wrote), never a re-evaluation. Run it twice
on the same bytes and the blocks are identical.

extract(data, fmt) -> (blocks, adapter), fmt in {"docx", "xlsx"}.

Never raises a bare exception for a content problem: a non-ZIP payload, a legacy
binary Office container, a missing required part, an unparseable worksheet — each
becomes a ProjectionError, which the dispatcher turns into status="skipped". A
skipped projection is a HALT signal to the ingest skill ("I cannot read this"),
deliberately distinct from an empty block list ("the source had nothing").

LOCATORS:

    docx   para:N            N counts emitted paragraphs and table rows in body
                             order (empty paragraphs skipped, so N is the Nth
                             non-empty block, stable across re-reads).
    xlsx   Sheet!A1          a single-cell row.
           Sheet!A1:F1       a multi-cell row; the block carries a cells map
                             {"A1": value, ...} so a single-cell locator
                             (Sheet!C1) resolves to the bare value via
                             projection.find_span. The first cells-bearing block
                             of a sheet is that sheet's header row, by convention.
"""

import io
import posixpath
import xml.etree.ElementTree as ET
import zipfile
import zlib

from . import projection

ProjectionError = projection.ProjectionError

REQUIRED_MEMBER = {
    "docx": "word/document.xml",
    "xlsx": "xl/workbook.xml",
}


def extract(data, fmt):
    if fmt not in REQUIRED_MEMBER:
        raise ProjectionError("ooxml reader does not handle format %r" % fmt)
    zf = _zopen(data, REQUIRED_MEMBER[fmt], fmt)
    blocks = {"docx": _docx, "xlsx": _xlsx}[fmt](zf)
    return blocks, "ooxml-" + fmt


def _zopen(data, required_member, fmt):
    if not data.startswith(b"PK\x03\x04"):
        if data.startswith(b"\xd0\xcf\x11\xe0"):
            raise ProjectionError(
                "legacy/encrypted binary Office container under a .%s extension; "
                "convert or decrypt it locally and re-stage" % fmt)
        raise ProjectionError(
            "extension .%s but the bytes are not a ZIP container" % fmt)
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
        names = set(zf.namelist())
    except zipfile.BadZipFile as exc:
        raise ProjectionError("unreadable ZIP container (%s)" % exc)
    if required_member not in names:
        raise ProjectionError(
            "ZIP container without %s; extension and content disagree"
            % required_member)
    return zf


def _zread(zf, member):
    try:
        return zf.read(member)
    except (KeyError, zipfile.BadZipFile, zlib.error, EOFError, OSError) as exc:
        raise ProjectionError("zip member %s unreadable (%s)" % (member, exc))


def _local(tag):
    """Strip an XML namespace, leaving the local element name."""
    return tag.rsplit("}", 1)[-1]


def _gather_text(el):
    """Concatenate <...:t> text runs under el in document order; tab / br / cr
    become a single space. Used for a <w:p>, whose runs never contain a table —
    a table is a sibling of a paragraph in the body, never a child of one — so
    this stays safely recursive. For a table CELL, use _cell_own_text instead:
    a cell CAN contain a nested table, and a recursive gather there would slurp
    the nested table's text into the parent row (the double-count bug)."""
    parts = []
    for node in el.iter():
        t = _local(node.tag)
        if t == "t" and node.text:
            parts.append(node.text)
        elif t in ("tab", "br", "cr"):
            parts.append(" ")
    return "".join(parts)


def _cell_own_text(tc):
    """The text a table cell contributes to ITS OWN row — the paragraphs that are
    direct children of the cell only. A nested <w:tbl> inside the cell is NOT
    gathered here; it is walked separately by _walk_table so its rows become their
    own blocks. This is what makes a nested table appear under exactly ONE locator
    (its own para:N) instead of two (also flattened into the parent row), so each
    block's text is a single source span and its sha256 source_ref is stable."""
    parts = []
    for child in tc:
        if _local(child.tag) == "p":
            t = _gather_text(child).rstrip()
            if t:
                parts.append(t)
    return " ".join(parts)


def _direct_rows(tbl):
    """The <w:tr> rows that belong to THIS table — its direct children only, never
    a nested table's rows (which _walk_table reaches by descending into the cell
    that holds them). Iterating tbl directly, not tbl.iter(), is the fix: iter()
    is recursive and would yield a nested table's rows here too."""
    return [c for c in tbl if _local(c.tag) == "tr"]


def _walk_table(tbl, blocks, n):
    """Emit one block per row of tbl in document order, descending into a nested
    table immediately after its containing row so its rows get the next sequential
    para:N. Each row is visited exactly once; no text appears under two locators.
    Returns the running block counter n."""
    for tr in _direct_rows(tbl):
        cells = [c for c in tr if _local(c.tag) == "tc"]
        row = " — ".join(_cell_own_text(tc) for tc in cells)
        if row.strip():
            n += 1
            blocks.append({"locator": "para:%d" % n, "text": row.rstrip()})
        # descend into any nested table(s), in document order, as their own blocks
        for tc in cells:
            for nested in (c for c in tc if _local(c.tag) == "tbl"):
                n = _walk_table(nested, blocks, n)
    return n


def _read_rels(zf, rels_path):
    out = {}
    if rels_path not in zf.namelist():
        return out
    root = ET.fromstring(_zread(zf, rels_path))
    for rel in root:
        if _local(rel.tag) == "Relationship":
            out[rel.attrib.get("Id", "")] = (
                rel.attrib.get("Target", ""), rel.attrib.get("Type", ""))
    return out


def _resolve_part(target, base_dir):
    if target.startswith("/"):
        return target[1:]
    return posixpath.normpath(posixpath.join(base_dir, target))


def _rid_attr(el):
    for k, v in el.attrib.items():
        if k.endswith("}id") or k.endswith("}embed"):
            return v
    return None


def _docx(zf):
    """One block per non-empty paragraph and per table row, in body order; para:N
    locators (N over emitted blocks). A NESTED table is walked structurally — its
    rows are emitted as their own blocks exactly once, and are NOT also flattened
    into the parent row. So every source span maps to a single para:N and the
    sha256 of a block's text (its source_ref) is stable and unique: there is no
    span that two conflicting locators both claim."""
    try:
        root = ET.fromstring(_zread(zf, "word/document.xml"))
    except ET.ParseError as exc:
        raise ProjectionError("word/document.xml does not parse (%s)" % exc)
    body = next((c for c in root if _local(c.tag) == "body"), None)
    if body is None:
        raise ProjectionError("word/document.xml has no <w:body>")
    blocks, n = [], 0
    for child in body:
        tag = _local(child.tag)
        if tag == "p":
            text = _gather_text(child).rstrip()
            if text:
                n += 1
                blocks.append({"locator": "para:%d" % n, "text": text})
        elif tag == "tbl":
            n = _walk_table(child, blocks, n)
    return blocks


def _xlsx(zf):
    """One block per non-empty row. Cells are serialised ref=value verbatim from
    their STORED lexical value — formulas are never evaluated. The block locator
    is Sheet!First when a row has one cell, Sheet!First:Last otherwise; each block
    carries its cells map so a single-cell locator resolves to the bare value."""
    try:
        wb = ET.fromstring(_zread(zf, "xl/workbook.xml"))
    except ET.ParseError as exc:
        raise ProjectionError("xl/workbook.xml does not parse (%s)" % exc)
    rels = _read_rels(zf, "xl/_rels/workbook.xml.rels")
    shared = []
    if "xl/sharedStrings.xml" in zf.namelist():
        ss = ET.fromstring(_zread(zf, "xl/sharedStrings.xml"))
        for si in ss:
            if _local(si.tag) == "si":
                shared.append("".join(
                    node.text or "" for node in si.iter()
                    if _local(node.tag) == "t"))
    sheets = []
    for el in wb.iter():
        if _local(el.tag) != "sheet":
            continue
        tgt = rels.get(_rid_attr(el))
        if tgt:
            sheets.append((el.attrib.get("name", ""),
                           _resolve_part(tgt[0], "xl")))
    blocks = []
    for name, part in sheets:
        try:
            sroot = ET.fromstring(_zread(zf, part))
        except ET.ParseError as exc:
            raise ProjectionError("worksheet %s unreadable (%s)" % (part, exc))
        for row in (e for e in sroot.iter() if _local(e.tag) == "row"):
            cells = {}
            for c in (e for e in row if _local(e.tag) == "c"):
                ref = c.attrib.get("r", "")
                ctype = c.attrib.get("t", "n")
                v_el = next((e for e in c if _local(e.tag) == "v"), None)
                is_el = next((e for e in c if _local(e.tag) == "is"), None)
                if ctype == "s" and v_el is not None and v_el.text is not None:
                    try:
                        val = shared[int(v_el.text)]
                    except (IndexError, ValueError) as exc:
                        raise ProjectionError(
                            "cell %s references a missing shared string (%s)"
                            % (ref or "?", exc))
                elif ctype == "inlineStr" and is_el is not None:
                    val = "".join(node.text or "" for node in is_el.iter()
                                  if _local(node.tag) == "t")
                elif v_el is not None and v_el.text is not None:
                    val = v_el.text
                else:
                    continue
                if val == "":
                    continue
                cells[ref] = val
            if not cells:
                continue
            refs = list(cells)
            loc = ("%s!%s" % (name, refs[0]) if len(refs) == 1
                   else "%s!%s:%s" % (name, refs[0], refs[-1]))
            text = "; ".join("%s=%s" % (r, v) for r, v in cells.items()).rstrip()
            blocks.append({"locator": loc, "text": text, "cells": cells})
    return blocks
