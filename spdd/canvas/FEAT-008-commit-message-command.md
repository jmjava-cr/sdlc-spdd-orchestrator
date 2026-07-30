# REASONS Canvas: FEAT-008-commit-message-command - Commit message slash command

## Metadata

- Work ID: FEAT-008-commit-message-command
- Work Type: Feature
- Status: Complete
- Readiness: Reviewed — Complete
- Created: 2026-07-30
- Updated: 2026-07-30 (REASONS section labels aligned for dogfood validate)
- Owner: framework
- Target Project: sdlc-spdd-orchestrator
- Stack: Markdown command specs (FEAT-002 generator)
- Source System: GitHub issue #41
- Roadmap: ROADMAP.md
- Milestone: milestone-1.md
- Related: FEAT-002-command-spec-generation
- Related PR: https://github.com/jmjava/sdlc-spdd-orchestrator/pull/42

## R - Requirements

### User Goal

From chat, generate a paste-ready commit message for the current local changes
— without creating the commit.

### Business / Product Goal

Speed up the commit step with a consistent message draft grounded in the actual
diff, using the existing lifecycle command pack.

### Acceptance Criteria

- [x] `/sdlc-spdd-commit-message` shipped for Cursor, Copilot, Claude
- [x] Python engine collects the diff (`sdlc.sh commit-message`)
- [x] Drafts from staged → unstaged → commits since base; optional hint + Work ID
- [x] Success/failure feedback; does not commit unless asked
- [x] Spec, adapters, docs, tests

## E - Entities

### Application Components

- `spec/commands/lifecycle-commit-message.spec.md`
- Generated adapters under `templates/{cursor,copilot,claude}/`
- `engine/src/sdlc_engine/commit_message.py`

### Files Likely Affected

- Spec + three adapters
- `scripts/sdlc.sh` commit-message route
- `tests/test-commit-message-command.sh`

## A - Approach

### Proposed Approach

Add a lifecycle command via FEAT-002 generator. Diff collection lives in the
Python engine; assistants draft the message from that report and never commit
unless the user explicitly asks afterward.

```
/sdlc-spdd-commit-message
        │
        ▼ ./scripts/sdlc.sh commit-message   (python-only route)
engine/src/sdlc_engine/commit_message.py     (staged|unstaged|ahead-of-base)
        │
        ▼ assistant drafts paste-ready subject/body from the report
```

## S - Structure

Spec → generated adapters; engine owns diff report; chat owns message prose.

## O - Operations

### T01 - Spec, adapters, registries, docs, tests

- Status: Complete
- Description: Add lifecycle-commit-message spec; generate three adapters; register
  in validate/extract/test harnesses; document in usage docs + grounding;
  extend harness coverage; link issue #41. Retargeted from an earlier PR-review
  comment interpretation to commit-message generation.

## N - Norms

- Prefer specs → generate adapters over hand-editing adapters.
- Generate only — do not run `git commit` unless the user explicitly asks after the draft.

## S - Safeguards

- Do not create commits unless explicitly asked after the draft
- Do not invent Work IDs or messages when there is nothing to commit
- Do not modify application source from this command
- No posture language in shipped templates/docs

## Review Checklist

- [x] Requirements satisfied
- [x] Operations completed
- [x] Tests added or updated
- [x] Documentation updated if needed

## Sync Notes

Merged via PR #42. Canvas section labels aligned 2026-07-30 for dogfood validate.

## Final Status

- Status: Complete
- Completed Date: 2026-07-30
- PR: https://github.com/jmjava/sdlc-spdd-orchestrator/pull/42
- Follow-Up Tasks: none
