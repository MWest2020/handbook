# Tasks: add-seed-derivation

- [ ] 1.1 Executie-facetten in `docs/agents/*.md` compleet maken tot volledige,
      canonieke rol-inhoud (builder/bouwer, reviewer, security, architect-plan)
- [ ] 1.2 `docs/agents/reviewer.md` + `security.md` toevoegen (executie-only,
      chat-facet leeg)
- [ ] 1.3 `scripts/gen_agent_seeds.py`: genereer per spoke
      `.claude/agents/<rol>.md` uit de executie-facetten; `uv`, bare script
- [ ] 1.4 Seeds regenereren met de generator (vervang de handmatige kopieën)
- [ ] 1.5 Drift-gate: CI-workflow die `gen_agent_seeds.py --check` draait en
      faalt bij afwijking tussen gecommitte seed en canonieke bron
- [ ] 1.6 `CHANGELOG.md` + spec-delta archiveren
- [ ] 1.7 Verificatie: bewuste afwijking in één seed → CI faalt; generator
      herstelt 'm exact

> Habitat-kant blijft ongewijzigd (leest de seed lokaal uit de doelrepo). Deze
> change verandert alleen de HERKOMST van die seed: afgeleid van de canonieke
> executie-facet i.p.v. met de hand gekopieerd.
