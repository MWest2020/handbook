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
- [x] 2.4 CI groen op de PR (#10, alle checks pass).

## 3. Bewijs

- [x] 3.1 Aangetoond met een verse `git clone --depth 50` van deze branch (dezelfde
      stap die de worker doet): `.claude/agents/{builder,reviewer,security}.md`
      resolven alle drie. Op `main` bestaat de map niet — precies de blokkade.
- [x] 3.2 De vervolgstap is intussen ook echt gebeurd: er heeft een habitat-run
      op de handbook gedraaid. Bewijs in de geschiedenis van deze repo — commit
      91ff6e9 (`add-agent-roodteam`, PR #11) voegde `.habitat/`-artefacten toe, en
      die kunnen alleen uit een run komen. Daarmee is aangetoond waar deze change
      voor bedoeld was: de naaf is een werk-repo.
