# Enhancement: Add Scope Lock-In to Analysis Phase (Prevent Scope Creep)

**Status:** Implemented (on `cursor/integration-981e`)  
**Date:** 2026-07-10  
**Implemented:** 2026-07-15  
**Framework Area:** Analysis Phase (`sdlc-spdd-analysis` workflow)

---

## Problem Statement

The analysis phase workflow generates comprehensive analysis artifacts without upfront scope validation. This leads to **scope creep** — analysis sections that include concepts, code areas, and acceptance criteria outside a CHORE's declared scope.

### Observed Pattern

When implementing database schema CHOREs, analysis generated included:
- Entity mapping concepts (belongs to API layer CHORE)
- Repository/service layer recommendations (belongs to separate CHORE)
- Integration point recommendations (belongs to later phase)
- Reference material that contextualizes but doesn't inform scope

**Result:** Multiple iterations removing out-of-scope sections → delayed architect/code phases

### Root Cause

Analysis prompt does not require scope lock-in **before** generation. Analysis is generated from requirements, then manually refined against scope boundaries afterward.

---

## Desired State

Analysis phase enforces **scope lock-in checkpoint** before generation:

1. **Read requirements document** — Identify declared scope boundaries
2. **Lock scope explicitly** — Document what IS and IS NOT in scope
3. **Identify deferred CHOREs** — Where does out-of-scope work belong?
4. **Generate analysis** — Only for locked scope items
5. **Validate sections** — Remove reference material outside boundaries
6. **Accept analysis** — Scope is now locked for architect/code phases

---

## Acceptance Criteria

- [x] **Framework Update:** Analysis phase prompt (`sdlc-spdd-analysis.prompt.md`) includes "Scope Lock-In" section before "Analysis Generation"
- [x] **Output Requirement:** Analysis artifact includes **Scope Lock** as first major section (what IS / IS NOT in scope)
- [x] **Validation Step:** Analysis generation section explicitly validates scope boundaries for each concept
- [x] **Guidance Document:** Reference document explains scope validation patterns and common pitfalls (`docs/analysis-phase-scope-validation.md`)
- [ ] **Testing:** Validate with new CHORE in future milestone — confirm scope lock prevents iterative refinement

---

## Implementation Plan

### Phase 1: Framework Prompt Update

**File:** `prompts/sdlc-spdd-analysis.prompt.md` (or equivalent in orchestrator)

**Changes:**
1. Add "Scope Lock-In (Before Analysis Generation)" section (2-3 steps)
2. Update "Analysis Generation (Locked Scope Only)" section with validation guidance
3. Add "Common Pitfalls" section warning against scope creep and reference bloat
4. Update Output requirements to include "Scope Lock" as required first section

**Example Section Structure:**
```markdown
## Scope Lock-In (Before Analysis Generation)

1. **Read Requirements Document** — Verify WORK-ID's declared scope from requirements/ artifact
2. **Document Scope Boundaries** — What IS in scope? What IS NOT? Where does deferred work belong?
3. **List Deferred CHOREs** — For out-of-scope work, identify target CHORE or future phase

[Continue with Analysis Generation (Locked Scope Only)]

## Common Pitfalls

**Scope Creep Before Lock:** Do not generate analysis and then discover scope issues afterward. Lock scope upfront.

**Reference Bloat:** Analysis should only include existing concepts that inform this CHORE. Exclude pre-existing patterns, interfaces, and handlers that are context-only.
```

### Phase 2: Guidance Document

Create `docs/sdlc-spdd/analysis-phase-scope-validation.md`:
- Explain why scope lock-in matters
- Document common scope creep patterns (e.g., including entity/repository when only schema is in scope)
- Provide checklist for analysts
- Link to examples from real CHOREs

### Phase 3: Validation

Run analysis phase on next CHORE with updated prompt:
- Verify scope lock-in checkpoint catches boundary issues
- Confirm no iterative scope refinement needed afterward
- Document lessons learned in CHANGELOG

---

## Technical Notes

### Scope Lock Section Format (Recommended)

```markdown
## Scope Lock

### In Scope for This CHORE
- Primary deliverable (schema, feature, integration, etc.)
- Direct dependencies only

### NOT in Scope (Deferred)
- Related work that belongs to separate CHOREs
- Integration points that belong to later phases

### Reference Materials (Context Only, Not Deliverables)
- Existing patterns and infrastructure that inform scope
- External systems and services (context reference)
```

### Scope Validation Checklist (For Prompt)

For each analysis section (New Concepts, Code Areas, Acceptance Criteria):
- [ ] Does this section address locked scope items?
- [ ] If reference material, does it inform locked scope?
- [ ] Should this be moved to deferred CHOREs section?
- [ ] Remove if out-of-scope

---

## Impact & Benefits

| Benefit | Impact |
|---------|--------|
| **Faster Analysis→Architect Transition** | No iterative scope refinement; analyst can move to architect phase immediately |
| **Clear Deferred Work Queue** | Deferred CHOREs documented; prevents forgotten scope items |
| **Reduced Rework** | Scope defined upfront prevents code phase surprises |
| **Better Team Communication** | Explicit scope lock shared in artifact; team alignment |

---

## Implementation Timeline

- **Phase 1 (Framework):** 1-2 hours — Update prompt + add pitfalls section
- **Phase 2 (Guidance):** 1-2 hours — Write reference document
- **Phase 3 (Validation):** Integrated into next CHORE workflow (no extra time)

---

## Questions for Stakeholders

1. Should scope lock be enforced as a gate (prevent analysis generation without explicit scope lock section)?
2. Should deferred work be captured in a separate "Backlog" artifact or within analysis?
3. Are there other SDLC phases that would benefit from similar scope validation (e.g., Plan phase)?
