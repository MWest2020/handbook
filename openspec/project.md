# Project: Personal Handbook (hub-and-spoke docs voor eigen projecten + homelab)

## Doel

Eén handbook als aggregatiepunt voor alle persoonlijke repos (open-source projecten
én homelab), naar het model van het Conduction-techbook, maar geschaald naar één
eigenaar. Documentatie leeft in de project-repos zelf (`/docs`); het handbook
aggregeert at build time via één importlijst. Geen kopieën, geen drift.

## Northstar

Dit is het volledige Conduction-model, niet een afgeslankte versie; de hub
krijgt later meer mogelijkheden, dus de gates wegen zwaarder, niet lichter.

1. **Bewezen sync vóór elke push.** Werken aan een repo betekent: vóór elke
   push is bewezen dat de docs in sync zijn met de code én dat de
   repo-functionaliteit het doet (unit tests / dry-runs) — beide via gates
   die zelf getest zijn. Documentatie-beweringen worden op termijn
   uitvoerbaar getoetst (docs-claims).
2. **Het handbook is DE ingang voor agents via MCP.** Site en agents lezen
   exact dezelfde importlijst; er bestaat geen tweede waarheid.
3. **Agents dichtgetimmerd voor idempotente werking.** Per repo een
   operatiecataloog (`docs/agents.md`) met autonomieniveaus (autonoom /
   mens-vereist / verboden), de creatie-regel (nieuwe entiteiten altijd
   voorstel-eerst), de escalatieregel (niet in de cataloog = eerst vragen),
   en GET-check-first als huisstijl.

## Uitgangspunten (niet onderhandelbaar)

- **Boring and auditable.** Standaard tooling (mkdocs), expliciete configuratie,
  geen slimmigheden. Elke beslissing herleidbaar in een ADR of proposal.
- **Eén bron van waarheid.** De importlijst in het handbook (`mkdocs.yml`) is de
  enige plek die bepaalt welke repos meedoen. Agents (MCP) lezen dezelfde lijst.
- **Docs bij de code.** Elk deelnemend repo heeft `/docs` volgens het contract
  (zie change `add-docs-contract`). Het handbook bevat zelf géén projectkennis,
  alleen overkoepelende pagina's (index, homelab-overzicht, conventies).
- **Publiek/privaat gescheiden op gevoeligheid, niet op onderwerp.** Secrets-
  locaties en credentials horen nooit op een publieke Pages-site; letterlijke
  identifiers (hostnamen, gebruikersnamen, tailnet-namen, LAN-IP's) worden
  geredigeerd naar generieke placeholders vóór publieke import (besluit
  2026-07-14: homelab-docs mogen publiek, mits geredigeerd — zie change
  `redact-homelab-docs` in het homelab-repo). Splitsing gebeurt verder op
  repo-niveau (privaat repo = private sectie), niet met per-pagina filters.
- **EUPL-1.2** voor publieke content, tenzij een repo al anders gelicenseerd is.
- **Python-tooling via `uv`**, nooit pip direct.

## Scope (forges)

- **GitHub** (`MWest2020`): de enige forge voor dit hele ecosysteem — bestaande
  projectrepos (o.a. zeef, wanderer, estafette, billbird, skill-forge, certswap,
  gitsweeper) én het handbook-repo zelf.
- **Codeberg is werkcontext** (werkgever-org) en blijft volledig buiten dit
  persoonlijke handbook — geen repos, geen imports, geen deploys daarheen.
  (Besluit Mark 2026-07-12; verving het oorspronkelijke Codeberg-plan.)

## Changes en afhankelijkheden

```
audit-repo-inventory      (change 1: inventarisatie + classificatie, read-only)
        │
        ▼
add-docs-contract         (change 2: /docs + .mcp.json remediatie per repo, via PR's)
        │
        ▼
add-handbook-portal       (change 3: handbook-repo + pipeline + Pages-deploy)
```

Change 1 produceert de classificatietabel waar 2 en 3 op draaien. Niet beginnen
aan 2 voordat de tabel door Mark is vastgesteld (menselijke goedkeuring is de gate).

## Roadmap (gepland, na changes 1–3)

Eén regel scope per change; specs volgen per change bij oppakken,
voorstel-eerst:

- `add-drift-gates`: freshness blocking na proefperiode, linkcheck,
  periodieke rebuild + zelfsluitend drift-issue.
- `add-hub-mcp`: read-only MCP-server (stdio) op de contentlaag die de
  importlijst leest; padbegrenzing en token-hygiëne als expliciete
  requirements; sessietest als verify.
- `add-agent-guardrails`: operatiecataloog per deelnemend repo, livetest
  met injectie-/creatie-scenario.
- `add-docs-claims`: uitvoerbare verify-blokken in docs + `scripts/verify.sh`
  per repo als tweede pre-push-gate (functionele dry-runs), sabotage-test
  als bewijs.

## Definities

- **mcp.json**: `.mcp.json` in de repo-root, declareert MCP-servers voor Claude
  Code-sessies in dat repo. Alleen voor repos met actieve agent-ontwikkeling.
- **Docs-contract**: `/docs` met Diátaxis-light indeling + front matter. Zie
  change 2 voor de exacte specificatie.
- **Handbook**: het aggregatie-repo (naam: `handbook`, op GitHub `MWest2020`). Bewust géén
  "techbook": dit dekt ook niet-platformzaken (administratie-verwijzingen,
  project-portfolio), en er is geen tweede boek om tegen af te bakenen.
