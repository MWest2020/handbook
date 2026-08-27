## ADDED Requirements

### Requirement: Eén canonieke definitie per agent-rol

Elke agent-rol SHALL precies één canonieke definitie hebben, in de handbook
onder `docs/agents/<naam>.md`; geen enkele andere plek (spoke-seeds,
boomhuis-config) SHALL een rol her-definiëren — die consumeren de canonieke
bron.

#### Scenario: Wijziging bereikt iedereen

- **WHEN** de definitie van een rol (bijv. `bouwer`) in de handbook wijzigt
- **THEN** lezen alle consumenten (boomhuis-chat, habitat-executie) die
  gewijzigde definitie, zonder dat er een kopie handmatig bijgewerkt hoeft

#### Scenario: Geen tweede waarheid

- **WHEN** iemand een rol op een andere plek dan `docs/agents/` probeert vast te
  leggen als bron
- **THEN** is dat volgens dit contract geen geldige bron; die plek hoort te
  verwijzen naar of af te leiden van de canonieke definitie

### Requirement: Twee facetten in één definitie

Een definitie SHALL een machine-leesbaar front-matter bevatten met minstens
`naam` en `npub`, plus een **chat-facet** (systemprompt + kanaal-scope) en een
**executie-facet** (kooi-rol/tools/schema, of expliciet leeg). Een consument
SHALL alleen zijn eigen facet gebruiken.

#### Scenario: Boomhuis leest de chat-facet

- **WHEN** de boomhuis-listener een agent draait
- **THEN** haalt hij systemprompt en kanaal-scope uit de chat-facet van de
  canonieke definitie, niet uit een eigen kopie

#### Scenario: Chat-only of executie-only

- **WHEN** een rol alleen chat is (assistent) of alleen executie (security)
- **THEN** is het andere facet expliciet leeg, en de definitie blijft geldig

### Requirement: MCP-leesbaar zonder nieuwe machinerie

De definities SHALL via de bestaande `handbook_mcp`-tool `read_doc` leesbaar
zijn (pad `docs/agents/**/*.md`), zodat elke agent de canonieke bron kan
opvragen; deze change SHALL geen nieuwe MCP-tool of guard-versoepeling vereisen.

#### Scenario: Agent vraagt zijn definitie op

- **WHEN** een agent `read_doc("handbook", "docs/agents/bouwer.md")` aanroept
- **THEN** krijgt hij de canonieke definitie terug, binnen de bestaande
  padbegrenzing en token-hygiëne van de MCP-laag
