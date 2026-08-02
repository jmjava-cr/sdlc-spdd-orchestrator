# Analysis: SPIKE-001-guide-rag-context-backend

## Metadata

- **Work ID:** SPIKE-001-guide-rag-context-backend
- **Requirement:** `requirements/milestones/SPIKE-001-guide-rag-context-backend.md`
- **Canvas:** `spdd/canvas/SPIKE-001-guide-rag-context-backend.md`
- **Timestamp:** 2026-07-05T15:10:00Z
- **Branch policy:** T06 **provisional go** (2026-08-01); Guide #2 merged to `jmjava/guide` `main`.
- **Guide pin:** tag **`sdlc-spdd-projection-v1`** (`a6e3246` on `main`) — NamedEntity + neo4j profiles
- **PR:** #24 (spike) · #56 (integration → `main` for field dogfood)

## Domain Keywords

- Guide RAG / Embabel MCP
- agent-context store
- context-index / domain-index
- resolve-agent-context
- retrieval A/B
- DICE domain graph
- menke profiles
- git incremental ingest
- mock retrieval fixture
- prompt-optimization ledger (FEAT-004 stub)

## Code Areas

- `templates/guide-profiles/` — menke-5 profile template (spike branch only)
- `scripts/guide/` — append-ingest helper (spike branch only)
- `docs/spike-guide-ingest-agent-context.md` — operator runbook (orchestrator-only, not shipped)
- `spdd/analysis/` — this artifact + exploration log + dice entity schema
- `spdd/canvas/SPIKE-001-guide-rag-context-backend.md` — REASONS contract
- `agent-context/features/SPIKE-001-guide-rag-context-backend/` — feature workspace
- `examples/retrieval-fixture/` — **planned** mock project for scriptable A/B (T07)
- `tests/test-retrieval-fixture-resolver.sh` — **planned** gold-file baseline test (T07)

## Existing Concepts

### Markdown-first context path (baseline — mode A)

The default SDLC-SPDD workflow does **not** call Guide. Context loads via:

1. Tier-1 grounding (`.cursor/rules/sdlc-spdd.mdc`, etc.) — operating model only
2. `start-agent-session.sh` → `current-session.md` with **Resolved Context** from
   `resolve-agent-context.sh`
3. Index-filtered reads: `context-index.md`, `domain-index.md`, `phase-index.md`
4. `capture-session-memory.sh` + `index-spdd-analysis.sh` grow indexes at session end

This is the **control arm** for the experiment.

### Guide research path (candidate — modes B and C)

Framework contributors optionally connect embabel-dev MCP during `/sdlc-spdd-analysis`.
Guide ingests curated URLs and local directories into Neo4j; MCP exposes `docs_vectorSearch`
and `docs_textSearch`. Today this is **manual and orchestrator-only** — not installed into
target projects.

Confirmational research (2026-06-19): architecture sound; legs 1–2 work via MCP; leg 3
(`__Entity__`) requires custom DICE projection ingest.

### Spike branch scaffold (2026-07-05)

On `cursor/spike-guide-ingest-agent-context-17f4`:

- menke-5 profile template → orchestrator `agent-context/memory/`, `spdd/canvas/`, `spdd/analysis/`
- `append-orchestrator-context.sh` wrapper
- Exploration log template for MCP spot-checks

## New Concepts (this spike)

### Branch isolation

| Rule | Rationale |
|------|-----------|
| All spike artifacts on `cursor/spike-*` branches | Keeps markdown-first `main` clean; no accidental Guide dependency |
| Draft PR only; no merge until T06 go/no-go | Spike output is a **decision**, not shippable framework code |
| Operator docs marked orchestrator-only | Same posture as `guide-rag-research-and-dogfooding.md` |
| No installer / resolver / command template changes on spike branch until go | Safeguard from canvas |

### Three-mode experiment (T05)

Run the **same Work ID task** under controlled conditions:

| Mode | Retrieval source | How the agent gets context |
|------|------------------|----------------------------|
| **(a) Resolver** | Markdown indexes | `resolve-agent-context.sh` output in session brief; MCP disabled |
| **(b) Embedding** | Guide RAG leg 2 | MCP `docs_vectorSearch` / `docs_textSearch`; resolver discouraged |
| **(c) Hybrid** | Legs 1+2+3 | Resolver + MCP + DICE graph (after T03) |

**Scoreboard** (FEAT-004 ledger or stub until FEAT-004 lands):

- rework count (corrective prompt-update/sync cycles after Ready For Coding)
- review-result (`pass | fail | mixed | blocked`)
- approximate context tokens (files loaded × rough size)
- auditability: can each inclusion be explained by index row / domain link / matched term?

### Mock retrieval fixture (T07 — planned)

Dogfooding on the live orchestrator is noisy (large menke corpus, many Work IDs). A
**controlled mock project** makes the experiment reproducible:

```
examples/retrieval-fixture/
  requirements/fixture-requirement.md
  spdd/canvas/SPIKE-FIX-001-retrieval-fixture.md
  spdd/analysis/SPIKE-FIX-001-retrieval-fixture-analysis.md
  agent-context/memory/          # seeded indexes + decisions + pitfalls
  src/billing/                   # tiny code area referenced by analysis
```

**Automatable today (mode A):** `tests/test-retrieval-fixture-resolver.sh` diffs
`resolve-agent-context.sh` output against a gold TSV per query/work-id/phase.

**Local-only (mode B):** Guide profile `menke-fixture` ingests only the fixture tree;
MCP spot-check script compares chunk URIs to gold set.

**Manual (full session A/B):** same `/sdlc-spdd-code` operation on fixture, MCP on vs off,
ledger stub filled by human.

## Strategic Direction

1. **Document through SPDD flow** — requirement, canvas, this analysis, feature workspace,
   progress log. Operator runbook supplements analysis; does not replace it.
2. **T01 menke-5 ingest** — get orchestrator memory into Guide for real Work ID spot-checks.
3. **T07 mock fixture** — **complete** (`examples/retrieval-fixture/`, 15 gold assertions).
4. **T05 comparison** — run modes (a) and (b) on fixture first, then one real Work ID.
5. **T06 go/no-go** — if go, open separate FEAT on a new branch; merge spike docs/analysis
   to `main` only as research notes, not production wiring.

## Risks and Gaps

| Risk | Mitigation |
|------|------------|
| Spike work merges to `main` prematurely | Branch policy in canvas Safeguards; **all PRs stay draft** until T06; no merge to `main` |
| FEAT-004 ledger not built | Stub markdown scoreboard in exploration log for T05 |
| Guide/Neo4j not available in CI | Resolver gold-test in CI; MCP checks local-only |
| Small-sample A/B inconclusive | Treat as directional; fixture first for recall/precision |
| Leg 3 blocks full hybrid | Run (a) vs (b) first; add (c) when T03 lands |

## Recommendation

### T06 — Provisional go (field confirmation)

**Decision (2026-08-01): provisional GO.** Ship optional Guide DICE backend wiring to
`main` (integration PR #56) so operators can confirm retrieval quality live and iterate.
Markdown-first remains the default when Guide is absent (`CONTEXT_BACKEND=files`).

| Keep if field confirms | Rollback / no-go if field rejects |
|------------------------|-----------------------------------|
| Runtime-resolved `guide-dice` + `spdd_*` tools improve context vs files alone | Strip command Context Backend / `--with-guide` seams; keep console as experimental ops only |
| Ops console + projection/ingest stay useful dogfood | Leave Guide on spike branch; do not promote Guide #2 |

**Next:** dogfood on real Work IDs with Guide up (`./scripts/sdlc.sh console` + embabel-dev MCP);
update this section with keep/rollback after sessions.
