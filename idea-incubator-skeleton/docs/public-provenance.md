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
