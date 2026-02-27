---
title: "Rule Layering"
weight: 45
bookToc: true
---

# Rule Layering

Keel supports three layers of rules that let organizations define global defaults while allowing teams and projects to customize behavior. Agents resolve conflicts between layers using precedence instructions embedded in the base rule.

## The Three Layers

| Layer | Directory | Owner | Purpose |
|-------|-----------|-------|---------|
| **Keel** | `keel/` | Platform / Keel maintainers | Global defaults — coding standards, security baselines, common patterns |
| **Org** | `org/` | Organization / engineering leadership | Organizational standards — company-specific conventions, compliance requirements |
| **Local** | `local/` | Team / individual developers | Project-specific overrides — team conventions, repo-specific patterns |

## Directory Convention

Rules are organized into subdirectories under your rules directory:

```
.cursor/rules/             # (or .agents/rules/)
  keel/                    # Global defaults (synced from Keel)
    base.mdc               # Always loaded — contains precedence instructions
    kubernetes.mdc
    helm.mdc
    typescript.mdc
  org/                     # Organizational standards
    kubernetes.mdc          # Overrides keel/kubernetes.mdc
    java.mdc               # Additive — no keel equivalent
  local/                   # Team/individual standards
    api-conventions.mdc    # Additive
    kubernetes.mdc          # Overrides both org/ and keel/
```

The subdirectory name signals the layer. The agent reads the precedence instructions from `keel/base.mdc` (which is `alwaysApply: true`) and uses them to resolve conflicts.

## How Precedence Works

AI coding tools like Cursor have no built-in precedence mechanism. When multiple rules match via globs, they're all concatenated into the agent's system prompt. The agent sees every matching rule simultaneously.

Keel solves this through prompting: the `base.mdc` rule (which always loads) contains a **Rule Precedence** section that teaches the agent how to handle conflicts:

1. **Local** (`local/`) — highest precedence
2. **Org** (`org/`) — middle precedence
3. **Keel** (`keel/`) — lowest precedence

When the agent encounters conflicting guidance — say, `keel/kubernetes.mdc` says "use Deployments" but `org/kubernetes.mdc` says "use StatefulSets for all services" — it follows the higher-precedence layer (org, in this case).

## Override vs. Additive Rules

### Overriding

When a higher-layer rule covers the **same topic** as a lower-layer rule, the higher layer fully replaces it. The agent does not attempt to merge conflicting guidance.

**Example:** Both `keel/kubernetes.mdc` and `org/kubernetes.mdc` exist. The org version takes precedence — the agent follows `org/kubernetes.mdc` and ignores `keel/kubernetes.mdc`.

### Additive

When a rule exists at one layer but has no counterpart at another, it simply adds to the agent's instructions. There's no conflict to resolve.

**Example:** `org/java.mdc` exists but there's no `keel/java.mdc` or `local/java.mdc`. The org Java rules apply as-is alongside all other rules.

## Common Patterns

### Copy and Extend

To partially override a lower-layer rule, copy it to a higher layer and modify the parts you want to change. The entire file at the higher layer replaces the lower one.

```
# Start with the keel default
cp .cursor/rules/keel/kubernetes.mdc .cursor/rules/org/kubernetes.mdc

# Edit org/kubernetes.mdc to change what you need
# The rest of the keel defaults in that file are preserved in your copy
```

### Org-Only Rules

Organizations can add rules that have no keel equivalent. These are purely additive and apply alongside keel defaults.

```
.cursor/rules/
  keel/
    base.mdc
    typescript.mdc
  org/
    compliance.mdc          # No keel equivalent — additive
    internal-apis.mdc       # No keel equivalent — additive
```

### Local Customization

Individual projects or teams can override both keel and org rules for their specific needs.

```
.cursor/rules/
  keel/
    base.mdc
    typescript.mdc
  org/
    typescript.mdc          # Org overrides keel typescript standards
  local/
    typescript.mdc          # This project overrides org typescript standards
```

## Frontmatter and Layers

When a higher-layer rule overrides a lower one, the higher layer's frontmatter controls activation. This means the org or local version can change the glob patterns, `alwaysApply` setting, or description.

```yaml
# keel/kubernetes.mdc — applies to all YAML files
---
globs: ["**/*.yaml", "**/*.yml"]
alwaysApply: false
---

# org/kubernetes.mdc — narrows scope to k8s directory only
---
globs: ["k8s/**/*.yaml"]
alwaysApply: false
---
```

## Sync Considerations

When syncing rules from Keel to a project, the sync process writes to the `keel/` subdirectory. Org and local rules are managed independently and are not overwritten by sync. This separation ensures that syncing updated keel defaults never clobbers organizational or local customizations.
