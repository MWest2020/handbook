# Change: handbook-canonical-memory

## Why

The coordinating session's local memory had grown into a second handbook: 55
files, of which 20 were cross-repo working agreements and 10 were project
knowledge (runbooks, gotchas, architecture decisions) documented nowhere else.
Only the session on one machine could read them; habitat workers, other
sessions and humans could not. The index alone cost ~3k tokens in every
session, and the larger files were changelogs drifting away from the repos
they described.

It also contradicted the hub: `AGENTS.md` said "merging stays human" while the
memory said "work on main, finish everything, merge without asking" (Mark,
2026-09-19). Whichever text a session read first decided how it behaved.

Decision Mark (2026-09-23): the handbook is canonical; memory routes to it.

## What Changes

- **Working agreements** move into `docs/reference/operating-agreements.md`,
  the page every agent starting here already abides by.
- **Project knowledge** moves into the owning repo's `docs/` (the docs
  contract), which the handbook imports. The handbook keeps holding only the
  map.
- **Local memory** keeps only what is personal or secret-adjacent (identity,
  credential and key locations, interaction preferences) plus one-line
  pointers into the handbook or a repo's docs.
- **`AGENTS.md`** resolves the merge contradiction: interactive sessions work
  on main and finish the job; dispatched habitat roles still leave merging to
  a human; `docs/agents/` and `.claude/agents/` stay behind CODEOWNERS.
- **agent-memory spec**: the canonical source moves from the memory directory
  to the handbook and repo docs. The private backup requirement stays.

## Impact

- Affected specs: `agent-memory`
- Affected files: `AGENTS.md`, `docs/reference/operating-agreements.md`;
  docs pages in ratatoskr, homelab, wordsworth, skill-forge and Billbird.
