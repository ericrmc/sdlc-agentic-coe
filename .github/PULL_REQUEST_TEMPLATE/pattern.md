<!--
  PATTERN PULL REQUEST — filled by the authoring agent, ratified by a human.
  Select with ?template=pattern.md (append &expand=1 to the compare URL).
  Use for any PR that adds, edits, supersedes, or deprecates a patterns/**/*.md file.
  For a skill use ?template=skill.md; for anything else use the default template.

  AGENT: you authored the pattern; now populate every field below FROM THE FILE YOU
  WROTE. Do not invent values — copy them from the frontmatter and body. Leave a field
  blank only when the schema leaves it optional and it genuinely does not apply. The
  human reviewing this PR is the CODEOWNER architect; they ratify by merging. Merging
  IS the ratification — there is no separate approval step.
-->

## What this PR does

- Pattern file(s): `patterns/<category>/<slug>.md`
- `pattern_key`: `PAT-...`
- Change: <!-- new candidate | promote (candidate→provisional/approved) | edit | supersede | deprecate -->

## Frontmatter, copied from the file

> Populate each value from the pattern you authored. These mirror
> `patterns/_schema/pattern.frontmatter.schema.json`; the `validate-patterns` Action
> checks shape and leaves an advisory comment. It does not bless the pattern — the
> CODEOWNER does, by merging.

| Field | Value (paste from the file) |
|---|---|
| `pattern_key` | `PAT-...` |
| `category` | `deployment` \| `integration` \| `data` |
| `intent` | `use WHEN ... so that ...` |
| `deployment_topology` | |
| `data_placement` | |
| `approval_status` | `candidate` \| `provisional` \| `approved` \| `deprecated` |
| `valid_from` | `YYYY-MM-DD` |
| `validity_check_months` | (re-review cadence; default 12) |
| `sunset_at` | `YYYY-MM-DD` if a known end-of-life, else leave blank |
| `supersedes` / `superseded_by` | `PAT-...` if this replaces / is replaced, else blank |
| `fulfils` | `CAP-...` the capability this serves (see below) |

> `approval_status: candidate` is the only status an agent writes. Leave `approved_by`,
> `approved_at`, and `evidence` for the human at promotion — do not set them yourself.
> Never write `maturity` or `adoption_count`: those are computed from
> `adoptions/ledger.jsonl`, never authored.

## Attached governance NFRs (measurable)

> Paste one row per `attached_nfrs` entry. Each `kind` is one of the closed 11; each
> carries a statement and a TESTABLE acceptance criterion (on adoption this becomes a
> real derived requirement downstream, so "is secure" is not acceptable). At least one.

<!-- closed kinds: security · availability · performance · data-residency · observability ·
     resilience · cost · compliance · scalability · data-governance · operations -->

| `kind` | statement | acceptance_criterion (measurable) |
|---|---|---|
| | | |

## Constraints (what adopting this gives up)

> Paste each `constraints` entry: the thing the pattern forces, and `hard` (cannot be
> waived) or `soft` (a waiver is a recorded compromise). A pattern that lists no
> tradeoffs is under-described — state the load-bearing one.

| statement | `enforced` |
|---|---|
| | `hard` \| `soft` |

## Reference implementations (optional — "start here", NOT evidence)

> Paste one row per `reference_implementations` entry: a working artefact an adopting
> project clones or scaffolds from. `kind` ∈ `iac` \| `app` \| `notebook` \| `scaffold`;
> `url` a real URI; `provisions` free-text (e.g. `azure`, `aws`); `notes` optional.
> This field is **ADVISORY and DISTINCT from evidence**: it answers "what do I start
> from?", not "was this built?", and it **never gates promotion** (the gate runs through
> `evidence[]` alone). If an entry IS a real build, list it under Evidence too. Do NOT
> fabricate a URL — if you have no confirmed repo, use a clearly-marked placeholder
> (`https://github.com/ORG/REPLACE-ME-...`) and note that a CODEOWNER replaces it before
> approval. Leave the table empty if the pattern has none.

| `kind` | url | provisions | notes |
|---|---|---|---|
| `iac` \| `app` \| `notebook` \| `scaffold` | | | |

## Fulfils a capability

> Name the `capability_key` from `capabilities/INDEX.md` that this pattern fulfils, and
> confirm the pattern meets (or honestly waives) that capability's `governance_nfrs`
> floor. The forward edge lives on the capability (`fulfilled_by[].pattern_key`); the
> `fulfils:` field on this pattern is its mirror.

- Fulfils: `CAP-...`
- Meets the capability's governance floor? <!-- yes / waived (say which and why) -->

## Evidence / artefacts proving it was built

> A pattern is a claim that something was built. Paste each `evidence` entry as
> `title` + a real, resolvable `url` (repo, PR, runbook, ADR, dashboard, load-test,
> post-mortem, doc). `evidence` is REQUIRED once `approval_status` is `provisional` or
> `approved`; a `candidate` may have none yet. Do not fabricate a link to fill the slot.

- <!-- title — url -->

## Validity, sunset, supersede

> Confirm the dated lifecycle. `valid_from` + `validity_check_months` derive the next
> review (the `pattern-lifecycle` Action nudges when it elapses; it never blocks). If
> this supersedes an older pattern, link both directions and set the old one to
> `deprecated` (never delete a pattern with adoptions — its provenance must survive).

- Next review derives as `valid_from` + `validity_check_months` = `YYYY-MM-DD`
- Supersede chain (if any): old `PAT-...` ↔ new `PAT-...`, old set to `deprecated`

## Spike caveats (for a spike-needed component)

> If this pattern was proven only through a spike, record the limits, caveats, and
> compromises the spike surfaced — the conditions under which it does NOT hold, what
> stayed unverified, and what a later project must re-check. Leave blank if the pattern
> is backed by a full production build rather than a spike.

-

## Agent self-certification

> AGENT: tick each box only after you have actually done it. These are honest
> self-checks, not a gate — the human reviewer relies on them to focus their read.

- [ ] `pattern_key` matches the schema regex `^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$` and is unique.
- [ ] Evidence is present **or** `approval_status: candidate` (no `provisional`/`approved` without evidence).
- [ ] This pattern fulfils a capability that exists in `capabilities/INDEX.md` (the `fulfils:` / `CAP-...` above).
- [ ] Ran the frontmatter linter and it passed: `python3 skills/_scripts/lint_pattern_frontmatter.py patterns/<category>/<slug>.md` — paste the result below.
- [ ] Did NOT set `approval_status` beyond `candidate`, `approved_by`, `approved_at`, `maturity`, or `adoption_count`.

```
<!-- AGENT: paste the lint_pattern_frontmatter.py output here -->
```

## Notes for the reviewing human

> What the reviewer needs to weigh before merging: where this was built, the sharpest
> tradeoff, anything left out of scope, anything you were unsure of. State the honest
> "here is what I could not verify" — it is the most useful line in this box.

<!--
  Merging this PR ratifies the pattern in its merged state. The CODEOWNER architect
  (patterns/** is gated) confirms the evidence is real and, in a commit they own,
  raises approval_status past candidate and fills approved_by / approved_at / evidence.
  The agent stops at candidate.
-->
