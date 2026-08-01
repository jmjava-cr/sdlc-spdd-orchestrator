#!/usr/bin/env bash
# Runtime resolution of the SPDD context backend.
#
# The file-based indexes (agent-context/memory/*) are ALWAYS the baseline.
# Guide DICE (Neo4j entity graph behind the Guide MCP/HTTP API) is an optional
# augmentation, resolved at runtime in two steps:
#
#   1. Opt-in:    agent-context/harness/guide-dice.md exists in the install.
#                 Installs without it never probe the network.
#   2. Liveness:  the Guide stats endpoint answers within the probe timeout.
#
# Output is stable key=value lines so both agents and scripts can parse it.
# The script never exits non-zero for "Guide absent" — files is a valid answer.
#
# Usage:
#   resolve-context-backend.sh [--target <path>]            probe and report
#   resolve-context-backend.sh --project [--target <path>] [--work-id <id>]
#       additionally POST a projection load (persist side) when guide-dice
#       is live; silently a no-op (exit 0) when the backend is files.
set -euo pipefail

TARGET="."
MODE="probe"
WORK_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --project)
      MODE="project"
      shift
      ;;
    --work-id)
      WORK_ID="${2:-}"
      shift 2
      ;;
    --help|-h)
      sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

TARGET="$(cd "${TARGET}" && pwd)"
MARKER="${TARGET}/agent-context/harness/guide-dice.md"

if [[ ! -f "${MARKER}" ]]; then
  echo "CONTEXT_BACKEND=files"
  echo "REASON=guide-dice not enabled for this install (no agent-context/harness/guide-dice.md)"
  exit 0
fi

# Endpoint resolution: env var beats marker-file `endpoint:` line beats default.
marker_endpoint="$(grep -E '^endpoint:' "${MARKER}" 2>/dev/null | head -1 | sed 's/^endpoint:[[:space:]]*//' || true)"
GUIDE_PORT="${GUIDE_PORT:-21337}"
GUIDE_BASE_URL="${GUIDE_BASE_URL:-${marker_endpoint:-http://localhost:${GUIDE_PORT}}}"
stats_url="${GUIDE_BASE_URL}/api/v1/data/spdd-projection/stats"

if ! curl -sf --max-time 2 "${stats_url}" >/dev/null 2>&1; then
  echo "CONTEXT_BACKEND=files"
  echo "REASON=guide-dice enabled but Guide is not reachable at ${stats_url}"
  exit 0
fi

echo "CONTEXT_BACKEND=guide-dice"
echo "GUIDE_BASE_URL=${GUIDE_BASE_URL}"
echo "MCP_TOOLS=spdd_workSubgraph spdd_areaLessons spdd_findByLabel spdd_projectionStats"

if [[ "${MODE}" == "project" ]]; then
  echo ""
  echo "Projecting SPDD entities from: ${TARGET}"
  curl -sf --max-time 30 -X POST "${GUIDE_BASE_URL}/api/v1/data/spdd-projection/load" \
    -H 'Content-Type: application/json' \
    -d "{\"rootPath\":\"${TARGET}\"}"
  echo ""
  if [[ -n "${WORK_ID}" ]]; then
    echo "WorkId subgraph: ${WORK_ID}"
    curl -sf --max-time 10 "${GUIDE_BASE_URL}/api/v1/data/spdd-projection/work/${WORK_ID}" || {
      echo "(work id ${WORK_ID} not found in projection)"
    }
    echo ""
  fi
fi
