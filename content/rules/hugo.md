---
title: "Hugo Standards"
description: "Hugo static site development conventions"
globs: ["hugo.yaml", "hugo.toml", "config.yaml", "config.toml", "layouts/**/*.html", "archetypes/**/*.md", "content/**/*.md", "static/**/*", "assets/**/*"]
alwaysApply: false
tags: ["hugo", "static-site"]
weight: 55
---

# Hugo Standards

Standards for Hugo static site development.

## Tooling

- Build with `hugo --gc --minify` to verify the site compiles cleanly
- Use `hugo server` for local development with live reload
- Lint content Markdown with `markdownlint`
- Validate HTML output with `htmltest` if available

## Configuration

- Use `hugo.yaml` as the config format — not TOML or JSON
- Use `camelCase` for custom params: `bookSection`, not `book_section` or `BookSection`
- Pin the Hugo version in CI and document it in the README
- Keep environment-specific overrides in `config/` directory trees when needed

```yaml
baseURL: https://example.org/
languageCode: en-us
title: My Site
theme: hugo-book
```

## Content Organization

- Place content under `content/` with one directory per section
- Use `_index.md` for section landing pages — it controls section metadata and listing behavior
- Use YAML frontmatter in all content files
- Define a consistent frontmatter schema per content type and document it

```yaml
---
title: "Page Title"
description: "Brief page summary"
weight: 10
tags: ["topic"]
---
```

- Use `weight` to control page ordering within a section — lower values appear first
- Prefer descriptive filenames in kebab-case: `getting-started.md`, not `page1.md`

## Layouts and Partials

- Override theme templates by mirroring the theme's directory structure under `layouts/`
- Name custom partials descriptively: `header-nav.html`, not `partial1.html`
- Use `baseof.html` for the page skeleton — keep it minimal
- Inject customizations through theme-provided blocks (`define "main"`, `define "footer"`) rather than copying entire templates
- Pass context explicitly to partials with `{{ partial "name.html" . }}`

## Shortcodes

- Use shortcodes for reusable content patterns that Markdown cannot express
- Name shortcodes in kebab-case: `code-tabs`, `callout`
- Store shortcodes in `layouts/shortcodes/`
- Prefer paired shortcodes (`{{</* shortcode */>}}content{{</* /shortcode */>}}`) when wrapping content
- Document shortcode parameters in comments at the top of the shortcode file

## Taxonomies

- Define taxonomies explicitly in `hugo.yaml`
- Use consistent, lowercase tag values across content
- Avoid creating taxonomies that will have fewer than 3 terms — use frontmatter fields instead

```yaml
taxonomies:
  tag: tags
```

## Assets and Styles

- Place custom styles in `assets/` and use Hugo Pipes for processing
- Override theme styles through the theme's designated extension points (e.g., `_custom.scss`)
- Avoid modifying theme files directly — changes will be lost on theme updates
- Keep custom CSS minimal; rely on the theme's design system

## Archetypes

- Create archetypes for each content type: `archetypes/rule.md`, `archetypes/post.md`
- Use YAML frontmatter in archetypes — match the format used in content files
- Include Hugo template functions for dynamic defaults: `{{ .File.ContentBaseName }}`
- Invoke with `hugo new --kind <archetype> <path>`

## Build and Deploy

- Use `hugo server` for local development with live reload
- Build for production with `hugo --gc --minify`
- Set `baseURL` correctly for the deployment target
- Enable `enableGitInfo: true` to populate `.GitInfo` variables (last modified dates)
- Add Hugo build output to `.gitignore`:

```gitignore
public/
resources/_gen/
.hugo_build.lock
```

## Agent Behavior

- After modifying content or layouts, run `hugo --gc --minify` to confirm the site builds without errors
- After adding new pages, verify they appear in the site navigation (check `weight` and section placement)
- When editing shortcodes or templates, test with `hugo server` to confirm rendering
