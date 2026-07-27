#!/usr/bin/env bash
# Milestone file resolution helpers.

# resolve_milestone TARGET WORK_ID [candidate] [mode]
#   mode absolute — return absolute path (capture-session-memory default)
#   mode relative — return path relative to TARGET (start-agent-session default)
resolve_milestone() {
  local target="$1"
  local work_id="$2"
  local candidate="${3:-}"
  local mode="${4:-absolute}"

  if [[ -n "${candidate}" ]]; then
    if [[ "${candidate}" != *.md ]]; then
      candidate="${candidate}.md"
    fi
    if [[ -f "${target}/${candidate}" ]]; then
      if [[ "${mode}" == "relative" ]]; then
        printf '%s' "${candidate}"
      else
        printf '%s' "${target}/${candidate}"
      fi
      return 0
    fi
    if [[ -f "${candidate}" ]]; then
      if [[ "${mode}" == "relative" ]]; then
        printf '%s' "${candidate#${target}/}"
      else
        printf '%s' "${candidate}"
      fi
      return 0
    fi
    return 1
  fi

  if [[ -z "${work_id}" ]]; then
    return 1
  fi

  shopt -s nullglob
  local file
  for file in "${target}"/milestone-*.md; do
    if grep -q "${work_id}" "${file}" 2>/dev/null; then
      shopt -u nullglob
      if [[ "${mode}" == "relative" ]]; then
        printf '%s' "${file#${target}/}"
      else
        printf '%s' "${file}"
      fi
      return 0
    fi
  done
  shopt -u nullglob
  return 1
}
