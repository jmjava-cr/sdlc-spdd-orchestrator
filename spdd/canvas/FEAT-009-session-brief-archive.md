# REASONS Canvas: FEAT-009-session-brief-archive - Session brief archive / rotation

## Metadata

- Work ID: FEAT-009-session-brief-archive
- Work Type: Feature
- Status: Complete
- Readiness: Reviewed — Complete (backfilled)
- Created: 2026-07-15
- Updated: 2026-07-15 (backfill after implementation-first ship)
- Target Project: sdlc-spdd-orchestrator (self / dogfood)
- Stack: Bash + Markdown
- Source System: Roadmap / issues
- Roadmap: ROADMAP.md
- Milestone: requirements/milestones/milestone-1/MILESTONE-1.md
- Delivery stage: make it right (session hygiene)
- Related PR: (local on cursor/integration-981e)

## R - Requirements

### User Goal

Rotate older timestamped session briefs into sessions/archive/ while keeping current-session.md.

### Acceptance Criteria

- [x] New session start creates timestamped brief + updates current-session.md
- [x] When timestamped briefs exceed the limit, oldest move to sessions/archive/
- [x] current-session.md is never archived
- [x] Omitting rotation (--no-session-rotate) preserves previous behavior
- [x] Test covers archive move (Test 21)

### Non-Goals

- Recorded in the requirement file; respected at ship time.

### Assumptions

- Implementation landed before this canvas; canvas backfilled for dogfood completeness.

## E - Entities

### Application Components

- See Files Likely Affected.

### Files Likely Affected

- `scripts/start-agent-session.sh`
- `tests/test-session-memory-index.sh`

## A - Approach

### Proposed Approach

Implementation-first on `cursor/integration-981e`, then backfill this REASONS canvas
so Milestone 1 Linked Work has a governing contract for review/sync.

## S - Structure

Operations below match shipped increments.

## O - Operations

### T01 - Rotate briefs in start-agent-session.sh

- Status: Complete
- Description: Default limit 20; --session-limit / --no-session-rotate
- Files: scripts/start-agent-session.sh
- Tests: tests/test-session-memory-index.sh Test 21
- Validation: Shipped

## N - Norms

- Ship-neutral for any templates/docs that leave this repo.
- Prefer specs → generate adapters over hand-editing adapters.

## S - Safeguards

- Do not invent scope beyond the requirement / origin issue.

## Review Checklist

- [x] Requirements satisfied
- [x] Operations completed
- [x] Tests added or updated
- [x] Documentation updated if needed

## Sync Notes

Backfilled 2026-07-15 after code landed. No further implementation drift known.

## Final Status

- Status: Complete
- Completed Date: 2026-07-15
- PR: (uncommitted on cursor/integration-981e unless requested)
- Follow-Up Tasks: None for this Work ID
