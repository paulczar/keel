---
title: "Base Rules"
description: "Global coding standards that apply to all files and languages"
globs: ["**/*"]
alwaysApply: true
tags: ["global", "general"]
weight: 1
---

# Base Rules

These rules apply globally to all files in the project regardless of language or framework.

## Code Quality

- Write clear, readable code that favors explicitness over cleverness
- Keep functions focused — each function should do one thing well
- Use meaningful variable and function names that describe intent
- Limit function length to ~50 lines; extract helpers when complexity grows
- Avoid deep nesting (max 3 levels); use early returns and guard clauses

## Error Handling

- Handle errors explicitly — never silently swallow exceptions
- Use typed errors where the language supports them
- Include context in error messages (what failed, why, and what to do)
- Log errors at the appropriate level (error vs warn vs info)

## Security

- Never commit secrets, tokens, or credentials to version control
- Validate and sanitize all external input (user input, API responses, environment variables)
- Use parameterized queries for database access — never interpolate user input into queries
- Follow the principle of least privilege for file permissions, API scopes, and service accounts

## Git Practices

- Write atomic commits — each commit should represent one logical change
- Use conventional commit messages: `type(scope): description`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`
- Keep pull requests focused and reviewable (under 400 lines when practical)
- Never force-push to shared branches

## Documentation

- Document *why*, not *what* — code shows what it does, comments explain why
- Keep README files up to date with setup instructions and architecture notes
- Document public APIs with clear parameter descriptions and usage examples
- Add inline comments only for non-obvious logic or important constraints

## Dependencies

- Pin dependency versions explicitly (lockfiles must be committed)
- Audit new dependencies for maintenance status, security, and license compatibility
- Prefer well-maintained, widely-adopted libraries over obscure alternatives
- Remove unused dependencies promptly

## Testing

- Write tests for business logic, edge cases, and bug fixes
- Follow the Arrange-Act-Assert pattern
- Keep tests independent — no shared mutable state between tests
- Name tests descriptively: `should [expected behavior] when [condition]`
