# Issue #28 — Merge integration branch to main

**GitHub:** https://github.com/jmjava/sdlc-spdd-orchestrator/issues/28  
**Branch:** `cursor/integration-981e`  
**PR:** [#27](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/27)

Use [docs/integration-branch.md](../docs/integration-branch.md) for gates and manual checklist before merging.

---

## What lands when #27 merges

| Deliverable | Work ID / source | Closes / supersedes |
|-------------|------------------|---------------------|
| Workflow assistant commands | Merged from `cursor/workflow-agent-commands-981e` | Closes #23; supersedes PR #25 |
| Catch-up documentation | Merged from `cursor/catch-up-branch-evaluation-981e` | Supersedes PR #26 |
| Shared `scripts/lib/` | FEAT-001 | — |
| Command spec generation | FEAT-002 | — |
| Extension manifest | FEAT-003 | — |

**Not included:** SPIKE-001 (PR #24), demo videos (#22), language playbooks (#18), readability pass.

---

## Issues to close

| Issue | Reason | When |
|-------|--------|------|
| [#23](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/23) | Workflow commands on integration | After #27 merges |
| [#7](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/7) | Instruction parity already on `main` | Anytime (not blocked on #27) |
| [#28](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/28) | Integration merged to `main` | After merge completes |

## PRs to close (do not merge separately)

| PR | Status | Superseded by |
|----|--------|---------------|
| [#25](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/25) | **Closed** 2026-07-15 (not merged) | #27 |
| [#26](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/26) | **Closed** 2026-07-15 (not merged) | #27 |

## Issues staying open

| Issue | Why |
|-------|-----|
| [#22](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/22) | Demo video regen — manual chore |
| [#18](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/18) | Language playbooks — separate effort |
| SPIKE / [#24](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/24) | Parked until T06 go/no-go |

---

## Post-merge verification on `main` (minimal)

```bash
git checkout main && git pull origin main

./scripts/validate-command-adapters.sh
./scripts/generate-command-adapters.sh --check
./scripts/verify-script-lib-duplicates.sh
./tests/test-extension-manifest.sh
./scripts/check-posture-boundary.sh
```

For the full gate list, use Quick start in [integration-branch.md](../docs/integration-branch.md).

---

## Manual close commands

```bash
gh issue close 23 --comment "Landed via integration branch PR #27. Supersedes #25."
gh issue close 7 --comment "Implemented on main: validate-command-adapters.sh grounding checks + CI paths."
gh issue close 28 --comment "Integration branch merged to main via PR #27."
# PRs #25 and #26 already closed as superseded by #27 (2026-07-15).
```

## Branch cleanup after merge

```bash
git push origin --delete cursor/workflow-agent-commands-981e
git push origin --delete cursor/catch-up-branch-evaluation-981e
# optional: delete cursor/integration-981e after merge
```

---

## Contributor docs added on integration

| Doc | Topic |
|-----|-------|
| [contributing-command-specs.md](../docs/contributing-command-specs.md) | Edit specs → regenerate adapters |
| [contributing-extensions.md](../docs/contributing-extensions.md) | Manifest and phase extensions |
