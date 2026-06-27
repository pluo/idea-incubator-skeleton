# Idea Incubator Skeleton Dev

This repository develops `idea-incubator-skeleton/`, a copyable Git repository skeleton for
idea-first projects.

The skeleton is for early-stage ideas that may later become research projects,
code projects, public products, or archived lines of thought. It preserves
public-safe provenance from day one while keeping private AI session notes out
of Git history.

## Intended Use

Use `idea-incubator-skeleton/` as a copyable template directory:

```sh
cp -R idea-incubator-skeleton/. /path/to/new-project/
```

After copying, initialize or continue Git in the destination project as needed.
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
