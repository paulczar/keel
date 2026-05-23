---
title: "Vault Skill Create"
description: "Create built skills from complex workflows, corrections, and repeatable tasks."
weight: 30
---

# Skill Builder

Creates reusable skills from work you've done. Turns complex workflows, corrected approaches, and repeatable tasks into persistent procedures the agent can load on demand.

## Skill Tiers

| Tier | Location | Owner | Updated by |
|------|----------|-------|------------|
| **Downloaded** | `content/keel/content/skills/<name>/SKILL.md` | Keel framework | `git pull` to keel clone; PR improvements upstream |
| **Built (vault)** | `content/local/skills/<name>/SKILL.md` | You (personal library) | Agent creates/edits, you confirm |
| **Built (project)** | `./local/skills/<name>/SKILL.md` | Project team | Agent creates/edits, committed with project |

Downloaded skills come from the keel framework. Built skills are created by the agent from your sessions.

## When to offer skill creation

After any of these, ask the user if they'd like to create a skill:

- **Complex task completed** — 5+ tool calls, multiple steps, non-trivial workflow
- **Errors and dead ends** — you hit failures and found the working path
- **User corrected your approach** — they showed you a better way to do something
- **Repeatable pattern** — you did something that's likely to be done again
- **User gave explicit instructions** — they walked you through a process step by step

If the user has opted into auto-create (configured in AGENTS.md or vault preferences), skip the ask and create the skill directly.

## Skill creation flow

1. Detect that a skill-worthy event occurred (see above)
2. Ask the user: "This looks like a reusable workflow. Want me to create a skill for it?"
3. If yes, ask: "Should this be project-local (`./local/skills/`), vault-wide (`content/local/skills/`), or should we PR it to the keel framework?"
4. Write the skill using the standard SKILL.md format
5. If project-level, add it to the project's AGENTS.md or skill directory reference
6. If vault-level, it's available across all projects that reference the vault

## Format for built skills

Same SKILL.md format as downloaded skills:

```markdown
---
name: my-deploy-workflow
description: Deploy the service with rollback and health checks.
---

# My Deploy Workflow

## When to use
Deploying the microservice to staging or production.

## Prerequisites
- Access to the cluster
- kubectl configured

## Procedure
1. Build and tag the image
2. Update the deployment manifest
3. Apply with `kubectl apply`
4. Run health checks
5. If checks fail, rollback with `kubectl rollout undo`

## Verification
- `kubectl get pods` shows all running
- Health endpoint returns 200
```

## Skill improvement

When a user corrects you while using a built skill:

1. Note the correction
2. Ask: "Should I update the [skill name] skill with this improvement?"
3. If yes, patch the skill file
4. If the user has opted into auto-improve, skip the ask

## See also

- [Knowledge Management]({{< relref "/skills/vault-knowledge" >}}) — when to capture knowledge vs build a skill
- [Sync MCP]({{< relref "/skills/vault-mcp" >}}) — installing tool MCP servers
