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

```
I'm setting up a keel vault. Keel is a cross-agent content management system for AI coding rules, skills, and knowledge — think of it as a centralized wiki for all the context your AI agents need.

## What you'll do

1. Clone the keel repository from https://github.com/paulczar/keel
2. Ask me where I want the vault to live (default: ~/.keel)
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
├── content/
│   ├── keel/              ← git clone of keel repo (the framework)
│   │   ├── rules/
│   │   ├── skills/
│   │   └── knowledge/
│   └── local/             ← my personal knowledge
│       └── knowledge/
├── .gitignore
└── README.md
```

`content/keel/` is the keel framework — I can update it by pulling from upstream.
`content/local/` is mine — never suggest syncing it anywhere.

## What to ask me

Start with: "I'll clone keel and set up your vault. First, where should it live? (default: ~/.keel)"

Then ask each question one at a time. Don't batch them.
```

After the agent finishes, you'll have a working keel vault. From there:
- Browse your rules and skills by opening the vault in Obsidian
- View the documentation site by running `hugo server` in `content/keel/`
- Sync rules to a project by running `keel-sync.py`

## Next Steps

- **Learn about [rules]({{< relref "/rules" >}})** — how coding standards work
- **Learn about [skills]({{< relref "/skills" >}})** — reusable agent procedures
- **Learn about the [knowledge wiki]({{< relref "/knowledge" >}})** — persistent agent memory
- **Learn about [behavior profiles]({{< relref "/behaviors" >}})** — choose your agent's style
- **Read the [design document](https://github.com/paulczar/keel/blob/main/DESIGN.md)** — full architecture

## Manual Setup

If you prefer to set up manually:

```bash
git clone https://github.com/paulczar/keel ~/.keel/content/keel
mkdir -p ~/.keel/content/local/knowledge
# Then pick a behavior profile and write it to ~/.keel/AGENTS.md
cp ~/.keel/content/keel/content/behaviors/karpathy.md ~/.keel/AGENTS.md
```
