# Tasks: add-agent-tool-skill-contract

- [x] 1.1 `design.md`: het front-matter-contract voor `tools.allow/deny` + `skills` per facet vastleggen.
- [x] 1.2 Retrofit `docs/agents/*.md`: `tools.allow/deny` + `skills` per niet-leeg
      facet (9 defs incl. archivaris; index.md valt buiten).
- [x] 1.3 `scripts/check_agent_tools.py`: gate die faalt bij ontbrekend veld,
      allow/deny-overlap of seed-`tools:`-mismatch met `executie.tools.allow`.
- [ ] 1.4 CI-stap (gate in `handbook.yml`) — HAND-toegepast door Mark als hub-commit
      (CI-config is een human-gate; een gekooide bouwer wijzigt geen CI). Precedent:
      a1c3ebc. Snippet staat in de PR-omschrijving.
- [x] 1.5 `CHANGELOG.md`: entry (expliciete tools allow/deny + skills per facet,
      afgedwongen).
- [x] 1.6 `uv run scripts/check_agent_tools.py` slaagt lokaal op de retrofitte
      defs; een bewust foutieve def/seed laat 'm falen (rooktest).
