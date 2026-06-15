#!/usr/bin/env python3
"""ghproject.py — GitHub Project snapshot normaliser (stdlib json only).

Normalises the JSON output of `gh project item-list --format json` into the same
tabular block shape the xlsx and csv readers produce, so a GitHub Project board
ingests through the identical row-to-requirement path with no special case.

Run against a PINNED, TIMESTAMPED snapshot the operator captured (a saved JSON
file), NEVER a live board read at ingest time: a live board is exactly as stale-
prone as any other export — a field rename silently remaps "acceptance", a column
reorder shifts what a locator points at. The raw JSON the operator captured is the
authoritative original; this projection is a regenerable cache of it.

NORMALIZED means deterministic against gh's nondeterministic ordering:
  - items sorted by stable item number (numbered items numerically, then
    unnumbered draft items by gh item id);
  - columns in a canonical order — gh's own item/content fields pinned first,
    then every org-custom field alphabetically (no org field name is ever
    hardcoded);
  - list values joined sorted.
So two pulls of an unchanged board normalise to byte-identical blocks and the same
normalized_hash — a no-change re-ingest stages nothing. That hash is the content-
hash de-dup key (it lives beside the row content, not over gh's raw byte order).

Each item is its own one-row "sheet" keyed item:<num>, so its citation locator is
exactly what the tabular path emits — a statement citing item:<num> resolves with
no special case. Per item, three block families:

    item:<num>!fields    the header block — cells {"A1": <column>, "B1": ...}
                         (the "first block is the header" convention; the SAME
                         canonical column list for every item, so letters line up
                         across the whole snapshot).
    item:<num>           the row — cells {"A2": <value>, ...}, text the canonical
                         "field=value; ..." serialisation.
    item:<num>:<field>   one text-only block per non-empty field, so a single
                         field cites and resolves exactly.

<num> is content.number (the org-visible issue/PR number); a draft item with no
number falls back to gh's item id. Numbers are unique per REPO, not per board: a
board spanning repos can collide, so a colliding item re-keys to repo#number (gh
item id as last resort) and the collision is WARNED, never blocked — warnings ride
in the projection, an advisory caveat, never a halt.

build(raw) -> a projection dict (status="ok"/"skipped"), ready to serialise via
projection.serialise. NEVER raises for a content problem: a payload that is not a
gh item list comes back status="skipped" with a reason (the dispatcher's contract
-> the ingest skill HALTs).
"""

import hashlib
import json

from . import projection

ProjectionError = projection.ProjectionError
PROJECTION_VERSION = projection.PROJECTION_VERSION

ADAPTER = "gh-project"
KEY_COLUMN = "number"

# gh's OWN item/content field names (the tool's vocabulary, not an org's), pinned
# first in canonical column order; every other field sorts after, alphabetically.
CORE_ORDER = ("number", "title", "status", "assignees", "labels", "repo",
              "milestone", "type", "url", "body")


def build(raw, original="gh-project-items.json"):
    """The normalised projection dict for one pulled snapshot.

    raw is the bytes or str of a saved `gh project item-list --format json`
    response. NEVER raises for a content problem: a non-gh payload, malformed
    JSON, or items with no stable identity come back status="skipped" with a
    reason — the dispatcher's contract, so the ingest skill HALTs rather than
    silently proceeding on an empty board."""
    proj = {
        "projection_version": PROJECTION_VERSION,
        "original": original,
        "format": ADAPTER,
        "adapter": ADAPTER,
        "status": "ok",
        "reason": None,
        "blocks": [],
    }
    try:
        rows, columns, warnings = normalize(parse_items(raw))
    except ProjectionError as exc:
        proj["status"], proj["reason"] = "skipped", str(exc)
        return proj
    letters = [_letters(i) for i in range(len(columns))]
    header_text = "; ".join(columns)
    blocks = []
    for row in rows:
        loc = "item:%s" % row["key"]
        head_cells, cells, parts = {}, {}, []
        for i, col in enumerate(columns):
            head_cells[letters[i] + "1"] = col
            val = row["fields"].get(col, "")
            if val == "":
                continue
            cells[letters[i] + "2"] = val
            parts.append("%s=%s" % (col, val))
        blocks.append({"locator": loc + "!fields", "text": header_text,
                       "cells": head_cells})
        blocks.append({"locator": loc, "text": "; ".join(parts), "cells": cells})
        for col in columns:
            val = row["fields"].get(col, "")
            if val != "":
                blocks.append({"locator": "%s:%s" % (loc, col), "text": val})
    proj["blocks"] = blocks
    proj["items"] = len(rows)
    proj["columns"] = columns
    proj["normalized_hash"] = normalized_hash(rows)
    proj["content_hash"] = proj["normalized_hash"]
    proj["warnings"] = warnings
    return proj


def parse_items(raw):
    """The items list out of a raw gh response (bytes or str). ProjectionError
    when the payload is not a gh project item list."""
    try:
        doc = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ProjectionError("response is not JSON (%s)" % exc)
    items = doc.get("items") if isinstance(doc, dict) else None
    if not isinstance(items, list):
        raise ProjectionError(
            'response has no "items" list — expected the output of '
            "`gh project item-list --format json`")
    return items


def normalize(items):
    """(rows, columns, warnings), deterministic regardless of gh's ordering:
    rows sorted by stable item number, each {"key", "fields"}; columns = core gh
    fields present (pinned order) + org-custom fields (alphabetical). Colliding
    numbers (a board spanning repos) are re-keyed collision-proof and warned."""
    rows, gh_ids = [], []
    for it in items:
        if not isinstance(it, dict):
            raise ProjectionError("item entries must be JSON objects")
        fields = _flatten(it)
        gh_id = _scalar(it.get("id"))
        key = fields.get(KEY_COLUMN)
        if not key:
            key = gh_id
            if not key:
                raise ProjectionError(
                    "an item carries neither content.number nor an id — "
                    "no stable identity to key on")
            fields[KEY_COLUMN] = key
        rows.append({"key": key, "fields": fields})
        gh_ids.append(gh_id)
    warnings = _dedupe_keys(rows, gh_ids)
    rows.sort(key=lambda r: ((0, int(r["key"]), "") if r["key"].isdigit()
                             else (1, 0, r["key"])))
    present = set()
    for r in rows:
        present.update(r["fields"])
    columns = [c for c in CORE_ORDER if c in present]
    columns += sorted(c for c in present if c not in CORE_ORDER)
    return rows, columns, warnings


def _dedupe_keys(rows, gh_ids):
    """Collision-proof row keys. When two items share a number, EVERY colliding
    item re-keys to repo#number (gh item id when repos do not disambiguate), and
    the new key lands in the key column too, so locator, cited key, and the keyed
    diff never disagree. Collision-free boards are untouched. Returns warnings
    (advisory; never blocks)."""
    counts = {}
    for r in rows:
        counts[r["key"]] = counts.get(r["key"], 0) + 1
    warnings = []
    for k in sorted(key for key, n in counts.items() if n > 1):
        group = [(r, gid) for r, gid in zip(rows, gh_ids) if r["key"] == k]
        candidates = ["%s#%s" % (r["fields"]["repo"], k)
                      if r["fields"].get("repo") else "" for r, _ in group]
        if ("" in candidates or len(set(candidates)) != len(candidates)
                or any(c in counts for c in candidates)):
            candidates = [gid for _, gid in group]
        if ("" in candidates or len(set(candidates)) != len(candidates)
                or any(c in counts for c in candidates)):
            warnings.append(
                "item number %r appears %d times and carries nothing to "
                "disambiguate on — locator item:%s is AMBIGUOUS; cite with care"
                % (k, len(group), k))
            continue
        for (r, _), new in zip(group, candidates):
            r["key"] = new
            r["fields"][KEY_COLUMN] = new
        warnings.append(
            "item number %r appears %d times (a board spanning repos?) — "
            "re-keyed collision-proof as %s; cite item:<key>"
            % (k, len(group), ", ".join(sorted(candidates))))
    return warnings


def normalized_hash(rows):
    """sha256 over the canonical row serialisation — equal iff the normalised
    content is equal, whatever order gh emitted it in. The content-hash de-dup
    key: a no-change re-pull hashes identically and stages nothing."""
    canon = json.dumps(rows, sort_keys=True)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


# flattening -------------------------------------------------------------------

def _flatten(item):
    """One gh item -> flat {column: scalar string}. content.* lifts to columns
    first (content.repository -> repo); every other top-level key becomes a column
    under gh's own field name. Dicts read their title/name/login; lists join
    sorted. Empty values drop — an absent cell, the tabular way."""
    fields = {}
    content = item.get("content")
    pair_groups = []
    if isinstance(content, dict):
        pair_groups.append(content.items())
    pair_groups.append((k, v) for k, v in item.items()
                       if k not in ("id", "content"))
    for pairs in pair_groups:
        for k, v in pairs:
            name = "repo" if k == "repository" else k
            val = _scalar(v)
            if val != "":
                fields.setdefault(name, val)
    return fields


def _scalar(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, dict):
        for k in ("title", "name", "login"):
            v = value.get(k)
            if isinstance(v, str) and v:
                return v
        return json.dumps(value, sort_keys=True)
    if isinstance(value, (list, tuple)):
        return ", ".join(sorted(s for s in (_scalar(v) for v in value)
                                if s != ""))
    return str(value)


def _letters(i):
    """0 -> A, 25 -> Z, 26 -> AA — spreadsheet column letters."""
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(ord("A") + r) + s
    return s


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write("usage: ghproject.py <gh-project-items.json>\n")
        raise SystemExit(2)
    with open(sys.argv[1], "rb") as fh:
        print(projection.serialise(build(fh.read(), original=sys.argv[1])))
