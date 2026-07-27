#!/usr/bin/env bash
# Regression tests for scripts/lib shared helpers (FEAT-001).
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

assert_contains() {
  local haystack="$1" needle="$2" label="$3"
  if grep -Fq "${needle}" <<< "${haystack}"; then ok "${label}"; else bad "${label} (missing '${needle}')"; fi
}

assert_exit() {
  local want_code="$1" label="$2"
  shift 2
  local rc=0
  "$@" >/dev/null 2>&1 || rc=$?
  if [[ "${rc}" -eq "${want_code}" ]]; then ok "${label}"; else bad "${label} (exit ${rc}, want ${want_code})"; fi
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
# shellcheck source=/dev/null
source "${LIB}/paths.sh"
# shellcheck source=/dev/null
source "${LIB}/framework-install.sh"
# shellcheck source=/dev/null
source "${LIB}/shipped-docs-boundary.sh"

tmp="$(mktemp -d)"
trap 'rm -rf "${tmp}"' EXIT

echo "== common.sh =="
assert_eq "$(sdlc_oneline $'hello\nworld' 20)" "hello world" "oneline collapses newlines"
assert_eq "$(sdlc_oneline 'a|b|c' 20)" "a/b/c" "oneline collapses pipes"
assert_eq "$(sdlc_oneline '  spaced  text  ' 20)" "spaced text" "oneline trims edges"
long="$(printf 'x%.0s' {1..50})"
assert_eq "$(sdlc_oneline "${long}" 10)" "xxxxxxxxxx..." "oneline truncates with ellipsis"

iso="$(sdlc_timestamp_iso)"
if [[ "${iso}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]]; then
  ok "timestamp_iso matches ISO-8601 UTC"
else
  bad "timestamp_iso format (${iso})"
fi
file_ts="$(sdlc_timestamp_file)"
if [[ "${file_ts}" =~ ^[0-9]{8}T[0-9]{6}Z$ ]]; then
  ok "timestamp_file is filename-safe"
else
  bad "timestamp_file format (${file_ts})"
fi
day="$(sdlc_timestamp_day)"
if [[ "${day}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  ok "timestamp_day is calendar day"
else
  bad "timestamp_day format (${day})"
fi

resolved="$(sdlc_resolve_target "${tmp}")"
assert_eq "${resolved}" "$(cd "${tmp}" && pwd)" "sdlc_resolve_target returns absolute path"

sdlc_ensure_dir "${tmp}/nested/dir" 0
if [[ -d "${tmp}/nested/dir" ]]; then ok "ensure_dir creates path"; else bad "ensure_dir did not create"; fi
dry_out="$(sdlc_ensure_dir "${tmp}/dry-only" 1)"
assert_contains "${dry_out}" "[dry-run] would mkdir" "ensure_dir dry-run message"
if [[ ! -d "${tmp}/dry-only" ]]; then ok "ensure_dir dry-run does not create"; else bad "ensure_dir dry-run mutated"; fi

sdlc_ensure_file "${tmp}/docs/note.md" "Note Title" 0
assert_eq "$(head -1 "${tmp}/docs/note.md")" "# Note Title" "ensure_file writes title"
sdlc_ensure_file "${tmp}/docs/note.md" "Other" 0
assert_eq "$(head -1 "${tmp}/docs/note.md")" "# Note Title" "ensure_file does not overwrite"
dry_file="$(sdlc_ensure_file "${tmp}/docs/dry.md" "Dry" 1)"
assert_contains "${dry_file}" "[dry-run] would create" "ensure_file dry-run message"
if [[ ! -f "${tmp}/docs/dry.md" ]]; then ok "ensure_file dry-run does not create"; else bad "ensure_file dry-run mutated"; fi

die_out="$(sdlc_die "boom-message" 7 2>&1)" && die_rc=0 || die_rc=$?
assert_eq "${die_rc}" "7" "sdlc_die exits with custom code"
assert_contains "${die_out}" "boom-message" "sdlc_die prints message"

fake_usage() { echo "USAGE_HIT"; }
unk_out="$(sdlc_unknown_option --nope fake_usage 2>&1)" && unk_rc=0 || unk_rc=$?
assert_eq "${unk_rc}" "1" "unknown_option exits 1"
assert_contains "${unk_out}" "Unknown option: --nope" "unknown_option names option"
assert_contains "${unk_out}" "USAGE_HIT" "unknown_option calls usage fn"

echo "== areas.sh =="
assert_eq "$(normalize_area '  Src/Billing/  ')" "src/billing" "normalize_area trims and lowercases"
assert_eq "$(normalize_area 'a///b///c/')" "a/b/c" "normalize_area collapses slashes"
assert_eq "$(normalize_token ' Billing. ')" "billing" "normalize_token strips punctuation"
assert_eq "$(normalize_token '(FooBar')" "foobar" "normalize_token strips leading wrapper"
assert_eq "$(normalize_token 'FooBar)')" "foobar" "normalize_token strips trailing paren"

cat > "${tmp}/sample.md" <<'MD'
## Code Areas

- com.acme.billing
- `src/foo`
- ignored trailing (note)

## Other

- not-this
MD
mapfile -t bullets < <(parse_section_bullets "${tmp}/sample.md" "Code Areas")
if [[ "${#bullets[@]}" -eq 3 && "${bullets[0]}" == "com.acme.billing" && "${bullets[1]}" == "src/foo" && "${bullets[2]}" == "ignored trailing" ]]; then
  ok "parse_section_bullets extracts and cleans list items"
else
  bad "parse_section_bullets (got ${#bullets[@]} items: ${bullets[*]-})"
fi
mapfile -t none < <(parse_section_bullets "${tmp}/missing.md" "Code Areas")
assert_eq "${#none[@]}" "0" "parse_section_bullets tolerates missing file"

echo "== work-id.sh =="
assert_eq "$(slugify 'FEAT Foo/Bar' strict)" "feat-foo-bar" "slugify strict"
assert_eq "$(slugify 'FEAT Foo Bar' legacy)" "feat-foo-bar" "slugify legacy"
assert_eq "$(slugify 'Hello_World!!' strict)" "hello-world" "slugify strict strips junk"
assert_eq "$(slugify 'Hello_World!!' legacy)" "hello-world" "slugify legacy strips junk"
assert_exit 2 "slugify rejects unknown mode" bash -c 'source "'"${LIB}"'/work-id.sh"; slugify x weird'

assert_eq "$(work_type_prefix feature)" "FEAT" "work_type_prefix feature"
assert_eq "$(work_type_prefix feat)" "FEAT" "work_type_prefix feat alias"
assert_eq "$(work_type_prefix bugfix)" "BUG" "work_type_prefix bugfix"
assert_eq "$(work_type_prefix bug)" "BUG" "work_type_prefix bug"
assert_eq "$(work_type_prefix refactor)" "REF" "work_type_prefix refactor"
assert_eq "$(work_type_prefix spike)" "SPIKE" "work_type_prefix spike"
assert_eq "$(work_type_prefix chore)" "CHORE" "work_type_prefix chore"
assert_eq "$(work_type_prefix doc)" "DOC" "work_type_prefix doc"
assert_eq "$(work_type_prefix test)" "TEST" "work_type_prefix test"
assert_eq "$(work_type_prefix unknown)" "FEAT" "work_type_prefix unknown defaults FEAT"

WORK="$(mktemp -d)"
mkdir -p "${WORK}/agent-context/features" "${WORK}/spdd/canvas"
touch "${WORK}/agent-context/features/FEAT-003-alpha" "${WORK}/spdd/canvas/FEAT-005-beta.md"
n="$(next_work_number FEAT "${WORK}" \
  "${WORK}/agent-context/features/FEAT-"* \
  "${WORK}/spdd/canvas/FEAT-"*.md)"
assert_eq "${n}" "6" "next_work_number scans features and canvas"
empty_n="$(next_work_number BUG "${WORK}" "${WORK}/agent-context/features/BUG-"*)"
assert_eq "${empty_n}" "1" "next_work_number starts at 1 when empty"

echo "== milestone.sh =="
echo 'FEAT-099-demo' > "${WORK}/milestone-1.md"
echo 'other' > "${WORK}/milestone-2.md"
abs="$(resolve_milestone "${WORK}" FEAT-099-demo "" absolute)"
rel="$(resolve_milestone "${WORK}" FEAT-099-demo "" relative)"
assert_eq "${abs}" "${WORK}/milestone-1.md" "resolve_milestone absolute"
assert_eq "${rel}" "milestone-1.md" "resolve_milestone relative"
cand_abs="$(resolve_milestone "${WORK}" "" "milestone-2.md" absolute)"
assert_eq "${cand_abs}" "${WORK}/milestone-2.md" "resolve_milestone candidate absolute"
cand_rel="$(resolve_milestone "${WORK}" "" "milestone-2" relative)"
assert_eq "${cand_rel}" "milestone-2.md" "resolve_milestone candidate adds .md"
assert_exit 1 "resolve_milestone missing work id fails" resolve_milestone "${WORK}" FEAT-nope "" absolute
assert_exit 1 "resolve_milestone empty work id fails" resolve_milestone "${WORK}" "" "" absolute

echo "== context-index.sh =="
idx="${WORK}/agent-context/memory/context-index.md"
prepend_context_index_rows "${idx}" "| src/foo | session | FEAT-1 | code | 2026-01-01T00:00:00Z | brief | entry |"
if grep -Fq 'Kinds: analysis, session' "${idx}" && grep -Fq 'src/foo' "${idx}"; then
  ok "prepend_context_index_rows writes header and row"
else
  bad "prepend_context_index_rows output"
fi
prepend_context_index_rows "${idx}" "| src/bar | analysis | FEAT-2 | analysis | 2026-01-02T00:00:00Z | analysis.md | entry |"
first_data="$(awk '/^\| / && $0 !~ /^\| Area/ { print; exit }' "${idx}")"
assert_contains "${first_data}" "src/bar" "prepend keeps newest row first"
row_count="$(awk '/^\| / && $0 !~ /^\| Area/ && $0 !~ /^\|[- ]+\|/' "${idx}" | wc -l | tr -d ' ')"
assert_eq "${row_count}" "2" "prepend preserves prior data rows"

echo "== paths.sh / framework-install / shipped-docs =="
if ((${#SDLC_SHIPPED_LIB_FILES[@]} >= 6)); then
  ok "SDLC_SHIPPED_LIB_FILES lists shipped libs (${#SDLC_SHIPPED_LIB_FILES[@]})"
else
  bad "SDLC_SHIPPED_LIB_FILES too short"
fi
for lib in "${SDLC_SHIPPED_LIB_FILES[@]}"; do
  if [[ -f "${LIB}/${lib}" ]]; then ok "shipped lib exists: ${lib}"; else bad "missing shipped lib: ${lib}"; fi
done
for lib in "${SDLC_ORCHESTRATOR_ONLY_LIB_FILES[@]}"; do
  if [[ -f "${LIB}/${lib}" ]]; then ok "orchestrator-only lib exists: ${lib}"; else bad "missing orchestrator-only lib: ${lib}"; fi
done

fake_caller="${tmp}/caller-scripts"
mkdir -p "${fake_caller}/lib"
cp "${LIB}/common.sh" "${fake_caller}/lib/"
cat > "${fake_caller}/consumer.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail
source "${LIB}/paths.sh"
run_require() {
  sdlc_require_lib common
  sdlc_oneline "from-lib" 20
}
run_require
EOF
out="$(bash "${fake_caller}/consumer.sh")"
assert_eq "${out}" "from-lib" "sdlc_require_lib sources sibling lib"

missing_caller="${tmp}/missing-lib-scripts"
mkdir -p "${missing_caller}"
cat > "${missing_caller}/consumer.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail
source "${LIB}/paths.sh"
sdlc_require_lib common
EOF
if bash "${missing_caller}/consumer.sh" >/dev/null 2>"${tmp}/missing.err"; then
  bad "sdlc_require_lib should fail when lib missing"
else
  assert_contains "$(cat "${tmp}/missing.err")" "missing shared library" "sdlc_require_lib errors clearly"
fi

framework_ensure_dir "${tmp}/fw-dir" 0
if [[ -d "${tmp}/fw-dir" ]]; then ok "framework_ensure_dir creates"; else bad "framework_ensure_dir failed"; fi
fw_dry="$(framework_ensure_dir "${tmp}/fw-dry" 1)"
assert_contains "${fw_dry}" "[dry-run]" "framework_ensure_dir dry-run"

if is_orchestrator_only_doc "docs/integration-branch.md"; then
  ok "integration-branch.md is orchestrator-only"
else
  bad "integration-branch.md should be orchestrator-only"
fi
if is_orchestrator_only_doc "docs/catch-up.md"; then
  ok "catch-up.md is orchestrator-only"
else
  bad "catch-up.md should be orchestrator-only"
fi
if ! is_orchestrator_only_doc "docs/workflow.md"; then
  ok "workflow.md is shippable"
else
  bad "workflow.md should ship"
fi
if declare -F collect_shipped_doc_paths >/dev/null; then
  ok "collect_shipped_doc_paths is defined"
else
  bad "collect_shipped_doc_paths missing"
fi

echo "== verify-script-lib-duplicates.sh =="
if "${REPO_ROOT}/scripts/verify-script-lib-duplicates.sh" >/dev/null; then
  ok "no stray lib helper duplicates in scripts/"
else
  bad "verify-script-lib-duplicates reported issues"
fi

echo
echo "Summary: ${pass} passed, ${fail} failed"
if (( fail > 0 )); then exit 1; fi
echo "All scripts/lib regression tests passed."
