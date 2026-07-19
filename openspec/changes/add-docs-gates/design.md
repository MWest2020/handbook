# Design — docs-gates

## Beslissingen

### Gate bij de bron, checker bij de hub (clevere valkuil)
De valkuil is de checker per spoke kopiëren: vijf kopieën die stuk voor stuk
verouderen — drift ín de drift-gate. Daarom een `workflow_call`-workflow in
dit repo die de spokes aanroepen met `uses:
MWest2020/handbook/.github/workflows/docs-gates.yml@main`; de workflow haalt
`check_contract.py` uit de hub-checkout. Eén implementatie, vijf gebruikers.

### `--repo-dir` in check_contract.py, geen tweede script
`check_repo()` bestaat al en is puur (pad in, fouten uit). Eén nieuwe vlag
`--repo-dir PATH` draait die functie op een lokale werkkopie zonder clone en
zonder inventaris. De multi-import-modus (hub-CI, nightly) blijft onaangeroerd.

### Drift-gate: padgebaseerd, dom met opzet
`git diff --name-only` over de PR-range: raakt de diff één van de opgegeven
`code_paths`-globs en géén `docs/**` → fail. Geen inhoudsanalyse, geen LLM,
geen heuristiek — die zijn niet-deterministisch en dus niet auditeerbaar als
gate. Vals-positieven (echte code-wijziging zonder docs-impact) krijgen een
expliciete uitweg: PR-label `docs-drift-ok`, zichtbaar en achteraf te tellen.
Per spoke instelbaar `drift_mode: warn|fail` (default `fail`); een spoke die
het patroon nog inregelt kan op `warn` starten.

### Wat deze change NIET doet
- Geen automatische her-aggregatie bij spoke-merge — de nightly dekt dat;
  event-gedreven rebuilds zijn een eigen change als de vertraging ooit knelt.
- Geen wijziging aan reviewer-rollen in spokes (`.claude/agents/` is voor
  agents een verboden pad; die ene regel is aan Mark).
- Geen docs-generatie. Gates dwingen af dat mensen/agents docs meebewegen;
  ze schrijven ze niet.

## Verificatie (DoD)
Testmatrix via één spoke-PR-reeks (habitat):
1. contractbreuk (pagina zonder front matter) → gate rood;
2. code-wijziging zonder docs → gate rood;
3. zelfde PR mét label `docs-drift-ok` → groen, label zichtbaar;
4. code + docs samen → groen.
Daarna uitrol naar de overige vier spokes; alle vijf tonen de check verplicht.
