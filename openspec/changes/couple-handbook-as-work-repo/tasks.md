## 1. Koppeling

- [x] 1.1 `prep/seeds/handbook/.claude/agents/` aangemaakt en gevuld via
      `uv run scripts/gen_agent_seeds.py` (geen handwerk, geen afwijkende kopie).
- [x] 1.2 `.claude/agents/{builder,reviewer,security}.md` in de repo-root,
      byte-identiek aan `docs/agents/seeds/*.md`.
- [x] 1.3 `CLAUDE.md`: "Coördineren, niet bouwen" begrensd tot een interactieve
      sessie; gedispatchte rol volgt zijn rolbestand.

## 2. Gate

- [x] 2.1 `uv run scripts/gen_agent_seeds.py --check` groen (geen drift).
- [x] 2.2 `uv run scripts/check_agent_tools.py` groen.
- [x] 2.3 Overige hub-gates ongewijzigd: `check_contract.py` OK voor alle repo's;
      `check_freshness.py` meldt alleen de drie al bestaande seeds zonder
      `last_reviewed` (pre-existing, geen regressie); `check_drift.py` draait in CI
      met `--code-paths`.
- [ ] 2.4 CI groen op de PR.

## 3. Bewijs

- [ ] 3.1 Aantonen dat de rolinstructie nu vindbaar is op het pad dat de worker
      gebruikt (`.claude/agents/<rol>.md` in de kloon van deze repo).
- [ ] 3.2 Vervolgstap benoemd, niet gedaan: pas ná merge kan een dispatch op de
      handbook zinvol draaien.
