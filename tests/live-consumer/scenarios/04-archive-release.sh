#!/usr/bin/env bash
# Complete-path archive + release.
set -euo pipefail
# shellcheck source=../lib.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/lib.sh"

ROOT="${1:?target root required}"
echo "== 04 archive + release =="

# Second work item already Complete for archive path.
mkdir -p "${ROOT}/spdd/canvas" "${ROOT}/agent-context/features/${DONE_WORK_ID}"
cat >"${ROOT}/spdd/canvas/${DONE_WORK_ID}.md" <<EOF
# REASONS Canvas: ${DONE_WORK_ID}

## Metadata

- Work ID: ${DONE_WORK_ID}
- Status: Complete
- Readiness: Ready For Coding

## Final Status

- Status: Complete
- Completed Date: 2026-07-31
EOF
printf '# requirement\n' >"${ROOT}/agent-context/features/${DONE_WORK_ID}/requirement.md"
printf '# progress\n' >"${ROOT}/agent-context/features/${DONE_WORK_ID}/progress-log.md"

if live_sdlc "${ROOT}" archive "${DONE_WORK_ID}" >/dev/null \
  && [[ -f "${ROOT}/spdd/canvas/archive/${DONE_WORK_ID}.md" ]]; then
  ok "archive ${DONE_WORK_ID}"
else
  bad "archive ${DONE_WORK_ID}"
fi

# Release active claim on primary work.
live_sdlc "${ROOT}" claim "${WORK_ID}" --force >/dev/null 2>&1 || true
if live_sdlc "${ROOT}" release --reason "live matrix done with claim" >/dev/null; then
  ok "release"
else
  bad "release"
fi

if live_sdlc "${ROOT}" sync-team >/dev/null 2>&1; then
  ok "sync-team"
else
  skipped "sync-team"
fi
