# Ecosystem MCP, read-only first

## Why

`handbook_mcp` today reads only the docs of the imported repos
(`list_repos`, `list_docs`, `read_doc`). Agents and sessions that want to know
who a role is, what the factory is doing, or what is in the wordsworth dossiers
have to go to other places, by hand. `roles-read-from-handbook` left
"an ecosystem MCP beyond `handbook_mcp`" explicitly out of scope; this is that
step, taken small.

Mark agreed by mail with the ecosystem MCP: *extend handbook_mcp, read-only
first.* The decision was relayed in the channel by the orchestrator.

## What changes

`handbook_mcp` gets read tools in three groups. Nothing else about it changes.

- **Roles and skills.** Look up an agent role from `docs/agents/` (its
  definition and facets) and a skill from the skills register
  (`inventory/skills-register.yml`, the mirror of skill-forge's catalogue).
- **Factory status.** Build queue, running chains, boards and the API ledger
  total, read from ratatoskr's state files. Read only; nothing is written back.
- **Wordsworth dossier search.** Search through wordsworth's API.
- **No write tools.** The server still offers no tool that mutates anything.
- **Tests per tool**, in the existing MCP session test, and **a how-to**.

## Out of scope

- Any write or dispatch tool (queueing a build, pinging, editing a board).
  Read-only is the decision; writes would be a separate proposal.
- Reading wordsworth documents themselves; the decision names search.

## Open questions

These were not decided in the channel. None is a requirement until answered.

1. **Where ratatoskr's state files are, and how the server reaches them.** The
   server runs over stdio on the caller's machine (`uvx`). Whether it reads a
   local path (and which, set how) or fetches from somewhere is not decided.
   What happens when the files are absent is also open.
2. **The wordsworth API: endpoint, credential and what a hit returns.**
   Dossiers are sensitive. Credentials must come from the environment (the
   existing token-hygiene rule). Whether results carry titles and topic only,
   or excerpts, is open.
3. **Tool names and result shapes** for the three groups.
4. **Whether the factory status tool shows the API ledger total only** or
   also a breakdown; the decision says "total".
