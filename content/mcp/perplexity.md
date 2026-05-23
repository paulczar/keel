---
title: "Perplexity Search"
description: "AI-powered web search with synthesized answers and citations."
weight: 30
---

# Perplexity Search

[Perplexity](https://www.perplexity.ai/) provides AI-powered web search that returns synthesized answers with numbered citations — not just raw links. Supports filtering by recency (hour/day/week/month/year) and domain restrictions.

## Why it matters for knowledge management

Perplexity is better suited for knowledge work than raw search engines because it synthesizes across multiple sources in one response. During **ingest**, the agent can get a research briefing on a topic before diving into sources. During **query**, it can answer "what's the current state of X?" with citations from multiple sources.

## Installation

Get an API key from [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api), then add to `opencode.json`:

```json
{
  "perplexity": {
    "type": "mcp",
    "command": "npx",
    "args": [
      "-y",
      "@anthropic/mcp-perplexity",
      "--api-key",
      "{env:PERPLEXITY_API_KEY}"
    ]
  }
}
```

Set the environment variable:

```bash
export PERPLEXITY_API_KEY=your_key_here
```

Restart opencode after adding the config.

## Choosing between Brave and Perplexity

| Criteria | Brave | Perplexity |
|----------|-------|------------|
| **Output** | Raw links + snippets | Synthesized answers + citations |
| **Cost** | Free tier (2K/mo) | Paid API |
| **Best for** | Source discovery | Research & verification |
| **Speed** | Fast | Slower (AI synthesis) |

Use Brave when you need to find specific sources. Use Perplexity when you need to understand a topic or verify a claim across multiple sources.

Both can coexist — use them for different phases of the knowledge workflow.

## Usage in keel

When the vault-knowledge skill needs research on a topic:

1. Ask Perplexity for a synthesized overview with citations
2. Review the answer and citations
3. Fetch cited sources via webfetch for deeper reading
4. Ingest each source into the knowledge wiki
5. File the synthesis as a concept page

When verifying a claim during lint:

1. Ask Perplexity "Is X still the recommended approach for Y?"
2. Compare the answer against the knowledge entry
3. Flag any contradictions

## See also

- [Brave Search]({{< relref "/mcp/brave-search" >}}) — raw web search for source discovery
- [Knowledge Management skill]({{< relref "/skills/vault-knowledge" >}})
- [Sync MCP skill]({{< relref "/skills/vault-mcp" >}})
