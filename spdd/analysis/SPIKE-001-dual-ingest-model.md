# SPIKE-001 — Dual ingest model (leg 2 RAG + leg 3 DICE projection)

Work ID: SPIKE-001-guide-rag-context-backend  
Branch pair:

| Repo | Branch |
|------|--------|
| `jmjava/sdlc-spdd-orchestrator` | `cursor/spike-guide-ingest-agent-context-17f4` |
| `jmjava/guide` | `cursor/spike-spdd-dice-projection-17f4` (base: `ingest-to-hub`) — **pushed** |

## Short answer: they coexist

Both ingests write to the **same Neo4j** store. They target **different node layers** and
serve **different retrieval legs**. Neither replaces the other.

| | Leg 2 — Guide RAG (current) | Leg 3 — SPDD projection (new) |
|---|------------------------------|-------------------------------|
| **Neo4j layer** | `ContentElement` chunks + embeddings | `__Entity__` + typed relationships |
| **Trigger** | `append-ingest.sh` / `load-references` | `POST /api/v1/data/spdd-projection/load` |
| **Config** | `guide.directories`, `guide.urls`, `guide.git-ingestion` | `guide.spdd-projection.enabled`, `default-root-path` |
| **Input** | Any files under configured directories | Structured SPDD markdown (canvas, context-index) |
| **Parser** | Tika + chunker + embed | Markdown → `SimpleNamedEntityData` + `mergeRelationship` |
| **MCP today** | `docs_vectorSearch`, `docs_textSearch` | Not yet — fork adds entity query tool (T04) |
| **Auditability** | Cosine / lexical on chunks | Typed edges (WorkId → Canvas → Area) |

## What leg 3 is NOT

| Path | Use for SPIKE-001 leg 3? |
|------|--------------------------|
| DICE **proposition pipeline** (conversation → propositions → graph) | **No** — unstructured text; wrong for REASONS canvases |
| Directory ingest alone | **No** — leaves `__Entity__` count at 0 (confirmed 2026-06-19) |
| Markdown `resolve-agent-context.sh` on orchestrator | **Baseline (mode a)** — separate from Guide; stays on `main` |

Leg 3 reuses **DICE entity conventions** (`NamedEntity`, `DataDictionary`, `__Entity__`
label) via **structured markdown projection**, not proposition extraction.

## Operator flow (both legs)

```bash
# 1. Guide on ingest-to-hub + menke-5 profile (leg 2 chunks)
cd ~/github/jmjava/guide
git checkout cursor/spike-spdd-dice-projection-17f4
# application-menke-5.yml + spdd-projection.enabled: true (see menke-5-spdd-projection example)
GUIDE_PROFILE=menke-5 ./scripts/append-ingest.sh

# 2. Leg 3 entity projection (same running Guide)
curl -s -X POST http://localhost:21337/api/v1/data/spdd-projection/load \
  -H 'Content-Type: application/json' \
  -d '{"rootPath":"~/github/jmjava/sdlc-spdd-orchestrator"}' | jq .

# 3. Verify __Entity__ populated
curl -s http://localhost:21337/api/v1/data/spdd-projection/stats | jq .
```

From orchestrator repo:

```bash
./scripts/guide/project-spdd-entities.sh
```

## Source → entity mapping (leg 3)

See `spdd/analysis/SPIKE-001-dice-entity-schema.md`. Implemented in guide
`SpddMarkdownProjectionService`:

| Markdown source | Entities | Relationships |
|-----------------|----------|---------------|
| `spdd/canvas/<WorkID>.md` | WorkId, Canvas | WorkId —canvas→ Canvas |
| `agent-context/memory/context-index.md` | Area, Decision, Pitfall | WorkId —area→ Area |

Markdown remains **source of truth**. Re-run leg 3 after `sdlc.sh capture` updates indexes.

## Re-ingest independence

| Change | Re-run |
|--------|--------|
| New/changed files in `agent-context/memory/` (leg 2) | `append-ingest.sh` (git incremental) |
| Canvas or context-index structure (leg 3) | `POST .../spdd-projection/load` |
| Bad chunk set for one directory | `purge` API (leg 2) — see guide `scripts/README.md` |
| Reset leg 3 only | Re-load projection; entity merge by id (future: purge by label) |

## Implementation status

| Component | Status |
|-----------|--------|
| Guide `SpddMarkdownProjectionService` | **Implemented** on guide spike branch |
| Guide operator API | `POST/GET /api/v1/data/spdd-projection/*` |
| Orchestrator fixture + mode (a) gold test | T07 complete |
| MCP entity traversal (leg 3) | T04 — fork follow-on |
| Full Kotlin `com.embabel.spdd.domain` module | T02/T03 hardening — DynamicType spike shortcut today |

## Related

- Guide: `docs/spdd-projection-ingest.md`
- Schema: `spdd/analysis/SPIKE-001-dice-entity-schema.md`
- Leg 2 runbook: `docs/spike-guide-ingest-agent-context.md`
