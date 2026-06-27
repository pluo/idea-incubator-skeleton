# Repo Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `repo-skeleton/` into a copyable, public-first Git repository template for idea-first projects with ignored local private AI session space.

**Architecture:** The outer `repo-skeleton-dev` repository contains development records for the template. The inner `repo-skeleton/` directory is the copyable template and contains only public-safe tracked files. The template uses Markdown-first documentation, dated provenance folders with in-place templates, current-state `docs/`, and a Git-ignored `private/` attachment point that may be a local folder or symlink.

**Tech Stack:** Git, Markdown, POSIX shell commands, symlinks, `.gitignore`.

---

## File Structure

Create or modify these files in `/Users/peluo/repos/repo-skeleton-dev`:

- Modify: `.gitignore` to explicitly ignore `repo-skeleton/private` as both a directory and a symlink.
- Create: `README.md` to explain that this repository develops a copyable template directory.
- Create: `repo-skeleton/.gitignore` so copied projects inherit the `private/` ignore rule.
- Create: `repo-skeleton/AGENTS.md` as the canonical rules file for all agents.
- Create: `repo-skeleton/CLAUDE.md` as a symlink to `AGENTS.md`.
- Create: `repo-skeleton/README.md` as the public entry point copied into future projects.
- Create: `repo-skeleton/docs/workflow.md` for current workflow guidance.
- Create: `repo-skeleton/docs/public-provenance.md` for the public-history model.
- Create: in-place Markdown template files in `repo-skeleton/docs/`, `repo-skeleton/ideas/`, `repo-skeleton/sessions/`, `repo-skeleton/decisions/`, `repo-skeleton/specs/`, and `repo-skeleton/research/` so Git preserves those documentation/provenance directories.
- Do not create a separate `repo-skeleton/templates/` directory.

`repo-skeleton/private/` must not be committed. The implementation may verify ignore behavior using `git check-ignore` without creating a private file.

### Task 1: Outer Repo Documentation And Ignore Boundary

**Files:**
- Modify: `.gitignore`
- Create: `README.md`
- Create: `repo-skeleton/.gitignore`

- [ ] **Step 1: Verify starting state**

Run:

```bash
git status --short
test -d repo-skeleton
test ! -e repo-skeleton/private
test ! -L repo-skeleton/private
```

Expected:

```text
git status --short prints nothing.
All test commands exit 0.
```

- [ ] **Step 2: Add private-workspace ignore rules**

Edit `.gitignore` by adding these lines under the `s3` section:

```gitignore

# repo-skeleton local private workspace; keep untracked even when it is a symlink
repo-skeleton/private
repo-skeleton/private/**
```

- [ ] **Step 3: Create the outer README**

Create `README.md` with this content:

````markdown
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
    .gitignore
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
````

- [ ] **Step 4: Create the template ignore file**

Create `repo-skeleton/.gitignore` with this content:

```gitignore
# Local private workspace; keep untracked even when it is a symlink
private
private/**
```

- [ ] **Step 5: Verify ignore behavior without creating private files**

Run:

```bash
git check-ignore -v repo-skeleton/private repo-skeleton/private/260626-private-session.md
git -C repo-skeleton check-ignore -v private private/260626-private-session.md
```

Expected output includes matching lines from the outer `.gitignore` for
`repo-skeleton/private` paths and matching lines from `repo-skeleton/.gitignore`
for copied-template `private` paths.

- [ ] **Step 6: Verify formatting**

Run:

```bash
git diff --check
git status --short
```

Expected:

```text
git diff --check prints nothing.
git status --short shows README.md, .gitignore, and repo-skeleton/.gitignore changed or untracked.
```

- [ ] **Step 7: Commit**

Run:

```bash
git add README.md .gitignore repo-skeleton/.gitignore
git commit -m "Document copyable skeleton usage"
```

Expected: commit succeeds and includes only `README.md`, `.gitignore`, and
`repo-skeleton/.gitignore`.

### Task 2: Agent Rules And Claude Compatibility

**Files:**
- Create: `repo-skeleton/AGENTS.md`
- Create symlink: `repo-skeleton/CLAUDE.md -> AGENTS.md`

- [ ] **Step 1: Verify no existing agent files would be replaced**

Run:

```bash
test ! -e repo-skeleton/AGENTS.md
test ! -L repo-skeleton/AGENTS.md
test ! -e repo-skeleton/CLAUDE.md
test ! -L repo-skeleton/CLAUDE.md
```

Expected: all commands exit 0.

- [ ] **Step 2: Create canonical agent rules**

Create `repo-skeleton/AGENTS.md` with this content:

```markdown
# Agent Instructions

This repository is public-history-first. Assume the exact Git repository and
commit history may be published later.

## Operating Model

- Follow explicit user instructions first, then this file, then broader agent
  guidance.
- Keep changes scoped, reversible, and public-safe.
- Use Markdown for documentation, notes, sessions, decisions, specs, research,
  and templates.
- Before editing a local path, check whether it is a symlink and preserve the
  symlink unless the user explicitly asks to replace it.
- Before committing, run `git status --short` and verify that no private files
  or private symlink targets are staged.

## Folder Roles

- `docs/`: current, up-to-date documentation. Files do not use date prefixes.
- `ideas/`: dated public-safe idea notes using `YYMMDD-short-slug.md`.
- `sessions/`: dated public-safe AI session summaries using
  `YYMMDD-topic-session.md`, plus tracked in-place templates.
- `decisions/`: numbered decision records using `001-short-slug.md`,
  `002-short-slug.md`, and so on. `000-decision-template.md` is the template.
- `specs/`: dated specs and implementation plans using `YYMMDD-short-slug.md`.
- `research/`: dated research notes using `YYMMDD-short-slug.md`.
- `src/`: optional implementation code when the project reaches that stage.
- `private/`: ignored local-only private workspace. It may be a real directory
  or a symlink to an external private store.

In-place template files include `template` in the filename so they are not
confused with real historical records. Historical project notes inside `ideas/`,
`sessions/`, `specs/`, `research/`, and `private/` use `YYMMDD-` prefixes.
Decision records are the exception: use ordered numeric prefixes such as `001-`,
`002-`, and `003-`.

## Private Workspace Rules

- `private/` is never committed.
- If `private/` is a symlink, the symlink itself remains ignored.
- Agents may create private Markdown session notes automatically under
  `private/` using `YYMMDD-topic-private-session.md` filenames.
- Private notes should still remove irrelevant turns, credentials, auth
  material, exact account identifiers, unnecessary personal details, and
  anything the user marked sensitive.
- Agents must not stage, commit, quote from, or link to private notes from
  tracked files unless the user explicitly requests a sanitized public
  derivative.

## Public Session Rules

- Create files under `sessions/` only when the user explicitly asks for a public
  session note.
- Public session notes are curated summaries, not raw transcript dumps.
- Session filenames do not include the agent identity. Record the agent or tool
  identity in YAML frontmatter inside the Markdown file.
- Public notes should preserve the initial intuition, useful context,
  alternatives considered, decision points, selected direction, tradeoffs,
  resulting artifacts, and next steps.
- Public notes must omit credentials, auth material, account identifiers,
  private contact details, unnecessary personal information, sensitive local
  paths, non-public business information, raw private transcripts, hidden
  reasoning, irrelevant model or tool internals, and anything the user marked
  sensitive.
- If content might not be public-safe, leave it out or ask the user.

## Commit Checklist

Before each commit:

1. Run `git status --short`.
2. Run `git diff --check`.
3. Confirm no `repo-skeleton/private` path is staged.
4. If committing a public session note, do a sanitization review against this
   file.
5. Commit only public-safe tracked files.
```

- [ ] **Step 3: Create Claude Code symlink**

Run:

```bash
ln -s AGENTS.md repo-skeleton/CLAUDE.md
```

Expected: command exits 0.

- [ ] **Step 4: Verify symlink and Git visibility**

Run:

```bash
test -L repo-skeleton/CLAUDE.md
readlink repo-skeleton/CLAUDE.md
git status --short repo-skeleton/AGENTS.md repo-skeleton/CLAUDE.md
```

Expected:

```text
readlink prints AGENTS.md.
git status shows AGENTS.md and CLAUDE.md as untracked.
```

- [ ] **Step 5: Verify formatting**

Run:

```bash
git diff --check
```

Expected: no output.

- [ ] **Step 6: Commit**

Run:

```bash
git add repo-skeleton/AGENTS.md repo-skeleton/CLAUDE.md
git commit -m "Add skeleton agent rules"
```

Expected: commit succeeds and tracks `CLAUDE.md` as a symlink.

### Task 3: Template Entry Point And Current Documentation

**Files:**
- Create: `repo-skeleton/README.md`
- Create: `repo-skeleton/docs/workflow.md`
- Create: `repo-skeleton/docs/public-provenance.md`

- [ ] **Step 1: Create template README**

Create `repo-skeleton/README.md` with this content:

````markdown
# Project Name

This repository starts from an idea-first skeleton. It is designed to preserve
public-safe provenance from early thinking through later research, specs,
decisions, and optional implementation.

## How To Use This Repository

- Capture public-safe initial thoughts in `ideas/`.
- Keep private AI session notes in ignored `private/`.
- Create public AI session summaries in `sessions/` only when explicitly
  requested.
- Record durable numbered decisions in `decisions/`.
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
````

- [ ] **Step 2: Create workflow documentation**

Create `repo-skeleton/docs/workflow.md` with this content:

````markdown
# Workflow

This project is idea-first. It can remain a thinking archive, grow into research,
or become an implementation project without changing its core structure.

## Lifecycle

```text
idea capture -> private AI work -> public session summary -> decision record -> specs/plans -> docs/research/prototype/code
```

## Current Documentation

Use `docs/` for current, up-to-date explanations of the project. Files in this
folder do not need date prefixes because they describe the current state.

## Historical Records

Use these Markdown filename conventions for historical records:

- `ideas/YYMMDD-short-slug.md`
- `sessions/YYMMDD-topic-session.md`
- `decisions/001-short-slug.md`
- `specs/YYMMDD-short-slug.md`
- `research/YYMMDD-short-slug.md`

Prefer creating a newer dated record or linking to current docs instead of
heavily rewriting old historical notes.
````

- [ ] **Step 3: Create public provenance documentation**

Create `repo-skeleton/docs/public-provenance.md` with this content:

```markdown
# Public Provenance

This repository is designed so its Git history can become public without
rewriting history.

## Public By Default

Tracked files must be safe for public readers. Public files may include
intentions, design alternatives, decision points, tradeoffs, and implementation
rationale.

## Private Work

Private AI session notes belong in ignored `private/`. That path can be a local
folder or a symlink to an external private store. It is not part of public Git
history.

## Public Session Notes

Public session notes in `sessions/` are created only when explicitly requested.
They should summarize useful context without exposing raw private transcripts,
credentials, account details, unnecessary personal information, or sensitive
local context.
```

- [ ] **Step 4: Verify docs are Markdown**

Run:

```bash
find repo-skeleton -path repo-skeleton/private -prune -o -type f -print
```

Expected: output includes `repo-skeleton/README.md`,
`repo-skeleton/docs/workflow.md`, and `repo-skeleton/docs/public-provenance.md`.

- [ ] **Step 5: Verify formatting**

Run:

```bash
git diff --check
```

Expected: no output.

- [ ] **Step 6: Commit**

Run:

```bash
git add repo-skeleton/README.md repo-skeleton/docs/workflow.md repo-skeleton/docs/public-provenance.md
git commit -m "Add skeleton documentation"
```

Expected: commit succeeds and includes only the template README and current docs.

### Task 4: In-Place Markdown Templates

**Files:**
- Create: `repo-skeleton/docs/current-feature-doc-template.md`
- Create: `repo-skeleton/ideas/YYMMDD-idea-template.md`
- Create: `repo-skeleton/sessions/YYMMDD-topic-session-template.md`
- Create: `repo-skeleton/sessions/YYMMDD-topic-private-session-template.md`
- Create: `repo-skeleton/decisions/000-decision-template.md`
- Create: `repo-skeleton/specs/YYMMDD-feature-design-template.md`
- Create: `repo-skeleton/research/YYMMDD-research-template.md`

- [ ] **Step 1: Create current documentation template**

Create `repo-skeleton/docs/current-feature-doc-template.md` with this content:

```markdown
---
title: Current Feature Documentation
status: current
---

# Current Feature Documentation

## Purpose

Describe the current behavior, workflow, or architecture in public-safe language.

## How It Works

Explain the current state readers should rely on.

## Related Historical Records

- Idea:
- Session:
- Decision:
- Spec:
```

- [ ] **Step 2: Create idea template**

Create `repo-skeleton/ideas/YYMMDD-idea-template.md` with this content:

```markdown
---
date: YYMMDD
status: draft
---

# Idea: Short Title

## Initial Intuition

Describe the idea in public-safe language.

## Context

Explain what prompted the idea and why it matters now.

## Possible Directions

- Direction one
- Direction two
- Direction three

## Open Questions

- Question one
- Question two
```

- [ ] **Step 3: Create public session template**

Create `repo-skeleton/sessions/YYMMDD-topic-session-template.md` with this content:

```markdown
---
date: YYMMDD
topic: short-topic
agent:
visibility: public
---

# Public Session: Short Title

## Initial Intuition

Describe the public-safe idea or question that started the session.

## Useful Context

Summarize context that helps public readers understand the work.

## Alternatives Considered

- Alternative one
- Alternative two
- Alternative three

## Decision Points

- Decision point one
- Decision point two

## Selected Direction

State the direction chosen during the session.

## Tradeoffs

- Tradeoff one
- Tradeoff two

## Resulting Artifacts

- Artifact one
- Artifact two

## Omitted Private Details

This note is a curated public summary. Raw private transcripts, sensitive local
context, credentials, account details, unnecessary personal information, and
non-public business information are omitted.
```

- [ ] **Step 4: Create private session template inside sessions**

Create `repo-skeleton/sessions/YYMMDD-topic-private-session-template.md` with this content:

```markdown
---
date: YYMMDD
topic: short-topic
agent:
visibility: private
intended_path: private/YYMMDD-topic-private-session.md
---

# Private Session: Short Title

Copy this template into ignored `private/` before using it for a real private
session note. Do not commit filled private session notes.

## User Goal

Record the user's goal for this session.

## Cleaned Private Context

Keep useful private context after removing irrelevant turns and sensitive
material that should not be retained.

## Session Summary

Summarize the useful reasoning and exploration.

## Alternatives Considered

- Alternative one
- Alternative two
- Alternative three

## Decisions

- Decision one
- Decision two

## Unresolved Concerns

- Concern one
- Concern two

## Follow-Ups

- Follow-up one
- Follow-up two
```

- [ ] **Step 5: Create decision template**

Create `repo-skeleton/decisions/000-decision-template.md` with this content:

```markdown
---
date: YYMMDD
status: active
---

# Decision: Short Title

## Decision

State the decision directly.

## Context

Explain the situation that required a decision.

## Options Considered

- Option one
- Option two
- Option three

## Rationale

Explain why this option was chosen.

## Consequences

- Consequence one
- Consequence two

## Links

- Supersedes:
- Superseded by:
```

- [ ] **Step 6: Create design spec template**

Create `repo-skeleton/specs/YYMMDD-feature-design-template.md` with this content:

```markdown
---
date: YYMMDD
status: draft
---

# Feature Design: Short Title

## Goal

State what this design is trying to achieve.

## Context

Explain the relevant background.

## Scope

- Included item one
- Included item two

## Non-Goals

- Excluded item one
- Excluded item two

## Design

Describe the intended structure, behavior, and interfaces.

## Acceptance Criteria

- Criterion one
- Criterion two

## Implementation Notes

Record constraints, sequencing notes, and verification expectations.
```

- [ ] **Step 7: Create research template**

Create `repo-skeleton/research/YYMMDD-research-template.md` with this content:

```markdown
---
date: YYMMDD
status: draft
---

# Research: Short Title

## Question

State the research question.

## Observations

- Observation one
- Observation two

## Findings

- Finding one
- Finding two

## Implications

Explain what the findings change about the project.

## Follow-Ups

- Follow-up one
- Follow-up two
```

- [ ] **Step 8: Verify in-place templates**

Run:

```bash
find repo-skeleton -path repo-skeleton/private -prune -o -type f -name '*template.md' -print | sort
```

Expected output:

```text
repo-skeleton/decisions/000-decision-template.md
repo-skeleton/docs/current-feature-doc-template.md
repo-skeleton/ideas/YYMMDD-idea-template.md
repo-skeleton/research/YYMMDD-research-template.md
repo-skeleton/sessions/YYMMDD-topic-private-session-template.md
repo-skeleton/sessions/YYMMDD-topic-session-template.md
repo-skeleton/specs/YYMMDD-feature-design-template.md
```

- [ ] **Step 9: Verify no separate templates directory exists**

Run:

```bash
test ! -e repo-skeleton/templates
```

Expected: command exits 0.

- [ ] **Step 10: Verify formatting**

Run:

```bash
git diff --check
```

Expected: no output.

- [ ] **Step 11: Commit**

Run:

```bash
git add repo-skeleton/docs/current-feature-doc-template.md repo-skeleton/ideas/YYMMDD-idea-template.md repo-skeleton/sessions/YYMMDD-topic-session-template.md repo-skeleton/sessions/YYMMDD-topic-private-session-template.md repo-skeleton/decisions/000-decision-template.md repo-skeleton/specs/YYMMDD-feature-design-template.md repo-skeleton/research/YYMMDD-research-template.md
git commit -m "Add in-place skeleton templates"
```

Expected: commit succeeds and includes the seven in-place template files.

### Task 5: Final Verification

**Files:**
- Verify: `.gitignore`
- Verify: `repo-skeleton/`
- Verify: Git index

- [ ] **Step 1: Verify private path remains ignored**

Run:

```bash
git check-ignore -v repo-skeleton/private repo-skeleton/private/260626-private-session.md
git -C repo-skeleton check-ignore -v private private/260626-private-session.md
```

Expected output includes outer `.gitignore` matches for the `repo-skeleton/private`
paths and `repo-skeleton/.gitignore` matches for copied-template `private` paths.

- [ ] **Step 2: Verify Claude symlink**

Run:

```bash
test -L repo-skeleton/CLAUDE.md
readlink repo-skeleton/CLAUDE.md
git ls-files -s repo-skeleton/CLAUDE.md
```

Expected:

```text
readlink prints AGENTS.md.
git ls-files mode for repo-skeleton/CLAUDE.md starts with 120000.
```

- [ ] **Step 3: Verify tracked files are public-safe paths**

Run:

```bash
git ls-files | sort
```

Expected: output includes public template files and does not include any path
starting with `repo-skeleton/private`.

- [ ] **Step 4: Verify Markdown-only documentation under the template**

Run:

```bash
find repo-skeleton -path repo-skeleton/private -prune -o -type f -print | sort
```

Expected: every printed template documentation, guide, and template file ends in
`.md`; `repo-skeleton/CLAUDE.md` is a symlink to `AGENTS.md`.

- [ ] **Step 5: Verify clean Git state**

Run:

```bash
git diff --check
git status --short
```

Expected:

```text
git diff --check prints nothing.
git status --short prints nothing.
```

- [ ] **Step 6: Inspect recent commits**

Run:

```bash
git log --oneline --decorate --max-count=8
```

Expected: recent commits show the implementation commits for outer docs,
agent rules, template docs, and in-place templates.
