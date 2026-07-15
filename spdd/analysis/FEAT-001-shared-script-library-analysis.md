# Analysis: FEAT-001-shared-script-library

**Work ID:** FEAT-001-shared-script-library  
**Canvas:** `spdd/canvas/FEAT-001-shared-script-library.md`  
**Date:** 2026-07-15  
**Branch:** `cursor/integration-981e`  
**Operation:** T01 — inventory duplication

---

## Scope

Inventory duplicated bash logic across `scripts/*.sh` to plan a behavior-identical extraction into `scripts/lib/`. Confirm duplicates are mechanical (same intent) and decide lib grouping plus the sourcing convention for orchestrator vs installed targets (`scripts/sdlc-spdd/`).

**Scripts surveyed:** 27 files under `scripts/` (26 `*.sh` + `scripts/lib/shipped-docs-boundary.sh`).

---

## Findings summary

| Category | Scripts affected | Extract to |
|----------|------------------|------------|
| `usage()` + `--target`/`--help` arg loops | ~24 | `lib/common.sh` |
| `SCRIPT_DIR` / `REPO_ROOT` / `TARGET` resolution | ~20 | `lib/common.sh`, `lib/paths.sh` |
| Timestamps (`date -u` formats) | 7 | `lib/common.sh` |
| Dry-run helpers | 12+ | `lib/common.sh` |
| `slugify` / Work-ID numbering | 2 | `lib/work-id.sh` |
| `context-index.md` read/write | 3 | `lib/context-index.sh` |
| Area normalization / `code-areas.md` | 3 | `lib/areas.sh` |
| `resolve_milestone()` | 2 | `lib/milestone.sh` |
| Framework install copy helpers | 2 (`init`, `upgrade`) | `lib/framework-install.sh` (orchestrator-only) |

Only `scripts/lib/shipped-docs-boundary.sh` is sourced today. **`scripts/lib/` is not copied** to installed targets — install/upgrade must be extended before shipped scripts can source libs.

---

## 1. Argument parsing and target resolution

**Pattern:** `usage()` heredoc → `TARGET="."` → `while case --target|--help|--dry-run` → `TARGET="$(cd "${TARGET}" && pwd)"`.

**Scripts:** `capture-session-memory.sh`, `resolve-agent-context.sh`, `index-spdd-analysis.sh`, `start-agent-session.sh`, `create-work-from-milestone.sh`, `sync-agent-context.sh`, `validate-command-adapters.sh`, `upgrade-project.sh`, `init-project.sh`, and ~15 more.

**Exceptions:**

- `validate-reasons-canvas.sh` — positional file arg, no `--target`
- `sdlc.sh` — thin wrapper, adaptive root
- `deploy-docs-pages-local.sh` — no `--target`

**Recommendation:** `parse_standard_args` or documented copy-paste macro in `lib/common.sh` with flags for required-target vs optional-target.

---

## 2. Path resolution

| Pattern | Where |
|---------|-------|
| `SCRIPT_DIR` + `REPO_ROOT` | `init-project.sh`, `upgrade-project.sh`, `install-*`, `setup-agent-prompts.sh` |
| `TARGET` only | Shipped runtime scripts (`capture-*`, `resolve-*`, `index-*`, etc.) |
| Adaptive sibling script lookup | `start-agent-session.sh` already resolves `scripts/sdlc-spdd/` vs `scripts/` |

**Installed-target convention (proposed):**

```bash
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${_SCRIPT_DIR}/lib/common.sh"
```

Requires `init-project.sh` / `upgrade-project.sh` to copy `scripts/lib/*.sh` → `${TARGET}/scripts/sdlc-spdd/lib/`.

---

## 3. Work-ID helpers (`lib/work-id.sh`)

**Today:** `slugify()` only in `create-work-from-milestone.sh`; inline slug in `create-feature.sh`.

**Behavior differences (must unify before extract):**

| Concern | `create-work-from-milestone` | `create-feature` |
|---------|------------------------------|------------------|
| Slug chars | `_ /` → `-`, strip non-alnum | `_ ` → `-` only |
| Empty slug fallback | `milestone-work` | none |
| Number scan | `features/` + `spdd/canvas/` | `features/` only |
| Type alias | `bug` / `bugfix` | `bug` only |

**Recommendation:** Single `slugify [--mode strict|legacy]` and `next_work_number --scan PATH…` with configurable globs. No shared Work-ID format validator exists today — add optional `require_work_id` for emptiness only (preserve current behavior).

---

## 4. Context index (`lib/context-index.sh` + `lib/areas.sh`)

**Consumers:**

| Script | Role |
|--------|------|
| `resolve-agent-context.sh` | Read/filter rows by area |
| `capture-session-memory.sh` | Prepend rows (session, decision, pitfall, pattern) |
| `index-spdd-analysis.sh` | Replace prior `analysis` rows for Work ID, then prepend |

**Shared sub-patterns:** `normalize_area()`, `parse_section_bullets()`, `code-areas.md` registry — duplicated across all three.

**Blocking differences:**

1. **Write mode:** prepend-only (capture) vs replace-by-`(kind, work_id)` (index)
2. **Header text:** capture includes `Kinds: analysis, session, …`; index-spdd-analysis omits
3. **Area on read:** resolve filters lowercase normalized; capture writes canonical registry spelling

**Recommendation:** Two write functions: `context_index_prepend_rows` and `context_index_replace_kind_rows`. One read: `context_index_filter_by_areas`. Unify header constant before extraction.

---

## 5. Milestone resolution (`lib/milestone.sh`)

`resolve_milestone()` duplicated in `capture-session-memory.sh` and `start-agent-session.sh`.

**Difference:** capture returns **absolute** paths; start returns **relative to TARGET**.

**Recommendation:** Single function with `--relative|--absolute` return mode.

---

## 6. Dry-run semantics

Not uniform — extraction must preserve per-script behavior:

| Script | Dry-run behavior |
|--------|------------------|
| `resolve-agent-context.sh` | Documented no-op (symmetry only) |
| `capture-session-memory.sh` | Early `exit 0` before any writes |
| `index-spdd-analysis.sh` | Lists plan, exits before writes |
| `init-project.sh` / `upgrade-project.sh` | `[dry-run]` prefix on copy/mkdir helpers |

**Recommendation:** Generic helpers for mkdir/cp/echo only; do not wrap resolve-agent-context dry-run.

---

## 7. Proposed `scripts/lib/` layout

| File | Shipped to targets? | Contents |
|------|---------------------|----------|
| `common.sh` | yes | Args, target resolve, timestamps, dry-run mkdir/cp, `die` |
| `paths.sh` | yes | Script dir, optional repo root |
| `work-id.sh` | yes | slugify, next number, type prefix |
| `areas.sh` | yes | normalize_area, code-areas registry |
| `context-index.sh` | yes | read/write context-index.md |
| `milestone.sh` | yes | resolve_milestone |
| `shipped-docs-boundary.sh` | no (orchestrator) | existing |
| `framework-install.sh` | no | shared init/upgrade copy helpers |

---

## 8. Consumer migration order (T03 clusters)

1. **Cluster A — index/read:** `resolve-agent-context.sh`, `index-spdd-analysis.sh` (areas + context-index)
2. **Cluster B — capture/write:** `capture-session-memory.sh` (depends on Cluster A libs)
3. **Cluster C — session:** `start-agent-session.sh` (milestone + common)
4. **Cluster D — work creation:** `create-work-from-milestone.sh`, `create-feature.sh` (work-id)
5. **Cluster E — install scripts:** `init-project.sh`, `upgrade-project.sh` (copy lib + framework-install)
6. **Cluster F — remaining arg-loop scripts:** install-*, sync-*, validate-* (common.sh only)

Validate after each cluster: existing test harnesses unchanged.

---

## 9. Install/upgrade changes required (T02 prerequisite)

Extend `init-project.sh` and `upgrade-project.sh`:

```bash
# Copy lib alongside runtime scripts
mkdir -p "${TARGET}/scripts/sdlc-spdd/lib"
for f in "${REPO_ROOT}/scripts/lib/"*.sh; do
  # skip orchestrator-only libs (shipped-docs-boundary, framework-install)
  cp … "${TARGET}/scripts/sdlc-spdd/lib/"
done
```

Orchestrator scripts continue to source `"${SCRIPT_DIR}/lib/…"`.

---

## 10. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Subtle slugify divergence | Unified helper with explicit mode; test both create scripts |
| context-index header drift | Pick one canonical header before extract |
| Missing lib in installed target | Fail loud if `lib/common.sh` not found |
| Dry-run behavior change | Per-script tests; no generic wrapper on resolve dry-run |

---

## 11. Open questions resolved

| Question (canvas) | Decision |
|-------------------|----------|
| One `common.sh` vs focused libs? | **Focused libs** (table above); `common.sh` for universal plumbing |
| Installed lib path? | `scripts/sdlc-spdd/lib/` copied by init/upgrade |
| Grouping | See section 7 |

---

## 12. Recommendation for T02

Proceed with `lib/common.sh` + install copy plumbing first, then `areas.sh` + `context-index.sh` (highest duplication ROI), then `work-id.sh` + `milestone.sh`.

Canvas readiness after this analysis: **Ready For Architect review** (T01 complete; T02–T04 still pending).
