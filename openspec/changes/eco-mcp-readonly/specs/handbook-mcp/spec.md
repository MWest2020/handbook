## MODIFIED Requirements

### Requirement: Read-only

All tools SHALL read only; the server SHALL offer no tool that mutates a
repository, a file or any external state. This includes the tools that read
roles, skills, factory status and wordsworth dossiers.

#### Scenario: Tool inventory

- WHEN a client calls `tools/list`
- THEN the result contains read tools only (list_repos, list_docs, read_doc and
  the role, skill, factory status and dossier search tools)

## ADDED Requirements

### Requirement: Role and skill lookup

The server SHALL offer read tools that return an agent role from
`docs/agents/` and a skill from `inventory/skills-register.yml`, from the
handbook's default branch.

#### Scenario: A known role

- WHEN the role lookup is called with the name of a role that has a file in
  `docs/agents/`
- THEN the role's definition is returned

#### Scenario: A known skill

- WHEN the skill lookup is called with a skill that is in the skills register
- THEN the register entry for that skill is returned

#### Scenario: An unknown role or skill

- WHEN the name matches no role file and no register entry
- THEN the server refuses with an error that names no other file

### Requirement: Factory status

The server SHALL offer a read tool that reports the factory's build queue,
running chains, boards and the API ledger total, read from ratatoskr's state
files. It SHALL NOT write to those files.

#### Scenario: Status is read

- WHEN the factory status tool is called and the state files are present
- THEN the result contains the build queue, the running chains, the boards and
  the API ledger total

#### Scenario: State files are absent

- WHEN the state files cannot be read
- THEN the tool reports that they are unavailable and does not return empty
  values as if they were current

### Requirement: Wordsworth dossier search

The server SHALL offer a read tool that searches wordsworth dossiers through
wordsworth's API. Any credential SHALL come from the process environment and
SHALL NOT appear in tool output, logging or error messages.

#### Scenario: A search

- WHEN the dossier search is called with a query
- THEN the results of wordsworth's API for that query are returned

#### Scenario: A failed call

- WHEN the API call fails (no credential, or an invalid one)
- THEN the error contains a status only, and no token or fragment of one
