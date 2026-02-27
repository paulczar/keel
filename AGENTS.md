# AGENTS.md — Project Keel

This file describes the Keel repository for AI agents working on the CMS itself. This is NOT the generated AGENTS.md that the sync script produces for downstream projects.

## Project Overview

Keel is a Hugo-powered CMS that serves as a centralized source of truth for AI coding rules. It renders Markdown rule files as a searchable documentation website for humans, while the same files serve as machine-actionable context for AI agents.

## Repository Structure

```
.
├── AGENTS.md                  # This file (agent instructions for this repo)
├── hugo.yaml                  # Hugo site configuration
├── content/
│   ├── _index.md              # Landing page / manifesto
│   ├── sync-prompt.md         # Copy-pasteable sync prompt for AI agents
│   └── rules/
│       ├── _index.md          # Rules section index
│       ├── base.md            # Global rules (alwaysApply: true)
│       ├── typescript.md      # TypeScript/React standards
│       ├── helm.md            # Kubernetes/Helm standards
│       ├── yaml.md            # YAML standards
│       ├── python.md          # Python standards
│       └── go.md              # Go standards
├── layouts/
│   └── partials/docs/inject/
│       └── content-before.html  # AI metadata box partial
├── assets/
│   └── _custom.scss           # Metadata box styles
├── scripts/
│   └── sync-rules.sh          # Rule sync + AGENTS.md generator
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

## Common Workflows

### Adding a New Rule

1. Create `content/rules/<name>.md` with the frontmatter schema above
2. Write the rule body in Markdown
3. Run `hugo server` to preview locally
4. Run `hugo --gc --minify` to verify the build succeeds

### Modifying the Metadata Display

- Template: `layouts/partials/docs/inject/content-before.html`
- Styles: `assets/_custom.scss`
- Hugo reads `.Params` from frontmatter — field names are lowercased by Hugo

### Syncing Rules to a Target Repo

**Primary method (interactive):** Use the sync prompt at `content/sync-prompt.md`. The user copies the prompt into their AI coding agent in the target project. The agent inspects the project, selects relevant rules, and generates the appropriate output formats.

**CI/CD fallback (deterministic):** Use the bash script for pipelines:
```bash
./scripts/sync-rules.sh /path/to/target-repo
```

Both methods generate:
- `.agents/rules/*.md` — Full rule files (Hugo metadata stripped)
- `.cursor/rules/*.mdc` — Cursor-compatible rule files
- `AGENTS.md` — Routing table with globs, descriptions, and file references

### Building the Site

```bash
# Development server with live reload
hugo server

# Production build
hugo --gc --minify
```

## Conventions

- The theme (hugo-book v10) is pinned via git submodule. Do not update without checking Hugo version compatibility.
- Hugo 0.129.0 is the target version. hugo-book v11+ requires Hugo 0.134+.
- `globs` in frontmatter should use single-line flow-sequence format (`["pattern"]`) for consistency.
- The `content/_index.md` serves as both the site landing page and the project manifesto. It uses hugo-book's `columns` shortcode.
- The `content/sync-prompt.md` contains the copy-pasteable prompt for AI-agent-driven rule syncing. This is the primary distribution mechanism.
