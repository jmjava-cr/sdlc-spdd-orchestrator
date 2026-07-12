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

### 2026-07-11 — Guide spike branch build + runtime friction (resolved on branch)

1. **`embabel-agent-rag-neo-drivine` snapshot drift.** Floating `0.1.2-SNAPSHOT` resolved to
   build `20260428` which extends `EmbeddingAwareChunkingContentElementRepository` — a class
   that only exists in embabel-agent `0.4.0-SNAPSHOT`. Guide pins agent `0.3.5-SNAPSHOT`, so
   compile failed (`cannot access EmbeddingAwareChunkingContentElementRepository`). A full bump
   to agent 0.4.0 breaks other Guide code (`InvalidApiKeyException` moved out of
   `com.embabel.agent.spi`). **Fix:** pin `embabel-agent-rag-neo-drivine` to timestamp
   `0.1.2-20260224.010659-19` (pre-`EmbeddingAware`).
2. **drivine4j starter too old for chat-store.** `ChatStoreAutoConfiguration` references
   `org.drivine.schema.SchemaCatalog`, absent in drivine4j `0.0.29` → startup
   `ClassNotFoundException`. **Fix:** bump `drivine4j-spring-boot-starter` to `0.0.45`.
3. **Unit test API drift.** `InMemoryNamedEntityDataRepository` no longer accepts a null
   `NativeFinder`; mocked `EmbeddingService.embed` must return a vector (save() embeds
   eagerly). Test updated; also asserts the new `subgraphForWorkId` read path.
4. **Ingest JVM dies mid-run — ONNX native crash.** Repeated `append-ingest` runs terminated
   during startup re-ingestion: exit 137 (SIGKILL) twice, then exit 134 with an hs_err file
   showing a SIGSEGV in `libonnxruntime.so` (`hs_err_pid2780387.log`, frame
   `libonnxruntime.so+0xbd6db3`, on the `IngestionRunner.run` stack). Root cause is the native
   ONNX embedding runtime under sustained embedding load, not heap sizing. Practical
   mitigation for the spike: ingestion is append-mode idempotent (merge by id), so re-running
   the script resumes; entity projection data is unaffected (separate write path).
5. Startup logs a transient Neo4j `AuthenticationException` (scheme 'none') from one early
   connection before credentials apply; ingestion proceeds normally afterwards.

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
