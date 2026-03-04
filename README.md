# Project Keel

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

### Syncing Rules to a Project

Use `keel-sync.py` to sync rules into any project — no AI agent needed:

```bash
# No install needed — run directly with curl
curl -fsSL https://raw.githubusercontent.com/paulczar/keel/main/scripts/keel-sync.py | python3 - --clone https://github.com/paulczar/keel

# Or from a local Keel clone
python3 scripts/keel-sync.py --path content/rules --project /path/to/target

# Preview what would change
python3 scripts/keel-sync.py --clone https://github.com/paulczar/keel --dry-run
```

The script auto-detects languages, AI tooling formats, writes matching rules, and installs slash commands (keel-sync, keel-apply, etc.) into `.cursor/commands/`, `.claude/commands/`, and `.github/prompts/`.

To use slash commands (e.g. `/keel-sync`, `/keel-apply`) in Claude Code, Cursor, or Copilot, run `keel-sync.py` once — it installs them. No separate install step.

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
