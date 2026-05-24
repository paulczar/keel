---
title: "Vault Project Sync"
description: "Resync a project's vault symlinks and configs after the vault updates."
weight: 20
---

# Vault Project Sync

Refreshes a project's vault connection after the keel framework has been updated (e.g., `git pull` in the vault). Rebuilds skill symlinks and checks that AGENTS.md references are current.

## When to run

- After updating the vault: `cd ~/.keel/content/keel && git pull`
- When new skills or rules were added to keel
- When a behavior profile was changed in the vault

## Steps

### Step 1: Read existing config

Read the project's AGENTS.md to find the vault path. If no AGENTS.md or no vault path is configured, suggest vault-project-init.

### Step 2: Verify vault is current

Check the vault's git status:

```bash
cd <vault>/content/keel && git log --oneline -3
```

If the vault is behind upstream, suggest pulling: `git pull`.

### Step 3: Rebuild skill symlinks

Remove old symlinks and recreate from current vault:

```bash
# Find and update opencode skills
mkdir -p .opencode/skills
for skill in <vault>/content/keel/content/skills/*.md; do
  name=$(basename "$skill" .md)
  [ "$name" = "_index" ] && continue
  mkdir -p ".opencode/skills/$name"
  ln -sf "$skill" ".opencode/skills/$name/SKILL.md"
done
```

### Step 4: Check for new content

Compare the vault's content sections against what the project has access to:

- New rules in `content/keel/content/rules/` — no action needed (agent reads them directly)
- New skills in `content/keel/content/skills/` — symlinked in step 3
- New MCP tools in `content/keel/content/mcp/` — remind the user they exist
- New behavior profiles in `content/keel/content/behaviors/` — offer to switch

### Step 5: Report

- Skills synced: N
- AGENTS.md status: current / needs update
- New content available: (list)
- Vault commit: (hash)

## See also

- [Vault Project Init]({{< relref "/skills/vault-project-init" >}}) — initial project setup
- [Vault Project Migrate]({{< relref "/skills/vault-project-migrate" >}}) — convert project-local setup
- [Vault Init]({{< relref "/skills/vault-init" >}}) — bootstrap the vault itself
