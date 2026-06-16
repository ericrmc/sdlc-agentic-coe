# Contributing

This repository holds three things: **skills** (portable agent instructions),
**patterns** (PR-reviewed, evidence-backed component building blocks), and
**capabilities** (the plain-language need that resolves to a pattern). Every
instruction here is read by an agent; an agent authors the file and fills the PR,
and a human reviews and ratifies. New here? See [GETTING-STARTED.md](GETTING-STARTED.md),
then [skills/MAP.md](skills/MAP.md) and [capabilities/INDEX.md](capabilities/INDEX.md).

> **Before a structural change** — a new top-level folder, a schema field, the key
> scheme, or weakening a gate, the grounding contract, or any invariant — read
> [RATIONALE.md](RATIONALE.md) §6 guard table first; it maps a tempting change to the
> invariant it touches and what breaks. Per-decision records are immutable [ADR.md](ADR.md)
> entries: a new decision adds the next ADR-NNNN, a reversal supersedes it — you never edit
> or delete an accepted record. Routine schema-field and convention rules live in the schema
> descriptions and this guide, where the linter is their guard.

The invariants that hold everywhere (propose→ratify, agent-authors-never-blesses, the one
CODEOWNERS structural gate, advisory CI, code-computes-not-models) are stated once in
[DESIGN.md §2](DESIGN.md#2-core-invariants). This guide is the *how-to*.

## Add a skill

A skill is one self-contained `SKILL.md` (YAML frontmatter + markdown body) that runs
in any markdown-reading agent, no tool or provider assumed.

1. An agent picks the category by intent — `understand`, `challenge`, `architect`,
   `panel`, `deliver`, `library` — and writes `skills/<category>/<skill-name>/SKILL.md`.
   Frontmatter carries `name` (kebab-case, matches the directory), `description` (one
   line saying WHEN to reach for it), `output_kinds` (a subset of the closed set
   `{proposal, question, menu, halt}`), `deterministic_fallback` (the no-model base),
   and a `suggested_tier` (`frontier` | `mid` | `light`, never a model id). The body
   runs Purpose → When to use → Inputs → numbered Steps → Output format → Notes, with a
   deterministic base first and the model step marked plainly.
2. An agent opens a PR with the skill template (`?template=skill.md`), runs the target-
   rule, shared-stub-drift, and security (`python3 security/skillspector/scan.py
   skills/<category>/<skill>`) checks, and pastes the results. A CODE maintainer reviews
   and ratifies by merging.

Write skills **tight**: a skill is loaded whole every run, so state each rule once at its
point of enforcement and cite it elsewhere — never re-narrate the frontmatter or a quoted
stub (see [ADR.md](ADR.md) ADR-0016; the advisory density check flags an over-long body).

## Add a pattern

A pattern is a building block the firm has **actually built**, carrying its governed
NFRs, constraints, and evidence. See [`patterns/_TEMPLATE.md`](patterns/_TEMPLATE.md),
the schema at [`patterns/_schema/pattern.frontmatter.schema.json`](patterns/_schema/pattern.frontmatter.schema.json),
and [patterns/README.md](patterns/README.md) for the full field set.

1. An agent writes `patterns/<category>/<slug>.md` with `approval_status: candidate`.
   The filename is human-readable lower-kebab; the cite-able `pattern_key` is
   UPPER-KEBAB (`^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$`) and need not equal it. The required floor
   is the schema's `required[]` (see [`patterns/_schema/pattern.frontmatter.schema.json`](patterns/_schema/pattern.frontmatter.schema.json)
   and [patterns/README.md](patterns/README.md) §Anatomy).
2. An agent runs the linter — `python3 skills/_scripts/lint_pattern_frontmatter.py
   patterns/<category>/<slug>.md` — then opens a PR with the pattern template
   (`?template=pattern.md`), populating every field from the file it authored.
3. A CODEOWNER architect reviews, confirms the evidence is real, and — in a commit they
   own — raises `approval_status` to `provisional`/`approved` and fills `approved_by`,
   `approved_at`, and `evidence` (`[{title, url}]`, required from `provisional` up). The
   agent stops at `candidate`.

A zero-evidence pattern can only be `candidate`. Never delete a pattern that has
adoptions — supersede it (`approval_status: deprecated` + `superseded_by`, the old and
new keys pointing at each other) so a downstream project's provenance survives.
`maturity` and `adoption_count` are computed, never written.

## Add a capability

A capability is the technology-free **need** between a requirement and a pattern: a
requirement adds `fulfils_capability: CAP-…`, and the capability names the pattern(s)
that fulfil it. See [capabilities/INDEX.md](capabilities/INDEX.md) and
`skills/library/author-capability`.

1. An agent writes `capabilities/<domain>/<slug>.md` against the schema's required floor
   (see [`capabilities/_schema/capability.frontmatter.schema.json`](capabilities/_schema/capability.frontmatter.schema.json)
   and [capabilities/README.md](capabilities/README.md)) and adds its alias rows to
   `capabilities/INDEX.md`.
2. An agent opens a PR (the new-capability issue can seed it). A CODEOWNER architect
   reviews (`capabilities/**` is gated like patterns) and ratifies by merging.

A fulfilment is `proven` (names a `pattern_key` + build evidence) or `candidate` (may
name a vendor in `note` with the `open_questions` a spike must answer). An agent writes
`confidence: candidate`; flipping it to `proven` is a human PR that attaches spike
evidence.

## Adoption

Each time a downstream project adopts a pattern, an agent appends one line to
`adoptions/ledger.jsonl` (`pattern_key`, `repo`, `disposition` ∈ {adopted-clean,
adopted-with-overrides, overridden-out}, `at`; `override_reason` required for anything
but `adopted-clean`). This append-only ledger is the "used in N engagements" number and
the input to computed maturity. Lines are never deleted; `overridden-out` is kept on
purpose — recorded dissent is signal. See [adoptions/README.md](adoptions/README.md).
