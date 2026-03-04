#!/usr/bin/env bash
set -euo pipefail

# Keel slash command installer
# Installs all commands from commands/ into AI tool directories in the current project.
#
# Usage:
#   From a Keel clone:  ./scripts/install.sh /path/to/target-project
#   Via curl:           curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/install.sh | bash -s /path/to/target-project
#   In current dir:     ./scripts/install.sh .

TARGET="${1:-.}"
TARGET="$(cd "$TARGET" && pwd)"

# Resolve the Keel repo root (relative to this script when run locally)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEEL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd 2>/dev/null || echo "")"

# Discover commands to install: all *.md in commands/ (local) or from GitHub API (curl case)
COMMANDS=()
if [ -d "${KEEL_ROOT}/commands" ]; then
  for f in "${KEEL_ROOT}"/commands/*.md; do
    [ -f "$f" ] && COMMANDS+=( "$(basename "$f")" )
  done
fi
if [ ${#COMMANDS[@]} -eq 0 ]; then
  while IFS= read -r name; do
    [ -n "$name" ] && COMMANDS+=( "$name" )
  done < <(curl -sL "https://api.github.com/repos/paulczar/keel/contents/commands" 2>/dev/null | grep -oE '"name"[[:space:]]*:[[:space:]]*"[^"]+\.md"' | sed 's/.*"\([^"]*\)"/\1/')
fi

installed=0

# When using curl, we download to a temp dir; clean up on exit
TEMP_DIR=""
trap 'rm -rf "$TEMP_DIR"' EXIT

get_command_source() {
  local name="$1"
  local local_path="${KEEL_ROOT}/commands/${name}"
  if [ -f "$local_path" ]; then
    echo "$local_path"
  else
    if [ -z "$TEMP_DIR" ]; then
      TEMP_DIR="$(mktemp -d)"
    fi
    local tmp="$TEMP_DIR/$name"
    curl -fsSL "https://raw.githubusercontent.com/paulczar/keel/main/commands/${name}" -o "$tmp"
    echo "$tmp"
  fi
}

install_command() {
  local dir="$1"
  local filename="$2"
  local source="$3"
  local dest="$TARGET/$dir/$filename"

  mkdir -p "$TARGET/$dir"
  cp "$source" "$dest"
  echo "  Installed $dir/$filename"
  installed=$((installed + 1))
}

install_commands_into() {
  local dir="$1"
  local cmd
  for cmd in "${COMMANDS[@]}"; do
    local src
    src="$(get_command_source "$cmd")"
    install_command "$dir" "$cmd" "$src"
  done
}

echo "Installing Keel slash commands in: $TARGET"
echo ""

# Claude Code: .claude/commands/
if [ -d "$TARGET/.claude" ] || command -v claude >/dev/null 2>&1; then
  install_commands_into ".claude/commands"
fi

# Cursor: .cursor/commands/
if [ -d "$TARGET/.cursor" ] || [ -f "$TARGET/.cursorrules" ]; then
  install_commands_into ".cursor/commands"
fi

# GitHub Copilot: .github/prompts/
if [ -d "$TARGET/.github" ]; then
  install_commands_into ".github/prompts"
fi

# If nothing was detected, install for all
if [ "$installed" -eq 0 ]; then
  echo "No AI tool directories detected. Installing for all supported tools."
  echo ""
  install_commands_into ".claude/commands"
  install_commands_into ".cursor/commands"
  install_commands_into ".github/prompts"
fi

echo ""
echo "Done! Installed ${#COMMANDS[@]} command(s) in $installed location(s)."
echo ""
echo "Usage:"
for cmd in "${COMMANDS[@]}"; do
  echo "  /${cmd%.md}"
done
echo ""
echo "  Claude Code, Cursor, Copilot: use /<command> in chat"
