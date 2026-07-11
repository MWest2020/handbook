# Spec-delta: handbook-portal

## ADDED Requirements

### Requirement: Importlijst is de enige waarheid

De importlijst in `mkdocs.yml` SHALL de enige plek zijn die bepaalt welke
repos in het handbook meedoen. De lijst SHALL gegenereerd/gevalideerd worden
tegen `inventory/repos.json` (`handbook_import: yes`); CI SHALL falen bij
drift tussen lijst en inventaris.

#### Scenario: Drift tussen importlijst en inventaris

- WHEN `mkdocs.yml` een repo importeert dat in `inventory/repos.json` niet
  op `handbook_import: yes` staat (of andersom)
- THEN faalt de CI-run met een diff van beide lijsten

### Requirement: Aggregatie zonder duplicatie

Het handbook SHALL zelf géén projectkennis bevatten; het SHALL uitsluitend
overkoepelende pagina's hebben (index, conventies, homelab-verwijzing) en
alle projectinhoud at build time importeren uit de deelnemende repos.

#### Scenario: Projectinhoud in de hub

- WHEN een pagina met projectspecifieke kennis in het handbook-repo zelf
  wordt toegevoegd
- THEN wordt die bij review geweigerd en verhuist de inhoud naar `/docs`
  van het betreffende repo

### Requirement: Publiek/privaat-splitsing op repo-niveau, fail closed

De publieke build SHALL uitsluitend repos importeren met
`sensitivity: public-ok` én `handbook_import: yes`. Splitsing SHALL op
repo-niveau gebeuren (geen per-pagina filters). Bij ontbrekende of
onduidelijke `sensitivity` SHALL het repo behandeld worden als
`private-only` (fail closed).

#### Scenario: Repo zonder sensitivity-classificatie

- WHEN een repo in de inventaris geen (geldige) `sensitivity`-waarde heeft
- THEN wordt het uitgesloten van de publieke build en alleen meegenomen in
  de private build

#### Scenario: Private-only repo in publieke build

- WHEN de import-generatie een `private-only` repo in `mkdocs.yml`
  (publiek) zou opnemen
- THEN faalt de CI-check vóór deploy
