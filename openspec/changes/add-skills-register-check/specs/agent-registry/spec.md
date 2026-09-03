## ADDED Requirements

### Requirement: Skills worden gevalideerd tegen het skill-register

Elke `skills:`-entry in een agent-facet SHALL bestaan als gepromoveerde skill in het skill-register (`inventory/skills-register.yml`, een mirror van skill-forge's `forge register`-uitvoer); de gate SHALL de PR laten falen bij een onbekende skill, en ook bij een niet-lege `skills:` terwijl het register ontbreekt (dan kan niet worden gevalideerd). Een lege `skills: []` SHALL altijd slagen.

#### Scenario: Geldige skill

- **WHEN** een agent-def `skills: [thinking-red-team]` declareert en die slug in het register staat
- **THEN** slaagt de gate

#### Scenario: Onbekende skill

- **WHEN** een agent-def een skill declareert die niet in het register staat
- **THEN** faalt de gate met de onbekende slug en de reden (niet gepromoveerd in skill-forge)

#### Scenario: Register ontbreekt

- **WHEN** een def een niet-lege `skills:` heeft maar het register-bestand ontbreekt
- **THEN** faalt de gate (kan niet valideren), terwijl een lege `skills: []` wel slaagt
