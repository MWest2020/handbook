# Change: mcp-hub-self-read

## Why

Agents die via handbook-mcp het ecosysteem lezen kunnen elk geïmporteerd
spoke-repo bevragen, maar niet de hub zelf: `read_doc("handbook", ...)` wordt
geweigerd omdat de importfilter (`handbook_import: yes` + `contract_applied:
yes`) ook de MCP-laag bepaalt en de hub bewust `handbook_import: no` heeft
("importeert zichzelf niet" — site-semantiek: zelf-import zou de eigen
`docs/` als sectie in de eigen build trekken). Gevolg: juist de docs die het
ecosysteem beschrijven (conventies, hub-index) zijn voor agents onzichtbaar.
Geconstateerd 2026-07-22 vanuit een zettelkast-sessie; besluit Mark: hub
leesbaar maken.

## What changes

- `handbook_mcp`: de hub (`handbook`) is altijd onderdeel van de ontsloten
  set, als expliciete code-exceptie — de inventarisvlaggen blijven puur
  site-semantiek. `list_repos` toont de hub mee; `list_docs`/`read_doc`
  werken op `docs/**/*.md` van de hub zoals bij elke spoke.
- `scripts/test_mcp.py`: assertie omgedraaid (hub MOET in `list_repos`) en
  een leescheck op `handbook docs/index.md` toegevoegd.
- `inventory/repos.json`: notes van de hub-rij aangevuld zodat de uitzondering
  daar vindbaar is; `handbook_import` blijft `no`.
- Spec-delta op `handbook-mcp` requirement "Eén waarheid" (hub-uitzondering).

## Non-goals

- Geen wijziging aan de site-import (mkdocs blijft zichzelf niet importeren).
- Geen wijziging aan padbegrenzing, token-hygiëne of read-only-gedrag.
- Geen docs-contract-migratie van de hub-`docs/` (staat los; `contract_applied`
  blijft `no` tot die migratie echt gebeurt).

## Impact

- `handbook_mcp/__init__.py`, `scripts/test_mcp.py`, `inventory/repos.json`,
  `CHANGELOG.md`.
- Spokes merken het na merge naar main vanzelf (uvx haalt de server van main;
  de inventaris wordt per aanroep van main gelezen).
