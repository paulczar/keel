---
title: "Brave Search"
description: "Web search via Brave Search API. Results as structured data."
weight: 20
---

# Brave Search

[Brave Search](https://search.brave.com/) provides web search results as structured data — titles, URLs, snippets, and dates. Useful for finding sources during the ingest flow and verifying facts during query.

Free tier: up to 2,000 queries/month with a free API key from [api.search.brave.com](https://api.search.brave.com/).

## Why it matters for knowledge management

During **ingest**, the agent searches for sources on a topic before reading and filing them. During **query**, the agent can verify claims against current web results. During **lint**, the agent can check if knowledge entries reference URLs that are still live.

## Installation

Get a free API key from [Brave Search API](https://api.search.brave.com/), then add to `opencode.json`:

```json
{
  "brave-search": {
    "type": "builtin",
    "builtin": "braveSearch",
    "config": {
      "apiKey": "{env:BRAVE_API_KEY}"
    }
  }
}
```

Set the environment variable:

```bash
export BRAVE_API_KEY=your_key_here
```

Restart opencode after adding the config.

## Usage in keel

When the knowledge-management skill needs to find sources on a topic:

1. Search Brave for the topic
2. Review the top results by title and snippet
3. Fetch the most promising sources via the agent's built-in webfetch
4. Ingest as usual

When verifying a claim during query:

1. Search for the specific claim
2. Cross-reference the knowledge entry against current results
3. Flag any discrepancies

## See also

- [Perplexity Search]({{< relref "/mcp/perplexity" >}}) — AI-powered search with synthesized answers
- [Knowledge Management skill]({{< relref "/skills/knowledge-management" >}})
- [Sync MCP skill]({{< relref "/skills/sync-mcp" >}})
