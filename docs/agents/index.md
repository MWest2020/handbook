---
status: draft
last_reviewed: 2026-09-21
---

# Agents — canonieke registry

De **enige waarheid** over wie de agents van het ecosysteem zijn. Elke rol heeft
hier één definitie; ratatoskr (chat) en habitat (executie) *lezen* die, ze
her-definiëren 'm niet. Zo is een bouwer altijd dezelfde bouwer.

## Hoe te lezen (mens én agent)

- Mens: deze pagina's op de site.
- Agent: via `handbook_mcp` → `read_doc("handbook", "docs/agents/<naam>.md")`.

## Twee facetten per definitie

| Facet | Wat | Consument |
|---|---|---|
| **chat** | systemprompt + kanaal-scope + `tools`/`skills` | ratatoskr (`claude -p`-listener) |
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

## Hoe de vloot samenwerkt: hub en spokes

> Mark, 2026-09-21: *"Ik wil eigenlijk enkel met Odin spreken, maar odin moet
> niet alles doen. Odin is de hub en niet de spokes."*

    Mark ──► odin (hub, #general)
               │  beslist: zelf antwoorden, routeren, of uitzetten
               ├─ !route #kanaal ───────► een spoke-agent in zijn eigen kanaal
               ├─ !sessie <type> … ─────► een losgekoppelde werksessie; het
               │                          antwoord komt terug in dit kanaal,
               │                          onder odins eigen naam
               └─ "dat loopt via bouwer" ► !dispatch → habitat (poort = Mark)

Drie regels die daaruit volgen, en die per definitie hieronder terugkomen:

1. **De hub doet het werk niet.** Wat tijd kost gaat naar een spoke. Odin
   blijft aanspreekbaar terwijl die spoke draait — dat is de hele winst. Zie
   `delegate_session` in [odin](odin.md).
2. **Bouwen gaat naar habitat, via bouwer.** Niet in een chat-beurt, niet in een
   leessessie. Bouwer is de bewaker van die weg; `!dispatch` blijft Marks eigen
   commando, want bouwen is waar een vergissing duur is.
3. **Ratatoskr is er voor menselijke context**, niet om dingen te doen: kunnen
   meelezen en reageren in meerdere kanalen tegelijk. Wat daar werkt zijn
   dagelijkse standups, escalaties, en het oordeel van een reviewer, architect
   of roodteamer. Wat daar niet werkt zijn gesprekken waarin een agent uitlegt
   wat hij niet mag.

Die derde is een maatstaf, geen sfeerbeeld. Een agent die "dat kan ik niet"
antwoordt terwijl er een weg bestaat, is een fout in zijn definitie — noem de
weg. Een beperking die alleen in een mandaattekst staat en niet in de listener,
is geen beperking maar een misverstand dat geld kost.

## Guardrails

- **Identiteit:** de relay is *closed* — alleen npubs uit deze registry doen mee.
- **Definitie:** consumenten draaien een agent alleen conform deze bron; een
  drift-gate vangt afwijking (CI), en deze map valt onder CODEOWNERS zodat "wie
  de agents zijn" langs Mark loopt.

## Rollen

- [odin](odin.md) — **de hub**: de enige agent in #general. Mark praat met odin;
  odin routeert naar de spokes (route / nieuwe agent / uitbreiding).
  Was `coordinator`; hernoemd 2026-09-07 op besluit van Mark.
- [bouwer](bouwer.md) — bouw-scoping (chat, #bouw) + habitat-`builder` (executie)
- architect — architectuur-sparring (chat, #architectuur) + habitat-plan (executie) *(volgt)*
- assistent — algemene chat-agent (spoke-kanalen), geen executie *(volgt)*
- [reviewer](reviewer.md) / [security](security.md) — alleen executie (habitat)
- [roodteam](roodteam.md) — security/red-team-agent (chat, #red-team, #review), geen executie
- **seeds/** — canonieke executie-seeds; de per-spoke `.claude/agents/` worden hieruit afgeleid (generator + drift-gate)
