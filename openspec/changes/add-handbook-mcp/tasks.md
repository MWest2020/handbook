# Tasks: add-handbook-mcp

- [x] 1.1 `handbook_mcp/` package: FastMCP-server met list_repos/list_docs/
      read_doc, padbegrenzing en token-hygiëne volgens spec-delta.
- [x] 1.2 `pyproject.toml`: script-entry `handbook-mcp`; runtime-deps
      minimaal (`mcp`); mkdocs-toolchain naar dependency-group `docs`
      (default-group, zodat CI ongewijzigd blijft); lockfile bijwerken.
- [x] 2.1 Sessietest `scripts/test_mcp.py` (stdio, echte server): happy path
      per tool + geweigerd pad + geweigerd repo. Draait in CI.
- [x] 2.2 `.mcp.json` in dit repo: handbook-server via `uv run handbook-mcp`
      (lokale checkout) — sessies die hier starten gebruiken de bron direct.
- [ ] 3.1 Rol de stdio-configuratie uit naar alle 17 spokes (placeholder
      `TODO-change-3` vervangen), één PR per repo.
- [ ] 4.1 Issue #1 sluiten met verwijzing; change archiveren
      (propose→apply→archive).
