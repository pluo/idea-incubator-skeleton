---
description: Public session summary for designing and shipping the idea-incubator installer.
created: 2026-06-28
agent: Codex
---

# Public Session: Designing And Shipping The Idea Incubator Installer

## Initial Intuition

The user wanted a more convenient way to start a new local project from
`idea-incubator-skeleton/`. The existing copyable-template model was transparent
and portable, but still required too many repeated manual steps: copy the
skeleton, create the destination folder, initialize Git, stage files, and make
the first commit.

The user specifically wanted the workflow to be frictionless enough to operate
from the ChatGPT Codex app on an iPhone.

## Useful Context

The project already had a public-first Markdown skeleton with a deliberate
private workspace boundary. The template lived under
`idea-incubator-skeleton/`, and prior design work had chosen a copyable
directory over an installer to keep the structure simple and inspectable.

This session revisited that distribution decision from a workflow perspective:
the skeleton should remain transparent, but starting a new project should become
nearly one command.

## How The User Steered The Session

- The user began by asking for installation options that would be convenient
  from Codex on iPhone.
- The user named possible directions: an agent skill, a reusable deterministic
  script, or another low-friction approach.
- The user asked for the top three options rather than immediate
  implementation.
- After comparing options, the user selected the deterministic script installer
  as the first step.
- The user answered the decisive design questions: default destinations should
  go under `~/repos/`, the script should still accept an explicit destination,
  the initial commit message should be `Initialize idea incubator project`, and
  the copied skeleton should remain generic.
- The user approved the design and requested a committed spec plus an
  implementation plan.
- The user chose the subagent-driven execution approach after the plan was
  written.
- After the pull request was raised, the user asked for the PR to be approved
  and merged automatically.

## Alternatives Considered

- A deterministic installer script with a thin Codex wrapper.
- A user-level Codex skill such as `$new-idea-incubator`.
- A more productized plugin, local Codex action, or deep-link flow.

The recommended path was to build the deterministic script first and later wrap
it with a skill or plugin if the workflow proved stable.

## Decision Points

- Build `scripts/new-idea-incubator.py` first, rather than starting with a
  skill or plugin.
- Resolve bare names under `~/repos/`.
- Treat explicit paths as exact destinations.
- Refuse to overwrite existing destinations.
- Preserve `CLAUDE.md -> AGENTS.md` while copying the skeleton.
- Initialize Git immediately on `main`.
- Stage and commit the generic copied skeleton with
  `Initialize idea incubator project`.
- Leave project identity customization out of the deterministic script.
- Use subagent-driven implementation with task-level review gates.

## Selected Direction

The selected direction was a deterministic Python installer with focused tests
and README documentation.

The script resolves the skeleton source relative to its own file location,
copies the template while preserving symlinks, checks Git and explicit Git
identity before copying, initializes a fresh Git repository, and creates the
first commit. The script keeps copied content generic so it can be launched from
a prompt or from a purely mechanical workflow.

## Tradeoffs

- A script is less conversational than a skill, but it is easier to test and
  reason about.
- Keeping the copied content generic avoids guessing user intent, but it leaves
  README and idea-note customization for a later step.
- Preflighting Git identity adds a stricter prerequisite, but prevents a copied
  destination with no initial commit and avoids accidental machine-local public
  history.
- A plugin or Codex deep link could make the workflow smoother later, but would
  add packaging surface before the behavior had stabilized.

## Resulting Artifacts

- `specs/260628-idea-incubator-installer-design.md`
- `specs/260628-idea-incubator-installer-implementation-plan.md`
- `scripts/new-idea-incubator.py`
- `tests/test_new_idea_incubator.py`
- Updated installer usage in `README.md`
- Pull request `#1`, merged into `main`

## Execution Summary

The implementation used a linked worktree on branch
`idea-incubator-installer`. Subagents added tests, implemented the script,
documented usage, and reviewed each stage for spec compliance and code quality.

Review caught two important retry-safety gaps:

- the script originally checked for `git` only after copying the skeleton;
- the script later needed stricter handling for blank or partial Git identity
  environment variables.

Both issues were fixed before merge. The final implementation had 15 unit tests
covering path resolution, destination refusal, symlink preservation, ignored
noise, Git command order, Git executable preflight, Git identity preflight,
Git failure wrapping, source-relative execution, and end-to-end temporary
installs.

The PR was marked ready and merged. GitHub rejected same-account self-approval,
so approval could not be recorded, but the PR was merged through the GitHub API.

## Omitted Private Details

This note is a curated public summary. Raw private transcripts, hidden
reasoning, sensitive local details, account tokens, unnecessary personal
information, candid private observations, and private working notes are omitted.

## Follow-Ups

- Decide whether to add a Codex skill wrapper around the deterministic script.
- Decide whether to add a local Codex action or deep link for iPhone launch.
- Optionally document Git identity prerequisites in the README.
- Clean up the local feature worktree and branch if no longer needed.
