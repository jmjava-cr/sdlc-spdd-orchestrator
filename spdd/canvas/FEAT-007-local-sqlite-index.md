# REASONS Canvas: FEAT-007-local-sqlite-index - Local SQLite index (pre-GUIDE)

## Metadata

- Work ID: FEAT-007-local-sqlite-index
- Work Type: Feature
- Status: Ready For Coding
- Created: 2026-07-27
- Updated: 2026-07-27
- Owner: framework
- Target Project: sdlc-spdd-orchestrator
- Stack: Python 3.11+ sqlite3 stdlib
- Source System: Local session / roadmap
- Roadmap: ROADMAP.md
- Milestone: milestone-1.md
- Related: SPIKE-001-guide-rag-context-backend (heavier successor)

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

## E - Essentials

- Stdlib `sqlite3` only
- Source of truth remains markdown + `work-registry.tsv`
- Never commit the binary DB; optional JSON/SQL export for inspection
- FTS5 when available

## A - Architecture

```
git artifacts → db rebuild → .sdlc/index.sqlite → db query / export
                                 │
                                 └── later: GUIDE/Neo4j (SPIKE-001)
```

## S - Safeguards

- Do not use SQLite as multi-writer shared store
- `db query` SQL is read-only SELECT only
- `.sdlc/` stays gitignored

## Operations

### T01 - Engine LocalIndex + CLI

- Status: Complete
- Description: `db.py`, CLI subcommands, `sdlc.sh` routing, pytest, docs.

## Final Status

- Status: Complete
