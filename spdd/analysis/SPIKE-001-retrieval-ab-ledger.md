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
| | code+work-id | (a) resolver | | | | | 0 | auto: `./scripts/guide/run-retrieval-ab-fixture.sh --capture-a` |
| | code+work-id | (b) embedding | | | | | 0 | MCP on; record via `--check-mcp` |
| | analysis+work-id | (a) resolver | | | | | 0 | |
| | analysis+work-id | (b) embedding | | | | | 0 | |
| | areas-only code | (a) resolver | | | | | 0 | |
| | areas-only code | (b) embedding | | | | | 0 | |

## Orchestrator Work ID rows (after fixture — optional)

| date | work_id | mode | context_paths | context_bytes | auditability | review_result | rework | notes |
|------|---------|------|---------------|---------------|--------------|---------------|--------|-------|
| | SPIKE-001-guide-rag-context-backend | (a) | | | | | | real session |
| | SPIKE-001-guide-rag-context-backend | (b) | | | | | | MCP enabled |

## Decision (T06 — pending)

_go / no-go / defer — rationale here after fixture + optional real Work ID runs._
