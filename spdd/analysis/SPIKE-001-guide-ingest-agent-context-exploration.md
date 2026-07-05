# SPIKE-001 — Guide ingest for agent-context (exploration log)

> **SPDD flow:** requirement → `spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md` →
> canvas → this log. **Branch:** `cursor/spike-guide-ingest-agent-context-17f4` only — not `main`.

Work ID: SPIKE-001-guide-rag-context-backend  
Task: T01 — stand up guide + ingest orchestrator memory (leg 2)  
Guide branch: `jmjava/guide` → `ingest-to-hub` (git incremental + operator purge API)

## Goal

Prove that append-ingesting `agent-context/memory/`, `spdd/canvas/`, and `spdd/analysis/`
into the existing menke corpus makes orchestrator Work IDs discoverable via embabel-dev MCP
(`docs_vectorSearch`, `docs_textSearch`) — the prerequisite for T05 A/B vs markdown resolver.

## Setup checklist

- [ ] Guide on `ingest-to-hub` at `~/github/jmjava/guide`
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
| `CHORE-001 docgen initial documentation` | vector | Hit on chore canvas/analysis | | |

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
2. T03 — entity projection ingest (leg 3, `__Entity__` > 0)
3. T05 — A/B one Work ID: resolver vs embedding-only vs hybrid

## T05 fixture drill (in progress)

Ledger: `spdd/analysis/SPIKE-001-retrieval-ab-ledger.md`

```bash
./scripts/guide/run-retrieval-ab-fixture.sh --capture-a
# after MCP: --check-mcp your-mcp-results.tsv
```
