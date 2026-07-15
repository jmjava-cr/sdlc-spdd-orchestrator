# Integration branch: `cursor/integration-981e`

**Purpose:** Collect planned merges off `main` for manual testing before a single merge back to `main`.  
**Created:** 2026-07-15  
**Base:** `origin/main` @ `3b519cb`  
**Tracking issue:** [#28 — Merge integration branch to main](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/28)

---

## What is on this branch

| Source branch | PR | Merged? | Contents |
|---------------|-----|---------|----------|
| `cursor/workflow-agent-commands-981e` | [#25](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/25) | yes | `/sdlc-claim`, `/sdlc-shelf`, `/sdlc-advance`, `/sdlc-next`, `/sdlc-team` |
| `cursor/catch-up-branch-evaluation-981e` | [#26](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/26) | yes | Catch-up docs (`docs/catch-up.md`, session note) |

### Explicitly excluded (parked)

| Branch | PR | Reason |
|--------|-----|--------|
| `cursor/spike-guide-ingest-agent-context-17f4` | [#24](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/24) | SPIKE-001 — do not merge until canvas **T06 go/no-go** (make it fast) |

### In progress on integration (not yet merged to `main`)

| Work ID | Operation | Artifact |
|---------|-----------|----------|
| FEAT-001-shared-script-library | T01–T04 complete | `scripts/lib/`, `scripts/verify-script-lib-duplicates.sh` |
| FEAT-002-command-spec-generation | T01–T05 complete | `spec/commands/`, `scripts/generate-command-adapters.sh`, CI staleness |
| FEAT-003-extension-hook-manifest | T01–T04 complete | `agent-context/extensions/manifest.md`, resolver + tests |

**Remaining milestone-1 item:** readability pass (item #4) — not started on integration.

---

## Automated gates (run before manual testing)

```bash
./scripts/validate-command-adapters.sh
./scripts/generate-command-adapters.sh --check
./scripts/verify-script-lib-duplicates.sh
./tests/test-adapter-install.sh
./tests/test-scripts-lib.sh
./tests/test-index-spdd-analysis.sh
./tests/test-resolve-agent-context.sh
./tests/test-extension-manifest.sh
./tests/test-sdlc-workflow.sh
./tests/test-sdlc-pointer.sh
./scripts/check-posture-boundary.sh
```

All should pass on the integration tip.

---

## Manual test checklist

Use a **throwaway target directory** so you do not disturb a real project:

```bash
export TARGET=/tmp/sdlc-integration-test
rm -rf "${TARGET}"
./scripts/init-project.sh --target "${TARGET}" --all
```

### 1. Install and adapter parity

- [ ] `init-project.sh --all` completes without error
- [ ] `.cursor/commands/sdlc-claim.md` exists in target
- [ ] `.github/prompts/sdlc-claim.prompt.md` exists in target
- [ ] `.claude/commands/sdlc-claim.md` exists in target
- [ ] Grounding files list workflow commands (`/sdlc-claim`, `/sdlc-team`, etc.)
- [ ] `./scripts/validate-command-adapters.sh --target "${TARGET}"` passes

### 2. Workflow CLI (shell)

From `${TARGET}`:

```bash
cd "${TARGET}"
./scripts/sdlc-spdd/sdlc.sh list-work
./scripts/sdlc-spdd/sdlc.sh claim FEAT-001-shared-script-library
./scripts/sdlc-spdd/sdlc.sh next
./scripts/sdlc-spdd/sdlc.sh team
./scripts/sdlc-spdd/sdlc.sh shelf --reason "integration test"
./scripts/sdlc-spdd/sdlc.sh list-work
```

- [ ] `claim` sets `.sdlc/pointer` and updates `work-registry.tsv`
- [ ] `next` shows phase and recommended command
- [ ] `team` shows registry row
- [ ] `shelf` clears pointer and marks shelved

### 3. Workflow commands (assistant — optional live test)

In Cursor / Copilot / Claude on the target project:

- [ ] `/sdlc-claim <WORK-ID>` appears in command palette
- [ ] `/sdlc-next` returns orientation (same family as `/sdlc-spdd-whereami`)
- [ ] `/sdlc-team` shows registry
- [ ] `/sdlc-shelf` parks active work
- [ ] `/sdlc-advance` moves phase when gates allow

### 4. Upgrade path

```bash
./scripts/upgrade-project.sh --target "${TARGET}" --all --force
./scripts/validate-command-adapters.sh --target "${TARGET}"
```

- [ ] Upgrade installs new workflow command files
- [ ] Parity validation still passes

### 5. Regression spot-check (orchestrator repo)

- [ ] `./scripts/sdlc.sh next` works in orchestrator repo root
- [ ] Existing `/sdlc-spdd-*` commands unchanged in templates

---

## Merge to `main` (after manual sign-off)

When the checklist passes:

```bash
git checkout main
git pull origin main
git merge cursor/integration-981e
# run automated gates again
git push origin main
```

Then close:

- Issue **#23** (workflow commands — on integration)
- Issue **#7** (instruction parity — already on `main`)
- Draft PRs **#25** and **#26** (superseded by #27)

See `issues/INTEGRATION-MERGE-28.md` for the full close list and commands.

Delete feature branches after merge:

```bash
git push origin --delete cursor/workflow-agent-commands-981e
git push origin --delete cursor/catch-up-branch-evaluation-981e
# keep or delete cursor/integration-981e after merge
```

---

## Next planned work (iterate on this branch)

Per [milestone-1.md](../milestone-1.md) make-it-right order:

1. ~~**FEAT-001** — shared `scripts/lib/`~~ (complete on integration)
2. ~~**FEAT-002** — command spec generation~~ (complete on integration)
3. ~~**FEAT-003** — extension/hook manifest~~ (complete on integration)
4. **Readability pass** — consistent structure, naming, and examples

See [docs/catch-up.md](catch-up.md) for full branch/issue inventory.

---

## Fetch locally

```bash
git fetch origin cursor/integration-981e
git checkout cursor/integration-981e
```

---

## Refresh integration from `main`

If `main` moves while you test:

```bash
git fetch origin main
git checkout cursor/integration-981e
git merge origin/main
# resolve conflicts, re-run gates, continue testing
git push origin cursor/integration-981e
```
