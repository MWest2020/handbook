# docs-gates Specification

## Purpose
Keep docs in step with behaviour per spoke pull request: a contract check
(shape) and a drift check (code ↔ docs), as a signal in the PR where the fix is
still cheap.
## Requirements
### Requirement: The contract gate runs in the spoke's pull request

Every repo on the import list (`handbook_import: yes`) SHALL validate the docs
contract as a check on its own pull requests, using the same checker the hub
uses (called through the hub's reusable workflow, not as a copy). The hub CI
and the nightly rebuild remain as a safety net.

#### Scenario: A contract breach in a spoke pull request

- WHEN a spoke pull request adds or changes a docs page that breaks the
  contract (no front matter, markdown outside the Diátaxis directories)
- THEN the contract gate fails in *that* pull request, before merge

#### Scenario: The checker changes at the hub

- WHEN the hub tightens the contract checker
- THEN the tightening applies on the next spoke pull request without any spoke
  having to update anything

### Requirement: The drift gate ties code to docs

A spoke pull request that touches configured code paths SHALL fail when
`docs/**` does not move with it in the same pull request, unless the pull
request carries an explicit, visible override (the label `docs-drift-ok`). The
gate SHALL be path-based and deterministic (no content analysis). Spokes MAY
set the gate to `warn` while settling in; the default is `fail`.

#### Scenario: Code changes, docs do not

- WHEN a pull request changes paths from `code_paths` and no file under `docs/`
- THEN the drift gate fails with a message pointing at the agreement that the
  two move together

#### Scenario: A deliberate exception

- WHEN that same pull request carries the label `docs-drift-ok`
- THEN the drift gate passes, and the exception stays visible and countable as
  a label in the pull request history
