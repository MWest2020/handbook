## REMOVED Requirements

### Requirement: Execution seeds are derived from the canonical source

**Reason**: the copies it derived (`prep/seeds/`) never reached the spokes, and the spokes' own copies drifted.
**Migration**: habitat reads the seed from the handbook at a pinned commit (the requirement below).

## ADDED Requirements

### Requirement: Habitat reads execution seeds from the handbook

The execution roles SHALL live canonically in `docs/agents/seeds/<role>.md`.
Habitat SHALL read a role's seed from the handbook at a pinned commit
(`HABITAT_HANDBOOK_REF`), not from a copy in the target repository, and SHALL
fail closed when the pinned seed cannot be read. Alongside `tools:`, a seed
SHALL also declare `model:` and `skills:` in its front matter, so that the
worker can read them from the seed it fetched.

#### Scenario: A pinned seed is used

- **WHEN** a habitat run starts with `HABITAT_HANDBOOK_REF` set
- **THEN** the role file is `docs/agents/seeds/<role>.md` at that commit, and
  any `.claude/agents/<role>.md` in the target repo is not used

#### Scenario: A missing seed stops the run

- **WHEN** the pinned commit has no seed for the role
- **THEN** the run stops with an error and does not fall back to a repo copy

#### Scenario: The worker can read model and skills

- **WHEN** a run starts
- **THEN** model and skills are read from the front matter of the fetched seed
