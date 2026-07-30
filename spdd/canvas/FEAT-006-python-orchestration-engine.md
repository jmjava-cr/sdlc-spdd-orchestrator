# REASONS Canvas: FEAT-006-python-orchestration-engine - Python orchestration engine (v2)

## Metadata

- Source URL: https://github.com/jmjava/sdlc-spdd-orchestrator/pull/31
- Source Issue: #31
- Source System: GitHub
- Work ID: FEAT-006-python-orchestration-engine
- Work Type: Feature
- Status: Complete
- Readiness: Reviewed — Complete
- Created: 2026-07-27
- Updated: 2026-07-30 (REASONS section labels aligned for dogfood validate)
- Owner: framework
- Target Project: sdlc-spdd-orchestrator
- Stack: Python 3.11+
- Roadmap: ROADMAP.md
- Milestone: milestone-1.md

## R - Requirements

### User Goal

Move orchestration from bash-only scripts to a reusable Python engine that can
drive the SDLC-SPDD workflow while keeping shell compatibility.

### Business / Product Goal

Make the framework embeddable, testable, and easier to extend without rewriting
assistant adapters or on-disk artifact contracts.

### Acceptance Criteria

- [x] Stdlib-first Python package `sdlc_engine`
- [x] CLI parity for next/claim/shelf/advance/archive/team/list-work/status
- [x] Shell wrapper `scripts/sdlc.sh` delegates via `SDLC_ENGINE=auto|python|shell`
- [x] Local/offline `LOCAL-*` sessions + promote into documented Work IDs
- [x] Pytest coverage for pointer/workflow/registry/archive/cli/local sessions
- [x] Docs: `docs/engine-v2.md`, `engine/README.md`

## E - Entities

### Application Components

- `engine/src/sdlc_engine/` — project/phases/pointer/workflow/registry/archive/canvas/cli/issues/db/local_sessions
- `scripts/sdlc.sh` — engine selection shim
- On-disk: `.sdlc/pointer`, `.sdlc/workflows/*.state`, `agent-context/work-registry.tsv`, `spdd/canvas/`

### Files Likely Affected

- `engine/**`
- `scripts/sdlc.sh`
- `docs/engine-v2.md`
- `.github/workflows/test-sdlc-engine.yml`

## A - Approach

### Proposed Approach

Ship a Python package beside existing bash scripts. Default `SDLC_ENGINE=auto`
prefers Python when importable; `shell` preserves bash-only installs. On-disk
artifact contracts stay unchanged so adapters and capture paths keep working.

```
sdlc.sh (compat) --> sdlc_engine.cli --> workflow/registry/archive/pointer
                              \--> shell bridge for remaining scripts/*.sh
```

## S - Structure

Package under `engine/` with CLI entrypoints; shell remains the public UX for
most operators. Milestone/Jira/GitHub sync and LOCAL sessions extend the same CLI.

## O - Operations

### T01 - Scaffold package + core modules

- Status: Complete
- Description: Create `engine/` package with project/phases/pointer/workflow/registry/archive/canvas/cli.

### T02 - Shell compatibility shim

- Status: Complete
- Description: Update `scripts/sdlc.sh` to prefer Python engine when importable.

### T03 - Tests + CI

- Status: Complete
- Description: Pytest suite + GitHub Actions workflow.

### T04 - Docs + roadmap linkage

- Status: Complete
- Description: engine-v2 docs, canvas, milestone/roadmap notes.

### T05 - Milestone / Jira / GitHub sync usability

- Status: Complete
- Description: `links`, `sync-links --repair`, `sync-roadmap`, `issues draft|push|pull`; claim auto-reads Jira/GitHub from milestone requirements; Linked Work status repair; Jira Cloud descriptions via markdown→ADF (`jira_format`).

### T06 - Local/offline work sessions

- Status: Complete
- Description: `LOCAL-*` sessions under `.sdlc/local-sessions/`; `local start|list|capture|shelf|resume|promote|abandon`; claim refuses LOCAL; `next` surfaces offline work until promoted into a documented Work ID.

## N - Norms

- Prefer stdlib-first Python; keep bash fallback.
- Do not change on-disk artifact contracts without a migration Work ID.
- Ship-neutral: no make-it-work/right/fast posture language in templates.

## S - Safeguards

- Do not break bash-only installs (`SDLC_ENGINE=shell`)
- Do not ship posture language into target templates
- Keep milestone files in place when archiving

## Review Checklist

- [x] Requirements satisfied
- [x] Entities updated correctly
- [x] Approach followed or synced
- [x] Structure followed or synced
- [x] Operations completed
- [x] Norms followed
- [x] Safeguards respected
- [x] Tests added or updated
- [x] Documentation updated if needed

## Sync Notes

Merged via PR #31. Canvas section labels aligned 2026-07-30 so dogfood
`validate-reasons-canvas.sh spdd/canvas` passes. Capture/resolve port may remain
follow-up outside this Work ID's closed ops.

## Final Status

- Status: Complete
- Completed Date: 2026-07-27
- PR: https://github.com/jmjava/sdlc-spdd-orchestrator/pull/31
- Follow-Up Tasks: optional further bash→Python ports
