---
description: Records the decision to name the public GitHub project idea-repo-skeleton.
created: 2026-06-27
---

# Decision: Name the Project idea-repo-skeleton

## Decision

Name the public GitHub project `idea-repo-skeleton`.

## Context

This project is intended to become public, so the name should be easy to
understand and easy to find on GitHub.

The project is a reusable repo skeleton for idea-first projects. It helps
preserve public-safe provenance from the first intuition through notes,
AI-assisted sessions, decisions, specs, research, and optional implementation.

The initial naming ideas were more creative, but less self-explanatory. The
final direction favored clarity and searchability over novelty.

## Options Considered

- `idea-repo-skeleton`: direct, searchable, and easy to understand.
- `idea-provenance-template`: more precise about history, but less obvious.
- `public-idea-skeleton`: highlights public-first intent, but less Git-specific.
- `ai-idea-repo-template`: clear about AI assistance, but too narrow.
- `idea-to-repo-template`: friendly lifecycle framing, but less direct.

## Rationale

`idea-repo-skeleton` is plain, but that is the point. It contains the most useful
search terms and quickly tells readers what the project is.

It also avoids making the project sound only about AI, only about public
publishing, or only about provenance. The name leaves room for the broader
workflow: ideas, sessions, decisions, specs, research, and eventual code.

## Consequences

- The public repository should be named `idea-repo-skeleton`.
- Public documentation should use `idea-repo-skeleton` as the project name.
- The current local development repository can remain `repo-skeleton-dev` as the
  development workspace unless it is renamed later.
- Future naming choices should favor clarity and searchability over novelty.
