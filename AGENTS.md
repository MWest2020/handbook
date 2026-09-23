# handbook — hub of the personal ecosystem

This repo is the coordination hub: specs (`openspec/`), inventory
(`inventory/`), the import list (mkdocs) and the starting point for Claude
Code sessions across the whole personal ecosystem. There is deliberately **no**
separate hub repo (unlike the work setup): one owner, one hub.

## What a session starting here is for

- **Coordinate, do not build.** Construction on spokes runs through habitat Jobs
  (`dispatch.sh <role> <change> <repo>` from a host with kubectl; see habitat
  `docs/reference/dispatch.md`). Reviewer and security always with
  `HABITAT_BASE_BRANCH=habitat/builder/<change>`.
  That applies to an *interactive* session started here. A **dispatched habitat
  role** follows its own role file (`.claude/agents/<role>.md`) and does build
  here — strictly within the change it was dispatched for, and without touching
  `AGENTS.md`, `.claude/agents/` or CI. For a dispatched role, merging stays
  human.
- **Interactive sessions finish the job.** Work on `main`, no PRs to ask for
  approval; merge, deploy, archive and fix follow-ups without asking, then
  report. The exceptions — `docs/agents/` and `.claude/agents/` (CODEOWNERS)
  and classifier-blocked commands — are in
  [operating agreements](docs/reference/operating-agreements.md).
- **The inventory is the single source of truth.** `inventory/repos.json`
  decides what takes part (site and agents alike). Changes to the import list go
  through `scripts/gen_imports.py`, never by hand. The table in
  `inventory/repos.md` is derived: regenerate it with
  `scripts/gen_inventory_md.py` (it edits only the marked table block; the prose
  around it stays handwritten).
- **Proposal first.** New changes, repos or entities come into being through an
  openspec proposal under `openspec/changes/`, never implicitly.
- **Escalation.** Anything not described in a proposal or in this mandate:
  ask first. One restart per failed habitat run without a human;
  a security FAIL or a reported secret always goes to a human.

## Where knowledge lives

- **Working agreements** (how we work, test, write):
  `docs/reference/operating-agreements.md`. Read it before starting work.
- **Project knowledge** (runbooks, gotchas, decisions): the owning repo's
  `docs/`, imported here.
- **Agent memory** holds only identity, credential locations and personal
  preferences, plus pointers to the two above. When memory and the handbook
  disagree, the handbook wins (spec `agent-memory`).

## Invariants

- `openspec/private/` is gitignored and holds homelab identifiers — never
  commit them, never quote them in public output (repos, PRs, docs).
- No secrets in this repo, not even in examples; tokens come from the
  environment.
- Public and private are separated at repo level; the private mkdocs build
  never goes to Pages.
- Python through `uv`, never pip. Bare CI scripts (no ANSI, no banners).
- **English everywhere.** Code, comments, docs, commit messages, interface
  text and the agent mandates in `docs/agents/`. Working in two languages is
  how Dutch ends up in code (Mark, 2026-09-21).
