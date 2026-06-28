# Idea Incubator Skeleton Design

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
idea-incubator-skeleton-dev/
  idea-incubator-skeleton/
```

A user can start a future project by copying the contents of `idea-incubator-skeleton/`
into a new repository. This keeps the skeleton portable and transparent without
requiring an installer script or GitHub template repository.

The outer repository, `idea-incubator-skeleton-dev`, is the development project for the
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
idea-incubator-skeleton-dev/
  README.md
  specs/
    YYMMDD-idea-incubator-skeleton-design.md
    YYMMDD-idea-incubator-skeleton-implementation-plan.md

  idea-incubator-skeleton/
    ...
```

Inside the copyable template:

```text
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
  private/
```

## Template Structure

The agreed template structure is:

```text
idea-incubator-skeleton/
  AGENTS.md
  CLAUDE.md
  .gitignore
  README.md

  docs/
    workflow.md
    public-provenance.md
    current-feature-doc-template.md

  ideas/
    YYMMDD-idea-template.md

  sessions/
    YYMMDD-topic-session-template.md
    YYMMDD-topic-private-session-template.md

  decisions/
    000-decision-template.md

  specs/
    YYMMDD-feature-design-template.md

  research/
    YYMMDD-research-template.md

  private/
    YYMMDD-topic-private-session.md
```

`AGENTS.md` is the canonical agent instruction file. `CLAUDE.md` should be a
symlink to `AGENTS.md` so Claude Code and Codex share the same rules without
drift.

`.gitignore` inside the copyable template must ignore `private/` and its
contents so copied projects inherit the private-workspace boundary directly.

All notes, documentation, sessions, decisions, specs, research, and in-place
templates inside the skeleton are Markdown files.

## Public-First Provenance Model

The skeleton is public-first because the exact Git repository may be published
later. Therefore, anything committed to Git must be suitable for public history.

Historical provenance folders generally use `YYMMDD-` filename prefixes:

- `ideas/`
- `sessions/`
- `specs/`
- `research/`
- `private/`

Decision records are the exception. They use ordered numeric prefixes such as
`001-`, `002-`, and `003-`, with `000-decision-template.md` reserved as the
template.

The date prefix signals that these files are historical records. Agents and
humans should prefer creating a newer dated note, superseding an older note, or
cross-linking to updated context instead of heavily rewriting old provenance.
For decisions, preserve history by appending the next numbered record instead of
renumbering or heavily rewriting older decisions.

Current-state documentation belongs in `docs/` and does not use date prefixes.

## Private Workspace Boundary

`private/` is a local-only workspace for private AI session notes and related
working context. It must be ignored by Git.

The copyable template includes its own `.gitignore` with `private` and
`private/**` rules. The outer `idea-incubator-skeleton-dev` repository also ignores
`idea-incubator-skeleton/private` so development of the template has the same guardrail.

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

Session filenames should not include the agent identity. Record the agent or
tool identity in YAML frontmatter inside the Markdown file instead. Public
session frontmatter should omit `model`; private session frontmatter may keep
`model` and a URL-like `permalink` containing the agent session id.

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
- `decisions/` records durable numbered decision points, especially when
  direction changes.
- `specs/` records dated design specs and implementation plans.
- `docs/` records current, up-to-date project documentation.
- `research/` records dated supporting investigation and findings.
- `src/` is reserved for later implementation so code can appear without
  restructuring the repository.

## In-Place Templates

The skeleton should include lightweight Markdown templates inside the folders
where future notes will live:

- `docs/current-feature-doc-template.md`: current documentation template without
  a date prefix.
- `ideas/YYMMDD-idea-template.md`: initial intuition, context, why now, possible
  directions, and open questions.
- `sessions/YYMMDD-topic-session-template.md`: public-safe session summary,
  initial intuition, useful context, decision points, tradeoffs, artifacts, and
  omitted-private-details statement.
- `sessions/YYMMDD-topic-private-session-template.md`: tracked public-safe
  template for private notes that should be copied into ignored `private/`
  before use.
- `decisions/000-decision-template.md`: decision, context, options
  considered, rationale, consequences, and optional non-empty relationship
  links.
- `specs/YYMMDD-feature-design-template.md`: goal, context, scope, non-goals,
  design, acceptance criteria, and implementation notes.
- `research/YYMMDD-research-template.md`: question, observations, findings,
  implications, and follow-ups.

Decision notes should include a `## Links` section only when there are real
relationships to record, such as superseding or being superseded by another
decision.

Template filenames include `template` so they are not confused with real
historical records. Actual dated notes should be created by copying a template,
renaming it, and updating its frontmatter and body.

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
