# Change: audit-repo-inventory

## Why

Er is geen actueel overzicht van welke persoonlijke repos bestaan (Codeberg +
GitHub), welke actief zijn, welke `/docs` hebben, en welke agent-ontwikkeling
kennen. Zonder die inventarisatie is elke remediatie giswerk. Dit is de
read-only fundering onder changes 2 en 3.

## What changes

- Eén nieuw artefact: `inventory/repos.md` (tabel) + `inventory/repos.json`
  (machine-leesbaar, zelfde inhoud) in het handbook-repo (of tijdelijk lokaal
  tot dat repo bestaat).
- GEEN wijzigingen aan bestaande repos. Deze change is strikt lezend.
- Geen spec-delta: dit is een read-only audit die geen capability-gedrag
  toevoegt of wijzigt; het artefact zelf is de output.

## Scope

- Alle repos onder de Codeberg-account/org van Mark (via Forgejo API).
- Alle repos onder GitHub `MWest2020` (via GitHub API of `gh`).
- Homelab-configuratie die (nog) niet in een repo zit: signaleren als gap,
  niet oplossen.

## Classificatie (per repo, verplichte velden)

| Veld | Waarden | Criterium |
|---|---|---|
| `forge` | codeberg / github | Waar staat het canonieke repo |
| `tier` | active / maintained / archive | Zie beslistabel hieronder |
| `visibility` | public / private | Zoals op de forge |
| `sensitivity` | public-ok / private-only | Mag de docs-inhoud op publieke Pages? |
| `has_docs` | yes / partial / no | Bestaat `/docs` met echte inhoud |
| `has_mcp_json` | yes / no | Bestaat `.mcp.json` in root |
| `needs_mcp_json` | yes / no | Zie beslistabel |
| `needs_docs` | yes / no | Zie beslistabel |
| `handbook_import` | yes / no | Komt in de mkdocs-importlijst |
| `notes` | vrij | Bijzonderheden, licentie-afwijkingen |

## Beslistabel tiers

- **active**: commits in de laatste 90 dagen ÓF genoemd in een lopend extern
  traject (zeef, openanonymiser, wanderer, estafette) ÓF homelab-infra die
  draait. → `needs_docs: yes`, `needs_mcp_json: yes` als er Claude Code-sessies
  in draaien (heuristiek: aanwezigheid van `.claude/`, `CLAUDE.md`, of
  `openspec/`), `handbook_import: yes`.
- **maintained**: geen recente commits maar in gebruik of leverbaar
  (certswap, billbird e.d.). → `needs_docs: yes` (minimaal README-niveau +
  reference), `needs_mcp_json: no`, `handbook_import: yes`.
- **archive**: dood, experiment, of vervangen. → alles `no`; aanbeveling:
  archiveren op de forge zodat de lijst niet opnieuw vervuilt.

Twijfelgevallen krijgen `tier: TBD` en een vraag in `notes` — de agent beslist
niet zelf. De vastgestelde tabel (na review door Mark) is de gate naar change 2.

## Impact

- Geen productie-impact; read-only.
- Output is tevens de kiem van het homelab-DR-verhaal: alles wat niet in de
  tabel staat maar wel draait, is per definitie bus-factor-1-risico.
