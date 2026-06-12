---
title: "Vault Project Sync"
description: "Resync a project's vault symlinks and configs after the vault updates."
weight: 20
---

# Vault Project Sync

Refreshes a project's vault connection after the keel framework has been updated (e.g., `git pull` in the vault). Rebuilds skill symlinks and checks that AGENTS.md references are current.

## When to run

- After updating the vault: `cd ~/.keel/keel && git pull`
- When new skills or rules were added to keel
- When a behavior profile was changed in the vault

## Steps

### Step 1: Read existing config

Read the project's AGENTS.md to find the vault path. If no AGENTS.md or no vault path is configured, suggest vault-project-init.

### Step 2: Verify vault is current

Check the vault's git status:

```bash
cd <vault>/keel && git log --oneline -3
```

If the vault is behind upstream, suggest pulling: `git pull`.

### Step 3: Rebuild skill symlinks

Detect which installation method was used previously (check `~/.config/opencode/skills/` for global, `.opencode/skills/` for per-project) and rebuild from current vault.

**For global install:**

```bash
mkdir -p ~/.config/opencode/skills
for skill in <vault>/keel/content/skills/*.md; do
  name=$(basename "$skill" .md)
  [ "$name" = "_index" ] && continue
  mkdir -p "${HOME}/.config/opencode/skills/${name}"
  desc=$(head -5 "$skill" | grep 'description:' | sed 's/description: *"\(.*\)"/\1/')
  body=$(sed '1,/^---$/d' "$skill" | sed '1,/^---$/d')
  cat > "${HOME}/.config/opencode/skills/${name}/SKILL.md" << SKILLEOF
---
name: ${name}
description: ${desc}
---

${body}
SKILLEOF
done
```

**For per-project install:**

```bash
mkdir -p .opencode/skills
for skill in <vault>/keel/content/skills/*.md; do
  name=$(basename "$skill" .md)
  [ "$name" = "_index" ] && continue
  mkdir -p ".opencode/skills/$name"
  ln -sf "$skill" ".opencode/skills/$name/SKILL.md"
done
```

### Step 4: Check for new content

Compare the vault's content sections against what the project has access to:

- New rules in `keel/content/rules/` — no action needed (agent reads them directly)
- New skills in `keel/content/skills/` — symlinked in step 3
- New MCP tools in `keel/content/mcp/` — remind the user they exist
- New behavior profiles in `keel/content/behaviors/` — offer to switch

### Step 5: Report

- Skills synced: N
- AGENTS.md status: current / needs update
- New content available: (list)
- Vault commit: (hash)

## See also

- [Vault Project Init]({{< relref "/skills/vault-project-init" >}}) — initial project setup
- [Vault Project Migrate]({{< relref "/skills/vault-project-migrate" >}}) — convert project-local setup
- [Vault Init]({{< relref "/skills/vault-init" >}}) — bootstrap the vault itself
