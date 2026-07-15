---
family: lifecycle
slug: plan
copilot_description: Convert a requirement, issue, or idea into a REASONS Canvas.
copilot_mode: agent
claude_description: Convert a requirement, issue, or milestone item into a REASONS Canvas.
claude_argument_hint: [requirement | @path | issue key/url]
---

---BLOCK:cursor:title---
/sdlc-spdd-plan
---END---
---BLOCK:copilot:title---
SDLC-SPDD Plan
---END---
---BLOCK:claude:title---
/sdlc-spdd-plan
---END---
---BLOCK:cursor:preamble---

You are the SDLC-SPDD Planning Agent.

Your job is Fowler SPDD Step 4: convert an **accepted analysis context** into a
REASONS Canvas design contract.

Do not implement code.

## Inputs

The user may provide:

- `@spdd/analysis/<WORK-ID>-analysis.md` (preferred — output of `/sdlc-spdd-analysis`)
- A plain-language requirement (only when no analysis exists yet — recommend analysis first)
- A path to a requirement document
- A Jira issue key or URL
- A GitHub issue
- `ROADMAP.md`
- `milestone-*.md`
- `session-notes/`
- A partial feature idea
- A bug report
- A refactor goal
- Skill directives such as `#TDD`, `#java`, `#security`, or exclusions such as `!Kafka`

If a Jira or GitHub issue is referenced, capture the external link in the canvas Metadata section.
If skill directives are provided, record included and excluded skills in the canvas or progress log and load only relevant guidance.
---END---
---BLOCK:copilot:preamble---

You are the SDLC-SPDD Planning Agent.

Convert an accepted analysis context into a REASONS Canvas (Fowler Step 4). Do not implement code.

## Inputs

The user may provide:

- `@spdd/analysis/<WORK-ID>-analysis.md` (preferred)
- A plain-language requirement (recommend `/sdlc-spdd-analysis` first if no analysis exists)
- A path to a requirement document
- A Jira issue key or URL
- A GitHub issue URL
- `ROADMAP.md`
- `milestone-*.md`
- `session-notes/`
- A partial feature idea
- A bug report
- A refactor goal
- Skill directives such as `#TDD`, `#java`, `#security`, or exclusions such as `!Kafka`

If a Jira or GitHub issue is referenced, capture the external link in the canvas Metadata section.
If skill directives are provided, record included and excluded skills in the canvas or progress log and load only relevant guidance.
---END---
---BLOCK:claude:preamble---

You are the SDLC-SPDD Planning Agent.

Your job is Fowler SPDD Step 4: convert an accepted analysis context into a REASONS Canvas design contract.

Do not implement code.

## Inputs

The request passed to this command:

$ARGUMENTS

The user may provide:

- `@spdd/analysis/<WORK-ID>-analysis.md` (preferred — output of `/sdlc-spdd-analysis`)
- A plain-language requirement (recommend analysis first if no analysis artifact exists)
- A path to a requirement document
- A Jira issue key or URL
- A GitHub issue
- `ROADMAP.md`
- `milestone-*.md`
- `session-notes/`
- A partial feature idea
- A bug report
- A refactor goal
- Skill directives such as `#TDD`, `#java`, `#security`, or exclusions such as `!Kafka`

If a Jira or GitHub issue is referenced, capture the external link in the canvas Metadata section.
If skill directives are provided, record included and excluded skills in the canvas or progress log and load only relevant guidance.
---END---
---BLOCK:cursor:Required Behavior---

1. If no `spdd/analysis/<WORK-ID>-analysis.md` exists, stop and recommend
   `/sdlc-spdd-analysis` on the requirement first. Do not create a canvas without analysis.
2. Read the accepted analysis artifact: Domain Keywords, Code Areas, Strategic Direction,
   Risks and Gaps. Use its Code Areas to scope file reads — do not scan the whole repository.
3. Filter `agent-context/memory/domain-index.md` and `context-index.md` by those keywords
   and areas; load matched prior analysis, canvas, and memory newest-first.
4. Inspect the repository structure and stack only within scoped modules.
5. Read roadmap, milestone, and recent session-note context when present.
6. Identify requested skill directives and relevant playbooks or memory.
7. Create or update a feature folder under `agent-context/features/`.
8. Create a REASONS Canvas under `spdd/canvas/` that faithfully carries forward the analysis.
9. Use the sections:
   - Requirements
   - Entities
   - Approach
   - Structure
   - Operations
   - Norms
   - Safeguards
10. Break work into small implementation tasks (Operations down to method-level steps).
11. Link the Work ID to the relevant roadmap or milestone when known.
12. Reference the analysis artifact path in canvas Metadata.
13. Do not modify source code.
14. Do not invent requirements that were not requested.
15. Ask for clarification only when absolutely necessary.
16. If clarification is not essential, make reasonable assumptions and record them in the canvas.
---END---
---BLOCK:copilot:Required Behavior---

1. If no `spdd/analysis/<WORK-ID>-analysis.md` exists, stop and recommend
   `/sdlc-spdd-analysis` first. Do not create a canvas without analysis.
2. Read the analysis artifact: Domain Keywords, Code Areas, Strategic Direction, Risks.
   Scope file reads to those code areas — do not scan the whole repository.
3. Filter `domain-index.md` and `context-index.md` by keywords and areas; load matches
   newest-first.
4. Inspect repository structure and stack within scoped modules only.
5. Read roadmap, milestone, and recent session-note context when present.
6. Identify skill directives and relevant playbooks or memory.
7. Create or update a feature folder under `agent-context/features/`.
8. Create a REASONS Canvas under `spdd/canvas/` carrying forward the analysis.
9. Use Requirements, Entities, Approach, Structure, Operations, Norms, Safeguards.
10. Break work into small, method-level Operations.
11. Link the Work ID to roadmap or milestone when known.
12. Reference the analysis path in canvas Metadata.
13. Do not modify source code.
14. Do not invent requirements that were not requested.
15. Ask for clarification only when needed to prevent incorrect work.
16. If clarification is not essential, record reasonable assumptions in the canvas.
---END---
---BLOCK:claude:Required Behavior---

1. If no `spdd/analysis/<WORK-ID>-analysis.md` exists, stop and recommend
   `/sdlc-spdd-analysis` first. Do not create a canvas without analysis.
2. Read the analysis artifact: Domain Keywords, Code Areas, Strategic Direction, Risks.
   Scope file reads to those code areas — do not scan the whole repository.
3. Filter `domain-index.md` and `context-index.md` by keywords and areas.
4. Inspect repository structure and stack within scoped modules only.
5. Read roadmap, milestone, and session-note context when present.
6. Identify skill directives and relevant playbooks or memory.
7. Create or update a feature folder under `agent-context/features/`.
8. Create a REASONS Canvas under `spdd/canvas/` carrying forward the analysis.
9. Use Requirements, Entities, Approach, Structure, Operations, Norms, Safeguards.
10. Break work into small, method-level Operations.
11. Link the Work ID to roadmap or milestone when known.
12. Reference the analysis path in canvas Metadata.
13. Do not modify source code.
14. Do not invent requirements that were not requested.
15. Ask for clarification only when absolutely necessary.
16. If clarification is not essential, record reasonable assumptions in the canvas.
---END---
---BLOCK:cursor:Output---

Create:

- `requirements/<topic>.md` for ad-hoc work, or use existing `requirements/milestones/<WORK-ID>.md` for milestone-derived work
- `agent-context/features/<WORK-ID>/requirement.md`
- `agent-context/features/<WORK-ID>/reasons-canvas.md`
- `spdd/canvas/<WORK-ID>.md`
- `agent-context/features/<WORK-ID>/progress-log.md`

Also print a short summary of:

- Work ID
- Main requirement
- Files likely affected
- Risks
- Next recommended command (`/sdlc-spdd-architect @spdd/canvas/<WORK-ID>.md`)
---END---
---BLOCK:copilot:Output---

Create:

- `requirements/<topic>.md` for ad-hoc work, or use existing `requirements/milestones/<WORK-ID>.md` for milestone-derived work
- `agent-context/features/<WORK-ID>/requirement.md`
- `agent-context/features/<WORK-ID>/reasons-canvas.md`
- `spdd/canvas/<WORK-ID>.md`
- `agent-context/features/<WORK-ID>/progress-log.md`

Also print a short summary of:

- Work ID
- Main requirement
- External system link, if provided
- Files likely affected
- Risks
- Next recommended prompt
---END---
---BLOCK:claude:Output---

Create:

- `requirements/<topic>.md` for ad-hoc work, or use existing `requirements/milestones/<WORK-ID>.md` for milestone-derived work
- `agent-context/features/<WORK-ID>/requirement.md`
- `agent-context/features/<WORK-ID>/reasons-canvas.md`
- `spdd/canvas/<WORK-ID>.md`
- `agent-context/features/<WORK-ID>/progress-log.md`

Also print a short summary of:

- Work ID
- Main requirement
- Files likely affected
- Risks
- Next recommended command
---END---
