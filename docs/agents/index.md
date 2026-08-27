---
status: draft
last_reviewed: 2026-08-27
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
| **chat** | systemprompt + kanaal-scope | boomhuis (`claude -p`-listener) |
| **executie** | kooi-rol / tools / output-schema | habitat (gekooide K8s-job) |

Een rol kan één leeg facet hebben (assistent = alleen chat; security = alleen
executie). Het `## Mandaat` is voor beide facetten én voor mensen de bron.

## Guardrails

- **Identiteit:** de relay is *closed* — alleen npubs uit deze registry doen mee.
- **Definitie:** consumenten draaien een agent alleen conform deze bron; een
  drift-gate vangt afwijking (CI), en deze map valt onder CODEOWNERS zodat "wie
  de agents zijn" langs Mark loopt.

## Rollen

- [bouwer](bouwer.md) — bouw-scoping (chat, #bouw) + habitat-`builder` (executie)
- architect — architectuur-sparring (chat, #architectuur) + habitat-plan (executie) *(volgt)*
- assistent — algemene chat-agent (alle kanalen), geen executie *(volgt)*
- [reviewer](reviewer.md) / [security](security.md) — alleen executie (habitat)
- **seeds/** — canonieke executie-seeds; de per-spoke `.claude/agents/` worden hieruit afgeleid (generator + drift-gate)
