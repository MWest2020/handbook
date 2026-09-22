---
status: actief
last_reviewed: 2026-09-22
agent:
  naam: security
  npub: null            # execution-only role (habitat), no ratatoskr chat identity
  chat: null
  executie:
    model: sonnet
    habitat_rol: security
    seed: docs/agents/seeds/security.md
    tools: { allow: [Read, Bash, Grep, Glob], deny: [Write, Edit] }
    skills: [thinking-red-team]
---

# security

## Mandate

An execution-only role in the cage (habitat). The canonical role content lives
in [`docs/agents/seeds/security.md`](seeds/security.md); each spoke's
`.claude/agents/security.md` is **derived** from it (generator plus drift gate),
not copied by hand.

## Chat facet

None — this role does not run in the ratatoskr chat.

## Execution facet (habitat · security)

Source: [`seeds/security.md`](seeds/security.md). Change the role *there*; the
generator keeps every spoke identical.
