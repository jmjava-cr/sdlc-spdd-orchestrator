#!/usr/bin/env bash
# Local-only: seed a Cursor consumer, then run REAL Cursor agents for each
# slash-command definition via @cursor/sdk (not CI).
#
# Prerequisites:
#   export CURSOR_API_KEY=...   # https://cursor.com/dashboard/integrations
#
# Usage:
#   ./tests/live-consumer/run-cursor-agent-matrix.sh
#   ./tests/live-consumer/run-cursor-agent-matrix.sh --only init,plan,claim
#   LIVE_CURSOR_MODEL=composer-2.5 ./tests/live-consumer/run-cursor-agent-matrix.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"

# Resolve CURSOR_API_KEY like BROAD_REPO_TOKEN: env → local file → gitignored .env
load_cursor_api_key() {
  if [[ -n "${CURSOR_API_KEY:-}" ]]; then
    return 0
  fi
  local key_file="${CURSOR_API_KEY_FILE:-$HOME/.config/courseforge/cursor-api-key}"
  if [[ -f "${key_file}" ]]; then
    CURSOR_API_KEY="$(tr -d '[:space:]' <"${key_file}")"
    export CURSOR_API_KEY
    return 0
  fi
  local env_file="${REPO_ROOT}/.env"
  if [[ -f "${env_file}" ]] && grep -qE '^CURSOR_API_KEY=' "${env_file}"; then
    # shellcheck disable=SC1090
    set -a
    # Only pull the one key; avoid sourcing unrelated secrets into the process broadly.
    CURSOR_API_KEY="$(grep -E '^CURSOR_API_KEY=' "${env_file}" | head -n1 | cut -d= -f2- | tr -d '"' | tr -d "'")"
    set +a
    export CURSOR_API_KEY
    return 0
  fi
  return 1
}

if ! load_cursor_api_key || [[ -z "${CURSOR_API_KEY:-}" ]]; then
  echo "CURSOR_API_KEY is required for real Cursor agent runs." >&2
  echo >&2
  echo "Create a key at https://cursor.com/dashboard/integrations" >&2
  echo "then pick one:" >&2
  echo "  export CURSOR_API_KEY=cursor_..." >&2
  echo "  # or next to BROAD_REPO_TOKEN style local file:" >&2
  echo "  mkdir -p ~/.config/courseforge && chmod 700 ~/.config/courseforge" >&2
  echo "  printf '%s' 'cursor_...' > ~/.config/courseforge/cursor-api-key && chmod 600 ~/.config/courseforge/cursor-api-key" >&2
  echo "  # or add to gitignored orchestrator .env:" >&2
  echo "  echo 'CURSOR_API_KEY=cursor_...' >> ${REPO_ROOT}/.env" >&2
  echo >&2
  echo "Optional (Cloud Agents only): also add CURSOR_API_KEY in" >&2
  echo "Cursor Dashboard → Cloud Agents → Secrets (beside BROAD_REPO_TOKEN)." >&2
  echo "That injects it into cloud VMs; this local matrix still needs one of the above." >&2
  exit 1
fi

export LIVE_CONSUMER_KEEP=1
export LIVE_CONSUMER_ROOT="${LIVE_CONSUMER_ROOT:-/tmp/sdlc-spdd-live}"

echo "Seeding consumer at ${LIVE_CONSUMER_ROOT} (shell install only; no fake slash effects)..."
ROOT="$("${SCRIPT_DIR}/seed-and-install.sh")"
echo "  consumer: ${ROOT}"

# Run only install + adapter presence checks (not effect simulation).
bash "${SCRIPT_DIR}/scenarios/01-install.sh" "${ROOT}"
bash "${SCRIPT_DIR}/scenarios/05-cursor-commands.sh" "${ROOT}"

AGENT_DIR="${SCRIPT_DIR}/cursor-agent"
if [[ ! -d "${AGENT_DIR}/node_modules/@cursor/sdk" ]]; then
  echo "Installing @cursor/sdk into ${AGENT_DIR} ..."
  (cd "${AGENT_DIR}" && npm install --no-fund --no-audit)
fi

echo
echo "Starting real Cursor SDK local agent matrix..."
echo "NOTE: This executes each .cursor/commands/*.md via the Cursor agent runtime."
echo "It does not click the IDE slash picker UI; it is the faithful headless equivalent."
echo

export LIVE_CONSUMER_ROOT="${ROOT}"
export LIVE_WORK_ID="${WORK_ID}"
node "${AGENT_DIR}/run-slash-matrix.mjs" "$@"
