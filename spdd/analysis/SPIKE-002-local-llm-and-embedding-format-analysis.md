# Analysis: SPIKE-002-local-llm-and-embedding-format

**Work ID:** SPIKE-002-local-llm-and-embedding-format  
**Date:** 2026-07-15  
**Phase:** analysis (resume after FEAT-004/005 scoreboard landed)  
**Related research:** `spdd/analysis/SPIKE-002-local-llm-and-embedding-format-research.md`  
**Sibling:** SPIKE-001 (shared Guide substrate + A/B method)

---

## Domain Keywords

- Ollama
- local LLM
- embedding
- nomic-embed-text
- all-MiniLM-L6-v2
- guide
- FEAT-004 ledger

## Code Areas

- (external) embabel guide UserModelFactory / application.yml
- (external) Ollama
- agent-context/memory/prompt-optimization-log.md

## Scope Lock

### IN SCOPE

- Confirm scoreboard readiness (FEAT-004/005)
- Sequence relative to SPIKE-001 (share harness; do not block SPIKE-001 T01)
- Interim recommendation under current environment constraints

### NOT IN SCOPE

- Making local models the default for target projects
- Exhaustive model benchmarks
- Orchestrator framework changes

### Reference-only

- Confirmational research 2026-06-19 (two knobs; re-embed cost; Ollama autoconfig)
- SPIKE-001 analysis for shared A/B method

---

## Findings (2026-07-15)

| Gate | Status |
|------|--------|
| FEAT-004 ledger | ✅ Complete |
| Guide MCP / Ollama agentic smoke | ❌ Guide MCP not connected; local LLM verification blocked |
| Embedding A/B | ⏳ Needs Guide + re-ingest harness |
| Cost/latency table | ⏳ Pending T05 |

### Interim recommendation (not final)

- Prefer `embabel-agent-ollama-autoconfigure` before forking `UserModelFactory`.
- Keep 384-dim ONNX as baseline until A/B proves 768-dim gain after isolating chunking.
- **Production default:** stay hosted/baseline until T02–T06 evidence exists.
- Run SPIKE-002 after SPIKE-001 T01 ingest is healthy (shared store).

### Unblock checklist

1. Guide MCP up + Ollama serving a tool-capable model.
2. T01–T02: local LLM smoke (tool calls + structured output).
3. T03–T05: embedding swap subset + A/B + cost table.
4. T06: go/no-go + recommended default.

### Next command (when Guide + Ollama are up)

```
./scripts/sdlc.sh claim SPIKE-002-local-llm-and-embedding-format
./scripts/sdlc.sh resume SPIKE-002-local-llm-and-embedding-format --phase code
/sdlc-spdd-code @spdd/canvas/SPIKE-002-local-llm-and-embedding-format.md operation T01
```
