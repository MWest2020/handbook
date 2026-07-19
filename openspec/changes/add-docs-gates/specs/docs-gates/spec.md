# Spec-delta: docs-gates (add-docs-gates)

## ADDED Requirements

### Requirement: Contract-gate draait in de spoke-PR

Elk repo op de importlijst (`handbook_import: yes`) SHALL het docs-contract
valideren als check op zijn eigen pull requests, met dezelfde checker die de
hub gebruikt (aangeroepen via de reusable workflow van de hub, niet als
kopie). De hub-CI en de nightly rebuild blijven als vangnet bestaan.

#### Scenario: Contractbreuk in een spoke-PR

- WHEN een spoke-PR een docs-pagina toevoegt of wijzigt die het contract
  schendt (geen front matter, markdown buiten de Diátaxis-mappen)
- THEN faalt de contract-gate in díe PR, vóór merge

#### Scenario: Checker wijzigt bij de hub

- WHEN de hub de contract-checker aanscherpt
- THEN geldt de aanscherping bij de eerstvolgende spoke-PR zonder dat een
  spoke iets hoeft bij te werken

### Requirement: Drift-gate koppelt code aan docs

Een spoke-PR die geconfigureerde code-paden raakt SHALL falen wanneer
`docs/**` niet in dezelfde PR meebeweegt, tenzij de PR een expliciete,
zichtbare override draagt (label `docs-drift-ok`). De gate SHALL
padgebaseerd en deterministisch zijn (geen inhoudsanalyse). Spokes MAY de
gate op `warn` zetten tijdens inregelen; de standaard is `fail`.

#### Scenario: Code wijzigt, docs niet

- WHEN een PR paden uit `code_paths` wijzigt en geen bestand onder `docs/`
- THEN faalt de drift-gate met een melding die naar de meebeweeg-afspraak
  verwijst

#### Scenario: Bewuste uitzondering

- WHEN dezelfde PR het label `docs-drift-ok` draagt
- THEN slaagt de drift-gate en blijft de uitzondering als label zichtbaar en
  telbaar in de PR-historie
