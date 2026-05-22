---
title: "qmd"
description: "Local search engine for markdown files. Hybrid BM25/vector search, on-device."
weight: 40
---

# qmd

[qmd](https://github.com/tobi/qmd) is a local search engine for markdown files. It indexes your knowledge wiki and provides hybrid BM25/vector search with optional LLM re-ranking — all on-device. No API calls, no data leaves your machine.

Recommended in [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) as the wiki grows beyond what `index.md` browsing can handle.

## Why it matters for knowledge management

At small scale (tens of pages), the agent reads `index.md` to find relevant pages and drills into them. As the wiki grows (hundreds of pages), this becomes slow — the index file itself gets long and the agent has to scan it on every query.

qmd replaces the index-scan pattern with direct search. The agent queries qmd with natural language, gets ranked results with relevance scores, and reads only the top matches. This scales to thousands of pages without slowing down.

## Installation

### CLI mode

```bash
# Install
go install github.com/tobi/qmd@latest

# Index your knowledge wiki
qmd index ~/.keel/content/knowledge/

# Search
qmd query "how does the build system work"
```

The agent shells out to `qmd query` when it needs to find relevant pages.

### MCP server mode

Add to `opencode.json`:

```json
{
  "qmd": {
    "type": "mcp",
    "command": "qmd",
    "args": ["mcp", "--index", "~/.keel/content/knowledge/"]
  }
}
```

Restart opencode after adding. The MCP server provides a `search` tool the agent calls natively.

## Usage in keel

When querying the knowledge wiki:

1. If the wiki is small (index.md fits in one screen), read index.md directly
2. If the wiki is large, use qmd to search for relevant pages
3. Read the top-ranked pages from qmd results
4. Synthesize the answer

The knowledge-management skill should check wiki size and decide which retrieval method to use.

## Choosing a search tool

| Tool | Searches | Cost | Best for |
|------|----------|------|----------|
| **qmd** | Your local wiki | Free | Wiki retrieval at scale |
| **Brave** | The web | Free tier | Finding new sources |
| **Perplexity** | The web | Paid | Research & verification |

qmd is the only one that's fully local and free. It complements Brave and Perplexity — they find sources from the web; qmd finds pages in your existing wiki.

## See also

- [Brave Search]({{< relref "/mcp/brave-search" >}})
- [Perplexity Search]({{< relref "/mcp/perplexity" >}})
- [Knowledge Management skill]({{< relref "/skills/knowledge-management" >}})
- [Sync MCP skill]({{< relref "/skills/sync-mcp" >}})
