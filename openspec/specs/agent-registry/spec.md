# agent-registry Specification

## Purpose
TBD - created by archiving change add-seed-derivation. Update Purpose after archive.
## Requirements
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

### Requirement: Eén canonieke definitie per agent-rol

Elke agent-rol SHALL precies één canonieke definitie hebben, in de handbook
onder `docs/agents/<naam>.md`; geen enkele andere plek (spoke-seeds,
boomhuis-config) SHALL een rol her-definiëren — die consumeren de canonieke
bron.

#### Scenario: Wijziging bereikt iedereen

- **WHEN** de definitie van een rol (bijv. `bouwer`) in de handbook wijzigt
- **THEN** lezen alle consumenten (boomhuis-chat, habitat-executie) die
  gewijzigde definitie, zonder dat er een kopie handmatig bijgewerkt hoeft

#### Scenario: Geen tweede waarheid

- **WHEN** iemand een rol op een andere plek dan `docs/agents/` probeert vast te
  leggen als bron
- **THEN** is dat volgens dit contract geen geldige bron; die plek hoort te
  verwijzen naar of af te leiden van de canonieke definitie

### Requirement: Twee facetten in één definitie

Een definitie SHALL een machine-leesbaar front-matter bevatten met minstens
`naam` en `npub`, plus een **chat-facet** (systemprompt + kanaal-scope) en een
**executie-facet** (kooi-rol/tools/schema, of expliciet leeg). Een consument
SHALL alleen zijn eigen facet gebruiken.

#### Scenario: Boomhuis leest de chat-facet

- **WHEN** de boomhuis-listener een agent draait
- **THEN** haalt hij systemprompt en kanaal-scope uit de chat-facet van de
  canonieke definitie, niet uit een eigen kopie

#### Scenario: Chat-only of executie-only

- **WHEN** een rol alleen chat is (assistent) of alleen executie (security)
- **THEN** is het andere facet expliciet leeg, en de definitie blijft geldig

### Requirement: MCP-leesbaar zonder nieuwe machinerie

De definities SHALL via de bestaande `handbook_mcp`-tool `read_doc` leesbaar
zijn (pad `docs/agents/**/*.md`), zodat elke agent de canonieke bron kan
opvragen; deze change SHALL geen nieuwe MCP-tool of guard-versoepeling vereisen.

#### Scenario: Agent vraagt zijn definitie op

- **WHEN** een agent `read_doc("handbook", "docs/agents/bouwer.md")` aanroept
- **THEN** krijgt hij de canonieke definitie terug, binnen de bestaande
  padbegrenzing en token-hygiëne van de MCP-laag

### Requirement: Spawnen kan alleen uit de canonieke bron (guardrail)

Een consument (boomhuis-listener, habitat-dispatch) SHALL een agent uitsluitend
draaien op basis van een definitie die overeenkomt met de canonieke
handbook-bron, en SHALL weigeren een agent te spawnen wiens npub/rol niet in de
registry staat. Afwijking tussen de effectieve consument-config en de bron
SHALL door een gate (CI drift-check) worden gevangen, niet aan een afspraak
worden overgelaten. De closed relay (identiteit-lidmaatschap) blijft de
achtervang: een agent zonder registry-identiteit komt sowieso de relay niet op.

#### Scenario: Onbekende agent geweigerd

- **WHEN** iets probeert een agent te draaien wiens npub niet in de registry
  (`docs/agents/`) staat
- **THEN** weigert de consument te spawnen, en zou de relay de identiteit
  sowieso weigeren (closed mode)

#### Scenario: Drift wordt gevangen, niet gehoopt

- **WHEN** de effectieve config van een consument (boomhuis `agents.yml`,
  habitat-seed) afwijkt van de canonieke definitie
- **THEN** faalt de drift-gate in CI, zodat de afwijking niet stil doorleeft

#### Scenario: Wie de agents zijn, vergt jouw review

- **WHEN** iemand een agent-definitie onder `docs/agents/` wil wijzigen of
  toevoegen
- **THEN** loopt dat via CODEOWNERS/branch-protection langs Mark, zodat "wie de
  agents zijn" niet buiten hem om verandert

