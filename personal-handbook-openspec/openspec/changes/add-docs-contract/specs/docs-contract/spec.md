# Spec-delta: docs-contract

## ADDED Requirements

### Requirement: Diátaxis-light structuur

Elk deelnemend repo SHALL een `docs/`-map hebben met `index.md` in de root.
Markdown-pagina's SHALL uitsluitend in de root of in de submappen `how-to/`,
`reference/` en `explanation/` staan (ADR's onder
`explanation/adr/NNNN-titel.md`). Mappen zonder markdown (assets,
afbeeldingen, diagram-bronnen) vallen buiten deze eis. Lege submappen SHALL
worden weggelaten.

#### Scenario: Conforme structuur

- WHEN een repo `docs/index.md` en `docs/reference/` met inhoud bevat en
  geen andere markdown-dragende submappen
- THEN voldoet de structuur aan het contract

#### Scenario: Onbekende submap met pagina's

- WHEN `docs/` een submap buiten de drie Diátaxis-mappen bevat mét
  markdown-bestanden
- THEN faalt de contract-check met vermelding van de afwijkende map

#### Scenario: Assets-map

- WHEN `docs/` een map `img/` met alleen afbeeldingen bevat
- THEN is dat geen contract-schending

### Requirement: Front matter per pagina

Elke pagina onder `docs/` SHALL YAML-front-matter hebben met minimaal de
velden `status` (current | draft | deprecated) en `last_reviewed`
(ISO-datum). Extra velden (bijv. `title` voor mkdocs-navigatie) zijn
toegestaan; een `owner`-veld SHALL NOT voorkomen (eigenaar is altijd Mark,
het veld zou ruis zijn).

#### Scenario: Ontbrekende front matter

- WHEN een pagina geen front matter of een ontbrekend verplicht veld heeft
- THEN faalt de contract-check voor die pagina

#### Scenario: Niet-gereviewde migratie

- WHEN een bestaande pagina wordt gemigreerd zonder inhoudelijke review
- THEN krijgt die pagina `status: draft` met `last_reviewed` = de
  migratiedatum; pas een echte inhoudelijke review zet `status: current`
  en een verse `last_reviewed`

### Requirement: Taalregel

Docs SHALL in het Engels zijn voor publieke open-source-repos; Nederlands is
toegestaan voor private/homelab-repos. Binnen één repo SHALL NOT worden
gemixt.

#### Scenario: Gemixte talen binnen een repo

- WHEN `docs/` van één repo pagina's in twee talen bevat
- THEN is dat een contract-schending en wordt één taal gekozen bij remediatie

### Requirement: Minimum viable docs

Een repo SHALL minimaal `docs/index.md` (wat is dit, status, link naar
README, links naar de aanwezige secties; maximaal 3 regels boilerplate) plus
één reference-pagina bevatten om als "voldoet" te tellen.

#### Scenario: Alleen een lege index

- WHEN `docs/` alleen een index zonder inhoudelijke reference-pagina bevat
- THEN telt het repo als `has_docs: partial`, niet `yes`
