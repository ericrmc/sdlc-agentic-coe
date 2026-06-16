# Skill security scan (SkillSpector, static)

Scans the skills for malicious or injectable patterns before they enter the shared
library — prompt-injection, data-exfiltration, privilege-escalation, supply-chain,
tool-misuse and ~12 more categories — using [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector)
(Apache-2.0). **Static analyzers only** (pattern + YARA + AST + taint + OSV): **no API
key, no model.**

**Advisory, never a gate.** A finding is a prompt for human review, not proof of malice.
Static patterns over-flag — e.g. `P2 Hidden Instructions` fires on a skill that legitimately
*discusses* instruction-handling (the `ingest` skill does). Read the finding and judge it.

## Run it

```bash
# scan the skills you changed (vs origin/main) — what you run before a PR
python3 security/skillspector/scan.py

python3 security/skillspector/scan.py --all                 # every skill
python3 security/skillspector/scan.py skills/<cat>/<name>   # specific skill(s)
```

Per-skill + merged SARIF land in `reports/` (git-ignored). The same runner backs the
advisory `skill-security-scan` GitHub Action, which scans a PR's changed skills and posts
findings to the **Security** tab.

**Prerequisite:** [`uv`](https://docs.astral.sh/uv/) (recommended) —
`curl -LsSf https://astral.sh/uv/install.sh | sh`. SkillSpector needs Python 3.12/3.13; uv
fetches it for you. The runner falls back to a local venv if you already have a 3.12/3.13.

## Pinning

SkillSpector has no PyPI release or git tag, so the runner pins an **immutable commit SHA**
(`SKILLSPECTOR_REF` in `scan.py`) and builds from source. An upgrade = bump that SHA after
reviewing the diff — the scanner pulls a wide tree (semgrep, YARA, langchain), so it is
itself a dependency surface worth a glance.

## The semantic layer (not run here)

SkillSpector also has 3 **semantic** analyzers (`developer_intent`, `quality_policy`,
`security_discovery`) that use an LLM to add depth and filter false positives. They are
**not** run locally-by-default or in CI, because they need a model. To run them, install
upstream and point it at a provider (`SKILLSPECTOR_PROVIDER=anthropic` + a key, or
`OPENAI_BASE_URL` at a local endpoint). A small OpenAI-compatible shim that fronts a local
coding-agent subscription (so no per-token key is needed) is a deliberate future add-on, not
yet built.
