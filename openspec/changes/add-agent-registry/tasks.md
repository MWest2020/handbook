# Tasks: add-agent-registry

- [ ] 1.1 `docs/agents/index.md`: overzicht (Diátaxis-reference) — wie de agents
      zijn, welke facetten een definitie heeft, hoe ze via MCP te lezen zijn
- [ ] 1.2 Canonieke definities aanmaken onder `docs/agents/`: de bestaande
      rollen consolideren tot één bron per rol — chat-personas (assistent,
      architect, bouwer) én executie-rollen (builder, reviewer, security,
      architect-plan), met het front-matter-contract uit design.md
- [ ] 1.3 `inventory/repos.json`: hub-notes verwijzen naar `docs/agents/` als
      de agent-registry (geen nieuwe vlaggen)
- [ ] 1.4 `mkdocs.yml`: nav-sectie "Agents" die `docs/agents/` ontsluit
- [ ] 1.5 `scripts/`: (optioneel in deze change) een check dat elke definitie
      het front-matter-contract heeft (naam, npub, chat/executie-facet)
- [ ] 1.6 MCP-rooktest: `read_doc("handbook","docs/agents/bouwer.md")` levert de
      definitie; `list_docs("handbook")` toont de agent-pagina's
- [ ] 1.7 `CHANGELOG.md`: entry met het besluit (single source of truth) en de
      twee-facetten-vorm

> Consumptie is aparte, latere changes (proposal-first in de betrokken repo):
> - boomhuis: listener leest chat-facet uit de handbook; `agents.yml` → pointer
> - habitat/handbook: seeds afgeleid van de executie-facet + drift-gate
