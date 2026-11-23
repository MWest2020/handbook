# Ecosystem MCP, read-only first

## Why

`handbook_mcp` today reads only the docs of the imported repos
(`list_repos`, `list_docs`, `read_doc`). Agents and sessions that want to know
who a role is, or which skill exists, have to go to other places, by hand.
`roles-read-from-handbook` left "an ecosystem MCP beyond `handbook_mcp`"
explicitly out of scope; this is that step, taken small.

Mark agreed by mail with the ecosystem MCP: *extend handbook_mcp, read-only
first.* The decision was relayed in the channel by the orchestrator.

## What changes

`handbook_mcp` gets read tools for roles and skills. Nothing else about it
changes.

- **Roles and skills.** Look up an agent role from `docs/agents/` (its
  definition and facets) and a skill from the skills register
  (`inventory/skills-register.yml`, the mirror of skill-forge's catalogue).
  The role lookup mostly overlaps `read_doc('handbook', 'docs/agents/<name>.md')`;
  it adds only name resolution and the unknown-name refusal. The skill lookup
  is the new ground, because the path guard blocks `inventory/`.
- **No widening of `_guard_path`.** Nobody may widen it to cover the skills
  register; the skill lookup reads that one fixed file itself.
- **No write tools.** The server still offers no tool that mutates anything.
- **Tests per tool**, in the existing MCP session test, asserting existence
  and structure only (for a role: the `## Mandate` heading is present; for a
  skill: the slug is present), not wording.
- **A how-to**, which also says the tool is not an identity or authorisation
  source (the closed-npub rule lives in the registry guardrails).

## Narrowed: follow-up changes

The architect passed tasks 1.x (role and skill lookup), 4.x (tool inventory)
and 5.x (docs). The other two groups move to follow-up changes, because
`handbook_mcp` only reads github.com through `_fetch`/`_guard_repo` and has no
access path to ratatoskr's state files or wordsworth's API:

- **Factory status** (build queue, running chains, boards, API ledger total,
  read from ratatoskr's state files): a follow-up change.
- **Wordsworth dossier search** (through wordsworth's API): a follow-up change.

Both keep the decision "read-only first" and need the access path settled
there. They are not requirements of this change.

## Out of scope

- Factory status and wordsworth dossier search (follow-up changes, above).
- Any write or dispatch tool (queueing a build, pinging, editing a board).
  Read-only is the decision; writes would be a separate proposal.
- Widening `_guard_path` or `read_doc` to reach `inventory/`.

## Open questions

These were not decided in the channel. None is a requirement until answered.

1. **Tool names and result shapes** for the role and skill lookups.
2. **For the follow-ups:** how the server reaches ratatoskr's state files and
   wordsworth's API (local path or fetch, credential, what a hit returns).
   Settled in those changes, not here.
