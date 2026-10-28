# Design: eco-mcp-readonly

## Choices

- **Extend `handbook_mcp`, do not add a second server.** Mark's decision.
  One server, one `.mcp.json` entry for every spoke.
- **Read-only, enforced by the tool inventory.** The existing "Read-only"
  requirement stays and the `tools/list` scenario is extended to the new
  tools, so a write tool shows up as a failing test.
- **Roles and skills come from the handbook's own files.** The role definition
  from `docs/agents/`, the skill from `inventory/skills-register.yml`. Both are
  already the single source (agent-registry), so the tool adds no second copy.
- **Factory status is read from ratatoskr's state files**, not from a new
  ratatoskr endpoint. This keeps the change inside the handbook; ratatoskr is
  not touched.
- **Wordsworth through its API**, not its database or files, so wordsworth's
  own access rules apply. The credential comes from the environment only.
- **New tool text is English** (repo invariant). The existing Dutch docstrings
  are not touched by this change.

## Rejected alternatives

- **A separate ecosystem MCP server.** Rejected by the decision to extend
  `handbook_mcp`.
- **Write tools in the first version** (queue a build, move a card). Rejected:
  "read-only first".
- **A new status API in ratatoskr.** More surface and a change in another repo
  for something the state files already hold.

## Risks

- State file formats belong to ratatoskr and can change under the tool. Tests
  therefore use fixture files, and the format questions are open (see the
  proposal).
- Dossier search returns data from a sensitive system; what it returns is an
  open question, and the server must never log or echo the credential.
