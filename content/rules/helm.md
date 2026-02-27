---
title: "Helm & Kubernetes Standards"
description: "Kubernetes manifest and Helm chart conventions"
globs: ["**/Chart.yaml", "**/values.yaml", "**/templates/**/*.yaml", "**/templates/**/*.tpl", "**/*.helm.yaml"]
alwaysApply: false
tags: ["kubernetes", "helm", "infrastructure"]
weight: 30
---

# Helm & Kubernetes Standards

Standards for Kubernetes manifests and Helm chart development.

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
- Always include standard labels: `app.kubernetes.io/name`, `app.kubernetes.io/instance`, `app.kubernetes.io/version`, `app.kubernetes.io/managed-by`
- Quote all string values in YAML templates: `{{ .Values.image.repository | quote }}`
- Use `{{- ... -}}` trim markers to control whitespace
- Gate optional resources with `{{- if .Values.feature.enabled }}`

## Resource Management

- Always define resource requests and limits for containers
- Set `requests` to typical usage; set `limits` to peak expected usage
- Use `LimitRange` and `ResourceQuota` in shared namespaces
- Configure health checks (`livenessProbe`, `readinessProbe`, `startupProbe`) for all containers

## Security

- Never run containers as root — set `runAsNonRoot: true` in `securityContext`
- Drop all capabilities and add back only what's needed
- Set `readOnlyRootFilesystem: true` where possible
- Use `NetworkPolicy` to restrict pod-to-pod communication
- Store secrets in external secret managers (Vault, AWS Secrets Manager) — never in `values.yaml`

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
  readOnlyRootFilesystem: true
```

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
