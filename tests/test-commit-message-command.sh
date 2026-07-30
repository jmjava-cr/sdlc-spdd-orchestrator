#!/usr/bin/env bash
# Regression harness for FEAT-008 /sdlc-spdd-commit-message adapters + engine routing.
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

assert_absent() {
  local path="$1"
  local pattern="$2"
  local label="$3"
  if grep -Fq "${pattern}" "${path}" 2>/dev/null; then
    bad "${label} (unexpected in ${path#${REPO_ROOT}/}: ${pattern})"
  else
    ok "${label}"
  fi
}

CURSOR="${REPO_ROOT}/templates/cursor/sdlc-spdd-commit-message.md"
COPILOT="${REPO_ROOT}/templates/copilot/prompts/sdlc-spdd-commit-message.prompt.md"
CLAUDE="${REPO_ROOT}/templates/claude/commands/sdlc-spdd-commit-message.md"
SPEC="${REPO_ROOT}/spec/commands/lifecycle-commit-message.spec.md"
ENGINE="${REPO_ROOT}/engine/src/sdlc_engine/commit_message.py"
SDLC_SH="${REPO_ROOT}/scripts/sdlc.sh"

echo "== Test 1: spec, adapters, and engine module exist =="
assert_file "${SPEC}"
assert_file "${CURSOR}"
assert_file "${COPILOT}"
assert_file "${CLAUDE}"
assert_file "${ENGINE}"

echo "== Test 2: generate-only commit message + engine delegation contract =="
for path in "${CURSOR}" "${COPILOT}" "${CLAUDE}"; do
  assert_contains "${path}" 'Do not run `git commit`' "no-commit guardrail (${path##*/})"
  assert_contains "${path}" "Do not implement code" "no-code guardrail (${path##*/})"
  assert_contains "${path}" "sdlc.sh commit-message" "engine delegation (${path##*/})"
  assert_contains "${path}" "Work ID" "Work ID metadata (${path##*/})"
  assert_contains "${path}" "On success:" "success feedback (${path##*/})"
  assert_contains "${path}" "On failure:" "failure feedback (${path##*/})"
  assert_contains "${path}" "Paste-ready commit message" "paste-ready output (${path##*/})"
  assert_absent "${path}" "PR review comment" "not a PR review command (${path##*/})"
done
assert_contains "${SDLC_SH}" 'commit-message)' "sdlc.sh routes commit-message to Python engine"

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

echo "== Test 4: engine commit-message CLI smoke =="
if PYTHONPATH="${REPO_ROOT}/engine/src${PYTHONPATH:+:${PYTHONPATH}}" \
  python3 -m sdlc_engine --root "${REPO_ROOT}" commit-message --hint "smoke" >/tmp/sdlc-cm-smoke.out 2>/tmp/sdlc-cm-smoke.err
then
  if grep -Eq 'source: (staged|unstaged|ahead-of-base)' /tmp/sdlc-cm-smoke.out; then
    ok "python -m sdlc_engine commit-message emits source"
  else
    bad "engine output missing source line"
  fi
else
  # Empty tree on a clean checkout of main is a valid failure mode.
  if grep -Fq "nothing to commit" /tmp/sdlc-cm-smoke.err; then
    ok "engine fails closed on empty change set"
  else
    bad "engine commit-message unexpected failure: $(cat /tmp/sdlc-cm-smoke.err)"
  fi
fi

echo
echo "Summary: ${pass} passed, ${fail} failed"
if [[ "${fail}" -gt 0 ]]; then
  echo "commit-message command regression tests FAILED." >&2
  exit 1
fi
echo "All commit-message command regression tests passed."
