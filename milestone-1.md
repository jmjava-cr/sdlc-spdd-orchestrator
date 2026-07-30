# Milestone 1 — Make it right

This root file is a compatibility stub for older `@milestone-1.md` links and docs.
**Canonical definition:** [`requirements/milestones/milestone-1/MILESTONE-1.md`](requirements/milestones/milestone-1/MILESTONE-1.md).
Scripts prefer the subdirectory definition when both exist.

Prompt optimization — including the ledger and leading indicators that measure it —
is "make it fast" and is deliberately sequenced with measurement complete and
remaining spikes deferred until Guide MCP is available.

## Plan (in order)

Make it right:

1. **FEAT-001 — shared `scripts/lib/`** — Complete.
2. **FEAT-002 — single command spec → generated adapters** — Complete.
3. **FEAT-003 — extension/hook manifest** — Complete.
4. **FEAT-006 — Python orchestration engine (v2)** — Complete (PR #31).
5. **FEAT-007 — Local SQLite index (pre-GUIDE)** — Complete (PR #38).
6. **FEAT-008 — `/sdlc-spdd-commit-message`** — Complete (PR #42).
7. **FEAT-009 — analysis Scope Lock-In** — Complete (local track; renumbered).
8. **FEAT-010 — Jira-compatible requirements format** — Complete (local track; renumbered).
9. **FEAT-011 — milestone subdirectory layout** — Complete (local track; renumbered).
10. **FEAT-012 — session-brief archive/rotation** — Complete (local track; renumbered).
11. **Readability pass** — residual optional.

Make it fast:

12. **FEAT-004 — prompt-optimization ledger + capture metrics** — Complete.
13. **FEAT-005 — canvas readiness + leading indicators** — Complete.
14. **SPIKE-001 / SPIKE-002** — Shelved until Guide MCP is available.

## Constraint

The make-it-work/right/fast posture is how *we* plan the orchestrator. It must not
appear in anything that ships to target projects (`templates/`, shipped docs,
grounding files). This is enforced by `./scripts/check-posture-boundary.sh`.

## Linked Work

See the Linked Work table in
[`requirements/milestones/milestone-1/MILESTONE-1.md`](requirements/milestones/milestone-1/MILESTONE-1.md)
and the SPDD Work Map in [`ROADMAP.md`](ROADMAP.md).
