---
description: Records the two-track model for private and public AI session notes.
created: 2026-06-27
---

# Decision: Separate Private and Public AI Session Notes

## Decision

Use a two-track session model.

Private session notes can preserve richer AI-assisted working context. Public
session notes are explicit, curated, sanitized derivatives intended for
publishable Git history.

## Context

AI conversations often contain useful project context: early intuition,
alternatives, tradeoffs, rejected paths, and rationale. That context can explain
why a project developed the way it did.

Raw or private sessions may also contain noise, sensitive details, personal
context, local-only information, or reasoning artifacts that should not become
part of a public repository.

Because this project is designed so the same Git history can later be published,
session handling needs to preserve useful provenance without contaminating
public history.

## Options Considered

- Commit raw AI sessions directly.
- Keep all AI session notes outside the repository.
- Commit only short public summaries and discard richer working context.
- Keep private working notes separately and create public summaries only when
  explicitly requested.

## Rationale

The two-track model best balances provenance and safety.

Private notes preserve enough working context to support future continuation and
reflection. Public notes preserve the parts that help readers understand intent,
tradeoffs, decisions, and outcomes.

This keeps the public repository useful without requiring raw private sessions
to become part of permanent Git history.

## Consequences

- Private session notes must remain outside public Git history.
- Public session notes should be created only through explicit user intent.
- Public session notes should summarize useful context, not dump transcripts.
- Public summaries must omit sensitive, personal, local-only, or noisy details.
- The repository remains publishable without rewriting history.
