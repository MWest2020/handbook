# test-gate Specification

## Purpose
Do not merge without green verification: every imported spoke runs a `verify`
check on pull requests (unit tests where they exist, otherwise lint or
validation), under a uniform name and with counted coverage.
## Requirements
### Requirement: Every imported spoke has a verify check on pull requests

Every repo on the import list (`handbook_import: yes`) SHALL have a PR check
that tests the repo with a command suited to the kind of repo (unit tests where
they exist; otherwise lint or validation). New checks SHOULD be called `verify`
so that coverage is uniformly countable; an already existing equivalent check
under another name (wordsworth's `test` CI, for instance) counts too and need
not be renamed. The inventory SHALL track coverage in `verify_gate`
(`yes|no|n/a`).

Enforcement is a signal, not a block: no branch protection on the solo repos
(consistent with docs-gates).

#### Scenario: A spoke without a verify check

- WHEN an imported spoke has `verify_gate: no`
- THEN that counts as open work until a `verify` check runs on its pull
  requests

#### Scenario: A repo with no meaningful test suite

- WHEN a spoke cannot have unit tests (infra, loose scripts)
- THEN a lint or validation check counts as `verify` and `verify_gate` becomes
  `yes`; an empty or fake test suite is not allowed (`n/a` only when lint and
  validation are pointless too, decided explicitly)

#### Scenario: Failing tests block the merge decision

- WHEN the `verify` check on a pull request is red
- THEN that is the signal not to merge until tests or lint are green (the
  maintainer decides; no hard branch protection on solo repos)
