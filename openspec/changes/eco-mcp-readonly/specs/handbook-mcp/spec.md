## MODIFIED Requirements

### Requirement: Read-only

All tools SHALL read only; the server SHALL offer no tool that mutates a
repository, a file or any external state. This includes the tools that read
roles and skills.

#### Scenario: Tool inventory

- WHEN a client calls `tools/list`
- THEN the result contains read tools only (list_repos, list_docs, read_doc and
  the role and skill lookup tools)

## ADDED Requirements

### Requirement: Role and skill lookup

The server SHALL offer read tools that return an agent role from
`docs/agents/` and a skill from `inventory/skills-register.yml`, from the
handbook's default branch. The skill lookup SHALL take a skill name, not a
path, and SHALL NOT widen the path bound of `read_doc`: `read_doc` still
refuses `inventory/`.

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

#### Scenario: The register is not reachable through read_doc

- WHEN `read_doc("handbook", "inventory/skills-register.yml")` is requested
- THEN the server refuses, as before this change
