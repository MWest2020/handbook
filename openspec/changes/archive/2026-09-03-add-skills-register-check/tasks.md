# Tasks: add-skills-register-check

- [x] 1.1 `inventory/skills-register.yml`: mirror van skill-forge's `forge register`.
- [x] 1.2 `scripts/check_agent_tools.py`: valideer `skills:` tegen het register-slugs.
- [x] 1.3 `docs/agents/security.md`: `skills: [thinking-red-team]` (nu geldig).
- [x] 1.4 CHANGELOG-entry.
- [x] 1.5 `check_agent_tools.py --selftest`: 7 logica-gevallen (geldige/onbekende
      skill, register-weg, lege skills, overlap, skills-ondanks-tools-weg) — de gate
      test zichzelf (northstar: geteste gates).
- [x] 1.6 Skills eerlijk gekaderd (intentie/bestaan, geen provisioning) in
      proposal/design/CHANGELOG; verversprocedure in docs/reference/bedieningsafspraken.md.
