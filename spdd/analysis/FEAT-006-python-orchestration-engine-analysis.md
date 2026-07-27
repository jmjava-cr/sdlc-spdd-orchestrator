# Analysis: FEAT-006-python-orchestration-engine

## Scope

Replace bash-centric orchestration with a Python engine for reuse, without
breaking existing installs or artifact layouts.

## Current state (v1)

| Concern | Location |
|---------|----------|
| CLI entry | `scripts/sdlc.sh` |
| Pointer | `agent-context/sdlc-pointer.sh` |
| Workflow | `agent-context/sdlc-workflow.sh` |
| Team registry | `agent-context/sdlc-team-registry.sh` |
| Session/install helpers | `scripts/*.sh` |

## Target state (v2)

| Concern | Location |
|---------|----------|
| Importable API + CLI | `engine/src/sdlc_engine/` |
| Compat wrapper | `scripts/sdlc.sh` (`SDLC_ENGINE`) |
| Remaining install/adapters | shell (bridged via `sdlc-engine shell`) |

## Risks

- Dual implementation drift (Python vs bash) — mitigate with shared on-disk
  contracts + pytest + existing bash harnesses still green under `SDLC_ENGINE=shell`
- Target projects without Python — keep shell path default-capable via `auto`
  fallback

## Code Areas

- `engine/src/sdlc_engine/`
- `scripts/sdlc.sh`
- `docs/engine-v2.md`
