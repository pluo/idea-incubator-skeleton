# Repo Skeleton Design

Date: 2026-06-26
Status: Approved for implementation planning

## Purpose

This repository develops a copyable Git repository skeleton for idea-first projects.
The skeleton is for moments when an idea, intuition, or creative direction appears
before it is clear whether the work will become code, a product, a public project,
or only an archived line of thought.

The design goal is to preserve public-safe provenance from day one while allowing
private AI-assisted exploration to happen locally. The same Git repository and
history should be publishable later without rewriting history.

## Intended Use

The skeleton is intended to be used as a copyable template directory.

The canonical template lives in:

```text
repo-skeleton-dev/
  repo-skeleton/
```

A user can start a future project by copying the contents of `repo-skeleton/`
into a new repository. This keeps the skeleton portable and transparent without
requiring an installer script or GitHub template repository.

The outer repository, `repo-skeleton-dev`, is the development project for the
template itself. Its own `specs/` directory contains dated design records and
implementation plans for developing the skeleton.

## Folder Semantics

The outer development repo and the inner copyable template intentionally use
the same broad convention:

- `docs/` contains current, up-to-date documentation and does not use date
  prefixes.
- `specs/` contains dated specs, design records, implementation plans, and
  planning artifacts.

In this development repository:

```text
repo-skeleton-dev/
  README.md
  specs/
    YYMMDD-repo-skeleton-design.md
    YYMMDD-repo-skeleton-implementation-plan.md

  repo-skeleton/
    ...
```

Inside the copyable template:

```text
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
  src/
  templates/
  private/
```

## Template Structure

The agreed template structure is:

```text
repo-skeleton/
  AGENTS.md
  CLAUDE.md
  README.md

  docs/
    workflow.md
    public-provenance.md

  ideas/
    YYMMDD-short-idea-slug.md

  sessions/
    YYMMDD-agent-topic-session.md

  decisions/
    YYMMDD-short-decision-slug.md

  specs/
    YYMMDD-short-spec-or-plan-slug.md

  research/
    YYMMDD-short-research-slug.md

  src/

  templates/
    idea.md
    private-session.md
    public-session.md
    decision.md
    spec.md
    research.md

  private/
    YYMMDD-agent-topic-private-session.md
```

`AGENTS.md` is the canonical agent instruction file. `CLAUDE.md` should be a
symlink to `AGENTS.md` so Claude Code and Codex share the same rules without
drift.

All notes, documentation, sessions, decisions, specs, research, and templates
inside the skeleton are Markdown files.

## Public-First Provenance Model

The skeleton is public-first because the exact Git repository may be published
later. Therefore, anything committed to Git must be suitable for public history.

Historical provenance folders use `YYMMDD-` filename prefixes:

- `ideas/`
- `sessions/`
- `decisions/`
- `specs/`
- `research/`
- `private/`

The date prefix signals that these files are historical records. Agents and
humans should prefer creating a newer dated note, superseding an older note, or
cross-linking to updated context instead of heavily rewriting old provenance.

Current-state documentation belongs in `docs/` and does not use date prefixes.

## Private Workspace Boundary

`private/` is a local-only workspace for private AI session notes and related
working context. It must be ignored by Git.

The private workspace may be:

- a normal local folder inside the working tree, or
- a symlink to an external private store, such as a centralized private Git
  repository or private knowledge bank.

If `private/` is a symlink, the symlink itself must also remain ignored. Git must
not record the target path.

Agents may create private Markdown session notes automatically under `private/`.
Agents must not stage, commit, quote from, or link to private notes from tracked
files unless the user explicitly requests a sanitized public derivative.

## Public Session Rules

Public session notes live in `sessions/`.

Agents may create a public session note only when the user explicitly asks for
one. Public session notes are curated Markdown summaries, not raw transcript
dumps.

Public session notes should preserve:

- the initial intuition or user intent,
- useful public context,
- meaningful alternatives considered,
- decision points,
- selected direction,
- tradeoffs and rationale,
- resulting artifacts or next steps.

Public session notes must omit:

- credentials or auth material,
- account identifiers,
- private contact details,
- unnecessary personal information,
- local-only sensitive paths,
- non-public business information,
- raw private transcripts,
- hidden reasoning,
- irrelevant model or tool internals,
- anything the user marked sensitive.

When uncertain, agents must default to leaving content out of tracked files or
asking the user.

## Lifecycle

The skeleton supports an idea-first lifecycle:

```text
idea capture -> private AI work -> public session summary -> decision record -> specs/plans -> docs/research/prototype/code
```

The intended roles are:

- `ideas/` records public-safe initial intuitions.
- `private/` records richer private AI work and remains ignored.
- `sessions/` records public-safe summaries of AI-assisted sessions when
  explicitly requested.
- `decisions/` records durable decision points, especially when direction
  changes.
- `specs/` records dated design specs and implementation plans.
- `docs/` records current, up-to-date project documentation.
- `research/` records dated supporting investigation and findings.
- `src/` is reserved for later implementation so code can appear without
  restructuring the repository.

## Templates

The skeleton should include lightweight Markdown templates:

- `templates/idea.md`: initial intuition, context, why now, possible directions,
  and open questions.
- `templates/private-session.md`: user goal, cleaned private context, session
  summary, alternatives, decisions, unresolved concerns, and follow-ups.
- `templates/public-session.md`: public-safe session summary, initial intuition,
  useful context, decision points, tradeoffs, artifacts, and omitted-private
  details statement.
- `templates/decision.md`: decision, context, options considered, rationale,
  consequences, supersedes, and superseded-by links.
- `templates/spec.md`: goal, context, scope, non-goals, design, acceptance
  criteria, and implementation notes.
- `templates/research.md`: question, observations, findings, implications, and
  follow-ups.

## Verification And Commit Rules

Agents should follow these rules when working in a repo created from the
skeleton:

- Check whether `private/` is a symlink before editing it, and preserve the
  symlink.
- Confirm `.gitignore` ignores `private/` and its contents.
- Before each commit, run `git status --short` and verify no private files or
  private symlink targets are staged.
- Commit public skeleton and documentation changes after verification.
- Do not commit automatically generated private session notes.
- Before committing public session notes, perform a sanitization review against
  the rules in `AGENTS.md`.

## Non-Goals

This skeleton does not include an installer script in its first version.
It does not rely on the Superpowers plugin or any specific agent framework.
It does not assume every idea will become code.
It does not preserve private AI sessions in public Git history.
