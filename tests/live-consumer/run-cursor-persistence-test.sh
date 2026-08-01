#!/usr/bin/env bash
# Local-only: Cursor SDK + SQLite + session/registry persistence test.
#
#   ./tests/live-consumer/run-cursor-persistence-test.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"

load_cursor_api_key() {
  if [[ -n "${CURSOR_API_KEY:-}" ]]; then return 0; fi
  local key_file="${CURSOR_API_KEY_FILE:-$HOME/.config/courseforge/cursor-api-key}"
  if [[ -f "${key_file}" ]]; then
    CURSOR_API_KEY="$(tr -d '[:space:]' <"${key_file}")"
    export CURSOR_API_KEY
    return 0
  fi
  local env_file="${REPO_ROOT}/.env"
  if [[ -f "${env_file}" ]] && grep -qE '^CURSOR_API_KEY=' "${env_file}"; then
    CURSOR_API_KEY="$(grep -E '^CURSOR_API_KEY=' "${env_file}" | head -n1 | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d '[:space:]')"
    export CURSOR_API_KEY
    return 0
  fi
  return 1
}

if ! load_cursor_api_key || [[ -z "${CURSOR_API_KEY:-}" ]]; then
  echo "CURSOR_API_KEY required (see tests/live-consumer/cursor-agent/README.md)" >&2
  exit 1
fi

export LIVE_CONSUMER_KEEP=1
export LIVE_CONSUMER_ROOT="${LIVE_CONSUMER_ROOT:-/tmp/sdlc-spdd-live}"
export ORCHESTRATOR_ROOT="${REPO_ROOT}"

echo "Seeding consumer for persistence test..."
ROOT="$("${SCRIPT_DIR}/seed-and-install.sh")"
echo "  consumer: ${ROOT}"

AGENT_DIR="${SCRIPT_DIR}/cursor-agent"
if [[ ! -d "${AGENT_DIR}/node_modules/@cursor/sdk" ]]; then
  (cd "${AGENT_DIR}" && npm install --no-fund --no-audit)
fi

if ! PYTHONPATH="${REPO_ROOT}/engine/src${PYTHONPATH:+:${PYTHONPATH}}" \
  python3 -c 'import sdlc_engine' 2>/dev/null; then
  echo "Installing orchestrator engine (editable) for db CLI..."
  python3 -m pip install -e "${REPO_ROOT}/engine" -q
fi

export LIVE_CONSUMER_ROOT="${ROOT}"
export LIVE_WORK_ID="${WORK_ID}"
chmod +x "${AGENT_DIR}/run-persistence-test.mjs"
node "${AGENT_DIR}/run-persistence-test.mjs" "$@"
