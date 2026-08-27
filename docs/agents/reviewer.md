---
status: actief
last_reviewed: 2026-08-27
agent:
  naam: reviewer
  npub: null            # executie-only rol (habitat), geen boomhuis-chat-identiteit
  chat: null
  executie:
    habitat_rol: reviewer
    seed: docs/agents/seeds/reviewer.md
---

# reviewer

## Mandaat

Executie-only rol in de kooi (habitat). De canonieke rol-inhoud staat in
[`docs/agents/seeds/reviewer.md`](seeds/reviewer.md); de per-spoke
`.claude/agents/reviewer.md` wordt daaruit **afgeleid** (generator + drift-gate), niet
met de hand gekopieerd.

## Chat-facet

Geen — deze rol draait niet in de boomhuis-chat.

## Executie-facet (habitat · reviewer)

Bron: [`seeds/reviewer.md`](seeds/reviewer.md). Wijzig de rol dáár; de generator houdt alle
spokes gelijk.
