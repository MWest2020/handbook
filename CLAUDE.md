# handbook — hub van het persoonlijke ecosysteem

Dit repo is de coördinatie-hub: specs (`openspec/`), inventaris
(`inventory/`), importlijst (mkdocs) en het startpunt voor Claude
Code-sessies over het hele persoonlijke ecosysteem. Er is bewust géén
apart hub-repo (verschil met de werkopzet): één eigenaar, één hub.

## Rol van een sessie die hier start

- **Coördineren, niet bouwen.** Bouwwerk aan spokes loopt via habitat-Jobs
  (`dispatch.sh <rol> <change> <repo>` vanaf een host met kubectl; zie
  habitat `docs/reference/dispatch.md`). Reviewer/security altijd met
  `HABITAT_BASE_BRANCH=habitat/builder/<change>`.
- **De inventaris is de enige waarheid.** `inventory/repos.json` bepaalt wat
  meedoet (site én agents). Wijzigingen aan de importlijst gaan via
  `scripts/gen_imports.py`, nooit met de hand.
- **Voorstel-eerst.** Nieuwe changes/repos/entiteiten ontstaan via een
  openspec-proposal onder `openspec/changes/`, nooit impliciet.
- **Escalatie.** Niet in een proposal of dit mandaat beschreven = eerst
  vragen. Eén herstart per mislukte habitat-run zonder mens;
  security-FAIL of gemeld geheim → altijd mens.

## Invarianten

- `openspec/private/` is gitignored en bevat homelab-identifiers — nooit
  committen, nooit citeren in publieke output (repos, PR's, docs).
- Geen secrets in dit repo, ook niet in voorbeelden; tokens via env.
- Publiek/privaat is gescheiden op repo-niveau; de private mkdocs-build
  gaat nooit naar Pages.
- Python via `uv`, nooit pip. Bare CI-scripts (geen ANSI/banners).
