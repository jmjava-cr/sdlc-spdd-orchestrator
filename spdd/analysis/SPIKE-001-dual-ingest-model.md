# SPIKE-001 — Dual ingest model (leg 2 RAG + leg 3 DICE projection)

Work ID: SPIKE-001-guide-rag-context-backend  
Branch pair:

| Repo | Branch |
|------|--------|
| `jmjava/sdlc-spdd-orchestrator` | `cursor/spike-guide-ingest-agent-context-17f4` |
| `jmjava/guide` | `cursor/spike-spdd-dice-projection-17f4` (base: `ingest-to-hub`) |

Entity schema contract: `spdd/analysis/SPIKE-001-dice-entity-schema.md`.

## Short answer: they coexist

Both write to the **same Neo4j** store. Different node layers, different retrieval legs.
Neither replaces the other. DICE value lives in **leg 3** (typed domain memory); leg 2 is
discovery / paraphrase reach into chunk text.

| | Leg 2 — Guide RAG | Leg 3 — SPDD / DICE projection |
|---|-------------------|--------------------------------|
| **Neo4j layer** | `ContentElement` chunks + embeddings | `__Entity__` + typed relationships |
| **Write trigger** | `append-ingest.sh` / `load-references` | `POST /api/v1/data/spdd-projection/load` |
| **Config** | `guide.directories`, `guide.git-ingestion` | `guide.spdd-projection.enabled`, `default-root-path` |
| **Input** | Files under configured directories | Structured SPDD markdown (canvas, context-index) |
| **Parser** | Tika + chunker + embed | Markdown → `SimpleNamedEntityData` + `mergeRelationship` |
| **Idempotency** | Git revision state (incremental files) | Merge-by-entity-id |
| **Read today** | MCP `docs_vectorSearch`, `docs_textSearch` | HTTP `…/stats`, `…/work/{workId}` |
| **Read gap (T04)** | — | MCP domain-graph tool (fork) |
| **Auditability** | Lexical / cosine on chunks | Typed edges from WorkId join key |

## What leg 3 is NOT

| Path | Use for SPIKE-001 leg 3? |
|------|--------------------------|
| DICE **proposition pipeline** (conversation → propositions → graph) | **No** — unstructured text; wrong for REASONS canvases |
| Directory ingest alone | **No** — leaves `__Entity__` at 0 |
| Markdown `resolve-agent-context.sh` | **Baseline mode (a)** — stays on `main`; not Guide |

Leg 3 reuses **DICE entity conventions** (`NamedEntityData`, `DataDictionary`, `__Entity__`)
via **structured markdown projection**.

## Operator flow (both legs)

```bash
# 1. Guide on spike branch + menke-5 (leg 2 chunks)
cd ~/github/jmjava/guide
git checkout cursor/spike-spdd-dice-projection-17f4
# application-menke-5.yml with spdd-projection.enabled: true
GUIDE_PROFILE=menke-5 GUIDE_PORT=21337 SERVER_PORT=21337 ./scripts/append-ingest.sh

# 2. Leg 3 entity projection (same running Guide)
curl -s -X POST http://localhost:21337/api/v1/data/spdd-projection/load \
  -H 'Content-Type: application/json' \
  -d '{"rootPath":"/home/ubuntu/github/jmjava/sdlc-spdd-orchestrator"}' | jq .

# 3. Verify + domain retrieve
curl -s http://localhost:21337/api/v1/data/spdd-projection/stats | jq .
curl -s http://localhost:21337/api/v1/data/spdd-projection/work/SPIKE-001-guide-rag-context-backend | jq .
```

Orchestrator helpers:

```bash
./scripts/guide/append-orchestrator-context.sh
./scripts/guide/project-spdd-entities.sh
./scripts/guide/project-spdd-entities.sh examples/retrieval-fixture
```

## Chunk ↔ entity join

Same store, optional drill-down:

- Entity nodes carry `uri` pointing at source markdown (canvas / index fragment).
- Store API `findChunksForEntity(entityId)` can recover related `ContentElement` chunks when
  the RAG layer has linked them; projection HTTP does **not** yet expose this join.
- Hybrid mode (c): resolve WorkId subgraph (leg 3) → optionally broaden with leg 2 searches
  seeded by entity names / Work ID terms → justify retained chunks via edge or matched term.

## Re-ingest independence

| Change | Re-run |
|--------|--------|
| Files under `agent-context/memory/` (leg 2) | `append-ingest.sh` (git incremental) |
| Canvas or context-index structure (leg 3) | `POST …/spdd-projection/load` |
| Bad chunk set for one directory | leg 2 purge / git-revision reset |
| Reset leg 3 only | Re-load projection (merge-by-id); purge-by-label future |

## Implementation status

| Component | Status |
|-----------|--------|
| Guide `SpddMarkdownProjectionService` | Implemented on guide spike branch |
| Write API `POST …/load` | Implemented |
| Read API `GET …/stats`, `GET …/work/{workId}` | Implemented |
| Orchestrator `project-spdd-entities.sh` | Implemented |
| MCP domain traversal | T04 — gap (document + minimal fork) |
| Typed Kotlin `com.embabel.spdd.domain` | Deferred; `DynamicType` spike shortcut |

## Related

- Guide: `docs/spdd-projection-ingest.md`
- Schema: `spdd/analysis/SPIKE-001-dice-entity-schema.md`
- Leg 2 runbook: `docs/spike-guide-ingest-agent-context.md`
