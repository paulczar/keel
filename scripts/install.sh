#!/usr/bin/env bash
# DEPRECATED: This script is deprecated. Use keel-sync.py directly — it syncs
# both rules and slash commands in one run. This wrapper exists for backward
# compatibility and will be removed in a future version.

set -euo pipefail

TARGET="${1:-.}"
TARGET="$(cd "$TARGET" && pwd)"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEEL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd 2>/dev/null || echo "")"
SYNC_SCRIPT="${KEEL_ROOT}/scripts/keel-sync.py"

echo "DEPRECATED: install.sh is deprecated. Use keel-sync.py directly." >&2
echo "  python3 scripts/keel-sync.py --path content/rules --project <target>" >&2
echo "" >&2

if [ -f "$SYNC_SCRIPT" ]; then
  echo "Running keel-sync.py for backward compatibility..." >&2
  python3 "$SYNC_SCRIPT" --path "$KEEL_ROOT" --project "$TARGET" --force
else
  echo "Error: keel-sync.py not found. Run from a Keel clone or use:" >&2
  echo "  curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py | python3 - --clone https://github.com/paulczar/keel --project $TARGET" >&2
  exit 1
fi
