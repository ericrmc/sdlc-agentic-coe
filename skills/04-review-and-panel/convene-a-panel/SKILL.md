---
name: convene-a-panel
description: Cast a fixed balanced 5-lens panel, derive 4-7 grounded questions, run one stance-shaped contribution per (persona,question) in parallel, red-team the strongest objection, and synthesise into proposals; a genuine split becomes a human-owned decision. Use when battle-testing a design or a feature brief with balanced affirmative and adversarial lenses.
when_to_use: battle-testing a design or a feature brief with balanced affirmative and adversarial lenses
output_kinds: [proposal, question, menu]
deterministic_fallback: the fixed roster + the 4 fixed feature-brief questions
suggested_tier: opus
---

# Convene a panel — the balanced 5-lens battle-test

> The panel proposes; the human disposes. This skill never returns a verdict.

## Purpose

This is the flagship battle-test. You convene a balanced panel of five fixed lenses, point each lens at a real artefact (a solution design, a requirement set, or a free-text feature brief), and let the panel argue the design with itself. The panel aggregates **real findings** — gaps, tensions, orphaned value, over-reach, open risks — into **proposals a human accepts on their own terms**.

Two rules make the output trustworthy rather than theatre:

- **It never promises a verdict.** Every contribution and every proposal is advisory. The panel surfaces; the human accepts, dismisses, or records a dissent. There is no path by which the panel resolves its own findings.
- **A genuine affirmative-vs-adversarial split is not auto-resolved.** When the affirmative side wants something and the adversarial side objects on the *same* node, the skill does **not** pick a winner. It emits both positions as the two options of a single human-owned decision. The panel could not agree, so the human decides.

The value is the *balance* and the *grounding*. A one-sided panel is worthless; a panel that fabricates findings is worse. Both are made structurally impossible here (see Balance rule and Honesty rule below).

## When to use

- You have a **solution design** (sections, requirements, NFRs, chosen patterns) and want it pressure-tested before you commit to building.
- You have a **requirement set** with outcomes and derived requirements and want the gaps, tensions, and gold-plating surfaced as a balanced argument, not a one-voice critique.
- You have a **free-text feature brief** ("add SSO with SCIM provisioning") and want a fast, balanced read across completeness / risk / alternatives / necessity before you write a single requirement.

Run it at any time. It is read-only and advisory — there is no gate, no state it must be in, no approval it produces. Re-run it freely as the design changes.

## Inputs

You supply a context bundle. Two modes:

**Artefact mode** (`scope: requirements` or `scope: solution`) — you supply the project's current findings, ideally already computed by upstream skills. The lenses read these nodes directly:

| context key | what it holds | which lens reads it |
|---|---|---|
| `open_challenges` | requirement challenges with a `kind` (`conflicting` / `unquantified` / `untestable` / `vague` / `gold_plated` / `missing_nfr` / ...) | skeptic (tension), minimalist (gold_plated), pragmatic_engineer (missing_nfr) |
| `open_reconcile_proposals` | open tensions between the design and the source of truth | skeptic (evidence) |
| `children_by_parent` + `ac_by_req` | derived/technical requirements grouped by parent, and which have acceptance criteria | pragmatic_engineer (requirements with no AC) |
| `open_roadblocks` | hard constraints not yet retired or accepted | pragmatic_engineer (risk) |
| `orphaned` | requirements carrying value no current outcome holds | explorer (alternative) |
| `domains` | data/capability domains, some still `surfaced` (unexplored) | explorer (alternative) |
| `pattern_override` | where the design departed from a recommended pattern | solution_designer (alternative) |
| `sections` | design sections with `body_md` (a thin section is a new body-length heuristic) | solution_designer (gap) |
| `by_id` | id → row lookup, so a proposal can cite the node it came from | synthesis |

**Feature-brief mode** (`scope: feature`) — you supply only `feature_brief: "<free text>"`. The skill skips signal-gating and asks the four fixed questions below.

If a context key is absent or empty, that is fine — the lens that reads it will honestly say "no open signal for this lens" rather than invent one. The skill degrades gracefully from a fully-instrumented project to a bare feature brief.

## The roster (fixed, balanced, 5 lenses)

The roster is **fixed and closed** — five persona kinds, never more, never fewer. A fixed set keeps the balance rule trivial to enforce and the output legible. Three affirmative lenses build the case for the design; two adversarial lenses attack it.

| persona_kind | side | the stance — how it reads every question |
|---|---|---|
| `explorer` | **affirmative** | "What is the bigger opportunity? What value is orphaned, what domain is unexplored, what are we not yet asking?" |
| `solution_designer` | **affirmative** | "What is the cleanest shape that serves the outcome? Where did we override a pattern; where is a section thin?" |
| `pragmatic_engineer` | **affirmative** | "What ships? What has no acceptance criterion, what NFR is uncovered, what roadblock is open?" |
| `skeptic` | **adversarial** | "What is the hidden assumption? Where is the evidence? Which requirements conflict, are unquantified, untestable, or vague?" |
| `minimalist` | **adversarial** | "What can we cut and still serve the outcome? What reaches beyond the captured outcome — what is gold-plating?" |

**Seating rule:** seat a couple of affirmative and a couple of adversarial per stage. The default seats all five. On an artefact, the lenses self-select by signal: a lens with nothing to read seats but contributes the honest empty note. On a stage where you want a tighter panel, seat `solution_designer` + `pragmatic_engineer` against `skeptic` + `minimalist` for solution design, or `explorer` + `solution_designer` against `skeptic` + `minimalist` for outcomes/requirements.

The roster is the deterministic fallback. Even with no LLM, the panel casts these five real lenses with real stances over real nodes.

## The two governing rules

### Balance rule — at least one affirmative AND at least one adversarial

A seated panel must always hold `>= 1 affirmative` lens AND `>= 1 adversarial` lens (the default holds 3 + 2). This is not a hope; it is the first thing the deterministic step asserts before it runs. A one-sided panel — all affirmative, or all adversarial — is **unrepresentable**. A panel that came back all-affirmative would rubber-stamp the design; a panel that came back all-adversarial would be a hit-job. The invariant makes both impossible, which is what lets a human trust the output without re-deriving it.

### Honesty rule — a no-signal lens says so, never fabricates

When a lens reads its bound node and finds nothing — no open challenge, no orphaned requirement, no thin section — it emits exactly one contribution: *"No open signal for this lens — nothing to push back on here,"* with signal `concurs`. It does **not** invent a finding to look busy. This is what keeps an empty project from producing a wall of fabricated objections. A clean design should produce a quiet panel, and "the panel found nothing to push back on" is an honest, valuable result — not a gap to be filled.

These two rules together are the whole contract: the panel is always balanced, and it never lies. Everything else is mechanics.

## The method (numbered steps)

The method has a **deterministic spine** (steps 1, 2, 6) you can run with no model at all, and an **LLM reasoning step** (steps 3, 4, 5) that deepens the prose without changing the structure. Keep both. The spine guarantees grounding and balance; the LLM gives the argument its voice.

### Step 1 — DETERMINISTIC: cast the roster

Cast all five lenses from the fixed roster above. Assert the balance rule (`>= 1` affirmative AND `>= 1` adversarial) before proceeding. Each lens carries a **charter** — a one-line stance string tuned to this project (templated from the project name and in-scope outcomes; the LLM may sharpen it in step 3 but never rebind it).

### Step 2 — DETERMINISTIC: derive the questions, bound to real nodes

Derive a **small** ordered set of questions — target **4 to 7** (the channel-width discipline that keeps a session readable rather than a stampede).

**Artefact mode:** each question is a template *bound to a real node*. Emit a question **only when its bound node is non-empty** — no node, no question. Each question carries `{kind, scope, prompt, surfaced_from: {node, ids}}`. The bindings:

- `tension` (skeptic) — bound to `open_challenges` of kind conflicting / unquantified / untestable / vague.
- `evidence` (skeptic) — bound to `open_reconcile_proposals`.
- `necessity` (minimalist) — bound to `open_challenges` of kind `gold_plated`.
- `completeness` (pragmatic_engineer) — bound to requirements with no acceptance criteria, else to `missing_nfr` challenges.
- `risk` (pragmatic_engineer) — bound to `open_roadblocks`.
- `alternative` (explorer) — bound to `orphaned` requirements, else to `surfaced` domains.
- `alternative` (solution_designer) — bound to `pattern_override`, else to thin `sections`.

The phrasing is templated; the binding is real data. So even with no LLM the questions name the project's own outcomes, requirements, and sections.

**Feature-brief mode:** skip signal-gating entirely. Ask these **four fixed questions**, each bound to the synthetic `feature_brief` node:

1. `completeness` — "What must this feature include to be complete and verifiable — the acceptance criteria and the edge cases?"
2. `risk` — "What are the risks, failure modes, and the hardest part to get right?"
3. `alternative` — "What are the strongest alternative shapes or approaches, and which fits best?"
4. `necessity` — "What is the simplest version that delivers the value — what can be cut or deferred?"

The four fixed questions map to lenses: completeness → pragmatic_engineer; risk → skeptic; alternative → explorer + solution_designer; necessity → minimalist. This is the deterministic fallback for feature mode.

### Step 3 — LLM: run one stance-shaped contribution per (persona, question), in parallel

For each `(persona, question)` pair whose lens speaks to that question kind, produce **one** contribution `{persona_kind, question_index, stance_summary, body_md, signal}`. With ~5 lenses over ~5 questions this is roughly 20 contributions — a genuinely longer session.

**Fan out one parallel agent per pair.** Compose the `llm-fanout-orchestrator` skill: it wraps the deterministic base (which already did the binding and applied the honesty rule) and launches one independent model call per real-signal contribution, so each persona deepens its own argument in its own voice without waiting on the others. A failed call falls back to the deterministic body — the base always stands. No-signal (`concurs`) contributions are not fanned out; they stay verbatim per the honesty rule.

Each contribution carries a **signal** — a structured hint the synthesiser clusters on so it never has to parse prose:

`proposes_requirement` · `flags_gap` · `proposes_alternative` · `raises_risk` · `concurs` · `objects`

Every contribution is **grounded in cited signal** — it keeps the facts of the node it was bound to, invents nothing new, and **declares no verdict**. Use this per-panellist prompt (provider-agnostic):

```
You are ONE panellist on a design deliberation, speaking strictly from your own lens.
Deepen your contribution to the question below: sharpen the argument and your stance.
Stay grounded in the cited signal in the grounding note — keep its facts, invent
nothing, and declare no final verdict (the facilitator synthesises; the human decides).

LENS: {persona_kind} ({side} voice)
CHARTER: {charter}
QUESTION: {question}
YOUR SIGNAL: {signal}
GROUNDING (the real platform signal this binds to — preserve its facts):
{grounding}

Return ONLY a JSON object of exactly this shape, no prose, no fence:
{ "stance_summary": "one sharp sentence — your position on the question",
  "body_md": "2-4 sentences deepening the argument from your lens, grounded in the cited signal" }
```

### Step 4 — LLM: red-team the single strongest objection per emerging proposal

Before synthesising, run one adversarial **objection per emerging proposal** — exactly the contributions the synthesiser would cluster into a proposal (`flags_gap` / `proposes_requirement` / `proposes_alternative` / `raises_risk`). Alternate the two adversarial voices (skeptic, minimalist). Each objection is the **single strongest** push-back on that proposal — not a list, the one that bites hardest — bound to the source contribution's question. Fan these out in parallel too. The objection is never a verdict: it gives the human the best reason to *not* accept, so the human can keep the proposal or record a dissent with eyes open.

```
You are the {persona_kind} red-teaming an emerging {proposal_kind} from a design panel.
Give the SINGLE STRONGEST objection — the one reason a careful person would not accept
this. Stay grounded in the note. Do NOT deliver a verdict; the human decides whether to
keep the proposal or record your objection as a dissent.

GROUNDING: {grounding}

Return ONLY: { "stance_summary": "one sentence — your strongest objection",
               "body_md": "2-4 sentences making that single objection land" }
```

### Step 5 — LLM: synthesise into proposals (and turn a real split into a decision)

Cluster the contributions by their bound node and signal, then emit into **four proposal channels** — never a report:

| cluster | becomes |
|---|---|
| `flags_gap` (missing AC / missing NFR / thin section) | a **gap** challenge on its home view (`untestable` / `missing_nfr` / `vague`) |
| `proposes_requirement` (orphaned value, panel concurs) | a **proposed requirement** carrying that value, threaded to the outcome it serves |
| `proposes_alternative` (a cheaper or different shape) | a **decision menu**: {adopt the alternative} vs {keep the current direction} |
| `raises_risk` (open roadblock / unsettled tension) | a **roadblock** to retire or accept |
| `concurs` / `objects` only | **no proposal** — `objects` already lives on the challenge row the adversary read; the panel does not duplicate it |

**The split rule (point 5 of the brief made concrete):** when an affirmative `proposes_requirement` / `proposes_alternative` lands on the *same node* as an adversarial `objects`, do **not** resolve it. Emit it as a **decision** whose two options are literally the two sides' positions ("adopt — the explorer's case" vs "hold — the minimalist's objection"), with the red-team objection from step 4 attached as the trade-off note. The human owns the call the panel could not make. This is the honest move: the skill never pretends the panel agreed when it did not.

Every proposal carries `derived_from_contribution_ids` (provenance back into the transcript) and an `agent_rationale` naming any split. Accepting a proposal is therefore never a leap of faith — the human can open the contributions that produced it.

```
You are the FACILITATOR. A balanced panel has been cast and bound to real findings and
has argued each question. Rewrite the framing and synthesis into a sharp, grounded
facilitation. Add, drop, reorder, and rebind NOTHING — every persona and question is
already bound to real signal. Do NOT promise a verdict: the panel proposes, the human
disposes. Where the affirmative and adversarial sides split on the same node, present
BOTH positions as the two options of one decision — never pick a winner.
```

### Step 6 — DETERMINISTIC: assemble the output

If no LLM is available, steps 3-5 fall back to templated bodies over the same real bindings: the roster is cast (step 1), the questions are bound (step 2), the signals cluster into the same four proposal channels (step 5's table is pure signal-counting), and the four fixed feature questions are the feature-mode fallback. The output is structurally identical — only the prose is shallower. Tag every templated body honestly: *"(panel depth — LLM-needed; the binding and the proposals are real.)"*

## Output format

The user gets back one markdown document with three parts: the cast + agenda, the transcript, and the synthesis (proposals + any human-owned split). Concrete template:

```markdown
# Panel — {stage} / {scope}

{framing: 2-4 sentences. The panel aggregates real findings into proposals you accept.
The panel proposes; you dispose.}

## The cast (balanced: 3 affirmative · 2 adversarial)
- explorer (affirmative) — {charter}
- solution_designer (affirmative) — {charter}
- pragmatic_engineer (affirmative) — {charter}
- skeptic (adversarial) — {charter}
- minimalist (adversarial) — {charter}

## The agenda (4-7 questions, each bound to a real finding)
1. [tension] {prompt}  ← open_challenges #12, #14
2. [completeness] {prompt}  ← requirements with no AC: REQ-7, REQ-9
3. [risk] {prompt}  ← open_roadblocks #3
...

## Transcript
### Q1 — tension
- **skeptic** (objects): {stance_summary}
  {body_md}
- **solution_designer** (concurs): No open signal for this lens — nothing to push back on here.
### Q2 — completeness
- **pragmatic_engineer** (flags_gap): {stance_summary}
  {body_md}
...

### Red-team (strongest objection per emerging proposal)
- **minimalist** vs the proposed requirement DLB-7: {objection_md}

## Synthesis — proposals (accept or dismiss each on its home view)
The panel aggregated the real findings and proposes:
- **2 gaps** to address — REQ-7 has no way to be verified (untestable); NFR coverage gap on performance (missing_nfr).
- **1 requirement** to carry orphaned value — "expose audit log export" (orphaned REQ-22), serves outcome O-3.
- **1 decision** you own (a real split) — "Adopt the lighter pattern?":
    - *Adopt* — solution_designer: the override is no longer justified.
    - *Hold* — minimalist objected on migration cost (red-team note attached).
- **0 roadblocks**.

Each proposal is stamped with this session's provenance; accept or dispose it where that
kind of thing already lives. Nothing here is a verdict.
```

When the panel finds nothing, the synthesis is the honest empty case:

```markdown
## Synthesis
The panel found no open signal to push back on — every lens concurred. This is the honest
empty result, not a gap. Nothing to propose.
```

## Notes / anti-patterns

- **Never return a verdict.** "The panel approves this design" is a banned output. The panel surfaces proposals; the human accepts, dismisses, or records a dissent. If you find yourself writing a conclusion, convert it to a proposal or a human-owned decision.
- **Never auto-resolve a genuine split.** Affirmative-wants-X vs adversarial-objects-to-X on the same node is a decision the human owns, with both positions as options — not a call the panel makes by counting voices.
- **Never fabricate a finding to fill a lens.** A no-signal lens says so. A quiet panel over a clean design is a real result. Inventing objections to look thorough destroys the trust the balance rule buys you.
- **Never seat a one-sided panel.** Always `>= 1` affirmative AND `>= 1` adversarial. If you ever have only one side, you have a critique or a cheer, not a panel.
- **Keep the agenda small (4-7).** More than seven questions and the session becomes a stampede no human will read. Bind to the nodes that actually matter; drop the rest.
- **Bind before you argue.** Every question and contribution cites the real node it came from. An ungrounded contribution ("I worry this might not scale") with no `surfaced_from` node is noise — make it cite the roadblock or NFR it actually reads, or drop it.
- **The deterministic spine is not a hollow placeholder.** Even with no LLM, the bindings and the four proposal channels are fully real — the human accepts genuine, provenance-stamped proposals. Only the depth of the argument waits on the model, and that gap is labelled, never hidden.
- **Provenance is mandatory.** Every proposal carries `derived_from_contribution_ids`. Accepting a proposal must always be openable back to the contributions that produced it; a proposal with no trail is not acceptable output.
