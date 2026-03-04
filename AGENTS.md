# AGENTS.md — Project Keel

This file describes the Keel repository for AI agents working on the CMS itself. This is NOT the generated AGENTS.md that the sync prompt produces for downstream projects.

## Project Overview

Keel is a Hugo-powered CMS that serves as a centralized source of truth for AI coding rules. It renders Markdown rule files as a searchable documentation website for humans, while the same files serve as machine-actionable context for AI agents.

## Repository Structure

```
.
├── AGENTS.md                  # This file (agent instructions for this repo)
├── CLAUDE.md                  # Points Claude Code to AGENTS.md
├── .cursorrules               # Points Cursor to AGENTS.md
├── Makefile                   # Build, preview, and local rule targets
├── hugo.yaml                  # Hugo site configuration
├── content/
│   ├── _index.md              # Landing page / manifesto
│   ├── layering.md            # Rule layering documentation
│   ├── sync-prompt.md         # Copy-pasteable sync prompt for AI agents
│   └── rules/
│       ├── _index.md          # Rules section index
│       ├── base.md            # Global rules (alwaysApply: true)
│       ├── agent-behavior.md  # Agent safety and behavioral rules
│       ├── scaffolding.md     # Project scaffolding standards
│       ├── typescript.md      # TypeScript/React standards
│       ├── python.md          # Python standards
│       ├── go.md              # Go standards
│       ├── terraform.md       # Terraform IaC standards
│       ├── kubernetes.md      # Kubernetes manifest standards
│       ├── helm.md            # Helm chart standards
│       ├── yaml.md            # YAML formatting standards
│       ├── markdown.md        # Markdown writing standards
│       ├── hugo.md            # Hugo development standards
│       └── mdc.md             # Cursor MDC format standards
├── commands/
│   ├── keel-sync.md           # Canonical /keel-sync slash command (tool-agnostic)
│   └── keel-apply.md          # Apply best practices (LICENSE, .gitignore, CONTRIBUTING, etc.)
├── scripts/
│   ├── install.sh             # Installs slash commands into target projects
│   └── keel-sync.py           # Deterministic rule sync (no LLM needed)
├── .cursor/
│   └── rules/keel/            # Symlinks to content/rules/ for local use
├── layouts/
│   └── partials/docs/inject/
│       └── content-before.html  # AI metadata box partial
├── assets/
│   └── _custom.scss           # Metadata box styles
├── themes/
│   └── hugo-book/             # Theme (git submodule, pinned to v10)
└── .github/
    └── workflows/
        └── deploy.yml         # GitHub Pages deployment
```

## Rule File Format

Every rule file in `content/rules/` uses this frontmatter schema:

```yaml
---
title: "Human-readable title"
description: "When this rule applies"
globs: ["**/pattern/*.ext"]
alwaysApply: false
tags: ["category"]
weight: 1
---
```

### Field Definitions

- **title** — Display title for the Hugo site sidebar and page heading
- **description** — Brief explanation of when/why this rule applies
- **globs** — File patterns that activate this rule (AGENTS.md scope). Use single-line flow-sequence format (`[...]`) for consistency
- **alwaysApply** — `true` for rules that apply globally; `false` for context-specific rules
- **tags** — Categories for filtering (rendered as taxonomy pages by Hugo)
- **weight** — Sort order in the sidebar (lower = higher)

## Rule Structure Conventions

Every language/tool rule should follow this section pattern:

1. **Tooling** — formatters, linters, type checkers, and validation tools
2. *(Language-specific sections — style, patterns, testing, etc.)*
3. **Agent Behavior** — when and how agents should run validation tools
4. **.gitignore** — language-specific ignore patterns

The `base.md` rule defines a **Code Validation** policy: agents should automatically run the relevant tooling after significant changes. Projects can opt out by setting `skip-auto-validation: true` in their `AGENTS.md` or a local rule.

## Rule Layering

Rules support three precedence layers (see `content/layering.md`):

1. **Local** (`local/`) — project or team-specific. Highest precedence.
2. **Org** (`org/`) — organizational standards.
3. **Keel** (`keel/`) — global defaults. Lowest precedence.

Higher layers fully replace lower-layer rules on the same topic. Non-conflicting rules are additive. The precedence instructions are embedded in `base.md` (which is `alwaysApply: true`).

## Common Workflows

### Adding a New Rule

1. Create `content/rules/<name>.md` with the frontmatter schema above
2. Write the rule body in Markdown — include Tooling and Agent Behavior sections
3. Run `make preview` to preview locally
4. Run `make build` to verify the build succeeds
5. If the rule applies to this repo, add it to `CURSOR_RULES` in the Makefile and run `make rules`

### Modifying the Metadata Display

- Template: `layouts/partials/docs/inject/content-before.html`
- Styles: `assets/_custom.scss`
- Hugo reads `.Params` from frontmatter — field names are lowercased by Hugo

### Syncing with keel-sync.py

`scripts/keel-sync.py` is the primary sync method — a deterministic, zero-dependency Python script that reads rule frontmatter, matches globs against the target project, and writes output files. Same input always produces same output.

```bash
# No install needed — run directly with curl
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py | python3 - --clone https://github.com/paulczar/keel

# Sync from a local Keel clone
python3 scripts/keel-sync.py --path /path/to/keel/content/rules --project /path/to/target

# Shallow-clone and sync
python3 scripts/keel-sync.py --clone https://github.com/paulczar/keel --project /path/to/target

# Preview what would change
python3 scripts/keel-sync.py --path content/rules --dry-run
```

Flags: `--path`, `--clone`, `--pull`, `--project`, `--formats`, `--force`, `--dry-run`.

### Syncing via Slash Command

The `/keel-sync` slash command (`commands/keel-sync.md`) delegates to `keel-sync.py` under the hood. The LLM's role is to locate or download the script, run it, and summarize the output.

The `/keel-apply` slash command (`commands/keel-apply.md`) audits the project against Keel best practices (from `scaffolding.md` and other rules) and guides the user through adding missing files such as `.gitignore`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, etc. It never creates files automatically — it presents findings, resolves ambiguity (e.g., which license), and creates only what the user explicitly agrees to.

The sync generates:
- `.agents/rules/keel/*.md` — Full rule files (Hugo metadata stripped)
- `.cursor/rules/keel/*.mdc` — Cursor-compatible rule files
- `AGENTS.md` — Routing table with globs, descriptions, and file references

Rules are placed in `keel/` subdirectories to support the layering model (see Rule Layering above).

A legacy manual prompt is available in `content/sync-prompt.md` for agents without shell access.

### Using Rules Locally (Dogfooding)

This repo symlinks its own rules into `.cursor/rules/keel/` so Cursor picks them up. The symlinks point directly to `content/rules/` sources — content edits are reflected immediately.

```bash
# Create/recreate symlinks (only needed when adding new rules)
make rules
```

To add a rule to the local set, add its name to `CURSOR_RULES` in the Makefile.

### Building the Site

```bash
make preview    # Development server with live reload
make build      # Production build with minification
make clean      # Remove generated files
```

### Git Commits

All commits must include a `Signed-off-by` trailer from the commit author in the commit message body.

## Conventions

- The theme (hugo-book v10) is pinned via git submodule. Do not update without checking Hugo version compatibility.
- Hugo 0.129.0 is the target version. hugo-book v11+ requires Hugo 0.134+.
- `globs` in frontmatter should use single-line flow-sequence format (`["pattern"]`) for consistency.
- The `content/_index.md` serves as both the site landing page and the project manifesto. It uses hugo-book's `columns` shortcode.
- The `content/sync-prompt.md` contains the copy-pasteable prompt for AI-agent-driven rule syncing. This is the primary distribution mechanism.
