#!/usr/bin/env bash
# Append-ingest examples/retrieval-fixture into Guide for SPIKE-001 mode B spot-checks.
# Queries: tests/fixtures/spike-001-mcp-queries.tsv
set -euo pipefail

GUIDE_ROOT="${GUIDE_ROOT:-${HOME}/github/jmjava/guide}"
GUIDE_PORT="${GUIDE_PORT:-21337}"
GUIDE_PROFILE="${GUIDE_PROFILE:-menke-fixture}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FIXTURE="${REPO_ROOT}/examples/retrieval-fixture"

if [[ ! -d "${GUIDE_ROOT}" ]]; then
  echo "Guide checkout not found at ${GUIDE_ROOT}" >&2
  exit 1
fi

profile="${GUIDE_ROOT}/scripts/user-config/application-${GUIDE_PROFILE}.yml"
if [[ ! -f "${profile}" ]]; then
  echo "Copy templates/guide-profiles/application-menke-fixture.yml.example to ${profile}" >&2
  exit 1
fi

if [[ ! -d "${FIXTURE}" ]]; then
  echo "Fixture not found: ${FIXTURE}" >&2
  exit 1
fi

echo "Fixture:     ${FIXTURE}"
echo "Guide:       ${GUIDE_ROOT} (profile ${GUIDE_PROFILE})"
echo "MCP queries: tests/fixtures/spike-001-mcp-queries.tsv"
echo ""
echo "After ingest, run MCP spot-checks and record URIs in:"
echo "  spdd/analysis/SPIKE-001-guide-ingest-agent-context-exploration.md"
echo ""

cd "${GUIDE_ROOT}"
export GUIDE_PROFILE GUIDE_PORT SERVER_PORT="${GUIDE_PORT}"
exec ./scripts/append-ingest.sh
