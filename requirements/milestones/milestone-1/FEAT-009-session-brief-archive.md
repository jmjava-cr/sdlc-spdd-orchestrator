---
work_id: "FEAT-009-session-brief-archive"
jira_key: ""
jira_epic: ""
jira_type: "Story"
**Status:** Complete
jira_assignee: ""
jira_due_date: ""
jira_sprint: ""
milestone: "milestone-1"
blocks: []
depends_on: []
related: []
---

# FEAT-009: Session Brief Archive / Rotation

**Work ID:** FEAT-009-session-brief-archive  
**Milestone:** Milestone 1 (Make it right)  
**Status:** Complete  
**Date:** 2026-07-15

## Summary

Keep `agent-context/sessions/` small by rotating older timestamped session briefs
into `agent-context/sessions/archive/`, while always preserving `current-session.md`.
Memory is already extracted at capture; briefs are handoff snapshots, not the
durable history.

## Source

- Roadmap: ROADMAP.md (make it right — session-brief archive/rotation)
- Milestone: requirements/milestones/milestone-1/MILESTONE-1.md

## Scope

### IN SCOPE

- Rotate timestamped `agent-context/sessions/*.md` (except `current-session.md`)
  into `archive/` when count exceeds a limit (default 20)
- Hook rotation into `start-agent-session.sh` after writing a new brief
- Optional `--session-limit` / `--no-session-rotate` flags
- Smoke test + short docs note

### NOT IN SCOPE

- Changing `session-history.md` rotation (already implemented in capture)
- Deleting archived briefs
- Changing current-session.md semantics

## Acceptance Criteria

- [x] New session start creates timestamped brief + updates `current-session.md`
- [x] When timestamped briefs exceed the limit, oldest move to `sessions/archive/`
- [x] `current-session.md` is never archived
- [x] Omitting rotation (`--no-session-rotate`) preserves previous behavior
- [x] Test covers archive move (`tests/test-session-memory-index.sh` Test 21)

**Status:** Complete

## Jira

- Key: TBD
- Issue type: Story
- Summary: Archive/rotate old agent-context/sessions briefs
- Labels: sdlc-spdd, sessions, make-it-right
