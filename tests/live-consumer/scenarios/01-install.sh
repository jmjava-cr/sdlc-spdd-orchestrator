#!/usr/bin/env bash
# Assert install layout for a Cursor-only consumer.
set -euo pipefail
# shellcheck source=../lib.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/lib.sh"

ROOT="${1:?target root required}"
echo "== 01 install layout =="

[[ -x "${ROOT}/scripts/sdlc-spdd/sdlc.sh" ]] && ok "sdlc.sh installed" || bad "sdlc.sh missing"
[[ -x "${ROOT}/agent-context/sdlc-pointer.sh" ]] && ok "pointer script" || bad "pointer script"
[[ -x "${ROOT}/agent-context/sdlc-workflow.sh" ]] && ok "workflow script" || bad "workflow script"
[[ -f "${ROOT}/agent-context/work-registry.tsv" ]] && ok "work-registry.tsv" || bad "work-registry.tsv"
[[ -f "${ROOT}/.cursor/rules/sdlc-spdd.mdc" ]] && ok "cursor rule" || bad "cursor rule"
[[ -d "${ROOT}/.cursor/commands" ]] && ok "cursor commands dir" || bad "cursor commands dir"

# Cursor-only: Copilot/Claude adapters must not appear.
if [[ -d "${ROOT}/.github/prompts" ]]; then
  bad "unexpected Copilot prompts on --cursor install"
else
  ok "no Copilot prompts (cursor-only)"
fi
if [[ -d "${ROOT}/.claude/commands" ]]; then
  bad "unexpected Claude commands on --cursor install"
else
  ok "no Claude commands (cursor-only)"
fi

# Seed work visible.
if live_sdlc "${ROOT}" list-work | grep -Fq "${WORK_ID}"; then
  ok "list-work sees ${WORK_ID}"
else
  bad "list-work missing ${WORK_ID}"
fi
