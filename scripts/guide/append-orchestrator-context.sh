#!/usr/bin/env bash
# Append-ingest orchestrator agent-context + spdd into Guide/Neo4j (SPIKE-001 T01, menke-5).
#
# Prerequisites:
#   - guide checkout on branch ingest-to-hub with application-menke-5.yml installed
#   - prior menke-* corpus layers already on the same Neo4j store (recommended)
#
# Override defaults:
#   GUIDE_ROOT=~/github/jmjava/guide
#   GUIDE_PORT=21337
#   GUIDE_PROFILE=menke-5
set -euo pipefail

GUIDE_ROOT="${GUIDE_ROOT:-${HOME}/github/jmjava/guide}"
GUIDE_PORT="${GUIDE_PORT:-21337}"
GUIDE_PROFILE="${GUIDE_PROFILE:-menke-5}"
GUIDE_INGEST_LOG="${GUIDE_INGEST_LOG:-/tmp/menke-5-ingest.log}"

if [[ ! -d "${GUIDE_ROOT}" ]]; then
  echo "Guide checkout not found at ${GUIDE_ROOT}" >&2
  echo "Set GUIDE_ROOT to your jmjava/guide path (ingest-to-hub branch)." >&2
  exit 1
fi

profile="${GUIDE_ROOT}/scripts/user-config/application-${GUIDE_PROFILE}.yml"
if [[ ! -f "${profile}" ]]; then
  echo "Profile not found: ${profile}" >&2
  echo "Copy templates/guide-profiles/application-menke-5-orchestrator-context.yml.example there." >&2
  exit 1
fi

branch="$(git -C "${GUIDE_ROOT}" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
if [[ "${branch}" != "ingest-to-hub" && "${branch}" != "main" ]]; then
  echo "Note: guide is on branch '${branch}'; ingest-to-hub recommended for git incremental ingest." >&2
fi

echo "Guide root:  ${GUIDE_ROOT}"
echo "Profile:     ${GUIDE_PROFILE}"
echo "Port:        ${GUIDE_PORT}"
echo "Ingest log:  ${GUIDE_INGEST_LOG}"
echo ""

cd "${GUIDE_ROOT}"
export GUIDE_PROFILE GUIDE_PORT SERVER_PORT="${GUIDE_PORT}"
exec ./scripts/append-ingest.sh 2>&1 | tee "${GUIDE_INGEST_LOG}"
