---
status: current
last_reviewed: 2026-09-22
---

# Docs gates (spoke PR checks)

Two checks that run in a spoke's pull request and keep the docs in step with
the behaviour. The implementation lives in the hub
(`scripts/check_contract.py`, `scripts/check_drift.py`,
`.github/workflows/docs-gates.yml`); spokes call the reusable workflow, so an
outdated per-repo copy can never come into being.

## What they do

- **Contract gate** — runs the contract checker against the PR's working copy:
  `docs/index.md` exists, markdown only in `how-to/`, `reference/` or
  `explanation/`, and every page has front matter (`status` +
  `last_reviewed`, no `owner`). Without a `docs/` directory the gate does not
  apply.
- **Drift gate** — if the PR touches configured code paths without anything
  moving under `docs/`, the check fails. Purely path-based; no content
  analysis. The way out for a genuine exception is the PR label
  `docs-drift-ok` (visible, and countable afterwards).

The hub CI and the nightly rebuild remain as a safety net; the gates only pull
the check forward, into the PR where the fix is still cheap.

## Wiring it up (caller template)

Put this in the spoke's `.github/workflows/docs-gates.yml`:

```yaml
name: docs-gates
on:
  pull_request:
    types: [opened, synchronize, reopened, labeled, unlabeled]
jobs:
  gates:
    uses: MWest2020/handbook/.github/workflows/docs-gates.yml@main
    with:
      # code paths that require a docs change (dir/ = prefix)
      code_paths: "dispatch/,worker/,cage/,report/,orchestrator/"
      # where THIS repo's documentation lives; defaults to docs/
      docs_paths: "docs/"
      drift_mode: "fail"   # or "warn" while settling in
```

Choose `code_paths` per repo: the directories holding production behaviour,
not tests, CI or docs.

**Only set `docs_paths` if your documentation lives somewhere else.** The
default `docs/` is the contract and is right for almost every spoke. homelab is
the exception: it writes its runbooks in `docusaurus/docs/` and also had a
`docs/` that had been standing still since August. The drift gate therefore
pointed at the dead tree — unsatisfiable by writing real documentation, only by
touching the wrong directory or using the label.

That is worse than a missing gate. A gate you cannot pass honestly teaches
people to route around it, and after that it does nothing where it *is* right
either.

**Enforcement (solo repos).** These repos have a single maintainer, so the
gates run as a *signal* rather than a hard block: no branch protection, and
`drift_mode: fail` everywhere. Without branch protection, `fail` blocks
nothing — it gives an honest red X when the docs lag, after which you fix it or
apply the label. `warn` is pointless then (always green, drift or not) and is
only meant as temporary damping while settling in. In a team context branch
protection is what makes the check genuinely blocking; on a solo repo that is
ceremony.

## When the label is justified

`docs-drift-ok` is for a code change with demonstrably no docs impact (an
internal refactor, a bugfix with no outward behaviour change). It is not a
general escape hatch: if the label shows up often, either `code_paths` is
wrong or the docs are structurally behind.
