# Tasks: eco-mcp-readonly

Tasks 2.x and 3.x need the state file location and the wordsworth API shape,
which are open questions in the proposal.

## 1. Roles and skills

- [ ] 1.1 Add the role lookup and skill lookup tools to `handbook_mcp`.
      Proof: `scripts/test_mcp.py` calls each against a known role
      (`docs/agents/`) and a known skill (`inventory/skills-register.yml`), and
      asserts the unknown-name error.

## 2. Factory status

- [ ] 2.1 Add the factory status tool (build queue, running chains, boards, API
      ledger total) reading ratatoskr's state files. Proof:
      `scripts/test_mcp.py` runs it against fixture state files and checks
      each of the four parts.
- [ ] 2.2 Missing or unreadable state files. Proof: a test that the tool reports
      the absence instead of crashing or returning empty values as if current.

## 3. Wordsworth dossier search

- [ ] 3.1 Add the dossier search tool over wordsworth's API. Proof:
      `scripts/test_mcp.py` against a stub API, including a failed call.
- [ ] 3.2 Token hygiene. Proof: a test that a failing call (bad credential)
      leaves no token or fragment of it in the error.

## 4. Read-only

- [ ] 4.1 Tool inventory. Proof: `scripts/test_mcp.py` asserts `tools/list` is
      exactly the three existing tools plus the new read tools, and none that
      mutates.

## 5. Docs

- [ ] 5.1 New how-to `docs/how-to/use-the-ecosystem-mcp.md`: the tools, what
      each reads, the environment variables, and that there are no write tools
      (front matter `status` + `last_reviewed`). Proof: `check_contract.py`
      passes in CI.
- [ ] 5.2 Update `docs/agents/index.md` (the "How to read this" section names
      `read_doc` only) and `docs/conventions.md` (line 31, "Agents (MCP,
      planned)") to point at the new tools. Proof: the docs gate passes on the
      PR.
- [ ] 5.3 `CHANGELOG.md` entry. Proof: present in the PR.
