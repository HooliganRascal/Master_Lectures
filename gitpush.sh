#!/bin/bash
set -euo pipefail

if [ -z "${1:-}" ]; then
  echo "Error: Please provide a commit message."
  echo "Usage: ./gitpush.sh \"Your commit message\""
  exit 1
fi

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

git rm --cached --ignore-unmatch -- ':(glob,icase)**/*.pdf'
git add --all
if ! git diff --cached --quiet; then
  git commit -m "$1"
fi
git push

echo "Push complete!"
