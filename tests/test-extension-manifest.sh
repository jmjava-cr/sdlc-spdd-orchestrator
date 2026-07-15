#!/usr/bin/env bash
# FEAT-003 — manifest-driven extension resolution parity with convention fallback.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESOLVE="${REPO_ROOT}/scripts/resolve-agent-context.sh"
WORK="$(mktemp -d)"
trap 'rm -rf "${WORK}"' EXIT

pass=0
fail=0
ok() { echo "  OK: $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL: $1" >&2; fail=$((fail + 1)); }

setup_base() {
  mkdir -p "${WORK}/agent-context/extensions/_all-agents" \
    "${WORK}/agent-context/extensions/coding-agent" \
    "${WORK}/agent-context/extensions/skills" \
    "${WORK}/agent-context/playbooks" \
    "${WORK}/agent-context/memory" \
    "${WORK}/agent-context/harness"
  echo "# Team norms" > "${WORK}/agent-context/extensions/_all-agents/team-norms.md"
  echo "# Coding style" > "${WORK}/agent-context/extensions/coding-agent/style.md"
  cp "${REPO_ROOT}/agent-context/playbooks/bugfix-playbook.md" "${WORK}/agent-context/playbooks/"
  cp "${REPO_ROOT}/agent-context/memory/phase-index.md" "${WORK}/agent-context/memory/"
}

echo "== Test 1: convention fallback when manifest missing =="
setup_base
conv="$("${RESOLVE}" --target "${WORK}" --phase code --format paths)"
if grep -Fq "team-norms.md" <<< "${conv}" && grep -Fq "coding-agent/style.md" <<< "${conv}"; then
  ok "convention resolves phase extensions"
else
  bad "convention fallback failed"
fi

echo "== Test 2: manifest drives same folders as convention =="
cp "${REPO_ROOT}/templates/agent-context/extensions/manifest.md" \
  "${WORK}/agent-context/extensions/manifest.md"
mani="$("${RESOLVE}" --target "${WORK}" --phase code --format paths)"
if grep -Fq "team-norms.md" <<< "${mani}" && grep -Fq "coding-agent/style.md" <<< "${mani}"; then
  ok "manifest resolves same extensions as convention"
else
  bad "manifest resolution missing expected files"
fi

echo "== Test 3: example manifest extension resolves =="
cp "${REPO_ROOT}/templates/agent-context/extensions/_all-agents/example-manifest-extension.md" \
  "${WORK}/agent-context/extensions/_all-agents/example-manifest-extension.md"
out="$("${RESOLVE}" --target "${WORK}" --phase code --format paths)"
if grep -Fq "example-manifest-extension.md" <<< "${out}"; then
  ok "example manifest extension file resolves"
else
  bad "example manifest extension missing"
fi

echo "== Test 4: malformed manifest falls back to convention =="
echo "# Not a manifest" > "${WORK}/agent-context/extensions/manifest.md"
fallback="$("${RESOLVE}" --target "${WORK}" --phase code --format paths)"
if grep -Fq "team-norms.md" <<< "${fallback}" && grep -Fq "coding-agent/style.md" <<< "${fallback}"; then
  ok "malformed manifest falls back to convention"
else
  bad "malformed manifest did not fall back"
fi

echo
echo "Summary: ${pass} passed, ${fail} failed"
if (( fail > 0 )); then exit 1; fi
echo "All extension manifest tests passed."
