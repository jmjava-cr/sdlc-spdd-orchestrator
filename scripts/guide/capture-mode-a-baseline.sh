#!/usr/bin/env bash
# Capture mode (a) resolver baseline for SPIKE-001 fixture gold cases.
# Writes tests/fixtures/spike-001-mode-a-baseline.tsv (committed on spike branch).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RESOLVE="${REPO_ROOT}/scripts/resolve-agent-context.sh"
FIXTURE="${REPO_ROOT}/examples/retrieval-fixture"
GOLD="${REPO_ROOT}/tests/fixtures/spike-001-retrieval-gold.tsv"
OUT="${REPO_ROOT}/tests/fixtures/spike-001-mode-a-baseline.tsv"

normalize_field() {
  local v="$1"
  [[ "${v}" == "-" ]] && v=""
  printf '%s' "${v}"
}

measure_paths() {
  local target="$1"
  shift
  local -a paths=("$@")
  local count=0 bytes=0 p abs
  for p in "${paths[@]}"; do
    [[ -z "${p}" ]] && continue
    abs="${target}/${p}"
    [[ -f "${abs}" ]] || continue
    count=$((count + 1))
    bytes=$((bytes + $(wc -c < "${abs}")))
  done
  printf '%s\t%s' "${count}" "${bytes}"
}

tmp="$(mktemp)"
trap 'rm -f "${tmp}"' EXIT

{
  printf '%s\n' "# SPIKE-001 mode (a) resolver baseline — generated; do not hand-edit"
  printf '%s\n' "# Columns: case_id	description	work_id	phase	areas	path_count	context_bytes	paths"
} > "${OUT}"

case_id=0
while IFS=$'\t' read -r work_id phase areas must_include must_exclude description; do
  [[ "${work_id}" == "work_id" ]] && continue
  [[ "${work_id}" =~ ^# ]] && continue
  [[ -z "${description}" ]] && continue

  case_id=$((case_id + 1))
  wid="$(normalize_field "${work_id}")"
  ph="$(normalize_field "${phase}")"
  ar="$(normalize_field "${areas}")"

  local_args=(--target "${FIXTURE}" --format paths)
  [[ -n "${ph}" ]] && local_args+=(--phase "${ph}")
  [[ -n "${wid}" ]] && local_args+=(--work-id "${wid}")
  [[ -n "${ar}" ]] && local_args+=(--areas "${ar}")

  mapfile -t paths < <("${RESOLVE}" "${local_args[@]}")
  metrics="$(measure_paths "${FIXTURE}" "${paths[@]}")"
  path_count="${metrics%%$'\t'*}"
  context_bytes="${metrics#*$'\t'}"

  paths_joined=""
  p=""
  for p in "${paths[@]}"; do
    [[ -z "${p}" ]] && continue
    if [[ -z "${paths_joined}" ]]; then paths_joined="${p}"; else paths_joined="${paths_joined}|${p}"; fi
  done

  printf 'C%02d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "${case_id}" "${description}" "${wid:--}" "${ph:--}" "${ar:--}" \
    "${path_count}" "${context_bytes}" "${paths_joined}"
done < <(grep -v '^#' "${GOLD}" | grep -v '^[[:space:]]*$') >> "${OUT}"

echo "Wrote mode (a) baseline: ${OUT} (${case_id} cases)"
