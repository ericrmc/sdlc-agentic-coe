---
name: reconcile-as-built
description: After a build, diff an as-built markdown against the as-designed sections + requirements + acceptance criteria, emitting neutral observations in exactly four kinds (match/difference/addition/gap); a gap means "confirm whether dropped", never FAIL.
when_to_use: closing the design->reality loop at handover
output_kinds: [question, proposal]
deterministic_fallback: heading-split + req_key + Jaccard requirement scan
suggested_tier: sonnet
---

# reconcile-as-built — four neutral observation kinds at handover

## Purpose

At handover, the design->reality loop is still open. A solution was *designed*
(see `05-solution-architecture`), then it was *built* — and the two rarely match
line for line. Things get renamed, merged, deferred, or quietly added. Someone has
to look at what was actually delivered and reconcile it against what was on paper.

This skill does that reconciliation. You give it the **as-built** document (markdown
describing what was really delivered) and the **as-designed** material (the
solution-design sections, the requirements, and their acceptance criteria). It emits
**neutral observations** in exactly **four kinds** — `match`, `difference`,
`addition`, `gap`.

It is a **delivery reviewer's notebook, not a gate.** It does not pass or fail the
build. It does not block a release. A `gap` does **not** mean "this failed" — it
means "an as-designed thing has no evident coverage; **confirm whether it was
dropped**." The human reads the observations and dispositions them. The skill's whole
job is to make the divergences *visible and named* so nothing slips through handover
unnoticed.

Tone throughout: a calm delivery reviewer writing margin notes. Observations, never
verdicts. Never the word FAIL.

## When to use

- At **handover**, when an engineer submits an as-built / "what we actually
  shipped" document and you want to close the loop against the design.
- When you suspect **scope drift** — features added or dropped between design and
  delivery — and want a named, reviewable list rather than a vibe.
- As a **pre-retro / pre-sign-off** pass: surface every divergence so the team can
  decide which were intentional and which were accidental.

Not for: grading work, blocking merges, or producing a compliance score. There is no
score here, by design.

## Inputs

The user supplies, as markdown / context:

1. **As-built document** — markdown describing what was delivered. Ideally organised
   under headings (ATX `#`/`##` style). Free-form prose still works; it just yields
   coarser matches.
2. **As-designed sections** — the solution-design sections, each with a stable
   `section_key` (e.g. `solution_overview`), a human `title`, and the designed body
   markdown.
3. **Requirements** — each with a `req_key` (e.g. `F-1`, `NFR-3.2`) and its text.
4. **Acceptance criteria** — the AC text per requirement (optional but improves the
   LLM step's judgement of whether a requirement is truly reflected).

If some inputs are missing, the method **degrades gracefully** (see Step 5): with
zero designed sections, every as-built heading becomes an `addition` and every
requirement becomes a `gap` — it never crashes and never invents material.

## The four kinds (verbatim)

These are the only four observations. Reproduced from the source reconcile prompt:

- **`match`** — an as-designed section or requirement is clearly reflected in the
  as-built document.
- **`difference`** — an as-built section is present but diverges substantially from
  the as-designed content.
- **`addition`** — the as-built document contains a section that has no corresponding
  as-designed section (possible new scope).
- **`gap`** — an as-designed section or requirement has no evident coverage in the
  as-built document.

> A `gap` is an **invitation to confirm**, not a failure. It says: this designed
> thing isn't evident in what was built — *was it dropped on purpose, built
> differently, or missed?* The reviewer answers. The skill never decides.

### Field rules per observation kind

Carry these exactly — they keep observations machine-readable and unambiguous:

| Kind | `section_key` | `section_title` | `req_key` |
|------|---------------|-----------------|-----------|
| `match` (section) | the as-designed section's key | the as-designed section's title | `null` |
| `match` (requirement) | `null` | `null` | the requirement's key |
| `difference` | the as-designed section's key | the as-designed section's title | `null` |
| `addition` | `null` | the **as-built** heading (there is no design key) | `null` |
| `gap` (section) | the as-designed section's key | the as-designed section's title | `null` |
| `gap` (requirement) | `null` | `null` | the requirement's key |

Plus, for every observation:
- **`message`** — a short, neutral, human-readable note a reviewer would read.
  Never a directive verdict.
- **`detail`** — a small object of supporting facts (may be empty `{}`); e.g. the
  Jaccard `overlap` for a section, or `matched_by: "key" | "text"` for a requirement.

See [`references/observation-kinds.md`](references/observation-kinds.md) for the full
table with examples of each kind.

## The method (steps)

The method has a **deterministic spine** (Steps 1–4, runnable with pure
string/set operations — no markdown library, no network) and an **LLM reasoning
step** (Step 5) that does the same reconciliation with judgement. Run the LLM step
when you have a model; fall back to the deterministic spine when you don't, or run
both and let the deterministic pass catch anything the model glossed.

### Step 1 — Heading-split the as-built markdown

Split the as-built markdown into `(heading, body)` blocks on ATX headings
(`^#{1,6}\s+...`). Any preamble before the first heading becomes a block with an
empty heading. Drop a leading empty/preamble block that has no content. This is the
unit of comparison: one as-built block per heading.

### Step 2 — Section coverage (tiered title/keyword matching)

For **each as-designed section**, try to find a matching as-built block, in two
tiers:

- **Tier 1 — exact title.** A block whose heading equals the section `title`,
  case-insensitive (trimmed).
- **Tier 2 — section_key keyword.** Failing Tier 1, split the `section_key` on `_`
  into keywords (e.g. `solution_overview` -> `{solution, overview}`) and match a
  block whose heading's words intersect those keywords.

Then:
- **No block matched** -> emit a **`gap`** (section), carrying the section's
  `section_key` + `section_title`. Message in the spirit of: *"The as-built document
  has no section matching '<title>'. Was this part of the design built differently or
  omitted?"*
- **A block matched** -> mark that block index as consumed and proceed to Step 4
  (drift) for that section.

### Step 3 — Additions (unmatched as-built blocks)

Any as-built block that matched **no** designed section (and has a non-empty heading)
-> emit an **`addition`**, with `section_key = null` and `section_title =` the
as-built heading. Message in the spirit of: *"The as-built document includes
'<heading>', which has no corresponding design section. Is this new scope?"*

### Step 4 — Drift within matched sections + requirement coverage

**Drift (deterministic):** for each section matched in Step 2, compute the **Jaccard
overlap** of the lowercased word-sets of the designed body vs. the as-built block
body.
- overlap **< 0.35** -> emit a **`difference`** (carry `detail.overlap`). Message:
  *"The as-built '<title>' section differs substantially from the as-designed
  content. Review the divergence."*
- overlap **>= 0.35** -> emit a **`match`** (section). Message: *"The as-built
  '<title>' section aligns with the design."*

**Requirement coverage (deterministic):** for **each requirement**, scan the **full**
as-built text:
- If the `req_key` (e.g. `F-1`) appears literally (case-insensitive substring) ->
  **`match`** (requirement), `detail.matched_by = "key"`.
- Else, if the **Jaccard overlap** of the requirement text's word-set vs. the full
  as-built word-set is **>= 0.5** -> **`match`** (requirement),
  `detail.matched_by = "text"`.
- Else -> **`gap`** (requirement), carrying `detail.requirement_text`. Message:
  *"Requirement <key> is not evident in the as-built document. Was it built?"*

> **The deterministic step is exactly this:** the heading-split (Step 1) plus the
> Jaccard scan — section drift at the 0.35 overlap threshold and requirement coverage
> at the 0.5 Jaccard threshold (with the literal `req_key` substring shortcut). Pure
> string/set math; no library, no model, no network. It is the floor the method never
> drops below.

### Step 5 — LLM reconciliation pass (judgement)

When a model is available, run the reconcile-as-built prompt. It does the same
reconciliation as Steps 1–4 but with judgement — it can see that "User Onboarding
Flow" as-built covers the designed "Sign-up & Activation" section even though neither
the title nor the keyword nor the word-overlap would have caught it, and it can weigh
the **acceptance criteria** when deciding whether a requirement is genuinely
reflected.

Prompt (provider-agnostic; fill the two `${...}` slots):

```
You are a delivery reviewer on an internal managed-services delivery team. After a
build, the engineer submits an AS-BUILT document (markdown) describing what was
actually delivered. Your job is to reconcile that AS-BUILT document against the
AS-DESIGNED solution-design sections, the requirements, and their acceptance
criteria, and emit neutral OBSERVATIONS — never a pass/fail verdict.

You produce four kinds of observation, and only these four:
- "match"      — an as-designed section or requirement is clearly reflected in the as-built document.
- "difference" — an as-built section is present but diverges substantially from the as-designed content.
- "addition"   — the as-built document contains a section that has no corresponding as-designed section (possible new scope).
- "gap"        — an as-designed section or requirement has no evident coverage in the as-built document.

AS-DESIGNED MATERIAL (sections, then requirements with their acceptance criteria):
${designed_block}

AS-BUILT DOCUMENT (markdown):
${as_built_markdown}

Rules:
- Stay strictly within the material above. Do not invent sections, requirements, or scope.
- For a section observation, set "section_key" and "section_title" to the as-designed
  section's key and title (use null for an "addition", whose title is the as-built heading
  and whose section_key is null). Leave "req_key" null for section observations.
- For a requirement observation, set "req_key" to the requirement's key and leave
  "section_key" and "section_title" null.
- Every "message" must be a short, neutral, human-readable note (an observation a reviewer
  would read), never a directive verdict.
- "detail" is a small object of supporting facts (may be empty {}).
- If a designed section or requirement has no coverage, emit a "gap". If an as-built section
  matches nothing designed, emit an "addition".

Return ONLY a JSON object of exactly this shape, no prose, no markdown fence:
{
  "findings": [
    {
      "observation": "match",
      "section_key": "solution_overview",
      "section_title": "Solution Overview",
      "req_key": null,
      "message": "The as-built 'Solution Overview' aligns with the design.",
      "detail": {}
    },
    {
      "observation": "gap",
      "section_key": null,
      "section_title": null,
      "req_key": "F-1",
      "message": "Requirement F-1 is not evident in the as-built document.",
      "detail": {}
    }
  ]
}
```

Build `${designed_block}` by listing each section (`section_key` — `title`, then its
designed body) followed by each requirement (`req_key` — text, then its acceptance
criteria). Keep the model strictly inside that material — it must not invent
sections, requirements, or scope.

### Step 6 — Hand the observations to the human

Collect the observations from Step 5 (or the deterministic spine, or both). Present
them grouped by kind. **Stop there.** Every observation is `open` until a human reads
it; the skill assigns no status and reaches no verdict. The two things you may
propose are a **question** ("Requirement NFR-2 isn't evident — was it dropped or
just undocumented?") or a **proposal** ("the addition 'Audit Log Export' looks like
real new scope — capture it as a requirement?"). Both go to the human to disposition.

## Output format

Return a short markdown report grouped by the four kinds, then the raw observations.
Neutral throughout. Concrete template:

```markdown
## As-built reconciliation — observations

Reconciled the as-built document against N as-designed sections and M requirements.
These are neutral observations for review, not a pass/fail. A "gap" means **confirm
whether it was dropped**, not that anything failed.

### Matches (k)
- **Solution Overview** (`solution_overview`) — as-built section aligns with the design (overlap 0.62).
- **Requirement F-1** — appears reflected in the as-built document (matched by key).

### Differences (k) — present, but diverged; review the divergence
- **Data Model** (`data_model`) — as-built differs substantially from the as-designed content (overlap 0.18).

### Additions (k) — present in as-built, no design counterpart; possible new scope
- **Audit Log Export** — no corresponding design section. Is this new scope?

### Gaps (k) — designed, no evident coverage; **confirm whether dropped**
- **Offline Mode** (`offline_mode`) — no matching as-built section. Built differently, or omitted?
- **Requirement NFR-2** — not evident in the as-built document. Was it built?

### For the human to disposition
- Question: NFR-2 has no evident coverage — dropped, or just undocumented in the as-built?
- Proposal: "Audit Log Export" looks like genuine new scope — capture it as a requirement?
```

If you also emit structured data, use the four-kind JSON shape from Step 5 verbatim
so downstream tooling (an issue tracker, a Project board) can consume it.

## Notes / anti-patterns

- **Never FAIL.** There is no pass/fail, no score, no gate. A `gap` is "confirm
  whether dropped," a `difference` is "review the divergence," an `addition` is "is
  this new scope?" — all open questions for a human, never verdicts.
- **Exactly four kinds.** Do not invent a fifth (no "partial", no "warning", no
  "violation"). If something doesn't fit, it is a `difference` (diverged) or a `gap`
  (not evident).
- **Field rules are load-bearing.** An `addition` always has `section_key = null` and
  uses the *as-built* heading as its `section_title` (there is no design key to
  carry). Section observations leave `req_key = null`; requirement observations leave
  `section_key`/`section_title` null. Mixing these makes the output unmergeable.
- **Stay inside the material.** The LLM step must not invent sections, requirements,
  or scope. If it isn't in the as-designed material or the as-built document, it
  isn't an observation.
- **Degrade, don't crash.** Zero designed sections -> every block is an `addition`,
  every requirement a `gap`. Empty as-built -> every section/requirement a `gap`.
  Both are valid, informative outputs.
- **The deterministic spine is the floor.** When in doubt about the model, run the
  heading-split + Jaccard scan. It is cheap, repeatable, and never hallucinates — it
  just sees coarser matches than the model would.
- **Messages are margin notes.** Keep each `message` short, neutral, and readable —
  what a reviewer would jot, not an instruction.
