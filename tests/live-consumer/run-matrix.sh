#!/usr/bin/env bash
# Seed/flush a fake consumer repo and run every live scenario.
#
# Usage:
#   ./tests/live-consumer/run-matrix.sh
#   LIVE_CONSUMER_KEEP=1 ./tests/live-consumer/run-matrix.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"

echo "SDLC-SPDD live consumer matrix"
echo "  orchestrator: ${REPO_ROOT}"
echo "  work-id: ${WORK_ID}"

ROOT="$("${SCRIPT_DIR}/seed-and-install.sh")"
echo "  consumer: ${ROOT}"
echo

if [[ "${LIVE_CONSUMER_KEEP}" != "1" && "${ROOT}" != /tmp/sdlc-spdd-live ]]; then
  trap 'rm -rf "${ROOT}"' EXIT
fi

chmod +x "${SCRIPT_DIR}/seed-and-install.sh" "${SCRIPT_DIR}"/scenarios/*.sh

for scenario in \
  01-install.sh \
  02-pointer-workflow.sh \
  03-session-scripts.sh \
  04-archive-release.sh \
  05-cursor-commands.sh \
  06-slash-effects-sim.sh \
  07-python-engine.sh \
  08-full-populate.sh \
  09-sqlite-session-context.sh; do
  out="$(mktemp)"
  set +e
  bash "${SCRIPT_DIR}/scenarios/${scenario}" "${ROOT}" >"${out}" 2>&1
  rc=$?
  set -e
  cat "${out}"
  # Aggregate counters from scenario output.
  c_ok="$(grep -c '^  ok   ' "${out}" || true)"
  c_bad="$(grep -c '^  FAIL ' "${out}" || true)"
  c_skip="$(grep -c '^  skip ' "${out}" || true)"
  pass=$((pass + c_ok))
  fail=$((fail + c_bad))
  skip=$((skip + c_skip))
  if [[ "${rc}" -ne 0 && "${c_bad}" -eq 0 ]]; then
    bad "scenario ${scenario} exited ${rc}"
  fi
  rm -f "${out}"
  echo
done

echo "Active consumer root: ${ROOT}"
if [[ "${LIVE_CONSUMER_KEEP}" == "1" || "${ROOT}" == /tmp/sdlc-spdd-live ]]; then
  echo "Kept for Cursor reopen. See tests/live-consumer/CURSOR-SLASH-LIVE.md"
fi

live_summary
