# Tasks: add-handbook-portal

Vereist: change 2 gemerged voor minimaal de NLnet-repos + homelab. Beantwoord
eerst de drie open vragen uit proposal.md.

## 1. Repos aanmaken

- [ ] 1.1 `handbook` repo op Codeberg (public), EUPL-1.2, deze openspec-map
      erin, `inventory/` erin.
- [ ] 1.2 `pages` repo (public, leeg op README na: "deploy target, niet
      handmatig bewerken").

## 2. Build

- [ ] 2.1 `pyproject.toml` via `uv` (mkdocs, mkdocs-material, multirepo-
      plugin, freshness-check als script). Lockfile committen.
- [ ] 2.2 `mkdocs.yml` (publiek): importlijst genereren uit
      `inventory/repos.json` waar `handbook_import: yes` en
      `sensitivity: public-ok`. Script `scripts/gen_imports.py` +
      CI-check dat mkdocs.yml en inventaris synchroon zijn.
- [ ] 2.3 `mkdocs.private.yml`: erft publiek, voegt private-only imports toe.
- [ ] 2.4 Overkoepelende pagina's: `index.md`, `conventies.md`,
      `homelab/herstel.md` (stub → private sectie).
- [ ] 2.5 `scripts/check_freshness.py`: warning >180 dagen, uitsluiting van
      `status: deprecated`. Bare output, geen ANSI/banners (CI-script).

## 3. CI/CD

- [ ] 3.1 Forgejo Actions workflow: lint (mkdocs build --strict) +
      freshness-check + import-sync-check op elke PR.
- [ ] 3.2 Deploy-job op main: publieke build naar `pages` repo pushen
      (deploy-token als repo-secret, minimale scope).
- [ ] 3.3 Nightly rebuild (cron in workflow) — spokes wijzigen buiten de hub om.
- [ ] 3.4 Private build: documenteer het commando (`uv run mkdocs build -f
      mkdocs.private.yml`); automatisering op de interne beheer-host pas na
      open vraag 3.

## 4. Sluitstuk

- [ ] 4.1 Placeholder-URLs in de `.mcp.json`'s van change 2 vervangen zodra
      het MCP-endpoint bestaat (aparte follow-up change; hier alleen een
      issue aanmaken in handbook: "add-handbook-mcp").
- [ ] 4.2 Kruislink: vanuit het handbook één verwijzing naar het GitHub-
      profiel-README en andersom. Eén link, geen dubbele bron.
- [ ] 4.3 Archive-change: verplaats deze openspec-changes naar
      `openspec/archive/` na oplevering, conform propose→apply→archive.
