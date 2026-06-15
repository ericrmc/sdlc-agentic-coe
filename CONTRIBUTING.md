# Contributing

This repository holds three things: **skills** (portable agent instructions),
**patterns** (PR-reviewed, evidence-backed component building blocks), and
**capabilities** (the plain-language need that resolves to a pattern). Every
instruction here is read by an agent; an agent authors the file and fills the PR,
and a human reviews and ratifies. New here? See [GETTING-STARTED.md](GETTING-STARTED.md),
then [skills/MAP.md](skills/MAP.md) and [capabilities/INDEX.md](capabilities/INDEX.md).

## The rules that hold everywhere

- **Propose, then ratify.** An agent opens a PR adding or editing markdown; a human
  merges it. The merge is the ratification — git history is the record. No separate
  approval artefact.
- **An agent authors, never blesses.** An agent may write any file end-to-end, but
  every output is a proposal a human takes, edits, or drops. An agent never sets a
  `status`, `verdict`, `score`, `ranking`, `approval_status` beyond `candidate`,
  `approved_by`, `approved_at`, `maturity`, or `adoption_count`.
- **One structural human gate.** `CODEOWNERS` routes `patterns/**` and
  `capabilities/**` to the architect team; branch protection requires that review
  before merge. Everything else is advisory.
- **CI is advisory.** Validation Actions annotate the PR. A red check is a strong
  signal, not a lock; a human may merge over it with a reason.
- **Code computes, models do not.** Maturity, adoption counts, and validity dates are
  computed from `adoptions/ledger.jsonl` and history — never authored.

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
   rule and shared-stub-drift checks, and pastes the results. A CODE maintainer reviews
   and ratifies by merging.

Every step a skill instructs produces exactly one of four kinds — `proposal`,
`question`, `menu`, `halt`. There is no kind for a status, verdict, score, maturity
grade, or judgement of a person: those are human-owned or computed in an Action.

## Add a pattern

A pattern is a building block the firm has **actually built**, carrying its governed
NFRs, constraints, and evidence. See [`patterns/_TEMPLATE.md`](patterns/_TEMPLATE.md),
the schema at [`patterns/_schema/pattern.frontmatter.schema.json`](patterns/_schema/pattern.frontmatter.schema.json),
and [patterns/README.md](patterns/README.md) for the full field set.

1. An agent writes `patterns/<category>/<slug>.md` with `approval_status: candidate`.
   The filename is human-readable lower-kebab; the cite-able `pattern_key` is
   UPPER-KEBAB (`^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$`) and need not equal it. Required floor:
   `pattern_key`, `name`, `category` ∈ {deployment, integration, data}, `intent`,
   `deployment_topology`, `data_placement`, `summary`, `valid_from`, and at least one
   `attached_nfrs` entry (each `{kind, statement, acceptance_criterion}`; `kind` from
   the closed 11 in [`patterns/_schema/nfr-kinds.enum.txt`](patterns/_schema/nfr-kinds.enum.txt)).
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

1. An agent writes `capabilities/<domain>/<slug>.md` (`capability_key` `^CAP-`, `name`,
   `capability_domain` ∈ {data, compute, integration, runtime, experience, governance},
   a technology-free `need_statement`, ≥2 `aliases`, `fulfilled_by` entries, a
   `governance_nfrs` floor reusing the closed 11 NFR kinds) and adds its alias rows to
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
