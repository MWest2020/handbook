## 1. Definitie

- [x] 1.1 `docs/agents/roodteam.md` aanmaken met front matter: `status: actief`,
      `last_reviewed` op de dag van de change, en `agent:` met `naam: roodteam`,
      `npub: null`, een chat-facet (`channels: [red-team, review]`,
      `tools: { allow: [], deny: [] }`, `skills: [thinking-red-team]`) en géén
      executie-facet.
- [x] 1.2 Body volgens het patroon van `docs/agents/bouwer.md`: `# roodteam`,
      `## Mandaat`, `## Chat-facet (boomhuis · #red-team, #review)` met de
      systemprompt in een codeblok, en een `## Executie-facet`-sectie die
      expliciet "geen" zegt met de reden (het `security`-seed dekt de kooi-rol).
- [x] 1.3 Mandaat en systemprompt **letterlijk** overnemen uit `proposal.md`.
      Geen herformulering, geen toevoegingen, geen weggelaten regels — in het
      bijzonder blijft "BREACH (only when explicitly asked ...)" intact.
- [x] 1.4 `docs/agents/index.md` bijwerken als daar een opsomming van agents staat.

## 2. Gate

- [x] 2.1 `uv run scripts/check_agent_tools.py` groen.
- [x] 2.2 `uv run scripts/check_freshness.py` — geen nieuwe waarschuwing voor dit bestand.
- [x] 2.3 `uv run scripts/gen_agent_seeds.py --check` groen (deze change raakt geen seeds).
- [x] 2.4 Niets anders gewijzigd: geen `agents/`-seeds, geen `inventory/`, geen CI,
      geen `CLAUDE.md`.
