---
title: "Agent Behaviors"
weight: 4
bookCollapseSection: true
---

# Agent Behaviors

Selectable behavioral profiles for AI coding agents.

When bootstrapping a project, keel can install one of these profiles as the project's behavioral guidelines (AGENTS.md). Each profile represents a different tradeoff between safety and speed.

Browse the profiles below and choose the one that fits your project.

### Available Profiles

- **[Karpathy](karpathy)** — Balanced, cautious. Inspired by Andrej Karpathy's well-known CLAUDE.md philosophy. Biases toward simple, surgical, well-thought-out code. Good default for most projects.
- **[Strict](strict)** — Maximum guardrails. Every destructive action requires confirmation. Requires plans before implementation. Best for production systems, regulated environments.
- **[Vibe](vibe)** — Minimal guardrails. Trusts the agent to use good judgment. Fewer prompts for confirmation. Best for prototypes, personal projects, fast iteration.

### Custom Profiles

You can also write your own behavioral profile by creating a new file in this directory and re-running the bootstrap. See an existing profile for the expected format.
