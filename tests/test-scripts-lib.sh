#!/usr/bin/env bash
# Smoke tests for scripts/lib shared helpers (FEAT-001 T02).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LIB="${REPO_ROOT}/scripts/lib"

pass=0
fail=0

ok()  { echo "  ok   $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL $1" >&2; fail=$((fail + 1)); }

assert_eq() {
  local got="$1" want="$2" label="$3"
  if [[ "${got}" == "${want}" ]]; then ok "${label}"; else bad "${label} (got '${got}', want '${want}')"; fi
}

# shellcheck source=/dev/null
source "${LIB}/common.sh"
# shellcheck source=/dev/null
source "${LIB}/areas.sh"
# shellcheck source=/dev/null
source "${LIB}/work-id.sh"
# shellcheck source=/dev/null
source "${LIB}/milestone.sh"
# shellcheck source=/dev/null
source "${LIB}/context-index.sh"

echo "== common.sh =="
assert_eq "$(sdlc_oneline $'hello\nworld' 20)" "hello world" "oneline collapses newlines"
assert_eq "$(slugify 'FEAT Foo/Bar' strict)" "feat-foo-bar" "slugify strict"
assert_eq "$(slugify 'FEAT Foo Bar' legacy)" "feat-foo-bar" "slugify legacy"
assert_eq "$(work_type_prefix bugfix)" "BUG" "work_type_prefix bugfix"

echo "== areas.sh =="
assert_eq "$(normalize_area '  Src/Billing/  ')" "src/billing" "normalize_area trims and lowercases"
assert_eq "$(normalize_token ' Billing. ')" "billing" "normalize_token strips punctuation"

tmp="$(mktemp -d)"
trap 'rm -rf "${tmp}"' EXIT
cat > "${tmp}/sample.md" <<'MD'
## Code Areas

- com.acme.billing
- `src/foo`
MD
mapfile -t bullets < <(parse_section_bullets "${tmp}/sample.md" "Code Areas")
if [[ "${#bullets[@]}" -eq 2 && "${bullets[0]}" == "com.acme.billing" ]]; then
  ok "parse_section_bullets extracts list items"
else
  bad "parse_section_bullets (got ${#bullets[@]} items)"
fi

echo "== work-id.sh =="
WORK="$(mktemp -d)"
mkdir -p "${WORK}/agent-context/features" "${WORK}/spdd/canvas"
touch "${WORK}/agent-context/features/FEAT-003-alpha" "${WORK}/spdd/canvas/FEAT-005-beta.md"
n="$(next_work_number FEAT "${WORK}" \
  "${WORK}/agent-context/features/FEAT-"* \
  "${WORK}/spdd/canvas/FEAT-"*.md)"
assert_eq "${n}" "6" "next_work_number scans features and canvas"

echo "== milestone.sh =="
mkdir -p "${WORK}"
echo 'FEAT-099-demo' > "${WORK}/milestone-1.md"
abs="$(resolve_milestone "${WORK}" FEAT-099-demo "" absolute)"
rel="$(resolve_milestone "${WORK}" FEAT-099-demo "" relative)"
assert_eq "${abs}" "${WORK}/milestone-1.md" "resolve_milestone absolute"
assert_eq "${rel}" "milestone-1.md" "resolve_milestone relative"

echo "== context-index.sh =="
idx="${WORK}/agent-context/memory/context-index.md"
prepend_context_index_rows "${idx}" "| src/foo | session | FEAT-1 | code | 2026-01-01T00:00:00Z | brief | entry |"
if grep -Fq 'Kinds: analysis, session' "${idx}" && grep -Fq 'src/foo' "${idx}"; then
  ok "prepend_context_index_rows writes header and row"
else
  bad "prepend_context_index_rows output"
fi

echo "== paths.sh manifest =="
# shellcheck source=/dev/null
source "${LIB}/paths.sh"
if ((${#SDLC_SHIPPED_LIB_FILES[@]} >= 6)); then
  ok "SDLC_SHIPPED_LIB_FILES lists shipped libs"
else
  bad "SDLC_SHIPPED_LIB_FILES too short"
fi

echo
echo "Summary: ${pass} passed, ${fail} failed"
if (( fail > 0 )); then exit 1; fi
echo "All scripts/lib smoke tests passed."
