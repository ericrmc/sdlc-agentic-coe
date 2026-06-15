---
name: necessity-check
description: When a specific technical component is proposed, ask "necessary for WHICH outcome?" — naming both ids and computing over-reach relative to a named outcome's NFRs. Raises the question; never asserts "gold-plated." The human rules; zero cuts is a legitimate outcome.
one_liner: Ask whether a proposed component earns its keep against a named outcome.
aliases: [gold-plating check, over-engineering check, is this component needed, scope creep check, justify this component, do we really need this, lean design check]
when_to_use: a specific technical component is proposed (Redis, Kafka, a queue, a cache, a second database) and you want to test that it isn't gold-plating relative to the outcomes it claims to serve
output_kinds: [question, halt]
deterministic_fallback: the component->NFR->outcome over-reach predicate
suggested_tier: mid
neighbours: |
  before: challenge/enumerate-roadblocks — pressure-testing the requirement set
  after: architect/recommend-component-patterns — choosing the components that survive the question
---

# necessity-check — anti-gold-plating tripwire

Ask whether a specific proposed component earns its keep against a named business outcome. Raise the **question**; never assert "gold-plated." The flag is computed; the human rules.

## Purpose

When a specific technical component shows up in a design — Redis, Kafka, a message queue, a read replica, a search cluster — there are exactly two honest possibilities: it earns its keep against a named business outcome, or it is reach beyond what any outcome needs. This skill does **not** decide which. It raises the **question**, and it names both ids so the human can rule in one glance:

> *"Redis serves only 'sub-200ms search' — already met by the adopted pattern. Necessary, or cut?"*

This is answerable **only because the `derives_from` trace edge exists** — the edge that threads a component to the NFR it satisfies, and that NFR to the outcome it serves. Walk that chain and the necessity question answers itself concretely instead of as a hunch. No trace edge, no honest necessity check.

The discipline is asymmetric on purpose:

- The skill **may** ask "necessary for which outcome?" and show its arithmetic.
- The skill **may never** say "this is gold-plated," "remove this," "over-engineered," or stamp a cut/keep verdict.
- A run that produces **zero cuts is a legitimate, non-failing outcome.** There is no acceptance-rate metric, no target cut count, nothing that pressures toward cutting. A clean design that survives the question is exactly as valid as one that loses a component.

## When to use

- A solution design or pattern adoption introduces a **named, specific component** and you want to test it isn't carrying weight no outcome asked for.
- The validation step surfaced a component whose NFRs are **already satisfied upstream** (e.g. the adopted pattern already meets the latency target the component was added for).
- Before a build handoff, as a final sweep over the component list.

Do **not** use this to rank components, to score a design, or to produce a "leanness" verdict. It fires once per component and emits one question (or stays silent). It is a tripwire, not a reviewer.

## Inputs

The user supplies (as markdown, or points you at the files):

1. **The component under test** — *Required.* A named id and one line of what it is (`comp:redis — in-memory cache fronting the search index`). If absent: HALT and ask which component to test (per `_shared/grounding.md`); never invent a component to interrogate.
2. **The outcomes** — *Required.* The business outcomes in play, each with an id (`out:fast-search — users find a record in under one screen-wait`). If absent/unreadable/empty: HALT and ask where the outcomes live (per `_shared/grounding.md`); never invent an outcome.
3. **The NFRs** — *Required.* Non-functional requirements, each with an id, a measurable target, and **which outcome it derives from** (`nfr:search-latency — p95 ≤ 200ms · derives_from out:fast-search`). If absent/unreadable/empty: HALT and ask where they live (per `_shared/grounding.md`); never invent a target.
4. **The trace** — *Required.* For each component, which NFR(s) it claims to satisfy; and crucially, **what already satisfies that NFR** (the adopted pattern, an existing service, a simpler component). The predicate (Step 2) is computed over this trace, so without it the check is meaningless. If the trace is **wholly absent**: HALT and ask for it (per `_shared/grounding.md`). If the trace is present but **one edge is incomplete** (e.g. the "already satisfied by" column is missing for the component under test): emit a single clarifying `question` for that missing edge rather than inventing it — never guess that the pattern covers it.

Readable forms for any of the above: a markdown file, an xlsx/csv path, a GitHub Project owner+number, a docs folder, or a pasted block. The check is only as honest as the trace it reads — a wholly-absent required input HALTs and asks; a present-but-incomplete edge is surfaced as a `question`, never patched with a plausible-looking guess.

This skill's no-fabrication discipline is one contract: see `skills/_contract/grounding-no-absent-input` — an absent required input HALTs and asks, never an invented hypothetical; "never arm on a hunch" and "ask for the missing edge — do not assume" are instances of it.

## Grounding (quoted)

<!-- BEGIN grounding (byte-stable; do not edit a quoted copy — edit _shared/grounding.md) -->

**GROUNDING RULE — name the required inputs; an absent required input HALTs and asks, never assumes.**

A skill **names its required inputs** up front (its Inputs section marks each row Required or
Optional). Then:

- **A required input that is absent, unreadable, or empty becomes a `halt`.** The halt asks
  the user *where the input is*, offering the formats ingestion can read (an xlsx/csv path, a
  GitHub Project owner+number, a docs folder, or a pasted block). It then **stops and waits.**
  It never assumes, invents, or reasons over a hypothetical — no invented id, key, number, NFR,
  requirement, acceptance criterion, file path, or source row.
- **Partial input is named, not patched.** When some required inputs are present and others are
  not, the skill **names exactly what is missing and asks for it** — it never silently proceeds
  on the part it has, and it never back-fills the gap with a plausible-looking guess.
- **An absent *optional* input proceeds honestly.** It is surfaced as a `question` or recorded
  as an explicit null — never padded with invented content to look complete.

**"I read nothing" and "I cannot read this" are different outputs.** An unreadable or
unsupported source HALTs (it asks for a readable form); it never returns an empty result, because
a silent-empty reads downstream as "the source had nothing in it" — a silent-proceed failure.

**A halt is a question, never a verdict.** A halt names the missing input and asks where it is.
It never smuggles a finding, an assumption, or a disposition for a human to rubber-stamp — no
"I halt because this is infeasible / too risky / out of scope." Those are JUDGMENTs the human
owns. The halt carries only: *what is required, what is missing, and the formats it can be read
from.*

<!-- END grounding -->

## The method

The base is deterministic; one reasoning step phrases the result. Keep them separate — the determinism is what makes this defensible, the phrasing is what makes it usable.

### Step 0 — Locate and verify the required inputs (deterministic, pre-model)

Before walking any edge, check the required inputs as file-level facts: a named component under test, the outcomes, the NFRs, and the trace. If the **component, outcomes, NFRs, or the trace are wholly absent / unreadable / empty**, emit the clean halt below and **stop** — do not interrogate an invented component or walk an invented edge:

```
HALT — required input missing.

I can't run a necessity check without the component and the trace it walks
(component → NFR → outcome, plus what already satisfies each NFR), and I won't
invent either. Tell me where they live and I'll pick up from there.

I'm missing: <name each absent input — e.g. the trace / the outcomes>.

I can read any of these:
  • a markdown file (outcomes / NFRs / the component list with trace edges)
  • an xlsx / csv file path
  • a GitHub Project (owner + project number)
  • a docs folder (markdown / text)
  • the rows pasted directly into the chat

Which one, and where? (Once you point me at it, I'll build the trace and ask the
necessity question — nothing is assumed until then.)
```

A *present-but-incomplete* edge is different from a wholly-absent input: if the trace exists but the "already satisfied by" edge for the component under test is missing, do **not** halt and do **not** guess the pattern covers it — emit the single clarifying `question` for that one edge (Step 3 / Inputs row 4). The halt copies the canonical exemplar in `skills/_contract/grounding-no-absent-input`; it names what is missing and asks, and carries no verdict.

### Step 1 — Build the component → NFR → outcome trace (deterministic)

For the component under test, walk its edges:

```
comp:redis ──satisfies──▶ nfr:search-latency (p95 ≤ 200ms) ──derives_from──▶ out:fast-search
```

A component with **no** edge to any NFR, or an NFR with **no** edge to any outcome, is itself a finding — surface it as the question "serves which outcome?" with an empty right-hand side. Do not silently drop it.

### Step 2 — Run the over-reach predicate (deterministic — the deterministic base)

For each NFR the component claims to satisfy, classify it on facts already in the trace, never on judgment:

- **`already-met-upstream`** — the NFR's target is met by something already in the design that is *not* this component (the adopted pattern, an existing service, a simpler component already present). The component adds no coverage this NFR didn't already have.
- **`sole-provider`** — this component is the only thing in the design that meets the NFR. Cutting it would breach a real target tied to a real outcome.
- **`no-outcome`** — the NFR (or the component directly) traces to no accepted business outcome at all.

**The component ARMS the question when every NFR it claims is `already-met-upstream` or `no-outcome`** — i.e. it adds no coverage that some outcome still needs. If even one NFR is `sole-provider`, the component is load-bearing: **stay silent, emit no question.**

This predicate is the whole point. It is computed over the trace, it is reproducible, and it decides only *whether to ask* — never *what to do*.

### Step 3 — Phrase the question, naming both ids (model reasoning step)

When (and only when) the predicate arms, phrase one question. Two ids are mandatory: the **component id** and the **outcome id** whose NFRs are the subject. Show the over-reach in plain terms — what the component claims, and what already covers it — then end on the open question. Minimal. Question-only. No recommendation, no lean toward cutting.

Template:

> **`<comp:id>`** serves only **`<nfr:id>`** (`<target>`), which already traces to **`<out:id>`** and is met by **`<what already meets it>`**. Necessary, or cut?

Forbidden phrasings (these turn the flag into a verdict — never emit them): "this is gold-plated," "you should remove," "over-engineered," "unnecessary," "redundant — cut it," or any cut/keep recommendation. The skill surfaces the over-reach; it does not adjudicate it.

### Step 4 — The human rules; record the ruling, not a score

The human answers keep or cut. Record the ruling as a fact tied to both ids. **Zero cuts across an entire design is a legitimate, non-failing outcome** — there is no metric anywhere that rewards cutting, and a design where every component survives the question is a good result, not a failed check. A "keep" with a stated reason is itself valuable record: it documents *why* the component earns its place.

If a component is cut, that cut belongs in the design's open-questions / overrides record so the next reader sees what was removed and why.

## Output format

You return **one of two things per component**:

**(a) The predicate did not arm — the component is load-bearing.** Emit nothing for that component, or a single quiet line for the record:

```
comp:redis — kept (sole provider of nfr:search-latency → out:fast-search). No question.
```

**(b) The predicate armed — emit the question.** One block, two ids, the arithmetic, then the open question:

```markdown
### Necessity question — comp:redis

- **Component:** `comp:redis` — in-memory cache fronting the search index
- **Claims to serve:** `nfr:search-latency` (p95 ≤ 200ms)
- **That NFR derives from:** `out:fast-search`
- **Already met by:** `pattern:managed-search` (adopted) — guarantees p95 ≤ 120ms
- **Predicate:** all claimed NFRs `already-met-upstream` → **question armed**

> `comp:redis` serves only `nfr:search-latency` (p95 ≤ 200ms), which already traces to
> `out:fast-search` and is met by the adopted `pattern:managed-search`. Necessary, or cut?

_The human rules. Keep is a valid answer; cut is a valid answer; zero cuts across the design is legitimate._
```

Worked example — a component that survives (no question):

```
comp:postgres — kept. Sole provider of nfr:durable-record (→ out:audit-trail)
and nfr:relational-query (→ out:portfolio-view). Predicate did not arm.
```

## Notes / anti-patterns

- **Never assert "gold-plated."** The output kind is `question`, full stop. If you find yourself writing a verdict, you have left this skill's contract. Re-read Step 3.
- **Never arm on a hunch.** The predicate runs on the trace (Step 2). If the "already met by" edge isn't in the input, ask for it — do not assume the pattern covers it.
- **Silence is a valid output.** A load-bearing component (`sole-provider` on any NFR) produces no question. Resist the urge to ask anyway; a tripwire that fires on everything trains the human to ignore it.
- **Two ids or it doesn't ship.** Every question names the component id *and* the outcome id. "Is Redis necessary?" with no outcome is not this skill — it's a hunch.
- **No score, no rate, no target.** Do not count cuts, do not report a "leanness score," do not aim for a cut quota. Zero cuts is a clean pass, not a miss.
- **This is advisory.** It does not block, does not set status, does not require resolution to proceed. The design can move forward with every necessity question still open — they travel into the open-questions record as honest unknowns.
- **It only works downstream of the trace.** This skill is meaningless without `derives_from` edges (component → NFR → outcome). If the design has no trace, the correct output is a single question asking for it, not a fabricated necessity check.
- **The `out:` / `nfr:` / `comp:` refs are illustrative semantic labels, not keys.** They name the edges this check walks. When a real design is loaded, an `out:` ref resolves to a `BO-<n>` business outcome and an `nfr:` ref resolves to a `REQ-<n>` requirement (non-functional is `classify` metadata, never part of the key); the trace edge is the same `derives_from` field either way. Resolve to the canonical key when one exists; keep the lowercase ref only as a worked-example shorthand.
