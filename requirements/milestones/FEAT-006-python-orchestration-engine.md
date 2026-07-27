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
- [x] Milestone↔Jira/GitHub sync: `links`, `sync-links`, `issues draft|push|pull`, claim auto-link
- [x] Local/offline sessions: `local start|list|capture|shelf|resume|promote|abandon` (`LOCAL-*`)
- [ ] Later: port capture/resolve helpers; optional install into target projects

## Jira

- Key: TBD
- Issue type: Story
- Summary: Python orchestration engine v2
- Labels: sdlc-spdd, feature

### Description

Introduce a Python orchestration engine (v2) so SDLC-SPDD workflow control is
reusable beyond bash scripts, while preserving shell compatibility and on-disk
artifact contracts. Includes milestone↔Jira/GitHub sync with **ADF** descriptions
for Jira Cloud.

### Business value

Agents and humans can push well-formatted Jira issues from milestone requirements
without hand-converting markdown, and keep Linked Work / canvas Source in sync.

### Acceptance criteria (Given/When/Then)

- Given a filled `## Jira` section on a milestone requirement
- When `issues push --system jira --apply` runs against Jira Cloud
- Then the issue description is ADF with headings, lists, and marks (not a raw markdown blob)
- Given `issues draft --format adf`
- When an engineer reviews the payload
- Then they can see the exact ADF JSON before applying

## GitHub

- Number: 31
- Title: FEAT-006: Python orchestration engine v2
- Labels: feature
- URL: https://github.com/jmjava/sdlc-spdd-orchestrator/pull/31
