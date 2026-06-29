import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "new-idea-incubator.py"
GIT_IDENTITY_ENV = {
    "GIT_AUTHOR_NAME": "Idea Installer Test",
    "GIT_AUTHOR_EMAIL": "idea-installer-test@example.invalid",
    "GIT_COMMITTER_NAME": "Idea Installer Test",
    "GIT_COMMITTER_EMAIL": "idea-installer-test@example.invalid",
}
EMPTY_GIT_IDENTITY_ENV = {key: "" for key in GIT_IDENTITY_ENV}


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

    def test_run_git_converts_subprocess_failures_to_system_exit(self):
        destination = Path("/tmp/example-project")

        with mock.patch.object(
            self.installer.subprocess,
            "run",
            side_effect=subprocess.CalledProcessError(
                returncode=128,
                cmd=["git", "status"],
                stderr="fatal: not a git repository\n",
            ),
        ):
            with self.assertRaisesRegex(SystemExit, "Git command failed: git status"):
                self.installer.run_git(["status"], cwd=destination)

    def test_git_identity_accepts_complete_author_and_committer_environment(self):
        with mock.patch.dict(os.environ, GIT_IDENTITY_ENV, clear=False), \
             mock.patch.object(self.installer.subprocess, "run") as run:
            self.installer.ensure_git_identity_configured()

        run.assert_not_called()

    def test_git_identity_accepts_global_name_and_email(self):
        def git_config(command, **kwargs):
            values = {
                "user.name": "Idea Installer Test",
                "user.email": "idea-installer-test@example.invalid",
            }
            return subprocess.CompletedProcess(
                command,
                0,
                stdout=f"{values[command[-1]]}\n",
                stderr="",
            )

        with mock.patch.dict(os.environ, EMPTY_GIT_IDENTITY_ENV, clear=False), \
             mock.patch.object(self.installer.subprocess, "run", side_effect=git_config):
            self.installer.ensure_git_identity_configured()

    def test_install_rejects_missing_git_identity_before_copying_skeleton(self):
        def git_config_missing(command, **kwargs):
            return subprocess.CompletedProcess(command, 1, stdout="", stderr="")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source"
            destination = tmp_path / "destination"
            source.mkdir()
            (source / "README.md").write_text("# Example\n", encoding="utf-8")

            with mock.patch.object(self.installer, "skeleton_source", return_value=source), \
                 mock.patch.object(self.installer.shutil, "which", return_value="/usr/bin/git"), \
                 mock.patch.dict(os.environ, EMPTY_GIT_IDENTITY_ENV, clear=False), \
                 mock.patch.object(
                     self.installer.subprocess,
                     "run",
                     side_effect=git_config_missing,
                 ):
                with self.assertRaisesRegex(SystemExit, "Git commit identity is not configured"):
                    self.installer.install(str(destination))

            self.assertFalse(destination.exists())

    def test_install_checks_git_before_copying_skeleton(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source"
            destination = tmp_path / "destination"
            source.mkdir()
            (source / "README.md").write_text("# Example\n", encoding="utf-8")

            with mock.patch.object(self.installer, "skeleton_source", return_value=source), \
                 mock.patch.object(self.installer.shutil, "which", return_value=None):
                with self.assertRaisesRegex(SystemExit, "git executable not found"):
                    self.installer.install(str(destination))

            self.assertFalse(destination.exists())


class InstallerEndToEndTests(unittest.TestCase):
    def test_installs_temp_project_with_clean_git_history(self):
        if not SCRIPT_PATH.exists():
            self.skipTest("installer script does not exist yet")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            destination = tmp_path / "installed-project"
            env = os.environ.copy()
            env.update(GIT_IDENTITY_ENV)

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
