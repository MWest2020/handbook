# handbook

Hub van het persoonlijke repo-ecosysteem (voorheen "Westmarch"): één plek
die de documentatie van alle persoonlijke repos at build time aggregeert,
naar het hub-and-spoke-model. Docs leven in de project-repos zelf
(`/docs`, Diátaxis-light contract); dit repo bevat alleen de kaart, de
specs en de pipeline.

- **Site**: publieke build → GitHub Pages
  (https://mwest2020.github.io/handbook/); de private build draait alleen
  waar zijn config staat (niet in dit repo):
  `GH_TOKEN=… uv run mkdocs build -f mkdocs.private.yml -d site-private`
- **Importlijst**: `inventory/repos.json` → `scripts/gen_imports.py` →
  `mkdocs.yml` (en de niet-getrackte private config waar aanwezig); CI
  faalt bij drift
- **Specs**: `openspec/` (northstar in `project.md`, changes met
  propose→apply→archive)
- **Checks**: `scripts/check_contract.py` (docs-contract per import),
  `scripts/check_freshness.py` (>180 dagen = waarschuwing)
- **Sessies**: Claude Code-sessies over het ecosysteem starten hier; zie
  `CLAUDE.md` voor het mandaat

Licentie: [EUPL-1.2](LICENSE).
