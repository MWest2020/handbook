---
status: current
last_reviewed: 2026-10-30
---

# How to use the ecosystem MCP

`handbook_mcp` is read-only: five tools, no tool that mutates a repository, a
file, or any other state. This page covers the two added by
`eco-mcp-readonly` — `read_role` and `read_skill` — and how they relate to the
three that were already there.

## `read_role(name)`

Returns the definition of an agent role from `docs/agents/<name>.md` on the
handbook's default branch (for example `read_role("bouwer")`).

This mostly overlaps calling
`read_doc("handbook", "docs/agents/<name>.md")` directly. What `read_role`
adds on top is name resolution (so a caller passes a bare name, not a path)
and a clean refusal when the name matches no role file, instead of a raw
fetch error.

## `read_skill(name)`

Returns one entry from the skills register
(`inventory/skills-register.yml`, the mirror of skill-forge's catalogue),
looked up by slug (for example `read_skill("mcp-builder")`).

This is new ground, not an overlap: `read_doc`'s path guard refuses anything
outside `docs/**/*.md`, so `inventory/skills-register.yml` stays unreachable
through it. `read_skill` reads that one fixed file itself — nobody may widen
`read_doc`'s path guard to cover `inventory/` to make this lookup possible
some other way.

## Unknown names

Both tools refuse a name that matches nothing, with an error that names no
other file — the error does not confirm or deny the existence of any file
beyond the one that was asked for.

## No write tools

`handbook_mcp` offers no tool that queues a build, moves a card, or changes
anything else. Read-only is the whole surface; a write tool would be a
separate proposal.

## Not an identity or authorisation source

A successful `read_role` or `read_skill` call says only that a definition
exists in the handbook's files — it says nothing about who is allowed to act
as that role or use that skill. The closed-npub rule that governs identity
lives in the registry guardrails (`docs/agents/index.md`), not here.
