# REASONS Canvas: FEAT-006-python-orchestration-engine - Python orchestration engine (v2)

## Metadata

- Source URL: https://github.com/jmjava/sdlc-spdd-orchestrator/pull/31
- Source Issue: #31
- Source System: GitHub
- Work ID: FEAT-006-python-orchestration-engine
- Work Type: Feature
- Status: In Progress
- Created: 2026-07-27
- Updated: 2026-07-27
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

## E - Essentials

- Stdlib-first Python package `sdlc_engine`
- CLI parity for next/claim/shelf/advance/archive/team/list-work/status
- Shell wrapper `scripts/sdlc.sh` delegates via `SDLC_ENGINE=auto|python|shell`
- Pytest coverage for pointer/workflow/registry/archive/cli
- Docs: `docs/engine-v2.md`, `engine/README.md`

## A - Architecture

```
sdlc.sh (compat) --> sdlc_engine.cli --> workflow/registry/archive/pointer
                              \--> shell bridge for remaining scripts/*.sh
```

On-disk formats unchanged: `.sdlc/pointer`, `.sdlc/workflows/*.state`,
`agent-context/work-registry.tsv`, `spdd/canvas/`.

## S - Safeguards

- Do not break bash-only installs (`SDLC_ENGINE=shell`)
- Do not ship posture language into target templates
- Keep milestone files in place when archiving

## Operations

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
- Description: `links`, `sync-links --repair`, `sync-roadmap`, `issues draft|push|pull`; claim auto-reads Jira/GitHub from milestone requirements; Linked Work status repair.

### T06 - Local/offline work sessions

- Status: Complete
- Description: `LOCAL-*` sessions under `.sdlc/local-sessions/`; `local start|list|capture|shelf|resume|promote|abandon`; claim refuses LOCAL; `next` surfaces offline work until promoted into a documented Work ID.

## Final Status

- Status: In Progress (T01–T06 complete; capture/resolve port still pending)
