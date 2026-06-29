#!/usr/bin/env python3
"""Create a new idea incubator project from the bundled skeleton."""

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


INITIAL_COMMIT_MESSAGE = "Initialize idea incubator project"
GIT_IDENTITY_ENV_VARS = (
    "GIT_AUTHOR_NAME",
    "GIT_AUTHOR_EMAIL",
    "GIT_COMMITTER_NAME",
    "GIT_COMMITTER_EMAIL",
)


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


def ensure_git_available() -> None:
    if shutil.which("git") is None:
        raise SystemExit("git executable not found on PATH.")


def format_git_failure(command: list[str], output: str | None = None) -> str:
    message = f"Git command failed: {shlex.join(command)}"
    if output:
        message = f"{message}: {output.strip()}"
    return message


def run_git(
    args: list[str],
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    command = ["git", *args]
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=check,
        )
    except subprocess.CalledProcessError as error:
        output = error.stderr or error.stdout
        raise SystemExit(format_git_failure(command, output)) from None


def git_global_config_value(name: str) -> str:
    result = run_git(["config", "--global", "--get", name], check=False)
    if result.returncode == 0:
        return result.stdout.strip()
    if result.returncode == 1:
        return ""

    output = result.stderr or result.stdout
    raise SystemExit(format_git_failure(["git", "config", "--global", "--get", name], output))


def has_complete_env_git_identity() -> bool:
    return all(os.environ.get(name, "").strip() for name in GIT_IDENTITY_ENV_VARS)


def has_any_env_git_identity() -> bool:
    return any(name in os.environ for name in GIT_IDENTITY_ENV_VARS)


def ensure_git_identity_configured() -> None:
    if has_any_env_git_identity():
        if has_complete_env_git_identity():
            return
        raise SystemExit(
            "Git commit identity environment is incomplete. "
            "Set all four Git author/committer environment variables to "
            "non-empty values, or unset them to use global Git config."
        )

    if git_global_config_value("user.name") and git_global_config_value("user.email"):
        return

    raise SystemExit(
        "Git commit identity is not configured. "
        'Run `git config --global user.name "Your Name"` and '
        "`git config --global user.email you@example.com`, or set all four "
        "Git author/committer environment variables."
    )


def copy_skeleton(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        destination,
        symlinks=True,
        ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"),
    )


def initialize_git(destination: Path) -> None:
    ensure_git_available()

    commands = [
        ["init", "-b", "main"],
        ["add", "."],
        ["commit", "-m", INITIAL_COMMIT_MESSAGE],
    ]

    for command in commands:
        run_git(command, cwd=destination)


def install(destination_arg: str) -> Path:
    source = skeleton_source()
    destination = resolve_destination(destination_arg)

    ensure_source_available(source)
    ensure_destination_available(destination)
    ensure_git_available()
    ensure_git_identity_configured()
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
