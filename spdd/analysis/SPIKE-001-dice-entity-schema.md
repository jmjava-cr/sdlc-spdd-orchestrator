# SPIKE-001 — SDLC-SPDD DICE Entity Schema (contract)

Typed domain entities for **leg 3** (domain-graph persist + retrieve) over guide/Neo4j.
This is the DICE contract: structured domain objects as memory, retrieved by typed
structure — not the proposition-extraction pipeline, and not embedding-only context.

Related:

- Canvas: `spdd/canvas/SPIKE-001-guide-rag-context-backend.md`
- Dual ingest: `spdd/analysis/SPIKE-001-dual-ingest-model.md`
- Guide operator: `docs/spdd-projection-ingest.md` (guide repo)

## Contract summary

| Concern | Contract |
|---------|----------|
| **Join key** | Work ID string (`SPIKE-001-guide-rag-context-backend`, `FEAT-004-…`) |
| **Persist** | Markdown (source of truth) → projection load → `__Entity__` + typed relationships |
| **Retrieve** | Walk edges from WorkId / Area / Canvas; explain inclusions via relationship type |
| **Idempotency** | Merge-by-id: `NamedEntityDataRepository.save(id=…)` + `mergeRelationship` |
| **Not in scope** | DICE proposition pipeline (`PropositionExtractor` → conversation graph) |

## Embabel convention alignment

| Embabel convention | Source | Our design |
|--------------------|--------|------------|
| Entities carry `id`, `name`, `description` | `NamedEntity` / `NamedEntityData` | ✅ All projected nodes |
| Neo4j label = type simple name + `__Entity__` | `NamedEntityData.ENTITY_LABEL` | ✅ `WorkId`, `Canvas`, … |
| Schema via `DataDictionary` | `DataDictionary.fromDomainTypes` / `fromClasses` | ✅ `SpddEntityDictionary` (spike: `DynamicType`) |
| Relationships via property / predicate names | `@Semantics` → Neo4j rel type | ✅ Rel types `canvas`, `area` |
| Persist via repository | `NamedEntityDataRepository` | ✅ Not raw Cypher; not propositions |
| Chunk join (optional) | `DrivineStore.findChunksForEntity(id)` | ⚠️ Available in store API; not yet wired to projection HTTP/MCP |

**Label naming:** no `Spdd*` prefix on Neo4j labels. Namespace via package / dictionary name
`sdlc-spdd`.

## Entity types

Spike implementation uses `SimpleNamedEntityData` + labels. Target module (post-spike):
`com.embabel.spdd.domain` Kotlin `NamedEntity` classes.

| Type | `id` rule | Produced from | Outgoing rels |
|------|-----------|---------------|---------------|
| **WorkId** | Work ID string as-is | Canvas metadata `- Work ID:` | `canvas` → Canvas; `area` → Area |
| **Canvas** | `{workId}:canvas` | `spdd/canvas/<WorkID>.md` | — |
| **Area** | `area:{path}` | `context-index.md` Area column | — |
| **Operation** | `{workId}:{Tnn}` | Canvas Operations (not yet projected in spike loader) | `canvas` (planned) |
| **Decision** | `decision:{workId}:{area}:{source}` | context-index Kind=decision | planned: `area`, `workId` |
| **Pitfall** | `pitfall:{workId}:{area}:{source}` | context-index Kind=pitfall | planned |
| **Pattern** | `pattern:{workId}:{area}:{source}` | context-index Kind=pattern | planned |

### Relationship types (property names)

| Rel type | From → To | Meaning |
|----------|-----------|---------|
| `canvas` | WorkId → Canvas | Work has this REASONS canvas |
| `area` | WorkId → Area | Work touched this code area (from index) |

Retrieval audit rule: an included entity must cite at least one of these edges (or a
matched lexical Work ID / Area term on leg 1). Cosine score alone is insufficient.

## Persist API (write)

| Surface | Path / entry | Behavior |
|---------|--------------|----------|
| Config | `guide.spdd-projection.enabled=true` | Activates beans |
| Config | `guide.spdd-projection.default-root-path` | Orchestrator or fixture root |
| HTTP | `POST /api/v1/data/spdd-projection/load` body `{"rootPath":"…"}` | Project canvases + context-index |
| Script | `scripts/guide/project-spdd-entities.sh [root]` | curl wrapper |

Loader: `SpddMarkdownProjectionService` → `save` + `mergeRelationship`. Re-running load
updates the same ids (merge-by-id).

## Retrieve API (read)

| Surface | Status | Behavior |
|---------|--------|----------|
| `GET /api/v1/data/spdd-projection/stats` | **Implemented** | Counts by label (`WorkId`, `Canvas`, `Area`) |
| `GET /api/v1/data/spdd-projection/work/{workId}` | **Implemented** | WorkId subgraph via `findRelated` (`canvas`, `area`) |
| MCP entity / graph tools | **T04 gap** | Guide MCP today: `docs_*` only (chunks). Fork needed to expose domain query |
| Chunk join by entity id | **Library exists** | `findChunksForEntity` on store; not exposed on projection API yet |

## Ingest mapping (sources)

| Source | Entities | Relationships |
|--------|----------|---------------|
| `spdd/canvas/<WorkID>.md` | WorkId, Canvas | WorkId —`canvas`→ Canvas |
| `agent-context/memory/context-index.md` | Area, Decision, Pitfall | WorkId —`area`→ Area |

Leg 2 (RAG chunks) remains independent: `guide.directories` + append-ingest.

## Spike validation

- [x] Schema aligned with Embabel `__Entity__` / repository conventions
- [x] Projection load on live Neo4j → `__Entity__` > 0
      (2026-07-11, :21337, `project-spdd-entities.sh` → 9 WorkId, 9 Canvas, 12 Area,
      21 relationships; stats endpoint confirms `entityLabel: __Entity__`)
- [x] Typed-edge retrieval by Work ID on live Neo4j — Cypher walk
      `MATCH (w:WorkId)-[r]->(x)` returns `canvas` edges for all 9 WorkIds and `area`
      edges for WorkIds whose analysis declares code areas (CHORE-001: 5, CHORE-002: 7).
- [x] `GET …/work/SPIKE-001-guide-rag-context-backend` → HTTP 200 with WorkId + canvas
      neighbor summaries (2026-07-11; endpoint added to the security permit list after
      the first live call returned 403).
- [ ] Hybrid retrieval auditability vs embedding-only (T05 — mode (a) rows captured;
      mode (b) pending MCP spot-checks)

## Status

Contract formalized 2026-07-11. Spike loader uses `DynamicType` + `SimpleNamedEntityData`;
promote to typed Kotlin `NamedEntity` module if T06 says go.
