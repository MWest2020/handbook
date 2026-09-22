# handbook-mcp Specification

## Purpose
Read-only MCP access to the ecosystem's content layer: agents read the docs of
every imported spoke repo and of the hub itself, from one truth (the
inventory), within tight path and token boundaries.
## Requirements
### Requirement: One truth

The MCP server SHALL derive the import list from `inventory/repos.json` on the
handbook repo's default branch — the same source the site build uses — and
SHALL additionally expose the hub (`handbook`) itself as an explicit exception:
`handbook_import` and `contract_applied` keep their site semantics and the hub
row keeps `handbook_import: no` (the site does not import itself). Other repos
outside that list (or without `handbook_import: yes` and
`contract_applied: yes`) SHALL NOT be reachable through the tools.

#### Scenario: A repo that is not imported

- WHEN `list_docs` or `read_doc` is called for a repo that is not on the import
  list and is not the hub
- THEN the server refuses with an error that does not disclose anything further
  about the repo

#### Scenario: Hub docs are readable

- WHEN `list_repos`, `list_docs("handbook")` or
  `read_doc("handbook", "docs/index.md")` is called
- THEN the hub appears in the repo list and the read tools deliver its
  `docs/**/*.md` as they would for any spoke, within the same path bounds

### Requirement: Path bounding

`read_doc` SHALL accept only normalised paths that begin with `docs/` and end
in `.md`; paths containing `..`, absolute paths, or paths outside `docs/` SHALL
be refused before any fetch.

#### Scenario: Path traversal

- WHEN `read_doc(repo, "docs/../.mcp.json")` or an absolute path is requested
- THEN the server refuses without any network traffic

### Requirement: Token hygiene

The server SHALL NOT contain credentials in code, in configuration or in
`.mcp.json`. An optional `GH_TOKEN` from the process environment may be used
only as an Authorization header and SHALL NOT appear in tool output, logging or
error messages.

#### Scenario: A failed private fetch

- WHEN a fetch to a private repo fails (no token, or an invalid one)
- THEN the error message contains no token or fragment of one, only a status
  and a path

### Requirement: Read-only

All tools SHALL read only; the server SHALL offer no tool that mutates a
repository, a file or any external state.

#### Scenario: Tool inventory

- WHEN a client calls `tools/list`
- THEN the result contains read tools only (list_repos, list_docs, read_doc)
