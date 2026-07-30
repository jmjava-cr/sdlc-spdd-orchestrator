# Analysis: SPIKE-001-guide-rag-context-backend

**Work ID:** SPIKE-001-guide-rag-context-backend  
**Date:** 2026-07-15  
**Phase:** analysis (resume after FEAT-004/005 scoreboard landed)  
**Related research:** `spdd/analysis/SPIKE-001-guide-rag-context-backend-research.md`  
**Entity schema:** `spdd/analysis/SPIKE-001-dice-entity-schema.md`

---

## Domain Keywords

- guide
- DICE
- Neo4j
- RAG
- MCP
- context retrieval
- FEAT-004 ledger

## Code Areas

- agent-context/memory
- spdd/canvas
- scripts/resolve-agent-context.sh
- (external) embabel guide / Neo4j

## Scope Lock

### IN SCOPE

- Confirm FEAT-004/005 scoreboard is available for A/B
- Formalize remaining experiment steps (T01–T06) against live Guide
- Record interim decision given environment blockers

### NOT IN SCOPE

- Production wiring into default `resolve-agent-context.sh`
- Shipping Guide/Neo4j as a required dependency
- Completing A/B while Guide MCP is unavailable

### Reference-only

- Prior confirmational research (2026-06-19)
- Draft DICE entity schema (T02 largely done as draft)
- FEAT-004 ledger + FEAT-005 readiness/cycle metrics

---

## Findings (2026-07-15)

| Gate | Status |
|------|--------|
| FEAT-004 ledger | ✅ Complete — usable as scoreboard |
| FEAT-005 readiness / cycle metrics | ✅ Complete — optional leading indicators |
| Guide MCP (`user-embabel-dev`) | ❌ Not connected (`helloBanner` → Not connected); `spdd_*` tools discovery error |
| Orchestrator memory ingest into Guide | ⏳ Pending (T01) |
| Entity projection / `__Entity__` | ⏳ Pending (T03); schema draft exists (T02) |
| A/B + go/no-go | ⏳ Blocked on MCP + T01/T03 |

### Interim recommendation (not final go/no-go)

- **Architecture:** proceed with the three-leg DICE hybrid experiment when Guide is up
  (research already validated design).
- **Production:** **no-go** until A/B (T05) and written decision (T06) complete.
- **Default path:** remain markdown-first; Guide stays optional.

### Unblock checklist

1. Restore Guide MCP SSE (local guide on `:21337` or configured port).
2. Finish T01: ingest `agent-context/memory/` + selected `spdd/canvas/`.
3. T03: projection ingest per entity schema.
4. T04–T06: sanity retrieval → A/B on one Work ID → go/no-go.

### Next command (when Guide is up)

```
./scripts/sdlc.sh claim SPIKE-001-guide-rag-context-backend
./scripts/sdlc.sh resume SPIKE-001-guide-rag-context-backend --phase code
/sdlc-spdd-code @spdd/canvas/SPIKE-001-guide-rag-context-backend.md operation T01
```
