---
status: actief
last_reviewed: 2026-09-03
agent:
  naam: security
  npub: null            # executie-only rol (habitat), geen boomhuis-chat-identiteit
  chat: null
  executie:
    habitat_rol: security
    seed: docs/agents/seeds/security.md
    tools: { allow: [Read, Bash, Grep, Glob], deny: [Write, Edit] }
    skills: [thinking-red-team]
---

# security

## Mandaat

Executie-only rol in de kooi (habitat). De canonieke rol-inhoud staat in
[`docs/agents/seeds/security.md`](seeds/security.md); de per-spoke
`.claude/agents/security.md` wordt daaruit **afgeleid** (generator + drift-gate), niet
met de hand gekopieerd.

## Chat-facet

Geen — deze rol draait niet in de boomhuis-chat.

## Executie-facet (habitat · security)

Bron: [`seeds/security.md`](seeds/security.md). Wijzig de rol dáár; de generator houdt alle
spokes gelijk.
