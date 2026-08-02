#!/usr/bin/env bash
# Deploy docs/ + locally generated recordings to GitHub Pages (gh-pages branch).
# MP4s stay gitignored on main; this script copies them from your working tree only.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: deploy-docs-pages-local.sh [--dry-run]

Build a Pages tree from docs/ plus local docs/demos/recordings/*.mp4 (gitignored on
main) and force-push to the gh-pages branch.

Requires: git, rsync, push access to origin.

One-time repo setup: Settings → Pages → Deploy from branch → gh-pages / root.

Options:
  --dry-run   Show actions without pushing
  --help      Print this help message
EOF
}

DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

STAGING="$(mktemp -d)"
cleanup() { rm -rf "${STAGING}"; }
trap cleanup EXIT

rsync -a \
  --exclude 'demos/audio/' \
  --exclude 'demos/animations/media/' \
  --exclude 'demos/animations/timing.json' \
  --exclude 'demos/animations/__pycache__/' \
  "${ROOT}/docs/" "${STAGING}/"

RECORDINGS="${ROOT}/docs/demos/recordings"
mkdir -p "${STAGING}/demos/recordings"
shopt -s nullglob
mp4s=("${RECORDINGS}"/*.mp4)
shopt -u nullglob
if ((${#mp4s[@]} == 0)); then
  echo "warning: no local MP4s in docs/demos/recordings/ — Pages videos will be missing" >&2
else
  cp "${mp4s[@]}" "${STAGING}/demos/recordings/"
  echo "Including ${#mp4s[@]} recording(s) from local tree (not committed on main)."
fi

# docs/demos/.gitignore ignores recordings/*.mp4 so they stay off main. For the
# Pages staging tree we must NOT ignore them — otherwise `git add -A` drops the
# copies above and the site serves zero-length / 404 players.
if [[ -f "${STAGING}/demos/.gitignore" ]]; then
  # Keep other regenerable ignores; stop ignoring published recordings.
  grep -v -E '^[[:space:]]*recordings/\*\.mp4[[:space:]]*$|^[[:space:]]*recordings/[[:space:]]*$' \
    "${STAGING}/demos/.gitignore" > "${STAGING}/demos/.gitignore.pages" || true
  mv "${STAGING}/demos/.gitignore.pages" "${STAGING}/demos/.gitignore"
fi

# Skip Jekyll so static HTML/MP4 are served as-is on GitHub Pages.
: > "${STAGING}/.nojekyll"

REMOTE="$(git -C "${ROOT}" remote get-url origin)"
staged_mp4="$(find "${STAGING}/demos/recordings" -name '*.mp4' -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "Staging site at ${STAGING} ($(find "${STAGING}" -type f | wc -l) files; ${staged_mp4} mp4)"

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo "[dry-run] would push ${STAGING} → origin gh-pages (${REMOTE})"
  exit 0
fi

pushd "${STAGING}" >/dev/null
git init -q
git checkout -q -b gh-pages
git add -A
# Belt-and-suspenders: force-add MP4s even if a nested ignore reappears.
shopt -s nullglob
staged=("${STAGING}/demos/recordings"/*.mp4)
shopt -u nullglob
if ((${#staged[@]} > 0)); then
  git add -f "${staged[@]}"
fi
committed_mp4="$(git ls-files 'demos/recordings/*.mp4' | wc -l | tr -d ' ')"
if (( committed_mp4 == 0 )) && ((${#mp4s[@]} > 0)); then
  echo "error: local MP4s exist but none were staged for gh-pages (check demos/.gitignore)" >&2
  exit 1
fi
git commit -q -m "Deploy docs and local demo recordings ($(date -u +%Y-%m-%dT%H:%MZ))"
echo "Committed ${committed_mp4} recording(s) on gh-pages tip."
git push -f "${REMOTE}" HEAD:gh-pages
popd >/dev/null

echo "OK: pushed gh-pages. Enable branch deploy in repo Pages settings if not already."