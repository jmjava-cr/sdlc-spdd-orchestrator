#!/usr/bin/env bash
# Verify mode (a) baseline capture produces expected case count.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASELINE="${REPO_ROOT}/tests/fixtures/spike-001-mode-a-baseline.tsv"

"${REPO_ROOT}/scripts/guide/capture-mode-a-baseline.sh"

rows="$(awk -F'\t' 'NR>2 && $1 ~ /^C/ {c++} END {print c+0}' "${BASELINE}")"
if [[ "${rows}" -ne 3 ]]; then
  echo "Expected 3 baseline cases, got ${rows}" >&2
  exit 1
fi

echo "OK: mode (a) baseline has ${rows} cases"
