---
title: "Playwright"
description: "Headless browser automation. Lets the agent click, navigate, and read multi-page docs."
weight: 50
---

# Playwright

[Playwright MCP](https://github.com/microsoft/playwright-mcp) gives the agent a headless browser. Instead of a single `webfetch` of a URL, the agent can navigate multi-page documentation, click through tutorials, fill forms, and take screenshots.

## Why it matters for knowledge management

Many documentation sources are multi-page — API reference sites, step-through tutorials, docs with expandable sections. A single `webfetch` only gets one page. Playwright lets the agent browse the full site during ingest, clicking through to capture all relevant pages.

During **query**, the agent can verify instructions that involve web-based UIs, CLI dashboards, or interactive documentation.

## Installation

Add to `opencode.json`:

```json
{
  "playwright": {
    "type": "mcp",
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-playwright"]
  }
}
```

No API key needed. Restart opencode after adding.

## Usage in keel

When ingesting a source that links to multi-page documentation:

1. Use Playwright to open the starting page
2. Navigate through the documentation (click links, expand sections, follow "next page" buttons)
3. Capture the content from each page
4. Use **Context7** or **Perplexity** to cross-reference any claims
5. Write a comprehensive summary page that covers the full docs

When the agent encounters a CLI or web UI during a task:

1. Use Playwright to navigate the interface
2. Read the current state
3. Report findings before taking action

## See also

- [Context7]({{< relref "/mcp/context7" >}}) — doc verification
- [Knowledge Management skill]({{< relref "/skills/knowledge-management" >}})
- [Sync MCP skill]({{< relref "/skills/sync-mcp" >}})
