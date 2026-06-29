# Idea Incubator Installer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic installer script that copies `idea-incubator-skeleton/` into a new destination, initializes Git on `main`, and creates the first commit.

**Architecture:** Add one Python CLI under `scripts/` with small helper functions for path resolution, source discovery, copying, and Git execution. Add a stdlib `unittest` suite that imports the script directly, tests helper behavior without touching real user folders, and runs one temporary end-to-end smoke test with Git identity supplied through environment variables.

**Tech Stack:** Python 3 standard library, `unittest`, `subprocess`, `pathlib`, `shutil`, Git.

---

## File Structure

Create or modify these files in `/Users/peluo/repos/repo-skeleton-dev`:

- Create: `scripts/new-idea-incubator.py`
  - CLI entry point.
  - Resolves bare names under `~/repos/`.
  - Treats explicit paths as exact destinations.
  - Copies the skeleton while preserving symlinks and ignoring local noise.
  - Runs Git initialization, staging, and first commit.
- Create: `tests/test_new_idea_incubator.py`
  - Imports the hyphenated script path with `importlib`.
  - Tests path resolution, destination refusal, symlink preservation, ignored files, and Git command order.
  - Runs a temporary end-to-end install smoke test.
- Modify: `README.md`
  - Add a short installer usage section while keeping the copyable-template explanation.

### Task 1: Add Tests For Installer Helpers

**Files:**
- Create: `tests/test_new_idea_incubator.py`

- [ ] **Step 1: Create the tests directory and test file**

Create `tests/test_new_idea_incubator.py` with this content:

```python
import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "new-idea-incubator.py"


def load_installer_module():
    spec = importlib.util.spec_from_file_location("new_idea_incubator", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InstallerHelperTests(unittest.TestCase):
    def setUp(self):
        self.installer = load_installer_module()

    def test_bare_name_resolves_under_repos(self):
        home = Path("/tmp/example-home")

        result = self.installer.resolve_destination("my-idea", home=home)

        self.assertEqual(result, home / "repos" / "my-idea")

    def test_explicit_tilde_path_is_honored(self):
        home = Path("/tmp/example-home")

        result = self.installer.resolve_destination("~/custom/my-idea", home=home)

        self.assertEqual(result, home / "custom" / "my-idea")

    def test_explicit_absolute_path_is_honored(self):
        result = self.installer.resolve_destination("/tmp/custom/my-idea")

        self.assertEqual(result, Path("/tmp/custom/my-idea"))

    def test_relative_path_with_slash_is_honored(self):
        result = self.installer.resolve_destination("custom/my-idea")

        self.assertEqual(result, Path("custom/my-idea"))

    def test_existing_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)

            with self.assertRaisesRegex(SystemExit, "Destination already exists"):
                self.installer.ensure_destination_available(destination)

    def test_copy_skeleton_preserves_symlink_and_ignores_ds_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source"
            destination = tmp_path / "destination"
            source.mkdir()
            (source / "AGENTS.md").write_text("# Agent Instructions\n", encoding="utf-8")
            (source / "CLAUDE.md").symlink_to("AGENTS.md")
            (source / ".DS_Store").write_text("local noise", encoding="utf-8")

            self.installer.copy_skeleton(source, destination)

            self.assertTrue((destination / "AGENTS.md").is_file())
            self.assertTrue((destination / "CLAUDE.md").is_symlink())
            self.assertEqual(os.readlink(destination / "CLAUDE.md"), "AGENTS.md")
            self.assertFalse((destination / ".DS_Store").exists())

    def test_initialize_git_runs_expected_commands(self):
        destination = Path("/tmp/example-project")

        with mock.patch.object(self.installer.shutil, "which", return_value="/usr/bin/git"), \
             mock.patch.object(self.installer.subprocess, "run") as run:
            self.installer.initialize_git(destination)

        self.assertEqual(
            [call.args[0] for call in run.call_args_list],
            [
                ["git", "init", "-b", "main"],
                ["git", "add", "."],
                ["git", "commit", "-m", "Initialize idea incubator project"],
            ],
        )
        self.assertEqual([call.kwargs["cwd"] for call in run.call_args_list], [destination] * 3)
        self.assertTrue(all(call.kwargs["check"] for call in run.call_args_list))


class InstallerEndToEndTests(unittest.TestCase):
    def test_installs_temp_project_with_clean_git_history(self):
        if not SCRIPT_PATH.exists():
            self.skipTest("installer script does not exist yet")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            destination = tmp_path / "installed-project"
            env = os.environ.copy()
            env.update(
                {
                    "GIT_AUTHOR_NAME": "Idea Installer Test",
                    "GIT_AUTHOR_EMAIL": "idea-installer-test@example.invalid",
                    "GIT_COMMITTER_NAME": "Idea Installer Test",
                    "GIT_COMMITTER_EMAIL": "idea-installer-test@example.invalid",
                }
            )

            subprocess.run(
                ["python3", str(SCRIPT_PATH), str(destination)],
                cwd=REPO_ROOT,
                env=env,
                check=True,
            )

            self.assertTrue((destination / "README.md").is_file())
            self.assertTrue((destination / "AGENTS.md").is_file())
            self.assertTrue((destination / "CLAUDE.md").is_symlink())
            self.assertEqual(os.readlink(destination / "CLAUDE.md"), "AGENTS.md")
            self.assertFalse((destination / "private").exists())

            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=destination,
                text=True,
                capture_output=True,
                check=True,
            ).stdout.strip()
            self.assertEqual(branch, "main")

            subject = subprocess.run(
                ["git", "log", "--oneline", "--format=%s", "-1"],
                cwd=destination,
                text=True,
                capture_output=True,
                check=True,
            ).stdout.strip()
            self.assertEqual(subject, "Initialize idea incubator project")

            status = subprocess.run(
                ["git", "status", "--short"],
                cwd=destination,
                text=True,
                capture_output=True,
                check=True,
            ).stdout.strip()
            self.assertEqual(status, "")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and verify the expected initial failure**

Run:

```bash
python3 -m unittest tests.test_new_idea_incubator
```

Expected:

```text
FileNotFoundError or a similar import failure for scripts/new-idea-incubator.py.
```

The failure confirms the tests are exercising the installer script that has not
been created yet.

- [ ] **Step 3: Commit the failing tests**

Run:

```bash
git add tests/test_new_idea_incubator.py
git commit -m "Test idea incubator installer behavior"
```

Expected: commit succeeds and includes only `tests/test_new_idea_incubator.py`.

### Task 2: Implement The Installer Script

**Files:**
- Create: `scripts/new-idea-incubator.py`

- [ ] **Step 1: Create the script**

Create `scripts/new-idea-incubator.py` with this content:

```python
#!/usr/bin/env python3
"""Create a new idea incubator project from the bundled skeleton."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


INITIAL_COMMIT_MESSAGE = "Initialize idea incubator project"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def skeleton_source() -> Path:
    return repo_root() / "idea-incubator-skeleton"


def resolve_destination(destination_arg: str, home: Path | None = None) -> Path:
    if not destination_arg:
        raise SystemExit("Destination is required.")

    if home is None:
        home = Path.home()

    if destination_arg.startswith("~/"):
        return home / destination_arg[2:]

    destination = Path(destination_arg)
    if destination.is_absolute() or "/" in destination_arg:
        return destination.expanduser()

    return home / "repos" / destination_arg


def ensure_source_available(source: Path) -> None:
    if not source.is_dir():
        raise SystemExit(f"Skeleton source not found: {source}")


def ensure_destination_available(destination: Path) -> None:
    if destination.exists() or destination.is_symlink():
        raise SystemExit(f"Destination already exists: {destination}")


def copy_skeleton(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        destination,
        symlinks=True,
        ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"),
    )


def initialize_git(destination: Path) -> None:
    if shutil.which("git") is None:
        raise SystemExit("git executable not found on PATH.")

    commands = [
        ["git", "init", "-b", "main"],
        ["git", "add", "."],
        ["git", "commit", "-m", INITIAL_COMMIT_MESSAGE],
    ]

    for command in commands:
        subprocess.run(command, cwd=destination, check=True)


def install(destination_arg: str) -> Path:
    source = skeleton_source()
    destination = resolve_destination(destination_arg)

    ensure_source_available(source)
    ensure_destination_available(destination)
    copy_skeleton(source, destination)
    initialize_git(destination)

    return destination


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new idea incubator project and initialize Git."
    )
    parser.add_argument(
        "destination",
        help="Bare name for ~/repos/<name>, or an explicit destination path.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    destination = install(args.destination)
    print(f"Created idea incubator project: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Make the script executable**

Run:

```bash
chmod +x scripts/new-idea-incubator.py
```

Expected: command exits 0.

- [ ] **Step 3: Run the focused tests**

Run:

```bash
python3 -m unittest tests.test_new_idea_incubator
```

Expected:

```text
Ran 8 tests
OK
```

- [ ] **Step 4: Run whitespace verification**

Run:

```bash
git diff --check
```

Expected: no output.

- [ ] **Step 5: Commit the implementation**

Run:

```bash
git add scripts/new-idea-incubator.py
git commit -m "Add idea incubator installer"
```

Expected: commit succeeds and includes only `scripts/new-idea-incubator.py`.

### Task 3: Document Installer Usage

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add installer documentation**

In `README.md`, replace the `## Intended Use` section with this content:

````markdown
## Intended Use

Use `scripts/new-idea-incubator.py` to create a new local idea project and
initialize Git immediately:

```sh
python3 scripts/new-idea-incubator.py my-new-idea
```

A bare name creates the project under `~/repos/`, so the command above creates
`~/repos/my-new-idea`. To use a different destination, pass an explicit path:

```sh
python3 scripts/new-idea-incubator.py ~/Documents/Codex/my-new-idea
python3 scripts/new-idea-incubator.py /absolute/path/to/my-new-idea
```

The installer copies `idea-incubator-skeleton/`, preserves symlinks, initializes
Git on `main`, stages the copied skeleton, and commits it with:

```text
Initialize idea incubator project
```

The script leaves copied content generic. After installation, update the new
project's README and notes when the project identity is clear.

The skeleton can also be copied manually:

```sh
cp -R idea-incubator-skeleton/. /path/to/new-project/
```

The copied project should be publishable with its Git history intact, because
private notes are kept in an ignored `private/` attachment point.
````

- [ ] **Step 2: Verify README rendering context**

Run:

```bash
sed -n '1,180p' README.md
```

Expected: output includes the installer usage, the explicit-path examples, the
manual copy fallback, and the existing repository layout section.

- [ ] **Step 3: Run tests and diff check**

Run:

```bash
python3 -m unittest tests.test_new_idea_incubator
git diff --check
```

Expected:

```text
Tests pass.
git diff --check prints nothing.
```

- [ ] **Step 4: Commit the documentation**

Run:

```bash
git add README.md
git commit -m "Document idea incubator installer"
```

Expected: commit succeeds and includes only `README.md`.

### Task 4: Final Verification

**Files:**
- Verify: `scripts/new-idea-incubator.py`
- Verify: `tests/test_new_idea_incubator.py`
- Verify: `README.md`

- [ ] **Step 1: Run the test suite**

Run:

```bash
python3 -m unittest tests.test_new_idea_incubator
```

Expected:

```text
Ran 8 tests
OK
```

- [ ] **Step 2: Run a manual temporary install**

Run:

```bash
tmpdir="$(mktemp -d)"
GIT_AUTHOR_NAME="Idea Installer Test" \
GIT_AUTHOR_EMAIL="idea-installer-test@example.invalid" \
GIT_COMMITTER_NAME="Idea Installer Test" \
GIT_COMMITTER_EMAIL="idea-installer-test@example.invalid" \
python3 scripts/new-idea-incubator.py "$tmpdir/manual-smoke"
git -C "$tmpdir/manual-smoke" log --oneline -1
git -C "$tmpdir/manual-smoke" status --short
test -L "$tmpdir/manual-smoke/CLAUDE.md"
test "$(readlink "$tmpdir/manual-smoke/CLAUDE.md")" = "AGENTS.md"
```

Expected:

```text
The installer prints the created project path.
git log --oneline -1 includes Initialize idea incubator project.
git status --short prints nothing.
Both symlink tests exit 0.
```

- [ ] **Step 3: Verify repository status and private safety**

Run:

```bash
git status --short
git diff --check
git ls-files | rg '(^|/)private(/|$)' || true
```

Expected:

```text
git status --short prints nothing.
git diff --check prints nothing.
No tracked private paths are printed.
```

- [ ] **Step 4: Report completion**

Summarize:

```text
Installer script path: scripts/new-idea-incubator.py
Default destination behavior: bare names create ~/repos/<name>
Verification run: python3 -m unittest tests.test_new_idea_incubator
Final Git status: clean
```
