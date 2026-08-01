#!/usr/bin/env bash
# Launch the SDLC-SPDD ops console (install/upgrade, SQLite, rollback, Guide).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
exec "${ROOT}/scripts/sdlc.sh" console "$@"