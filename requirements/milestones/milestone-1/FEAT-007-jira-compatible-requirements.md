---
work_id: "FEAT-007-jira-compatible-requirements"
jira_key: ""
jira_epic: ""
jira_type: "Story"
jira_status: "Done"
jira_assignee: ""
jira_due_date: ""
jira_sprint: ""
milestone: "milestone-1"
blocks: []
depends_on:
  - "FEAT-006-analysis-scope-lock"
related:
  - "FEAT-008-milestone-subdirectory-layout"
---

# FEAT-007: Jira-Compatible Requirements Format

**Work ID:** FEAT-007-jira-compatible-requirements  
**Milestone:** Milestone 1 (Make it right)  
**Status:** Complete  
**Date:** 2026-07-15

## Related Work

| Relationship | Work ID | Status | Notes |
|--------------|---------|--------|-------|
| Depends On | FEAT-006-analysis-scope-lock | Complete | Analysis reads frontmatter during Scope Lock |
| Related | FEAT-008-milestone-subdirectory-layout | Complete | Shared milestone-N directory hierarchy |
| Source issue | issues/ENHANCEMENT-jira-compatible-requirements-format.md | Implemented | Origin ticket |

## Summary

Embed Jira metadata and dependency links in Markdown requirements (YAML frontmatter
+ Related Work + Scope), with templates and a format-only validation script.

## Source

- Roadmap: ROADMAP.md (make it right — planning artifacts / tracker alignment)
- Milestone: requirements/milestones/milestone-1/MILESTONE-1.md
- Issue: issues/ENHANCEMENT-jira-compatible-requirements-format.md

## Scope

### IN SCOPE

- Spec: `docs/jira-compatible-requirements-format.md`
- Templates: chore/feature requirements, `milestone-template.yml`
- `scripts/validate-requirements-format.sh` (shipped on init/upgrade)
- Analysis integration (read metadata; do not rewrite Jira keys)
- `create-work-from-milestone.sh` stubs with frontmatter + Scope + Related Work
- Docs: jira-runbook, context-loading, docs hub

### NOT IN SCOPE

- Live Jira API status sync from the validator
- Auto-migrating all existing flat requirements to frontmatter (optional warnings only)
- Replacing the `## Jira` copy-paste create flow (kept alongside frontmatter)

## Acceptance Criteria

- [x] Format specification documented
- [x] Requirement + milestone templates checked in
- [x] Validation script checks keys, Work ID refs, `_milestone.yml` presence
- [x] Analysis prompt extracts Jira context read-only
- [x] Migration guidance documented (with FEAT-008 migration doc)

## Jira

- Key: TBD
- Issue type: Story
- Summary: Jira-compatible requirements frontmatter and validation
- Labels: sdlc-spdd, jira, requirements, make-it-right

## Next Step

Implementation landed on `cursor/integration-981e`. Optionally add frontmatter to
legacy flat stubs under `requirements/milestones/*.md` when next touched.
