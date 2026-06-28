---
description: Public session summary for developing the idea-incubator-skeleton project.
created: 2026-06-27
agent: Codex
---

# Public Session: Developing idea-incubator-skeleton

## Initial Intuition

The user wanted a reusable Git repository skeleton for early-stage ideas. The
goal was not to start with a code scaffold, but to preserve the path from an
initial intuition through AI-assisted exploration, decision-making, research,
specs, and possible implementation.

The user also wanted the resulting repository to be publishable from day one,
so the same Git history could later serve as public provenance for the idea.

## Useful Context

The project was designed as a public-first idea incubator. It needed to support
uncertain early ideas that might become software projects, public products,
research directions, or archived explorations.

The central tension was preserving rich development context without exposing
private working notes, raw AI conversations, sensitive local details, or
unnecessary personal information.

## How The User Steered The Session

- The user began with a broad request for a universal, future-proof repo
  skeleton that could preserve brainstorming, AI sessions, decision points, and
  later implementation context.
- The user clarified that public and private areas should exist from day one,
  with private notes ignored and public notes sanitized.
- The user simplified the folder structure by shortening public sessions to
  `sessions/` and private notes to `private/`.
- The user pushed the design away from tool-specific assumptions and toward a
  portable Markdown-first structure usable across multiple agents and editors.
- The user rejected placeholder folder README files and chose in-place
  templates instead.
- The user simplified YAML frontmatter and clarified that `description` is
  metadata, while the Markdown H1 remains the title.
- The user changed decision records from dated filenames to numbered records.
- The user repeatedly asked for decision notes to be brief, high-level, and
  resistant to future implementation churn.
- The user directed the project name discussion toward a balance of
  searchability, clarity, and distinctiveness, then selected
  `idea-incubator-skeleton`.
- The user later revisited the name, identified possible confusion between
  "idea repo" and IntelliJ IDEA, and chose `idea-incubator-skeleton` as the
  clearer public name.

## Alternatives Considered

- A tool-specific structure versus a portable repo skeleton.
- Public raw transcripts versus curated public session summaries.
- Tracking private context in Git versus keeping private notes ignored.
- A central templates directory versus in-place templates inside each note
  family.
- Dated decision records versus numbered decision records.
- Creative project names versus a plain, searchable GitHub repository name.
- The earlier searchable name versus `idea-incubator-skeleton` after the
  IntelliJ IDEA ambiguity became clear.

## Decision Points

- Build the project as a public-first idea incubation skeleton.
- Keep private AI session notes separate from public session summaries.
- Use Markdown files for docs, ideas, sessions, decisions, specs, research, and
  templates.
- Keep `AGENTS.md` as the canonical agent instruction file and symlink
  `CLAUDE.md` to it.
- Use dated filenames for ideas, sessions, specs, research, and private notes.
- Use numbered filenames for decision records.
- Keep current-state documentation under `docs/` and dated implementation
  plans under `specs/`.
- Name the public project `idea-incubator-skeleton`.
- Rename the copyable template directory to `idea-incubator-skeleton/`.

## Selected Direction

The selected direction is a copyable, Markdown-first repository skeleton for
early-stage ideas. It keeps public provenance and private working context
separate while allowing future implementation work to grow with minimal
restructure.

The skeleton includes folders for public docs, ideas, sessions, decisions,
specs, research, optional implementation code, and ignored private notes.

## Tradeoffs

- Public history is more credible when it starts early, but it requires
  stronger sanitation rules.
- Private notes can preserve richer context, but they must stay outside public
  Git history.
- In-place templates make each folder's intended use concrete, but template
  filenames must clearly indicate that they are templates.
- Numbered decision records are easier to read as a stable decision sequence,
  but they are less directly chronological than dated note families.
- `idea-incubator-skeleton` is slightly longer than the earlier name, but it is
  less ambiguous for developer readers.

## Resulting Artifacts

- A public Git repository named `idea-incubator-skeleton`.
- A copyable template directory under `idea-incubator-skeleton/`.
- Agent rules for public/private session handling, decision note brevity, and
  Markdown-first documentation.
- A `CLAUDE.md` symlink to `AGENTS.md`.
- In-place Markdown templates for docs, ideas, public sessions, private session
  notes, decisions, specs, and research.
- Public decision records covering the project origin, project name, and
  public/private session split.

## Omitted Private Details

This note is a curated public summary. Raw private transcripts, sensitive local
context, credentials, account details, unnecessary personal information, candid
private observations, and improvement suggestions are omitted.

## Follow-Ups

- Review and refine the public session template.
- Review this public session note before committing it.
- Continue documenting only durable decisions as numbered decision records.
- Review other templates in detail before treating the skeleton as ready for
  public reuse.
