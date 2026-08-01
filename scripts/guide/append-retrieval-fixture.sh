#!/usr/bin/env bash
# Append-ingest examples/retrieval-fixture into Guide for SPIKE-001 mode B spot-checks.
# Queries: tests/fixtures/spike-001-mcp-queries.tsv
#
# Forces GUIDE_PROFILE=menke-fixture (overrides guide/.env) and rewrites the
# fixture profile's ORCHESTRATOR_ROOT / directories to this repo's absolute path
# so we never depend on ~/ expansion or a stale copy.
set -euo pipefail

GUIDE_ROOT="${GUIDE_ROOT:-${HOME}/github/jmjava/guide}"
GUIDE_PORT="${GUIDE_PORT:-21337}"
# Explicit export so append-ingest.sh's .env load cannot replace it with menke/menke-5.
export GUIDE_PROFILE=menke-fixture

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FIXTURE="${REPO_ROOT}/examples/retrieval-fixture"
PROFILE="${GUIDE_ROOT}/scripts/user-config/application-menke-fixture.yml"
EXAMPLE="${REPO_ROOT}/templates/guide-profiles/application-menke-fixture.yml.example"

if [[ ! -d "${GUIDE_ROOT}" ]]; then
  echo "Guide checkout not found at ${GUIDE_ROOT}" >&2
  exit 1
fi

if [[ ! -d "${FIXTURE}" ]]; then
  echo "Fixture not found: ${FIXTURE}" >&2
  exit 1
fi

# Always regenerate the profile from the template so path + reload=false stay correct.
if [[ ! -f "${EXAMPLE}" ]]; then
  echo "Missing template: ${EXAMPLE}" >&2
  exit 1
fi
mkdir -p "$(dirname "${PROFILE}")"
sed "s|ORCHESTRATOR_ROOT|${REPO_ROOT}|g" "${EXAMPLE}" > "${PROFILE}"

# Drop prior git-ingest state so the fixture directory is treated as first-run
# (full ingest of that tree) instead of an empty diff.
rm -f "${GUIDE_ROOT}/scripts/user-config/ingestion-git-revisions-menke-fixture.json"

echo "Fixture:     ${FIXTURE}"
echo "Guide:       ${GUIDE_ROOT} (profile ${GUIDE_PROFILE})"
echo "Profile:     ${PROFILE}"
echo "MCP queries: tests/fixtures/spike-001-mcp-queries.tsv"
echo ""
echo "Profile gates (must show empty versions + fixture directory):"
grep -E 'versions:|supplementary:|/examples/retrieval-fixture|reload-content' "${PROFILE}" || true
echo ""
# Refuse to start if the profile still points at the default URL corpus.
if grep -qE 'versions:\s*\[[^]]*[0-9]' "${PROFILE}"; then
  echo "Refusing to start: profile still has non-empty content.versioned.versions" >&2
  exit 1
fi

cd "${GUIDE_ROOT}"
export GUIDE_PORT SERVER_PORT="${GUIDE_PORT}"
exec ./scripts/append-ingest.sh
