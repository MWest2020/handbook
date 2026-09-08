# Tasks: add-agent-registry

- [x] 1.1 `docs/agents/index.md`: overzicht (Diátaxis-reference) — wie de agents
      zijn, welke facetten een definitie heeft, hoe ze via MCP te lezen zijn.
- [x] 1.2 Canonieke definities onder `docs/agents/`: tien rollen met het
      front-matter-contract uit design.md, plus `seeds/` voor de executie-kant.
- [x] 1.3 `inventory/repos.json`: de hub-notes wijzen naar `docs/agents/` als de
      agent-registry, met de gate erbij genoemd. Geen nieuwe vlaggen.
- [x] 1.4 **Niet gedaan, met reden.** `mkdocs.yml` zegt bovenaan: *"Nav is bewust
      automatisch (mappenstructuur)"*. Er is geen `nav:`-sleutel; `docs/agents/`
      wordt dus al ontsloten. Een handgeschreven "Agents"-sectie zou precies de
      uitzondering zijn waar dat commentaar tegen waarschuwt, en zou bij elke
      nieuwe agent met de hand bijgewerkt moeten worden.
- [x] 1.5 `scripts/check_agent_tools.py` bewaakt nu ook het identiteitsdeel:
      `naam` verplicht én gelijk aan de bestandsnaam, `npub` verplicht (`null`
      mag, met melding). Beide faalpaden getest door ze kapot te maken:
      `naam: bouwertje` → FAIL, `npub` weggehaald → FAIL, daarna hersteld en
      groen (10 definities).
- [x] 1.6 MCP-rooktest tegen de echte server: `list_docs("handbook")` geeft 20
      pagina's waarvan 14 agent-pagina's;
      `read_doc("handbook","docs/agents/bouwer.md")` levert 2548 tekens mét
      `naam`, `npub` en chat-facet. (Een eerdere meting die "1 pagina" leek te
      geven was mijn testclient die alleen het eerste content-block las, niet de
      server.)
- [x] 1.7 `CHANGELOG.md`: entry met het besluit (single source of truth), de
      twee-facetten-vorm en de nav-motivering.

> Consumptie is aparte, latere changes (proposal-first in de betrokken repo):
> - boomhuis: listener leest chat-facet uit de handbook — **gedaan**, de listener
>   haalt de defs op via `registry_base` uit `agents/agents.yml`.
> - habitat/handbook: seeds afgeleid van de executie-facet + drift-gate —
>   **gedaan** via `scripts/gen_agent_seeds.py --check`.
