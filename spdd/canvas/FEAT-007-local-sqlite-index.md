# REASONS Canvas: FEAT-007-local-sqlite-index - Local SQLite index (pre-GUIDE)

## Metadata

- Work ID: FEAT-007-local-sqlite-index
- Work Type: Feature
- Status: Complete
- Readiness: Reviewed — Complete
- Created: 2026-07-27
- Updated: 2026-07-30 (REASONS section labels aligned for dogfood validate)
- Owner: framework
- Target Project: sdlc-spdd-orchestrator
- Stack: Python 3.11+ sqlite3 stdlib
- Source System: Local session / roadmap
- Roadmap: ROADMAP.md
- Milestone: milestone-1.md
- Related: SPIKE-001-guide-rag-context-backend (heavier successor)
- Related PR: https://github.com/jmjava/sdlc-spdd-orchestrator/pull/38

## R - Requirements

### User Goal

Query Work IDs, Jira keys, and artifact paths locally without installing Neo4j/GUIDE
or a database server — while keeping multi-user sync on git.

### Business / Product Goal

A lighter storage/query step before GUIDE. Prove stdlib SQLite as regenerable cache.

### Acceptance Criteria

- [x] Regenerable `.sdlc/index.sqlite` (gitignored)
- [x] `sdlc.sh db rebuild|status|query|export`
- [x] Docs + tests

## E - Entities

### Application Components

- `engine/src/sdlc_engine/db.py` — LocalIndex rebuild/query/export
- `scripts/sdlc.sh` — `db` subcommands
- Artifact: `.sdlc/index.sqlite` (gitignored)

### Files Likely Affected

- `engine/src/sdlc_engine/db.py`
- `engine/tests/test_db.py`
- `docs/local-sqlite-index.md`

## A - Approach

### Proposed Approach

Treat git markdown + `work-registry.tsv` as source of truth. Rebuild a local
SQLite cache on demand for FTS/query. GUIDE/Neo4j remains a later spike.

```
git artifacts → db rebuild → .sdlc/index.sqlite → db query / export
                                 │
                                 └── later: GUIDE/Neo4j (SPIKE-001)
```

## S - Structure

Index lives under `.sdlc/`; CLI under `sdlc.sh db …` routed to the Python engine.

## O - Operations

### T01 - Engine LocalIndex + CLI

- Status: Complete
- Description: `db.py`, CLI subcommands, `sdlc.sh` routing, pytest, docs.

## N - Norms

- Stdlib `sqlite3` only; optional FTS5 when available.
- Never commit the binary DB; optional JSON/SQL export for inspection.
- Multi-user sync stays on git.

## S - Safeguards

- Do not use SQLite as multi-writer shared store
- `db query` SQL is read-only SELECT only
- `.sdlc/` stays gitignored

## Review Checklist

- [x] Requirements satisfied
- [x] Operations completed
- [x] Tests added or updated
- [x] Documentation updated if needed

## Sync Notes

Merged via PR #38. Canvas section labels aligned 2026-07-30 for dogfood validate.

## Final Status

- Status: Complete
- Completed Date: 2026-07-27
- PR: https://github.com/jmjava/sdlc-spdd-orchestrator/pull/38
- Follow-Up Tasks: none for this Work ID (GUIDE is SPIKE-001)
