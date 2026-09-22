---
status: current
last_reviewed: 2026-09-22
---

# Operating agreements

Operational agreements that apply when running the ecosystem but live neither
in code nor in a spec. Short, one per subject; an agent that starts here
abides by them.

## Wordsworth — VC reveal gate: never `REQUIRED` with a test or public issuer

Wordsworth can optionally gate a reveal behind a verifiable credential
(EUDI-aligned, see wordsworth `ADR-0003`): with
`WORDSWORTH_VC_REQUIRED=true` a valid credential becomes mandatory for every
reveal.

**Never turn `WORDSWORTH_VC_REQUIRED=true` on while the VC issuer is a test
issuer or otherwise public** — for instance when a valid test credential is
embedded in a public repo.

The reason: if a valid credential is publicly available, anyone can satisfy the
"VC required" check, so enforcing it buys no additional certainty. Real
enforcement needs a **non-public issuer** *and* **holder binding**
(proof-of-possession: key binding plus audience/nonce).

Until that exists the gate stays **additive** (`REQUIRED=false`): a presented
credential can only **narrow** a reveal (the intersection with the grant),
never widen it. That way the gate gives defence in depth without becoming a
single point of trust.

## Skill register — refreshing the mirror

`inventory/skills-register.yml` is a **mirror** of skill-forge's catalogue of
promoted skills (the source is skill-forge, not the handbook). The agent
tool/skill gate validates every `skills:` entry in an agent definition against
it.

Refresh after a `promote` or `demote` in skill-forge:

    # in skill-forge:
    uv run forge register
    # copy the output into the handbook mirror:
    cp ~/skill-forge/register.yml ~/handbook/inventory/skills-register.yml

Commit the mirror in the handbook. A declared skill that is no longer in the
register makes the gate fail — which is the point: no phantom skills.
Refreshing automatically plus a drift gate against skill-forge's live output
(like the seed drift gate) is deferred work.
