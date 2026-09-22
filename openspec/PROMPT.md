# PROMPT — start here (Claude Code)

Paste the prompt below into Claude Code in an empty working directory that has
this `openspec/` directory beside it. Make sure `CODEBERG_TOKEN` (read-only
scope: repository) and `gh auth status` work before you start.

Tokens per change (minimal scope, a separate token per purpose):

- **Change 1 (audit, read-only):** `CODEBERG_TOKEN` with only
  `read:repository`; GitHub through `gh` with standard read access. No write
  scopes during the audit.
- **Change 2 (PRs to your own repos):** a separate write token per forge —
  Codeberg/Forgejo: `write:repository` (push a branch, open a PR), no admin or
  org scopes; GitHub: `gh` with the `repo` scope or a fine-grained token with
  `contents: write` + `pull requests: write`, limited to the repos involved.
  Create and use these only from change 2 onwards.

---

You are working on my personal handbook ecosystem. Read these in full first:

1. `openspec/project.md` — context and starting points
2. `openspec/changes/audit-repo-inventory/proposal.md` and `tasks.md`

Then carry out change `audit-repo-inventory` and NOTHING else, task by task, in
order. Hard rules:

- This change is read-only: no commits, no PRs, no changes to existing repos.
  Shallow clones or API calls purely to inspect.
- Inspect the repos themselves on Codeberg (Forgejo API) *and* GitHub (`gh`) —
  base the classification on what you find, not on assumptions. Paginate fully;
  half a list is worse than no list.
- Do not decide when in doubt: `tier: TBD` plus a concrete question in `notes`.
  Sensitivity when in doubt: `private-only`.
- Output exactly as task 4 describes: `inventory/repos.md` plus
  `inventory/repos.json`, identical content, field names exactly as in the
  proposal's table.
- Stop after task 4.3 and present the table plus your TBD questions. Changes 2
  and 3 start only after my explicit approval of the classification — do not
  start on them, not even "in preparation".

Style: boring and auditable. Bare scripts (no ANSI, no banners), and every
classification decision that does not follow trivially from the decision table
gets one line of reasoning in `notes`.

---

After the inventory is approved: the same pattern for
`openspec/changes/add-docs-contract/` (one PR per repo, stop per PR) and then
`openspec/changes/add-handbook-portal/` (answer the three open questions in that
proposal first).
