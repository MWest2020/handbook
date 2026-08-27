# Change: add-seed-derivation

## Why

`add-agent-registry` legde de canonieke agent-definities vast in `docs/agents/`
en koppelde boomhuis eraan (de chat-listener leest de chat-facet uit de
handbook). De **habitat-kant** is nog niet gesloten: de per-spoke executie-rollen
staan als **met de hand gekopieerde** `prep/seeds/*/.claude/agents/*.md` — byte-
identiek nu, maar niets dwingt af dat ze de canonieke **executie-facet** volgen.
Zolang dat handwerk is, kan een `builder` op één spoke stilletjes afwijken van
"de builder". Dat is precies de drift die de registry moet uitsluiten.

## What changes

- **`docs/agents/*.md` executie-facetten compleet maken**: de executie-facet van
  elke rol (builder=bouwer, reviewer, security, architect-plan) wordt de
  volledige, canonieke rol-inhoud — niet langer een samenvatting.
- **`scripts/gen_agent_seeds.py`**: genereert per spoke de
  `.claude/agents/<rol>.md`-seeds **uit** de canonieke executie-facetten. De
  seeds worden afgeleid, nooit met de hand geschreven.
- **Drift-gate (CI)**: een check die faalt als een gecommitte seed afwijkt van
  wat de generator uit de canonieke bron zou produceren. Enforcement, geen
  afspraak — spiegelt de boomhuis-runtime-read (geen lokale kopie om te driften).
- **`docs/agents/reviewer.md`, `security.md`**: executie-only definities
  toevoegen (chat-facet leeg) zodat de volledige rollenset canoniek is.

## Non-goals

- **Geen wijziging aan habitat's kooi** (NetworkPolicies, RBAC, Job-templates,
  worker). Habitat blijft de rol-definitie uit de doelrepo lezen; alleen de
  herkomst van die seed verandert (afgeleid i.p.v. gekopieerd).
- Geen runtime-koppeling habitat→handbook in deze change; de seed blijft in de
  doelrepo staan (habitat leest lokaal). De bron-van-waarheid is de handbook via
  generatie + gate.
- Geen wijziging aan de boomhuis-koppeling (die is al runtime-read).

## Impact

- Nieuw: `scripts/gen_agent_seeds.py`, een CI-workflow (drift-gate),
  `docs/agents/reviewer.md` + `security.md`, aangevulde executie-facetten.
- Herschreven (gegenereerd): `prep/seeds/*/.claude/agents/*.md`.
- `CHANGELOG.md`. Spec-delta op `agent-registry` (executie-facet is bron van de
  seeds; drift-gate).
