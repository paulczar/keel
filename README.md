# Project Keel

[https://tech.paulcz.net/keel/](https://tech.paulcz.net/keel/)

**Standardized rules for AI-assisted software development.**

Keel is a Hugo-powered CMS that serves as a centralized source of truth for AI coding rules. Write your coding standards once as Markdown; sync them to any project in any format (AGENTS.md, Cursor MDC, Claude Code, Copilot).

## Prerequisites

- [Hugo](https://gohugo.io/) v0.129.0+ (extended edition)
- Git

## Quick Start

```bash
# Clone with submodules (theme)
git clone --recurse-submodules https://github.com/paulczar/keel.git
cd keel

# Preview locally
make preview

# Build for production
make build
```

## Usage

### Browsing Rules

Run `make preview` and open the local site to browse all rules with search, tagging, and navigation.

### Cursor Plugin (Recommended for Cursor Users)

Keel can be installed as a [Cursor Plugin](https://cursor.com/docs/plugins) directly from its Git repo. Choose the method that fits your setup:

**Individual install** (any Cursor plan):

```bash
# No clone needed — fetch and install in one step
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/install-plugin.sh | bash -s -- --clone https://github.com/paulczar/keel

# Or from a Keel clone
./scripts/install-plugin.sh
```

Restart Cursor after installing. You may need to enable **Settings > Features > "Include third-party Plugins, Skills, and other configs"**.

**Team Marketplace** (Teams / Enterprise plans):

1. Go to **Dashboard > Settings > Plugins**
2. Under **Team Marketplaces**, click **Import**
3. Paste the repo URL: `https://github.com/paulczar/keel`
4. Set as **required** (auto-install for all members) or **optional**

Once installed, rules activate per-file based on `globs` and `alwaysApply`, and commands (`/keel-sync`, `/keel-apply`) are available immediately.

To use `/keel-sync` when syncing to other projects, add to your shell profile:

```bash
export KEEL_PATH=~/.cursor/plugins/keel
```

### Syncing Rules to a Project (Multi-Tool)

Use `keel-sync.py` when you need rules in **Claude Code**, **AGENTS.md**, **GitHub Copilot**, or prefer script-based sync for Cursor:

```bash
# No install needed — run directly with curl
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py | python3 - --clone https://github.com/paulczar/keel

# Or from a local Keel clone
python3 scripts/keel-sync.py --path content/rules --project /path/to/target

# Preview what would change
python3 scripts/keel-sync.py --clone https://github.com/paulczar/keel --dry-run
```

The script auto-detects languages and AI tooling formats, writes matching rules to the appropriate directories, and installs slash commands into `.cursor/commands/`, `.claude/commands/`, and `.github/prompts/`. Run it once per project to install commands.

See the [Sync Prompt](/sync-prompt) page for full details and options.

### Adding a New Rule

```bash
hugo new --kind rule content/rules/my-rule.md
```

Edit the generated file, then run `make build` to verify.

### Dogfooding (Using Rules Locally)

```bash
make rules
```

This creates `.cursor/rules/keel/` symlinks pointing to `content/rules/` so Cursor picks up the rules directly. Edit `CURSOR_RULES` in the Makefile to control which rules are active.

## Rule Layering

Rules support three precedence layers:

1. **Local** (`local/`) — project or team-specific. Highest precedence.
2. **Org** (`org/`) — organizational standards.
3. **Keel** (`keel/`) — global defaults. Lowest precedence.

See the [Rule Layering](/layering) page for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to submit rules, report issues, and set up your development environment.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
