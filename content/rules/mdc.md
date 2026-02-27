---
title: "MDC Rule Format"
description: "Standards for Cursor's .mdc rule files"
globs: ["**/*.mdc", ".cursor/rules/*.mdc"]
alwaysApply: false
tags: ["mdc", "cursor", "rules"]
weight: 50
---

# MDC Rule Format

Standards for writing Cursor rule files in the `.mdc` format.

## Overview

MDC files are Cursor's native rule format for providing AI-assistant context. Each `.mdc` file defines a single rule with frontmatter metadata and Markdown content. Cursor loads matching rules based on glob patterns and injects them as system context during conversations.

## Frontmatter

MDC frontmatter uses YAML between `---` delimiters. Include only the fields Cursor expects:

- **`description`** — short summary of what the rule covers (required)
- **`globs`** — array of file patterns that trigger this rule (required unless `alwaysApply` is true)
- **`alwaysApply`** — set to `true` only for rules that should apply to every conversation

```yaml
---
description: "TypeScript and React coding conventions"
globs: ["**/*.ts", "**/*.tsx"]
alwaysApply: false
---
```

- Do not include Hugo-specific fields (`title`, `tags`, `weight`) in MDC output — those belong in Hugo content frontmatter only
- Keep `description` under 120 characters — it appears in Cursor's rule list

## Content Guidelines

- Write in imperative mood — "Use strict mode" not "You should use strict mode"
- Lead with the most important rules — Cursor may truncate long rules
- Use bullet points for individual rules; use headings to group related topics
- Include short code examples to clarify non-obvious conventions

```markdown
## Naming

- Use `camelCase` for variables and functions
- Use `PascalCase` for types and components
```

- Avoid lengthy explanations — rules are reference material, not tutorials
- Keep total rule content under 500 lines; split large topics into multiple rules

## File Organization

- Store project rules in `.cursor/rules/` at the repository root
- Use one rule per file — each file covers a single language, tool, or concern
- Name files descriptively with kebab-case: `typescript.mdc`, `api-conventions.mdc`
- Avoid generic names like `rules.mdc` or `general.mdc`

## Glob Patterns

- Use `**/*.ext` to match files by extension anywhere in the project
- Use specific paths for scoped rules: `src/components/**/*.tsx`
- Combine multiple patterns in the array when a rule spans related file types

```yaml
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
```

- Test globs against actual project structure — overly broad globs waste context tokens
- Omit `globs` and set `alwaysApply: true` for universal rules (coding standards, commit conventions)

## Relationship to AGENTS.md

MDC is one output format in a multi-format rule system. The same rule content can target:

- **MDC** (`.mdc`) — Cursor's native format
- **AGENTS.md** — Markdown-based format for other AI tools
- **Hugo content** — documentation site with additional metadata (`title`, `tags`, `weight`)

When writing rules, focus on the content. Format-specific fields and structure are handled during sync or export. Keep the source of truth in Hugo content files and generate MDC and AGENTS.md outputs from them.
