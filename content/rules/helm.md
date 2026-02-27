---
title: "Helm Standards"
description: "Helm chart development conventions"
globs: ["**/Chart.yaml", "**/values.yaml", "**/templates/**/*.yaml", "**/templates/**/*.tpl", "**/*.helm.yaml"]
alwaysApply: false
tags: ["helm", "infrastructure"]
weight: 30
---

# Helm Standards

Standards for Helm chart development.

## Chart Structure

- Follow the standard Helm chart layout:
  ```
  chart-name/
    Chart.yaml
    values.yaml
    templates/
      _helpers.tpl
      deployment.yaml
      service.yaml
      ingress.yaml
      NOTES.txt
    charts/       # subcharts
    tests/
  ```
- Keep `Chart.yaml` metadata accurate — `appVersion` must match the deployed application version
- Use semantic versioning for chart versions (`version` in `Chart.yaml`)

## Values

- Provide sensible defaults in `values.yaml` for all configurable parameters
- Document every value with inline comments explaining purpose and valid options
- Use flat keys where possible — avoid deeply nested structures
- Never hardcode values in templates that should be configurable
- Use `null` for optional values that should be omitted by default

```yaml
# Number of pod replicas
replicaCount: 1

image:
  # Container image repository
  repository: ghcr.io/org/app
  # Image pull policy
  pullPolicy: IfNotPresent
  # Overrides the image tag (defaults to chart appVersion)
  tag: ""
```

## Templates

- Use `_helpers.tpl` for reusable template definitions (labels, names, selectors)
- Quote all string values in YAML templates: `{{ .Values.image.repository | quote }}`
- Use `{{- ... -}}` trim markers to control whitespace
- Gate optional resources with `{{- if .Values.feature.enabled }}`
- Use `{{ include "chart.labels" . }}` over `{{ template }}` for pipeline compatibility

## Dependencies

- Declare subchart dependencies in `Chart.yaml` under `dependencies`
- Pin dependency versions to a specific range — avoid `*`
- Run `helm dependency update` after changing dependencies
- Override subchart values under the subchart's key in `values.yaml`

## Testing

- Include Helm test templates in `templates/tests/`
- Use `helm lint` in CI to catch template errors
- Validate rendered manifests with `helm template` + `kubeconform` or `kubeval`
- Test upgrades: ensure `helm upgrade --install` works cleanly from the previous version

## .gitignore

Ensure these Helm-specific patterns are in the project's `.gitignore`:

```gitignore
charts/*.tgz
```

Also ensure each chart has a `.helmignore` file to exclude unnecessary files from the packaged chart (e.g., `.git/`, `*.md`, `.gitignore`).

## Agent Behavior

Behavioral guidance for AI agents managing Helm releases, whether via `helm` CLI, MCP tools, or client libraries.

- Review existing releases in the target namespace before installing or upgrading (e.g., `helm list --namespace <ns>`)
- Preview changes before applying — use diff or dry-run capabilities (e.g., `helm diff upgrade`, `helm upgrade --dry-run`) to show what will change
- Always scope operations to an explicit namespace (e.g., `--namespace <ns>`)
- Never uninstall a release without showing its current status (e.g., `helm status <release>`) and confirming with the user
- Review release status and history to understand current state before making changes (e.g., `helm status`, `helm history`)
- Prefer upgrade-or-install (idempotent) operations over separate install/upgrade for resilience (e.g., `helm upgrade --install`)
