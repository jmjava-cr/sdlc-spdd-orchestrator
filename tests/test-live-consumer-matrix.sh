#!/usr/bin/env bash
# CI / local entrypoint for the idempotent live consumer matrix.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "${REPO_ROOT}/tests/live-consumer/run-matrix.sh" "$@"
