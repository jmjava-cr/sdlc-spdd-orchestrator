#!/usr/bin/env bash
# SPIKE-001 T05 — run retrieval A/B drill on examples/retrieval-fixture.
#
# Mode (a): auto-captures resolver paths + byte counts.
# Mode (b): checks MCP results file against tests/fixtures/spike-001-mcp-queries.tsv.
#
# Usage:
#   ./scripts/guide/run-retrieval-ab-fixture.sh --capture-a
#   ./scripts/guide/run-retrieval-ab-fixture.sh --check-mcp /path/to/mcp-results.tsv
#   ./scripts/guide/run-retrieval-ab-fixture.sh --capture-a --check-mcp mcp-results.tsv
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CAPTURE="${REPO_ROOT}/scripts/guide/capture-mode-a-baseline.sh"
BASELINE="${REPO_ROOT}/tests/fixtures/spike-001-mode-a-baseline.tsv"
MCP_QUERIES="${REPO_ROOT}/tests/fixtures/spike-001-mcp-queries.tsv"
LEDGER="${REPO_ROOT}/spdd/analysis/SPIKE-001-retrieval-ab-ledger.md"

CAPTURE_A=0
MCP_RESULTS=""
CHECK_SETUP=0

usage() {
  cat <<EOF
Usage: run-retrieval-ab-fixture.sh [options]

Options:
  --capture-a           Regenerate mode (a) baseline TSV and print summary
  --check-mcp <file>    Validate MCP result URIs against spike-001-mcp-queries.tsv
  --verify-setup        Run fixture gold test + prereq hints (no Guide required)
  -h, --help            Show this help

Record outcomes in: ${LEDGER}
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --capture-a) CAPTURE_A=1; shift ;;
    --check-mcp) MCP_RESULTS="${2:-}"; shift 2 ;;
    --verify-setup) CHECK_SETUP=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if (( CHECK_SETUP )); then
  echo "== Verify fixture gold test =="
  "${REPO_ROOT}/tests/test-retrieval-fixture-resolver.sh"
  echo ""
  echo "== T01 prereq hints =="
  echo "  Guide:  \${GUIDE_ROOT:-~/github/jmjava/guide} on branch ingest-to-hub"
  echo "  Profiles: application-menke-5.yml + application-menke-fixture.yml in scripts/user-config/"
  echo "  MCP:    http://localhost:\${GUIDE_PORT:-21337}/sse"
  if curl -sf -o /dev/null --max-time 2 "http://localhost:${GUIDE_PORT:-21337}/actuator/health" 2>/dev/null; then
    echo "  Guide health: UP on port ${GUIDE_PORT:-21337}"
  else
    echo "  Guide health: not reachable (start guide before mode b)"
  fi
  exit 0
fi

if (( CAPTURE_A )); then
  echo "== Mode (a) — resolver baseline =="
  "${CAPTURE}"
  echo ""
  echo "Case summary:"
  awk -F'\t' 'NR>2 {printf "  %s: %s paths, %s bytes\n", $1, $6, $7}' "${BASELINE}"
  echo ""
  echo "Append metrics to: ${LEDGER}"
fi

if [[ -n "${MCP_RESULTS}" ]]; then
  [[ -f "${MCP_RESULTS}" ]] || { echo "MCP results file not found: ${MCP_RESULTS}" >&2; exit 1; }
  echo "== Mode (b) — MCP URI checks =="
  pass=0 fail=0
  while IFS=$'\t' read -r tool query must_match expect description; do
    [[ "${tool}" == "tool" ]] && continue
    [[ "${tool}" =~ ^# ]] && continue
    [[ -z "${tool}" ]] && continue
    expect="${expect:-match}"
    if [[ "${expect}" == "no_match" ]]; then
      if grep -Fq "${must_match}" "${MCP_RESULTS}"; then
        echo "  FAIL: ${description} — unexpected URI containing '${must_match}'" >&2
        fail=$((fail + 1))
      else
        echo "  OK: ${description} (no ${must_match} — expected)"
        pass=$((pass + 1))
      fi
    elif grep -Fq "${must_match}" "${MCP_RESULTS}"; then
      echo "  OK: ${description} (substring ${must_match})"
      pass=$((pass + 1))
    else
      echo "  FAIL: ${description} — no URI containing '${must_match}' in ${MCP_RESULTS}" >&2
      fail=$((fail + 1))
    fi
  done < <(grep -v '^#' "${MCP_QUERIES}")
  echo ""
  if (( fail > 0 )); then
    echo "${fail} MCP checks failed, ${pass} passed" >&2
    exit 1
  fi
  echo "All ${pass} MCP URI checks passed. Record mode (b) metrics in ${LEDGER}"
fi

if (( ! CAPTURE_A )) && [[ -z "${MCP_RESULTS}" ]]; then
  usage >&2
  exit 1
fi
