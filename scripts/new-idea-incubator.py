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
