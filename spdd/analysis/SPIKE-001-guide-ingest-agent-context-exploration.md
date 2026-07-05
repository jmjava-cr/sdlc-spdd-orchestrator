# SPIKE-001 — Guide ingest for agent-context (exploration log)

> **SPDD flow:** requirement → `spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md` →
> canvas → this log. **Branch:** `cursor/spike-guide-ingest-agent-context-17f4` only — not `main`.

Work ID: SPIKE-001-guide-rag-context-backend  
Task: T01 — stand up guide + ingest orchestrator memory (leg 2)  
Guide branch (leg 2): `jmjava/guide` → `ingest-to-hub`  
Guide branch (leg 3): `jmjava/guide` → `cursor/spike-spdd-dice-projection-17f4` (includes leg 2 + projection API)

## Goal

Prove that append-ingesting `agent-context/memory/`, `spdd/canvas/`, and `spdd/analysis/`
into the existing menke corpus makes orchestrator Work IDs discoverable via embabel-dev MCP
(`docs_vectorSearch`, `docs_textSearch`) — the prerequisite for T05 A/B vs markdown resolver.

## Setup checklist

- [ ] Guide on `cursor/spike-spdd-dice-projection-17f4` (or `ingest-to-hub` for leg 2 only)
- [ ] `application-menke-5.yml` with `spdd-projection.enabled: true` (see guide `application-menke-5-spdd-projection.yml.example`)
- [ ] menke-1–4 (or needed subset) already on Neo4j port `21337`
- [ ] `application-menke-5.yml` copied from `templates/guide-profiles/application-menke-5-orchestrator-context.yml.example`
- [ ] `./scripts/guide/append-orchestrator-context.sh` completed (INGESTION COMPLETE banner)
- [ ] embabel-dev MCP connected to `http://localhost:21337/sse`

## MCP spot-checks (fill in after ingest)

| Query | Tool | Expected | Result | Notes |
|-------|------|----------|--------|-------|
| `SPIKE-001 guide RAG context backend` | vector | Hit on `spdd/canvas/SPIKE-001-guide-rag-context-backend.md` | | |
| `+context-index +agent-context/memory` | text | Hit on `context-index.md` | | |
| `FEAT-004 prompt optimization ledger` | vector | Hit on FEAT-004 canvas or analysis | | |
| `SPIKE-FIX-001 retrieval fixture` | vector | Hit on fixture canvas | | |

## Leg 3 spot-checks (after projection load)

| Check | Command / API | Expected | Result | Notes |
|-------|---------------|----------|--------|-------|
| Projection API up | `GET /api/v1/data/spdd-projection/stats` | 200 JSON | | |
| Entity count | stats `totalEntities` | > 0 | | |
| Fixture subgraph | `./scripts/guide/project-spdd-entities.sh examples/retrieval-fixture` | WorkId entities | | |

## Ingestion summary

_Paste INGESTION COMPLETE banner stats here (directories loaded/failed, document counts)._

## Git incremental follow-up

After `sdlc.sh capture` updates memory indexes:

- [ ] Re-run append; confirm only changed files processed (check ingest log / git-ingestion state)
- [ ] MCP query returns updated index content

## Blockers / findings

_Record friction (path resolution, ingest time, chunk quality, false positives) here._

## T05 A/B protocol (fixture)

```bash
# 1. Mode (a) — auto-capture resolver metrics
./scripts/guide/run-retrieval-ab-fixture.sh --capture-a

# 2. Mode (b) — after menke-fixture ingest + MCP queries in Cursor:
#    Save URIs to mcp-results.tsv (see tests/fixtures/spike-001-mcp-results.example.tsv)
./scripts/guide/run-retrieval-ab-fixture.sh --check-mcp mcp-results.tsv

# 3. Record path_count + context_bytes in spdd/analysis/SPIKE-001-retrieval-ab-ledger.md
```

T01 setup check: `./scripts/guide/verify-spike-guide-setup.sh`

## Next steps (if ingest succeeds)

1. T02 — finalize DICE entity schema (`SPIKE-001-dice-entity-schema.md`)
2. T03 — verify entity projection locally (`project-spdd-entities.sh`, `__Entity__` > 0)
3. T04 — MCP entity traversal fork
4. T05 — A/B one Work ID: resolver vs embedding-only vs hybrid

## T05 fixture drill (in progress)

Ledger: `spdd/analysis/SPIKE-001-retrieval-ab-ledger.md`

```bash
./scripts/guide/run-retrieval-ab-fixture.sh --capture-a
# after MCP: --check-mcp your-mcp-results.tsv
```
