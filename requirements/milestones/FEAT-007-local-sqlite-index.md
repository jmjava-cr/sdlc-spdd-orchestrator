# Requirement: FEAT-007-local-sqlite-index

## Summary

Add a regenerable local SQLite index (stdlib `sqlite3`, no DB server) as a
lightweight query cache before GUIDE/Neo4j. Multi-user sync remains git.

## Acceptance Criteria

- [x] `.sdlc/index.sqlite` rebuilt from canvases, milestone requirements, registry, local sessions
- [x] CLI: `db rebuild|status|path|query|export` via `sdlc.sh` (Python engine even when shell default)
- [x] Read-only SQL + FTS5/LIKE search; JSON/SQL export
- [x] Docs: `docs/local-sqlite-index.md`
- [x] Pytest coverage

## Jira

- Key: TBD
- Issue type: Story
- Summary: Local SQLite index before GUIDE
- Labels: sdlc-spdd, feature

### Description

Zero-install SQLite query cache under `.sdlc/` for Work ID metadata. Not a shared
live database — each machine rebuilds after git sync. Precursor to SPIKE-001 GUIDE.

### Acceptance criteria (Given/When/Then)

- Given repo artifacts on disk
- When `db rebuild` runs
- Then `.sdlc/index.sqlite` lists work items with registry/Jira/canvas fields
- Given `db query --search …`
- When FTS5 is available
- Then matching Work IDs are returned without scanning markdown by hand

## GitHub

- Number: TBD
- Title: FEAT-007: Local SQLite index (pre-GUIDE)
- Labels: feature
- URL:
