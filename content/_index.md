---
title: "Project Keel"
type: docs
---

# Project Keel

**Standardized Rules for AI-Assisted Software Development**

Keel is an opinionated [AGENTS.md](https://agents.md/) implementation — a governance CMS that produces AGENTS.md-compatible output following the Linux Foundation's open standard. Write your coding standards once; sync them everywhere.

---

## The Problem

Every AI coding tool invented its own configuration format:

| Tool | Config Location | Format |
|------|----------------|--------|
| Cursor | `.cursor/rules/*.mdc` | MDC (Markdown Components) |
| GitHub Copilot | `.github/copilot-instructions.md` | Markdown |
| Claude Code | `CLAUDE.md` | Markdown |
| Windsurf | `global_rules.md` | Markdown |
| OpenAI Codex | `AGENTS.md` | Markdown + YAML |
| Google Jules | `AGENTS.md` | Markdown + YAML |

Each tool has its own format, directory structure, and activation model. Teams using multiple AI assistants maintain duplicate rules across formats, with no single source of truth and no governance over what agents are told to do.

## Our Approach

Keel implements the [AGENTS.md open standard](https://agents.md/) as a Hugo-powered CMS. Rules are authored as Markdown files with YAML frontmatter — the same format used by AGENTS.md (adopted by 60k+ repos, supported by OpenAI Codex, GitHub Copilot, Google Jules, and Cursor).

This site renders those rules as a **searchable documentation website for humans**, while the same files serve as **machine-actionable context for AI agents**. A [sync prompt]({{< relref "/sync-prompt" >}}) distributes rules to any project in all supported formats.

## Core Principles

{{< columns >}}

### Declarative & Human-Readable

Rules are natural language Markdown, readable by both humans and agents. No proprietary DSL. No JSON schemas. Just prose that describes how code should be written.

<--->

### Version-Controlled

Rules are code. They live in Git, are reviewed via pull requests, and have full audit history. Every change is traceable.

{{< /columns >}}

{{< columns >}}

### Modular & Composable

Each rule is a standalone file with clear scope defined by glob patterns. Rules can be combined, overridden, and selectively applied.

<--->

### Hierarchical

Base rules apply globally (`alwaysApply: true`). Language-specific and framework-specific rules activate only when matching files are in context. Rules support a [three-layer model]({{< relref "/layering" >}}) — global defaults (`keel/`), organizational standards (`org/`), and local overrides (`local/`) — with higher layers taking precedence on conflicting topics.

{{< /columns >}}

{{< columns >}}

### Tool-Agnostic

One source of truth, multiple outputs. Your AI agent reads the rules and generates AGENTS.md, `.cursor/rules/`, and `.agents/rules/` — adapting to each project's actual stack.

<--->

### Governable

A centralized CMS with sync tooling enforces organizational standards. Teams share a common rule set while retaining the ability to extend it per-project.

{{< /columns >}}

## How It Works

1. **Author rules** in `content/rules/` using Markdown with YAML frontmatter (title, description, globs, alwaysApply, tags)
2. **Preview** the documentation site locally with `hugo server`
3. **Distribute** rules to any project — choose the path that fits:

### Cursor Plugin

Keel can be installed as a [Cursor Plugin](https://cursor.com/docs/plugins) directly from this Git repo.

**Individual install** (any Cursor plan):

```bash
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/install-plugin.sh | bash -s -- --clone https://github.com/paulczar/keel
```

Restart Cursor after installing. You may need to enable **Settings > Features > "Include third-party Plugins, Skills, and other configs"**.

**Team Marketplace** (Teams / Enterprise plans):

1. Go to **Dashboard > Settings > Plugins**
2. Under **Team Marketplaces**, click **Import**
3. Paste the repo URL: `https://github.com/paulczar/keel`
4. Set as **required** (auto-install for all members) or **optional**

Once installed, rules activate per-file based on `globs` and `alwaysApply`, and commands (`/keel-sync`, `/keel-apply`) are available immediately.

### Multi-Tool Sync (`keel-sync.py`)

Use the sync script when you need rules in **Claude Code**, **AGENTS.md**, **GitHub Copilot**, or prefer script-based sync:

```bash
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py | python3 - --clone https://github.com/paulczar/keel
```

The script inspects your project, selects only relevant rules based on your stack, detects which output formats are needed, and writes rules to the appropriate directories.

### Rule Format

```yaml
---
title: "TypeScript Standards"
description: "TypeScript and React coding conventions"
globs: ["**/*.ts", "**/*.tsx"]
alwaysApply: false
tags: ["typescript", "react"]
weight: 20
---

Your rule content here in Markdown...
```

The frontmatter fields map directly to AGENTS.md concepts:
- **`globs`** — File patterns that activate this rule (AGENTS.md `<rule>` scope)
- **`alwaysApply`** — Whether the rule applies to all files (AGENTS.md global context)
- **`tags`** — Categories for filtering and organization

## References

- [AGENTS.md Open Standard](https://agents.md/) — The Linux Foundation-backed standard for AI agent instructions
- [AGENTS.md GitHub Repository](https://github.com/anthropics/agents-md) — Specification and community
- [aicodingrules.org](https://aicodingrules.org) — Community-curated AI coding rules and best practices
