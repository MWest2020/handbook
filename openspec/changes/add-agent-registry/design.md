# Design: add-agent-registry

## Kernprincipe: één definitie, twee facetten

Een agent-rol heeft twee gezichten die vandaag op verschillende plekken leven.
De registry brengt ze samen in **één canoniek bestand per rol**:

- **chat-facet** — systemprompt + kanaal-scope. Consument: **boomhuis** (de
  `claude -p`-listener praat in kanalen).
- **executie-facet** — kooi-regels, toegestane tools, output-schema, mandaat.
  Consument: **habitat** (gekooide K8s-job die een branch produceert).

Zo bepaalt één plek "wie is bouwer", en elke laag pakt zijn eigen facet. Een
rol die alleen chat is (assistent) heeft een lege executie-facet; een rol die
alleen executie is (security) een lege chat-facet.

## Waarom `docs/agents/` en niet een eigen map

`handbook_mcp`'s padguard laat uitsluitend `docs/**/*.md` toe (token-hygiëne +
padbegrenzing, zie `handbook-mcp`-spec). Door de definities onder `docs/agents/`
te zetten zijn ze **meteen** MCP-leesbaar via de bestaande `read_doc`-tool —
geen nieuwe tool, geen guard-versoepeling — én ze renderen op de site als
documentatie. Drie eisen (single source, MCP, documentatie) vallen samen zonder
nieuwe machinerie. Een map buiten `docs/` zou een MCP-code- en guard-wijziging
vergen; bewust niet in deze change.

## Verworpen alternatieven

| Optie | Waarom niet |
|---|---|
| Aparte "roster"-repo | Fragmenteert; tegen het synergie-principe. De handbook ís al de MCP-naaf. |
| Definities in habitat | Habitat is bewust alleen de executie/kooi-laag; chat-personas horen daar niet. |
| Laten in boomhuis/agents.yml | Dat is een consument, geen naaf; habitat zou er niet natuurlijk uit lezen. |
| Nieuwe `read_agent`-MCP-tool nu | Overbodig: `read_doc` op `docs/agents/` werkt al. Kan later als gemak. |

## Structuur van één definitie (voorbeeld `bouwer`)

Front-matter voor de machine-leesbare velden, secties voor de facetten:

```markdown
---
status: actief
last_reviewed: 2026-08-27
agent:
  naam: bouwer
  npub: npub19qn78kzy2...          # publieke sleutel (boomhuis-identiteit)
  chat: { channels: [bouw] }        # chat-facet: waar praat 'ie
  executie: { habitat_rol: builder } # executie-facet: welke kooi-rol (of leeg)
---
# bouwer

## Mandaat
<canonieke omschrijving — de enige waarheid over wat 'bouwer' is>

## Chat-facet (boomhuis)
<systemprompt voor de chat-listener>

## Executie-facet (habitat)
<kooi-regels/tools/schema, of "n.v.t.">
```

boomhuis leest het front-matter + de chat-facet; habitat leest het front-matter
+ de executie-facet. De `## Mandaat` is voor beide (en voor mensen) de bron.

## Drift is dan een gate, geen hoop

Zodra de seeds en de boomhuis-`agents.yml` **afgeleid** zijn van deze bron, is
"gelijk blijven" afdwingbaar (een check dat de gegenereerde kopie overeenkomt
met de bron) i.p.v. een belofte. Die generatie/gates zijn vervolg-changes; deze
change legt alleen de bron en het contract vast.
