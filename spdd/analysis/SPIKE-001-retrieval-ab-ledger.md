# SPIKE-001 — Retrieval A/B ledger (stub until FEAT-004)

Work ID: SPIKE-001-guide-rag-context-backend  
Fixture Work ID: SPIKE-FIX-001-retrieval-fixture  
Branch: `cursor/spike-guide-ingest-agent-context-17f4` (draft PR #24)

Records mode comparisons for T05. FEAT-004 will replace this with
`agent-context/memory/prompt-optimization-log.md`; until then, append rows here.

## Modes

| Mode | Label | Retrieval source |
|------|-------|------------------|
| (a) | resolver | `resolve-agent-context.sh` + markdown indexes |
| (b) | embedding | Guide MCP `docs_vectorSearch` / `docs_textSearch` |
| (c) | hybrid | resolver + MCP + DICE graph (after T03) |

## Scoring columns

| Column | How to measure |
|--------|----------------|
| context_paths | Count of distinct file paths loaded |
| context_bytes | Sum of file sizes for resolved paths (proxy for tokens) |
| auditability | `pass` if every inclusion explainable by index row / domain link / matched term |
| rework | Corrective prompt-update/sync cycles after Ready For Coding (0 for fixture drill) |
| review_result | `pass \| fail \| mixed \| blocked` |
| notes | Free text |

## Fixture drill rows (T05 — fill after runs)

| date | fixture_case | mode | context_paths | context_bytes | auditability | review_result | rework | notes |
|------|--------------|------|---------------|---------------|--------------|---------------|--------|-------|
| 2026-07-11 | code+work-id (C01) | (a) resolver | 6 | 2579 | pass | pass | 0 | auto: `run-retrieval-ab-fixture.sh --capture-a`; every path from index row / Work ID artifact chain |
| | code+work-id (C01) | (b) embedding | | | | | 0 | MCP on; record via `--check-mcp` |
| 2026-07-11 | analysis+work-id (C02) | (a) resolver | 8 | 4026 | pass | pass | 0 | Fowler index trio + Work ID artifacts; all explainable by phase budget rows |
| | analysis+work-id (C02) | (b) embedding | | | | | 0 | |
| 2026-07-11 | areas-only code (C03) | (a) resolver | 2 | 311 | pass | pass | 0 | area-scoped only; no Work ID artifacts pulled |
| | areas-only code (C03) | (b) embedding | | | | | 0 | |

## Orchestrator Work ID rows (after fixture — optional)

| date | work_id | mode | context_paths | context_bytes | auditability | review_result | rework | notes |
|------|---------|------|---------------|---------------|--------------|---------------|--------|-------|
| | SPIKE-001-guide-rag-context-backend | (a) | | | | | | real session |
| 2026-07-11 | SPIKE-001-guide-rag-context-backend | (b) | 5 chunks | ~6 KB | mixed | pass | 0 | live MCP spot-check (below) |
| 2026-07-11 | SPIKE-001-guide-rag-context-backend | (c) leg 3 | 2 entities | <1 KB | pass | pass | 0 | `GET …/work/{workId}` → WorkId + canvas via typed edge |

### 2026-07-11 live MCP spot-check (mode (b) vs leg 3 domain read)

Store: menke-5 append corpus (24.9k `ContentElement`) + SPDD projection (30 `__Entity__`).

- `docs_textSearch` `"SPIKE-001" +DICE +retrieval` (topK 5): top hits are the spike's own
  canvas/analysis chunks (scores 1.0–0.83) — good, but inclusion is justified only by
  similarity score.
- `docs_vectorSearch` "How is the SPDD entity projection retrieved by Work ID…" (topK 5):
  the schema-doc chunk ranks 0.76 **tied with** unrelated Embabel framework source about
  `ProjectedRelationship`/`GraphProjector` — embedding-only cannot distinguish the
  project's contract from framework docs about similar concepts → `auditability: mixed`.
- Leg 3 domain read for the same Work ID returns exactly the WorkId node + its canvas
  neighbor, each inclusion explained by a typed `canvas` edge → `auditability: pass`.

Takeaway for T06: embedding leg is a good discovery layer; the domain graph is what makes
inclusions explainable and tightly scoped.

## Decision (T06 — pending)

_go / no-go / defer — rationale here after fixture + optional real Work ID runs._
