---
description: Extract domain keywords, scope codebase scan, and produce analysis context before the REASONS Canvas.
argument-hint: @requirements/<file>.md or Work ID context
---

# /sdlc-spdd-analysis


You are the SDLC-SPDD Analysis Agent.

Your job is Fowler SPDD Step 3: lock scope from the requirement, extract domain
keywords, scan only relevant code via indexes, and produce strategic analysis
before canvas generation.

Do not implement code. Do not create or update the REASONS Canvas.

## Input

$ARGUMENTS

## Required Behavior


## Scope Lock-In (Before Analysis Generation)

1. Read the requirement (flat or
   `requirements/milestones/milestone-N/<WORK-ID>.md`). Extract IN/NOT IN scope,
   YAML frontmatter Jira fields, and `## Jira` when present. Do not modify Jira
   keys.
2. Document scope boundaries and deferred Work IDs **before** code scan.
3. List deferred CHOREs / future phases for out-of-scope items.

## Analysis Generation (Locked Scope Only)

4. Extract **domain keywords** (domain nouns and concepts, not file paths) for
   locked scope only.
5. Load `agent-context/memory/code-areas.md` and filter
   `agent-context/memory/context-index.md` and `agent-context/memory/domain-index.md`
   by keywords and related code areas. Read matches newest-first; do not scan the
   whole repository.
6. Locate relevant source files for locked scope only.
7. Identify existing vs new concepts, business rules, and risks within locked
   scope. Validate each concept against scope boundaries; move out-of-scope items
   to Deferred.
8. Record **code areas** for later phases.
9. Create or update the analysis artifact with **Scope Lock** after Metadata.
10. Tell the user to run
    `./scripts/sdlc-spdd/index-spdd-analysis.sh --target . --work-id <WORK-ID>`.
11. Recommend `/sdlc-spdd-plan` once analysis is accepted.

## Common Pitfalls

Scope creep before lock; reference bloat; layer bleed into other Work IDs. See
`docs/sdlc-spdd/analysis-phase-scope-validation.md` (or repo
`docs/analysis-phase-scope-validation.md`).

## Output


Create or update:

- `spdd/analysis/<WORK-ID>-analysis.md`
- `agent-context/features/<WORK-ID>/analysis-context.md`

Required sections: Metadata, **Scope Lock** (In / NOT / Reference-only), Domain
Keywords, Code Areas, Existing Concepts, New Concepts, Strategic Direction,
Risks and Gaps, Recommendation.

Print summary (include scope lock) and next command:
`/sdlc-spdd-plan @spdd/analysis/<WORK-ID>-analysis.md`.
