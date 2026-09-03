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

### Requirement: Facetten declareren tools (allow/deny) en skills expliciet

Elk niet-leeg facet van een agent-definitie SHALL in het front-matter expliciet `tools.allow`, `tools.deny` en `skills` declareren, waarbij `tools.deny` en `skills` leeg mogen zijn en `allow` en `deny` niet mogen overlappen. Voor een executie-facet met een seed SHALL `executie.tools.allow` gelijk zijn aan de `tools:`-regel van die seed. Een gate in de handbook-pipeline (`handbook.yml`) SHALL de PR laten falen bij een ontbrekend veld, een allow/deny-overlap of een afwijking tussen `allow` en de seed.

#### Scenario: Read-only rol is machine-checkbaar

- **WHEN** een reviewer- of security-definitie `tools.deny: [Write, Edit]` declareert en de seed enkel `Read, Bash, Grep, Glob` toestaat
- **THEN** slaagt de gate, en zou een seed die `Write` toevoegt de gate laten falen op de allow/seed-mismatch

#### Scenario: Ontbrekend veld wordt gevangen

- **WHEN** een facet wél bestaat maar `tools` of `skills` niet declareert
- **THEN** faalt de gate met een verwijzing naar het ontbrekende veld, zodat "vergeten" niet stil als "geen beperking" of "geen skills" doorgaat

#### Scenario: Leeg is een geldige, expliciete keuze

- **WHEN** een chat-facet geen tools verleent (`allow: []`) en geen tools weigert en geen skills nodig heeft
- **THEN** zijn `tools.allow: []`, `tools.deny: []` en `skills: []` geldig en slaagt de gate — leeg betekent expliciet "geen", niet "onbekend"

### Requirement: Skills worden gevalideerd tegen het skill-register

Elke `skills:`-entry in een agent-facet SHALL bestaan als gepromoveerde skill in het skill-register (`inventory/skills-register.yml`, een mirror van skill-forge's `forge register`-uitvoer); de gate `check_agent_tools.py` SHALL falen (exit 1) bij een onbekende skill, en ook bij een niet-lege `skills:` terwijl het register ontbreekt (dan kan niet worden gevalideerd); de CI-stap die de gate draait wordt door Mark met de hand ingehaakt (CI-config is een human-gate). Een lege `skills: []` SHALL altijd slagen.

#### Scenario: Geldige skill

- **WHEN** een agent-def `skills: [thinking-red-team]` declareert en die slug in het register staat
- **THEN** slaagt de gate

#### Scenario: Onbekende skill

- **WHEN** een agent-def een skill declareert die niet in het register staat
- **THEN** faalt de gate met de onbekende slug en de reden (niet gepromoveerd in skill-forge)

#### Scenario: Register ontbreekt

- **WHEN** een def een niet-lege `skills:` heeft maar het register-bestand ontbreekt
- **THEN** faalt de gate (kan niet valideren), terwijl een lege `skills: []` wel slaagt

