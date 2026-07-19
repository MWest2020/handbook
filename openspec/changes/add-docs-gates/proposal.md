# Change: add-docs-gates

## Why

De docs-gates draaien nu alleen centraal: `check_contract.py` en
`check_freshness.py` in de handbook-CI, plus de nightly rebuild. Een spoke-PR
die het contract breekt of docs laat achterlopen wordt dus pas rood in een
ánder repo, uren tot een dag later, buiten de PR waar de fix nog goedkoop was.

Bewijs (2026-07-19, habitat): de README beschreef een Squid-architectuur die al
vóór de bouw geschrapt was, en `explanation/architecture.md` droeg een
statustabel vol "nog te schrijven" naast een archief met diezelfde changes
afgerond — en dat passeerde béide bestaande gates (vorm klopte, front matter
klopte, jonger dan 180 dagen). Vorm-checks vangen geen inhoudelijke drift.
De industrie-norm is shift-left: dezelfde check draait als gate in het repo
dat de wijziging produceert, op het moment van de PR.

## What changes

- **Reusable workflow `.github/workflows/docs-gates.yml`** in dit repo
  (`workflow_call`), met twee gates per spoke-PR:
  1. *contract-gate*: de bestaande `check_contract.py` op de werkkopie van de
     spoke zelf (nieuwe `--repo-dir`-modus; zelfde checker, geen kopie);
  2. *drift-gate*: raakt de PR geconfigureerde code-paden zonder dat
     `docs/**` meebeweegt → fail, tenzij expliciete zichtbare override
     (PR-label `docs-drift-ok`). Puur padgebaseerd, geen inhoudsanalyse.
- **Caller-template** (±12 regels) voor spokes; per spoke alleen de eigen
  `code_paths` en `drift_mode` (warn|fail).
- **Uitrol** naar de vijf homelab-spokes (habitat, homelab, wordsworth,
  zettelkast, skill-forge) via habitat-builder-Jobs, zoals de contract-seeds.
- **Documentatie**: één reference-pagina in `docs/` van dit repo;
  inventaris-notes bijgewerkt na uitrol.

## Impact

- Spokes krijgen één extra verplichte PR-check; wie code en docs in dezelfde
  change meebeweegt (de afspraak) merkt er niets van.
- Handbook-CI en nightly blijven ongewijzigd als vangnet (spokes wijzigen ook
  buiten PR's om); de hub blijft eigenaar van de checker.
- Geen wijziging aan importlijst of validatielogica van de hub-build.
