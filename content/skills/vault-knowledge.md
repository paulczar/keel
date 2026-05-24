---
title: "Vault Knowledge"
description: "Process for capturing and maintaining project knowledge across sessions."
weight: 10
---

# Knowledge Management

Keel's knowledge wiki is a persistent, interlinked collection of markdown files that compounds over time. Agents write it; humans curate it.

This pattern is directly inspired by [Andrej Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the idea that instead of rediscovering knowledge from scratch on every query, an LLM incrementally builds and maintains a structured wiki. The index/log/lint operations and the ingest-query-lint loop are adapted from that design.

## Where knowledge lives

The knowledge wiki is at `content/knowledge/` with two special files:

- **`content/knowledge/index.md`** — a catalog of all pages, organized by category (concepts, entities, sources). The agent reads this first to find relevant pages.
- **`content/knowledge/log.md`** — an append-only chronological record of ingests, queries, and lint passes. Each entry starts with `## [YYYY-MM-DD]` for easy shell grepping.

## When to write

Write knowledge immediately when any of these happen:

- **User corrected you**: You made a mistake or wrong assumption and the user corrected it. This is the strongest signal — write down the correct information right away before moving on. The fact that you were wrong means the knowledge wasn't obvious.
- **User gave explicit guidance**: The user told you how they want things done (a preference, a pattern, a convention). Record it so you don't need to be told again.
- **Non-obvious constraint**: Something that would be easy to unknowingly violate.
- **Gotcha**: A quirk that cost significant time to figure out.
- **Design rationale**: Why a decision was made, especially if counterintuitive.
- **Good answers**: A synthesis you produced during a query — file it back as a new page.

If multiple triggers fire at once (e.g., a corrected assumption that's also a gotcha), write a single entry that covers all angles. Don't over-split.

## How to format

```
## [2026-05-22] Build System
Assumed `npm run build` uses esbuild, actually uses tsup.
Context: Fixing a bundle issue required checking tsup config.
```

Keep entries brief. Use bullet points for related items. Tag with YAML frontmatter for Dataview queries.

## Operations

### Ingest

When a new source is added:

1. Read the source. If the source is a URL:
   - Use **Playwright** for multi-page documentation (API refs, tutorials, docs that require clicking through)
   - Use the agent's built-in webfetch for single-page sources
2. If the source discusses library or framework APIs, use **Context7** to fetch current docs and cross-reference. Note any discrepancies.
3. Write a summary page in `content/knowledge/sources/`
4. Add a `## [YYYY-MM-DD] ingest | Title` entry to `log.md`
5. Update `index.md` with the new page
6. Update relevant entity/concept pages if the source adds new information

### Query

When answering a question:

1. Find relevant pages:
   - If the wiki is small (index.md fits one screen), read `index.md` directly
   - If the wiki is large, use **qmd** to search for relevant pages
2. Read the top-ranked pages
3. If the answer involves commands, API calls, or library usage, use **Context7** to verify syntax and flags before writing the answer
4. If the answer needs fact-checking against current web sources, use **Brave Search** or **Perplexity** to verify
5. Synthesize an answer with citations
6. If the answer is reusable, file it as a new page in `content/knowledge/concepts/`

### Slurp

Process unprocessed sources in `content/knowledge/unsorted/`:

1. List all files in `content/knowledge/unsorted/`
2. For each file, treat it as an ingest source:
   - Read the source
   - Use **Context7** and **Perplexity** to cross-reference and verify
   - Write a summary page to the appropriate knowledge section
   - Update `index.md` and `log.md`
   - Update relevant entity/concept pages
3. Move or delete the processed source from unsorted
4. Report: how many sources processed, what was created, any discrepancies found

The human fills unsorted via **Obsidian Web Clipper** or by dropping markdown files into the directory. Run slurp when asked or when unsorted has accumulated several files.

### Lint

Triggered after 3+ writes in a session, or when a contradiction is detected:

1. Check for contradictions between pages — surface both sides, don't silently pick
2. Check for orphan pages (no inbound links)
3. Check for stale entries (claims superseded by newer sources)
4. Check for mentioned concepts that lack their own page
5. Report results and suggest fixes

## Staleness audit

At the end of a multi-step session or when the wiki feels large:

- Scan for entries referencing tools, APIs, or patterns no longer in use
- Delete or archive them
- Merge related entries
- If `index.md` gets long, archive old sections

## Periodic Review Nudge

Every ~10 turns of conversation, do a quick scan of the session so far. Look for:

- User corrections or guidance you haven't saved yet
- Gotchas or constraints you discovered
- Complex workflows the user walked you through
- Decisions made that should be documented

If you find anything, write it to the knowledge wiki. This prevents the session from ending with important context still only in the conversation history.

## Consolidation

The wiki has no hard size limit, but as it grows, retrieval slows down. When the wiki feels large (index.md is long, log.md has many entries):

1. Merge related entries — e.g., three "project uses X" facts into one comprehensive entry
2. Archive old log entries to `log.archive.md`
3. Split large pages into sub-pages with cross-references
4. Rebuild `index.md` to reflect the consolidated structure

Consolidation is the wiki equivalent of memory compaction. Do it during lint or when you notice retrieval slowing down.

## Session Recall

The knowledge wiki is for persistent, curated facts. For "what did we discuss last week?" recall, the agent can search its past conversation history if the tool provides session search (e.g., FTS5 full-text search over past sessions). This is complementary — the wiki holds what's been distilled; session search holds what was said.

## Tips

- **Obsidian Web Clipper** — browser extension that converts web articles to markdown. Clip into `content/knowledge/unsorted/` for the agent to process later during a slurp.
- **Agent-created skills** — see the vault-skill-create skill for saving complex workflows as reusable procedures.
- **Migrate to vault** — see the vault-project-migrate skill for converting a project-local setup.

## Contributing back to keel

If you identify an improvement to this skill or the knowledge system itself, suggest creating a pull request to the [keel repository](https://github.com/paulczar/keel).
