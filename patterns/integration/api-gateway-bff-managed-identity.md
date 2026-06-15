---
pattern_key: PAT-APIGW-BFF
name: API gateway + managed identity + backend-for-frontend
category: integration
intent: "use WHEN a multi-client product portfolio needs consolidated auth/rate-limiting/observability so that a gateway + per-client BFF mediates all auth and downstream calls"
deployment_topology: API gateway (APIM/Kong) fronting microservices; BFF layer per client type; Entra/OIDC for identity
data_placement: No client receives raw service tokens; the BFF mediates all auth flows and downstream calls
summary: Consolidates cross-cutting concerns at the gateway; a BFF reshapes responses per client; suitable for multi-client (web/mobile/partner) portfolios.
approval_status: provisional
approved_by: "@architects"
approved_at: "2026-06-15"
valid_from: "2026-06-15"
validity_check_months: 12
evidence:
  - {title: "Multi-client web project — recorded gateway/BFF adoption decision (with override)", url: "https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/multi-client-web/adoption-decision.md", kind: doc, project: "multi-client-web"}
constraints:
  - {statement: "BFF must be stateless; session affinity disabled", enforced: hard}
attached_nfrs:
  - {kind: security, statement: "All tokens short-lived; refresh-token rotation mandatory", acceptance_criterion: "Access tokens expire <=1h; refresh rotation enforced"}
  - {kind: observability, statement: "Distributed tracing through gateway and BFF; correlation IDs required", acceptance_criterion: "Every request carries a correlation ID traced end-to-end"}
  - {kind: availability, statement: "Gateway is a SPOF; active-active with health checks required", acceptance_criterion: "Gateway runs active-active across >=2 nodes with health checks"}
  - {kind: scalability, statement: "BFF stateless; session affinity disabled at the gateway", acceptance_criterion: "BFF instances are interchangeable; no sticky sessions"}
---

# API gateway + managed identity + backend-for-frontend (`PAT-APIGW-BFF`)

> Integration pattern. **`approval_status: provisional`** — reviewed and usable with care; its
> evidence is a real recorded adoption decision (including the worked override below) pending a
> production reference build. **Advisory, not enforced** — recommend it, adopt it, or override it
> with a recorded reason. Nothing in this Centre of Excellence blocks a project from choosing
> otherwise; it only asks that the *why* be written down.

## Summary

Consolidates cross-cutting concerns (auth, rate limiting, observability) at the gateway. A backend-for-frontend (BFF) aggregates and reshapes service responses per client. Suitable for multi-client (web, mobile, partner) product portfolios.

The deployment topology is an **API gateway (APIM / Kong) fronting microservices**, with a **BFF layer per client type**, and **Entra/OIDC for identity**. On data placement: **no client receives raw service tokens; the BFF mediates all auth flows and downstream calls.**

## When to use

Reach for this pattern when you have a **multi-client product portfolio** — web, mobile, and partner clients consuming the same underlying services — and you want one place to enforce authentication, rate limiting, and observability rather than re-implementing those concerns in every service.

- **Use it WHEN:** several client types share a backend and each needs a slightly different response shape; cross-cutting auth/rate-limiting/tracing should be consolidated; clients must never hold raw service tokens.
- **Use it WHEN:** identity is centralised (Entra/OIDC) and you want the gateway + BFF to mediate every downstream call so the client surface stays thin.

## Attached NFRs

These four NFRs ride with the pattern. Adopt the pattern and you inherit them; each carries a measurable acceptance criterion so a downstream project can check it later. Kinds are drawn from the closed enum: `security`, `observability`, `availability`, `scalability`.

| Kind | Statement | Acceptance criterion |
|---|---|---|
| `security` | All tokens are short-lived; refresh-token rotation mandatory | Access tokens expire `<=1h`; refresh rotation enforced |
| `observability` | Distributed tracing through gateway and BFF; correlation IDs required | Every request carries a correlation ID traced end-to-end |
| `availability` | Gateway is a SPOF; active-active with health checks required | Gateway runs active-active across `>=2` nodes with health checks |
| `scalability` | BFF must be stateless; session affinity disabled at the gateway | BFF instances are interchangeable; no sticky sessions |

## Trade-offs

- **The gateway is a single point of failure.** Everything flows through it, so an outage takes the whole portfolio down. *Mitigate with active-active* across at least two nodes with health checks (see the `availability` NFR). This is the price of consolidating cross-cutting concerns in one tier.
- **A BFF per client type adds tiers to run and review.** More services means more deployment surface, more network paths, and — in regulated shops — more security review. That cost is real and is exactly what the override example below pushes back on.
- **Statelessness is non-negotiable for scale.** The BFF must hold no session state and session affinity must be disabled at the gateway (the `scalability` NFR + the hard constraint), otherwise instances stop being interchangeable and you lose horizontal scaling.

## Adoption & overrides

This pattern is **recommended, never mandated**. A project may adopt it as-is, adopt it partially, or decline it — and declining is a first-class, honest signal as long as the reason is recorded. The Centre of Excellence values a well-reasoned non-adoption as much as an adoption: it tells the next team *why* the obvious choice was the wrong one here.

### Worked override example (real, from the seed corpus)

A multi-client web project mapped cleanly onto this pattern — **Azure Application Gateway + Entra SSO**, with a BFF layer that would have neatly separated the admin and customer views. The agent recommended it. But the client could not take it:

- **Recommended:** API gateway + managed identity + BFF (this pattern).
- **Blocker:** the **client IT security policy prohibited a separate BFF service tier** (additional service tiers triggered a separate network-level security review the client would not sanction).
- **Chosen alternative:** **"path-prefix routing within a single container (no separate BFF service), `/admin` protected by an Entra role claim at the application layer."**

So instead of a dedicated BFF service, the admin and customer surfaces live in one container, separated by path prefix, with `/admin` gated by an Entra role claim at the application layer rather than at a network tier. The security intent (only admins reach admin) is preserved; the tier count is reduced to satisfy the policy.

### How this gets recorded

This override would be recorded in **`adoptions/ledger.jsonl`** as one line with **`disposition: overridden-out`** and the reason above — a ready demonstration of capturing *why a recommended pattern was declined*:

```jsonl
{"pattern_key": "PAT-APIGW-BFF", "repo": "acme/citizen-portal", "disposition": "overridden-out", "at": "2026-06-13", "override_reason": "Client IT security policy prohibits additional service tiers that require separate network-level security review; chose path-prefix routing within a single container (/admin protected by an Entra role claim at the application layer).", "override_count": 1}
```

(This is exactly the line already recorded in `adoptions/ledger.jsonl` for this pattern.)

Nothing here blocks the project — the ledger line *is* the governance: lightweight, append-only, and honest about what was not adopted and why.

## Example / artefacts

- **Reference topology:** Azure Application Gateway (L7, WAF) → microservices, with a per-client BFF and Entra/OIDC identity. The gateway holds auth, rate limiting, and tracing; the BFF reshapes responses per client and is the only thing that ever touches raw service tokens.
- **Evidence of adoption:** see the `evidence` entry in this file's frontmatter — the recorded gateway/BFF adoption decision (with override) on the multi-client web engagement. Patterns in this library are PR-reviewed by a human; a CODEOWNER attaches a production reference build to promote this from `provisional` to `approved`.
- **Override evidence:** the worked example above, drawn from the seed corpus, is the artefact for the non-adoption path — it shows the `overridden-out` ledger shape end to end.

## References

- Closed NFR kind vocabulary: `nfrs/nfr-kinds.md` (this pattern attaches `security`, `observability`, `availability`, `scalability`).
- Adoption ledger: `adoptions/ledger.jsonl` (append-only; `disposition` ∈ `adopted-clean` | `adopted-with-overrides` | `overridden-out`) — see `adoptions/README.md`.
- Validity: re-reviewed every `validity_check_months` (12). When retired, set `approval_status: deprecated` + `superseded_by: <key>`, and optionally a `sunset_at` date — the pattern is deprecated, never deleted, because it has a recorded adoption.
