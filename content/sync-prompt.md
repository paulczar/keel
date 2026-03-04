---
title: "Sync Prompt"
weight: 50
bookToc: true
---

# Syncing Rules

The primary way to sync Keel rules into a project is the `keel-sync.py` script — a deterministic, zero-dependency Python tool that reads rule frontmatter, matches globs against the target project, and writes output files. Same input always produces the same output.

## Quick Start

No install needed — run directly with curl:

```bash
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py | python3 - --clone https://github.com/paulczar/keel
```

This shallow-clones the Keel repo to a temp directory, detects your project's languages and AI tooling, and writes the matching rules.

## Direct Script Usage

### From a local Keel clone

```bash
python3 scripts/keel-sync.py --path /path/to/keel/content/rules --project /path/to/target
```

### Shallow-clone and sync (no local clone needed)

```bash
python3 scripts/keel-sync.py --clone https://github.com/paulczar/keel --project /path/to/target
```

### Preview changes without writing

```bash
python3 scripts/keel-sync.py --path content/rules --dry-run
```

### Specify output formats explicitly

```bash
python3 scripts/keel-sync.py --path content/rules --formats agents,cursor
```

The script auto-detects output formats (Cursor, AGENTS.md, CLAUDE.md) based on what exists in the target project. Use `--formats` to override. It respects `.keelignore` in the target project root.

**Flags:** `--path`, `--clone`, `--pull`, `--project`, `--formats`, `--force`, `--dry-run`.

## Slash Commands

`keel-sync.py` installs slash commands automatically when you sync rules. No separate install step needed.

- **`/keel-sync`** — Syncs coding rules from Keel. Delegates to `keel-sync.py`; the LLM locates or downloads the script, runs it, and reports the results.
- **`/keel-apply`** — Audits the project against Keel best practices (`.gitignore`, `LICENSE`, `CONTRIBUTING.md`, etc.) and guides you through adding missing scaffolding. Never creates files automatically — it asks first and resolves ambiguity (e.g., which license).

### Install (via keel-sync.py)

Run `keel-sync.py` — it syncs both rules and slash commands in one go:

```bash
# No install needed — run directly with curl
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py | python3 - --clone https://github.com/paulczar/keel --project /path/to/target

# Or from a local Keel clone
python3 scripts/keel-sync.py --path content/rules --project /path/to/target
```

The script writes commands to:

| Tool | Location |
|------|----------|
| Claude Code | `.claude/commands/keel-sync.md`, `keel-apply.md`, etc. |
| Cursor | `.cursor/commands/keel-sync.md`, `keel-apply.md`, etc. |
| GitHub Copilot | `.github/prompts/keel-sync.md`, `keel-apply.md`, etc. |

**Note:** `install.sh` is deprecated; use `keel-sync.py` instead.

### Run

```
/keel-sync
/keel-apply
```

`/keel-sync` defaults to cloning rules from the GitHub repo. You can also pass a local path:

```
/keel-sync /path/to/keel/content/rules/
```

The command files are project-local and committable — your whole team gets them.

## Manual AI-Driven Sync (Legacy)

If you prefer to have the AI agent handle the full sync without the script (e.g., the agent doesn't have shell access), copy the prompt below into your agent in the target project.

This works with any AI coding agent — Claude Code, Cursor, GitHub Copilot, Windsurf, Codex, or anything that accepts natural language instructions.

1. Open your AI coding agent in the **target project**
2. Copy the prompt below
3. Optionally replace the GitHub URL with a local path if you have a Keel clone
4. Paste it into your agent and let it work

---

### The Prompt

```markdown
# Sync Coding Rules from Keel

You are setting up AI coding rules for this project. The rules are maintained
in a central repository (Project Keel) and need to be synced here in the
formats this project uses.

## Source

The Keel rule files can come from either:
1. **The GitHub repository** (default): `https://github.com/paulczar/keel`
   Use raw content URLs like:
   `https://raw.githubusercontent.com/paulczar/keel/main/content/rules/`
2. **A local path** if you have a clone: `/path/to/keel/content/rules/`

If a path or URL was provided as an argument, use that. Otherwise default to
fetching from the GitHub repository — no local clone needed.

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

List all rule files from the source, but **only read the YAML frontmatter**
(the content between the opening `---` and closing `---`) of each file. Do NOT
read the full file body at this stage — frontmatter alone contains `alwaysApply`,
`globs`, and `description`, which is all you need to determine relevance.

Select rules that are relevant:
- **Always include** rules where `alwaysApply: true` (e.g., `base.md`)
- **Include** language/framework rules whose `globs` match files that exist
  in this project (e.g., include `typescript.md` if there are `.ts` files)
- **Skip** rules for languages/frameworks not present in this project

Tell me which rules you selected and why before proceeding.

Only read the full body of selected rules in Step 4 when generating output.

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
a reference to the full file in `.agents/rules/keel/`.

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
