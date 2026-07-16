# REASONS Canvas: FEAT-006-analysis-scope-lock - Analysis Phase Scope Lock-In

## Metadata

- Work ID: FEAT-006-analysis-scope-lock
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
- Delivery stage: make it right (analysis contract)
- Related PR: (local on cursor/integration-981e)

## R - Requirements

### User Goal

Lock analysis scope (IN / NOT / Reference-only) before generating analysis prose.

### Acceptance Criteria

- [x] Analysis prompt includes Scope Lock-In before Analysis Generation
- [x] Analysis output requires Scope Lock (In / NOT / Reference-only)
- [x] Generation steps validate concepts against locked scope
- [x] Guidance document shipped under docs/

### Non-Goals

- Recorded in the requirement file; respected at ship time.

### Assumptions

- Implementation landed before this canvas; canvas backfilled for dogfood completeness.

## E - Entities

### Application Components

- See Files Likely Affected.

### Files Likely Affected

- `spec/commands/lifecycle-analysis.spec.md`
- `docs/analysis-phase-scope-validation.md`
- `templates/cursor/sdlc-spdd-analysis.md`
- `templates/copilot/prompts/sdlc-spdd-analysis.prompt.md`
- `templates/claude/commands/sdlc-spdd-analysis.md`

## A - Approach

### Proposed Approach

Implementation-first on `cursor/integration-981e`, then backfill this REASONS canvas
so Milestone 1 Linked Work has a governing contract for review/sync.

## S - Structure

Operations below match shipped increments.

## O - Operations

### T01 - Add Scope Lock to analysis lifecycle spec

- Status: Complete
- Description: Require Scope Lock section in analysis adapters
- Files: spec/commands/lifecycle-analysis.spec.md, generated adapters
- Tests: validate-command-adapters.sh
- Validation: Shipped

### T02 - Ship guidance doc

- Status: Complete
- Description: Document Scope Lock pitfalls and workflow
- Files: docs/analysis-phase-scope-validation.md
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
