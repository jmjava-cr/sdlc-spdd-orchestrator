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
4. **FEAT-006 — Python orchestration engine (v2).** Reusable `sdlc_engine`
   package + `SDLC_ENGINE` shell shim; port remaining helpers gradually.
5. **FEAT-007 — Local SQLite index (pre-GUIDE).** Regenerable `.sdlc/index.sqlite`
   query cache; multi-user sync stays git until/unless GUIDE lands.
6. **Readability pass — consistent structure, naming, and examples** across code
   and docs.

Make it fast (do last, deferred):

7. **FEAT-004 — prompt-optimization ledger + capture metrics.** Already specced;
   parked until the refactors above land. (`spdd/canvas/FEAT-004-prompt-optimization-ledger.md`.)
8. **FEAT-005 — canvas `readiness:` front matter + leading indicators.**

Work IDs are numbered in execution order. FEAT-001–003 are complete on `main`;
FEAT-006 (Python engine) is in progress; FEAT-004 (deferred) is at Ready For
Coding; FEAT-005 remains draft until make-it-fast work begins.

## Constraint

The make-it-work/right/fast posture is how *we* plan the orchestrator. It must not
appear in anything that ships to target projects (`templates/`, shipped docs,
grounding files). This is enforced by `./scripts/check-posture-boundary.sh`.

## Linked Work

| Work ID | Canvas | Requirement | Status | Notes |
|---------|--------|-------------|--------|-------|
| FEAT-001-shared-script-library | spdd/canvas/FEAT-001-shared-script-library.md | requirements/milestones/FEAT-001-shared-script-library.md | Complete | On integration branch |
| FEAT-002-command-spec-generation | spdd/canvas/FEAT-002-command-spec-generation.md | requirements/milestones/FEAT-002-command-spec-generation.md | Complete | On integration branch |
| FEAT-003-extension-hook-manifest | spdd/canvas/FEAT-003-extension-hook-manifest.md | requirements/milestones/FEAT-003-extension-hook-manifest.md | Complete | On integration branch |
| FEAT-006-python-orchestration-engine | spdd/canvas/FEAT-006-python-orchestration-engine.md | requirements/milestones/FEAT-006-python-orchestration-engine.md | Complete | Python v2 engine + shell shim (merged #31) |
| FEAT-007-local-sqlite-index | spdd/canvas/FEAT-007-local-sqlite-index.md | requirements/milestones/FEAT-007-local-sqlite-index.md | Complete | Pre-GUIDE local SQLite query cache |
| FEAT-008-diff-comment-command | spdd/canvas/FEAT-008-diff-comment-command.md | requirements/milestones/FEAT-008-diff-comment-command.md | Complete | `/sdlc-spdd-diff-comment` generate-only PR note (closes #41) |
| FEAT-004-prompt-optimization-ledger | spdd/canvas/FEAT-004-prompt-optimization-ledger.md | requirements/milestones/FEAT-004-prompt-optimization-ledger.md | Draft | Make it fast; runs after refactors |
| FEAT-005-canvas-readiness-indicators | spdd/canvas/FEAT-005-canvas-readiness-indicators.md | requirements/milestones/FEAT-005-canvas-readiness-indicators.md | Draft | Make it fast; do last |
| CHORE-001-docgen-initial-documentation | spdd/canvas/CHORE-001-docgen-initial-documentation.md | requirements/milestones/CHORE-001-docgen-initial-documentation.md | Complete | Docgen bundle scaffold + initial narration (parallel) |
| CHORE-002-docgen-video-generation | spdd/canvas/CHORE-002-docgen-video-generation.md | requirements/milestones/CHORE-002-docgen-video-generation.md | Complete | 3 MP4s + Pages deploy; manual video regen (no render CI) |

## Session Updates

Record shipped increments under `session-notes/`.
