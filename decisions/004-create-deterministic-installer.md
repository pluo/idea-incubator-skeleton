---
description: Records the decision to add a deterministic installer script.
created: 2026-06-28
---

# Decision 4: Create a Deterministic Installer

## Decision

Create a deterministic installer script for starting new projects from
`idea-incubator-skeleton/`.

The installer should make a copied skeleton immediately usable as a local Git
repository while keeping the copied content generic.

## Context

The skeleton began as a copyable template directory. That kept the project
transparent and portable, but it still required repeated manual setup each time
a new idea project was started.

The intended workflow includes operating from Codex on mobile, where minimizing
manual steps matters. A reusable installer also gives future Codex skills,
plugins, local actions, or deep links a stable command to call instead of
reimplementing copy and Git behavior in prompts.

## Options Considered

- Keep only the manual copy command.
- Create a Codex skill that performs the whole setup conversationally.
- Create a plugin, local action, or deep-link flow first.
- Create a deterministic installer script first, then wrap it later if useful.

## Rationale

The deterministic script is the right first layer because it is testable,
repeatable, and independent of any one agent surface.

The script can safely handle the mechanical work: resolve the destination, copy
the skeleton while preserving symlinks, initialize Git, stage the generic
files, and create the first commit. A future skill or plugin can then focus on
user interaction and call the script rather than duplicating setup logic.

Keeping project identity customization out of the installer avoids guessing
context when the script is launched without a rich prompt.

## Consequences

- Bare destination names should default under `~/repos/`.
- Explicit destination paths should remain supported.
- The installer should refuse existing destinations instead of merging or
  overwriting.
- The copied skeleton should remain generic until the user customizes it.
- Git setup should happen immediately, including the first commit.
- Future skill, plugin, action, or deep-link workflows should treat the
  installer as the deterministic setup primitive.
