---
name: necessity-check
description: When a specific technical component is proposed, ask "necessary for WHICH outcome?" — naming both ids and computing over-reach relative to a named outcome's NFRs. Raises the question; never asserts "gold-plated." The human rules; zero cuts is a legitimate outcome.
when_to_use: a specific technical component is proposed (Redis, Kafka, a queue, a cache, a second database) and you want to test that it isn't gold-plating relative to the outcomes it claims to serve
output_kinds: [question]
deterministic_fallback: the component->NFR->outcome over-reach predicate
suggested_tier: sonnet
---

# necessity-check — anti-gold-plating tripwire

> FORGE Stage 7 · Principle V: *Necessity is a flag, never a verdict.*
> A tripwire that raises the necessity **question**. It is structurally incapable of asserting "this is gold-plated." The flag is computed; the human rules.

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

1. **The component under test** — a named id and one line of what it is (`comp:redis — in-memory cache fronting the search index`).
2. **The outcomes** — the business outcomes in play, each with an id (`out:fast-search — users find a record in under one screen-wait`).
3. **The NFRs** — non-functional requirements, each with an id, a measurable target, and **which outcome it derives from** (`nfr:search-latency — p95 ≤ 200ms · derives_from out:fast-search`).
4. **The trace** — for each component, which NFR(s) it claims to satisfy; and crucially, **what already satisfies that NFR** (the adopted pattern, an existing service, a simpler component). Without the "already satisfied by" column the predicate cannot fire honestly — say so rather than guess.

If any of the four is missing, **emit a single clarifying question** for the missing edge rather than inventing it. The check is only as honest as the trace it reads.

## The method

The spine is deterministic; one reasoning step phrases the result. Keep them separate — the determinism is what makes this defensible, the phrasing is what makes it usable.

### Step 1 — Build the component → NFR → outcome trace (deterministic)

For the component under test, walk its edges:

```
comp:redis ──satisfies──▶ nfr:search-latency (p95 ≤ 200ms) ──derives_from──▶ out:fast-search
```

A component with **no** edge to any NFR, or an NFR with **no** edge to any outcome, is itself a finding — surface it as the question "serves which outcome?" with an empty right-hand side. Do not silently drop it.

### Step 2 — Run the over-reach predicate (deterministic — THE deterministic spine)

For each NFR the component claims to satisfy, classify it on facts already in the trace, never on judgment:

- **`already-met-upstream`** — the NFR's target is met by something already in the design that is *not* this component (the adopted pattern, an existing service, a simpler component already present). The component adds no coverage this NFR didn't already have.
- **`sole-provider`** — this component is the only thing in the design that meets the NFR. Cutting it would breach a real target tied to a real outcome.
- **`no-outcome`** — the NFR (or the component directly) traces to no accepted business outcome at all.

**The component ARMS the question when every NFR it claims is `already-met-upstream` or `no-outcome`** — i.e. it adds no coverage that some outcome still needs. If even one NFR is `sole-provider`, the component is load-bearing: **stay silent, emit no question.**

This predicate is the whole point. It is computed over the trace, it is reproducible, and it decides only *whether to ask* — never *what to do*.

### Step 3 — Phrase the question, naming both ids (LLM reasoning step)

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
- **This is advisory, not a gate.** It does not block, does not set status, does not require resolution to proceed. The design can move forward with every necessity question still open — they travel into the open-questions record as honest unknowns.
- **It only works downstream of the trace.** This skill is meaningless without `derives_from` edges (component → NFR → outcome). If the design has no trace, the correct output is a single question asking for it, not a fabricated necessity check.
