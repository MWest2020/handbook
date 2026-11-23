# Tasks: eco-mcp-readonly

Factory status and wordsworth dossier search (formerly 2.x and 3.x) are
follow-up changes; see the proposal.

## 1. Roles and skills

- [x] 1.1 Add the role lookup tool to `handbook_mcp`: resolves a name to
      `docs/agents/<name>.md`. Proof: `scripts/test_mcp.py` calls it for a
      known role and asserts the `## Mandate` heading is present (structure,
      not wording).
- [x] 1.2 Add the skill lookup tool: takes a skill name, reads
      `inventory/skills-register.yml` itself, leaves `_guard_path` unchanged.
      Proof: `scripts/test_mcp.py` asserts the slug is present in the result,
      and that `read_doc("handbook", "inventory/skills-register.yml")` is still
      refused.
- [x] 1.3 Unknown names. Proof: `scripts/test_mcp.py` asserts the refusal for
      an unknown role and an unknown skill, and that the error names no other
      file.

## 2. Read-only

- [x] 2.1 Tool inventory. Proof: `scripts/test_mcp.py` asserts `tools/list` is
      exactly the three existing tools plus the role and skill lookups, and
      none that mutates.

## 3. Docs

- [x] 3.1 New how-to `docs/how-to/use-the-ecosystem-mcp.md` (front matter
      `status` + `last_reviewed`): the two tools and what each reads; that the
      role lookup mostly overlaps `read_doc('handbook','docs/agents/<name>.md')`
      and adds only name resolution and the unknown-name refusal; that the
      skill lookup is the new ground; that there are no write tools; and that
      the tool is not an identity or authorisation source (the closed-npub
      rule lives in the registry guardrails). Proof: `check_contract.py`
      passes in CI.
- [x] 3.2 Update `docs/agents/index.md` (the "How to read this" section names
      `read_doc` only) and `docs/conventions.md` (line 31, "Agents (MCP,
      planned)") to point at the new tools. Proof: the docs gate passes on the
      PR.
- [x] 3.3 `CHANGELOG.md` entry. Proof: present in the PR.
