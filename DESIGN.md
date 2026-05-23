# Keel v2 Design

Keel v2 is the evolution of keel v1 from a **rule distribution CMS** into a **cross-agent content management system** for rules, skills, and knowledge. Same Hugo site, same sync tooling, expanded to cover the full lifecycle of AI agent context.

## Two Systems

Keel has two distinct forms depending on who is using it:

| | **Framework repo** (this repo) | **Downstream vault** (`~/.keel/`) |
|---|---|---|
| **Is a...** | Source of truth for the framework | Your personal instance |
| **Rendered as** | Hugo documentation site | Obsidian vault |
| **Agentic context** | Rules, skills, behaviors, MCP guidance | Chosen behavior profile as AGENTS.md |
| **Memory system** | Documents how it works | *Is* the memory system |
| **What goes in** | Rules, skills, behaviors, MCP tool definitions | `content/keel/` (framework clone) + `content/local/` (your knowledge) |
| **Sync direction** | PR back with improvements | Pull framework updates, keep local private |
| **Authored by** | Humans (PRs) | Agents + Humans |

The repo **describes** the system. The vault **runs** the system. This distinction resolves a lot of the ambiguity in v1 — the repo doesn't need layers, doesn't host your personal knowledge, and doesn't need to be an Obsidian vault. It ships the blueprint that makes downstream vaults work.

## Three Content Dimensions

Keel v2 manages three distinct types of content. Each has different authorship patterns, lifecycle, and consumption mechanisms:

| Dimension | Keel v1 | Keel v2 | Authored by | Lifecycle |
|-----------|---------|---------|-------------|-----------|
| **Rules** | Yes | Yes | Humans (via PRs) | Static, versioned, infrequent change |
| **Skills** | No | Yes | Humans (via PRs) | Semi-static, updated per workflow need |
| **Knowledge** | No | Yes | Agents + Humans | Dynamic, constantly evolving |

### Rules

Static coding standards and conventions. What agents *must* do.

- Authored as Markdown with YAML frontmatter (`globs`, `alwaysApply`, `description`)
- Stored in `content/rules/` for Hugo rendering
- Distributed via `keel-sync.py` to `.cursor/rules/keel/`, `.agents/rules/keel/`, CLAUDE.md references
- Layer precedence is handled downstream — see "The Layering Model" below

### Skills

Reusable procedures loaded on-demand. How to do specific things.

- Authored as SKILL.md with opencode-compatible frontmatter (`name`, `description`, `compatibility`)
- Stored in `content/skills/` for Hugo rendering
- Distributed as symlinks or copies to `.opencode/skills/`, `.claude/skills/`, `.cursor/skills/`
- Agents load skills lazily via native tool (e.g., opencode `skill()` tool)
- Each skill is self-contained: instructions + embedded ` ```bash ` or ` ```python ` code blocks
- Layer precedence is handled downstream — see below

Skills may embed scripts as code blocks. The agent extracts, writes to a temp file, and executes.

### Knowledge

A persistent, interlinked wiki that compounds over time. What agents *have learned*.

- Evolved from [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern
- Stored in `content/knowledge/` for Hugo rendering
- Agents write to `content/knowledge/` directly; humans curate via PRs
- Supports three operations: **Ingest** (add source → agent updates wiki), **Query** (ask questions against wiki), **Lint** (health-check for contradictions, orphans, staleness)
- Agent writes new pages under `content/knowledge/keel/`
- Project-specific knowledge lives in the project's own store, not in keel — see below

## Framework Structure

This repo is the framework source — NOT a downstream vault. The downstream vault adds `content/local/` and uses a behavior profile as its AGENTS.md.

```
keel/                               ← this repo (the framework)
├── content/                        ← Hugo source (renders everything)
│   ├── _index.md                   ← landing page
│   ├── rules/                      ← rule files
│   │   ├── _index.md
│   │   ├── base.md
│   │   └── typescript.md
│   ├── skills/                     ← skill files
│   │   ├── _index.md
│   │   └── knowledge-management.md
│   └── knowledge/                  ← knowledge wiki pages
│       ├── _index.md
│       ├── index.md
│       ├── log.md
│       ├── concepts/
│       ├── entities/
│       └── sources/
│
├── scripts/
│   ├── keel-sync.py                ← sync rules + skills to projects
│   └── keel-init.py                ← init knowledge wiki in a project
│
├── templates/                      ← agent config templates
│   ├── AGENTS.md.tmpl
│   ├── CLAUDE.md.tmpl
│   └── mdc.tmpl
│
├── DESIGN.md                       ← this file
├── README.md
├── hugo.yaml
├── Makefile
└── ...
```

### The Layering Model

keel itself does not implement layering. Layering is a **downstream convention** between multiple independent vaults:

```
~/keel/                         ← global defaults (keel layer)
~/org-standards/                ← organizational standards (org layer)
~/obsidian/personal/            ← personal knowledge (local layer)

~/src/my-project/
├── AGENTS.md                   ← tells agents:
│   # Knowledge sources (precedence order):
│   # 1. ./local/              ← project-specific (highest)
│   # 2. ~/org-standards/      ← org standards
│   # 3. ~/keel/               ← global defaults (lowest)
│   ├── knowledge/
│   └── local/
```

Each vault is a standalone keel instance (framework clone + local knowledge). The project's AGENTS.md configures which vaults to consult and in what order. keel-sync.py writes to the `keel/` subdirectory in downstream projects — it owns only that layer.

Rule precedence: higher layer **replaces** lower on the same topic (set in base.md).
Knowledge precedence: higher layer **augments** lower; contradictions are flagged, not silently resolved (handled by the knowledge-management skill).

## Two Modes of Use

### Vault mode (recommended)

The user maintains a downstream vault (e.g., `~/.keel/`) with the framework cloned into `content/keel/` and their personal knowledge in `content/local/`. Their project's AGENTS.md tells agents where the vault lives. Agents read rules, skills, and knowledge directly from the vault. No per-project sync needed — the agent knows the path.

Output mapping for vault mode:

| Content | How agents access it |
|---------|----------------------|
| **Rules** | Agent reads from vault path (configured in project's AGENTS.md) |
| **Skills** | Symlinked or copied to `.opencode/skills/`, `.claude/skills/` at vault setup |
| **Knowledge** | Agent reads directly from vault's `content/knowledge/` |

### Project-local mode (optional)

For users who don't want a vault and prefer rules inside each project.

`keel-sync.py` is an optional helper that copies relevant rules into a project based on its contents (language detection, existing tooling). Originally keel v1's primary mechanism; now a convenience for the project-local workflow.

```
# Copy matching rules into the current project
python3 scripts/keel-sync.py --project /path/to/target

# Preview what would change
python3 scripts/keel-sync.py --project /path/to/target --dry-run
```

The script reads rule frontmatter (`globs`, `alwaysApply`), matches against the target project's files, and writes matching rules to the appropriate location (`.cursor/rules/`, `.agents/rules/`, or AGENTS.md routing table). It also installs slash commands if the project uses opencode or Claude Code.

## Self-Improvement Loop

1. Agent starts session → reads `KNOWLEDGE.md` (or whatever path AGENTS.md configures) and relevant rules
2. Agent makes an incorrect assumption → user corrects it → agent writes correction to the project's knowledge store
3. At lint time, agent scans for contradictions between knowledge sources, orphan pages, stale entries
4. Promising project knowledge can be promoted to org or keel vaults via PR

## Development

```bash
# Preview the Hugo site
make preview

# Dogfood: symlink rules + skills into local tooling
make dev-sync

# Run tests
make test
```

## Design Decisions

### Q1: Skills and rules — independent or cross-referencing?

**Decision: Self-contained by default. Skills may reference rules when globs wouldn't match.**

A skill is self-contained — the agent loads one skill and gets everything it needs to execute that procedure. No duplication of rule content inside skills.

Exception: if a skill genuinely needs a rule that wouldn't be caught by normal glob matching (e.g., a deployment skill needs kubernetes rules, but the project has no `.yaml` files yet), the skill may include a `## Required Rules` section naming specific rules. The agent loads those rules directly by path, bypassing glob matching.

### Q2: Knowledge linting cadence

**Decision: Agent-initiated, triggered by session activity.**

- After 3+ knowledge writes in a single session → suggest a lint pass
- If the agent detects a contradiction during a query → flag it immediately
- Explicit `/keel-knowledge-lint` command always available
- No cron — the vault is passive when no agent is active

The knowledge-management skill encodes the trigger logic. The agent self-decides based on those heuristics.

### Q3: Hugo layout for skills

**Decision: Yes, a custom layout is warranted.**

Skills have different visual weight than rules:

| Element | Rules | Skills |
|---------|-------|--------|
| Primary content | Prose (conventions) | Instructions + code blocks |
| Frontmatter display | Minimal (description only) | Prominent (name, description, compatibility, tool) |
| Code blocks | Occasional examples | Central (the executable part) |
| Navigation role | Reference | How-to / workflow |

Create `layouts/skills/single.html` — close to the default book layout but with:
- Frontmatter rendered as a "card" at top (name, description, target tools)
- Code blocks visually emphasized with a "copy" affordance
- Sections for prerequisites, usage, and examples

### Q4: keel-sync.py — subcommands vs flags

**Decision: Subcommands, with backward compatibility.**

```
keel-sync.py rules      ← default (same as v1 behavior)
keel-sync.py skills     ← sync skills to project
keel-sync.py knowledge  ← init knowledge wiki in project
keel-sync.py all        ← do everything
```

Flags are reserved for options ( `--project`, `--dry-run`, `--force`). Subcommands keep the CLI navigable as the tool grows. No subcommand defaults to `rules` for v1 compatibility.

### Q5: Obsidian compatibility model

**Decision: The downstream vault is the Obsidian vault, not this repo.**

The framework repo is a Hugo site — not an Obsidian vault. The downstream vault at `~/.keel/` is the Obsidian vault. It contains the framework as a clone (`content/keel/`) plus personal knowledge (`content/local/`).

The framework repo's `content/` directory can be opened in Obsidian for editing if desired (same markdown files), but this is a convenience, not the primary model. The downstream vault is where Obsidian's graph view, Dataview queries, and Web Clipper integration live.
