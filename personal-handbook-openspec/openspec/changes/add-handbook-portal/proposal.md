# Change: add-handbook-portal

## Why

De spokes bestaan na change 2; nu de hub. Eén repo dat aggregeert, bouwt en
deployt, plus een MCP-endpoint dat dezelfde importlijst leest zodat agents en
site nooit uiteenlopen — het Conduction-model, geschaald naar één persoon.

## What changes

Eén nieuw repo op Codeberg:

- **`handbook`**: mkdocs-bron, importlijst, pipeline, deze openspec-map.
  Deploy-target is een orphan branch **`pages`** in ditzelfde repo
  (Codeberg Pages serveert een `pages`-branch van repo X op
  `<user>.codeberg.page/X/`). Geen handwerk op die branch, alleen CI pusht
  ernaartoe. Bewust géén apart repo met de naam `pages`: dat zou op de ROOT
  van `<user>.codeberg.page` serveren en het account-brede Pages-domein
  claimen.

## Ontwerp

- **mkdocs + multirepo-import.** De importlijst in `mkdocs.yml` is de enige
  waarheid over welke repos meedoen; die lijst wordt gegenereerd/gevalideerd
  tegen `inventory/repos.json` (`handbook_import: yes` én
  `sensitivity: public-ok`). CI faalt bij drift tussen lijst en inventaris.
- **Publiek/privaat-splitsing.** Publieke build → Codeberg Pages
  (`<user>.codeberg.page/handbook`). Private sectie (homelab, private-only
  repos): aparte build-target die lokaal of op de interne beheer-host draait en NIET naar
  Pages pusht. Zelfde mkdocs-bron, tweede config (`mkdocs.private.yml`) die
  de publieke config erft en de private imports toevoegt. Cross-forge import
  vanaf GitHub is toegestaan (read-only clone in CI).
- **Freshness-gate.** Hergebruik het check_freshness-principe uit het
  Conduction-handbook: pagina's met `last_reviewed` ouder dan 180 dagen →
  CI-warning (geen hard fail; één eigenaar, dus een fail zou alleen jezelf
  blokkeren). `status: deprecated` pagina's uitgesloten.
- **MCP-server.** Fase 2 (aparte taak, mag later): kleine read-only MCP-server
  die de importlijst + gebouwde site leest. Tot die tijd blijft de placeholder
  in de `.mcp.json`'s staan.
- **Overkoepelende pagina's in het handbook zelf** (en alléén deze):
  `index.md` (portfolio/kaart van alle projecten), `conventies.md` (het
  docs-contract, licentiebeleid, uv-regel), `homelab/herstel.md` (verwijzing
  naar de private sectie). Geen projectinhoud.

## Impact

- Nieuwe CI-runs bij elke push naar handbook + nightly rebuild (spokes wijzigen
  zonder dat de hub het weet; nightly vangt dat).
- Codeberg Pages is per account gedeeld; het handbook serveert via zijn
  eigen `pages`-branch op het subpad `/handbook`, niet op de root.

## Open vragen (beslissen vóór apply)

1. Codeberg-accountnaam/org voor de twee repos.
2. Nightly rebuild via Forgejo Actions of Woodpecker? (Voorstel: Forgejo
   Actions, consistent met con-ci-ervaring; geen OCI-build nodig, dus geen
   rootless-problematiek.)
3. Draait de private build op de interne beheer-host als cronjob of on-demand?
