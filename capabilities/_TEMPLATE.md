---
# ============================================================================
# CAPABILITY FRONTMATTER — copy this whole block into your new capability file.
# A capability is the named middle term between a plain-language need and the
# component patterns that fulfil it. Every field carries an inline comment:
# REQUIRED | CONDITIONAL | OPTIONAL. This library is LIGHT and ADVISORY —
# nothing here gates a downstream project. approval_status and confidence:
# proven are human signals of trust, not enforcement locks; an agent never
# sets them.
# ============================================================================

capability_key: CAP-EXAMPLE-KEY  # REQUIRED. Stable, UPPER-KEBAB after CAP-, cite-able, survives renames.
                                 #   This is what a requirement cites (fulfils_capability: CAP-...) and
                                 #   what a pattern back-references (fulfils: [CAP-...]).
name: ""                         # REQUIRED. Human title, e.g. "Online Analytical Processing (OLAP)".
capability_domain: data          # REQUIRED. Closed enum: data | compute | integration | runtime | experience | governance.
summary: ""                      # REQUIRED. One paragraph. What the capability is, at a glance.
need_statement: ""               # REQUIRED. Technology-free, "a system needs to ... so that ..." form.
                                 #   Name the PROBLEM, never the product. The need outlives the component.
aliases:                         # REQUIRED (>=2). Lay synonyms a non-expert would type for this need.
  - ""                           #   These feed capabilities/INDEX.md, the alias-searchable lookup a
  - ""                           #   need-first reader is pointed at first. One alias is not findable.

# ---- How the need is fulfilled — proven-vs-candidate lives HERE -------------
fulfilled_by:                    # REQUIRED (>=1 entry). Each {confidence, note, ...}.
  - confidence: candidate        #   'proven' = a built, evidenced pattern fulfils this today.
                                 #   'candidate' = plausible but still owes a spike; not recommendable yet.
                                 #   *** AN AGENT NEVER WRITES confidence: proven. ***
    note: ""                     #   One line: for proven, why this pattern fits; for candidate, the
                                 #   vendor component and the headline caveat.
    # pattern_key: PAT-...        #   REQUIRED when confidence: proven; OPTIONAL for a candidate (a
                                 #   candidate may name a vendor in `note` before any PAT- file exists).
    # evidence:                   #   REQUIRED when confidence: proven (build evidence, like a pattern).
    #   - {title: "", url: "https://..."}
    open_questions:              #   The spike questions a candidate must answer before promotion.
      - ""                       #   This is the honest core of a candidate — what gates its promotion.

# ---- The governance floor any fulfilling pattern must meet or waive ---------
governance_nfrs:                 # REQUIRED (>=1). [{kind, statement, acceptance_criterion}]
  - kind: security               #   kind is the CLOSED 11-value NFR enum shared with patterns:
                                 #     security | availability | performance | data-residency | observability |
                                 #     resilience | cost | compliance | scalability | data-governance | operations
    statement: ""                #   The minimum governance bar. Concrete and measurable.
    acceptance_criterion: ""     #   The testable "done" — e.g. "region == declared classification region".

# ---- Lifecycle (HUMAN-ONLY beyond candidate) -------------------------------
valid_from: "2026-06-15"         # REQUIRED. ISO date (quote it so it stays a string).
validity_check_months: 12        # OPTIONAL. Re-review cadence in months; candidates may have matured.
approval_status: candidate       # REQUIRED. Closed enum, ordered:
                                 #   candidate    — proposed; no proven fulfilment yet. An agent leaves it HERE.
                                 #   provisional  — a human reviewed it; has a proven, evidenced fulfilment.
                                 #   approved     — a human blessed it.
                                 #   deprecated   — do not use; see superseded_by.
                                 #   *** AN AGENT NEVER ADVANCES THIS BEYOND 'candidate'. ***
approved_by:                     # CONDITIONAL. Required once approval_status >= provisional. The reviewer.
approved_at:                     # CONDITIONAL. Required once approval_status >= provisional. ISO date.
superseded_by:                   # CONDITIONAL. Required when approval_status == deprecated. The capability_key to use instead.
---

# <name> (`CAP-EXAMPLE-KEY`)

> While `approval_status` reads `candidate`, this capability is a proposal — a named
> need with fulfilment options, not yet a blessed entry. A human promotes it in PR review.

## The need

State the need in plain, technology-free language — the problem a system has, and why it
matters. Mirror the `need_statement` frontmatter line. This is the stable part: the need
holds even as the components that fulfil it change.

## How it is fulfilled

> One subsection per `fulfilled_by` entry, ordered proven first, then candidates. A proven
> entry names its pattern and the evidence; a candidate names the vendor component and the
> spike questions that gate its promotion.

### Proven
- **`PAT-...`** — why this pattern fulfils the need cleanly, and the evidence behind it.

### Candidates (spikes owed)
- **<vendor component>** — confidence: candidate. Open questions a spike must answer:
  - <question 1>
  - <question 2>

## Governance floor

> One bullet per `governance_nfrs` entry, restating its **kind**, **statement**, and
> **acceptance_criterion**. This is the minimum bar any fulfilling pattern must meet or
> honestly waive — measure a candidate's spike result against it.

- **<kind>** — <statement>.
  _Acceptance:_ <testable criterion>.

## Aliases

Plain-language terms that resolve to this capability (these feed `capabilities/INDEX.md`):
<alias>, <alias>, ...

## Promotion

A candidate fulfilment is promoted to proven only by a human PR that attaches spike
evidence and a fulfilling pattern meeting the governance floor, then flips
`confidence: proven`. `approval_status` advances by the same human review. See
`CONTRIBUTING.md`. An agent stops at `candidate` and never flips `confidence` or
`approval_status`.
