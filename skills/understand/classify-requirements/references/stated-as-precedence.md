# `stated_as` precedence + the deterministic backstop

This file is the **optional, deterministic backstop** for `classify-requirements`. It is a coarse keyword/regex pass that produces the same five fields with **no model call** — useful for offline runs, regression tests, and cross-checking the model. The model reasoning step in `SKILL.md` is the real classifier; when the two disagree, prefer the model and note the divergence.

Everything here is pure substring/regex over the lowercased requirement text, so the same text always classifies the same way (idempotent).

---

## The precedence rule (load-bearing)

When more than one `stated_as` could apply, the **highest** wins:

```
solution > constraint > symptom > need
```

Read top to bottom; the first bucket whose keywords match decides `stated_as`. If none match, it is `need` (the default).

| stated_as  | one-line definition                                              |
|------------|------------------------------------------------------------------|
| solution   | names an implementation / mechanism / product (solutioneering)   |
| constraint | a boundary / prohibition / residency / compliance rule           |
| symptom    | a problem with no target or condition                            |
| need       | a clean statement of the underlying need (the default)           |

---

## Field-by-field backstop

### `layer` — `technical` if any tech keyword appears, else `business`

```
TECH_KEYWORDS:
  psycopg, sqlalchemy, cors, tls, endpoint, container, postgres, schema,
  raw sql, migration, api tier, data store, encrypt, react, fastapi, vite
```

### `stated_as` — first bucket to match, in precedence order

**1. solution** (highest precedence):
```
SOLUTION_KEYWORDS:
  sqlalchemy, psycopg, "use ", "call an external", llm api, power automate,
  kafka, redis, "via entra", react, vite, docker, kubernetes
```

**2. constraint:**
```
CONSTRAINT_KEYWORDS:
  must not, shall not, never, no network, residency, regional boundary,
  remain within, in-region, boundary, sovereign
```

**3. symptom:**
```
SYMPTOM_KEYWORDS:
  is slow, too slow, users complain, hard to, difficult to, confusing, unreliable
```

**4. need** — none of the above matched.

### `quantified` — a digit co-occurring with a unit/consequence token

`true` iff the text contains a digit **and** one of:

```
ms | % | days | users | GB | TLS 1. | 99.
```

(A bare number with no unit/consequence token → `false`.)

### `value_outcome` — first outcome keyword hit (insertion order), else `null`

The keyword → outcome map is project-specific; below is an illustrative example map. Replace its keywords and labels with ones drawn from the project context, keep them short, and return `null` (a value-orphan) when nothing matches.

| keyword      | outcome label                                                       |
|--------------|---------------------------------------------------------------------|
| propose      | Faster, more consistent requirement capture for delivery leads.     |
| ratif        | Auditable human control over what the system commits to.            |
| event        | Defensible governance + handover via a complete audit trail.        |
| governance   | Repeatable, compliant sign-off that de-risks delivery.              |
| portfolio    | Multi-project visibility for practice leads.                        |
| comment      | Captured peer/reviewer dissent without blocking flow.               |
| pattern      | Reuse of proven solutions to cut delivery effort and risk.          |
| estimate     | Credible, comparator-grounded effort forecasts.                     |
| residency    | Regulatory compliance and client data-sovereignty guarantees.       |
| availability | Reliable access for delivery teams during working hours.            |
| respond      | Responsive interaction keeps users in flow.                         |

> When emitting the final field, compress the outcome to a **≤ 4 word display label** (e.g. "Data sovereignty", "Audit trail"). The long forms above are the rationale, not the label.

### `suggested_rewrite` — only when `stated_as = solution`, else `null`

Match a per-keyword rewrite; fall back to the generic one. In every non-solution case it MUST be `null`.

| keyword        | need-shaped rewrite                                                                                                          |
|----------------|-----------------------------------------------------------------------------------------------------------------------------|
| sqlalchemy     | Express the need: the backend must persist and query structured records reliably — let the design phase choose the access mechanism. |
| psycopg        | Express the need: the backend must persist and query structured records reliably — let the design phase choose the access mechanism. |
| llm api        | Express the need: the system must generate candidate requirements from project context — let the design phase choose where the model runs. |
| power automate | Express the need: approval steps must be orchestrated and auditable — let the design phase choose the orchestration mechanism. |

Generic fallback (no keyword matched):
```
Express the underlying need: <what capability/outcome is required> — and
let the design phase choose the mechanism.
```

---

## Worked precedence examples

| text                                                           | matches                | stated_as (precedence) |
|----------------------------------------------------------------|------------------------|------------------------|
| "Use Redis; it must not leave the AU region."                  | solution + constraint  | **solution**           |
| "Data must remain within the region and is too slow today."    | constraint + symptom   | **constraint**         |
| "The current export is too slow."                              | symptom                | **symptom**            |
| "A dispatcher can publish a day's routes in under 30 seconds." | none                   | **need**               |

The backstop is intentionally blunt. Treat any case where the deterministic pass and the model disagree as an edge case worth a human glance — that disagreement is exactly where the interesting requirements live.
