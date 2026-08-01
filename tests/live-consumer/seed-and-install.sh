#!/usr/bin/env bash
# Wipe → seed → git init → install Cursor adapters → verify.
# stdout: absolute consumer root only (last line). Diagnostics go to stderr.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"

ROOT="$(live_resolve_root)"
live_flush "${ROOT}"
mkdir -p "${ROOT}"
live_seed_app "${ROOT}"

echo "Installing Cursor adapters into ${ROOT} ..." >&2
live_install_cursor "${ROOT}" >/dev/null

echo "Verifying install ..." >&2
if ! "${REPO_ROOT}/scripts/verify-project-install.sh" \
  --target "${ROOT}" --require-cursor >/dev/null; then
  echo "verify-project-install failed for ${ROOT}" >&2
  "${REPO_ROOT}/scripts/verify-project-install.sh" \
    --target "${ROOT}" --require-cursor >&2 || true
  exit 1
fi

printf '%s\n' "${ROOT}"
