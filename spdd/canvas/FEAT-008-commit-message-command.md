# REASONS Canvas: FEAT-008-commit-message-command - Commit message slash command

## Metadata

- Work ID: FEAT-008-commit-message-command
- Work Type: Feature
- Status: Complete
- Created: 2026-07-30
- Updated: 2026-07-30
- Owner: framework
- Target Project: sdlc-spdd-orchestrator
- Stack: Markdown command specs (FEAT-002 generator)
- Source System: GitHub issue #41
- Roadmap: ROADMAP.md
- Milestone: milestone-1.md
- Related: FEAT-002-command-spec-generation

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

## E - Essentials

- Generate only — do not run `git commit` unless the user explicitly asks after the draft
- Diff collection lives in the Python engine (`CommitMessageService`)
- Prefer staged changes; fall back to unstaged; then commits since merge base
- Empty change set → fail closed
- Own Work ID (FEAT-008); not a FEAT-002-only change

## A - Architecture

```
/sdlc-spdd-commit-message
        │
        ▼ ./scripts/sdlc.sh commit-message   (python-only route)
engine/src/sdlc_engine/commit_message.py     (staged|unstaged|ahead-of-base)
        │
        ▼ assistant drafts paste-ready subject/body from the report
```

## S - Safeguards

- Do not create commits unless explicitly asked after the draft
- Do not invent Work IDs or messages when there is nothing to commit
- Do not modify application source from this command
- No posture language in shipped templates/docs

## Operations

### T01 - Spec, adapters, registries, docs, tests

- Status: Complete
- Description: Add lifecycle-commit-message spec; generate three adapters; register
  in validate/extract/test harnesses; document in usage docs + grounding;
  extend harness coverage; link issue #41. Retargeted from an earlier PR-review
  comment interpretation to commit-message generation.

## Final Status

- Status: Complete
