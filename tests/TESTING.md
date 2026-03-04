# Testing Guide

This document covers how to test Keel end-to-end: the install script, the
`keel-sync.py` script, the `/keel-sync` slash command, and the Hugo site build.

## Prerequisites

- Bash 4+
- Git
- Python 3
- Hugo (`/opt/homebrew/bin/hugo` or adjust `HUGO` in `Makefile`)
- At least one AI tool: Claude Code (`claude`), Cursor, or GitHub Copilot

## 1. Automated Tests

Run the install-script test suite:

```bash
make test
```

This creates a temp directory with a Go fixture project, runs `install.sh`
against it under five scenarios, and verifies the right files land in the right
places. All tests run with a restricted `PATH` so results are deterministic
regardless of which AI CLIs you have installed.

| Test | Setup | Expected result |
|------|-------|-----------------|
| No AI dirs | bare project | installs to all three destinations (fallback) |
| `.cursor/` exists | `mkdir .cursor` | only `.cursor/commands/keel-sync.md` |
| `.claude/` exists | `mkdir .claude` | only `.claude/commands/keel-sync.md` |
| `.github/` exists | `mkdir .github` | only `.github/prompts/keel-sync.md` |
| `.cursorrules` file | `touch .cursorrules` | only `.cursor/commands/keel-sync.md` |

## 2. keel-sync.py Tests

Run the pytest suite for `scripts/keel-sync.py`:

```bash
python3 -m pytest tests/test_keel_sync.py -v
```

Or run all tests together:

```bash
make test
```

### Manual end-to-end test

```bash
# Create a throwaway project
mkdir /tmp/keel-sync-test && cd /tmp/keel-sync-test
git init
echo 'package main' > main.go
echo 'module example.com/test' > go.mod

# Dry-run to preview which rules match and what would be written
python3 /path/to/keel/scripts/keel-sync.py \
  --path /path/to/keel/content/rules \
  --project . \
  --dry-run

# Actual sync
python3 /path/to/keel/scripts/keel-sync.py \
  --path /path/to/keel/content/rules \
  --project .

# Verify output
ls -la .agents/rules/keel/
cat AGENTS.md
head -20 .agents/rules/keel/base.md   # should NOT have title/tags/weight

# Cleanup
rm -rf /tmp/keel-sync-test
```

### Curl one-liner test

Verify the script can be run without a local clone:

```bash
mkdir /tmp/keel-curl-test && cd /tmp/keel-curl-test
git init
echo 'package main' > main.go
echo 'module example.com/test' > go.mod

# Run via curl — should clone, detect Go, and sync rules
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py | python3 - --clone https://github.com/paulczar/keel --project .

# Verify
ls -la .agents/rules/keel/

# Cleanup
rm -rf /tmp/keel-curl-test
```

## 3. Manual Install Test

Test the install script against a real project on your machine:

```bash
# pick any git repo you have locally
cd /path/to/some-project

# run install from the Keel repo
/path/to/keel/scripts/install.sh .
```

Verify:
- [ ] Output says "Installing keel-sync command in: ..."
- [ ] Correct destinations were detected (check which AI dirs exist)
- [ ] The installed file content matches `commands/keel-sync.md`

Then test the curl-based install (simulates a user who hasn't cloned Keel):

```bash
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/install.sh | bash -s /path/to/some-project
```

Verify:
- [ ] Script downloads `keel-sync.md` from GitHub and installs it
- [ ] Same detection logic applies

## 4. Testing `/keel-sync` with Claude Code

The slash command delegates to `keel-sync.py`. The AI agent's job is to locate
or download the script, run it, and report the output — not to perform the
sync logic itself.

### Setup

```bash
# create a throwaway project to sync into
mkdir /tmp/keel-test-project && cd /tmp/keel-test-project
git init

# give it some language files so the script has something to detect
cat > main.go <<'EOF'
package main

import "fmt"

func main() { fmt.Println("hello") }
EOF

cat > go.mod <<'EOF'
module example.com/test
go 1.21
EOF

# install the slash command
/path/to/keel/scripts/install.sh .
```

### Run the sync

Open Claude Code in the test project:

```bash
cd /tmp/keel-test-project
claude
```

Then run:

```
/keel-sync
```

### What to verify

The agent should:

1. **Check for python3** — verify it's available
2. **Locate or download keel-sync.py** — via `KEEL_PATH`, sibling dir, or curl
3. **Run the script** — with `--clone https://github.com/paulczar/keel --force`
4. **Report the output** — show which rules were selected, formats generated,
   and files written

The script (not the LLM) handles:
- Project inspection and language detection
- Rule selection based on globs and `alwaysApply`
- Format detection (Cursor, AGENTS.md, CLAUDE.md)
- File generation with Hugo field stripping

### Verify the output

```bash
# check files were created
ls -la .agents/rules/keel/
cat AGENTS.md

# confirm Hugo-only fields are stripped
head -20 .agents/rules/keel/base.md
# should NOT contain: title, tags, weight
# should contain: description, globs, alwaysApply
```

## 5. Testing `/keel-sync` with Cursor

Same setup as above, but create a `.cursor/` directory so the script detects
Cursor format:

```bash
mkdir /tmp/keel-test-cursor && cd /tmp/keel-test-cursor
git init
cp /tmp/keel-test-project/main.go /tmp/keel-test-project/go.mod .
mkdir .cursor
/path/to/keel/scripts/install.sh .
```

Open Cursor, then run `/keel-sync`.

Verify:
- [ ] The agent runs `keel-sync.py` (not doing the sync itself)
- [ ] `.cursor/rules/keel/base.mdc` exists (note `.mdc` extension)
- [ ] `.cursor/rules/keel/go.mdc` exists
- [ ] Frontmatter has `description`, `globs`, `alwaysApply` but not `title`,
      `tags`, `weight`
- [ ] Rule body content matches the source

## 6. Testing with Multiple AI Tools

Create a project with markers for all tools:

```bash
mkdir /tmp/keel-test-multi && cd /tmp/keel-test-multi
git init
echo 'module example.com/test' > go.mod
echo 'package main' > main.go
mkdir .cursor .claude .github
/path/to/keel/scripts/install.sh .
```

Run `/keel-sync` from any tool. Verify the agent runs the script and it generates
all formats:
- [ ] `.cursor/rules/keel/*.mdc`
- [ ] `.agents/rules/keel/*.md`
- [ ] `AGENTS.md`

## 7. Hugo Site Build

Verify the documentation site builds without errors:

```bash
make build
```

Check the output:
- [ ] `public/` directory is created
- [ ] `public/rules/` has a page for each rule
- [ ] `public/sync-prompt/` exists
- [ ] `public/layering/` exists
- [ ] No build warnings or errors

Preview locally:

```bash
make preview
```

Then open `http://localhost:1313/keel/` and check:
- [ ] Rules are listed in the sidebar
- [ ] Each rule page shows the metadata box (globs, alwaysApply, tags)
- [ ] Search works
- [ ] Sync prompt page renders correctly

## 8. Cleanup

```bash
rm -rf /tmp/keel-test-project /tmp/keel-test-cursor /tmp/keel-test-multi
```
