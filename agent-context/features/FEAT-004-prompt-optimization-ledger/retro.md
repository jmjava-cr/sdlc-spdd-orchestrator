# Retro: FEAT-004-prompt-optimization-ledger

**Date:** 2026-07-15  
**Phase:** retro  
**Canvas:** `spdd/canvas/FEAT-004-prompt-optimization-ledger.md`

## What went well

- Reused existing capture/index/rotation machinery — no new store.
- Metric Kind is additive; omitting flags preserves prior capture behavior.
- Spec → adapter generation kept three assistants in parity for T03.
- Session-memory tests (72) give a clear gate for T02/T04.

## What slowed us down

- `_wf_infer_next_operation` treated empty Final Status `- Status:` as keeping
  the last operation incomplete, so `sdlc.sh next` stuck on T05 after all ops
  were Complete. Fixed by stopping at `##` section boundaries.
- Advanced past review before writing the review artifact; gates had already
  inferred pass — write review before advancing next time.

## Prompt / process changes

- Ledger entry required in prompt-update and retro (T03) — first real use of the
  measurement loop this Work ID creates.
- Prefer one Operation → capture → next; batching T03–T05 in one close-out was
  faster but blurred operation boundaries for `next`.

## Keep / stop / start

| Keep | Stop | Start |
|------|------|-------|
| Ship-neutral check on template/doc changes | Advancing review before the review file exists | Explicit “all ops complete” smoke in workflow tests |
| Reuse rotate_session_history for ledgers | Hand-editing generated adapters | Capture with `--review-result` / `--rework` on review/retro |

## Ledger entry (required)

See `agent-context/memory/prompt-optimization-log.md` — FEAT-004 close-out entry
dated 2026-07-15 (outcome: improved — measurement substrate landed).
