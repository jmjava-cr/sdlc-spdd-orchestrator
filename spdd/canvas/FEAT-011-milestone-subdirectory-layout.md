# REASONS Canvas: FEAT-011-milestone-subdirectory-layout - Milestone files in subdirectories

## Metadata

- Work ID: FEAT-011-milestone-subdirectory-layout
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
- Delivery stage: make it right (planning layout)
- Related PR: (local on cursor/integration-981e)

## R - Requirements

### User Goal

Prefer requirements/milestones/milestone-N/ while keeping root milestone-*.md working.

### Acceptance Criteria

- [x] Discovery prefers subdirectory milestone defs
- [x] Init/upgrade scaffold nested milestone-1
- [x] create-work writes stubs into the milestone directory
- [x] Migration doc shipped

### Non-Goals

- Recorded in the requirement file; respected at ship time.

### Assumptions

- Implementation landed before this canvas; canvas backfilled for dogfood completeness.

## E - Entities

### Application Components

- See Files Likely Affected.

### Files Likely Affected

- `scripts/lib/milestone.sh`
- `docs/MIGRATION-root-to-subdirectories.md`
- `requirements/milestones/milestone-1/`

## A - Approach

### Proposed Approach

Implementation-first on `cursor/integration-981e`, then backfill this REASONS canvas
so Milestone 1 Linked Work has a governing contract for review/sync.

## S - Structure

Operations below match shipped increments.

## O - Operations

### T01 - milestone.sh discovery helpers

- Status: Complete
- Description: Root + subdir; prefer subdir; warn on dual
- Files: scripts/lib/milestone.sh
- Tests: tests/test-scripts-lib.sh
- Validation: Shipped

### T02 - Init/upgrade + create-work paths

- Status: Complete
- Description: Nested scaffold and stub placement
- Files: scripts/init-project.sh, upgrade-project.sh, create-work-from-milestone.sh
- Tests: lib smoke
- Validation: Shipped

### T03 - Migration guidance

- Status: Complete
- Description: Root-to-subdir migration doc
- Files: docs/MIGRATION-root-to-subdirectories.md
- Tests: Not applicable
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
