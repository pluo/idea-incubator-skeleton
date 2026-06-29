# Idea Incubator Skeleton Dev

This repository develops `idea-incubator-skeleton/`, a copyable Git repository skeleton for
idea-first projects.

The skeleton is for early-stage ideas that may later become research projects,
code projects, public products, or archived lines of thought. It preserves
public-safe provenance from day one while keeping private AI session notes out
of Git history.

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
python3 scripts/new-idea-incubator.py relative/path/to/my-new-idea
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

## Repository Layout

```text
idea-incubator-skeleton-dev/
  README.md
  specs/
    YYMMDD-idea-incubator-skeleton-design.md
    YYMMDD-idea-incubator-skeleton-implementation-plan.md

  idea-incubator-skeleton/
    AGENTS.md
    CLAUDE.md -> AGENTS.md
    .gitignore
    README.md
    docs/
    ideas/
    sessions/
    decisions/
    specs/
    research/
```

`idea-incubator-skeleton-dev/specs/` contains dated design records and implementation
plans for developing this template. Inside the template, `docs/` contains
current documentation and `specs/` contains dated specs and plans for future
projects created from the skeleton.
