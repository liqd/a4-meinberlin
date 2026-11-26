#!/bin/bash

# Negative + positive tests for scripts/a4-check.sh
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
A4_CHECK="$SCRIPT_DIR/a4-check.sh"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

SHA_A="98ed5cece944d9bbbfa37e232e72a172508a19c4"
SHA_B="c576719daff919ba3841b4456f47d47576d7cec4"

UV_LOCK="$WORK/uv.lock"
PACKAGE_LOCK="$WORK/package-lock.json"

failures=0

# --- helpers ---------------------------------------------------------------

write_uv_lock() {
  cat > "$UV_LOCK" <<EOF
version = 1
requires-python = ">=3.12,<3.13"

[[package]]
name = "adhocracy4"
version = "2611.4.dev4+g98ed5cece"
source = { git = "https://github.com/liqd/adhocracy4.git?rev=$1#$1" }
EOF
}

write_package_lock() {
  cat > "$PACKAGE_LOCK" <<EOF
{
  "name": "meinberlin",
  "lockfileVersion": 3,
  "packages": {
    "node_modules/adhocracy4": {
      "resolved": "git+ssh://git@github.com/liqd/adhocracy4.git#$1",
      "license": "AGPL-3.0-only"
    }
  }
}
EOF
}

run_check() {
  UV_LOCK_FILE="$UV_LOCK" PACKAGE_LOCK_FILE="$PACKAGE_LOCK" "$A4_CHECK"
}

# assert <description> <expected_result:ok|fail> <message-substring-or-empty>
assert() {
  local desc="$1" expected="$2" needle="$3"
  local output status
  output="$(run_check 2>&1)"
  status=$?
  if [ "$expected" = ok ]; then
    if [ $status -ne 0 ]; then
      echo "FAIL: $desc (expected success, got exit $status): $output"
      failures=$((failures + 1))
      return
    fi
  else
    if [ $status -eq 0 ]; then
      echo "FAIL: $desc (expected failure, got success): $output"
      failures=$((failures + 1))
      return
    fi
    if [ -n "$needle" ] && ! grep -qF "$needle" <<< "$output"; then
      echo "FAIL: $desc (missing message '$needle'): $output"
      failures=$((failures + 1))
      return
    fi
  fi
  echo "PASS: $desc"
}

# --- positive --------------------------------------------------------------

write_uv_lock "$SHA_A"
write_package_lock "$SHA_A"
assert "matching commits succeed" ok ""

# --- negative: mismatch ----------------------------------------------------

write_uv_lock "$SHA_A"
write_package_lock "$SHA_B"
assert "mismatched commits fail" fail "mismatch"

# --- negative: cannot parse uv.lock ---------------------------------------

printf 'version = 1\n' > "$UV_LOCK"
write_package_lock "$SHA_A"
assert "missing adhocracy4 in uv.lock fails" fail "Could not find the adhocracy4 commit in"

# --- negative: cannot parse package-lock.json ------------------------------

write_uv_lock "$SHA_A"
printf '{ "name": "meinberlin", "packages": {} }\n' > "$PACKAGE_LOCK"
assert "missing adhocracy4 in package-lock.json fails" fail "Could not find the adhocracy4 commit in"

# package-lock using a non-git resolved form (e.g. tarball) must not parse
write_uv_lock "$SHA_A"
cat > "$PACKAGE_LOCK" <<EOF
{ "packages": { "node_modules/adhocracy4": { "resolved": "https://codeload.github.com/liqd/adhocracy4/tar.gz/$SHA_A" } } }
EOF
assert "non-git package-lock resolved form fails" fail "Could not find the adhocracy4 commit in"

# --- real repository -------------------------------------------------------

if UV_LOCK_FILE="$REPO_ROOT/uv.lock" PACKAGE_LOCK_FILE="$REPO_ROOT/package-lock.json" "$A4_CHECK" >/dev/null 2>&1; then
  echo "PASS: repository uv.lock and package-lock.json match"
else
  echo "FAIL: repository uv.lock and package-lock.json do not match"
  failures=$((failures + 1))
fi

echo
if [ $failures -gt 0 ]; then
  echo "$failures test(s) failed"
  exit 1
fi
echo "All a4-check.sh tests passed"
