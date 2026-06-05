# Project Keel

[https://tech.paulcz.net/keel/](https://tech.paulcz.net/keel/)

**Rules, skills, and knowledge for AI-assisted software development.**

Keel is a cross-agent content management system for everything your AI agents need — coding standards, reusable procedures, and a persistent knowledge wiki. One vault, multiple tools, agent-first setup.

**[Get started →](content/getting-started.md)** Copy a prompt, paste it to your agent, and have your keel vault set up in minutes.

## How It Works

Keel manages three content types in a single markdown vault:

| Type | Purpose | Lifecycle |
|------|---------|-----------|
| **Rules** | Coding standards agents must follow | Static, versioned via PRs |
| **Skills** | Reusable procedures loaded on-demand | Semi-static, updated per workflow |
| **Knowledge** | Persistent wiki agents write and maintain | Dynamic, constantly evolving |

The vault lives at `~/.keel/` (or wherever you put it). Your project's AGENTS.md tells agents where to find it. Agents read rules and knowledge directly; skills are loaded lazily via native tooling.

## What's in the Vault

```
~/.keel/
├── AGENTS.md              ← behavioral profile (pick your agent's style)
├── content/
│   ├── keel/              ← git clone of this repo (the framework)
│   │   ├── rules/         ← coding standards
│   │   ├── skills/        ← reusable procedures
│   │   ├── knowledge/     ← persistent wiki
│   │   ├── behaviors/     ← selectable agent profiles
│   │   └── mcp/           ← recommended MCP tools
│   └── local/             ← your personal knowledge (never synced)
```

### Behavioral Profiles

Choose how your agent behaves:

- **[Karpathy](https://tech.paulcz.net/keel/behaviors/karpathy/)** — Balanced, cautious. The default.
- **[Strict](https://tech.paulcz.net/keel/behaviors/strict/)** — Maximum guardrails. Every action confirmed.
- **[Vibe](https://tech.paulcz.net/keel/behaviors/vibe/)** — Minimal friction. Fast iteration.

Your chosen profile becomes the project's AGENTS.md.

## Vault Mode (Recommended)

Set vault path in your project's AGENTS.md and agents find everything:

- **Rules** — agents read from `content/keel/content/rules/`
- **Skills** — agents load via `skill()` tool from `content/keel/content/skills/`
- **Knowledge** — agents read and write to `content/keel/content/knowledge/`
- **Behaviors** — selected profile is the project's AGENTS.md
- **MCP** — curated MCP tools installable via the vault-mcp skill

No per-project sync. No script. Just a path in AGENTS.md.

## Project-Local Mode (Optional)

If you don't want a vault, `keel-sync.py` copies relevant rules directly into a project:

```bash
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py | \
  python3 - --clone https://github.com/paulczar/keel
```

The script inspects your project's languages and tooling, selects matching rules, and writes them to `.cursor/rules/`, `.agents/rules/`, or AGENTS.md.

### Cursor Plugin

Keel can also be installed as a Cursor plugin:

```bash
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/install-plugin.sh | bash
```

## Adding Content

```bash
# New rule
hugo new --kind rule content/rules/my-new-rule.md

# New skill
hugo new --kind skill content/skills/my-new-skill.md
```

Edit the generated file and run `make build` to verify.

## Dogfooding

```bash
# Symlink rules + skills into local tooling
make dev-sync
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE](LICENSE).
