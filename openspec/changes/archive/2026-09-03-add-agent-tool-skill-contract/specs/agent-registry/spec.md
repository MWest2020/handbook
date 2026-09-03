## ADDED Requirements

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
