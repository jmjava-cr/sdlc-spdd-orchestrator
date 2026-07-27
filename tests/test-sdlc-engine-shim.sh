#!/usr/bin/env bash
# Smoke: scripts/sdlc.sh can delegate to the Python engine.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
pass=0
fail=0
ok()  { echo "  ok   $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL $1" >&2; fail=$((fail + 1)); }

echo "== Python engine importable =="
if PYTHONPATH="${REPO_ROOT}/engine/src" python3 -c 'import sdlc_engine; print(sdlc_engine.__version__)'; then
  ok "import sdlc_engine"
else
  bad "import sdlc_engine"
fi

echo "== SDLC_ENGINE=python via sdlc.sh =="
ver="$(SDLC_ENGINE=python "${REPO_ROOT}/scripts/sdlc.sh" version)"
if [[ "${ver}" == 2.0.0a* ]]; then
  ok "sdlc.sh version via python engine (${ver})"
else
  bad "unexpected version: ${ver}"
fi

out="$(SDLC_ENGINE=python "${REPO_ROOT}/scripts/sdlc.sh" next)"
if grep -Fq 'Do now' <<< "${out}" || grep -Fq 'No active Work ID' <<< "${out}"; then
  ok "sdlc.sh next via python engine"
else
  bad "python next output unexpected"
fi

echo "== default remains shell =="
out="$(SDLC_ENGINE=shell "${REPO_ROOT}/scripts/sdlc.sh" next)"
if grep -Fq 'No active Work ID' <<< "${out}" || grep -Fq 'SDLC:' <<< "${out}" || grep -Fq 'resume' <<< "${out}"; then
  ok "shell engine still works"
else
  bad "shell next unexpected"
fi

echo "== local sessions route even when SDLC_ENGINE=shell =="
tmp="$(mktemp -d)"
trap 'rm -rf "${tmp}"' EXIT
# Use --root via python engine; sdlc.sh local* always hits python.
out="$(
  SDLC_ENGINE=shell SDLC_USER=shim-test \
    PYTHONPATH="${REPO_ROOT}/engine/src" \
    python3 -m sdlc_engine --root "${tmp}" local start --name shim-local --intent "offline"
)"
if grep -Fq 'Started local session LOCAL-' <<< "${out}"; then
  ok "local start creates LOCAL session"
else
  bad "local start unexpected: ${out}"
fi
if [[ -f "${tmp}/.sdlc/local-sessions/"LOCAL-*/session.json ]]; then
  ok "local session artifacts under .sdlc/local-sessions"
else
  # glob may not expand in [[ -f ]]; check via find
  if find "${tmp}/.sdlc/local-sessions" -name session.json | grep -q .; then
    ok "local session artifacts under .sdlc/local-sessions"
  else
    bad "missing local session artifacts"
  fi
fi

echo
echo "Results: ${pass} passed, ${fail} failed"
if (( fail > 0 )); then exit 1; fi
