# Local SQLite index (pre-GUIDE)

Lightweight, **zero-install** query cache for Work IDs and artifacts. Uses Python’s
stdlib `sqlite3` — no database server.

## What it is / is not

| Is | Is not |
|----|--------|
| Regenerable index under `.sdlc/index.sqlite` (gitignored) | A multi-user live shared database |
| Fast local `SELECT` / full-text over canvases + registry | A replacement for GUIDE/Neo4j RAG |
| Optional JSON/SQL export for inspection | Something you commit and merge as a binary |

**Multi-user sync stays git:** `work-registry.tsv`, canvases, milestone requirements.
Each machine rebuilds its own SQLite file after pull/claim.

This is the intended step **before** GUIDE (Embabel Guide + Neo4j): same questions,
cheaper substrate; swap the backend later if SPIKE-001 goes ahead.

## Commands

Always routed to the Python engine (even when `SDLC_ENGINE=shell`):

```bash
./scripts/sdlc.sh db rebuild
./scripts/sdlc.sh db status
./scripts/sdlc.sh db path

./scripts/sdlc.sh db query --columns work_id,registry_status,jira_key,canvas_status
./scripts/sdlc.sh db query --status done --limit 20
./scripts/sdlc.sh db query --search "orchestration"
./scripts/sdlc.sh db query "SELECT work_id, jira_key FROM work_items WHERE has_canvas = 1"

./scripts/sdlc.sh db export --format json -o /tmp/sdlc-index.json
./scripts/sdlc.sh db export --format sql  -o /tmp/sdlc-index.sql
```

`db query` with raw SQL is **read-only** (single `SELECT` only).

## Schema (v1)

- `work_items` — one row per Work ID (title, statuses, Jira/GitHub, paths, registry)
- `artifacts` — canvas / requirement / feature / analysis / review / sync paths
- `local_sessions` — machine-private `LOCAL-*` sessions under `.sdlc/local-sessions/`
- `work_search` — FTS5 when available (else LIKE fallback)
- `meta` — schema version, rebuild time, source git commit

## Relationship to GUIDE

```
markdown + TSV (git, source of truth)
        │
        ▼ rebuild
  .sdlc/index.sqlite   ← you are here (local cache)
        │
        ▼ later (SPIKE-001)
  GUIDE / Neo4j        ← optional RAG / graph retrieval
```

Do not treat the SQLite file as authoritative. If it drifts, `db rebuild`.
