# agent-registry Specification

## Purpose
One canonical definition per agent role, in the handbook, with two facets (chat
and execution) — so that ratatoskr and habitat consume the same source instead
of each keeping a copy, and so that tools, model and skills are machine-checked
rather than merely declared.
## Requirements
### Requirement: Execution seeds are derived from the canonical source

The execution roles SHALL live canonically in `docs/agents/seeds/<role>.md` and
be derived byte-identically per spoke (`scripts/gen_agent_seeds.py`, with
`--check` as the drift gate). Alongside `tools:`, a seed SHALL also declare
`model:` and `skills:` in its front matter, so that the worker can read them
from the role file in the target repo without having to fetch the registry.

#### Scenario: Drift is caught

- **WHEN** a per-spoke `.claude/agents/<role>.md` deviates from the canonical seed
- **THEN** `gen_agent_seeds.py --check` fails

#### Scenario: The worker can read model and skills

- **WHEN** a run starts in a target repo
- **THEN** model and skills are present in that repo's `.claude/agents/<role>.md`, derived from the canonical seed

### Requirement: Facets declare tools (allow/deny) and skills explicitly

Every non-empty facet of an agent definition SHALL explicitly declare `model`,
`tools.allow`, `tools.deny` and `skills` in its front matter, where
`tools.deny` and `skills` may be empty and `allow` and `deny` may not overlap.
`model` SHALL be one of `haiku`, `sonnet` or `opus` — the *intent* (search,
think, exception), not an exact model id, so that a model release does not
expire every definition. For an execution facet with a seed,
`executie.tools.allow` SHALL equal that seed's `tools:` line, and
`executie.model` its `model:` line. A gate in the handbook pipeline
(`handbook.yml`) SHALL fail the pull request on a missing field, an unknown
model, an allow/deny overlap, or a divergence between definition and seed.

#### Scenario: A read-only role is machine-checkable

- **WHEN** a reviewer or security definition declares `tools.deny: [Write, Edit]` and the seed allows only `Read, Bash, Grep, Glob`
- **THEN** the gate passes, and a seed that added `Write` would fail it on the allow/seed mismatch

#### Scenario: A missing field is caught

- **WHEN** a facet exists but does not declare `model`, `tools` or `skills`
- **THEN** the gate fails naming the missing field, so that "forgotten" does not quietly pass as "no restriction", "no skills" or "the default model"

#### Scenario: Model and seed do not diverge

- **WHEN** an execution facet declares `model: sonnet` while its seed says `model: haiku`
- **THEN** the gate fails, because the worker reads the role file in the target repo and would otherwise run on a different model than the registry promises

#### Scenario: Empty is a valid, explicit choice

- **WHEN** a chat facet grants no tools (`allow: []`), denies none and needs no skills
- **THEN** `tools.allow: []`, `tools.deny: []` and `skills: []` are valid and the gate passes — empty means an explicit "none", not "unknown"

### Requirement: Skills are validated against the skill register

Every `skills:` entry in an agent facet SHALL exist as a promoted skill in the
skill register (`inventory/skills-register.yml`, a mirror of skill-forge's
`forge register` output); the gate `check_agent_tools.py` SHALL fail (exit 1)
on an unknown skill, and equally on a non-empty `skills:` while the register is
absent (validation is then impossible); the CI step that runs the gate is wired
in by Mark by hand (CI config is a human gate). An empty `skills: []` SHALL
always pass.

#### Scenario: A valid skill

- **WHEN** an agent definition declares `skills: [thinking-red-team]` and that slug is in the register
- **THEN** the gate passes

#### Scenario: An unknown skill

- **WHEN** an agent definition declares a skill that is not in the register
- **THEN** the gate fails with the unknown slug and the reason (not promoted in skill-forge)

#### Scenario: The register is absent

- **WHEN** a definition has a non-empty `skills:` but the register file is missing
- **THEN** the gate fails (validation impossible), while an empty `skills: []` does pass

### Requirement: One canonical definition per agent role

Every agent role SHALL have exactly one canonical definition, in the handbook
under `docs/agents/<name>.md`; no other place (spoke seeds, ratatoskr config)
SHALL redefine a role — those consume the canonical source.

#### Scenario: A change reaches everyone

- **WHEN** the definition of a role (`bouwer`, say) changes in the handbook
- **THEN** every consumer (ratatoskr chat, habitat execution) reads that changed
  definition, without a copy having to be updated by hand

#### Scenario: No second truth

- **WHEN** someone tries to establish a role somewhere other than
  `docs/agents/` as its source
- **THEN** under this contract that is not a valid source; that place should
  point at, or derive from, the canonical definition

### Requirement: Two facets in one definition

A definition SHALL contain machine-readable front matter with at least `naam`
and `npub`, plus a **chat facet** (system prompt + channel scope) and an
**execution facet** (cage role, tools, schema — or explicitly empty). A
consumer SHALL use only its own facet.

#### Scenario: Ratatoskr reads the chat facet

- **WHEN** the ratatoskr listener runs an agent
- **THEN** it takes the system prompt and channel scope from the chat facet of
  the canonical definition, not from a copy of its own

#### Scenario: Chat-only or execution-only

- **WHEN** a role is chat only (assistent) or execution only (security)
- **THEN** the other facet is explicitly empty, and the definition stays valid

### Requirement: MCP-readable without new machinery

The definitions SHALL be readable through the existing `handbook_mcp` tool
`read_doc` (path `docs/agents/**/*.md`), so that any agent can request the
canonical source; this change SHALL require no new MCP tool and no loosening of
a guard.
