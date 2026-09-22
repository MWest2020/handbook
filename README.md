# handbook

Hub of the personal repo ecosystem (formerly "Westmarch"): one place that
aggregates the documentation of every personal repo at build time, following
the hub-and-spoke model. Docs live in the project repos themselves (`/docs`,
Diátaxis-light contract); this repo holds only the map, the specs and the
pipeline.

- **Site**: public build → GitHub Pages
  (https://mwest2020.github.io/handbook/); the private build runs only where
  its config lives (not in this repo):
  `GH_TOKEN=… uv run mkdocs build -f mkdocs.private.yml -d site-private`
- **Import list**: `inventory/repos.json` → `scripts/gen_imports.py` →
  `mkdocs.yml` (and the untracked private config where present); CI fails on
  drift
- **Specs**: `openspec/` (northstar in `project.md`, changes follow
  propose → apply → archive)
- **Checks**: `scripts/check_contract.py` (docs contract per import),
  `scripts/check_freshness.py` (>180 days = warning)
- **Sessions**: Claude Code sessions about the ecosystem start here; see
  `AGENTS.md` for the mandate

License: [EUPL-1.2](LICENSE).
