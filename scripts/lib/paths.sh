#!/usr/bin/env bash
# Path and lib-sourcing helpers for SDLC-SPDD scripts.

# Lib files copied into installed targets (scripts/sdlc-spdd/lib/).
SDLC_SHIPPED_LIB_FILES=(
  common.sh
  paths.sh
  areas.sh
  work-id.sh
  milestone.sh
  context-index.sh
  readiness.sh
)

# Orchestrator-only libs (never installed into targets).
SDLC_ORCHESTRATOR_ONLY_LIB_FILES=(
  shipped-docs-boundary.sh
  framework-install.sh
)

# Source a lib file from ${caller_dir}/lib/<name>.sh; fail loud if missing.
sdlc_require_lib() {
  local lib_name="$1"
  local caller_dir
  caller_dir="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
  local lib_path="${caller_dir}/lib/${lib_name}.sh"
  if [[ ! -f "${lib_path}" ]]; then
    echo "Error: missing shared library ${lib_path}" >&2
    echo "Re-run init-project.sh or upgrade-project.sh to install scripts/sdlc-spdd/lib/." >&2
    exit 1
  fi
  # shellcheck source=/dev/null
  source "${lib_path}"
}
