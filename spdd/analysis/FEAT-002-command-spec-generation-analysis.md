# Analysis: FEAT-002-command-spec-generation

**Work ID:** FEAT-002-command-spec-generation  
**Date:** 2026-07-15  
**Branch:** `cursor/integration-981e`

## Findings

- Workflow commands (`claim`, `shelf`, `advance`, `next`, `team`) share identical
  `Required Behavior` and `Output` across Cursor, Copilot, and Claude.
- Lifecycle commands differ mainly in preamble and occasional per-adapter steps
  (for example `init` step 8: Cursor vs Copilot vs Claude command file creation).
- Copilot adapters use YAML front matter (`description`, `mode`); Claude adds
  `argument-hint` for workflow commands.

## Spec format

- Location: `spec/commands/<family>-<slug>.spec.md`
- Front matter: `family`, `slug`, per-adapter metadata
- Body blocks: `---BLOCK:<adapter>:<section>---` … `---END---`
- Shared sections when all adapters match: `shared:Required Behavior`, `shared:Output`

## Generator

- `scripts/extract-command-specs.sh` — bootstrap specs from current templates
- `scripts/generate-command-adapters.sh` — emit adapters; `--check` for CI staleness

## Validation

- `./scripts/generate-command-adapters.sh --check`
- `./scripts/validate-command-adapters.sh`
- `./scripts/check-posture-boundary.sh`
