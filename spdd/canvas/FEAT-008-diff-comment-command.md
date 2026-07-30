# REASONS Canvas: FEAT-008-diff-comment-command - Diff comment slash command

## Metadata

- Work ID: FEAT-008-diff-comment-command
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

From chat, generate a paste-ready PR review comment based on the current diff
versus base — without posting it.

### Business / Product Goal

Close the gap between “I have a diff open” and “I have a review note ready,”
using the existing lifecycle command pack.

### Acceptance Criteria

- [x] `/sdlc-spdd-diff-comment` shipped for Cursor, Copilot, Claude
- [x] Drafts from current diff vs base; optional message + Work ID
- [x] Success/failure feedback; does not post
- [x] Spec, adapters, docs, tests

## E - Essentials

- Generate only — never post (`gh pr comment` / API forbidden)
- Diff must be versus merge base (prefer `origin/main`)
- Empty/missing base → fail closed
- Own Work ID (FEAT-008); not a FEAT-002-only change

## A - Architecture

```
spec/commands/lifecycle-diff-comment.spec.md
        │
        ▼ generate-command-adapters.sh
templates/{cursor,copilot,claude}/…/sdlc-spdd-diff-comment*
        │
        ▼ install-* scripts (glob)
.target assistant slash command
```

## S - Safeguards

- Do not post comments to remotes
- Do not invent Work IDs or findings when the diff is empty
- Do not modify application source from this command
- No posture language in shipped templates/docs

## Operations

### T01 - Spec, adapters, registries, docs, tests

- Status: Complete
- Description: Add lifecycle-diff-comment spec; generate three adapters; register
  in validate/extract/test harnesses; document in usage docs + grounding;
  extend harness coverage; link issue #41.

## Final Status

- Status: Complete
