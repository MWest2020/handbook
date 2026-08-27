# agent-registry Specification

## Purpose
TBD - created by archiving change add-seed-derivation. Update Purpose after archive.
## Requirements
### Requirement: Executie-seeds zijn afgeleid van de canonieke bron

De per-spoke `.claude/agents/<rol>.md`-seeds SHALL door een generator worden
afgeleid van de executie-facet van de canonieke definitie in `docs/agents/`, en
SHALL nooit met de hand geschreven of gekopieerd worden. Een drift-gate in CI
SHALL falen als een gecommitte seed afwijkt van wat de generator uit de bron zou
produceren.

#### Scenario: Seed afwijking wordt gevangen

- **WHEN** een `.claude/agents/builder.md`-seed op een spoke afwijkt van de
  canonieke executie-facet van `bouwer`
- **THEN** faalt de drift-gate in CI en wordt de afwijking niet gemerged

#### Scenario: Wijziging aan de rol propageert via generatie

- **WHEN** de executie-facet van een rol in `docs/agents/` wijzigt
- **THEN** produceert de generator nieuwe seeds die alle spokes gelijk houden,
  in plaats van dat elke kopie met de hand bijgewerkt moet worden

#### Scenario: Habitat leest de afgeleide seed ongewijzigd

- **WHEN** een habitat-run een rol uitvoert
- **THEN** leest hij de seed lokaal uit de doelrepo zoals altijd; alleen de
  herkomst van die seed (afgeleid van de canonieke bron) is veranderd, niet de
  kooi of het leesmechanisme

