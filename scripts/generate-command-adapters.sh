#!/usr/bin/env bash
# FEAT-002 — generate Cursor/Copilot/Claude adapters from spec/commands/*.spec.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SPEC_DIR="${REPO_ROOT}/spec/commands"

usage() {
  cat <<'EOF'
Usage: generate-command-adapters.sh [--check]

Generate templates/cursor, templates/copilot/prompts, and templates/claude/commands
from canonical specs under spec/commands/.

  --check   Exit 1 if generated output would differ from checked-in templates.
EOF
}

CHECK_ONLY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) CHECK_ONLY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

WORK="$(mktemp -d)"
trap 'rm -rf "${WORK}"' EXIT

failures=0

spec_meta() {
  local spec="$1"
  local key="$2"
  awk -v key="${key}" '
    BEGIN { in_fm=0 }
    /^---$/ { in_fm = !in_fm; next }
    in_fm && $0 ~ "^" key ":" {
      sub("^" key ":[[:space:]]*", "")
      print
      exit
    }
  ' "${spec}"
}

read_block() {
  local spec="$1"
  local block_id="$2"
  awk -v id="${block_id}" '
    $0 == "---BLOCK:" id "---" { capture=1; next }
    capture && $0 == "---END---" { exit }
    capture { print }
  ' "${spec}" | sed -e :a -e '/^\s*$/N; s/\n$//' -e ta
}

block_or_shared() {
  local spec="$1"
  local adapter="$2"
  local section="$3"
  local body
  body="$(read_block "${spec}" "${adapter}:${section}")"
  if [[ -n "${body}" ]]; then
    printf '%s' "${body}"
    return 0
  fi
  read_block "${spec}" "shared:${section}"
}

adapter_paths() {
  local family="$1"
  local slug="$2"
  case "${family}" in
    lifecycle)
      CURSOR_OUT="${REPO_ROOT}/templates/cursor/sdlc-spdd-${slug}.md"
      COPILOT_OUT="${REPO_ROOT}/templates/copilot/prompts/sdlc-spdd-${slug}.prompt.md"
      CLAUDE_OUT="${REPO_ROOT}/templates/claude/commands/sdlc-spdd-${slug}.md"
      ;;
    workflow)
      CURSOR_OUT="${REPO_ROOT}/templates/cursor/sdlc-${slug}.md"
      COPILOT_OUT="${REPO_ROOT}/templates/copilot/prompts/sdlc-${slug}.prompt.md"
      CLAUDE_OUT="${REPO_ROOT}/templates/claude/commands/sdlc-${slug}.md"
      ;;
    *)
      echo "Unknown family: ${family}" >&2
      return 1
      ;;
  esac
}

write_cursor() {
  local spec="$1"
  local out="$2"
  local title preamble rb out_body
  title="$(read_block "${spec}" "cursor:title")"
  preamble="$(read_block "${spec}" "cursor:preamble")"
  rb="$(block_or_shared "${spec}" cursor "Required Behavior")"
  out_body="$(block_or_shared "${spec}" cursor "Output")"
  {
    printf '# %s\n\n' "${title}"
    [[ -n "${preamble}" ]] && printf '%s\n\n' "${preamble}"
    printf '## Required Behavior\n\n%s\n\n' "${rb}"
    printf '## Output\n\n%s\n' "${out_body}"
  } > "${out}"
}

write_copilot() {
  local spec="$1"
  local out="$2"
  local desc mode title preamble rb out_body
  desc="$(spec_meta "${spec}" copilot_description)"
  mode="$(spec_meta "${spec}" copilot_mode)"
  title="$(read_block "${spec}" "copilot:title")"
  preamble="$(read_block "${spec}" "copilot:preamble")"
  rb="$(block_or_shared "${spec}" copilot "Required Behavior")"
  out_body="$(block_or_shared "${spec}" copilot "Output")"
  {
    echo "---"
    echo "description: ${desc}"
    [[ -n "${mode}" ]] && echo "mode: ${mode}"
    echo "---"
    echo
    printf '# %s\n\n' "${title}"
    [[ -n "${preamble}" ]] && printf '%s\n\n' "${preamble}"
    printf '## Required Behavior\n\n%s\n\n' "${rb}"
    printf '## Output\n\n%s\n' "${out_body}"
  } > "${out}"
}

write_claude() {
  local spec="$1"
  local out="$2"
  local desc hint title preamble rb out_body
  desc="$(spec_meta "${spec}" claude_description)"
  hint="$(spec_meta "${spec}" claude_argument_hint)"
  title="$(read_block "${spec}" "claude:title")"
  preamble="$(read_block "${spec}" "claude:preamble")"
  rb="$(block_or_shared "${spec}" claude "Required Behavior")"
  out_body="$(block_or_shared "${spec}" claude "Output")"
  {
    echo "---"
    echo "description: ${desc}"
    [[ -n "${hint}" ]] && echo "argument-hint: ${hint}"
    echo "---"
    echo
    printf '# %s\n\n' "${title}"
    [[ -n "${preamble}" ]] && printf '%s\n\n' "${preamble}"
    printf '## Required Behavior\n\n%s\n\n' "${rb}"
    printf '## Output\n\n%s\n' "${out_body}"
  } > "${out}"
}

compare_or_install() {
  local generated="$1"
  local target="$2"
  if [[ ! -f "${target}" ]]; then
    echo "Missing target template: ${target#${REPO_ROOT}/}" >&2
    failures=$((failures + 1))
    return 0
  fi
  if ! diff -q "${generated}" "${target}" >/dev/null 2>&1; then
    if (( CHECK_ONLY )); then
      echo "Stale adapter: ${target#${REPO_ROOT}/}" >&2
      diff -u "${target}" "${generated}" | head -40 >&2 || true
      failures=$((failures + 1))
    else
      cp "${generated}" "${target}"
      echo "Updated ${target#${REPO_ROOT}/}"
    fi
  fi
}

shopt -s nullglob
specs=( "${SPEC_DIR}"/*.spec.md )
if ((${#specs[@]} == 0)); then
  echo "No specs found in ${SPEC_DIR}. Run ./scripts/extract-command-specs.sh first." >&2
  exit 1
fi

for spec in "${specs[@]}"; do
  family="$(spec_meta "${spec}" family)"
  slug="$(spec_meta "${spec}" slug)"
  adapter_paths "${family}" "${slug}"

  write_cursor "${spec}" "${WORK}/cursor.md"
  write_copilot "${spec}" "${WORK}/copilot.md"
  write_claude "${spec}" "${WORK}/claude.md"

  compare_or_install "${WORK}/cursor.md" "${CURSOR_OUT}"
  compare_or_install "${WORK}/copilot.md" "${COPILOT_OUT}"
  compare_or_install "${WORK}/claude.md" "${CLAUDE_OUT}"
done

if (( failures > 0 )); then
  echo "generate-command-adapters: ${failures} issue(s)." >&2
  exit 1
fi

if (( CHECK_ONLY )); then
  echo "generate-command-adapters --check: all adapters match specs."
else
  echo "generate-command-adapters: generation complete."
fi
