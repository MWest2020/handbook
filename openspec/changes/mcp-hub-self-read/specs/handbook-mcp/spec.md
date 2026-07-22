# Spec-delta: handbook-mcp (mcp-hub-self-read)

## MODIFIED Requirements

### Requirement: Eén waarheid

De MCP-server SHALL de importlijst afleiden uit `inventory/repos.json` op de
default branch van het handbook-repo — dezelfde bron als de site-build — en
SHALL daarnaast de hub (`handbook`) zelf ontsluiten als expliciete
uitzondering: `handbook_import`/`contract_applied` blijven site-semantiek en
de hub-rij houdt `handbook_import: no` (de site importeert zichzelf niet).
Andere repos buiten die lijst (of zonder `handbook_import: yes` +
`contract_applied: yes`) SHALL NOT benaderbaar zijn via de tools.

#### Scenario: Niet-geïmporteerd repo

- WHEN `list_docs` of `read_doc` wordt aangeroepen voor een repo dat niet in
  de importlijst staat en niet de hub is
- THEN weigert de server met een foutmelding die het repo niet verder ontsluit

#### Scenario: Hub-docs leesbaar

- WHEN `list_repos`, `list_docs("handbook")` of
  `read_doc("handbook", "docs/index.md")` wordt aangeroepen
- THEN staat de hub in de repolijst en leveren de leestools zijn
  `docs/**/*.md` zoals bij elke spoke, binnen dezelfde padbegrenzing
