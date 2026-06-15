#!/usr/bin/env python3
"""textual.py — plain text / markdown projection (stdlib only).

Every non-blank line becomes a line:N block, where N is the 1-based line number
in the original file (blank lines counted, so a locator survives a hexdump). This
is the deterministic floor for an unstructured source: when a docs folder holds a
markdown backlog or a pasted block of text, an ingest skill still gets a usable,
locator-addressed skeleton with no model in the loop.

extract(data) -> (blocks, adapter). Never raises: undecodable bytes are decoded
with errors="replace" rather than failing, because a projection of garbled text
is still a more honest output than a halt that hides recoverable content. (A truly
unreadable FILE — one that cannot be opened at all — is caught upstream in the
dispatcher and skipped there.)
"""

ADAPTER = "text-lines"


def extract(data):
    """One line:N block per non-blank line. N is 1-based over the original lines,
    blanks counted, CRLF normalised to LF."""
    if isinstance(data, bytes):
        text = data.decode("utf-8", "replace")
    else:
        text = data
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = []
    for i, line in enumerate(text.split("\n"), 1):
        line = line.rstrip()
        if line.strip():
            blocks.append({"locator": "line:%d" % i, "text": line})
    return blocks, ADAPTER
