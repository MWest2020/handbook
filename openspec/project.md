# Project: Personal Handbook (hub-and-spoke docs for personal projects + homelab)

## Goal

One handbook as the aggregation point for every personal repo (open-source
projects and homelab alike), modelled on the Conduction techbook but scaled to a
single owner. Documentation lives in the project repos themselves (`/docs`);
the handbook aggregates at build time through one import list. No copies, no
drift.

## Northstar

This is the full Conduction model, not a slimmed-down version; the hub gains
capabilities over time, so the gates weigh more heavily rather than less.

1. **Proven sync before every push.** Working on a repo means: before every
   push it is proven that the docs are in sync with the code *and* that the
   repo's functionality works (unit tests / dry runs) — both through gates that
   are themselves tested. Documentation claims will eventually be verified
   executably (docs claims).
2. **The handbook is THE entrance for agents via MCP.** Site and agents read
   exactly the same import list; there is no second truth.
3. **Agents pinned down for idempotent operation.** One operations catalogue
   per repo (`docs/agents.md`) with autonomy levels (autonomous /
   human-required / forbidden), the creation rule (new entities are always
   proposal-first), the escalation rule (not in the catalogue = ask first), and
   GET-check-first as house style.

## Starting points (non-negotiable)

- **Boring and auditable.** Standard tooling (mkdocs), explicit configuration,
  no cleverness. Every decision traceable to an ADR or a proposal.
- **One source of truth.** The import list in the handbook (`mkdocs.yml`) is the
  only place that decides which repos take part. Agents (MCP) read the same
  list.
- **Docs next to the code.** Every participating repo has `/docs` following the
  contract (see change `add-docs-contract`). The handbook itself holds no
  project knowledge, only overarching pages (index, homelab overview,
  conventions).
- **Public and private separated by sensitivity, not by subject.** Secret
  locations and credentials never belong on a public Pages site; literal
  identifiers (hostnames, usernames, tailnet names, LAN IPs) are redacted to
  generic placeholders before public import (decision 2026-07-14: homelab docs
  may be public provided they are redacted — see change `redact-homelab-docs`
  in the homelab repo). Beyond that the split happens at repo level (private
  repo = private section), not with per-page filters.
- **EUPL-1.2** for public content, unless a repo is already licensed otherwise.
- **Python tooling through `uv`**, never pip directly.
- **English everywhere**, in every participating repo: code, comments, docs and
  commit messages. A Dutch-language deliverable for a Dutch audience is a
  different thing and stays fine (decision Mark, 2026-09-21).

## Scope (forges)

- **GitHub** (`MWest2020`): the only forge for this entire ecosystem — existing
  project repos (zeef, wanderer, estafette, billbird, skill-forge, certswap,
  gitsweeper among others) and the handbook repo itself.
- **Codeberg is work context** (employer org) and stays entirely outside this
  personal handbook — no repos, no imports, no deploys there.
  (Mark's decision, 2026-07-12; replaced the original Codeberg plan.)

## Changes and dependencies

```
audit-repo-inventory      (change 1: inventory + classification, read-only)
        |
        v
add-docs-contract         (change 2: /docs + .mcp.json remediation per repo, via PRs)
        |
        v
add-handbook-portal       (change 3: handbook repo + pipeline + Pages deploy)
```

Change 1 produces the classification table that 2 and 3 run on. Do not start on
2 before Mark has settled that table (human approval is the gate).

## Roadmap (planned, after changes 1–3)

One line of scope per change; specs follow per change when picked up,
proposal-first:

- `add-drift-gates`: freshness blocking after a trial period, link checking,
  periodic rebuild plus a self-closing drift issue.
- `add-hub-mcp`: a read-only MCP server (stdio) on the content layer that reads
  the import list; path bounding and token hygiene as explicit requirements; a
  session test as the verify.
- `add-agent-guardrails`: an operations catalogue per participating repo, live
  tested with injection and creation scenarios.
- `add-docs-claims`: executable verify blocks in docs plus `scripts/verify.sh`
  per repo as a second pre-push gate (functional dry runs), with a sabotage
  test as proof.

## Definitions

- **mcp.json**: `.mcp.json` in the repo root, declaring MCP servers for Claude
  Code sessions in that repo. Only for repos with active agent development.
- **Docs contract**: `/docs` with a Diátaxis-light layout plus front matter. See
  change 2 for the exact specification.
- **Handbook**: the aggregation repo (named `handbook`, on GitHub under
  `MWest2020`). Deliberately not a "techbook": this also covers non-platform
  matters (administrative references, the project portfolio), and there is no
  second book to delimit it against.
