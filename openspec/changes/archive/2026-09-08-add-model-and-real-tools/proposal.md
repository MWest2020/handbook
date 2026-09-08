# Change: add-model-and-real-tools

## Why

Mark, 2026-09-06, bij het lezen van de eerste nieuwe agent-definitie: *"de
agent.md is proza. ik zie niet welke tools, niet welk model. Dat moet niet alleen
daar, maar bij elke agent."*

Vastgesteld over alle tien definities:

| gap | stand vóór deze change |
|---|---|
| model | **geen enkele** def noemt een model; de listener geeft geen `--model` mee → elke chat-agent draait op wat de omgeving toevallig default is |
| tools | alle tien hadden `chat.tools = {allow: [], deny: []}`, en de listener geeft geen `--allowedTools` mee → gedeclareerd noch afgedwongen |
| gate | `check_agent_tools.py` eiste alleen dát de velden bestaan; `allow: []` slaagde, dus de gate kon dit niet vangen |

## What changes

- **`model` per facet, verplicht**, uit `{haiku, sonnet, opus}`. Regel van Mark:
  *zoeken = haiku, denken = sonnet, uitzonderlijk = opus.*

  | agent | chat | executie |
  |---|---|---|
  | architect | opus | opus |
  | bouwer · reviewer · roodteam · coordinator · ontwerper · marketing | sonnet | sonnet (bouwer, reviewer) |
  | security | — | sonnet |
  | archivaris · assistent | haiku | — |

- **Chat-facetten krijgen echte tools**: `allow: [Read, Grep, Glob]`,
  `deny: [Write, Edit, Bash]`. Chat-rollen doen geen executie; lezen mogen ze,
  schrijven en shellen niet. Verruimen gebeurt per aangetoonde behoefte, niet
  vooraf.
- **Seeds krijgen `model:` en `skills:`** in hun front-matter, zodat de worker ze
  uit `.claude/agents/<rol>.md` van de doelrepo kan lezen zonder de registry op te
  halen. Afgeleid met `gen_agent_seeds.py` (51 bestanden bijgewerkt).
- **Gate**: `model` verplicht en uit de vaste set, en voor een executie-facet met
  seed wordt het model gekruist met de seed — zoals `tools.allow` dat al werd.

## Waarom `haiku|sonnet|opus` en geen exacte model-id

De def legt de *intentie* vast. Een exacte id (`claude-sonnet-5`) laat elke
definitie verlopen bij de volgende release en verplaatst een modelbesluit naar tien
losse bestanden. De alias houdt de keuze op één plek uitlegbaar: zoeken is goedkoop,
denken is duur, uitzonderingen zijn expliciet.

## Wat hier NIET gebeurt

- **Geen afdwinging**: `--model` en `--allowedTools` doorgeven is de listener
  (boomhuis) en de worker (habitat). Deze change levert de data waarop die
  afdwinging leunt; zonder de vervolgstappen verandert er runtime niets.
- **`allow: []` blijft geldig.** Ik wilde het eerst verbieden, maar de bestaande
  spec noemt leeg expliciet een geldige keuze ("leeg betekent expliciet geen, niet
  onbekend"), en zodra de runtime afdwingt is een lege lijst een zichtbare,
  zelfcorrigerende keuze in plaats van een stille onbeperktheid. Regel
  teruggedraaid; het probleem zat in de afwezige afdwinging, niet in de leegte.
- **Geen npub voor roodteam** — die identiteit hoort in boomhuis.

## Impact

- 10 defs, 3 canonieke seeds, 51 afgeleide seed-bestanden, 1 gate, 1 spec.
- Volgende stappen die hierop wachten: listener (`--model`/`--allowedTools` +
  escalatiemelding per run) en worker (model + skills uit het rolbestand).
