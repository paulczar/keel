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
3. **Sync** rules to any project using the [Sync Prompt]({{< relref "/sync-prompt" >}})
   - Open your AI coding agent in the target project
   - Paste the sync prompt — it tells the agent to inspect your project, select relevant rules, and generate the right output formats
   - The agent adapts: it only syncs rules that match your stack and writes to the formats your project actually uses
4. **Commit & deploy** — the target repo now has AI-agent-ready rules in all formats

> **Why a prompt instead of a script?** Your AI agent can inspect the target project, skip irrelevant rules, detect which output formats are needed, and handle conflicts intelligently. A bash script can't.

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
