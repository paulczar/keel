---
title: "Sync MCP"
description: "Install MCP servers and tools from keel's curated MCP directory."
weight: 20
---

# Sync MCP

Reads an MCP tool definition from `content/mcp/` and installs it. Supports both opencode.json MCP server configs (JSON blocks) and standalone tool installs (shell commands).

## How it works

Each file in `content/mcp/` documents a tool with:

- **Standard install** — a shell command (e.g., `npx ctx7 setup`)
- **Config** — an optional JSON block for opencode.json MCP server definitions

The sync-mcp skill reads the file, identifies the install method, and executes it.

## Usage

To install a specific MCP tool:

1. Browse `content/mcp/` for available tools
2. Tell your agent: "Install MCP tool [name] from keel"
3. The agent reads the file and runs the install

Or request all recommended tools:

1. "Install all recommended MCP tools from keel"
2. The agent iterates through `content/mcp/` and installs each one

## Installing an opencode.json MCP server

Some tools are configured as MCP servers in `opencode.json`. Their markdown file contains a JSON block like this:

````markdown
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@some/mcp-server"]
}
```
````

The skill extracts the JSON and merges it into `opencode.json` under `mcp.<tool-name>`. After writing, suggest restarting opencode for the new server to load.

## Installing standalone tools

Other tools (like Context7) install via a shell command:

```bash
npx ctx7 setup
```

The skill runs the command directly. No opencode.json modification needed.

## Adding a new MCP tool

To add a tool to keel's MCP directory:

1. Create `content/mcp/<tool-name>.md`
2. Add frontmatter: `title`, `description`
3. Document the install method
4. Include a JSON ` ```json ` block for opencode.json MCP servers (if applicable)

## See also

- [MCP Tools directory]({{< relref "/mcp" >}})
- [Knowledge Management skill]({{< relref "/skills/knowledge-management" >}})
