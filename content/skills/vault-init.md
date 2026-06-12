---
title: "Vault Init"
description: "Bootstrap a new keel vault from scratch."
weight: 5
---

# Init Vault

Bootstraps a new keel vault at `~/.keel/` (or a custom path). Clones the framework, picks a behavior profile, sets up the directory structure, and configures local tooling.

## Prerequisites

- Git installed
- Write access to the target directory (default `~/.keel/`)

## Smart detection

Before setting up the vault, check whether this project already has agent configs:

- Does it have an AGENTS.md or CLAUDE.md with local rules?
- Does it have a `KNOWLEDGE.md`, `local/`, or `docs/` with knowledge files?
- Does it have `.opencode/skills/`, `.cursor/rules/`, or similar tooling configs?

If yes, this project has existing context that should be preserved. **Suggest running vault-project-migrate instead** — it will migrate the existing configs into the new vault structure. Offer to run vault-init anyway if the user just wants a clean vault without migrating.

## Steps

### Step 1: Ask where to put the vault

Ask the user where they want the vault to live. Default is `~/.keel/`.

Check if the path already exists. If it does, confirm they want to overwrite/reuse it.

### Step 2: Clone the framework

```bash
git clone https://github.com/paulczar/keel <vault>/keel
```

### Step 3: Pick a behavior profile

Show the user the available profiles and ask which they want:

- **Karpathy** — Balanced, cautious. Good default.
- **Strict** — Maximum guardrails. Production/regulated environments.
- **Vibe** — Minimal friction. Prototypes, personal projects.

Copy the chosen profile to `<vault>/AGENTS.md`.

### Step 4: Create local directories

```bash
mkdir -p <vault>/local/knowledge
mkdir -p <vault>/local/skills
```

### Step 5: Set up gitignore

```bash
cat > <vault>/.gitignore << 'EOF'
tmp/
EOF
```

### Step 6: Ask about git remotes

Ask if the user wants to set up any git remotes (e.g., their own fork for personalizing the framework). If yes, ask for the remote URL and add it to the keel clone:

```bash
cd <vault>/keel
git remote add fork <url>
```

### Step 7: Ask about AI tools

Ask which AI tools the user uses (opencode, Claude Code, Cursor, Copilot, etc.) and install vault skills into each.

**For opencode (ask: global profile or per-project?):**

Install globally to `~/.config/opencode/skills/` so skills are available in every project:

```bash
mkdir -p ~/.config/opencode/skills
for skill in <vault>/keel/content/skills/*.md; do
  name=$(basename "$skill" .md)
  [ "$name" = "_index" ] && continue
  mkdir -p "${HOME}/.config/opencode/skills/${name}"
  # Convert Hugo frontmatter (title, description) to OpenCode frontmatter (name, description)
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

If they prefer per-project (e.g., for team repos), symlink into `.opencode/skills/` instead:

```bash
mkdir -p .opencode/skills
for skill in <vault>/keel/content/skills/*.md; do
  name=$(basename "$skill" .md)
  [ "$name" = "_index" ] && continue
  mkdir -p ".opencode/skills/$name"
  ln -sf "$skill" ".opencode/skills/$name/SKILL.md"
done
```

**For Claude Code:**

```bash
mkdir -p ~/.claude/skills
# Same pattern as opencode global, into ~/.claude/skills/<name>/SKILL.md
```

**For Cursor:**

```bash
mkdir -p .cursor/rules/keel
# Symlink rules from the vault
```

### Step 8: Summary

Show the user what was set up:

- Vault location
- Behavior profile chosen
- Tools configured
- Next steps: set vault path in any project's AGENTS.md, run the vault-project-migrate skill for existing projects

## See also

- [Getting Started]({{< relref "/getting-started" >}}) — human-readable version with bootstrap prompt
- [Migrate to Vault]({{< relref "/skills/vault-project-migrate" >}}) — convert existing projects to vault mode
- [Knowledge Management]({{< relref "/skills/vault-knowledge" >}}) — using the vault's knowledge wiki
