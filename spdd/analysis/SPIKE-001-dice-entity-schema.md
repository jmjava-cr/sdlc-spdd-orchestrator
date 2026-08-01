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
| **WorkId** | Work ID string as-is | Canvas metadata `- Work ID:` | `canvas` → Canvas; `area` → Area; `decision` → Decision; `pitfall` → Pitfall; `pattern` → Pattern |
| **Canvas** | `{workId}:canvas` | `spdd/canvas/<WorkID>.md` | — |
| **Area** | `area:{path}` | `context-index.md` Area column | — |
| **Operation** | `{workId}:{Tnn}` | Canvas Operations (not yet projected in spike loader) | `canvas` (planned) |
| **Decision** | `decision:{workId}:{area}:{source}` | context-index Kind=decision | `about` → Area |
| **Pitfall** | `pitfall:{workId}:{area}:{source}` | context-index Kind=pitfall | `about` → Area |
| **Pattern** | `pattern:{workId}:{area}:{source}` | context-index Kind=pattern | `about` → Area |

### Relationship types (property names)

| Rel type | From → To | Meaning |
|----------|-----------|---------|
| `canvas` | WorkId → Canvas | Work has this REASONS canvas |
| `area` | WorkId → Area | Work touched this code area (from index) |
| `decision` | WorkId → Decision | Work recorded this decision (2026-07-11) |
| `pitfall` | WorkId → Pitfall | Work recorded this pitfall (2026-07-11) |
| `pattern` | WorkId → Pattern | Work recorded this pattern (2026-07-11) |
| `about` | Decision/Pitfall/Pattern → Area | Lesson concerns this code area — enables **cross-run** lookup: "any prior work's lessons for area X" via incoming `about` edges (2026-07-11) |

Retrieval audit rule: an included entity must cite at least one of these edges (or a
matched lexical Work ID / Area term on leg 1). Cosine score alone is insufficient.

### Edge taxonomy roadmap (from agent-context data model)

Candidate edges present in the framework's artifact kinds but not yet projected:
`Session -for→ WorkId` (session briefs), `Keyword -covers→ Area/WorkId`
(`domain-index.md`), `Canvas -operation→ Operation` (Tnn sections),
`WorkId -depends-on→ WorkId` (canvas metadata), `WorkId -requirement/review→ …`
(feature workspace files). Highest-value next: **Keyword** — entry into the graph
by domain term before areas are known.

## Persist API (write)

| Surface | Path / entry | Behavior |
|---------|--------------|----------|
| Config | `guide.spdd-projection.enabled=true` | Activates beans |
| Config | `guide.spdd-projection.default-root-path` | Orchestrator or fixture root |
| Config | `guide.spdd-projection.allowed-roots` | Extra roots a load override may target; overrides outside default root + this list → HTTP 400 (hardening 2026-07-11) |
| HTTP | `POST /api/v1/data/spdd-projection/load` body `{"rootPath":"…"}` | Project canvases + context-index |
| Script | `scripts/guide/project-spdd-entities.sh [root]` | curl wrapper |

Loader: `SpddMarkdownProjectionService` → `save` + `mergeRelationship`. Re-running load
updates the same ids (merge-by-id). Hardening (2026-07-11): a malformed source file is
skipped (counted in `skippedFiles`) instead of failing the whole load; canvas files are
processed in sorted order; validation errors map to HTTP 400 (`{"error": …}`), feature
disabled to 409.

## Retrieve API (read)

| Surface | Status | Behavior |
|---------|--------|----------|
| `GET /api/v1/data/spdd-projection/stats` | **Implemented** | Counts by label (`WorkId`, `Canvas`, `Area`, `Decision`, `Pitfall`, `Pattern`) |
| `GET /api/v1/data/spdd-projection/work/{workId}` | **Implemented** | WorkId subgraph via `findRelated` (`canvas`, `area`, `decision`, `pitfall`, `pattern`) |
| `GET /api/v1/data/spdd-projection/area?name={area}` | **Implemented** (2026-07-11) | Cross-run lessons: incoming `about` + `area` edges — decisions/pitfalls/patterns from ANY Work ID for a code area |
| MCP entity / graph tools | **Implemented** (2026-07-11) | `spdd_workSubgraph`, `spdd_projectionStats`, `spdd_findByLabel`, `spdd_areaLessons` via `McpToolExport` + `@LlmTool`; errors return `{"error": …}` JSON |
| Chunk join by entity id | **Library exists** | `findChunksForEntity` on store; not exposed on projection API yet |

Read-side guards (2026-07-11): `findByLabel` accepts only schema labels and caps results
(default 50, max 200); blank workId/area → 400.

## Ingest mapping (sources)

| Source | Entities | Relationships |
|--------|----------|---------------|
| `spdd/canvas/<WorkID>.md` | WorkId, Canvas | WorkId —`canvas`→ Canvas |
| `agent-context/memory/context-index.md` | Area, Decision, Pitfall, Pattern | WorkId —`area`→ Area; WorkId —`decision`/`pitfall`/`pattern`→ lesson; lesson —`about`→ Area |

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

## Design verification (hardening pass, 2026-07-11)

Cross-check of implementation vs this contract, row by row:

| Contract row | Verified |
|--------------|----------|
| Join key = Work ID string | ✅ `subgraphForWorkId(workId)`, `findById(workId)` — id **is** the Work ID |
| Persist markdown → `__Entity__` | ✅ `saveEntity` sets `labels = {type, __Entity__}`; live Neo4j confirmed |
| Merge-by-id idempotency | ✅ unit test `load is idempotent` — reload does not duplicate |
| Retrieve = typed edge walk | ✅ `findRelated` only; no cosine in leg 3 read paths |
| Auditability | ✅ every subgraph/area-lessons member arrives via a named edge (`canvas`/`area`/`decision`/`pitfall`/`pattern`/`about`) |
| Not proposition pipeline | ✅ no `PropositionExtractor` usage |
| Label naming (no `Spdd*` prefix) | ✅ labels are `WorkId`, `Canvas`, `Area`, `Decision`, `Pitfall`, `Pattern` |
| Schema via `DataDictionary` | ✅ `SpddEntityDictionary` / `DataDictionary.fromClasses` (NamedEntity module) |

Test evidence: SPDD unit tests green in guide `com.embabel.guide.spdd`.

Known gaps (accepted for spike): Operation nodes not projected; Keyword/Session edges
not projected (see roadmap above); chunk↔entity join not exposed on the operator API.

## Status

**Implemented (guide spike):** Kotlin `NamedEntity` types in `com.embabel.guide.spdd.domain` +
`DataDictionary.fromClasses("sdlc-spdd", …)`. Persist still uses `SimpleNamedEntityData` with
`linkedDomainType` + `__Entity__` (Embabel merge-by-id path); schema is no longer `DynamicType`.

T02 schema path closed on guide branch `cursor/spike-spdd-dice-projection-17f4` (NamedEntity +
`fromClasses`). T03 projection loader + MCP `spdd_*` tools already on that branch; T06 go/no-go remains.
Hardening pass 2026-07-11: root-path allowlist, per-file error isolation, HTTP status
mapping, capped/validated reads, lesson edges (`decision`/`pitfall`/`pattern`/`about`),
cross-run area retrieval (`/area`, `spdd_areaLessons`).
