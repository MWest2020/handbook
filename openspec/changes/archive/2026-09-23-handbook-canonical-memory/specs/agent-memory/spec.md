# Spec delta: agent-memory (handbook-canonical-memory)

## MODIFIED Requirements

### Requirement: Agent memory is backed up privately and split by sensitivity

The coordinating session's memory SHALL be backed up under version control to
`private-only` repos exclusively, split by sensitivity: sensitive homelab and
topology context to `zettelkast`, working preferences to `dotfiles`. It SHALL
never go to a public repo. The local memory directory is canonical only for
what it is still allowed to hold (see "Memory routes to the handbook"); the
repo copies are the backup.

#### Scenario: A new, unclassified memory file

- WHEN a memory file is not on the explicit preferences allowlist
- THEN it goes to the sensitive repo (`zettelkast`), not to `dotfiles`
  (fail-closed: unknown counts as sensitive)

#### Scenario: The target repo is not private

- WHEN a sync target does not have `PRIVATE` visibility
- THEN the sync aborts without pushing (no memory to a public repo)

#### Scenario: No change since the previous sync

- WHEN the canonical memory is unchanged relative to the backup
- THEN the sync pushes nothing (idempotent)

## ADDED Requirements

### Requirement: Memory routes to the handbook

Working agreements that apply across repos SHALL live in the handbook
(`docs/reference/operating-agreements.md` or `AGENTS.md`), and project
knowledge SHALL live in the owning repo's `docs/`. Local agent memory SHALL
hold only what cannot be published — identity, the location of credentials
and keys, personal interaction preferences — plus one-line pointers to the
canonical page.

#### Scenario: A new cross-repo working rule

- WHEN the owner states a rule that applies beyond one repo
- THEN it is written into the handbook's operating agreements, and memory at
  most points there

#### Scenario: A new project gotcha

- WHEN a session learns something about one project that the next session
  would need
- THEN it goes into that repo's `docs/`, not into memory

#### Scenario: Memory and handbook disagree

- WHEN a memory entry contradicts the handbook
- THEN the handbook wins, and the memory entry is corrected or removed
