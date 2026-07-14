# Spec-delta: handbook-mcp

## ADDED Requirements

### Requirement: Eén waarheid

De MCP-server SHALL de importlijst afleiden uit `inventory/repos.json` op de
default branch van het handbook-repo — dezelfde bron als de site-build. Repos
buiten die lijst (of zonder `handbook_import: yes` + `contract_applied: yes`)
SHALL NOT benaderbaar zijn via de tools.

#### Scenario: Niet-geïmporteerd repo

- WHEN `list_docs` of `read_doc` wordt aangeroepen voor een repo dat niet in
  de importlijst staat
- THEN weigert de server met een foutmelding die het repo niet verder ontsluit

### Requirement: Padbegrenzing

`read_doc` SHALL uitsluitend genormaliseerde paden accepteren die met
`docs/` beginnen en op `.md` eindigen; paden met `..`, absolute paden of
paden buiten `docs/` SHALL worden geweigerd vóór enige fetch.

#### Scenario: Pad-traversal

- WHEN `read_doc(repo, "docs/../.mcp.json")` of een absoluut pad wordt gevraagd
- THEN weigert de server zonder netwerkverkeer

### Requirement: Token-hygiëne

De server SHALL NOT credentials bevatten in code, configuratie of
`.mcp.json`. Een optioneel `GH_TOKEN` uit de procesomgeving mag alleen als
Authorization-header worden gebruikt en SHALL NOT voorkomen in tool-output,
logging of foutmeldingen.

#### Scenario: Fout bij private fetch

- WHEN een fetch naar een privaat repo faalt (geen of ongeldig token)
- THEN bevat de foutmelding geen token(fragment), alleen status en pad

### Requirement: Read-only

Alle tools SHALL uitsluitend lezen; de server SHALL geen tool aanbieden die
een repository, bestand of externe staat muteert.

#### Scenario: Toolinventaris

- WHEN een client `tools/list` doet
- THEN bevat het resultaat uitsluitend lees-tools (list_repos, list_docs,
  read_doc)
