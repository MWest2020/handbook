# Change: add-skills-register-check

## Why

`add-agent-tool-skill-contract` gaf agent-defs een `skills:`-veld maar hield het
overal op `[]`: een concrete skill-naam was niet te valideren, want de handbook had
geen bron van "welke skills bestaan". skill-forge heeft nu (`forge register`) een
gezaghebbend manifest van gepromoveerde skills. Deze change laat de handbook dat
consumeren zodat een `skills:`-claim écht afdwingbaar wordt — net zo hard als de
tools.

## What Changes

- **Mirror** `inventory/skills-register.yml` — een gespiegelde kopie van
  skill-forge's `register.yml` (slug + description + origin). skill-forge blijft de
  bron; de handbook spiegelt, definieert niet.
- **Gate** `scripts/check_agent_tools.py` valideert elke `skills:`-entry tegen de
  slugs in het register: onbekende skill → FAIL; register ontbreekt terwijl een def
  niet-lege skills heeft → FAIL.
- **Herstel** `security` → `skills: [thinking-red-team]` (die skill is gepromoveerd
  in skill-forge, dus nu geldig) — het eerste echt gevulde skills-veld.
- Spec-delta op `agent-registry`, CHANGELOG.

**Bewust NIET in scope (vervolg):** dit valideert dat een gedeclareerde skill
*bestaat* (geen phantom-namen). Het *levert* de skill niet aan habitat: anders dan
tools (die via de seed als `--allowedTools` de kooi in gaan) bereikt een skill de
uitvoerende agent vandaag nog niet — de seed heeft geen `skills:` en niets mount de
SKILL.md. Skill-*provisioning* (seed-`skills:` + kooi-mount, met pariteit-check
zoals tools↔seed) is een eigen, grotere change. `skills:` is hier dus een
gevalideerde *intentie/declaratie*, geen runtime-garantie.

## Impact

- Betrokken specs: `agent-registry` (skills-validatie).
- Betrokken code: `inventory/skills-register.yml` (nieuw), `scripts/check_agent_tools.py`,
  `docs/agents/security.md`, `docs/agents/index.md`, `CHANGELOG.md`. Geen
  CI-config (human-gate); de CI-stap die de gate draait voegt Mark met de hand toe.
- Consumptie-only: geen wijziging aan skill-forge (die leverde de bron).
