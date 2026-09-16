---
status: current
last_reviewed: 2026-07-20
---

# Docs-gates (spoke-PR-checks)

Twee checks die in een spoke-PR draaien en de docs bij het gedrag houden. De
implementatie leeft in de hub (`scripts/check_contract.py`,
`scripts/check_drift.py`, `.github/workflows/docs-gates.yml`); spokes roepen de
reusable workflow aan, zodat er nooit een verouderde kopie per repo ontstaat.

## Wat ze doen

- **Contract-gate** — draait de contract-checker op de werkkopie van de PR:
  `docs/index.md` bestaat, markdown alleen in `how-to/`, `reference/`,
  `explanation/`, en elke pagina heeft front matter (`status` + `last_reviewed`,
  geen `owner`). Zonder `docs/` is de gate niet van toepassing.
- **Drift-gate** — raakt de PR geconfigureerde code-paden zonder dat er iets
  onder `docs/` meebeweegt, dan faalt de check. Puur padgebaseerd, geen
  inhoudsanalyse. Uitweg voor een terechte uitzondering: het PR-label
  `docs-drift-ok` (zichtbaar en achteraf telbaar).

De hub-CI en de nightly rebuild blijven als vangnet bestaan; de gates zetten de
check alleen naar voren, in de PR waar de fix nog goedkoop is.

## Aanhaken (caller-template)

Plaats in de spoke `.github/workflows/docs-gates.yml`:

```yaml
name: docs-gates
on:
  pull_request:
    types: [opened, synchronize, reopened, labeled, unlabeled]
jobs:
  gates:
    uses: MWest2020/handbook/.github/workflows/docs-gates.yml@main
    with:
      # code-paden die een docs-wijziging vereisen (map/ = prefix)
      code_paths: "dispatch/,worker/,cage/,report/,orchestrator/"
      # waar de documentatie van DEZE repo woont; default docs/
      docs_paths: "docs/"
      drift_mode: "fail"   # of "warn" tijdens inregelen
```

Kies `code_paths` per repo: de mappen met productiegedrag, niet tests/CI/docs.

**`docs_paths` alleen zetten als je documentatie ergens anders staat.** De
default `docs/` is het contract en klopt voor bijna elke spoke. homelab is de
uitzondering: die schrijft zijn runbooks in `docusaurus/docs/` en had daarnaast
een `docs/` die sinds augustus stilstond. De drift-gate wees daarmee naar de dode
boom — niet te halen door échte documentatie te schrijven, alleen door de
verkeerde map aan te raken of het label te gebruiken.

Dat is erger dan een gate die ontbreekt. Een gate die je niet eerlijk kunt halen,
leert mensen hem te omzeilen, en daarna doet hij ook niets meer waar hij wél
klopt.

**Handhaving (solo-repo's).** Deze repo's hebben één beheerder, dus de gates
draaien als *signaal*, niet als harde blokkade: geen branch protection, en
`drift_mode: fail` overal. Zonder branch protection blokkeert `fail` niets — het
geeft een eerlijke rode X als de docs achterlopen, waarna jij fixt of het label
zet. `warn` is dan zinloos (altijd groen, ook bij drift) en alleen bedoeld als
tijdelijke demping tijdens inregelen. In een team-context maakt branch
protection de check pas écht blokkerend; op een solo-repo is dat ceremonie.

## Wanneer het label gerechtvaardigd is

`docs-drift-ok` is voor een code-wijziging die aantoonbaar geen docs-impact
heeft (een interne refactor, een bugfix zonder gedragswijziging naar buiten).
Het is geen algemene ontsnapping: staat het label er vaak, dan klopt óf
`code_paths` niet, óf de docs lopen structureel achter.
