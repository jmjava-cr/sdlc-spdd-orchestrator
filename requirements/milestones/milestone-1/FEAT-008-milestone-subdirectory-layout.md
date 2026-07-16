---
work_id: "FEAT-008-milestone-subdirectory-layout"
jira_key: ""
jira_epic: ""
jira_type: "Story"
jira_status: "Done"
jira_assignee: ""
jira_due_date: ""
jira_sprint: ""
milestone: "milestone-1"
blocks: []
depends_on: []
related:
  - "FEAT-007-jira-compatible-requirements"
---

# FEAT-008: Milestone Files in Subdirectories

**Work ID:** FEAT-008-milestone-subdirectory-layout  
**Milestone:** Milestone 1 (Make it right)  
**Status:** Complete  
**Date:** 2026-07-15

## Related Work

| Relationship | Work ID | Status | Notes |
|--------------|---------|--------|-------|
| Related | FEAT-007-jira-compatible-requirements | Complete | `_milestone.yml` + nested stubs |
| Source issue | issues/REQUIREMENT-001-milestone-files-in-subdirectories.md | Implemented | Origin ticket |

## Summary

Support milestone definitions and requirement stubs under
`requirements/milestones/milestone-N/` while keeping root `milestone-*.md` working.
New installs prefer the subdirectory layout.

## Source

- Roadmap: ROADMAP.md (make it right — planning layout / root declutter)
- Milestone: requirements/milestones/milestone-1/MILESTONE-1.md
- Issue: issues/REQUIREMENT-001-milestone-files-in-subdirectories.md

## Scope

### IN SCOPE

- `scripts/lib/milestone.sh` discovery (root + subdirectory; prefer subdir)
- Init/upgrade scaffold for `milestone-1/MILESTONE-1.md` + `_milestone.yml`
- `create-work-from-milestone.sh` writes stubs into the milestone directory
- Team registry / workflow requirement path resolution for nested stubs
- Docs + `docs/MIGRATION-root-to-subdirectories.md`
- Grounding files mention both patterns

### NOT IN SCOPE

- Forced migration of all existing projects' root milestones
- Auto-deleting root `milestone-*.md` files
- Reorganizing `spdd/canvas/` into milestone subdirs (already optional elsewhere)

## Acceptance Criteria

- [x] New project scaffold creates subdirectory milestone layout
- [x] Scripts discover root and subdirectory definitions (backward compatible)
- [x] Documentation and grounding updated
- [x] Migration guide available
- [x] This repo dogfoods the layout (canonical MILESTONE-1 under `requirements/milestones/milestone-1/`)

## Jira

- Key: TBD
- Issue type: Story
- Summary: Support milestone files in requirements/milestones subdirectories
- Labels: sdlc-spdd, milestones, make-it-right

## Next Step

Implementation landed on `cursor/integration-981e`. This orchestrator repo now uses
the subdirectory as the canonical Milestone 1 definition; root `milestone-1.md` is
a compatibility stub.
