# scripts/lib — shared bash helpers

Sourced library files for SDLC-SPDD runtime scripts. Not executed directly.

## Layout

| File | Shipped to targets? | Purpose |
|------|---------------------|---------|
| `common.sh` | yes | Timestamps, target resolve, dry-run mkdir, oneline |
| `paths.sh` | yes | `sdlc_require_lib`, shipped lib manifest |
| `areas.sh` | yes | `normalize_area`, `normalize_token`, `parse_section_bullets` |
| `work-id.sh` | yes | `slugify`, `next_work_number`, `work_type_prefix` |
| `milestone.sh` | yes | `resolve_milestone` (absolute or relative paths) |
| `context-index.sh` | yes | Context index header + `prepend_context_index_rows` |
| `shipped-docs-boundary.sh` | no | Orchestrator doc install skip list |

## Sourcing convention

**Orchestrator** (`scripts/<script>.sh`):

```bash
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${_SCRIPT_DIR}/lib/areas.sh"
```

**Installed target** (`scripts/sdlc-spdd/<script>.sh`):

```bash
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${_SCRIPT_DIR}/lib/areas.sh"
```

Same relative path — `init-project.sh` / `upgrade-project.sh` copy `scripts/lib/*.sh`
to `${TARGET}/scripts/sdlc-spdd/lib/`.

## Install

Shipped libs are installed by `init-project.sh` and upgraded by `upgrade-project.sh`
alongside runtime scripts under `scripts/sdlc-spdd/`.
