# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Conventional Commits](https://www.conventionalcommits.org/).

## [Unreleased]

### Added

- Rule layering model with three-tier precedence (local > org > keel)
- Tooling and Agent Behavior sections for all language rules
- Code Validation section in base rule with opt-out via `skip-auto-validation`
- Local dogfooding via `.cursor/rules/keel/` symlinks and `make rules`
- Sync prompt as sole distribution mechanism (replaced sync script)
- CLAUDE.md and .cursorrules pointing to AGENTS.md
- Rules: Terraform, Kubernetes, Helm, Hugo, Markdown, MDC, Agent Behavior, Scaffolding
- Hugo archetype for new rules (`hugo new --kind rule`)
- Rule layering documentation page
- Project scaffolding (LICENSE, README, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, SECURITY, .editorconfig)
