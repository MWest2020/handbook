# Change: add-agent-registry

## Why

De agent-rollen van het ecosysteem zijn nu op meerdere plekken gedefinieerd en
lopen dus uiteen. De executie-rollen (builder/reviewer/security) staan als
byte-identieke **kopieën** per spoke in `prep/seeds/*/.claude/agents/*.md` —
niets bewaakt dat ze gelijk blijven. De chat-agent-rollen (assistent, architect,
bouwer) staan los in `boomhuis/agents/agents.yml`. Zo is een "bouwer" niet
gegarandeerd overal dezelfde bouwer: een wijziging op één plek bereikt de andere
niet ("ow, dat had ik niet meegekregen").

Besluit Mark (2026-08-27): **één canonieke definitie per agent-rol**, in de
handbook (de naaf), geserveerd via `handbook_mcp` — zodat elke agent en elke
laag (boomhuis-chat, habitat-executie) dezelfde definitie *leest* in plaats van
kopieert. Documentatie, MCP-ontsluiting en single-source-of-truth vallen dan
samen op één plek.

## What changes

- **`docs/agents/<naam>.md`**: de canonieke definitie per agent-rol, met vaste
  secties (facetten): **identiteit** (naam, npub), **mandaat** (wat de rol ís),
  **chat-facet** (systemprompt + kanaal-scope), **executie-facet** (kooi-regels,
  tools, output-schema, of een verwijzing). Onder `docs/` zodat ze via de
  bestaande `read_doc`-MCP-tool leesbaar zijn én op de site renderen.
- **`inventory/repos.json`**: de hub-notes verwijzen naar `docs/agents/` als de
  agent-registry; geen nieuwe vlaggen nodig (de hub-docs zijn al MCP-leesbaar
  via de `mcp-hub-self-read`-uitzondering).
- **Consumptie, niet her-definitie** (uitgewerkt in latere changes per repo):
  - boomhuis: de listener leest de chat-facet uit de handbook i.p.v. uit z'n
    eigen `agents.yml`; `agents.yml` wordt een dunne "welke agents draai ik +
    npub"-pointer.
  - habitat/seeds: de per-spoke `.claude/agents/*.md` worden **afgeleid** van de
    canonieke executie-facet (gegenereerd, niet met de hand gekopieerd) — de
    drift-fix.
- **`docs/agents/index.md`**: mens-leesbaar overzicht (Diátaxis-reference) van
  wie de agents zijn en waar ze draaien.

## Non-goals

- Geen nieuwe MCP-tool in deze change — `read_doc`/`list_docs` op `docs/agents/`
  volstaat. Een `list_agents`/`read_agent`-gemakstool is een latere, aparte
  change als het nodig blijkt.
- Geen verhuizing van de sleutels: privésleutels blijven in boomhuis
  (SOPS+age). De registry bevat alleen publieke npubs + rol-definitie.
- Geen automatische her-generatie van de habitat-seeds in deze change; dit
  legt de bron vast, de generatie is een vervolg-change in habitat/handbook.

## Impact

- Nieuw: `docs/agents/*.md`, `docs/agents/index.md`; `inventory/repos.json`
  (notes), `mkdocs.yml` (nav-sectie Agents), `CHANGELOG.md`.
- Spec: nieuwe capability `agent-registry`.
- Boomhuis en habitat consumeren later uit deze bron (aparte changes daar,
  proposal-first).
