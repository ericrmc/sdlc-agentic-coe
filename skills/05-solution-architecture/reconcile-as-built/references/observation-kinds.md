# Observation kinds — reconcile-as-built

The reconcile-as-built skill emits **neutral observations** when diffing an as-built
document against the as-designed sections, requirements, and acceptance criteria.
There are **exactly four kinds**, and only these four. None of them is a verdict.

This is a delivery reviewer's notebook, not a gate. The skill names the divergences;
a human dispositions them. Nothing here ever FAILs a build.

---

## The four kinds

### `match`
An as-designed section or requirement is **clearly reflected** in the as-built
document.

- A **section** match: an as-built block aligns with a designed section (deterministic
  test: Jaccard word-overlap of the bodies `>= 0.35`).
- A **requirement** match: the requirement is evident in the as-built text
  (deterministic test: the `req_key` appears literally, OR the requirement text's
  Jaccard overlap with the full as-built text is `>= 0.5`).

### `difference`
An as-built section is **present but diverges substantially** from the as-designed
content. The thing was built and is recognisably the same section — but the content
drifted (deterministic test: section body Jaccard overlap `< 0.35`). This is "review
the divergence," not "wrong."

### `addition`
The as-built document contains a section with **no corresponding as-designed
section** — possible new scope. Something was built that the design didn't describe.
This is "is this new scope?", a candidate to capture as a requirement — not a problem.

### `gap`
An as-designed section or requirement has **no evident coverage** in the as-built
document.

> **A `gap` means "confirm whether it was dropped." It is NEVER a failure.** The
> designed thing isn't visible in what was built — maybe it was dropped on purpose,
> maybe built differently under another name, maybe missed. The reviewer decides; the
> skill only flags.

---

## Field rules per kind

Every observation carries `observation`, `section_key`, `section_title`, `req_key`,
`message`, `detail`. The keys that are set vs. `null` depend on the kind:

| Kind | `section_key` | `section_title` | `req_key` | `detail` (typical) |
|------|---------------|-----------------|-----------|--------------------|
| `match` (section) | designed section's key | designed section's title | `null` | `{"overlap": 0.62}` |
| `match` (requirement) | `null` | `null` | requirement's key | `{"matched_by": "key"}` or `{"matched_by": "text"}` |
| `difference` | designed section's key | designed section's title | `null` | `{"overlap": 0.18}` |
| `addition` | `null` | the **as-built** heading | `null` | `{}` |
| `gap` (section) | designed section's key | designed section's title | `null` | `{}` |
| `gap` (requirement) | `null` | `null` | requirement's key | `{"requirement_text": "..."}` |

Rules of thumb:
- **Section observations** (`match`/`difference`/`gap` on a section) carry the
  **designed** `section_key` + `section_title`, and leave `req_key = null`.
- **Requirement observations** (`match`/`gap` on a requirement) carry the `req_key`,
  and leave `section_key` + `section_title = null`.
- **`addition`** is special: it has **no design key**, so `section_key = null` and
  `section_title` is the **as-built heading** that had no design counterpart.
- **`message`** is always a short, neutral, human-readable note — never a directive
  verdict.
- **`detail`** is a small facts object; it may be empty `{}`.

---

## Examples (the four-kind JSON shape)

```json
{
  "findings": [
    {
      "observation": "match",
      "section_key": "solution_overview",
      "section_title": "Solution Overview",
      "req_key": null,
      "message": "The as-built 'Solution Overview' section aligns with the design.",
      "detail": { "overlap": 0.62 }
    },
    {
      "observation": "match",
      "section_key": null,
      "section_title": null,
      "req_key": "F-1",
      "message": "Requirement F-1 appears reflected in the as-built document.",
      "detail": { "matched_by": "key" }
    },
    {
      "observation": "difference",
      "section_key": "data_model",
      "section_title": "Data Model",
      "req_key": null,
      "message": "The as-built 'Data Model' section differs substantially from the as-designed content. Review the divergence.",
      "detail": { "overlap": 0.18 }
    },
    {
      "observation": "addition",
      "section_key": null,
      "section_title": "Audit Log Export",
      "req_key": null,
      "message": "The as-built document includes 'Audit Log Export', which has no corresponding design section. Is this new scope?",
      "detail": {}
    },
    {
      "observation": "gap",
      "section_key": "offline_mode",
      "section_title": "Offline Mode",
      "req_key": null,
      "message": "The as-built document has no section matching 'Offline Mode'. Was this built differently or omitted?",
      "detail": {}
    },
    {
      "observation": "gap",
      "section_key": null,
      "section_title": null,
      "req_key": "NFR-2",
      "message": "Requirement NFR-2 is not evident in the as-built document. Was it built?",
      "detail": { "requirement_text": "The system must respond within 200ms at p95." }
    }
  ]
}
```

---

## Deterministic thresholds (the spine)

The deterministic pass uses pure string/set math — no library, no model, no network:

- **Heading split:** ATX headings (`#`..`######`); preamble before the first heading
  is its own block; empty leading blocks are dropped.
- **Section match — Tier 1:** as-built heading equals the designed `title`,
  case-insensitive.
- **Section match — Tier 2:** the designed `section_key` keywords (split on `_`)
  intersect the as-built heading's words.
- **Section drift:** body Jaccard overlap `< 0.35` -> `difference`; `>= 0.35` ->
  `match`.
- **Requirement coverage:** literal `req_key` substring (case-insensitive) ->
  `match` by key; else requirement-text Jaccard vs. full as-built text `>= 0.5` ->
  `match` by text; else -> `gap`.

When a model is available, the LLM step does the same reconciliation with judgement
(and weighs the acceptance criteria), but it stays strictly inside the same four
kinds and the same field rules.
