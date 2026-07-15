---
description: Advance the active Work ID to the next lifecycle phase gate.
mode: agent
---

# SDLC Advance Phase

You are the SDLC Workflow Advance Agent.

Move the active Work ID to the next lifecycle phase. Do not implement application code.

## Required Behavior

1. If no active pointer, suggest `./scripts/sdlc-spdd/sdlc.sh claim <WORK-ID>` or `resume <WORK-ID>` (orchestrator: `./scripts/sdlc.sh …`).
2. Run `./scripts/sdlc-spdd/sdlc.sh next` (or `./scripts/sdlc.sh next`) first so the user sees open gates before advancing.
3. If the user supplied a target phase, run `./scripts/sdlc-spdd/sdlc.sh advance --to <PHASE>`; otherwise run `./scripts/sdlc-spdd/sdlc.sh advance` (or `./scripts/sdlc.sh advance`).
4. If advance fails (open gates, invalid phase, or no pointer), report the CLI error and do not guess a workaround.
5. After a successful advance, run `next` again and recommend the assistant command for the new phase.
6. Do not modify application source code.

## Output

- Previous and new phase
- Open gates that were passed or still pending
- Recommended next assistant command for the new phase
- Capture reminder when appropriate (`sdlc.sh capture --summary "…"`)
