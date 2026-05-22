# Sync Rules from Keel (Project-Local Mode)

This command is for **project-local mode** — when you want rules copied directly into this project rather than using a shared keel vault.

If this project uses a keel vault (configured in AGENTS.md), the agent reads rules directly from the vault path instead. No sync needed.

## Step 1: Check if vault mode is in use

If the project's AGENTS.md points to a keel vault path (`~/.keel/` or similar), tell the user that vault mode is active and the sync script isn't needed. Stop.

## Step 2: Locate the sync script

Try these in order:

1. **`KEEL_PATH` env var** — if set, the script is at `$KEEL_PATH/scripts/keel-sync.py`
2. **Sibling directory** — look for `../keel/scripts/keel-sync.py` relative to this project
3. **Download** — fetch the script to a temp location:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py -o /tmp/keel-sync.py
   ```

Set `SCRIPT` to the path of whichever you found.

## Step 3: Run the script

Build the command based on the arguments provided:

- **If an argument was provided** (a local path or URL):
  - If it looks like a URL: `python3 $SCRIPT --clone <arg>`
  - Otherwise: `python3 $SCRIPT --path <arg>`
- **If `KEEL_PATH` is set**: `python3 $SCRIPT --path $KEEL_PATH`
- **Otherwise**: `python3 $SCRIPT --clone https://github.com/paulczar/keel`

Always add `--force` so the script overwrites without prompting.

## Step 4: Report results

Show the user the script output. Summarize:
- Which rules were selected and which were skipped
- Which output formats were generated
- That slash commands (keel-sync, keel-apply) were installed to `.cursor/commands/`, `.claude/commands/`, `.github/prompts/`
- How many files were written
- Any errors encountered
