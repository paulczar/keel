#!/usr/bin/env bash
# Install Keel as a Cursor Plugin (local install, no marketplace required).
#
# Usage:
#   ./scripts/install-plugin.sh              # from a Keel clone
#   ./scripts/install-plugin.sh --clone URL  # clone from Git first
#
# After install: restart Cursor. Rules and commands (/keel-sync, /keel-apply)
# will appear. You may need to enable "Include third-party Plugins, Skills,
# and other configs" in Settings > Features.
#
# For /keel-sync to find the script when syncing to other projects, set:
#   export KEEL_PATH=~/.cursor/plugins/keel

set -euo pipefail

PLUGIN_NAME="keel"
PLUGIN_ID="${PLUGIN_NAME}@local"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEEL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Resolve source: local or clone
if [[ "${1:-}" == "--clone" && -n "${2:-}" ]]; then
  REPO_URL="$2"
  TMP="$(mktemp -d -t keel-install-XXXXXX)"
  trap 'rm -rf "$TMP"' EXIT
  echo "Cloning $REPO_URL ..."
  git clone --depth 1 -q "$REPO_URL" "$TMP"
  SOURCE="$TMP"
else
  SOURCE="$KEEL_ROOT"
fi

if [[ ! -f "$SOURCE/.cursor-plugin/plugin.json" ]]; then
  echo "Error: No plugin manifest at $SOURCE/.cursor-plugin/plugin.json" >&2
  exit 1
fi

command -v python3 >/dev/null || { echo "Error: python3 required for JSON updates" >&2; exit 1; }

TARGET="$HOME/.cursor/plugins/$PLUGIN_NAME"
CLAUDE_PLUGINS="$HOME/.claude/plugins/installed_plugins.json"
CLAUDE_SETTINGS="$HOME/.claude/settings.json"

# 1. Copy plugin files
echo "Installing to $TARGET ..."
rm -rf "$TARGET"
mkdir -p "$TARGET"
for dir in .cursor-plugin content commands scripts; do
  if [[ -d "$SOURCE/$dir" ]]; then
    cp -R "$SOURCE/$dir" "$TARGET/"
  fi
done

# 2. Register in installed_plugins.json (upsert)
python3 - "$CLAUDE_PLUGINS" "$PLUGIN_ID" "$TARGET" <<'PY'
import json, os, sys
path, pid, ipath = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
data = {}
if os.path.exists(path):
    try:
        data = json.load(open(path))
    except Exception:
        data = {}
plugins = data.get("plugins", {})
entries = [e for e in plugins.get(pid, []) if not (isinstance(e, dict) and e.get("scope") == "user")]
entries.insert(0, {"scope": "user", "installPath": ipath})
plugins[pid] = entries
data["plugins"] = plugins
os.makedirs(os.path.dirname(path), exist_ok=True)
json.dump(data, open(path, "w"), indent=2)
PY

# 3. Enable in settings.json (upsert)
python3 - "$CLAUDE_SETTINGS" "$PLUGIN_ID" <<'PY'
import json, os, sys
path, pid = sys.argv[1], sys.argv[2]
data = {}
if os.path.exists(path):
    try:
        data = json.load(open(path))
    except Exception:
        data = {}
data.setdefault("enabledPlugins", {})[pid] = True
os.makedirs(os.path.dirname(path), exist_ok=True)
json.dump(data, open(path, "w"), indent=2)
PY

echo ""
echo "Installed Keel as a Cursor Plugin."
echo ""
echo "Next steps:"
echo "  1. Restart Cursor (Cmd+Shift+P → 'Reload Window' or quit and reopen)"
echo "  2. If commands don't appear: Settings > Features > enable 'Include third-party Plugins, Skills, and other configs'"
echo ""
echo "For /keel-sync to work when syncing to other projects, add to your shell profile:"
echo "  export KEEL_PATH=\"$TARGET\""
