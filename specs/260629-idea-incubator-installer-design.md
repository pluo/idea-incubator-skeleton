# Idea Incubator Installer Design

Date: 2026-06-29
Status: Approved for implementation planning

## Purpose

This repository currently exposes `idea-incubator-skeleton/` as a copyable
template directory. That model is transparent and portable, but it still leaves
too many repeated manual steps when starting a new idea project from mobile or
from the Codex app.

The installer should make the deterministic path one command: create a new local
folder from the skeleton, initialize Git immediately, and make the first commit.
It should not infer project identity or rewrite copied content.

## User Experience

The primary command should accept a single destination argument:

```sh
python3 scripts/new-idea-incubator.py my-idea
```

A bare name with no slash is resolved under `~/repos/`, so the command above
creates:

```text
~/repos/my-idea
```

The script should also accept an explicit destination path:

```sh
python3 scripts/new-idea-incubator.py ~/Documents/Codex/my-idea
python3 scripts/new-idea-incubator.py /absolute/path/to/my-idea
python3 scripts/new-idea-incubator.py relative/path/to/my-idea
```

Paths that include `/`, absolute paths, and `~/...` paths are treated as exact
destinations after normal path expansion. The default parent is only used for
bare folder names.

## Behavior

The installer creates a new project by copying the contents of
`idea-incubator-skeleton/` into the destination. It preserves symlinks, including
`CLAUDE.md -> AGENTS.md`, and excludes local filesystem noise such as `.DS_Store`.

After copying, it runs these Git operations inside the destination:

```sh
git init -b main
git add .
git commit -m "Initialize idea incubator project"
```

The initial commit should contain only the copied generic skeleton files.

## Safety Rules

The script should be conservative and deterministic:

- Refuse to continue if the destination already exists.
- Refuse to continue if the skeleton source directory cannot be found.
- Fail clearly if `git` or `python3` prerequisites are unavailable.
- Do not overwrite, merge into, or clean an existing directory.
- Do not configure a Git remote.
- Do not create `private/`.
- Do not edit `README.md`, create an initial idea note, or infer project name
  metadata from the destination.
- Preserve the skeleton's `.gitignore` rules so copied projects keep `private/`
  out of public history.

## Architecture

The installer should be a Python script at:

```text
scripts/new-idea-incubator.py
```

Python is preferred over shell because it provides explicit path handling,
portable symlink-preserving copy behavior, deterministic ignore filtering, and
straightforward tests. The script should depend only on the Python standard
library and the local `git` executable.

The script should resolve the skeleton source relative to its own file location,
not relative to the caller's current working directory. This allows agents or
humans to invoke it from the repository root or from another directory.

## Verification Strategy

Implementation should include focused automated tests for:

- bare names resolving under `~/repos/`,
- explicit paths being honored,
- refusal when the destination already exists,
- copying expected skeleton files,
- preserving the `CLAUDE.md -> AGENTS.md` symlink,
- excluding `.DS_Store`, and
- invoking Git in the expected order.

The final verification should also run the script against a temporary directory,
inspect the resulting Git history, and confirm the working tree is clean.

## Future Work

After the deterministic script is stable, a Codex skill can provide a
mobile-friendly conversational wrapper around it. A plugin, local Codex action,
or deep link can later make the same workflow easier to launch from the Codex app
or from Obsidian.
