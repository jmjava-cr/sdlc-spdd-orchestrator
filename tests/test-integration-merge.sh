#!/usr/bin/env bash
# End-to-end merge gate: install + workflow CLI + lib/manifest/spec checks.
# Automates the critical path from docs/integration-branch.md sections A–G.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SETUP="${REPO_ROOT}/scripts/setup-agent-prompts.sh"
UPGRADE="${REPO_ROOT}/scripts/upgrade-project.sh"
VALIDATE="${REPO_ROOT}/scripts/validate-command-adapters.sh"
GEN="${REPO_ROOT}/scripts/generate-command-adapters.sh"
DUPES="${REPO_ROOT}/scripts/verify-script-lib-duplicates.sh"
RESOLVE="${REPO_ROOT}/scripts/resolve-agent-context.sh"
POSTURE="${REPO_ROOT}/scripts/check-posture-boundary.sh"

WORK="$(mktemp -d)"
trap 'rm -rf "${WORK}"' EXIT
TARGET="${WORK}/target"
mkdir -p "${TARGET}"

pass=0
fail=0
ok()  { echo "  ok   $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL $1" >&2; fail=$((fail + 1)); }

echo "== A. Orchestrator gates =="
if "${VALIDATE}" >/dev/null; then ok "validate-command-adapters"; else bad "validate-command-adapters"; fi
if "${GEN}" --check >/dev/null; then ok "generate-command-adapters --check"; else bad "generate-command-adapters --check"; fi
if "${DUPES}" >/dev/null; then ok "verify-script-lib-duplicates"; else bad "verify-script-lib-duplicates"; fi
if "${POSTURE}" >/dev/null; then ok "check-posture-boundary"; else bad "check-posture-boundary"; fi

echo "== B. Install --all into throwaway target =="
if "${SETUP}" --target "${TARGET}" --all >/dev/null; then
  ok "setup-agent-prompts --all"
else
  bad "setup-agent-prompts --all"
fi

for cmd in claim shelf advance next team; do
  if [[ -f "${TARGET}/.cursor/commands/sdlc-${cmd}.md" \
     && -f "${TARGET}/.github/prompts/sdlc-${cmd}.prompt.md" \
     && -f "${TARGET}/.claude/commands/sdlc-${cmd}.md" ]]; then
    ok "workflow command installed: ${cmd}"
  else
    bad "missing workflow command: ${cmd}"
  fi
done

if [[ -f "${TARGET}/scripts/sdlc-spdd/lib/common.sh" \
   && -f "${TARGET}/scripts/sdlc-spdd/lib/work-id.sh" \
   && -f "${TARGET}/agent-context/extensions/manifest.md" ]]; then
  ok "shared lib + extension manifest installed"
else
  bad "lib/manifest install incomplete"
fi

if "${VALIDATE}" --target "${TARGET}" >/dev/null; then
  ok "target adapter validation"
else
  bad "target adapter validation"
fi

echo "== C. Workflow CLI claim/next/team/shelf/archive =="
mkdir -p "${TARGET}/spdd/canvas"
printf '%s\n' '# DEMO-001-integration-smoke' '' '## Final Status' '' '- Status: In Progress' \
  > "${TARGET}/spdd/canvas/DEMO-001-integration-smoke.md"
SDLC="${TARGET}/scripts/sdlc-spdd/sdlc.sh"
list_out="$(SDLC_USER="merge-bot" SDLC_ROOT="${TARGET}" "${SDLC}" list-work)"
if grep -Fq 'DEMO-001-integration-smoke' <<< "${list_out}"; then
  ok "list-work discovers demo"
else
  bad "list-work missing demo"
fi
if SDLC_USER="merge-bot" SDLC_ROOT="${TARGET}" "${SDLC}" claim DEMO-001-integration-smoke >/dev/null; then
  ok "claim succeeds"
else
  bad "claim failed"
fi
next_out="$(SDLC_USER="merge-bot" SDLC_ROOT="${TARGET}" "${SDLC}" next)"
if grep -Fq 'Do now' <<< "${next_out}"; then
  ok "next is actionable"
else
  bad "next output weak"
fi
team_out="$(SDLC_USER="merge-bot" SDLC_ROOT="${TARGET}" "${SDLC}" team)"
if grep -Fq 'DEMO-001-integration-smoke' <<< "${team_out}"; then
  ok "team shows claim"
else
  bad "team missing claim"
fi
if SDLC_USER="merge-bot" SDLC_ROOT="${TARGET}" "${SDLC}" shelf --reason "integration test" >/dev/null; then
  ok "shelf succeeds"
else
  bad "shelf failed"
fi

# Complete + archive path
printf '%s\n' '# DEMO-002-done' '' '## Final Status' '' '- Status: Complete' \
  > "${TARGET}/spdd/canvas/DEMO-002-done.md"
mkdir -p "${TARGET}/agent-context/features/DEMO-002-done"
printf '# feat\n' > "${TARGET}/agent-context/features/DEMO-002-done/requirement.md"
if SDLC_ROOT="${TARGET}" "${SDLC}" archive DEMO-002-done >/dev/null \
  && [[ -f "${TARGET}/spdd/canvas/archive/DEMO-002-done.md" ]]; then
  ok "archive completed demo work"
else
  bad "archive completed demo work"
fi

echo "== D. Upgrade path refreshes managed files =="
rm -f "${TARGET}/.cursor/commands/sdlc-claim.md"
if "${UPGRADE}" --target "${TARGET}" --all >/dev/null \
  && [[ -f "${TARGET}/.cursor/commands/sdlc-claim.md" ]]; then
  ok "upgrade restores missing workflow command"
else
  bad "upgrade did not restore workflow command"
fi

echo "== E. Extension resolve on target =="
paths="$("${RESOLVE}" --target "${TARGET}" --phase code --format paths)"
if grep -Fq "example-manifest-extension.md" <<< "${paths}"; then
  ok "resolve finds example manifest extension"
else
  bad "resolve missing example manifest extension"
fi

echo "== F. Nested harnesses =="
for t in \
  test-scripts-lib.sh \
  test-extension-manifest.sh \
  test-archive-work.sh \
  test-sdlc-pointer.sh; do
  if "${REPO_ROOT}/tests/${t}" >/dev/null; then
    ok "nested ${t}"
  else
    bad "nested ${t}"
  fi
done

echo
echo "Results: ${pass} passed, ${fail} failed"
if [[ "${fail}" -gt 0 ]]; then
  exit 1
fi
echo "All integration-merge tests passed."
