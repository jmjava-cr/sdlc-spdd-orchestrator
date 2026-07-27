# Requirement: FEAT-006-python-orchestration-engine

## Summary

Introduce a Python orchestration engine (v2) so SDLC-SPDD workflow control is
reusable beyond bash scripts, while preserving shell compatibility and on-disk
artifact contracts.

## Acceptance Criteria

- [x] `engine/` package importable as `sdlc_engine`
- [x] CLI supports next/claim/shelf/advance/archive/team/list-work/status/pointer
- [x] `scripts/sdlc.sh` can delegate via `SDLC_ENGINE=auto|python|shell`
- [x] Pytest coverage for core modules
- [x] Docs under `docs/engine-v2.md` and `engine/README.md`
- [ ] Later: port capture/resolve helpers; optional install into target projects

## Jira

- Key: TBD
- Summary: Python orchestration engine v2
