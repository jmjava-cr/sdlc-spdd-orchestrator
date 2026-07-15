# Issue #28 — Merge integration branch to main

**GitHub:** https://github.com/jmjava/sdlc-spdd-orchestrator/issues/28  
**Branch:** `cursor/integration-981e`  
**PR:** #27

## Issues to close (work now on integration)

| Issue | Reason | Action |
|-------|--------|--------|
| [#23](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/23) | Workflow agent commands implemented on integration | **Close** when PR #27 merges (supersedes draft PR #25) |
| [#7](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/7) | Instruction-file parity already on `main` (pre-integration) | **Close** as completed — not part of integration branch but done |

## PRs to close when #27 lands (do not merge separately)

| PR | Superseded by |
|----|----------------|
| [#25](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/25) | #27 |
| [#26](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/26) | #27 |

## Issues staying open (not on integration)

| Issue | Why |
|-------|-----|
| [#22](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/22) | Demo video regen — manual chore |
| [#18](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/18) | Language playbooks — separate effort |
| SPIKE / [#24](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/24) | Parked until T06 go/no-go |

## Manual close commands (if closing locally)

```bash
gh issue close 23 --comment "Landed via integration branch PR #27. Supersedes #25."
gh issue close 7 --comment "Implemented on main: validate-command-adapters.sh grounding checks + CI paths."
gh pr close 25 --comment "Superseded by integration PR #27."
gh pr close 26 --comment "Superseded by integration PR #27."
```
