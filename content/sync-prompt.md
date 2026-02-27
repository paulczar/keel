---
title: "Sync Prompt"
weight: 50
bookToc: true
---

# Sync Prompt

The primary way to distribute Keel rules is to **ask your AI coding agent to do it**. Copy the prompt below, paste it into your agent in the target project, and let it figure out which rules apply and where to put them.

This works with any AI coding agent — Claude Code, Cursor, GitHub Copilot, Windsurf, Codex, or anything that accepts natural language instructions.

## Usage

1. Open your AI coding agent in the **target project** (the repo that should receive the rules)
2. Copy the prompt below
3. Replace `<KEEL_REPO_PATH>` with the path to your local Keel clone (or a GitHub raw URL)
4. Paste it into your agent and let it work

---

## The Prompt

```markdown
# Sync Coding Rules from Keel

You are setting up AI coding rules for this project. The rules are maintained
in a central repository (Project Keel) and need to be synced here in the
formats this project uses.

## Source

The Keel rule files are located at:

    <KEEL_REPO_PATH>/content/rules/

Each rule file is Markdown with YAML frontmatter containing these fields:
- `title` — Human-readable name (Hugo-only, do not sync)
- `description` — When this rule applies
- `globs` — File patterns that activate the rule
- `alwaysApply` — true if the rule applies globally, false if scoped by globs
- `tags` — Categories (Hugo-only, do not sync)
- `weight` — Sort order (Hugo-only, do not sync)

Ignore `_index.md` — it is a Hugo section index, not a rule.

## Step 1: Inspect this project

Look at the project structure — check for files like `package.json`, `go.mod`,
`pyproject.toml`, `Pipfile`, `Cargo.toml`, `Chart.yaml`, `*.yaml`, `*.tf`,
`Dockerfile`, etc. Determine which languages and frameworks are in use.

## Step 2: Select relevant rules

Read all rule files from the source. Select rules that are relevant:
- **Always include** rules where `alwaysApply: true` (e.g., `base.md`)
- **Include** language/framework rules whose `globs` match files that exist
  in this project (e.g., include `typescript.md` if there are `.ts` files)
- **Skip** rules for languages/frameworks not present in this project

Tell me which rules you selected and why before proceeding.

## Step 3: Detect output formats

Check what AI tooling this project already uses and determine which output
formats to generate:

| Signal | Format | Output Location |
|--------|--------|-----------------|
| `.cursor/` directory or `.cursorrules` exists | Cursor (MDC) | `.cursor/rules/keel/<name>.mdc` |
| `AGENTS.md` exists or project uses GitHub | AGENTS.md | `AGENTS.md` (root) + `.agents/rules/keel/<name>.md` |
| `CLAUDE.md` exists | Claude Code | Append references to `CLAUDE.md` |
| `.github/copilot-instructions.md` exists | Copilot | Append references to instructions file |
| None of the above detected | Default | Ask me which formats I want |

Rules are placed in a `keel/` subdirectory to support the layering model.
The project can add `org/` and `local/` subdirectories alongside `keel/`
to override or extend rules. See the base rule for precedence instructions.

If multiple formats are detected, generate all of them.

## Step 4: Generate output

### For `.agents/rules/keel/*.md` files:
Copy the rule files as-is, but **strip Hugo-only frontmatter fields** (`title`,
`tags`, `weight`). Keep `description`, `globs`, and `alwaysApply`.

### For `.cursor/rules/keel/*.mdc` files:
Same as above — strip `title`, `tags`, `weight` from frontmatter. Change the
file extension to `.mdc`. The body content stays identical.

### For `AGENTS.md`:
Generate a routing table at the top:

```
# AGENTS.md

## Rules

| Rule | Globs | Always Apply |
|------|-------|-------------|
| base | `["**/*"]` | true |
| typescript | `["**/*.ts", "**/*.tsx"]` | false |
...

## Rule Details

### base
- **Description:** Global coding standards
- **Globs:** `["**/*"]`
- **File:** `.agents/rules/keel/base.md`
```

Include a `## Rule Details` section with each rule's description, globs, and
a reference to the full file in `.agents/rules/`.

### For `CLAUDE.md` (if applicable):
Add a section pointing to the rule files:
```
## Coding Rules
See `.agents/rules/keel/` for detailed coding standards. Key rules:
- `.agents/rules/keel/base.md` — Global standards (always apply)
- `.agents/rules/keel/typescript.md` — TypeScript conventions (*.ts, *.tsx)
```

## Step 5: Handle existing rules

- If rule files already exist at the target paths, **show me the diff** and
  ask before overwriting
- If the project has hand-written rules (e.g., a custom `CLAUDE.md` or
  `.cursorrules`), **do not overwrite** — instead, append or create new files
  alongside them
- Never delete files that Keel didn't create

## Step 6: Summary

After syncing, show me:
1. Which rules were synced and which were skipped (with reasons)
2. Which output formats were generated
3. A list of all files created or modified
```

---

## For CI/CD Pipelines

If you need deterministic, non-interactive syncing (e.g., in a GitHub Action or
pre-commit hook), use the bash script instead:

```bash
./scripts/sync-rules.sh /path/to/target-repo
```

The bash script syncs **all** rules in **all** formats without inspection. It's
a blunt instrument — the sync prompt above is the recommended approach for
interactive use.
