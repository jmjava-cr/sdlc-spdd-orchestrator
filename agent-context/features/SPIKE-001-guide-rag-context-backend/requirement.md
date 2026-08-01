# Requirement: SPIKE-001-guide-rag-context-backend

## Summary

Time-boxed feasibility spike: evaluate Embabel **guide** (RAG MCP over Neo4j) as an
*optional* retrieval backend versus today's markdown `context-index.md` +
`resolve-agent-context.sh` resolver.

## Source

- `requirements/milestones/SPIKE-001-guide-rag-context-backend.md`
- Analysis: `spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md`
- Canvas: `spdd/canvas/SPIKE-001-guide-rag-context-backend.md`

## Branch policy

**All work for this spike stays off `main`.** Active branch:

    cursor/spike-guide-ingest-agent-context-17f4

Draft PR #24. **Keep PR draft** until T06 go/no-go — do not mark ready for review or merge.
The markdown-first default path on `main` must remain unchanged during the experiment.

## Question to answer

Does Guide RAG retrieval measurably improve outcomes (rework, review-result, context
tokens, auditability) versus the markdown resolver — enough to justify an optional
JVM + Neo4j dependency?

## Success criteria

See canvas Decision Criteria and milestone requirement. Key gates:

- [ ] menke-5 ingest + MCP spot-checks (T01)
- [ ] Mock retrieval fixture + resolver gold test (T07)
- [ ] A/B on fixture then one real Work ID (T05)
- [ ] Go/no-go written (T06)

## Non-Goals

- No production wiring on `main`
- No installer or command template changes until go/no-go
- No target-project shipment of Guide profiles or Neo4j data
