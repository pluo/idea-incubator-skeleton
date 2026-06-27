---
description: Records why this public-first idea incubation skeleton exists.
created: 2026-06-27
---

# Decision: Build a Public-First Idea Incubation Repo Skeleton

## Decision

Develop a reusable Git repository skeleton for
idea-first projects, with the explicit intent that the resulting workflow can be
made public and reused by others.

The skeleton should preserve public-safe evidence of how an idea begins,
develops, and matures through notes, AI-assisted sessions, decisions, specs,
research, and optional implementation.

## Context

Early ideas often appear before it is clear whether they will become code,
products, research threads, or archived thoughts. That early phase is still
valuable. It contains the original intuition, the surrounding context, the
alternatives considered, the AI-assisted exploration, and the decision points
that later explain why the project exists.

Without a deliberate structure, this material tends to be scattered across
private chats, local notes, temporary agent sessions, and implementation commits
that begin too late to capture the real origin of the work.

The goal of this project is to create a lightweight, portable repo skeleton that
can capture this provenance from day one while keeping the eventual Git history
safe to publish.

## Options Considered

- Keep early thinking in private notes or chats, then start a Git repo only when
  implementation begins.
- Use a conventional code-first repository layout and add idea notes later.
- Keep a private-only archive of raw AI sessions and reasoning artifacts.
- Build a public-first, idea-first skeleton that separates public provenance
  from ignored private working context.

## Rationale

The public-first, idea-first skeleton best matches the intended workflow.

It lets the repo preserve authorship, intent, and project history from the
earliest stage without requiring certainty that the idea will become software.
It also creates a disciplined pattern for AI-era project incubation: public
files can explain the development path, while raw or sensitive private session
material stays out of Git history.

Making the skeleton public is part of the point. The project is not only a
personal organization aid; it is also a reusable practice for showing how ideas,
AI conversations, decisions, and implementation can coexist in a publishable
repository.

## Consequences

- The repository must be safe to publish without rewriting history.
- Private AI session notes must remain ignored and must not be committed.
- Public notes should preserve meaningful intent, context, tradeoffs, and
  decisions without exposing raw private transcripts or sensitive details.
- The skeleton should stay simple enough to copy into future projects.
- Later implementation work should fit into the structure without forcing a
  major reorganization.
