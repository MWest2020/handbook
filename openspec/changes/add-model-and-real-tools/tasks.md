## 1. Definities

- [x] 1.1 `model` per facet in alle tien defs, volgens Marks mapping.
- [x] 1.2 Chat-facetten: `allow: [Read, Grep, Glob]`, `deny: [Write, Edit, Bash]`.
- [x] 1.3 Seeds (`builder`, `reviewer`, `security`) krijgen `model:` + `skills:`;
      afgeleide seeds geregenereerd met `gen_agent_seeds.py`.

## 2. Gate

- [x] 2.1 `model` verplicht en uit `{haiku, sonnet, opus}`.
- [x] 2.2 `executie.model` gekruist met de seed.
- [x] 2.3 Negatieftest: ontbrekend model → FAIL; afwijkend seed-model → FAIL;
      daarna hersteld en groen.
- [x] 2.4 `gen_agent_seeds.py --check` groen (geen drift).

## 3. Spec

- [x] 3.1 Delta op `agent-registry`: model verplicht, seed-kruising, seeds dragen
      model + skills.

## 4. Gate (CI)

- [x] 4.1 `openspec validate add-model-and-real-tools --strict` groen.
- [ ] 4.2 CI groen op de PR.
