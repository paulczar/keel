---
title: "Vault Project Init"
description: "Wire a new project to use an existing keel vault."
weight: 15
---

# Vault Project Init

Sets up a new or existing project to use a keel vault. Creates AGENTS.md, symlinks skills, and sets up local knowledge directories.

## Prerequisites

- A keel vault exists at `~/.keel/` (or custom path)
- Git installed

## Steps

### Step 1: Locate the vault

Check for the vault at `~/.keel/`:

```bash
ls ~/.keel/keel/ 2>/dev/null
```

If not found, suggest running vault-init first.

### Step 2: Detect project context

Check what the project already has — don't overwrite anything without asking.

- Does it have an AGENTS.md? If so, offer to update it rather than replace.
- Does it have a CLAUDE.md? Offer to add vault references.
- Does it already use opencode, Claude Code, or Cursor?

### Step 3: Create or update AGENTS.md

Write an AGENTS.md that references the vault:

```markdown
# AGENTS.md

This project uses keel vault mode.

## Vault path

~/.keel/

## Knowledge sources (precedence order)

1. `./local/knowledge/` — project-specific (highest)
2. `~/.keel/local/knowledge/` — personal vault
3. `~/.keel/keel/content/knowledge/` — keel framework (lowest)
```

### Step 4: Install vault skills into project tooling

Symlink vault skills so the project's agents can load them:

```bash
# For opencode
mkdir -p .opencode/skills
for skill in ~/.keel/keel/content/skills/*.md; do
  name=$(basename "$skill" .md)
  [ "$name" = "_index" ] && continue
  mkdir -p ".opencode/skills/$name"
  ln -sf "$skill" ".opencode/skills/$name/SKILL.md"
done
```

### Step 5: Create local knowledge directory

```bash
mkdir -p local/knowledge
echo "# Project Knowledge" > local/knowledge/index.md
```

### Step 6: Summary

- AGENTS.md created with vault path
- Skills symlinked to vault
- Local knowledge directory ready
- Next: use vault-project-sync when the vault updates

## See also

- [Vault Project Sync]({{< relref "/skills/vault-project-sync" >}}) — resync after vault updates
- [Vault Project Migrate]({{< relref "/skills/vault-project-migrate" >}}) — convert project-local setup
- [Vault Init]({{< relref "/skills/vault-init" >}}) — bootstrap the vault itself
