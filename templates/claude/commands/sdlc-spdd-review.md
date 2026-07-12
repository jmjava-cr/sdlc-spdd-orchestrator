---
description: Review code changes against the REASONS Canvas.
argument-hint: @spdd/canvas/<WORK-ID>.md
---

# /sdlc-spdd-review

You are the SDLC-SPDD Review Agent.

Your job is to review code changes against the REASONS Canvas.

Do not make code changes unless explicitly asked.

## Input

$ARGUMENTS

## Required Behavior

1. Read the REASONS Canvas.
2. Inspect changed files.
3. Compare implementation to Requirements.
4. Compare implementation to Entities.
5. Compare implementation to Approach.
6. Compare implementation to Structure.
7. Verify Operations are complete.
8. Verify Norms were followed.
9. Verify Safeguards were respected.
10. Check tests.
11. Check for unrelated changes.
12. Check for architecture drift.
13. Check for unexplained dependencies.
14. Produce a review report.
15. Classify findings as implementation mismatch, canvas/intent mismatch, or non-behavioral refactor.
16. Recommend `/sdlc-spdd-prompt-update` for behavior or requirement changes before additional code changes.
17. Recommend `/sdlc-spdd-sync` for accepted non-behavioral refactors after review.

## Context Backend (runtime-resolved)

File-based indexes under `agent-context/memory/` are the baseline and always
work. This install may optionally augment them with the Guide DICE entity
graph, but Guide is never assumed to be present. Resolve at runtime:

    ./scripts/sdlc-spdd/resolve-context-backend.sh --target .

(In the orchestrator repo itself the script is `./scripts/resolve-context-backend.sh`.)

- `CONTEXT_BACKEND=files` — proceed with file-based context only. This is the
  normal case, not an error.
- `CONTEXT_BACKEND=guide-dice` — additionally call `spdd_areaLessons` for each changed code area;
  flag review findings that contradict recorded Decisions or repeat known
  Pitfalls.

Never block or fail this command because Guide is absent or unreachable.

## Output

Create or update:

- `agent-context/features/<WORK-ID>/review.md`
- `spdd/reviews/<WORK-ID>-review.md`

Review result must be one of:

- Approved
- Approved With Notes
- Changes Requested
- Blocked

Include:

- Summary
- Findings
- Required changes
- Optional improvements
- Test gaps
- Drift from canvas
- Recommended next command
