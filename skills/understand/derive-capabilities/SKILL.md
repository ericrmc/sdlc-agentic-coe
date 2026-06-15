---
name: derive-capabilities
description: Annotate each grounded requirement with the capability it fulfils — MATCHED (a fulfils_capability CAP- tag resolving to a real capabilities/INDEX.md row, traced to the REQ-/BO- keys that imply it) and PROPOSED-NEW (candidate needs the INDEX does not yet name, each cited to its requirement keys and routed to library/author-capability). Never invents a capability not grounded in a requirement; a single-requirement need is proposed-but-flagged, not withheld. Advisory.
one_liner: Tag each requirement with the capability it fulfils; route genuinely new needs to author-capability.
aliases: [derive capabilities, requirement to capability, fulfils_capability tag, match capabilities, what need does this serve, capability gap, propose a capability from requirements, capability coverage]
when_to_use: after requirements are grounded (hardened/classified) and before pattern recommendation — to emit the fulfils_capability edge recommend-component-patterns assumes, and to surface needs the capability index does not yet name.
output_kinds: [proposal, menu, halt]
deterministic_fallback: Read capabilities/INDEX.md directly; alias-match each requirement's need phrasing to a real CAP- row for MATCHED; collect the requirements that match nothing into the PROPOSED-NEW menu, one row per distinct unmatched need, each citing its req_keys.
suggested_tier: mid
tier_reason: A bounded retrieve-against-the-closed-INDEX pass like classify-requirements; the high-stakes synthesis of a NEW capability file is delegated to library/author-capability (frontier), not done here.
neighbours: |
  before: understand/classify-requirements (annotates the requirements this then matches to capabilities)
  after: architect/recommend-component-patterns (a MATCHED CAP- resolves straight to its pattern; a PROPOSED-NEW or OPEN capability is the honest-empty signal arriving one stage earlier)
---

# derive-capabilities — tag each requirement with the capability it fulfils

Annotate each grounded requirement with the **capability** it serves, exactly the way its
sibling `classify-requirements` annotates each requirement's *shape*. The output is a
per-requirement `fulfils_capability: CAP-…` tag plus a menu of needs the library does not
yet name. This skill closes the one open edge in the chain: `recommend-component-patterns`
resolves a need to a capability and then to a pattern, but **no skill emits the
`fulfils_capability` tag onto a requirement** — this is where that edge is born.

This skill is **advisory and non-destructive**. It describes; it never decides. It does
**not** write a capability file, flip a `confidence`, or advance an `approval_status`. It
attaches a tag alongside the requirement (MATCHED) or routes a stub to the
CODEOWNERS-ratified contribution flow (PROPOSED-NEW). A human reads and ratifies.

> Retrieval, not generation. The legal `CAP-` key set is the rows of
> `capabilities/INDEX.md`, **fixed before reasoning** — the exact mirror of
> `recommend-component-patterns` STEP 0/1. A MATCHED tag must resolve to a real INDEX
> row; a PROPOSED-NEW need must cite the `req_key`(s) that imply it. A capability with no
> requirement behind it has nowhere to live here.

## Purpose

Two outputs, from one pass over a grounded requirement set:

1. **MATCHED** — for each requirement whose need resolves to a capability **already in
   `capabilities/INDEX.md`**, a `fulfils_capability: CAP-…` tag, traced to the `REQ-`/`BO-`
   key(s) that imply it. This is the LOW/derived edge that rides the requirement PR; it
   feeds `recommend-component-patterns` STEP 0, which today *assumes the tag already exists*.
2. **PROPOSED-NEW** — an **un-ranked `menu`** of candidate needs the INDEX does **not** yet
   name, each **citing the `req_key`(s)** that imply it and pre-filling
   `.github/ISSUE_TEMPLATE/new-capability.yml`, routed to `library/author-capability` (a
   HIGH-commitment, human-ratified act). A candidate need cited by exactly **one**
   requirement is **proposed-but-flagged** ("single — confirm it recurs"), never withheld.

The value: a requirement that names its capability can be resolved to a proven pattern in
one hop; a need the library does not name is surfaced *here*, one stage before
`recommend-component-patterns` would hit honest-empty, so the gap is named while the
requirement context is still in hand.

## When to use

After requirements are **grounded** (hardened / classified) and before pattern
recommendation. Run it whenever the requirement set changes and you want the
requirement→capability edge populated. It is idempotent over an unchanged set: the same
requirement text against the same INDEX resolves the same way every time.

Do **not** use this to author a capability file — that is `library/author-capability`'s job
(it writes at `candidate`; a CODEOWNER ratifies). This skill only **routes a stub** to it.
Do **not** use it to recommend a pattern — that is `architect/recommend-component-patterns`,
the after-neighbour this feeds.

## Inputs

The user supplies, as markdown or plain context. Each row is marked **Required** or
**Optional**; a Required input that is absent/unreadable/empty HALTs (see
[Grounding (quoted)](#grounding-quoted) and STEP 0).

- **Grounded requirements list** — *Required.* The hardened requirement set, each row
  carrying its stable key (`REQ-<n>`, or a `BO-` outcome key, or a bare integer index that
  maps to one) and the requirement text; ideally the `classify-requirements` annotations
  too. Reference each row by its real key; do not renumber, merge, skip, or duplicate.
  **If absent/unreadable/empty: HALT and ask where the requirement set is** (per
  `_shared/grounding.md`); never invent a requirement, a key, or a need. Readable forms: a
  markdown file, an xlsx/csv path, a GitHub Project owner+number, a docs folder, or rows
  pasted into the chat.
- **The capability index** — *Required.* `capabilities/INDEX.md`, the alias→capability
  lookup. This is the **set of legal `CAP-` keys**, fixed before reasoning. **If
  absent/unreadable: HALT and ask where the index lives** (per `_shared/grounding.md`);
  never invent a `CAP-` key to stand in for it. An **empty-but-readable** INDEX (zero
  capability rows) is **not** a halt — it is the honest case where **every** requirement's
  need routes to PROPOSED-NEW (there is nothing to MATCH against), per STEP 2/3.
- **Project context** — *Optional.* A short paragraph of what the project is and what it's
  for. It grounds the need-vs-mechanism read when a requirement's underlying need is
  implicit. If absent: proceed and surface the gap as a `question`; never pad it with an
  invented context.

This skill **names its required inputs and grounds every tag in supplied text**; it follows
the no-fabrication contract `skills/_contract/grounding-no-absent-input`. The "never invent
a `CAP-` key" rule throughout (it appears in the description, STEP 1, STEP 2, and the
anti-patterns) is one **instance** of that contract — the exact mirror of
`recommend-component-patterns`' "never invent a `pattern_key`" — not a separate rule.

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

## Trace edge (quoted)

The MATCHED tag and the requirement's existing `derives_from` edge **coexist**: the
requirement keeps `derives_from` to its outcome AND gains `fulfils_capability` to its
capability (the INDEX "chain" documents this as edge 1). The tag is a citation, never a
verdict — it records *which need this requirement serves*, not that the requirement is
necessary, sufficient, or done.

<!-- BEGIN trace-edge (byte-stable; do not edit a quoted copy — edit _shared/trace-edge.md) -->

**TRACE EDGE — `derives_from` is a portable `req_key` citation, not a foreign key.**

Every derived artefact carries a `derives_from:` line naming the **stable `req_key`** of
the upstream node it serves. The edge is plain text — a key, optionally a markdown link
to the file/anchor that defines that key. It needs no database, no id, no schema:

```
derives_from: BO-1
```

or, when the upstream node lives in another file:

```
derives_from: [BO-1](../outcomes/OUTCOMES.md#bo-1)
```

`req_key`s are short, human-readable, and **stable for the life of the project** — they
are the citation target, so renaming or renumbering one silently breaks every edge that
cites it. Conventional prefixes (advisory, not enforced):

- `CAP-<SLUG>` business **C**apability
- `BO-*` business **O**utcome
- `REQ-*` derived **R**equirement (functional or non-functional; F/NF is classify metadata, not part of the key)
- `PAT-<SLUG>` adopted **P**attern
- `DEC-*` **D**ecision / contested call / dissent

The edges compose into one directed **outcome-impact graph**:

```
capability    ->  outcome  ->  requirement  ->  pattern        ->  decision
CAP-<SLUG>        BO-*          REQ-*            PAT-<SLUG>          DEC-*
```

The graph is walkable in **both** directions, and both walks matter:

- **Downward = decomposition.** From a capability or outcome, follow `derives_from`
  *backwards* (find every artefact that cites this key) to see everything synthesised
  beneath it — the technical reqs, the NFRs, the pattern, the calls. This is how
  "accept HIGH, derive LOW" stays legible: the low artefacts are auto-applied, but each
  one names the high thing it serves.
- **Upward = impact.** From any node, follow its own `derives_from:` *forwards* to the
  outcome and capability it ultimately serves. This is how a failing or compromised node
  answers "what business outcome takes the hit, and which capability?" — the necessity
  check and the compromise/impact view both ride this walk.

**A rejected upstream node orphans its entire subtree.** If a human rejects outcome `BO-1`,
every artefact whose `derives_from:` chain leads to `BO-1` is now an **orphan** — it points
at nothing accepted. Orphans are not deleted and not errors; they are **surfaced, not
swept** (an orphan leads the open-questions handoff). This visible orphaning is what makes
auto-derivation safe: nothing technical can quietly survive the rejection of the business
reason it existed for.

**The edge is a citation, never a verdict.** `derives_from` records *what serves what*. It
never asserts that a requirement is necessary, sufficient, good, or done — those are human
calls. A node with a valid edge can still be cut; a node can be kept with its edge orphaned
and flagged. The edge informs the judgment; it never is the judgment.

<!-- END trace-edge -->

## The method — STEPS

The model reasoning step **is** the method. The deterministic alias-match (STEP 1 / the
fallback) is an optional backstop and a sanity check — not the primary matcher. Run the
steps in order.

### STEP 0 (DETERMINISTIC) — Locate / verify the required inputs (pre-model; the halt path)

Before any reasoning, confirm the two Required inputs are present as a file-level fact: the
**grounded requirements list** (something to derive capabilities *from*) and the
**capability index** (`capabilities/INDEX.md`, the set of legal `CAP-` keys). This is
mechanical — absent / unreadable / empty — never a model judgement on "is this enough to
work with."

- **Requirements list absent/unreadable/empty** → emit the clean HALT below and **stop**.
  Do not derive capabilities for a hypothetical set, and do not return an empty result (a
  silent-empty reads downstream as "there were no requirements" — a silent-proceed failure).
- **`capabilities/INDEX.md` absent/unreadable** → HALT and ask where the index lives; never
  invent a `CAP-` key.
- **INDEX present but empty** (zero capability rows) → this is **not** a halt. It is the
  honest case: there is nothing to MATCH against, so every requirement's need routes to
  PROPOSED-NEW (STEP 3). Proceed.

```
HALT — required input missing.

I can't derive capabilities without the grounded requirement set to derive them from, and I
won't invent a requirement or a need to stand in for it. Tell me where the requirements live
and I'll tag each one with the capability it fulfils — nothing is assumed until then.

I can read any of: a markdown file · an xlsx/csv path · a GitHub Project (owner + number) ·
a docs folder · the rows pasted directly here. Which one, and where?
```

If the requirements are present but `capabilities/INDEX.md` is absent/unreadable, halt the
same way for the index instead — name exactly which input is missing (per the partial-input
rule above), never silently proceed on the half you have. This halt is a `question`, never a
verdict: it names the missing input and the readable formats, and stops — it carries no
finding, no "this set looks thin," no assumption. With both Required inputs present, proceed.

### STEP 1 (DETERMINISTIC) — Load and fix the legal `CAP-` key set

Read `capabilities/INDEX.md`. Build the **closed set of legal `CAP-` keys** from its rows:
each row carries an alias phrase, a canonical `CAP-` key, a name, and a fulfilment state
(`proven — PAT-…` or `OPEN — N candidates, spikes owed`). This is mechanical: no judgement,
no filtering. Every `CAP-` key that can later be returned as a MATCHED tag **must** be one of
these keys — the set is fixed *before* the model reasons, exactly as
`recommend-component-patterns` STEP 1 fixes the legal `pattern_key` set. Carry the
fulfilment state alongside each key so STEP 4 can route a MATCHED-but-OPEN capability
honestly.

### STEP 2 (LLM) — Resolve each requirement's need to a capability

For each requirement, read past the mechanism to the **underlying need** (a requirement that
says "use Power Automate to route approvals" needs *workflow orchestration / auditable
approval routing*, not "Power Automate"). Then attempt to resolve that need against the
alias column of the fixed `CAP-` set from STEP 1.

> Match a requirement's underlying need to a capability **already in the index**. Resolve to
> a `CAP-` key **only** when the requirement's need genuinely *is* that capability's need —
> a lay-synonym alias hit grounded in the requirement text, not a loose theme. Do **NOT**
> invent a `CAP-` key: every key returned MUST be one of the keys listed in the INDEX set.
> When the need does not resolve to any indexed capability, it is a PROPOSED-NEW candidate
> (STEP 3), not a forced weak match.

Three outcomes per requirement:

- **MATCHED** — the need resolves to a real INDEX `CAP-` key. Record the tag and the
  `req_key`(s) that imply it (STEP 4).
- **UNMATCHED** — the need is real but the INDEX does not name it. Collect it for STEP 3.
- **AMBIGUOUS** — the requirement could plausibly serve more than one capability, or its
  need is too thin to resolve confidently. **An ambiguous requirement becomes a `menu` row**
  (a question for the human: "REQ-9 could be CAP-A or CAP-B — which, or neither?"), never a
  forced pick and never a third output kind. Surface it; the human resolves it.

A requirement may fulfil **more than one** capability (a tag list is legal). A requirement
may fulfil **none** that is named yet (it becomes a PROPOSED-NEW driver). Never pad a
requirement with a capability it does not genuinely serve to make the table look complete —
an honest `null`/PROPOSED-NEW is the useful signal.

> **Multi-agent option (advisory).** This step deepens with independent parallel agents:
> launch one sub-agent per requirement cluster, at most 4 at a time, each a separate
> sub-agent resolving its cluster against the same fixed INDEX set. A failed sub-agent
> returns nothing and is never fatal — the deterministic alias-match base stands; merge what
> succeeded. (Claude Code: use the Task tool / subagents. Other tools: parallel model calls,
> or a matrix-strategy CI job.) Never required — it adds coverage and cuts single-pass bias.
> See `skills/_contract/parallel-agents`.

### STEP 3 (LLM) — Assemble the PROPOSED-NEW menu (cited by construction)

Collect the UNMATCHED needs. **Group requirements that imply the same need into one
candidate** (two requirements both needing "a message queue between services" are one
candidate need cited by both `req_key`s, not two). For each distinct candidate need, build a
menu row carrying:

- a **plain, technology-free need statement** ("a system needs to … so that …"), drafted
  from the requirements — never a vendor or product name (those belong to candidate
  components inside `author-capability`);
- the **`req_key`(s)** that imply it — **by construction**: a need with no requirement
  behind it has nowhere to live in this menu, so a parentless capability cannot appear here;
- a **recurrence flag**: a need cited by exactly **one** requirement is flagged
  **"single — confirm it recurs"** and still listed (proposed-but-flagged, **not** withheld
  — a single citation is a weaker but real signal a human should weigh); a need cited by
  **two or more** requirements is flagged "recurs (N reqs)";
- a **proposed `CAP-` key** as a *suggestion only* — clearly marked "(proposed — not yet a
  real key)", so it is never mistaken for an INDEX row. It becomes real only if
  `author-capability` writes the file and a CODEOWNER ratifies it.

The menu is **un-ranked and equal**: every candidate need is presented as a peer for the
human to send onward, hold, or drop; none is starred, ordered best-first, or pre-disposed.
"Author none of these" is always an available choice.

### STEP 4 (LLM) — Write the two outputs

**MATCHED → a `proposal`** that rides the requirement PR (LOW/derived). Each tagged
requirement gains a `fulfils_capability: CAP-…` line citing the real INDEX key, alongside
its existing `derives_from`. For a MATCHED capability whose INDEX state is **OPEN** (no
proven pattern, spikes owed), carry that state onto the tag so the after-neighbour
(`recommend-component-patterns`) goes straight to honest-empty rather than hunting a pattern
that does not exist yet.

**PROPOSED-NEW → the `menu`** from STEP 3, each row pre-filling
`.github/ISSUE_TEMPLATE/new-capability.yml` and routed to **`library/author-capability`**.
This skill **never writes the capability file and never sets `confidence`/`approval_status`**
— it hands a stub; `author-capability` writes at `candidate`; a CODEOWNERS human ratifies.

### STEP 5 — Compose forward

- A **MATCHED** `CAP-` resolves straight to its pattern in `recommend-component-patterns`
  STEP 0 (the tag this skill emits is the input that STEP assumes already exists).
- A **MATCHED-but-OPEN** capability arrives pre-flagged so `recommend-component-patterns`
  goes straight to its honest-empty route.
- A **PROPOSED-NEW** (unauthored) capability is the honest-empty signal arriving one stage
  earlier — the need is named here, while the requirement context is in hand, before the
  pattern step would hit an empty library.

## Output format

Return the MATCHED tags (a machine-readable block + a human digest) and the PROPOSED-NEW
menu. Use only real INDEX keys for MATCHED; mark every proposed key as proposed.

### MATCHED — machine-readable block

```json
{
  "matched": [
    {
      "requirement_id": 7,
      "req_key": "REQ-7",
      "fulfils_capability": ["CAP-OLTP"],
      "index_state": "proven — PAT-WEBAPP-PG",
      "via_alias": "application database"
    },
    {
      "requirement_id": 14,
      "req_key": "REQ-14",
      "fulfils_capability": ["CAP-AGENT-RUNTIME"],
      "index_state": "OPEN — 3 candidates, spikes owed",
      "via_alias": "run our agents in prod"
    }
  ]
}
```

### MATCHED — human digest

```
| key     | fulfils_capability | index state                      | via alias                |
|---------|--------------------|----------------------------------|--------------------------|
| REQ-7   | CAP-OLTP           | proven — PAT-WEBAPP-PG           | "application database"   |
| REQ-14  | CAP-AGENT-RUNTIME  | OPEN — 3 candidates, spikes owed | "run our agents in prod" |
| REQ-9   | — (ambiguous)      | see menu row below              | —                        |

Notes for the human:
- REQ-14 resolves to an OPEN capability — recommend-component-patterns will honestly
  recommend none until a fulfilling pattern is proven (a question, not a verdict).
- REQ-9 is ambiguous (CAP-OLTP vs CAP-OLAP) — surfaced as a menu row to resolve.
```

### PROPOSED-NEW — the menu (un-ranked; route each to author-capability)

```markdown
## Capabilities the index does not yet name — choose what to author

Each row is a candidate **need** drafted from the requirements, cited to the requirement
key(s) that imply it. Routing one opens `library/author-capability` (writes a `candidate`;
a CODEOWNER ratifies). Author none if none recurs enough to deserve a stable name.

### A. Workflow orchestration / auditable approval routing  _(proposed key: CAP-WORKFLOW — not yet a real key)_
- **Need:** a system needs to route and track approval requests with an auditable record, so
  that approvals are consistent and reviewable.
- **Cited by:** REQ-7, REQ-22 — **recurs (2 reqs)**.
- **Route →** `library/author-capability` (pre-fills new-capability.yml).

### B. Real-time event stream between services  _(proposed key: CAP-EVENT-STREAM — not yet a real key)_
- **Need:** a system needs to publish and consume events between services with at-least-once
  delivery, so that components stay decoupled and resilient.
- **Cited by:** REQ-31 — **single — confirm it recurs.**
- **Route →** `library/author-capability`.

### Ambiguous (resolve before tagging)
- **REQ-9** could fulfil `CAP-OLTP` or `CAP-OLAP` — which, or neither? (a question, not a pick.)

### Author none
- Hold the whole menu: the index stays as is, no capability is proposed.
```

## Idempotency

The same requirement text against the same `capabilities/INDEX.md` resolves the same way
every time. The MATCHED tag is a function of (requirement text + project context + the fixed
INDEX set); the PROPOSED-NEW grouping is a function of the unmatched needs. There is no stored
state, no run-order dependence, no dependence on other requirements beyond the same-need
grouping. Re-running over an unchanged set against an unchanged INDEX yields identical tags
and an identical menu — safe to run on every change. A new INDEX row may turn a former
PROPOSED-NEW need into a MATCHED tag on the next run; that is the index doing its job, not a
non-deterministic result.

## Notes / anti-patterns

- **Never invent a `CAP-` key.** Every MATCHED key must be a row of `capabilities/INDEX.md`.
  The deterministic STEP 1 exists precisely so the legal key set is fixed before reasoning.
  Wanting to tag a need that isn't in the index is the PROPOSED-NEW signal (STEP 3), not
  licence to mint a key. This is the no-fabrication keystone applied to capability keys — the
  exact mirror of `recommend-component-patterns`' pattern-key rule; see
  `skills/_contract/grounding-no-absent-input`.
- **Every PROPOSED-NEW need cites its requirement(s).** A capability with no `req_key` behind
  it cannot appear in the menu — citation is by construction, not a model promise. This is
  what makes "never invent a capability not grounded in a requirement" structural.
- **A single citation is proposed-but-flagged, never withheld.** A need cited by one
  requirement is a weaker but real signal; list it flagged "single — confirm it recurs" and
  let the human weigh it. Silently dropping it would hide a real gap.
- **Ambiguity is a menu row, not a guess and not a third kind.** When a requirement could
  serve more than one capability, ask which (a `menu` row / `question`); never force the
  nicest pick, and never invent a new output kind for it.
- **This skill never writes the capability or flips confidence.** It tags (MATCHED) or routes
  a stub (PROPOSED-NEW). `library/author-capability` writes at `candidate`; a CODEOWNER
  ratifies. Advancing `approval_status` or setting `confidence: proven` is a human act.
- **Both edges coexist.** The requirement keeps `derives_from` to its outcome AND gains
  `fulfils_capability` to its capability — they answer different questions (what it derives
  from vs what need it serves). Do not collapse one into the other.
- **The tag is a citation, never a verdict.** `fulfils_capability` records which need a
  requirement serves; it never asserts the requirement is necessary, sufficient, or done.
  Those are human calls.
- **MATCHED-but-OPEN propagates honestly.** Carry an OPEN capability's state onto the tag so
  the after-neighbour reaches its honest-empty route instead of hunting a pattern that does
  not exist yet.
- **The model step is the method.** The alias-match backstop is a sanity check, not the
  source of truth; where the two disagree, prefer the model and note the divergence — usually
  an edge case worth a human glance.

---

### Companion reference

Ship and read `references/capability-matching.md` alongside this skill: the deterministic
alias-match backstop, the same-need grouping rule, and the worked MATCHED-vs-PROPOSED-NEW
split — so a MATCHED tag is always cited to a real INDEX row and a PROPOSED-NEW need is
always cited to its requirement keys.
