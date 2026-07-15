# Catch-up guide

Use this when returning after time away or when reconciling remote branches offline.

**Latest evaluation:** [session-notes/2026-07-15-catch-up-branch-evaluation.md](../session-notes/2026-07-15-catch-up-branch-evaluation.md)

That note covers:

- Which remote branches are stale vs active
- Open PRs (#24 spike, #25 workflow commands) and merge policy
- Open issues and what to close
- Milestone 1 (make it right) next work — FEAT-001 analysis
- Copy-paste commands for branch cleanup and refreshing the inventory

To fetch the catch-up branch locally:

```bash
git fetch origin cursor/catch-up-branch-evaluation-981e
git checkout cursor/catch-up-branch-evaluation-981e
```

## Integration branch (manual testing before `main`)

Collect planned merges and run manual tests on **`cursor/integration-981e`**:

```bash
git fetch origin cursor/integration-981e
git checkout cursor/integration-981e
```

See [integration-branch.md](integration-branch.md) for contents, automated gates, manual checklist, and merge procedure.

After merging useful parts into `main`, delete the catch-up branch or add a new dated session note for the next evaluation.
