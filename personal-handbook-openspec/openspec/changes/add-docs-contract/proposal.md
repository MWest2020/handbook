# Change: add-docs-contract

## Why

Zonder een uniform contract wordt aggregatie zinloos: het handbook zou lege of
wildgroeiende `/docs`-mappen importeren. Het contract is bewust lichter dan het
Conduction-techbook — één eigenaar, dus geen owner-governance, wel freshness.

## What changes

Per repo met `needs_docs: yes` (uit de vastgestelde inventaris) een PR die het
contract aanbrengt. Per repo met `needs_mcp_json: yes` bevat dezelfde PR een
`.mcp.json`. Eén PR per repo, geen bulk-force-pushes.

## Docs-contract (specificatie)

```
docs/
  index.md          # wat is dit, status, 3 regels max boilerplate
  how-to/           # taakgericht ("deploy naar k8s", "release maken")
  reference/        # feiten (config-opties, API, tenant/waarden-schema's)
  explanation/      # waarom-besluiten; ADR's horen hier (adr/NNNN-titel.md)
```

- Lege mappen weglaten. Minimum viable: `index.md` + één reference-pagina.
- Front matter per pagina (YAML):

```yaml
---
status: current        # current | draft | deprecated
last_reviewed: 2026-07-11
---
```

  Geen `owner`-veld: eigenaar is altijd Mark; het veld zou ruis zijn.
- Taal: Engels voor publieke open-source-repos, Nederlands toegestaan voor
  private/homelab-repos. Niet mixen binnen één repo.
- Geen projectkennis in het handbook dupliceren; het handbook linkt alleen.

## .mcp.json-template (specificatie)

Alleen voor repos met actieve Claude Code-ontwikkeling. Minimaal en expliciet:

```json
{
  "mcpServers": {
    "handbook": {
      "type": "http",
      "url": "<handbook-mcp-url, in te vullen na change 3>"
    }
  }
}
```

- Per repo alléén de servers die dat repo echt nodig heeft — geen kopie van
  een maximale lijst. Extra servers vereisen een regel motivatie in de PR.
- Nooit tokens of URLs met credentials in `.mcp.json` (het bestand is
  gecommit). Secrets via env-verwijzing.

## Impact

- Geen verplaatsingen buiten taak 2.2 (migratie van bestaande losse docs
  naar de Diátaxis-structuur); alle overige wijzigingen zijn additief
  (nieuwe bestanden).
- Bestaande README's blijven; `docs/index.md` verwijst ernaar, vervangt niet.
