# The architecture checklist — the deterministic floor of design review

> The built-in checklist `design-review-findings` walks against every design draft
> **before** any open-ended reasoning. These are the things a managed-services
> governance panel will ask about *every single time*, so a draft that is silent on
> one of them has a gap worth a finding. The checklist is the **floor**: even with no
> model available, walking it (Step 1) and running the validation harness (Step 3)
> produces a useful, trustworthy review.
>
> This is a **reviewer's checklist, not a verdict.** A silent item produces a *finding*,
> never a pass/fail. A human decides what to do with it.

## How to use it

For each item below, ask of the draft: **does it state this, and is what it states
adequate?**

- **Silent** on the item → typically a `medium` finding (raise to `high` when the
  project context makes that item load-bearing — e.g. a regulated-data project that
  is silent on encryption-at-rest).
- **Present but vague** → a `low` or `medium` finding ("stated, but not specific
  enough to act on / audit").
- **Present and adequate** → no finding needed (optionally an `info` note for
  traceability).

Every finding carries a `ref` citing the thing it attaches to (an NFR, a pattern, a
design section). Run the output through the validation harness (severity clamp,
default-ref, drop-empty) exactly as `design-review-findings` Step 3 specifies.

## The checklist items

### 1. RPO / RTO — recovery point & recovery time objectives
Is the **data-loss tolerance** (how much data may be lost on failure — the recovery
*point*) and the **recovery time** (how long to be back up — the recovery *time*)
stated, or unstated? A topology with an availability SLA but no stated RPO/RTO is not
credibly recoverable — the SLA is a number with no recovery story behind it. Cite the
availability NFR or the deployment section.

### 2. Encryption at rest
Is the **at-rest posture** for stored data declared — what is encrypted, with what,
and who holds the keys (key custody)? "Encrypted at rest" with no key-custody story is
half a finding. A managed-services panel asks this for every datastore. Cite the data
section or the storage NFR.

### 3. RBAC between tiers
Is access control **between the tiers** (web → app → data) specified — not just at the
edge? A draft that secures the public edge but leaves tier-to-tier access implicit has
a gap: a compromised web tier should not have unrestricted reach into the data tier.
Cite the adopted pattern or the security NFR.

### 4. Deployment topology / availability model
**How is it deployed** — across how many zones / regions, with what availability
target, and what failover behaviour? A single-region topology paired with a high
availability SLA is a contradiction worth surfacing. Cite the deployment / application-
architecture section.

### 5. Secret rotation
Are **credentials and keys rotated**, and how / on what cadence? Static, never-rotated
secrets are a standing audit finding. State whether secrets rotate and the mechanism.
Cite the operations section or the security NFR.

### 6. Unclassified integrations
Are there **integration points whose data-sensitivity, auth mechanism, or ownership is
left unclassified**? Every external feed, partner API, or third-party dependency should
have its sensitivity, how it authenticates, and who owns it stated. An unclassified
integration is the most common thing a panel sends back. Cite the integrations section
or the specific integration.

## The severity rubric (applied per item)

| Draft state | Default severity |
|---|---|
| Item is silent | `medium` (→ `high` if context makes it load-bearing) |
| Item present but vague / un-auditable | `low` or `medium` |
| Item present and adequate | no finding (or `info` for traceability) |

## Notes

- **This is the universal-omissions checklist.** The LLM step (`design-review-findings`
  Step 2) catches the *design-specific* gaps beyond these six; this checklist catches
  the ones a panel raises on every project. Together they are the engine.
- **The checklist is the only licence to flag an *absence*.** Everything else a finding
  raises must be grounded in text that is *present* in the draft. A silent checklist
  item is a legitimate finding precisely because the checklist says a panel will ask.
- **It is advisory.** A silent item is a finding, never a verdict. There is no
  pass/fail — surface it, let a human decide.
- The **front-end / a11y** companion (`frontend-a11y-review`) is the same engine with a
  **WCAG 2.2 AA** success-criteria checklist swapped in for this one and `wcag:` refs;
  the finding shape, the severity set, and the harness are identical.
