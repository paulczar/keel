# Testing Guide

This document covers how to test Keel end-to-end: the install script, the
`/keel-sync` slash command, and the Hugo site build.

## Prerequisites

- Bash 4+
- Git
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

## 2. Manual Install Test

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

## 3. Testing `/keel-sync` with Claude Code

This is the real end-to-end test: run the slash command and watch the AI agent
sync rules into a target project.

### Setup

```bash
# create a throwaway project to sync into
mkdir /tmp/keel-test-project && cd /tmp/keel-test-project
git init

# give it some language files so the agent has something to detect
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
/keel-sync /path/to/keel/content/rules/
```

### What to verify

The agent should:

1. **Inspect the project** — recognize Go files (`main.go`, `go.mod`)
2. **Select rules** — tell you which rules it picked and why:
   - `base.md` (alwaysApply: true)
   - `agent-behavior.md` (alwaysApply: true)
   - `scaffolding.md` (alwaysApply: true)
   - `go.md` (globs match `*.go` / `go.mod`)
   - Possibly `markdown.md` if it sees `.md` files
   - Should skip: `typescript.md`, `python.md`, `helm.md`, `terraform.md`,
     `kubernetes.md`, `hugo.md`, `mdc.md`
3. **Detect output formats** — since `.claude/` exists (we just installed
   the command there), it should generate Claude/AGENTS format
4. **Create files** — check that these exist afterward:
   - `.agents/rules/keel/base.md`
   - `.agents/rules/keel/agent-behavior.md`
   - `.agents/rules/keel/scaffolding.md`
   - `.agents/rules/keel/go.md`
   - `AGENTS.md` with a routing table
5. **Strip Hugo fields** — open any generated rule file and confirm that
   `title`, `tags`, and `weight` are removed from the frontmatter, but
   `description`, `globs`, and `alwaysApply` are kept

### Verify the output

```bash
# check files were created
ls -la .agents/rules/keel/
cat AGENTS.md

# confirm Hugo-only fields are stripped
head -20 .agents/rules/keel/base.md
# should NOT contain: title, tags, weight
# should contain: description, globs, alwaysApply

# confirm the routing table
grep -c '|' AGENTS.md   # should have table rows
```

## 4. Testing `/keel-sync` with Cursor

Same setup as above, but create a `.cursor/` directory so the agent detects
Cursor format:

```bash
mkdir /tmp/keel-test-cursor && cd /tmp/keel-test-cursor
git init
cp /tmp/keel-test-project/main.go /tmp/keel-test-project/go.mod .
mkdir .cursor
/path/to/keel/scripts/install.sh .
```

Open Cursor, then run `/keel-sync` and provide the path to
`/path/to/keel/content/rules/` when prompted.

Verify:
- [ ] `.cursor/rules/keel/base.mdc` exists (note `.mdc` extension)
- [ ] `.cursor/rules/keel/go.mdc` exists
- [ ] Frontmatter has `description`, `globs`, `alwaysApply` but not `title`,
      `tags`, `weight`
- [ ] Rule body content matches the source

## 5. Testing with Multiple AI Tools

Create a project with markers for all tools:

```bash
mkdir /tmp/keel-test-multi && cd /tmp/keel-test-multi
git init
echo 'module example.com/test' > go.mod
echo 'package main' > main.go
mkdir .cursor .claude .github
/path/to/keel/scripts/install.sh .
```

Run `/keel-sync` from any tool. Verify the agent generates all formats:
- [ ] `.cursor/rules/keel/*.mdc`
- [ ] `.agents/rules/keel/*.md`
- [ ] `AGENTS.md`

## 6. Hugo Site Build

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

## 7. Cleanup

```bash
rm -rf /tmp/keel-test-project /tmp/keel-test-cursor /tmp/keel-test-multi
```
