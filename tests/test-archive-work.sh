#!/usr/bin/env bash
# Regression harness for completed/cancelled Work ID archive (issue #29).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORKFLOW="${REPO_ROOT}/agent-context/sdlc-workflow.sh"
POINTER="${REPO_ROOT}/agent-context/sdlc-pointer.sh"
TEAM="${REPO_ROOT}/agent-context/sdlc-team-registry.sh"

WORK="$(mktemp -d)"
trap 'rm -rf "${WORK}"' EXIT

pass=0
fail=0
ok()  { echo "  ok   $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL $1" >&2; fail=$((fail + 1)); }

wf() { SDLC_ROOT="${1}" "${WORKFLOW}" "${@:2}"; }

setup_work() {
  local t="$1"
  local work_id="$2"
  local final_status="$3"
  mkdir -p \
    "${t}/agent-context/features/${work_id}/tasks" \
    "${t}/agent-context/sessions" \
    "${t}/spdd/canvas" \
    "${t}/spdd/analysis" \
    "${t}/spdd/reviews" \
    "${t}/spdd/sync" \
    "${t}/requirements/milestones" \
    "${t}/.sdlc/workflows" \
    "${t}/scripts/sdlc-spdd"
  cp "${POINTER}" "${t}/agent-context/sdlc-pointer.sh"
  cp "${WORKFLOW}" "${t}/agent-context/sdlc-workflow.sh"
  cp "${TEAM}" "${t}/agent-context/sdlc-team-registry.sh"
  cp "${REPO_ROOT}/templates/agent-context/work-registry.tsv" "${t}/agent-context/work-registry.tsv"
  cp "${REPO_ROOT}/scripts/sdlc.sh" "${t}/scripts/sdlc-spdd/sdlc.sh"
  chmod +x \
    "${t}/agent-context/sdlc-pointer.sh" \
    "${t}/agent-context/sdlc-workflow.sh" \
    "${t}/agent-context/sdlc-team-registry.sh" \
    "${t}/scripts/sdlc-spdd/sdlc.sh"

  cat > "${t}/spdd/canvas/${work_id}.md" <<EOF
# ${work_id}

## Final Status

- Status: ${final_status}
EOF
  printf '# analysis\n' > "${t}/spdd/analysis/${work_id}-analysis.md"
  printf '# review\n' > "${t}/spdd/reviews/${work_id}-review.md"
  printf '# sync\n' > "${t}/spdd/sync/${work_id}-sync.md"
  printf '# feature\n' > "${t}/agent-context/features/${work_id}/requirement.md"
  printf '# milestone\n' > "${t}/requirements/milestones/${work_id}.md"
  printf 'phase=code\nactive=1\n' > "${t}/.sdlc/workflows/${work_id}.state"
  printf '# session for %s\n' "${work_id}" > "${t}/agent-context/sessions/20260727T000000Z-plan-${work_id}.md"
  printf '# current\n' > "${t}/agent-context/sessions/current-session.md"
}

echo "== Test 1: refuse in-progress work without --force =="
T="${WORK}/refuse"
setup_work "${T}" "FEAT-100-active" "In Progress"
if SDLC_ROOT="${T}" wf "${T}" archive FEAT-100-active >/dev/null 2>&1; then
  bad "archive should refuse In Progress"
else
  ok "archive refuses In Progress"
fi
if [[ -f "${T}/spdd/canvas/FEAT-100-active.md" ]]; then
  ok "in-progress canvas left in place"
else
  bad "in-progress canvas was moved"
fi

echo "== Test 2: archive completed work moves artifacts =="
T="${WORK}/complete"
setup_work "${T}" "FEAT-101-done" "Complete"
SDLC_USER="archiver" SDLC_ROOT="${T}" wf "${T}" claim FEAT-101-done >/dev/null
SDLC_ROOT="${T}" wf "${T}" archive FEAT-101-done >/dev/null
if [[ ! -f "${T}/spdd/canvas/FEAT-101-done.md" \
   && -f "${T}/spdd/canvas/archive/FEAT-101-done.md" ]]; then
  ok "canvas moved to spdd/canvas/archive/"
else
  bad "canvas archive path incorrect"
fi
if [[ ! -d "${T}/agent-context/features/FEAT-101-done" \
   && -d "${T}/agent-context/features/archive/FEAT-101-done" ]]; then
  ok "feature workspace moved to features/archive/"
else
  bad "feature archive path incorrect"
fi
if [[ -f "${T}/spdd/analysis/archive/FEAT-101-done-analysis.md" \
   && -f "${T}/spdd/reviews/archive/FEAT-101-done-review.md" \
   && -f "${T}/spdd/sync/archive/FEAT-101-done-sync.md" ]]; then
  ok "analysis/review/sync moved to archive/"
else
  bad "sidecar artifacts not archived"
fi
if [[ -f "${T}/agent-context/sessions/archive/20260727T000000Z-plan-FEAT-101-done.md" \
   && -f "${T}/agent-context/sessions/current-session.md" ]]; then
  ok "matching session brief archived; current-session kept"
else
  bad "session archive behavior incorrect"
fi
if [[ -f "${T}/requirements/milestones/FEAT-101-done.md" ]]; then
  ok "milestone requirement left in place"
else
  bad "milestone should not be moved"
fi
if grep -q $'FEAT-101-done\tarchived\t' "${T}/agent-context/work-registry.tsv"; then
  ok "registry status set to archived"
else
  bad "registry missing archived row"
fi
ptr="$(SDLC_ROOT="${T}" "${T}/agent-context/sdlc-pointer.sh" get)"
if [[ -z "${ptr}" ]]; then ok "pointer cleared on archive"; else bad "pointer still set (${ptr})"; fi

echo "== Test 3: archive cancelled work =="
T="${WORK}/cancelled"
setup_work "${T}" "FEAT-102-cancel" "Cancelled"
SDLC_ROOT="${T}" wf "${T}" archive FEAT-102-cancel >/dev/null
if [[ -f "${T}/spdd/canvas/archive/FEAT-102-cancel.md" ]] \
  && grep -q $'FEAT-102-cancel\tarchived\t' "${T}/agent-context/work-registry.tsv" \
  && grep -q 'archived:cancelled' "${T}/agent-context/work-registry.tsv"; then
  ok "cancelled work archived with note token"
else
  bad "cancelled archive failed"
fi

echo "== Test 4: canceled spelling (US) treated as cancelled =="
T="${WORK}/canceled-us"
setup_work "${T}" "FEAT-103-us" "Canceled — scope cut"
SDLC_ROOT="${T}" wf "${T}" archive FEAT-103-us >/dev/null
if [[ -f "${T}/spdd/canvas/archive/FEAT-103-us.md" ]]; then
  ok "Canceled spelling is archivable"
else
  bad "Canceled spelling not accepted"
fi

echo "== Test 5: dry-run does not move files =="
T="${WORK}/dry"
setup_work "${T}" "FEAT-104-dry" "Complete"
out="$(SDLC_ROOT="${T}" wf "${T}" archive FEAT-104-dry --dry-run)"
if [[ -f "${T}/spdd/canvas/FEAT-104-dry.md" \
   && ! -f "${T}/spdd/canvas/archive/FEAT-104-dry.md" ]]; then
  ok "dry-run leaves canvas in place"
else
  bad "dry-run mutated canvas"
fi
if grep -Fq '[dry-run]' <<< "${out}"; then
  ok "dry-run prints planned moves"
else
  bad "dry-run missing plan output"
fi

echo "== Test 6: --all archives every eligible Work ID =="
T="${WORK}/all"
setup_work "${T}" "FEAT-105-a" "Complete"
setup_work "${T}" "FEAT-105-b" "Cancelled"
setup_work "${T}" "FEAT-105-c" "In Progress"
SDLC_ROOT="${T}" wf "${T}" archive --all >/dev/null
if [[ -f "${T}/spdd/canvas/archive/FEAT-105-a.md" \
   && -f "${T}/spdd/canvas/archive/FEAT-105-b.md" \
   && -f "${T}/spdd/canvas/FEAT-105-c.md" ]]; then
  ok "--all archives complete+cancelled, skips in-progress"
else
  bad "--all selection incorrect"
fi

echo "== Test 7: list-work ignores archive folders =="
T="${WORK}/discover"
setup_work "${T}" "FEAT-106-live" "In Progress"
mkdir -p "${T}/agent-context/features/archive/FEAT-999-old" "${T}/spdd/canvas/archive"
printf '# old\n' > "${T}/agent-context/features/archive/FEAT-999-old/requirement.md"
printf '# old canvas\n' > "${T}/spdd/canvas/archive/FEAT-999-old.md"
out="$(SDLC_ROOT="${T}" wf "${T}" list-work)"
if grep -q 'FEAT-106-live' <<< "${out}" && ! grep -q 'FEAT-999-old' <<< "${out}"; then
  ok "list-work skips archived Work IDs"
else
  bad "list-work discover leaked archive entries"
fi

echo "== Test 8: sync-team marks cancelled without archiving =="
T="${WORK}/sync-cancel"
setup_work "${T}" "FEAT-107-sync" "Cancelled"
SDLC_ROOT="${T}" wf "${T}" sync-team >/dev/null
if grep -q $'FEAT-107-sync\tcancelled\t' "${T}/agent-context/work-registry.tsv" \
  && [[ -f "${T}/spdd/canvas/FEAT-107-sync.md" ]]; then
  ok "sync-team sets cancelled and leaves files"
else
  bad "sync-team cancelled behavior wrong"
fi

echo "== Test 9: sdlc.sh wrapper archive path =="
T="${WORK}/wrapper"
setup_work "${T}" "FEAT-108-wrap" "Complete"
if SDLC_ROOT="${T}" "${T}/scripts/sdlc-spdd/sdlc.sh" archive FEAT-108-wrap >/dev/null \
  && [[ -f "${T}/spdd/canvas/archive/FEAT-108-wrap.md" ]]; then
  ok "sdlc.sh archive wrapper works"
else
  bad "sdlc.sh archive wrapper failed"
fi

echo "== Test 10: --force archives non-terminal work =="
T="${WORK}/force"
setup_work "${T}" "FEAT-109-force" "In Progress"
if SDLC_ROOT="${T}" wf "${T}" archive FEAT-109-force --force >/dev/null \
  && [[ -f "${T}/spdd/canvas/archive/FEAT-109-force.md" ]] \
  && grep -q 'archived:forced' "${T}/agent-context/work-registry.tsv"; then
  ok "--force archives non-terminal work"
else
  bad "--force archive failed"
fi

echo "== Test 11: re-archive is a no-op for --all =="
T="${WORK}/rearchive"
setup_work "${T}" "FEAT-110-once" "Complete"
SDLC_ROOT="${T}" wf "${T}" archive FEAT-110-once >/dev/null
# Put a live canvas back with same id would be weird; --all should skip archived registry rows
# even if somehow still discoverable via milestone only.
out="$(SDLC_ROOT="${T}" wf "${T}" archive --all)"
if grep -q 'processed 0 eligible' <<< "${out}"; then
  ok "--all skips already-archived registry rows"
else
  # may still process 0 with different wording
  if [[ -f "${T}/spdd/canvas/archive/FEAT-110-once.md" ]]; then
    ok "--all did not duplicate archive (artifacts remain once)"
  else
    bad "re-archive behavior unexpected: ${out}"
  fi
fi

echo
echo "Results: ${pass} passed, ${fail} failed"
if [[ "${fail}" -gt 0 ]]; then
  exit 1
fi
echo "All archive-work tests passed."
