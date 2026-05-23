---
title: "Context7"
description: "Up-to-date library documentation for AI coding agents."
weight: 10
---

# Context7

[Context7](https://context7.com) provides current documentation for thousands of libraries and frameworks directly to your AI coding agent. Instead of relying on potentially stale training data, the agent fetches real-time docs when answering questions about library usage.

## Why it matters for knowledge management

During the **ingest** flow, the agent can cross-reference sources against current docs to catch outdated claims. During **query**, the agent can verify commands, API signatures, and configuration options before writing them to the knowledge wiki. This prevents stale or incorrect library knowledge from accumulating.

## Installation

```bash
npx ctx7 setup
```

This installs Context7 for whichever AI agent you're running (opencode, Claude Code, Cursor, Codex, etc.).

## Usage in keel

When the vault-knowledge skill ingests a source about a library or framework, it should:

1. Use Context7 to fetch current docs for the relevant APIs
2. Compare the source's claims against current docs
3. Note any discrepancies in the knowledge entry
4. Include current docs as a reference link

When answering a query that involves command verification:

1. Use Context7 to confirm the correct syntax and flags
2. Cite the source in the response
3. File the verified command as a knowledge entry if it's likely to be reusable

## Configuration

Context7 works out of the box after `npx ctx7 setup`. No additional configuration needed. It integrates with your agent as a tool it can call when it needs documentation.

## See also

- [Knowledge Management skill]({{< relref "/skills/vault-knowledge" >}})
- [Sync MCP skill]({{< relref "/skills/vault-mcp" >}})
