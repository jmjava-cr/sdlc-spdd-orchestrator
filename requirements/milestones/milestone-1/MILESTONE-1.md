# Milestone 1 — Make it right

## Goal

Take the framework from its current working state to "right": refactor the
*existing* code and docs for readability, maintainability, and extensibility. No
new features. Ship each refactor as working code.

Prompt optimization — including the ledger and leading indicators that measure it —
is "make it fast" and is deliberately **last**, after the framework is structurally
right.

## Plan (in order)

Make it right (do first):

1. **FEAT-001 — shared `scripts/lib/` for capture/resolve/verify.** Foundational
   maintainability refactor; the other refactors build on it. Start here.
2. **FEAT-002 — single command spec → generated adapters.** Kills hand-maintained
   adapter drift across Cursor/Copilot/Claude.
3. **FEAT-003 — extension/hook manifest.** A clean, documented extension point.
4. **FEAT-006 — Python orchestration engine (v2).** `engine/sdlc_engine` + `SDLC_ENGINE` shim (PR #31).
5. **FEAT-007 — Local SQLite index (pre-GUIDE).** Regenerable `.sdlc/index.sqlite` (PR #38).
6. **FEAT-008 — `/sdlc-spdd-commit-message`.** Engine diff report → paste-ready message (PR #42).
7. **Readability pass — consistent structure, naming, and examples** across code
   and docs.
8. **FEAT-009 — analysis Scope Lock-In.** Prevent analysis scope creep before generation.
9. **FEAT-010 — Jira-compatible requirements format.** Frontmatter, templates, validation.
10. **FEAT-011 — milestone subdirectory layout.** Prefer `requirements/milestones/milestone-N/`.
11. **FEAT-012 — session-brief archive/rotation.** Keep `agent-context/sessions/` bounded.

Make it fast (measurement + spikes):

12. **FEAT-004 — prompt-optimization ledger + capture metrics.** **Complete**
   (`spdd/canvas/FEAT-004-prompt-optimization-ledger.md`).
13. **FEAT-005 — canvas `readiness:` / Metadata readiness + leading indicators.** **Complete**
    (`spdd/canvas/FEAT-005-canvas-readiness-indicators.md`).
14. **SPIKE-001 / SPIKE-002** — Guide DICE hybrid + local LLM/embedding spikes.
    Shelved until Guide MCP is available.

Work IDs are numbered in execution order. Local analysis/Jira/milestone/session-archive work was renumbered to FEAT-009–012 so main's FEAT-006–008 (engine/SQLite/commit-message) keep their IDs. FEAT-001–009 Milestone 1 feature track is
complete on the integration branch; SPIKE-001/002 remain for make-it-fast retrieval/LLM spikes.

## Constraint

The make-it-work/right/fast posture is how *we* plan the orchestrator. It must not
appear in anything that ships to target projects (`templates/`, shipped docs,
grounding files). This is enforced by `./scripts/check-posture-boundary.sh`.

## Linked Work

| Work ID | Canvas | Requirement | Status | Notes |
|---------|--------|-------------|--------|-------|
| FEAT-001-shared-script-library | spdd/canvas/FEAT-001-shared-script-library.md | requirements/milestones/FEAT-001-shared-script-library.md | Complete (T01–T04) | On integration branch |
| FEAT-002-command-spec-generation | spdd/canvas/FEAT-002-command-spec-generation.md | requirements/milestones/FEAT-002-command-spec-generation.md | Complete (T01–T05) | On integration branch |
| FEAT-003-extension-hook-manifest | spdd/canvas/FEAT-003-extension-hook-manifest.md | requirements/milestones/FEAT-003-extension-hook-manifest.md | Complete (T01–T04) | On integration branch |
| FEAT-006-python-orchestration-engine | spdd/canvas/FEAT-006-python-orchestration-engine.md | requirements/milestones/FEAT-006-python-orchestration-engine.md | Complete | Merged PR #31 |
| FEAT-007-local-sqlite-index | spdd/canvas/FEAT-007-local-sqlite-index.md | requirements/milestones/FEAT-007-local-sqlite-index.md | Complete | Merged PR #38 |
| FEAT-008-commit-message-command | spdd/canvas/FEAT-008-commit-message-command.md | requirements/milestones/FEAT-008-commit-message-command.md | Complete | Merged PR #42 |
| FEAT-004-prompt-optimization-ledger | spdd/canvas/FEAT-004-prompt-optimization-ledger.md | requirements/milestones/FEAT-004-prompt-optimization-ledger.md | Complete (T01–T05) | Make it fast; ledger + metrics + rotation + docs |
| FEAT-005-canvas-readiness-indicators | spdd/canvas/FEAT-005-canvas-readiness-indicators.md | requirements/milestones/FEAT-005-canvas-readiness-indicators.md | Complete (T01–T04) | Make it fast; readiness + cycle metrics |
| FEAT-009-analysis-scope-lock | spdd/canvas/FEAT-009-analysis-scope-lock.md | requirements/milestones/milestone-1/FEAT-009-analysis-scope-lock.md | Complete | Scope Lock-In in analysis; shipped 2026-07-15 |
| FEAT-010-jira-compatible-requirements | spdd/canvas/FEAT-010-jira-compatible-requirements.md | requirements/milestones/milestone-1/FEAT-010-jira-compatible-requirements.md | Complete | Frontmatter + validator; shipped 2026-07-15 |
| FEAT-011-milestone-subdirectory-layout | spdd/canvas/FEAT-011-milestone-subdirectory-layout.md | requirements/milestones/milestone-1/FEAT-011-milestone-subdirectory-layout.md | Complete | Subdir discovery + scaffold; shipped 2026-07-15 |
| FEAT-012-session-brief-archive | spdd/canvas/FEAT-012-session-brief-archive.md | requirements/milestones/milestone-1/FEAT-012-session-brief-archive.md | Complete | Rotate timestamped briefs to sessions/archive/; shipped 2026-07-15 |
| CHORE-001-docgen-initial-documentation | spdd/canvas/CHORE-001-docgen-initial-documentation.md | requirements/milestones/CHORE-001-docgen-initial-documentation.md | Complete (T01–T07) | Docgen bundle scaffold + initial narration (parallel) |
| CHORE-002-docgen-video-generation | spdd/canvas/CHORE-002-docgen-video-generation.md | requirements/milestones/CHORE-002-docgen-video-generation.md | Complete | 3 MP4s + Pages deploy; manual video regen (no render CI) |

## Session Updates

Record shipped increments under `session-notes/`.

### 2026-07-15T23:05:49Z - FEAT-004-prompt-optimization-ledger - code

- Summary: FEAT-004 T02: capture metric flags (--readiness/--review-result/--rework/--context-files) write Kind: metric rows; invalid review-result warns and skips
- Validation: tests/test-session-memory-index.sh 69/69
- Next: /sdlc-spdd-code @spdd/canvas/FEAT-004-prompt-optimization-ledger.md operation T03

### 2026-07-15T23:18:43Z - FEAT-004-prompt-optimization-ledger - code

- Summary: FEAT-004 T03-T05: ledger required in prompt-update/retro specs; ledger rotation via capture; docs metric Kind + workflow
- Validation: Not recorded
- Next: Not recorded

### 2026-07-15T23:19:59Z - FEAT-004-prompt-optimization-ledger - retro

- Summary: FEAT-004 retro: ledger measurement landed; fixed next-op Final Status boundary; Approved With Notes
- Validation: Not recorded
- Next: Not recorded

### 2026-07-15T23:20:00Z - FEAT-004-prompt-optimization-ledger - sync

- Summary: FEAT-004 sync: canvas/requirement/milestone aligned; Work ID Complete
- Validation: Not recorded
- Next: Not recorded

### 2026-07-15T23:21:58Z - FEAT-005-canvas-readiness-indicators - code

- Summary: FEAT-005 T01-T04: readiness vocab + validate + cycle metrics + docs
- Validation: Not recorded
- Next: Not recorded

### 2026-07-15T23:21:59Z - FEAT-005-canvas-readiness-indicators - retro

- Summary: FEAT-005 retro complete
- Validation: Not recorded
- Next: Not recorded

### 2026-07-15T23:21:59Z - FEAT-005-canvas-readiness-indicators - sync

- Summary: FEAT-005 sync complete
- Validation: Not recorded
- Next: Not recorded
