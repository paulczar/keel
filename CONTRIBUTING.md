# Contributing to Keel

Thanks for your interest in contributing to Project Keel. This document explains how to participate.

## Reporting Bugs

Open a [GitHub issue](https://github.com/your-org/keel/issues) with:

- Steps to reproduce the problem
- Expected vs actual behavior
- Hugo version (`hugo version`)

## Proposing New Rules

1. Open an issue describing the rule: what language/tool it covers, why it's needed, and a rough outline of the content
2. Discuss scope and approach in the issue before writing the full rule
3. Submit a pull request when the approach is agreed upon

## Submitting Pull Requests

1. Fork the repository and create a branch from `main`
2. Follow the commit conventions: `type(scope): description` (see `base.md` rule for details)
3. Run `make build` to verify the site builds cleanly
4. Keep PRs focused — one rule or concern per PR
5. Include a brief description of what changed and why

### Branch Naming

Use `<type>/<short-description>`:

- `feat/terraform-rule`
- `fix/base-rule-typo`
- `docs/layering-examples`

## Development Setup

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/your-org/keel.git
cd keel

# Preview the site
make preview

# Build for production
make build

# Set up local rule symlinks
make rules
```

### Adding a New Rule

```bash
hugo new --kind rule content/rules/my-rule.md
```

Every rule should include:

- **Tooling** section — formatters, linters, validators for that language/tool
- **Agent Behavior** section — when agents should run validation automatically
- Proper frontmatter: `title`, `description`, `globs`, `alwaysApply`, `tags`, `weight`

See `AGENTS.md` for the full rule format and conventions.

## Code Style

- Markdown files follow the standards in `content/rules/markdown.md`
- YAML follows `content/rules/yaml.md`
- Hugo templates follow `content/rules/hugo.md`

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.
