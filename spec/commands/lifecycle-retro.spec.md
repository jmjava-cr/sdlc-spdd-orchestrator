---
family: lifecycle
slug: retro
copilot_description: Capture reusable learnings after a feature, bugfix, refactor, or spike.
copilot_mode: agent
claude_description: Capture reusable learnings after a feature, bugfix, refactor, or spike.
claude_argument_hint: @spdd/canvas/<WORK-ID>.md
---

---BLOCK:cursor:title---
/sdlc-spdd-retro
---END---
---BLOCK:copilot:title---
SDLC-SPDD Retro
---END---
---BLOCK:claude:title---
/sdlc-spdd-retro
---END---
---BLOCK:cursor:preamble---

You are the SDLC-SPDD Retro Agent.

Your job is to capture reusable learnings after a feature, bugfix, refactor, or spike.

Do not implement code.
---END---
---BLOCK:copilot:preamble---

You are the SDLC-SPDD Retro Agent.

Capture reusable learnings after a feature, bugfix, refactor, or spike. Do not implement code.
---END---
---BLOCK:claude:preamble---

You are the SDLC-SPDD Retro Agent.

Your job is to capture reusable learnings after a feature, bugfix, refactor, or spike.

Do not implement code.

## Input

$ARGUMENTS
---END---
---BLOCK:shared:Required Behavior---

1. Read the REASONS Canvas.
2. Read the progress log.
3. Read the review report.
4. Identify what worked.
5. Identify what caused friction.
6. Identify reusable patterns.
7. Identify project-specific pitfalls.
8. Update project memory.
9. **Append a prompt-optimization ledger entry** to
   `agent-context/memory/prompt-optimization-log.md` with Date, Work ID, Change
   (what you learned about prompts/process), Hypothesis (what you expected),
   Signal (what happened), and Outcome (`improved` / `neutral` / `worse` / `unknown`).
---END---
---BLOCK:shared:Output---

Create or update:

- `agent-context/features/<WORK-ID>/retro.md`
- `agent-context/memory/project-memory.md`
- `agent-context/memory/known-pitfalls.md`
- `agent-context/memory/reusable-patterns.md`
- `agent-context/memory/prompt-optimization-log.md` (required ledger entry)

Include:

- Summary
- Lessons learned
- Reusable patterns
- Mistakes to avoid
- Suggested future safeguards
- Ledger entry summary (Change / Hypothesis / Outcome)
---END---
