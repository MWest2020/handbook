# agent-memory Specification

## Purpose
Keep the coordinating session's memory durable, version-controlled and
leak-free: backed up privately, split by sensitivity, never to a public repo.
## Requirements
### Requirement: Agent memory is backed up privately and split by sensitivity

The coordinating session's memory SHALL be backed up under version control to
`private-only` repos exclusively, split by sensitivity: sensitive homelab and
topology context to `zettelkast`, working preferences to `dotfiles`. It SHALL
never go to a public repo. The canonical source remains the local memory
directory; the repo copies are the backup.

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
