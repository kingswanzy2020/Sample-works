#!/usr/bin/env bash
# Copy one project out of this roadmap into a standalone git repo.
#
# Usage: scripts/new-project-repo.sh <project-number> <destination-dir>
# Example: scripts/new-project-repo.sh 03 ../zero-downtime-deploys
#
# The new repo gets:
#   - everything in projects/<NN>-*/        (at the repo root)
#   - the shared directories listed in the project's SHARED file
#     (default: app/, the shared sample service; some projects also need landscape/)
#   - templates/                             (ADR, postmortem, break-it)
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 <project-number> <destination-dir>" >&2
  exit 1
fi

root="$(cd "$(dirname "$0")/.." && pwd)"
num="$(printf '%02d' "$((10#$1))")"
dest="$2"

shopt -s nullglob
matches=("$root"/projects/"$num"-*/)
if [[ ${#matches[@]} -ne 1 ]]; then
  echo "no unique project found for number $num under $root/projects" >&2
  exit 1
fi
src="${matches[0]%/}"

if [[ -e "$dest" && -n "$(ls -A "$dest" 2>/dev/null)" ]]; then
  echo "destination $dest exists and is not empty" >&2
  exit 1
fi

# Shared directories a project needs are listed in its SHARED file (default: app).
shared="app"
[[ -f "$src/SHARED" ]] && shared="$( (grep -v "^#" "$src/SHARED" || true) | xargs)"

mkdir -p "$dest"
cp -R "$src"/. "$dest"/
rm -f "$dest/SHARED"
for dir in $shared; do
  cp -R "$root/$dir" "$dest/$dir"
done
cp -R "$root/templates" "$dest/templates"

cd "$dest"
if [[ ! -d .git ]]; then
  git init -q
  git add -A
  git commit -q -m "Start $(basename "$src") from portfolio roadmap"
fi

echo "Created $(pwd) from $(basename "$src")"
echo "Next: read README.md, then fill in docs/adr/0001-*.md before writing code."
