# Retrieval, not generation — the grounding discipline

> The single rule that makes `recommend-component-patterns` trustworthy: **every
> pattern named must already exist in `patterns/`** — proven, PR-reviewed,
> evidence-backed, in date. This step retrieves and judges; it does not author new
> patterns. Any similarity or fit claim is **computed from and cited to real
> pattern frontmatter**, never emitted from the model's imagination.
>
> Concretely: the model chooses **only** from a candidate block of real library
> rows, and returns keys that MUST be among them.

## Why retrieval, not generation

The project already has outcomes, requirements, attached NFRs, and a sense of
topology and data placement. The job is **not** to invent an architecture. It is
to **retrieve** the approved patterns that genuinely fit and hand a human a short,
defensible shortlist.

Adopting an approved pattern is the fastest route to a *governed* design: the
pattern already carries its validated NFRs, its evidence of having been built, and
its caveats. **Reuse beats invention.** If nothing fits, that is a real, useful
answer — say so and route to `architect/surface-solution-options`.

## The discipline, concretely

### 1. The legal key set is fixed before reasoning

The deterministic STEP 1 reads every file under `patterns/` and builds the
`patterns_block` — one line per real file:

```
pattern_key | name | category | deployment_topology | data_placement — one-line summary
```

This exists **precisely so the set of legal keys is fixed before reasoning.**
Every `pattern_key` the model may later return is guaranteed to trace to a real
file. Wanting to recommend something that is not in the block is the
**honest-empty signal**, not licence to mint a key.

### 2. Fit is computed from real frontmatter dimensions

Ground every fit claim in **these exact dimensions**, read from the candidate row
— not in vague vibes:

- **`deployment_topology`** — does it match the project's stated topology? (Don't
  recommend an on-prem cluster for an in-region managed-service project.)
- **`data_placement`** — does it satisfy the data-residency constraint? (Reject a
  global multi-region store when "PII stays in-region" is a requirement.)
- **`attached_nfrs`** — do they cover the NFRs this project actually needs, and
  where are the gaps the human should know about? (NFR-kind vocabulary:
  `patterns/_schema/nfr-kinds.enum.txt`.)

A rationale that cites a row's topology / placement / NFRs is grounded. A
rationale that reads like a generated essay about an ideal architecture is not —
rewrite it to cite the row.

### 3. Status and dates condition adoptability (advisory, not hard)

- `approval_status: deprecated` → do **not** recommend; point at `superseded_by`.
- `approval_status: candidate` → may be recommended, but **must** be flagged as an
  unreviewed draft in the rationale; `provisional` → "reviewed, use with care."
- `sunset_at` / the computed next-review date (`valid_from + validity_check_months`)
  in the past → flag as **stale** (a soft caveat, not a hard exclusion — the
  library is advisory).

### 4. Honest emptiness routes to exploration

If, after reasoning, **nothing genuinely fits**, do **not** pad the list to look
productive. Recommend **none**, say plainly why the library does not cover this
project's shape, and route to `architect/surface-solution-options`. A confident
"the library has nothing for this — here's why, go explore" is more valuable than
a forced match the human has to unpick later. Honest emptiness is a first-class
outcome.

### 5. Override is a recorded escape hatch

A human may **accept**, **override**, or **reject** any recommendation. Override
is not silent — it appends a reasoned line to `adoptions/ledger.jsonl`:

```jsonl
{"pattern_key": "PAT-WEBAPP-PG", "repo": "<owner/project>", "disposition": "overridden-out", "at": "2026-06-15", "override_reason": "Client contract mandates on-prem; managed-Postgres topology is disallowed."}
```

`disposition` is the closed ledger enum — `adopted-clean`, `adopted-with-overrides`
(with an `override_reason`), `overridden-out` (with an `override_reason`). The
ledger is the durable "why this / why not this" provenance; it is advisory. (These
same rows feed the maturity computation in `library/pattern-library-curate`.)

## The v1 scaling ceiling

The LLM reads the pattern `.md` files **directly** — no vector index, no embedding
store, no retrieval service. This keeps the library portable (plain markdown in
git), human-auditable (a PR diff shows exactly what changed), and dependency-free.
The ceiling: reading every file into context does not scale past ~a few dozen
patterns. Past that, the fix is a retrieval index (embed each pattern's
frontmatter + summary, retrieve top-K) **feeding this same prompt** — the method
does not change, only how the `patterns_block` is assembled. Retrieval stays
grounded in real rows either way.

## The anti-patterns this prevents

- **Never invent a `pattern_key`.** Every key traces to a real file. The
  honest-empty route exists for the case where nothing fits.
- **Don't oversell.** Every recommendation states its trade-off or caveat. A
  recommendation with no caveat is one not thought hard enough about.
- **Prefer a small set.** One well-defended pattern beats five hedged ones.
- **None is a valid answer.** Recommending nothing and routing to exploration is a
  confident, correct outcome — not a failure.
