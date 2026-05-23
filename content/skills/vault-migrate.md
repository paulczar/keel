---
title: "Vault Migrate"
description: "Migrate a project from project-local mode to keel vault mode."
weight: 40
---

# Migrate to Vault

Converts a project from standalone mode (rules/skills/knowledge inside the project) to vault mode (shared `~/.keel/` vault with the project referencing it).

## Prerequisites

- The project has an AGENTS.md or CLAUDE.md (or local knowledge files)
- Git installed

## Migration steps

### Step 1: Check for existing vault

Check if `~/.keel/` exists:

```bash
ls ~/.keel/content/keel/content/skills/ 2>/dev/null
```

If the vault exists, skip to Step 2.

### Step 2: Bootstrap the vault (delegate to vault-init)

If no vault exists, run vault-init first:

1. Tell the user: "No keel vault found. Let's set one up first."
2. Load the vault-init skill and follow its steps
3. Return here after the vault is bootstrapped

### Step 3: Inventory project knowledge

Scan the project for existing knowledge files:

- `KNOWLEDGE.md` in project root
- `content/local/knowledge/` if it exists
- `docs/` or `notes/` directories that look like knowledge
- Any agent-created files the project has accumulated

### Step 4: Offer migration choices

For each knowledge source found, ask the user:

- **Project-specific** (configs, CI quirks, team conventions) → leave in project at `./local/knowledge/`
- **Personal** (learnings, gotchas, preferences) → move to `~/.keel/content/local/knowledge/`
- **Universal** (should be in the framework) → migrate to keel as a PR later

### Step 5: Update project AGENTS.md

Replace the project's AGENTS.md with a vault-mode configuration:

```markdown
# AGENTS.md

## Vault

This project uses keel vault mode. Agent context sources:

- **Rules**: `~/.keel/content/keel/content/rules/`
- **Skills**: `~/.keel/content/keel/content/skills/`
- **Knowledge**: `~/.keel/content/keel/content/knowledge/` (keel framework)
- **Local knowledge**: `./local/knowledge/` (project-specific)

Knowledge sources in precedence order:
1. `./local/knowledge/` — project-specific (highest)
2. `~/.keel/content/local/knowledge/` — personal vault
3. `~/.keel/content/keel/content/knowledge/` — keel framework (lowest)

When knowledge from different sources conflicts, higher precedence wins.
When an assumption proves incorrect, add a correction to the appropriate knowledge source before moving on.
```

### Step 6: Install vault skills into project tooling

Symlink or copy keel skills so the project's agents can load them:

```bash
# For opencode
mkdir -p .opencode/skills
for skill in ~/.keel/content/keel/content/skills/*.md; do
  name=$(basename "$skill" .md)
  [ "$name" = "_index" ] && continue
  mkdir -p ".opencode/skills/$name"
  ln -sf "$skill" ".opencode/skills/$name/SKILL.md"
done

# For Claude Code (if used)
mkdir -p .claude/skills
# Symlink similarly
```

### Step 7: Report

Summarize what was done:

- Vault location: `~/.keel/`
- Behavior profile chosen
- Knowledge files kept in project vs moved to vault
- AGENTS.md updated
- Skills symlinked into project tooling
- Any cleanup performed (original KNOWLEDGE.md backed up, etc.)

## Cleanup

After migration:

- If `KNOWLEDGE.md` content was moved, either delete it or replace with a symlink to the vault copy
- If `keel-sync.py` was the previous method, it's no longer needed for vault mode — but can be left for project-local use in other projects

## See also

- [Getting Started]({{< relref "/getting-started" >}}) — bootstrap a new vault from scratch
- [Knowledge Management]({{< relref "/skills/vault-knowledge" >}}) — using the vault's knowledge wiki
- [Skill Builder]({{< relref "/skills/vault-skill-create" >}}) — creating project or vault-level skills
