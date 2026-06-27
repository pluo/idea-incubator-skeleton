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

Keep `.gitignore` configured to ignore `private` and `private/**`. Do not remove
that rule when adapting this skeleton.

In-place template files include `template` in the filename so they are not
confused with real historical records. Historical project notes inside `ideas/`,
`sessions/`, `specs/`, `research/`, and `private/` use `YYMMDD-` prefixes.
Decision records are the exception: use ordered numeric prefixes such as `001-`,
`002-`, and `003-`.

In YAML frontmatter, `description` is not the title. The Markdown H1 is the
title. Keep `description` to 20 words or fewer and use it to summarize what the
document is.

In decision notes, include a `## Links` section only when there are real
relationships to record. If present, include only non-empty relationship bullets
such as `Supersedes:` or `Superseded by:`.

Keep decision notes brief and future-proof. Emphasize the high-level decision
and durable rationale first. Avoid overfitting the note to technical details,
file paths, implementation mechanics, or temporary tooling choices that are
likely to change.

## Private Workspace Rules

- `private/` is never committed.
- If `private/` is a symlink, the symlink itself remains ignored.
- Agents may create private Markdown session notes automatically under
  `private/` using `YYMMDD-topic-private-session.md` filenames.
- Private session notes should be reflective records written to the user, from
  the user's perspective. Use "I" for the user in private notes; do not use
  "the user" to refer to the owner except in quoted text. Reserve "the user"
  for public session summaries.
- Private notes should foreground how the user prompted, corrected,
  challenged, redirected, changed the trajectory, and made decisions with the
  agent. They should not read like neutral summaries of model outputs.
- Private notes may include honest personal context, challenges, experience,
  lessons learned, and candid agent observations about the user's prompting and
  decision-making behavior. Keep that feedback direct, specific, and useful;
  avoid flattery, defensiveness, or vague praise.
- Private notes should still remove irrelevant turns, credentials, auth
  material, exact account identifiers, unnecessary personal details that do not
  help future continuation, and anything the user marked sensitive.
- Agents must not stage, commit, quote from, or link to private notes from
  tracked files unless the user explicitly requests a sanitized public
  derivative.

## Public Session Rules

- Create files under `sessions/` only when the user explicitly asks for a public
  session note.
- Public session notes are curated summaries, not raw transcript dumps.
- Session filenames do not include the agent identity. Record the agent or tool
  identity in YAML frontmatter inside the Markdown file.
- Public session notes should use third-person language. Refer to the owner as
  "the user" rather than "I".
- Public notes should foreground the user's initial intuition, prompting
  trajectory, constraints, corrections, redirections, decision points,
  selected direction, tradeoffs, resulting artifacts, and next steps.
- Public notes should not include candid private observations about the user's
  prompting behavior, personal challenges, or improvement suggestions. Keep
  those in private session notes only.
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
