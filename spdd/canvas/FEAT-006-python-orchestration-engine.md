# REASONS Canvas: FEAT-006-python-orchestration-engine - Python orchestration engine (v2)

## Metadata

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

## Final Status

- Status: In Progress (T01–T04 scaffolding complete; broader script port pending)
