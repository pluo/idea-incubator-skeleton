# Project Name

This repository starts from an idea-first skeleton. It is designed to preserve
public-safe provenance from early thinking through later research, specs,
decisions, and optional implementation.

## How To Use This Repository

- Capture public-safe initial thoughts in `ideas/`.
- Keep private AI session notes in ignored `private/`.
- Create public AI session summaries in `sessions/` only when explicitly
  requested.
- Record durable decisions in `decisions/`.
- Put dated specs and implementation plans in `specs/`.
- Keep current project documentation in `docs/`.
- Add implementation code under `src/` when the project reaches that stage.

## Private Workspace

Create `private/` locally when needed, or make it a symlink to an external
private store. The path is ignored by Git and must not appear in public history.

## Copying This Skeleton

This repository can be created by copying the contents of a template directory:

```sh
cp -R repo-skeleton/. /path/to/new-project/
```

After copying, update this README with the project name and public overview.
