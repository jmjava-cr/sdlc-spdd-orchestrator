# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Python orchestration engine v2 (`engine/sdlc_engine`) with CLI + pytest; `scripts/sdlc.sh` supports `SDLC_ENGINE=auto|python|shell` (FEAT-006)
- Engine milestone sync usability: `links`, `sync-links --repair`, `sync-roadmap`, `issues draft|push|pull` for Jira/GitHub; claim auto-reads `## Jira` Key and `## GitHub` Number
- Local/offline work sessions (`LOCAL-*`): `sdlc.sh local start|list|capture|shelf|resume|promote|abandon` — machine-private under `.sdlc/local-sessions/` until promoted into a documented Work ID
- Issue sync test harness: mocked Jira HTTP + fake `gh` write-back tests; live GitHub Issues integration (`SDLC_GITHUB_INTEGRATION=1`) and CI job with `issues: write`
- Jira description formatting: markdown → ADF (Cloud v3) / wiki (Server v2), structured sections from milestone `## Jira`, `issues draft --format adf|wiki`, pull ADF→markdown
- Shared `scripts/lib/` helpers + consumer migration (FEAT-001); `verify-script-lib-duplicates.sh`
- Canonical `spec/commands/*.spec.md` → generated Cursor/Copilot/Claude adapters (FEAT-002)
- Extension manifest + resolver fallback (FEAT-003)
- `sdlc.sh archive` / `archive --all`: move Complete/Cancelled Work ID artifacts into `archive/` folders (closes [#29](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/29))
- Expanded CI/regression harnesses: `test-scripts-lib`, `test-extension-manifest`, `test-command-spec-generation`, `test-archive-work`, `test-integration-merge`
- SDLC pointer manager (`agent-context/sdlc-pointer.sh`): persistent Work ID in `.sdlc/pointer`, guarded execution wrappers ([#20](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/20), closes [#19](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/19))
- Workflow CLI (`scripts/sdlc.sh` / `scripts/sdlc-spdd/sdlc.sh`): phase/gate tracking, `next`/`advance`/`skip`/`shelf`/`resume`/`sync`, guarded `capture` ([#21](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/21))
- Team Work ID registry (`agent-context/work-registry.tsv`, `sdlc-team-registry.sh`): `claim`/`release`/`team`/`list-work`, stale TTL, branch/PR/Jira notes ([#21](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/21))
- `/sdlc-spdd-whereami` assistant command (Cursor, Copilot, Claude) — chat orientation aligned with `sdlc.sh next` ([#21](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/21))
- Workflow agent commands (`/sdlc-claim`, `/sdlc-shelf`, `/sdlc-advance`, `/sdlc-next`, `/sdlc-team`) for Cursor, Copilot, and Claude — chat wrappers for `sdlc.sh claim|shelf|advance|next|team` (closes [#23](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/23))
- Milestone `## Jira` draft convention in `requirements/milestones/<WORK-ID>.md`; auto-link on claim
- CI regression harnesses: `tests/test-sdlc-pointer.sh`, `tests/test-sdlc-workflow.sh`
- Claude Code support as a third assistant adapter: `templates/claude/` command pack
  and `CLAUDE.md`, `scripts/install-claude-commands.sh`, `--claude` flags on
  setup/init/upgrade, `--require-claude` install verification, Claude command-pack
  parity validation, CI path coverage, and `docs/claude-usage.md`
- Always-on Cursor operating-model rule (`templates/cursor/rules/sdlc-spdd.mdc`,
  installed to `.cursor/rules/`) giving Cursor the same whole-ecosystem grounding
  as Copilot's `copilot-instructions.md` and Claude's `CLAUDE.md`
- Whole-ecosystem grounding norm enforced in CI: `validate-command-adapters.sh`
  asserts every assistant's always-on grounding file covers Planning + SPDD + SDLC
- Adapter install/upgrade regression harness (`tests/test-adapter-install.sh`) and
  `test-adapter-install` CI workflow proving Cursor/Copilot are not regressed,
  no-flag defaults remain backward compatible, and existing `CLAUDE.md` content
  is preserved on upgrade
- Initial repository structure per STARTER-SPEC.md
- REASONS Canvas templates (feature, bugfix, refactor, spike)
- Eight Cursor command templates for SDLC-SPDD lifecycle
- Shell scripts: init, install commands, create feature, validate canvas, detect stack, sync context
- Stack rules for Java/Spring Boot, Gradle, Maven, Kubernetes, Tekton, Python, Node, Docker
- Agent overlays, playbooks, memory, and harness files
- Spring Boot order API example workflow
- Tekton pipeline demo layout
- GitHub issue and pull request templates
- GitHub Actions workflow for canvas validation
- Project documentation under `docs/`
