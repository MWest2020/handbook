# Change: add-agent-tool-skill-contract

## Why

Een agent-definitie zegt vandaag niet gestructureerd wélke tools een rol mag
gebruiken en welke expliciet niet, en niets over relevante skills. De tools staan
als proza in het executie-facet ("Tools read-only (`Read, Bash, Grep, Glob`)"),
terwijl de afgeleide seed een losse `tools:`-allowlist heeft. Gevolg:

- "reviewer is read-only" en "security schrijft nooit" zijn beloftes in proza,
  niet machine-checkbaar. Een seed die per ongeluk `Write` toevoegt wordt niet
  gevangen door een tegenspraak met de definitie.
- Er is geen plek waar staat wélke tools een rol juist NIET mag (deny). Mark wil
  dat expliciet zien ("welke tools wel niet"), niet als complement-in-je-hoofd.
- Skills komen nergens voor, terwijl sommige rollen een duidelijke skill hebben
  (security ↔ red-team).

## What changes

- **Front-matter-contract uitgebreid.** Elk niet-leeg facet (`agent.chat` /
  `agent.executie`) krijgt gestructureerd:
  - `tools.allow: [...]` — de toegestane tools.
  - `tools.deny: [...]` — de expliciet geweigerde tools (maakt "read-only"
    checkbaar; leeg = niets expliciet verboden).
  - `skills: [...]` — relevante skills (leeg = geen).
- **Retrofit** van de bestaande agent-defs (`docs/agents/*.md`) met deze velden;
  de proza-`Tools:`-regels verwijzen voortaan naar het front-matter als bron.
- **Consistentie-tie met de seeds.** Voor elke executie-rol met een seed
  (`docs/agents/seeds/<rol>.md`) SHALL `executie.tools.allow` gelijk zijn aan de
  `tools:`-regel van de seed — de allowlist die habitat daadwerkelijk uitvoert.
- **Gate.** `scripts/check_agent_tools.py` (stdlib-only, geen yaml-dep) faalt als
  een facet het contract mist, allow/deny overlappen, of een seed-`tools:` afwijkt
  van `executie.tools.allow`. De CI-stap die 'm in `handbook.yml` inhaakt wordt
  door Mark met de hand toegevoegd (CI-config is een human-gate; deze PR raakt CI
  niet), precedent a1c3ebc.
- **CHANGELOG**-entry.

Downstream-consumptie (habitat die `deny` als `--disallowedTools` doorgeeft; de
boomhuis-listener die `chat.tools`/`skills` toepast) is bewust vervolgwerk per
repo — net zoals `add-agent-registry` z'n consumptie uitstelt. Deze change legt
het contract + de afdwinging in de naaf vast.

## Impact

- Betrokken specs: `agent-registry` (nieuwe eis).
- Betrokken code: `docs/agents/*.md`, `docs/agents/index.md`,
  `scripts/check_agent_tools.py`, `CHANGELOG.md`. De CI-stap in
  `.github/workflows/handbook.yml` past Mark met de hand toe (buiten deze PR).
- Geen runtime-/kooiwijziging; puur declaratie + gate in de handbook.
