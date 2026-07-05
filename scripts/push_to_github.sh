#!/usr/bin/env bash
# Push RS-Agent to GitHub. Run from repo root on a machine with GitHub access.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Error: not a git repository. Run from RS-Agent directory."
  exit 1
fi

# Set identity locally if not configured
if ! git config user.email >/dev/null; then
  git config user.email "xuwenjia@bupt.edu.cn"
  git config user.name "IntelliSensing"
fi

git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/IntelliSensing/RS-Agent.git

echo "Fetching remote main..."
git fetch origin main

echo "Merging remote history..."
git merge origin/main --allow-unrelated-histories -m "Merge upstream placeholder with RS-Agent framework release" || {
  echo "Merge conflict — resolve manually, then: git push origin main"
  exit 1
}

echo "Pushing to GitHub..."
git push origin main

echo "Done: https://github.com/IntelliSensing/RS-Agent"
