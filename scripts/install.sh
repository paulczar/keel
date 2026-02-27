#!/usr/bin/env bash
set -euo pipefail

# Keel slash command installer
# Installs the /keel-sync command into AI tool directories in the current project.
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
COMMAND_SOURCE="${KEEL_ROOT}/commands/keel-sync.md"

installed=0

# If we can't find the source command (curl case), embed it
if [ ! -f "$COMMAND_SOURCE" ]; then
  COMMAND_SOURCE="$(mktemp)"
  trap 'rm -f "$COMMAND_SOURCE"' EXIT
  curl -fsSL "https://raw.githubusercontent.com/paulczar/keel/main/commands/keel-sync.md" -o "$COMMAND_SOURCE"
fi

install_command() {
  local dir="$1"
  local filename="$2"
  local dest="$TARGET/$dir/$filename"

  mkdir -p "$TARGET/$dir"
  cp "$COMMAND_SOURCE" "$dest"
  echo "  Installed $dir/$filename"
  installed=$((installed + 1))
}

echo "Installing keel-sync command in: $TARGET"
echo ""

# Claude Code: .claude/commands/
if [ -d "$TARGET/.claude" ] || command -v claude >/dev/null 2>&1; then
  install_command ".claude/commands" "keel-sync.md"
fi

# Cursor: .cursor/commands/
if [ -d "$TARGET/.cursor" ] || [ -f "$TARGET/.cursorrules" ]; then
  install_command ".cursor/commands" "keel-sync.md"
fi

# GitHub Copilot: .github/prompts/
if [ -d "$TARGET/.github" ]; then
  install_command ".github/prompts" "keel-sync.md"
fi

# If nothing was detected, ask
if [ "$installed" -eq 0 ]; then
  echo "No AI tool directories detected. Installing for all supported tools."
  echo ""
  install_command ".claude/commands" "keel-sync.md"
  install_command ".cursor/commands" "keel-sync.md"
  install_command ".github/prompts" "keel-sync.md"
fi

echo ""
echo "Done! Installed keel-sync command in $installed location(s)."
echo ""
echo "Usage:"
echo "  Claude Code:  /keel-sync /path/to/keel/content/rules/"
echo "  Cursor:       /keel-sync (then provide the path when prompted)"
echo "  Copilot:      /keel-sync (in Copilot Chat)"
