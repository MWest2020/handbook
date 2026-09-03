---
status: draft
last_reviewed: 2026-09-03
---

# Agents — canonieke registry

De **enige waarheid** over wie de agents van het ecosysteem zijn. Elke rol heeft
hier één definitie; boomhuis (chat) en habitat (executie) *lezen* die, ze
her-definiëren 'm niet. Zo is een bouwer altijd dezelfde bouwer.

## Hoe te lezen (mens én agent)

- Mens: deze pagina's op de site.
- Agent: via `handbook_mcp` → `read_doc("handbook", "docs/agents/<naam>.md")`.

## Twee facetten per definitie

| Facet | Wat | Consument |
|---|---|---|
| **chat** | systemprompt + kanaal-scope + `tools`/`skills` | boomhuis (`claude -p`-listener) |
| **executie** | kooi-rol + `tools`/`skills` + output-schema | habitat (gekooide K8s-job) |

Een rol kan één leeg facet hebben (assistent = alleen chat; security = alleen
executie). Het `## Mandaat` is voor beide facetten én voor mensen de bron.

Elk niet-leeg facet declareert in het front-matter expliciet `tools.allow`,
`tools.deny` (welke tools juist níet) en `skills` — leeg (`[]`) is een geldige,
expliciete keuze. De gate `scripts/check_agent_tools.py` bewaakt dat het contract
er staat, dat een executie-`allow` overeenkomt met de seed die habitat uitvoert, én
dat elke `skills:`-entry bestaat in het skill-register (`inventory/skills-register.yml`,
mirror van skill-forge); de CI-stap die 'm draait wordt met de hand ingehaakt
(CI-config is een human-gate).

## Guardrails

- **Identiteit:** de relay is *closed* — alleen npubs uit deze registry doen mee.
- **Definitie:** consumenten draaien een agent alleen conform deze bron; een
  drift-gate vangt afwijking (CI), en deze map valt onder CODEOWNERS zodat "wie
  de agents zijn" langs Mark loopt.

## Rollen

- [coordinator](coordinator.md) — meta-agent: routeert droppings (route/nieuw/update)
- [bouwer](bouwer.md) — bouw-scoping (chat, #bouw) + habitat-`builder` (executie)
- architect — architectuur-sparring (chat, #architectuur) + habitat-plan (executie) *(volgt)*
- assistent — algemene chat-agent (alle kanalen), geen executie *(volgt)*
- [reviewer](reviewer.md) / [security](security.md) — alleen executie (habitat)
- **seeds/** — canonieke executie-seeds; de per-spoke `.claude/agents/` worden hieruit afgeleid (generator + drift-gate)
