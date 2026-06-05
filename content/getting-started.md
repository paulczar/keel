---
title: "Getting Started"
weight: 0
---

# Getting Started with Keel

Copy the prompt below and paste it into your AI coding agent (OpenCode, Claude Code, Cursor, or any tool that accepts natural language instructions). The agent will walk you through setting up your keel vault.

Alternatively, browse the steps yourself and decide what to use.

---

## Bootstrap Prompt

Copy everything between the lines below and paste it to your agent:

````
I'm setting up a keel vault. Keel is a cross-agent content management system for AI coding rules, skills, and knowledge — think of it as a centralized wiki for all the context your AI agents need.

## What you'll do

1. Ask me where I want the vault to live (default: ~/.keel)
2. Clone the keel repository into `<vault>/keel/`
3. Ask me which AI tools I use (opencode, Claude Code, Cursor, Copilot, etc.)
4. Show me the available behavior profiles and ask which one I want as my default
5. Ask if I want to set up any git remotes (e.g., my own fork for personalizations)
6. Set up the vault directory structure
7. Install the initial configs

## Vault structure

The vault will look like this:

```
~/.keel/
├── AGENTS.md              ← behavioral guidelines (picked from profiles)
├── keel/                  ← git clone of keel repo (the framework)
├── local/                 ← my personal knowledge
│   └── knowledge/
├── .gitignore
└── README.md
```

`keel/` is the keel framework — I can update it by pulling from upstream.
`local/` is mine — never suggest syncing it anywhere.

## What to ask me

Start with: "I'll clone keel and set up your vault. First, where should it live? (default: ~/.keel)"

Then ask each question one at a time. Don't batch them.
````

After the agent finishes, you'll have a working keel vault. From there:
- Open the vault in Obsidian to browse rules, skills, and knowledge
- View the documentation site by running `hugo server` in `keel/`
- Install recommended MCP tools via the vault-mcp skill
- Set your vault path in any project's AGENTS.md to use it in vault mode
- Have an existing project? Use the **vault-project-migrate** skill to convert it

## Next Steps

- **Learn about [rules]({{< relref "/rules" >}})** — how coding standards work
- **Learn about [skills]({{< relref "/skills" >}})** — reusable agent procedures
- **Learn about the [knowledge wiki]({{< relref "/knowledge" >}})** — persistent agent memory
- **Learn about [behavior profiles]({{< relref "/behaviors" >}})** — choose your agent's style
- **Learn about [MCP tools]({{< relref "/mcp" >}})** — recommended MCP servers for knowledge management
- **Migrate an existing project** with the [vault-project-migrate skill]({{< relref "/skills/vault-project-migrate" >}})
- **Read the [design document](https://github.com/paulczar/keel/blob/main/DESIGN.md)** — full architecture

## Manual Setup

If you prefer to set up manually:

```bash
git clone https://github.com/paulczar/keel ~/.keel/keel
mkdir -p ~/.keel/local/knowledge
# Then pick a behavior profile and write it to ~/.keel/AGENTS.md
cp ~/.keel/keel/content/behaviors/karpathy.md ~/.keel/AGENTS.md
```
