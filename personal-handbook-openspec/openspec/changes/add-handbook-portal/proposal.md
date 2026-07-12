# Change: add-handbook-portal

## Why

De spokes bestaan na change 2; nu de hub. Eén repo dat aggregeert, bouwt en
deployt, plus een MCP-endpoint dat dezelfde importlijst leest zodat agents en
site nooit uiteenlopen — het Conduction-model, geschaald naar één persoon.

## What changes

Eén nieuw repo op GitHub `MWest2020` (besluit 2026-07-12: alles personal
blijft op GitHub; Codeberg is werkcontext en blijft buiten dit ecosysteem):

- **`handbook`**: mkdocs-bron, importlijst, pipeline, deze openspec-map.
  Deploy-target is een orphan branch **`gh-pages`** in ditzelfde repo
  (GitHub Pages serveert op `mwest2020.github.io/handbook/`). Geen handwerk
  op die branch, alleen CI pusht ernaartoe.

## Ontwerp

- **mkdocs + multirepo-import.** De importlijst in `mkdocs.yml` is de enige
  waarheid over welke repos meedoen; die lijst wordt gegenereerd/gevalideerd
  tegen `inventory/repos.json` (`handbook_import: yes` én
  `sensitivity: public-ok`). CI faalt bij drift tussen lijst en inventaris.
- **Publiek/privaat-splitsing.** Publieke build → GitHub Pages
  (`mwest2020.github.io/handbook/`). Private sectie (homelab, private-only
  repos): aparte build-target die lokaal of op de interne beheer-host draait en NIET naar
  Pages pusht. Zelfde mkdocs-bron, tweede config (`mkdocs.private.yml`) die
  de publieke config erft en de private imports toevoegt. Alle imports komen
  van GitHub (private repos via read-only token in CI, alleen voor de
  private build).
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
- GitHub Pages serveert per repo op `mwest2020.github.io/<repo>/`; het
  handbook claimt dus alleen het subpad `/handbook`.

## Open vragen (beslist 2026-07-12)

1. ~~Forge/account~~ → GitHub `MWest2020` (Codeberg = werk, blijft erbuiten).
2. ~~Forgejo Actions of Woodpecker~~ → GitHub Actions (zelfde workflow-syntax,
   forge waar alles al staat; wave 1 draaide er al CI).
3. Private build: on-demand commando eerst; automatisering op de interne
   beheer-host pas als de private sectie stabiel is (herzien na een maand).
