## MODIFIED Requirements

### Requirement: Facetten declareren tools (allow/deny) en skills expliciet

Elk niet-leeg facet van een agent-definitie SHALL in het front-matter expliciet
`model`, `tools.allow`, `tools.deny` en `skills` declareren, waarbij `tools.deny`
en `skills` leeg mogen zijn en `allow` en `deny` niet mogen overlappen. `model`
SHALL één van `haiku`, `sonnet` of `opus` zijn — de *intentie* (zoeken, denken,
uitzondering), niet een exacte model-id, zodat een modelrelease niet elke
definitie laat verlopen. Voor een executie-facet met een seed SHALL
`executie.tools.allow` gelijk zijn aan de `tools:`-regel van die seed, en
`executie.model` aan de `model:`-regel van die seed. Een gate in de
handbook-pipeline (`handbook.yml`) SHALL de PR laten falen bij een ontbrekend
veld, een onbekend model, een allow/deny-overlap of een afwijking tussen def en
seed.

#### Scenario: Read-only rol is machine-checkbaar

- **WHEN** een reviewer- of security-definitie `tools.deny: [Write, Edit]` declareert en de seed enkel `Read, Bash, Grep, Glob` toestaat
- **THEN** slaagt de gate, en zou een seed die `Write` toevoegt de gate laten falen op de allow/seed-mismatch

#### Scenario: Ontbrekend veld wordt gevangen

- **WHEN** een facet wél bestaat maar `model`, `tools` of `skills` niet declareert
- **THEN** faalt de gate met een verwijzing naar het ontbrekende veld, zodat "vergeten" niet stil als "geen beperking", "geen skills" of "het standaardmodel" doorgaat

#### Scenario: Model en seed lopen niet uiteen

- **WHEN** een executie-facet `model: sonnet` declareert terwijl zijn seed `model: haiku` zegt
- **THEN** faalt de gate, want de worker leest het rolbestand in de doelrepo en zou anders op een ander model draaien dan de registry belooft

#### Scenario: Leeg is een geldige, expliciete keuze

- **WHEN** een chat-facet geen tools verleent (`allow: []`) en geen tools weigert en geen skills nodig heeft
- **THEN** zijn `tools.allow: []`, `tools.deny: []` en `skills: []` geldig en slaagt de gate — leeg betekent expliciet "geen", niet "onbekend"

### Requirement: Executie-seeds zijn afgeleid van de canonieke bron

De executie-rollen SHALL canoniek in `docs/agents/seeds/<rol>.md` staan en per
spoke byte-identiek afgeleid worden (`scripts/gen_agent_seeds.py`, met `--check`
als drift-gate). Een seed SHALL in zijn front-matter naast `tools:` ook `model:`
en `skills:` declareren, zodat de worker die uit het rolbestand in de doelrepo
kan lezen zonder de registry te hoeven ophalen.

#### Scenario: Drift wordt gevangen

- **WHEN** een per-spoke `.claude/agents/<rol>.md` afwijkt van de canonieke seed
- **THEN** faalt `gen_agent_seeds.py --check`

#### Scenario: De worker kan model en skills lezen

- **WHEN** een run start in een doelrepo
- **THEN** staan model en skills in `.claude/agents/<rol>.md` van die repo, afgeleid van de canonieke seed
