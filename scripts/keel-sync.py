#!/usr/bin/env python3
"""
keel-sync — Sync coding rules from Project Keel into local AI tooling formats.

Reads Markdown rule files with YAML frontmatter from a Keel repository and
generates output for Cursor (.mdc), AGENTS.md, and CLAUDE.md.

Source resolution order:
  1. --path argument
  2. KEEL_PATH environment variable
  3. --clone argument (shallow clone to temp directory)
  4. KEEL_REPO environment variable (shallow clone to temp directory)

Rule selection:
  - Rules with alwaysApply: true are always included
  - Other rules are included if their globs match files in the project
  - Hidden directories (.git/, .cursor/, .agents/) are excluded from matching
  - A .keelignore file in the project root can exclude additional paths

.keelignore format:
  - One pattern per line, blank lines and # comments are ignored
  - Patterns use fnmatch syntax (*, ?, [seq])
  - Trailing / matches directories: scripts/ ignores everything under scripts/
  - Bare names match anywhere: AGENTS.md ignores that file in any directory
  - Path patterns match from project root: docs/*.md
"""

from __future__ import annotations

import argparse
import atexit
import difflib
import fnmatch
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HUGO_ONLY_FIELDS = {"title", "tags", "weight"}
SKIP_FILES = {"_index.md"}
KEELIGNORE = ".keelignore"


# ---------------------------------------------------------------------------
# Frontmatter parsing (stdlib only — no PyYAML dependency)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and Markdown body from file content."""
    m = re.match(r"^---\n(.+?)\n---\n?(.*)", text, re.DOTALL)
    if not m:
        return {}, text
    fm: dict = {}
    for line in m.group(1).splitlines():
        key, sep, val = line.partition(":")
        if not sep:
            continue
        fm[key.strip()] = _parse_value(val)
    return fm, m.group(2)


def _parse_value(raw: str):
    v = raw.strip()
    if v.startswith("[") and v.endswith("]"):
        return [_parse_value(i) for i in _split_array(v[1:-1]) if i.strip()]
    for q in ('"', "'"):
        if v.startswith(q) and v.endswith(q):
            return v[1:-1]
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    try:
        return int(v)
    except ValueError:
        return v


def _split_array(s: str) -> list[str]:
    items: list[str] = []
    buf: list[str] = []
    q = None
    for c in s:
        if c in ('"', "'") and q is None:
            q = c
            buf.append(c)
        elif c == q:
            q = None
            buf.append(c)
        elif c == "," and q is None:
            items.append("".join(buf))
            buf = []
        else:
            buf.append(c)
    if buf:
        items.append("".join(buf))
    return [i.strip() for i in items]


def format_frontmatter(fm: dict) -> str:
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
        elif isinstance(v, list):
            items = ", ".join(
                f'"{i}"' if isinstance(i, str) else str(i) for i in v
            )
            lines.append(f"{k}: [{items}]")
        elif isinstance(v, str):
            lines.append(f'{k}: "{v}"')
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def strip_hugo_fields(fm: dict) -> dict:
    return {k: v for k, v in fm.items() if k not in HUGO_ONLY_FIELDS}


# ---------------------------------------------------------------------------
# Source resolution
# ---------------------------------------------------------------------------

def resolve_source(args: argparse.Namespace) -> tuple[Path, bool]:
    """Return (rules_dir, is_temp_clone)."""
    path = args.path or os.environ.get("KEEL_PATH")
    if path:
        return _find_rules(Path(path).expanduser().resolve()), False

    repo = args.clone or os.environ.get("KEEL_REPO")
    if repo:
        return _shallow_clone(repo), True

    print(
        "Error: no Keel source specified.\n"
        "Use --path, --clone, KEEL_PATH, or KEEL_REPO.",
        file=sys.stderr,
    )
    sys.exit(1)


def _find_rules(src: Path) -> Path:
    if (src / "base.md").exists():
        return src
    candidate = src / "content" / "rules"
    if candidate.exists():
        return candidate
    print(f"Error: cannot find rules directory in {src}", file=sys.stderr)
    sys.exit(1)


def _shallow_clone(repo_url: str) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="keel-"))
    atexit.register(shutil.rmtree, tmp, True)
    print(f"Cloning {repo_url} …")
    subprocess.run(
        ["git", "clone", "--depth=1", "-q", repo_url, str(tmp)],
        check=True,
    )
    return _find_rules(tmp)


def git_pull(rules_dir: Path) -> None:
    git_root = rules_dir
    while git_root != git_root.parent:
        if (git_root / ".git").exists():
            break
        git_root = git_root.parent
    else:
        print("Warning: not a git repo, skipping --pull", file=sys.stderr)
        return
    print(f"Pulling {git_root} …")
    subprocess.run(["git", "-C", str(git_root), "pull", "-q"], check=True)


# ---------------------------------------------------------------------------
# Rule reading & filtering
# ---------------------------------------------------------------------------

def read_rules(rules_dir: Path) -> list[dict]:
    rules = []
    for p in sorted(rules_dir.glob("*.md")):
        if p.name in SKIP_FILES:
            continue
        fm, body = parse_frontmatter(p.read_text())
        rules.append({"name": p.stem, "file": p.name, "fm": fm, "body": body})
    return rules


def read_keelignore(project: Path) -> list[str]:
    """Read .keelignore patterns from the project root."""
    path = project / KEELIGNORE
    if not path.exists():
        return []
    patterns = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


def _is_ignored(rel_path: str, ignore: list[str]) -> bool:
    """Check if a relative path matches any ignore pattern."""
    parts = rel_path.split("/")
    for pat in ignore:
        # Directory pattern (trailing /) — match any path component
        if pat.endswith("/"):
            dirname = pat[:-1]
            if any(part == dirname for part in parts):
                return True
        # Match against the full relative path and the filename
        elif fnmatch.fnmatch(rel_path, pat):
            return True
        elif fnmatch.fnmatch(parts[-1], pat):
            return True
    return False


def filter_rules(
    rules: list[dict], project: Path, ignore: list[str]
) -> tuple[list[dict], list[dict]]:
    selected, skipped = [], []
    for r in rules:
        if r["fm"].get("alwaysApply"):
            r["reason"] = "alwaysApply"
            selected.append(r)
        elif _has_matches(r["fm"].get("globs", []), project, ignore):
            r["reason"] = f"matches {r['fm']['globs']}"
            selected.append(r)
        else:
            r["reason"] = f"no files for {r['fm'].get('globs', [])}"
            skipped.append(r)
    return selected, skipped


def _has_matches(globs: list, project: Path, ignore: list[str]) -> bool:
    for g in globs:
        try:
            for m in project.glob(g):
                # Skip hidden directories (e.g. .agents/, .cursor/)
                rel = m.relative_to(project)
                if any(part.startswith(".") for part in rel.parts):
                    continue
                if not m.is_file():
                    continue
                if _is_ignored(str(rel), ignore):
                    continue
                return True
        except (ValueError, OSError):
            continue
    return False


# ---------------------------------------------------------------------------
# Format detection
# ---------------------------------------------------------------------------

def detect_formats(project: Path) -> list[str]:
    fmts = []
    if (project / ".cursor").exists() or (project / ".cursorrules").exists():
        fmts.append("cursor")
    if (project / "AGENTS.md").exists():
        fmts.append("agents")
    if (project / "CLAUDE.md").exists():
        fmts.append("claude")
    # Copilot detection: not yet supported as a sync target.
    # if (project / ".github" / "copilot-instructions.md").exists():
    #     fmts.append("copilot")
    if not fmts:
        fmts = ["agents", "cursor", "claude"]
    return fmts


# ---------------------------------------------------------------------------
# File writing helpers
# ---------------------------------------------------------------------------

def write_if_changed(
    path: Path, content: str, *, force: bool, dry_run: bool
) -> bool:
    """Write file if content differs. Returns True if written/would-write."""
    if path.exists():
        old = path.read_text()
        if old == content:
            return False
        if not force:
            diff = difflib.unified_diff(
                old.splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile=str(path),
                tofile=str(path),
            )
            sys.stdout.writelines(diff)
    tag = " (dry run)" if dry_run else ""
    action = "update" if path.exists() else "create"
    print(f"  {action}: {path}{tag}")
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return True


def clean_dir(directory: Path, keep: set[str], *, dry_run: bool) -> None:
    """Remove files in directory that are not in the keep set."""
    if not directory.exists():
        return
    for p in sorted(directory.iterdir()):
        if p.is_file() and p.name not in keep:
            tag = " (dry run)" if dry_run else ""
            print(f"  remove: {p}{tag}")
            if not dry_run:
                p.unlink()


# ---------------------------------------------------------------------------
# Output generators
# ---------------------------------------------------------------------------

def sync_agents_rules(
    rules: list[dict], project: Path, **kw
) -> list[str]:
    out = project / ".agents" / "rules" / "keel"
    out.mkdir(parents=True, exist_ok=True)
    written = []
    keep: set[str] = set()
    for r in rules:
        clean = strip_hugo_fields(r["fm"])
        content = format_frontmatter(clean) + "\n" + r["body"]
        keep.add(r["file"])
        if write_if_changed(out / r["file"], content, **kw):
            written.append(str(out / r["file"]))
    clean_dir(out, keep, dry_run=kw.get("dry_run", False))
    return written


def sync_cursor_rules(
    rules: list[dict], project: Path, **kw
) -> list[str]:
    out = project / ".cursor" / "rules" / "keel"
    out.mkdir(parents=True, exist_ok=True)
    written = []
    keep: set[str] = set()
    for r in rules:
        clean = strip_hugo_fields(r["fm"])
        content = format_frontmatter(clean) + "\n" + r["body"]
        fname = r["name"] + ".mdc"
        keep.add(fname)
        if write_if_changed(out / fname, content, **kw):
            written.append(str(out / fname))
    clean_dir(out, keep, dry_run=kw.get("dry_run", False))
    return written


def sync_agents_md(rules: list[dict], project: Path, **kw) -> list[str]:
    MARKER_START = "<!-- keel:start - DO NOT EDIT between these markers -->"
    MARKER_END = "<!-- keel:end -->"

    gen_lines = [
        "## Rules",
        "",
        "| Rule | Globs | Always Apply |",
        "|------|-------|--------------|",
    ]
    for r in rules:
        globs = r["fm"].get("globs", [])
        always = str(r["fm"].get("alwaysApply", False)).lower()
        gen_lines.append(f"| {r['name']} | `{_fmt_globs(globs)}` | {always} |")

    gen_lines += ["", "## Rule Details"]

    for r in rules:
        fm = r["fm"]
        gen_lines += [
            "",
            f"### {r['name']}",
            f"- **Description:** {fm.get('description', '')}",
            f"- **Globs:** `{_fmt_globs(fm.get('globs', []))}`",
            f"- **File:** `.agents/rules/keel/{r['file']}`",
        ]

    generated = "\n".join(gen_lines)
    block = f"{MARKER_START}\n{generated}\n{MARKER_END}"

    path = project / "AGENTS.md"
    if path.exists():
        text = path.read_text()
        pat = re.escape(MARKER_START) + r"\n.*?\n" + re.escape(MARKER_END)
        if re.search(pat, text, re.DOTALL):
            content = re.sub(pat, block, text, count=1, flags=re.DOTALL)
        else:
            # No markers yet — replace the entire file but keep the heading
            content = f"# AGENTS.md\n\n{block}\n"
    else:
        content = f"# AGENTS.md\n\n{block}\n"

    written = []
    if write_if_changed(path, content, **kw):
        written.append(str(path))
    return written


def _fmt_globs(globs: list) -> str:
    """Format a glob list with double quotes (JSON-style)."""
    items = ", ".join(f'"{g}"' for g in globs)
    return f"[{items}]"


def _glob_label(fm: dict) -> str:
    if fm.get("alwaysApply"):
        return "(always apply)"
    globs = fm.get("globs", [])
    short = [g.replace("**/", "") for g in globs]
    return f"({', '.join(short)})"


def sync_claude_md(rules: list[dict], project: Path, **kw) -> list[str]:
    section_lines = [
        "## Coding Rules",
        "",
        "See `.agents/rules/keel/` for detailed coding standards. Key rules:",
    ]
    for r in rules:
        label = _glob_label(r["fm"])
        desc = r["fm"].get("description", r["name"])
        section_lines.append(
            f"- `.agents/rules/keel/{r['file']}` — {desc} {label}"
        )
    new_section = "\n".join(section_lines)

    path = project / "CLAUDE.md"
    if path.exists():
        text = path.read_text()
        pat = r"## Coding Rules\n.*?(?=\n## |\Z)"
        if re.search(pat, text, re.DOTALL):
            content = re.sub(pat, new_section, text, count=1, flags=re.DOTALL)
        else:
            content = text.rstrip() + "\n\n" + new_section + "\n"
    else:
        content = new_section + "\n"

    written = []
    if write_if_changed(path, content, **kw):
        written.append(str(path))
    return written


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Sync coding rules from Project Keel",
    )
    ap.add_argument("--path", help="Path to Keel repo or rules directory")
    ap.add_argument("--clone", metavar="URL", help="Shallow-clone repo URL")
    ap.add_argument("--pull", action="store_true", help="git pull before sync")
    ap.add_argument("--force", action="store_true", help="Skip diff display")
    ap.add_argument(
        "--dry-run", action="store_true", help="Preview without writing"
    )
    ap.add_argument(
        "--formats",
        help="Comma-separated formats: agents,cursor,claude (default: auto-detect)",
    )
    ap.add_argument(
        "--project",
        help="Target project directory (default: current directory)",
    )
    args = ap.parse_args()

    project = Path(args.project).resolve() if args.project else Path.cwd()

    # 1. Resolve source
    rules_dir, is_temp = resolve_source(args)
    if args.pull and not is_temp:
        git_pull(rules_dir)

    # 2. Read & filter
    ignore = read_keelignore(project)
    if ignore:
        print(f".keelignore: {len(ignore)} pattern(s)")
    all_rules = read_rules(rules_dir)
    selected, skipped = filter_rules(all_rules, project, ignore)

    print(f"\nSelected ({len(selected)}):")
    for r in selected:
        print(f"  + {r['name']:<20s} {r['reason']}")
    if skipped:
        print(f"\nSkipped ({len(skipped)}):")
        for r in skipped:
            print(f"  - {r['name']:<20s} {r['reason']}")

    if not selected:
        print("\nNo relevant rules found.")
        return

    # 3. Detect formats
    if args.formats:
        formats = [f.strip() for f in args.formats.split(",")]
    else:
        formats = detect_formats(project)
    print(f"\nFormats: {', '.join(formats)}\n")

    # 4. Sync
    kw = {"force": args.force, "dry_run": args.dry_run}
    written: list[str] = []

    if "agents" in formats or "claude" in formats:
        written += sync_agents_rules(selected, project, **kw)
    if "agents" in formats:
        written += sync_agents_md(selected, project, **kw)
    if "claude" in formats:
        written += sync_claude_md(selected, project, **kw)
    if "cursor" in formats:
        written += sync_cursor_rules(selected, project, **kw)

    # 5. Summary
    verb = "would write" if args.dry_run else "wrote"
    print(f"\nDone — {verb} {len(written)} file(s).")


if __name__ == "__main__":
    main()
