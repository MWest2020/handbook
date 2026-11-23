# Habitat reads the roles from the handbook

## Why

Mark, 2026-10-25: *"i think the cleanest is all looks at the handbook and
there is where we have or index our agents and skills? consumed by habitat
for whatever project?"*

The registry already says it is the single source, but the execution roles
reached habitat through copies: `gen_agent_seeds.py` wrote byte-identical
seeds into `prep/seeds/<spoke>/.claude/agents/` (19 spokes), and nothing
carried those into the spoke repositories. Habitat read each target repo's own
`.claude/agents/<role>.md`, so the copies that mattered drifted: wordsworth's
and convergence's builder, reviewer and security differ from the canonical
seeds, and convergence runs an `architect` that has no seed here at all.

Habitat can now fetch the seed itself (habitat #44): `HABITAT_HANDBOOK_REF`
pins a handbook commit, the worker reads
`docs/agents/seeds/<role>.md` at that commit, and fails closed when it cannot.
With that, copies have no job left.

## What changes

- **The worker reads the seed from the handbook**, at a pinned commit, instead
  of from the target repo. The requirement that seeds are derived into every
  spoke is replaced by that.
- **`prep/seeds/` and `scripts/gen_agent_seeds.py` are removed**, with the CI
  drift step that ran the generator.
- **An `architect` seed** is added (`docs/agents/seeds/architect.md`), and
  `docs/agents/architect.md` points its execution facet at it, so a chain that
  starts with the architect can run with the pin set.
- **`docs/agents/index.md`** says how habitat reads the roles, and what Bash
  means in the cage (habitat's per-role settings are the enforcement).

## Out of scope

- An execution facet for `ontwerper` (designer): it needs a habitat role,
  settings and an output schema first.
- Removing the per-repo `.claude/agents/` copies in the spokes: that follows
  once the pin is set in the factory and a chain has run on it.
- An ecosystem MCP beyond `handbook_mcp`.
