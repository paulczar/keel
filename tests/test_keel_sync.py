"""Tests for scripts/keel-sync.py."""

import importlib.util
import sys
import textwrap
from pathlib import Path

import pytest

# Import keel-sync.py as a module despite the hyphen in the filename.
_spec = importlib.util.spec_from_file_location(
    "keel_sync",
    Path(__file__).resolve().parent.parent / "scripts" / "keel-sync.py",
)
ks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ks)


# ---------------------------------------------------------------------------
# parse_frontmatter
# ---------------------------------------------------------------------------

class TestParseFrontmatter:
    def test_basic(self):
        text = textwrap.dedent("""\
            ---
            title: "Go Standards"
            alwaysApply: false
            globs: ["**/*.go"]
            ---
            # Body
        """)
        fm, body = ks.parse_frontmatter(text)
        assert fm["title"] == "Go Standards"
        assert fm["alwaysApply"] is False
        assert fm["globs"] == ["**/*.go"]
        assert body.strip() == "# Body"

    def test_missing_frontmatter(self):
        text = "Just a plain markdown file.\n"
        fm, body = ks.parse_frontmatter(text)
        assert fm == {}
        assert body == text

    def test_always_apply_true(self):
        text = "---\nalwaysApply: true\n---\nBody\n"
        fm, body = ks.parse_frontmatter(text)
        assert fm["alwaysApply"] is True

    def test_multiple_globs(self):
        text = '---\nglobs: ["**/*.go", "**/go.mod", "**/go.sum"]\n---\n'
        fm, _ = ks.parse_frontmatter(text)
        assert fm["globs"] == ["**/*.go", "**/go.mod", "**/go.sum"]


# ---------------------------------------------------------------------------
# _parse_value
# ---------------------------------------------------------------------------

class TestParseValue:
    def test_bool_true(self):
        assert ks._parse_value(" true ") is True

    def test_bool_false(self):
        assert ks._parse_value("false") is False

    def test_int(self):
        assert ks._parse_value(" 42 ") == 42

    def test_string_unquoted(self):
        assert ks._parse_value(" hello ") == "hello"

    def test_string_double_quoted(self):
        assert ks._parse_value(' "hello world" ') == "hello world"

    def test_string_single_quoted(self):
        assert ks._parse_value(" 'hello' ") == "hello"

    def test_array(self):
        assert ks._parse_value('["a", "b"]') == ["a", "b"]

    def test_empty_array(self):
        assert ks._parse_value("[]") == []


# ---------------------------------------------------------------------------
# _split_array
# ---------------------------------------------------------------------------

class TestSplitArray:
    def test_simple(self):
        assert ks._split_array('"a", "b", "c"') == ['"a"', '"b"', '"c"']

    def test_quoted_comma(self):
        result = ks._split_array('"a, b", "c"')
        assert result == ['"a, b"', '"c"']

    def test_empty(self):
        # Empty string produces [""] from the buffer, but callers filter blanks
        result = ks._split_array("")
        assert all(item.strip() == "" for item in result)


# ---------------------------------------------------------------------------
# strip_hugo_fields
# ---------------------------------------------------------------------------

class TestStripHugoFields:
    def test_strips_hugo_only(self):
        fm = {
            "title": "Test",
            "tags": ["go"],
            "weight": 10,
            "description": "desc",
            "globs": ["*.go"],
            "alwaysApply": False,
        }
        result = ks.strip_hugo_fields(fm)
        assert "title" not in result
        assert "tags" not in result
        assert "weight" not in result
        assert result["description"] == "desc"
        assert result["globs"] == ["*.go"]
        assert result["alwaysApply"] is False


# ---------------------------------------------------------------------------
# format_frontmatter
# ---------------------------------------------------------------------------

class TestFormatFrontmatter:
    def test_round_trip(self):
        text = textwrap.dedent("""\
            ---
            description: "Go coding conventions"
            globs: ["**/*.go", "**/go.mod"]
            alwaysApply: false
            ---
            # Body
        """)
        fm, body = ks.parse_frontmatter(text)
        clean = ks.strip_hugo_fields(fm)
        output = ks.format_frontmatter(clean)
        assert output.startswith("---\n")
        assert output.endswith("\n---")
        # Re-parse the output to check validity
        fm2, _ = ks.parse_frontmatter(output + "\n")
        assert fm2["description"] == "Go coding conventions"
        assert fm2["globs"] == ["**/*.go", "**/go.mod"]
        assert fm2["alwaysApply"] is False

    def test_bool_formatting(self):
        output = ks.format_frontmatter({"alwaysApply": True})
        assert "alwaysApply: true" in output

    def test_int_formatting(self):
        output = ks.format_frontmatter({"weight": 5})
        assert "weight: 5" in output


# ---------------------------------------------------------------------------
# read_keelignore
# ---------------------------------------------------------------------------

class TestReadKeelignore:
    def test_reads_patterns(self, tmp_path):
        (tmp_path / ".keelignore").write_text(
            "# comment\nscripts/\n\nAGENTS.md\n"
        )
        patterns = ks.read_keelignore(tmp_path)
        assert patterns == ["scripts/", "AGENTS.md"]

    def test_missing_file(self, tmp_path):
        assert ks.read_keelignore(tmp_path) == []


# ---------------------------------------------------------------------------
# _is_ignored
# ---------------------------------------------------------------------------

class TestIsIgnored:
    def test_directory_pattern_match(self):
        assert ks._is_ignored("scripts/foo.py", ["scripts/"])

    def test_directory_pattern_nested(self):
        assert ks._is_ignored("src/scripts/bar.py", ["scripts/"])

    def test_directory_pattern_no_false_positive(self):
        """scripts/ should NOT match my-scripts/foo.py."""
        assert not ks._is_ignored("my-scripts/foo.py", ["scripts/"])

    def test_directory_pattern_no_false_positive_prefix(self):
        """scripts/ should NOT match pre-scripts/foo.py."""
        assert not ks._is_ignored("pre-scripts/foo.py", ["scripts/"])

    def test_filename_pattern(self):
        assert ks._is_ignored("docs/AGENTS.md", ["AGENTS.md"])

    def test_filename_pattern_root(self):
        assert ks._is_ignored("AGENTS.md", ["AGENTS.md"])

    def test_path_pattern(self):
        assert ks._is_ignored("docs/readme.md", ["docs/*.md"])

    def test_no_match(self):
        assert not ks._is_ignored("src/main.go", ["scripts/", "AGENTS.md"])

    def test_wildcard_pattern(self):
        assert ks._is_ignored("README.md", ["*.md"])

    def test_deep_directory_match(self):
        assert ks._is_ignored("a/b/scripts/c.py", ["scripts/"])


# ---------------------------------------------------------------------------
# filter_rules
# ---------------------------------------------------------------------------

class TestFilterRules:
    def test_always_apply_included(self, tmp_path):
        rules = [
            {"name": "base", "file": "base.md", "fm": {"alwaysApply": True}, "body": ""},
        ]
        selected, skipped = ks.filter_rules(rules, tmp_path, [])
        assert len(selected) == 1
        assert selected[0]["name"] == "base"
        assert selected[0]["reason"] == "alwaysApply"

    def test_glob_match(self, tmp_path):
        (tmp_path / "main.go").write_text("package main")
        rules = [
            {
                "name": "go",
                "file": "go.md",
                "fm": {"alwaysApply": False, "globs": ["**/*.go"]},
                "body": "",
            },
        ]
        selected, skipped = ks.filter_rules(rules, tmp_path, [])
        assert len(selected) == 1

    def test_no_match_skipped(self, tmp_path):
        rules = [
            {
                "name": "go",
                "file": "go.md",
                "fm": {"alwaysApply": False, "globs": ["**/*.go"]},
                "body": "",
            },
        ]
        selected, skipped = ks.filter_rules(rules, tmp_path, [])
        assert len(skipped) == 1
        assert skipped[0]["name"] == "go"

    def test_ignored_file_not_matched(self, tmp_path):
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "test.py").write_text("x")
        rules = [
            {
                "name": "python",
                "file": "python.md",
                "fm": {"alwaysApply": False, "globs": ["**/*.py"]},
                "body": "",
            },
        ]
        selected, skipped = ks.filter_rules(rules, tmp_path, ["scripts/"])
        assert len(skipped) == 1


# ---------------------------------------------------------------------------
# detect_formats
# ---------------------------------------------------------------------------

class TestDetectFormats:
    def test_cursor_directory(self, tmp_path):
        (tmp_path / ".cursor").mkdir()
        fmts = ks.detect_formats(tmp_path)
        assert "cursor" in fmts

    def test_cursorrules_file(self, tmp_path):
        (tmp_path / ".cursorrules").touch()
        fmts = ks.detect_formats(tmp_path)
        assert "cursor" in fmts

    def test_agents_md(self, tmp_path):
        (tmp_path / "AGENTS.md").touch()
        fmts = ks.detect_formats(tmp_path)
        assert "agents" in fmts

    def test_claude_md(self, tmp_path):
        (tmp_path / "CLAUDE.md").touch()
        fmts = ks.detect_formats(tmp_path)
        assert "claude" in fmts

    def test_copilot_not_detected(self, tmp_path):
        """Copilot format is disabled — should not appear even if file exists."""
        gh = tmp_path / ".github"
        gh.mkdir()
        (gh / "copilot-instructions.md").touch()
        fmts = ks.detect_formats(tmp_path)
        assert "copilot" not in fmts

    def test_fallback(self, tmp_path):
        fmts = ks.detect_formats(tmp_path)
        assert fmts == ["agents", "cursor", "claude"]


# ---------------------------------------------------------------------------
# write_if_changed
# ---------------------------------------------------------------------------

class TestWriteIfChanged:
    def test_creates_new_file(self, tmp_path):
        path = tmp_path / "test.md"
        result = ks.write_if_changed(path, "content", force=True, dry_run=False)
        assert result is True
        assert path.read_text() == "content"

    def test_no_change(self, tmp_path):
        path = tmp_path / "test.md"
        path.write_text("content")
        result = ks.write_if_changed(path, "content", force=True, dry_run=False)
        assert result is False

    def test_updates_changed(self, tmp_path):
        path = tmp_path / "test.md"
        path.write_text("old")
        result = ks.write_if_changed(path, "new", force=True, dry_run=False)
        assert result is True
        assert path.read_text() == "new"

    def test_dry_run_no_write(self, tmp_path):
        path = tmp_path / "test.md"
        result = ks.write_if_changed(path, "content", force=True, dry_run=True)
        assert result is True
        assert not path.exists()

    def test_dry_run_no_update(self, tmp_path):
        path = tmp_path / "test.md"
        path.write_text("old")
        result = ks.write_if_changed(path, "new", force=True, dry_run=True)
        assert result is True
        assert path.read_text() == "old"


# ---------------------------------------------------------------------------
# clean_dir
# ---------------------------------------------------------------------------

class TestCleanDir:
    def test_removes_stale(self, tmp_path):
        (tmp_path / "keep.md").write_text("keep")
        (tmp_path / "stale.md").write_text("stale")
        ks.clean_dir(tmp_path, {"keep.md"}, dry_run=False)
        assert (tmp_path / "keep.md").exists()
        assert not (tmp_path / "stale.md").exists()

    def test_keeps_listed(self, tmp_path):
        (tmp_path / "a.md").write_text("a")
        (tmp_path / "b.md").write_text("b")
        ks.clean_dir(tmp_path, {"a.md", "b.md"}, dry_run=False)
        assert (tmp_path / "a.md").exists()
        assert (tmp_path / "b.md").exists()

    def test_dry_run_keeps_all(self, tmp_path):
        (tmp_path / "stale.md").write_text("stale")
        ks.clean_dir(tmp_path, set(), dry_run=True)
        assert (tmp_path / "stale.md").exists()

    def test_missing_directory(self, tmp_path):
        # Should not raise
        ks.clean_dir(tmp_path / "nonexistent", set(), dry_run=False)


# ---------------------------------------------------------------------------
# Integration: dry-run against real content/rules/
# ---------------------------------------------------------------------------

class TestIntegration:
    @pytest.fixture()
    def project(self, tmp_path):
        """Create a minimal Go project fixture."""
        (tmp_path / "main.go").write_text("package main\n")
        (tmp_path / "go.mod").write_text("module example.com/test\ngo 1.21\n")
        return tmp_path

    def test_dry_run_against_fixture(self, project):
        """Run the full pipeline in dry-run mode against a fixture project."""
        rules_dir = Path(__file__).resolve().parent.parent / "content" / "rules"
        if not rules_dir.exists():
            pytest.skip("content/rules/ not found")

        all_rules = ks.read_rules(rules_dir)
        assert len(all_rules) > 0

        selected, skipped = ks.filter_rules(all_rules, project, [])
        # base should always be selected
        names = [r["name"] for r in selected]
        assert "base" in names
        # go should match
        assert "go" in names

    def test_sync_agents_rules_dry_run(self, project):
        rules = [
            {
                "name": "base",
                "file": "base.md",
                "fm": {
                    "description": "Global standards",
                    "globs": ["**/*"],
                    "alwaysApply": True,
                    "title": "Base",
                    "tags": ["global"],
                    "weight": 1,
                },
                "body": "# Base\n",
            }
        ]
        written = ks.sync_agents_rules(rules, project, force=True, dry_run=True)
        assert len(written) == 1
        # File should NOT exist in dry-run
        out = project / ".agents" / "rules" / "keel" / "base.md"
        assert not out.exists()

    def test_sync_cursor_rules(self, project):
        rules = [
            {
                "name": "go",
                "file": "go.md",
                "fm": {
                    "description": "Go standards",
                    "globs": ["**/*.go"],
                    "alwaysApply": False,
                },
                "body": "# Go\n",
            }
        ]
        written = ks.sync_cursor_rules(rules, project, force=True, dry_run=False)
        assert len(written) == 1
        out = project / ".cursor" / "rules" / "keel" / "go.mdc"
        assert out.exists()
        content = out.read_text()
        assert "title" not in content
        assert "description" in content

    def test_sync_agents_md(self, project):
        rules = [
            {
                "name": "base",
                "file": "base.md",
                "fm": {
                    "description": "Global standards",
                    "globs": ["**/*"],
                    "alwaysApply": True,
                },
                "body": "# Base\n",
            }
        ]
        written = ks.sync_agents_md(rules, project, force=True, dry_run=False)
        assert len(written) == 1
        content = (project / "AGENTS.md").read_text()
        assert "## Rules" in content
        assert "base" in content

    def test_sync_claude_md(self, project):
        rules = [
            {
                "name": "base",
                "file": "base.md",
                "fm": {
                    "description": "Global standards",
                    "globs": ["**/*"],
                    "alwaysApply": True,
                },
                "body": "# Base\n",
            }
        ]
        written = ks.sync_claude_md(rules, project, force=True, dry_run=False)
        assert len(written) == 1
        content = (project / "CLAUDE.md").read_text()
        assert "## Coding Rules" in content
        assert "base.md" in content
