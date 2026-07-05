# Analysis context: SPIKE-001-guide-rag-context-backend

Canonical analysis artifact:

    spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md

Supporting research (read as needed):

| File | Role |
|------|------|
| `spdd/analysis/SPIKE-001-guide-rag-context-backend-research.md` | Confirmational research (2026-06-19) |
| `spdd/analysis/SPIKE-001-dice-entity-schema.md` | Leg 3 DICE entity design (T02) |
| `spdd/analysis/SPIKE-001-guide-ingest-agent-context-exploration.md` | T01 ingest + MCP spot-check log |

Operator runbook (spike branch, orchestrator-only):

    docs/spike-guide-ingest-agent-context.md

## Top keywords

Guide RAG, agent-context, context-index, resolve-agent-context, retrieval A/B,
menke-5, mock retrieval fixture, branch isolation

## Code areas (spike branch)

- `templates/guide-profiles/`
- `scripts/guide/`
- `examples/retrieval-fixture/` (planned T07)
- `tests/test-retrieval-fixture-resolver.sh` (planned T07)
