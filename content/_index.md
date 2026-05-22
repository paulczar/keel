---
title: "Project Keel"
type: docs
---

# Project Keel

**Rules, skills, and knowledge for AI-assisted software development.**

Keel is a cross-agent content management system for everything your AI agents need — coding standards, reusable procedures, and a persistent knowledge wiki. One vault, multiple tools, agent-first setup.

**[Get started →]({{< relref "/getting-started" >}})** Copy a prompt, paste it to your agent, and have your keel vault set up in minutes.

---

## The Problem

Every AI coding tool invented its own configuration format:

| Tool | Config Location | Format |
|------|----------------|--------|
| Cursor | `.cursor/rules/*.mdc` | MDC |
| GitHub Copilot | `.github/copilot-instructions.md` | Markdown |
| Claude Code | `CLAUDE.md` | Markdown |
| Windsurf | `global_rules.md` | Markdown |
| OpenAI Codex | `AGENTS.md` | Markdown + YAML |
| Google Jules | `AGENTS.md` | Markdown + YAML |

Each tool has its own format, directory structure, and activation model. Teams using multiple assistants maintain duplicate context across formats, with no single source of truth and no governance over what agents are told to do.

## Our Approach

Keel is a markdown vault that serves as the single source of truth for all AI agent context. It manages three content types:

- **Rules** — coding standards agents must follow
- **Skills** — reusable procedures agents load on-demand
- **Knowledge** — a persistent wiki agents write and maintain

The vault is an Obsidian-compatible directory of markdown files. Agents read from it directly — no sync needed. A [getting-started prompt]({{< relref "/getting-started" >}}) bootstraps your vault in minutes.

## Core Principles

{{< columns >}}

### Declarative & Human-Readable

Everything is natural language Markdown. No proprietary DSL. No JSON schemas. Human-readable, machine-actionable.

<--->

### Version-Controlled

All content lives in Git. Changes are reviewed via pull requests. Full audit history. Every edit is traceable.

{{< /columns >}}

{{< columns >}}

### Three Content Dimensions

Rules *constrain* what agents do. Skills *instruct* how to do specific things. Knowledge *informs* agents with learned context. Each has its own lifecycle and consumption pattern.

<--->

### Agent-First

Agents bootstrap the vault, maintain the knowledge wiki, and load skills on-demand. The human's job is to curate, direct, and ask good questions.

{{< /columns >}}

{{< columns >}}

### Tool-Agnostic

The same vault serves opencode, Claude Code, Cursor, Copilot, and any other agent. Each tool's native access pattern (skills, rules, prompts) reads from the same source.

<--->

### Governable

Three content types, three review workflows. Rules go through PRs. Skills go through PRs. Knowledge evolves with agent sessions and human curation.

{{< /columns >}}

## How It Works

### Vault Mode (Recommended)

1. **Bootstrap** — Paste the getting-started prompt to your agent. It clones keel, asks your preferences, and sets up `~/.keel/`.
2. **Configure** — Pick a behavior profile (Karpathy, Strict, or Vibe). It becomes your project's AGENTS.md.
3. **Use** — Agents read rules and knowledge from the vault. Skills load on-demand. Knowledge compounds over time.

No per-project sync. No scripts. Just a path in AGENTS.md.

### Project-Local Mode (Optional)

For users who don't want a vault, `keel-sync.py` copies relevant rules directly into a project:

```bash
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py | python3 - --clone https://github.com/paulczar/keel
```

The script inspects your project, selects matching rules, and writes them to `.cursor/rules/`, `.agents/rules/`, or AGENTS.md.

### Cursor Plugin

Keel can also be installed as a Cursor plugin for automatic rule matching:

```bash
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/install-plugin.sh | bash
```

## Browse

- [Rules]({{< relref "/rules" >}}) — coding standards
- [Skills]({{< relref "/skills" >}}) — reusable procedures
- [Knowledge]({{< relref "/knowledge" >}}) — persistent wiki
- [Behaviors]({{< relref "/behaviors" >}}) — agent profiles

## References

- [AGENTS.md Open Standard](https://agents.md/)
- [AGENTS.md GitHub Repository](https://github.com/anthropics/agents-md)
- [aicodingrules.org](https://aicodingrules.org)
