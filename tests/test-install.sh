#!/usr/bin/env bash
set -euo pipefail

# Test suite for scripts/install.sh
# Verifies the install script detects AI tool directories correctly and
# installs the keel-sync command to the right locations.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_SCRIPT="$REPO_ROOT/scripts/install.sh"
FIXTURE_DIR="$REPO_ROOT/tests/fixture"
COMMAND_SOURCE="$REPO_ROOT/commands/keel-sync.md"

TMPDIR=""
passed=0
failed=0

# Minimal PATH that excludes claude CLI so detection is based solely on
# directory markers.  Keep basic tools (cp, mkdir, git, etc.) available.
SAFE_PATH="/usr/bin:/bin:/usr/sbin:/sbin"

cleanup() {
  if [ -n "$TMPDIR" ] && [ -d "$TMPDIR" ]; then
    rm -rf "$TMPDIR"
  fi
}
trap cleanup EXIT

# ---------- helpers ----------

setup() {
  cleanup
  TMPDIR="$(mktemp -d)"
  cp -r "$FIXTURE_DIR"/* "$TMPDIR/"
  git -C "$TMPDIR" init -q
}

run_install() {
  # Run install.sh with a restricted PATH so `command -v claude` fails.
  env PATH="$SAFE_PATH" bash "$INSTALL_SCRIPT" "$TMPDIR"
}

assert_file_exists() {
  local relpath="$1"
  if [ ! -f "$TMPDIR/$relpath" ]; then
    echo "  FAIL: expected $relpath to exist"
    return 1
  fi
}

assert_file_missing() {
  local relpath="$1"
  if [ -f "$TMPDIR/$relpath" ]; then
    echo "  FAIL: expected $relpath to NOT exist"
    return 1
  fi
}

assert_content_matches() {
  local relpath="$1"
  if ! diff -q "$COMMAND_SOURCE" "$TMPDIR/$relpath" >/dev/null 2>&1; then
    echo "  FAIL: $relpath content does not match source"
    return 1
  fi
}

run_test() {
  local name="$1"
  shift
  echo "--- $name ---"
  if "$@"; then
    echo "  PASS"
    passed=$((passed + 1))
  else
    echo "  FAIL"
    failed=$((failed + 1))
  fi
  echo ""
}

# ---------- tests ----------

test_no_ai_dirs() {
  setup
  run_install

  assert_file_exists ".claude/commands/keel-sync.md" &&
  assert_file_exists ".cursor/commands/keel-sync.md" &&
  assert_file_exists ".github/prompts/keel-sync.md" &&
  assert_content_matches ".claude/commands/keel-sync.md" &&
  assert_content_matches ".cursor/commands/keel-sync.md" &&
  assert_content_matches ".github/prompts/keel-sync.md"
}

test_only_cursor() {
  setup
  mkdir -p "$TMPDIR/.cursor"
  run_install

  assert_file_exists  ".cursor/commands/keel-sync.md" &&
  assert_file_missing ".claude/commands/keel-sync.md" &&
  assert_file_missing ".github/prompts/keel-sync.md" &&
  assert_content_matches ".cursor/commands/keel-sync.md"
}

test_only_claude() {
  setup
  mkdir -p "$TMPDIR/.claude"
  run_install

  assert_file_exists  ".claude/commands/keel-sync.md" &&
  assert_file_missing ".cursor/commands/keel-sync.md" &&
  assert_file_missing ".github/prompts/keel-sync.md" &&
  assert_content_matches ".claude/commands/keel-sync.md"
}

test_only_github() {
  setup
  mkdir -p "$TMPDIR/.github"
  run_install

  assert_file_exists  ".github/prompts/keel-sync.md" &&
  assert_file_missing ".claude/commands/keel-sync.md" &&
  assert_file_missing ".cursor/commands/keel-sync.md" &&
  assert_content_matches ".github/prompts/keel-sync.md"
}

test_cursorrules_file() {
  setup
  touch "$TMPDIR/.cursorrules"
  run_install

  assert_file_exists  ".cursor/commands/keel-sync.md" &&
  assert_file_missing ".claude/commands/keel-sync.md" &&
  assert_file_missing ".github/prompts/keel-sync.md" &&
  assert_content_matches ".cursor/commands/keel-sync.md"
}

# ---------- run ----------

echo "=== install.sh test suite ==="
echo ""

run_test "No AI dirs (fallback to all)" test_no_ai_dirs
run_test "Only .cursor/ exists"         test_only_cursor
run_test "Only .claude/ exists"         test_only_claude
run_test "Only .github/ exists"         test_only_github
run_test ".cursorrules file exists"     test_cursorrules_file

echo "=== Results: $passed passed, $failed failed ==="

if [ "$failed" -gt 0 ]; then
  exit 1
fi
