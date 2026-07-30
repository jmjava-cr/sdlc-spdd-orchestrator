# Requirement: FEAT-008-commit-message-command

## Summary

Add a lifecycle slash command that generates (does not commit) a commit message
from the current local change set the user is about to commit, with an optional
short hint and Work ID.

## Acceptance Criteria

- [x] Slash command `/sdlc-spdd-commit-message` available for Cursor, Copilot, and Claude
- [x] Python engine `commit-message` collects staged → unstaged → ahead-of-base diffs (`sdlc.sh commit-message`)
- [x] Slash command drafts from the engine report (not ad-hoc git)
- [x] Supports a short hint and optional Work ID metadata
- [x] Responds with explicit success or failure feedback
- [x] Explicitly does **not** run `git commit` unless the user asks after the draft
- [x] Spec → generated adapters; registries, docs, and tests updated

## Jira

- Key: TBD
- Issue type: Story
- Summary: Slash command to generate a commit message from current changes
- Labels: sdlc-spdd, feature

### Description

When ready to commit, agents and users need a fast way to draft a commit message
from the actual change set (staged preferred). Generation only — committing stays
an explicit follow-up.

### Acceptance criteria (Given/When/Then)

- Given staged or unstaged local changes
- When `/sdlc-spdd-commit-message` runs with an optional hint and Work ID
- Then the assistant returns a paste-ready subject (+ optional body)
- Given a clean working tree with no commits ahead of base
- When the command runs
- Then it reports failure and does not invent a message
- Given a successful draft
- When the command finishes
- Then it has not run `git commit` unless the user explicitly asked afterward

## GitHub

- Number: 41
- Title: [FEAT]: create a slash command for creating comment for current diff
- Labels: feature
- URL: https://github.com/jmjava/sdlc-spdd-orchestrator/issues/41
