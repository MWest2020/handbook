---
status: current
last_reviewed: 2026-09-22
---

# Conventions

## Docs contract (Diátaxis-light)

Every participating repo has a `docs/` directory with `index.md` at its root
and markdown only in that root or in `how-to/`, `reference/` and
`explanation/` (ADRs under `explanation/adr/NNNN-title.md`). Every page
carries front matter with `status` (current | draft | deprecated) and
`last_reviewed` (ISO date); an `owner` field is forbidden. Minimum viable:
`index.md` plus one reference page.

**One language, and that language is English** — repo content, docs, code and
commit messages alike. Dutch was allowed for private and homelab repos until
2026-09-21; that exception is gone, because working in two languages is how
Dutch ends up in code. A Dutch-language *deliverable* for a Dutch audience is a
different thing and stays fine.

The full specification lives in
[`openspec/archive/2026-07/add-docs-contract/`](https://github.com/MWest2020/handbook/tree/main/openspec/archive/2026-07/add-docs-contract);
`scripts/check_contract.py` enforces the contract in CI.

## Import list

`inventory/repos.json` is the single source of truth about which repos take
part. `scripts/gen_imports.py` generates the mkdocs import blocks from it; CI
fails on drift. Agents (MCP, planned) read the same list — there is no second
truth.

## Licences and tooling

- **EUPL-1.2** for public content, unless a repo is already licensed
  otherwise (deviations are recorded in the inventory notes).
- **Python through `uv`**, never pip directly.
- Boring and auditable: standard tooling, explicit configuration, every
  decision traceable to a proposal or an ADR.

## Public and private

Separated by sensitivity rather than by subject, and at repo level: a repo is
public-ok or private-only; per-page filters do not exist. The private build
(`mkdocs.private.yml`, not tracked in this repo) runs on the administration
host and never goes to Pages.
