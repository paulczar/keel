# Project Keel

**Standardized rules for AI-assisted software development.**

Keel is a Hugo-powered CMS that serves as a centralized source of truth for AI coding rules. Write your coding standards once as Markdown; sync them to any project in any format (AGENTS.md, Cursor MDC, Claude Code, Copilot).

## Prerequisites

- [Hugo](https://gohugo.io/) v0.129.0+ (extended edition)
- Git

## Quick Start

```bash
# Clone with submodules (theme)
git clone --recurse-submodules https://github.com/your-org/keel.git
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

1. Open your AI coding agent in the **target project**
2. Copy the sync prompt from the [Sync Prompt](/sync-prompt) page
3. Replace `<KEEL_REPO_PATH>` with the path to your Keel clone
4. Paste it into your agent — it inspects the project, selects relevant rules, and generates the right output formats

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
