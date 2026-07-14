# Change: add-handbook-mcp

## Why

Northstar 2: het handbook is DE ingang voor agents via MCP, en agents lezen
exact dezelfde importlijst als de site — geen tweede waarheid. De
`.mcp.json`'s in alle 17 spokes staan sinds change 2 op placeholder
`TODO-change-3`; dit is de invulling (issue #1).

## What changes

- **`handbook_mcp/`**: kleine read-only MCP-server (Python, stdio, FastMCP)
  in dit repo. Geen aparte hosting: spokes starten hem via
  `uvx --from git+https://github.com/MWest2020/handbook handbook-mcp`.
- **Drie tools, alle read-only**:
  - `list_repos()` — de importlijst uit `inventory/repos.json` (main),
    gefilterd op `handbook_import: yes` + `contract_applied: yes`;
  - `list_docs(repo)` — markdown-bestanden onder `docs/` van een
    geïmporteerd repo;
  - `read_doc(repo, path)` — inhoud van één docs-pagina.
- **Runtime-dependencies minimaal**: alleen `mcp`; de mkdocs-toolchain
  verhuist naar een dependency-group zodat `uvx` hem niet meesleept.
- **`.mcp.json` in alle 17 spokes + dit repo**: placeholder vervangen door
  de stdio-configuratie (rolt deze change uit, één PR per repo).

## Requirements (expliciet, zie spec-delta)

1. **Eén waarheid**: de server leest `inventory/repos.json` van `main` via
   GitHub raw — hetzelfde bestand waar `gen_imports.py` de site uit bouwt.
2. **Padbegrenzing**: alleen `docs/**/*.md` binnen repos die in de
   importlijst staan; genormaliseerde paden, geen `..`, geen absolute paden.
3. **Token-hygiëne**: geen credentials in code of `.mcp.json`; optioneel
   `GH_TOKEN` uit de omgeving voor private repos; tokens verschijnen nooit
   in tool-output of foutmeldingen.
4. **Read-only**: geen enkele tool muteert iets.

## Verify

Sessietest (script `scripts/test_mcp.py`): start de server over stdio,
initialiseert, roept alle drie tools aan (incl. een geweigerd pad en een
geweigerd repo) en faalt hard bij afwijkingen.
