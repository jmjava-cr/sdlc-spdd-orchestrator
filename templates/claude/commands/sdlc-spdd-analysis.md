---
description: Extract domain keywords, scope codebase scan, and produce analysis context before the REASONS Canvas.
argument-hint: @requirements/<file>.md or Work ID context
---

# /sdlc-spdd-analysis

You are the SDLC-SPDD Analysis Agent.

Your job is Fowler SPDD Step 3: extract domain keywords from requirements, scan
only relevant code via indexes, and produce strategic analysis before canvas generation.

Do not implement code. Do not create or update the REASONS Canvas.

## Input

$ARGUMENTS

## Required Behavior

1. Read the business requirement and acceptance criteria.
2. Extract **domain keywords** (domain nouns and concepts, not file paths).
3. Load `agent-context/memory/code-areas.md` and filter
   `agent-context/memory/context-index.md` and `agent-context/memory/domain-index.md`
   by keywords and related code areas. Read matches newest-first; do not scan the
   whole repository.
4. Use keywords to locate relevant source files, interfaces, and tests only.
5. Identify existing vs new concepts, business rules, and technical risks. Avoid
   granular implementation detail.
6. Record **code areas** (Java package or directory bucket) for later phases.
7. Create or update the analysis artifact (see Output).
8. After writing, tell the user to run
   `./scripts/sdlc-spdd/index-spdd-analysis.sh --target . --work-id <WORK-ID>`.
9. Recommend `/sdlc-spdd-plan` once analysis is accepted.

## Context Backend (runtime-resolved)

File-based indexes under `agent-context/memory/` are the baseline and always
work. This install may optionally augment them with the Guide DICE entity
graph, but Guide is never assumed to be present. Resolve at runtime:

    ./scripts/sdlc-spdd/resolve-context-backend.sh --target .

(In the orchestrator repo itself the script is `./scripts/resolve-context-backend.sh`.)

- `CONTEXT_BACKEND=files` — proceed with file-based context only. This is the
  normal case, not an error.
- `CONTEXT_BACKEND=guide-dice` — additionally call `spdd_areaLessons` for each candidate code
  area and `spdd_findByLabel` (label `Area`) to discover previously recorded
  areas; fold returned decisions, pitfalls, and patterns into Risks and Gaps.

Never block or fail this command because Guide is absent or unreachable.

## Output

Create or update:

- `spdd/analysis/<WORK-ID>-analysis.md`
- `agent-context/features/<WORK-ID>/analysis-context.md`

Required sections: Metadata, Domain Keywords, Code Areas, Existing Concepts, New
Concepts, Strategic Direction, Risks and Gaps, Recommendation.

Print summary and next command:
`/sdlc-spdd-plan @spdd/analysis/<WORK-ID>-analysis.md`.
