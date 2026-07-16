#!/usr/bin/env bash
# context-index.md header and write helpers.

# Canonical header for capture-style prepend writes (includes Kinds line).
context_index_header_capture() {
  cat <<'CTX'
# Context Index

Maps code areas to indexed project context. Filter by Area to find prior sessions,
analysis artifacts, architecture decisions, known pitfalls, and reusable patterns
for the code you are about to touch — across any Work ID or date. Newest first.
Kinds: analysis, session, decision, pitfall, pattern, metric.

| Area | Kind | Work ID | Phase | Timestamp | Source | Entry |
|------|------|---------|-------|-----------|--------|-------|
CTX
}

# Prepend new_rows to index_file (newest first), preserving existing data rows.
prepend_context_index_rows() {
  local index_file="$1"
  local new_rows="$2"
  local header
  header="$(context_index_header_capture)"
  local existing_rows=""
  mkdir -p "$(dirname "${index_file}")"
  if [[ -f "${index_file}" ]]; then
    existing_rows="$(awk '/^\| / && $0 !~ /^\| Area/' "${index_file}")"
  fi
  {
    printf '%s\n' "${header}"
    printf '%s\n' "${new_rows}"
    if [[ -n "${existing_rows}" ]]; then
      printf '%s\n' "${existing_rows}"
    fi
  } > "${index_file}"
}
