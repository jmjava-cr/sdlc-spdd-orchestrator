# Analysis: FEAT-003-extension-hook-manifest

**Work ID:** FEAT-003-extension-hook-manifest  
**Date:** 2026-07-15  
**Branch:** `cursor/integration-981e`

## Current resolution (convention)

`resolve-agent-context.sh` maps SDLC phases to extension folders via
`phase_agent_dir()`, then loads `*.md` from `_all-agents` and the phase folder.
Skills resolve from `extensions/skills/` and `playbooks/` via `#SkillName`.

## Manifest format

- Path: `agent-context/extensions/manifest.md`
- Markdown tables: Phase extensions, Skills (documentation), Hooks (declarative)
- Phase table columns: Folder, Phases (`*` or comma-separated), Description

## Resolver behavior

- When manifest exists and the phase table is parseable, folders are taken from
  the manifest (backtick-stripped).
- When manifest is missing or malformed, convention fallback is unchanged.
- Hook paths are declared only; no execution runtime in this Work ID.

## Validation

- `./tests/test-extension-manifest.sh` — manifest vs convention parity
- `./tests/test-resolve-agent-context.sh` — full regression harness
