# Prompt Optimization Log

Record whether a prompt or context change improved an outcome. One global ledger
for the project — retrieve by Work ID or via `context-index.md` rows with
Kind: `metric` (added when capture metric flags are used).

This file is measurement only. It does not score prompts or auto-optimize them.

## Row schema

Append one markdown section per entry (newest last, or follow project capture
conventions). Required fields:

| Field | Meaning |
|-------|---------|
| **Date** | ISO date or timestamp of the change |
| **Work ID** | Owning Work ID (for example `FEAT-001-example`) |
| **Change** | What changed (command template, grounding, playbook, analysis prompt, …) |
| **Hypothesis** | Why you expected the change to help |
| **Signal** | What you observed (review loops, rework count, clarity, …) |
| **Outcome** | Did it help? (`improved` / `neutral` / `worse` / `unknown`) plus a short note |

Optional capture-time metrics (when wired by `capture-session-memory.sh`):

- `--readiness` — canvas readiness value at capture
- `--review-result` — `pass` \| `fail` \| `mixed` \| `blocked`
- `--rework` — non-negative count of corrective prompt-update/sync cycles after
  first Ready For Coding
- `--context-files` — approximate context file count loaded for the session
- `--validate-cycles` / `--review-cycles` — leading indicator counts (FEAT-005)

Older entries may be rotated into `agent-context/memory/archive/` (same pattern as
`session-history.md`) once rotation is enabled.

## Entries

<!-- Append ledger entries below. Do not seed dogfood Work IDs into target projects. -->
