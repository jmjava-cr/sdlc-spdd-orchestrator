#!/usr/bin/env bash
# Regression harness for FEAT-008 /sdlc-spdd-diff-comment adapters.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pass=0
fail=0

ok() { echo "  OK: $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL: $1" >&2; fail=$((fail + 1)); }

assert_file() {
  if [[ -f "$1" ]]; then ok "file ${1#${REPO_ROOT}/}"; else bad "missing file $1"; fi
}

assert_contains() {
  local path="$1"
  local pattern="$2"
  local label="$3"
  if grep -Fq "${pattern}" "${path}" 2>/dev/null; then
    ok "${label}"
  else
    bad "${label} (missing in ${path#${REPO_ROOT}/}: ${pattern})"
  fi
}

CURSOR="${REPO_ROOT}/templates/cursor/sdlc-spdd-diff-comment.md"
COPILOT="${REPO_ROOT}/templates/copilot/prompts/sdlc-spdd-diff-comment.prompt.md"
CLAUDE="${REPO_ROOT}/templates/claude/commands/sdlc-spdd-diff-comment.md"
SPEC="${REPO_ROOT}/spec/commands/lifecycle-diff-comment.spec.md"

echo "== Test 1: spec and adapters exist =="
assert_file "${SPEC}"
assert_file "${CURSOR}"
assert_file "${COPILOT}"
assert_file "${CLAUDE}"

echo "== Test 2: generate-only + diff vs base contract =="
for path in "${CURSOR}" "${COPILOT}" "${CLAUDE}"; do
  assert_contains "${path}" "Do not post" "no-post guardrail (${path##*/})"
  assert_contains "${path}" "Do not implement code" "no-code guardrail (${path##*/})"
  assert_contains "${path}" "merge-base" "merge-base step (${path##*/})"
  assert_contains "${path}" "Work ID" "Work ID metadata (${path##*/})"
  assert_contains "${path}" "On success:" "success feedback (${path##*/})"
  assert_contains "${path}" "On failure:" "failure feedback (${path##*/})"
  assert_contains "${path}" "gh pr comment" "forbids gh pr comment (${path##*/})"
done

echo "== Test 3: generator --check and adapter validation =="
if "${REPO_ROOT}/scripts/generate-command-adapters.sh" --check >/dev/null; then
  ok "generate-command-adapters --check"
else
  bad "generate-command-adapters --check"
fi
if "${REPO_ROOT}/scripts/validate-command-adapters.sh" >/dev/null; then
  ok "validate-command-adapters"
else
  bad "validate-command-adapters"
fi

echo
echo "Summary: ${pass} passed, ${fail} failed"
if [[ "${fail}" -gt 0 ]]; then
  echo "diff-comment command regression tests FAILED." >&2
  exit 1
fi
echo "All diff-comment command regression tests passed."
