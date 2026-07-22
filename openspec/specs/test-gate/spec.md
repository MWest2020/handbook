# test-gate Specification

## Purpose
Niet mergen zonder groene verificatie: elke import-spoke draait een
`verify`-check op PR's (unit-tests waar die bestaan, anders lint/validatie),
met uniforme naam en getelde dekking.
## Requirements
### Requirement: Elke import-spoke heeft een verify-check op PR's

Elk repo op de importlijst (`handbook_import: yes`) SHALL een PR-check hebben
die de repo controleert met een commando dat bij het repo-type past (unit-tests
waar die bestaan; anders lint/validatie). Nieuwe checks SHOULD `verify` heten
zodat dekking uniform telbaar is; een reeds bestaande, equivalente check onder
een andere naam (bv. wordsworth's `test`-CI) telt ook en hoeft niet hernoemd te
worden. De inventaris SHALL de dekking bijhouden in `verify_gate` (`yes|no|n/a`).

Handhaving is signaal, niet blokkade: geen branch protection op de solo-repo's
(consistent met docs-gates).

#### Scenario: Spoke zonder verify-check

- WHEN een import-spoke `verify_gate: no` heeft
- THEN geldt dat als openstaand werk tot er een `verify`-check op PR's draait

#### Scenario: Repo zonder zinvolle testsuite

- WHEN een spoke geen unit-tests kan hebben (infra, losse scripts)
- THEN telt een lint-/validatiecheck als `verify` en wordt `verify_gate: yes`;
  een lege of nep-testsuite is niet toegestaan (`n/a` alleen als ook lint/
  validatie zinloos is, expliciet besloten)

#### Scenario: Falende tests blokkeren de merge-beslissing

- WHEN de `verify`-check op een PR rood is
- THEN is dat het signaal om niet te mergen tot tests/lint groen zijn (de
  beheerder beslist; geen harde branch protection op solo-repo's)

