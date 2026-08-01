#!/usr/bin/env bash
# SPIKE-001 T07 — gold-test harness for mode (a) markdown resolver baseline.
# Compares resolve-agent-context.sh output against tests/fixtures/spike-001-retrieval-gold.tsv
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESOLVE="${REPO_ROOT}/scripts/resolve-agent-context.sh"
FIXTURE="${REPO_ROOT}/examples/retrieval-fixture"
GOLD="${REPO_ROOT}/tests/fixtures/spike-001-retrieval-gold.tsv"

pass=0
fail=0
ok() { echo "  OK: $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL: $1" >&2; fail=$((fail + 1)); }

[[ -d "${FIXTURE}" ]] || { echo "Fixture not found: ${FIXTURE}" >&2; exit 1; }
[[ -f "${GOLD}" ]] || { echo "Gold file not found: ${GOLD}" >&2; exit 1; }

normalize_field() {
  local v="$1"
  [[ "${v}" == "-" ]] && v=""
  printf '%s' "${v}"
}

run_case() {
  local work_id="$1"
  local phase="$2"
  local areas="$3"
  local must_include="$4"
  local must_exclude="$5"
  local description="$6"

  echo "== case: ${description} =="

  local -a args=(--target "${FIXTURE}" --format paths)
  [[ -n "${phase}" ]] && args+=(--phase "${phase}")
  [[ -n "${work_id}" ]] && args+=(--work-id "${work_id}")
  [[ -n "${areas}" ]] && args+=(--areas "${areas}")

  local out
  out="$("${RESOLVE}" "${args[@]}")"

  local path
  if [[ -n "${must_include}" ]]; then
    IFS='|' read -ra includes <<< "${must_include}"
    for path in "${includes[@]}"; do
      [[ -z "${path}" ]] && continue
      if grep -Fxq "${path}" <<< "${out}"; then
        ok "includes ${path}"
      else
        bad "missing required path: ${path}"
        echo "--- resolver output ---" >&2
        echo "${out}" >&2
        echo "----------------------" >&2
      fi
    done
  fi

  if [[ -n "${must_exclude}" ]]; then
    IFS='|' read -ra excludes <<< "${must_exclude}"
    for path in "${excludes[@]}"; do
      [[ -z "${path}" ]] && continue
      if grep -Fxq "${path}" <<< "${out}"; then
        bad "excluded path present: ${path}"
        echo "--- resolver output ---" >&2
        echo "${out}" >&2
        echo "----------------------" >&2
      else
        ok "excludes ${path}"
      fi
    done
  fi
}

while IFS=$'\t' read -r work_id phase areas must_include must_exclude description; do
  [[ "${work_id}" == "work_id" ]] && continue
  [[ "${work_id}" =~ ^# ]] && continue
  [[ -z "${description}" ]] && continue

  work_id="$(normalize_field "${work_id}")"
  phase="$(normalize_field "${phase}")"
  areas="$(normalize_field "${areas}")"

  run_case "${work_id}" "${phase}" "${areas}" "${must_include}" "${must_exclude}" "${description}"
done < <(grep -v '^#' "${GOLD}" | grep -v '^[[:space:]]*$')

echo
if (( fail > 0 )); then
  echo "${fail} failed, ${pass} passed" >&2
  exit 1
fi
echo "All ${pass} retrieval-fixture resolver gold assertions passed."
