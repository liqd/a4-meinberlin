#!/bin/bash

# Ensure the adhocracy4 commit locked for Python (uv.lock) and JavaScript
# (package-lock.json) is the same, so backend and frontend come from one a4 commit.
set -euo pipefail

UV_LOCK_FILE="${UV_LOCK_FILE:-uv.lock}"
PACKAGE_LOCK_FILE="${PACKAGE_LOCK_FILE:-package-lock.json}"

PACKAGE_NAME="adhocracy4"

fail() {
  echo "$*" >&2
  exit 1
}

[ -f "$UV_LOCK_FILE" ] || fail "Could not find $UV_LOCK_FILE."
[ -f "$PACKAGE_LOCK_FILE" ] || fail "Could not find $PACKAGE_LOCK_FILE."

# adhocracy4 commit locked for Python: <repo>.git?rev=<sha>#<sha> in uv.lock
UV_HASH=$(grep -oE 'liqd/adhocracy4\.git[^#"]*#[0-9a-f]{40}' "$UV_LOCK_FILE" | head -n1 | sed -E 's/.*#([0-9a-f]{40})$/\1/' || true)

if [[ -z "$UV_HASH" ]]; then
  fail "Could not find the $PACKAGE_NAME commit in $UV_LOCK_FILE."
fi

# adhocracy4 commit locked for JavaScript in package-lock.json:
# "resolved": "git+ssh://git@github.com/liqd/adhocracy4.git#<sha>"
NPM_HASH=$(grep -oE 'git\+ssh://git@github\.com/liqd/adhocracy4\.git#[0-9a-f]{40}' "$PACKAGE_LOCK_FILE" | head -n1 | sed -E 's/.*#([0-9a-f]{40})$/\1/' || true)

if [[ -z "$NPM_HASH" ]]; then
  fail "Could not find the $PACKAGE_NAME commit in $PACKAGE_LOCK_FILE."
fi

# Check if the hashes match
if [[ "$UV_HASH" != "$NPM_HASH" ]]; then
  echo "$PACKAGE_NAME commit mismatch:" >&2
  echo "  $UV_LOCK_FILE: $UV_HASH" >&2
  echo "  $PACKAGE_LOCK_FILE: $NPM_HASH" >&2
  echo "Run 'make bump-a4' to update both." >&2
  exit 1
fi

echo "OK: $PACKAGE_NAME $UV_HASH matches in $UV_LOCK_FILE and $PACKAGE_LOCK_FILE."
