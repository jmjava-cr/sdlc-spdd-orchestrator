# Analysis: FEAT-005-canvas-readiness-indicators

**Work ID:** FEAT-005-canvas-readiness-indicators  
**Requirement:** `requirements/milestones/FEAT-005-canvas-readiness-indicators.md`  
**Date:** 2026-07-15  
**Branch:** `cursor/integration-981e`  
**Phase:** analysis

---

## Metadata

- Depends on: FEAT-004-prompt-optimization-ledger (Complete — Kind: `metric` exists)
- Milestone: `requirements/milestones/milestone-1/MILESTONE-1.md`
- Domain keywords: readiness, canvas, validate-reasons-canvas, capture metrics, leading indicators

## Domain Keywords

- readiness
- canvas
- validate-reasons-canvas
- leading indicators
- metric
- FEAT-004

## Code Areas

- scripts/validate-reasons-canvas.sh
- scripts/capture-session-memory.sh
- docs/context-loading-and-scaling.md
- spdd/canvas

## Scope Lock

### IN SCOPE

- Fixed readiness vocabulary and where it lives on the canvas
- `validate-reasons-canvas.sh` reads/validates readiness (optional → missing OK)
- Capture-time leading indicators for validate/review cycle counts (Kind: `metric`)
- Docs describing vocabulary + indicators (ship-neutral)

### NOT IN SCOPE

- Scoring, ranking, or acting on indicators
- Migrating every historical canvas to YAML frontmatter
- Changing FEAT-004 `--rework` semantics
- New datastore or `spdd --metrics` query surface

### Reference-only

- Existing Metadata bullet `- Readiness: …` on canvases (reuse, do not invent a second prose field)
- FEAT-004 `--readiness` capture flag (already present)
- `check-posture-boundary.sh` for shipped docs wording

---

## Findings

### Current state

| Artifact | Behavior today |
|----------|----------------|
| Canvas Metadata | Prose bullet `- Readiness: Ready For Coding` (etc.) — not validated |
| `validate-reasons-canvas.sh` | Section presence only; no readiness check |
| `capture-session-memory.sh` | Optional `--readiness` string → Kind: `metric` (FEAT-004) |
| Canvas templates | No dedicated scaffold template file; canvases authored by plan |

### Open questions → proposed resolution

| Question | Decision |
|----------|----------|
| Vocabulary | Fixed enum (kebab + Title Case aliases): `needs-analysis`, `needs-clarification`, `ready-for-coding`, `reviewed`, `complete` |
| Placement | Prefer optional YAML frontmatter `readiness:`; else Metadata `- Readiness:` bullet. Either is enough. |
| Cycle counts | Capture optional `--validate-cycles` / `--review-cycles` (non-negative ints) into the same Kind: `metric` row — do not scrape logs |

### Code areas

- `scripts/validate-reasons-canvas.sh`
- `scripts/capture-session-memory.sh`
- `docs/context-loading-and-scaling.md` (or small dedicated doc linked from docs hub)
- Existing canvases (backward compatible — no mass edit required)

### Risks

- Unknown readiness value must **warn**, not fail validation (older canvases / free-text notes like `Reviewed — Approved With Notes` normalize via prefix `reviewed`).
- Ship-neutral: docs describe capability, not make-it-fast posture.

### Recommended operations

1. T01 — Encode vocabulary + placement in canvas Resolved Decisions + short doc section
2. T02 — Teach `validate-reasons-canvas.sh` to parse/validate (warn on unknown; OK if absent)
3. T03 — Add `--validate-cycles` / `--review-cycles` to capture → metric entry
4. T04 — Document vocabulary + indicators

### Next command

```
/sdlc-spdd-plan @spdd/analysis/FEAT-005-canvas-readiness-indicators-analysis.md
```
(Canvas already exists — advance to architect / Ready For Coding with Resolved Decisions, then code T01.)
