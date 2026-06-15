---
name: import-external-design
description: Merge an externally-authored design (any markdown structure) onto the canonical frozen-8 sections — preserve, integrate, dedupe overlapping statements, thread req_keys inline, bucket the genuinely-unmappable as 'unmapped'; produce a per-section candidate-vs-current diff before adopting. Use when a specialist authored a design elsewhere and it must land on the canonical sections.
when_to_use: a specialist authored a design elsewhere (another IDE, team, or agent) and it must land on the canonical frozen-8 sections without losing fidelity or scope
output_kinds: [proposal]
deterministic_fallback: heading-split + section title/keyword matching onto the frozen-8
suggested_tier: opus
---

# import-external-design

Merge an externally-authored solution design — written in whatever structure its author chose — onto **the canonical frozen-8 sections** that are this project's single source of truth. You are an **editor**, not a co-author: preserve what is already there, integrate the new material faithfully, dedupe overlap, thread requirement keys inline, and never invent scope. The genuinely-unmappable goes into an `unmapped` bucket — never force-fit.

This skill supports **scaffold-then-handoff**: a specialist (a solution architect, a partner team, another agent) authors the design *elsewhere*, and this is how their work lands on the canonical sections in-voice, with a reviewable diff, instead of being pasted over the top.

## Purpose

A design authored outside this project arrives as one or more markdown files with arbitrary headings. The project already holds a sectioned design under a **fixed** set of canonical keys (the "frozen-8"). This skill maps and merges the incoming material into the correct canonical sections so it becomes authoritative — **faithfully, never inventing scope** — and hands you a per-section **candidate-vs-current diff** to review *before* you adopt anything.

Truth is only written when you adopt the diff. The incoming bundle is **input, never truth**.

## The frozen-8 canonical sections

You may only target these eight `section_key` values. Never invent a section.

| `section_key`            | Title                              | Roughly holds                                                        |
| ------------------------ | ---------------------------------- | ------------------------------------------------------------------- |
| `background_context`     | Background & context               | Why this exists, the problem, the situation, drivers, scope framing |
| `business_architecture`  | Business architecture              | Capabilities, value streams, business processes, actors, outcomes   |
| `requirements_acceptance`| Requirements & acceptance criteria | What must be true, acceptance conditions, functional behaviour      |
| `application_architecture`| Application & solution shape      | Components, services, data flow, integrations, the technical shape   |
| `quality_nfrs`           | Quality attributes & NFRs          | Performance, security, availability, a11y/WCAG, operability targets |
| `key_decisions`          | Key decisions & trade-offs         | Decisions made, options weighed, rationale, what was rejected       |
| `estimate_plan`          | Estimate & delivery plan           | Sizing, phases/releases/waves, sequencing, effort, milestones       |
| `open_questions`         | Open questions & risks             | Unknowns, risks, assumptions, things still to resolve               |

## When to use

- A specialist authored a solution design **outside** this project and you need to land it on the canonical sections.
- An external partner / consultancy delivered a design bundle and you want it integrated, not bolted on.
- Another agent or workflow produced design markdown and you want it merged in-voice, deduped against what exists, with a diff to review.

**Do not use this** for incrementally generating a section from scratch (that is a generate step), or for reconciling a design against requirements after the fact (that is a reconcile step). This skill is specifically about *landing external prose onto fixed sections*.

## Inputs

You supply:

1. **The incoming design bundle** — one or more markdown files, any headings. If multiple files, keep per-file provenance (fence each file with an invisible marker so the source survives, e.g. `<!-- design-import-file: <filename> -->` on its own line before each file's content).
2. **The current canonical sections** — the existing `body_md` for each of the frozen-8 keys (empty string if a section has nothing yet). This is what you merge *into*.
3. **The project requirements** (optional but recommended) — a list of `req_key` + short text, so you can thread traceability references inline where the design plainly addresses a requirement.

## The method

The method has a **deterministic spine** and an **LLM merge step**. Run the deterministic step first so you always have a defensible routing even if the LLM step is skipped or unavailable; then run the LLM step to do the real preserve-and-integrate merge. Always end with a diff for a human.

### Step 1 — Concatenate and fence the bundle (deterministic)

If the design arrived as several files, concatenate them into one markdown bundle, fencing each file so provenance survives the merge:

```
<!-- design-import-file: architecture.md -->
# Solution Architecture
...file content...

<!-- design-import-file: nfrs.md -->
# Non-functional requirements
...file content...
```

The fences are ATX-invisible (HTML comments), so they don't disturb heading structure but let you attribute any block back to its source file.

### Step 2 — Heading-split + route to the frozen-8 (deterministic fallback)

Split the bundle on its top-level (and second-level) headings into **blocks** (heading + the prose beneath it). For each block, route it to a canonical `section_key` by matching the block's heading — and, if the heading is ambiguous, its body keywords — against the frozen-8 titles and their topic vocabulary:

| Route to                  | Heading / keyword signals                                                                 |
| ------------------------- | ----------------------------------------------------------------------------------------- |
| `background_context`      | background, context, overview, problem, purpose, drivers, scope, introduction             |
| `business_architecture`   | business, capability, value stream, process, actor, stakeholder, outcome, operating model |
| `requirements_acceptance` | requirement, acceptance, user story, functional, criteria, must/should, behaviour         |
| `application_architecture`| architecture, component, service, data flow, integration, API, system, sequence, the technical shape |
| `quality_nfrs`            | non-functional, NFR, performance, latency, security, availability, scalability, accessibility, WCAG, a11y, observability, SLO/SLA |
| `key_decisions`           | decision, trade-off, option, ADR, rationale, chose, rejected, alternative                 |
| `estimate_plan`           | estimate, sizing, effort, plan, phase, release, wave, roadmap, timeline, milestone, sequencing |
| `open_questions`          | open question, risk, assumption, unknown, TBD, to be resolved, dependency, concern         |

A block that matches **no** signal is parked as **unmapped** — it is not force-fit into the nearest section.

This deterministic routing is the fallback: it gives you a coarse but honest placement (heading goes to a section, body follows) when you can't run the LLM merge.

### Step 3 — LLM merge: preserve + integrate + dedupe + thread req_keys

This is the load-bearing step. For **each** canonical section that the incoming design has relevant content for, produce a **merged body** that:

- **PRESERVES** the existing section body and **INTEGRATES** the incoming content into it — you are extending and enriching, not replacing.
- **DEDUPES** overlapping statements — do not say the same thing two ways. If the incoming design restates something already present, fold them into one clean statement.
- Is written **in the section's voice** as clean markdown (you may use `###` sub-headings *inside* a section to organise).
- Threads relevant **`req_key`s inline** where the design plainly addresses them (e.g. "...the ingest pipeline (REQ-014) validates each file before...").

Rules that keep the merge honest:

- **Leave a section out entirely** if the incoming design adds nothing to it. Do not echo an unchanged body — silence means "no change to this section."
- Put any incoming content that fits **no** canonical section into `unmapped`. **Never invent a section, never force-fit.**
- **Never invent scope.** If the incoming design doesn't say it, you don't add it. Faithful, not creative.

Use this prompt (substitute the bracketed inputs):

```
You are synthesising an EXTERNALLY-AUTHORED solution design (written in another IDE / by
another team, in WHATEVER structure they chose) onto this project's FIXED set of canonical
design sections. The sectioned design is the single source of truth; your job is to map and
MERGE the incoming material into the correct sections so it becomes authoritative —
faithfully, never inventing scope.

THE CANONICAL SECTIONS (you may ONLY use these section_key values; never invent a section):
[for each of the frozen-8: section_key — Title — current body_md]

THE INCOMING DESIGN (one or more files, arbitrary headings):
[the fenced bundle markdown]

THE PROJECT REQUIREMENTS (for traceability — reference req_keys where the design plainly
addresses them):
[req_key + short text, one per line]

For EACH canonical section that the incoming design has relevant content for, produce a
MERGED body that:
- PRESERVES the existing section body (shown above) and integrates the incoming content into it,
- DEDUPES overlapping statements (do not repeat the same point in two ways),
- is written as clean markdown in that section's voice (you may use ### sub-headings inside a section),
- references the relevant req_keys inline where the design addresses them.
Leave a section OUT of "sections" if the incoming design adds nothing to it (do not echo an
unchanged body). Put any incoming content that genuinely fits NO canonical section into
"unmapped" (do NOT force-fit it).

Return ONLY a JSON object of exactly this shape, no prose, no fence:
{
  "sections": [
    { "section_key": "one of the canonical keys", "body_md": "the merged markdown body for this section" }
  ],
  "unmapped": [
    { "heading": "the incoming heading", "body": "the content", "source_filename": "which file (or empty)" }
  ]
}
```

### Step 4 — Produce a per-section candidate-vs-current DIFF (review before adopt)

For each merged candidate, compute a diff of **current body → candidate body** and present it for human review. This is a PR-style diff: the reviewer sees exactly what would change in each section before anything is adopted. Skip sections where the candidate is byte-identical to the current body (no spurious "changed" entries — one diff per genuinely-changed section).

**Nothing is authoritative until a human reviews this diff and adopts it.** The preview is pure: produce the candidates and the diff, write nothing. On adopt, the accepted candidates replace those section bodies (and the unmapped bucket is surfaced separately for the author to place by hand or discard).

## Output format

Return a single markdown review document. Lead with the unmapped bucket (it is the thing most likely to need a human decision), then one block per changed section showing the diff, then the adopt instruction.

```markdown
# Design import — review before adopt

**Source:** 3 file(s) — architecture.md, nfrs.md, decisions.md
**Sections changed:** 4 of 8 · **Unmapped blocks:** 1

---

## Unmapped (fits no canonical section — place by hand or discard)

- **"Glossary of domain terms"** _(from architecture.md)_
  > Defines ledger, posting, settlement... [not force-fit; suggest a separate glossary doc or discard]

---

## Changed sections

### application_architecture — Application & solution shape  `changed`

```diff
  The system exposes a REST ingest API backed by raw-SQL repositories.
+ Incoming design files are concatenated into a single fenced bundle (REQ-014),
+ then synthesised onto the canonical sections by the merge step. Each accepted
+ section is written as a new versioned body; the bundle itself is never truth.
  Reconcile then checks the ingested design against requirements.
```

### quality_nfrs — Quality attributes & NFRs  `changed`

```diff
  Availability target: 99.5% during business hours.
+ ### Accessibility
+ All review surfaces meet WCAG 2.2 AA (REQ-031): diff views carry text
+ alternatives and are keyboard-navigable.
```

### key_decisions — Key decisions & trade-offs  `changed`
... (diff) ...

### open_questions — Open questions & risks  `changed`
... (diff) ...

---

## Sections unchanged (no incoming content): background_context, business_architecture, requirements_acceptance, estimate_plan

---

**To adopt:** accept the sections whose diffs you want; each replaces that section's
body as a new `ingested` version. Re-running the import supersedes this candidate set —
it does not stack.
```

## Notes & anti-patterns

- **Preserve, don't overwrite.** The default failure mode is treating the incoming design as a replacement. It is a *merge target*. Existing prose stays unless the incoming content genuinely supersedes it — and even then you fold, you don't blank.
- **Never force-fit into the nearest section.** If content belongs nowhere in the frozen-8, it goes to `unmapped`. A glossary, a meeting log, an org chart — park it; don't smear it across a section it doesn't belong in.
- **Never invent scope.** You are an editor with a faithful tone. If the incoming design didn't say it, it doesn't appear in the merged body — no "helpful" elaboration, no filling gaps.
- **Silence means no change.** Omit a section from the candidate set if the import adds nothing. Don't echo an unchanged body — it produces noise diffs and false "changed" signals.
- **One diff per genuinely-changed section.** Compute current→candidate and drop byte-identical candidates. The reviewer should only see real changes.
- **Diff before adopt — always.** The preview writes nothing. Truth is written only when a human accepts the diff. This is what keeps an external author's bundle from silently becoming the source of truth.
- **Thread req_keys, don't dump them.** Reference a requirement inline where the design *plainly* addresses it. Don't append a "requirements: REQ-1, REQ-2..." list that the author never wrote.
- **Provenance survives.** Keep the per-file fences so any merged statement — and especially any unmapped block — can be traced back to the file it came from.
- This is **advisory**: it produces a reviewable proposal, not an enforced gate. The human decides what lands. There is no approval state machine — just a clean diff and an adopt action.
