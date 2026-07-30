# REASONS Canvas: FEAT-010-jira-compatible-requirements - Jira-compatible requirements format

## Metadata

- Work ID: FEAT-010-jira-compatible-requirements
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
- Delivery stage: make it right (planning artifacts)
- Related PR: (local on cursor/integration-981e)

## R - Requirements

### User Goal

Embed Jira metadata and dependency links in Markdown requirements with validation.

### Acceptance Criteria

- [x] Format specification documented
- [x] Requirement + milestone templates checked in
- [x] Validation script checks keys, Work ID refs, _milestone.yml presence
- [x] Analysis prompt extracts Jira context read-only
- [x] Migration guidance documented

### Non-Goals

- Recorded in the requirement file; respected at ship time.

### Assumptions

- Implementation landed before this canvas; canvas backfilled for dogfood completeness.

## E - Entities

### Application Components

- See Files Likely Affected.

### Files Likely Affected

- `docs/jira-compatible-requirements-format.md`
- `scripts/validate-requirements-format.sh`
- `templates/requirements/`

## A - Approach

### Proposed Approach

Implementation-first on `cursor/integration-981e`, then backfill this REASONS canvas
so Milestone 1 Linked Work has a governing contract for review/sync.

## S - Structure

Operations below match shipped increments.

## O - Operations

### T01 - Document format + templates

- Status: Complete
- Description: Spec + templates under templates/requirements/
- Files: docs/jira-compatible-requirements-format.md, templates/requirements/
- Tests: Not applicable
- Validation: Shipped

### T02 - Ship validate-requirements-format.sh

- Status: Complete
- Description: Format-only validator on init/upgrade
- Files: scripts/validate-requirements-format.sh
- Tests: manual/script smoke
- Validation: Shipped

### T03 - Wire create-work + analysis read-only

- Status: Complete
- Description: Frontmatter stubs + analysis extracts metadata
- Files: scripts/create-work-from-milestone.sh, analysis adapters
- Tests: validate-requirements-format.sh
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
