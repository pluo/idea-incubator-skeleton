# Repo Skeleton Dev

This repository develops `repo-skeleton/`, a copyable Git repository skeleton for
idea-first projects.

The skeleton is for early-stage ideas that may later become research projects,
code projects, public products, or archived lines of thought. It preserves
public-safe provenance from day one while keeping private AI session notes out
of Git history.

## Intended Use

Use `repo-skeleton/` as a copyable template directory:

```sh
cp -R repo-skeleton/. /path/to/new-project/
```

After copying, initialize or continue Git in the destination project as needed.
The copied project should be publishable with its Git history intact, because
private notes are kept in an ignored `private/` attachment point.

## Repository Layout

```text
repo-skeleton-dev/
  README.md
  specs/
    YYMMDD-repo-skeleton-design.md
    YYMMDD-repo-skeleton-implementation-plan.md

  repo-skeleton/
    AGENTS.md
    CLAUDE.md -> AGENTS.md
    README.md
    docs/
    ideas/
    sessions/
    decisions/
    specs/
    research/
```

`repo-skeleton-dev/specs/` contains dated design records and implementation
plans for developing this template. Inside the template, `docs/` contains
current documentation and `specs/` contains dated specs and plans for future
projects created from the skeleton.
