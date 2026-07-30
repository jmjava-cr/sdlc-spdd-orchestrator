# Requirement: FEAT-008-diff-comment-command

## Summary

Add a lifecycle slash command that generates (does not post) a PR review comment
draft from the current git diff versus the merge base, with an optional short
message and Work ID metadata.

## Acceptance Criteria

- [x] Slash command `/sdlc-spdd-diff-comment` available for Cursor, Copilot, and Claude
- [x] Command drafts a comment from the current diff vs base (merge-base + `git diff`)
- [x] Supports a short message and optional Work ID metadata
- [x] Responds with explicit success or failure feedback
- [x] Explicitly does **not** post to GitHub/GitLab
- [x] Spec → generated adapters; registries, docs, and tests updated

## Jira

- Key: TBD
- Issue type: Story
- Summary: Slash command to generate a comment from the current diff
- Labels: sdlc-spdd, feature

### Description

Reviewers and agents need a fast way to draft a PR comment from the actual
diff-against-base for the current change set. The command must generate text
only — posting remains a manual paste into the review UI.

### Acceptance criteria (Given/When/Then)

- Given a branch with commits (or local changes) versus `origin/main`
- When `/sdlc-spdd-diff-comment` runs with an optional short message and Work ID
- Then the assistant returns a paste-ready comment plus base ref metadata
- Given an empty diff or missing base
- When the command runs
- Then it reports failure and does not invent findings
- Given a successful draft
- When the command finishes
- Then it has not called `gh pr comment` or otherwise posted remotely

## GitHub

- Number: 41
- Title: [FEAT]: create a slash command for creating comment for current diff
- Labels: feature
- URL: https://github.com/jmjava/sdlc-spdd-orchestrator/issues/41
