#!/usr/bin/env bash
# Orchestrator-only helpers for init-project.sh and upgrade-project.sh.
# Not shipped to target projects.

framework_ensure_dir() {
  local dir="$1"
  local dry_run="$2"
  if [[ "${dry_run}" -eq 1 ]]; then
    echo "[dry-run] would mkdir -p ${dir}"
  else
    mkdir -p "${dir}"
  fi
}
