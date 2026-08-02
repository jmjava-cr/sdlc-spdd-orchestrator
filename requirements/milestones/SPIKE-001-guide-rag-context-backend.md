---
work_id: "SPIKE-001-guide-rag-context-backend"
jira_key: ""
jira_epic: ""
jira_type: "Story"
jira_status: "Draft"
jira_assignee: ""
jira_due_date: ""
jira_sprint: ""
milestone: "milestone-1"
blocks: []
depends_on: []
related: []
---

# Requirement: SPIKE-001-guide-rag-context-backend

## Summary

Time-boxed feasibility spike: evaluate using the Embabel **guide** project (a RAG MCP
server over Neo4j) as an *optional* retrieval/memory backend for the orchestrator —
storing work memory as we go and retrieving the most relevant of it before composing
prompt context, to optimize outcomes.

## Source

- Roadmap: ROADMAP.md (make it fast — optimization; parked behind FEAT-004/005)
- Milestone: none (not part of milestone-1 / make it right)

## Question to answer

Does retrieving context from guide's Neo4j RAG before composing a prompt measurably
improve outcomes (lower rework, stable/better review-result, fewer/looser tokens)
versus today's markdown `context-index.md` + `resolve-agent-context.sh` resolver —
enough to justify an optional JVM + Neo4j dependency?

## Why a spike (not a feature)

It introduces a heavy runtime dependency (JVM + Neo4j + a guide instance) onto a
deliberately markdown-first, portable framework. We must prove value on real sessions
before committing. The output is a **decision**, not production code.

## Success / decision criteria

- [ ] SDLC-SPDD DICE entity schema designed (`spdd/analysis/SPIKE-001-dice-entity-schema.md`).
- [ ] Entity projection ingest loads at least one Work ID subgraph into Neo4j `__Entity__`.
- [ ] A measured A/B on at least one real Work ID: guide-RAG retrieval vs. current resolver, scored on the FEAT-004 ledger (rework, review-result) and approximate context tokens.
- [ ] A clear go / no-go recommendation with the trade-offs (value vs. dependency/adoption cost).
- [ ] If go: a sketch of the follow-on FEAT(s) — DICE entity ingest, retrieval seam, and (optionally) a live `remember()` write tool in the fork.

## Dependencies / sequencing

- After FEAT-004 (ledger) exists — it is the scoreboard this spike needs.
- Independent of the make-it-right refactors except that they come first.

## Non-Goals

- No production integration, no required dependency, no changes to the default
  markdown-first path.
- Markdown-first path remains the default; Guide stays optional and runtime-resolved.
- T06 **provisional go** (2026-08-01): optional Guide path + ops console are on `main`
  for field confirmation ([#56](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/56)).

## Branch policy

Spike exploration lived on `cursor/spike-*` branches (draft PR #24). Product path for
field dogfood is now `main`. Guide projection ships as tag **`sdlc-spdd-projection-v1`**
on `jmjava/guide` (after [guide #2](https://github.com/jmjava/guide/pull/2)). Default
installs still must not *require* Guide — only `--with-guide` / harness marker opt-in.

## Next Step

Field-confirm Guide retrieval vs files on real Work IDs:

    ./scripts/sdlc.sh console --target .   # Guide tab + ADF launch — docs/ops-console.md
    # pin: GUIDE_GIT_REF defaults to sdlc-spdd-projection-v1

See [docs/guide-flow.md](../../docs/guide-flow.md) and
[docs/dice-projection-runbook.md](../../docs/dice-projection-runbook.md).

## Jira

Draft for issue creation — paste into Jira UI, MCP, or approved API.
After create, set **Key** and commit.

- Key: TBD
- Issue type: Story
- Summary: 
- Labels:

## GitHub

Optional — use when tracking is GitHub Issues instead of/in addition to Jira.

- Number: TBD
- Title: 
- Labels: 
- URL:
