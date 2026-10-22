---
status: draft
last_reviewed: 2026-10-22
---

# Agents — canonical registry

The **single source of truth** about who the agents of the ecosystem are. Every
role has exactly one definition here; ratatoskr (chat) and habitat (execution)
*read* it, they do not redefine it. That is how a builder is always the same
builder.

## How to read this (human and agent alike)

- Human: these pages on the site.
- Agent: through `handbook_mcp` → `read_doc("handbook", "docs/agents/<name>.md")`.

## Two facets per definition

| Facet | What | Consumer |
|---|---|---|
| **chat** | system prompt + channel scope + `tools`/`skills` | ratatoskr (the `claude -p` listener) |
| **execution** | cage role + `tools`/`skills` + output schema | habitat (a caged Kubernetes job) |

A role may have one empty facet (assistent is chat only; security is execution
only). The `## Mandate` section is the source for both facets and for humans.

Every non-empty facet explicitly declares `tools.allow`, `tools.deny` (which
tools specifically *not*) and `skills` in its front matter — empty (`[]`) is a
valid and explicit choice. The gate `scripts/check_agent_tools.py` guards that
the contract is present, that an execution `allow` matches the seed habitat
runs, and that every `skills:` entry exists in the skill register
(`inventory/skills-register.yml`, a mirror of skill-forge); the CI step that
runs it is wired in by hand (CI config is a human gate).

## How the fleet works together: hub and spokes

> Mark, 2026-09-21: *"Ik wil eigenlijk enkel met Odin spreken, maar odin moet
> niet alles doen. Odin is de hub en niet de spokes."*

    Mark ──► odin (hub, #general)
               │  decides: answer, route, or delegate
               ├─ !route #channel ──────► a spoke agent, in its own channel
               ├─ !sessie <type> … ─────► a detached work session; the answer
               │                          returns in this channel, under odin's
               │                          own name
               └─ "that goes via bouwer" ► !dispatch → habitat (gate = Mark)

Three rules follow from that, and they come back in the definitions below:

1. **The hub does not do the work.** Anything that costs time goes to a spoke.
   Odin stays reachable while that spoke runs — which is the entire gain. See
   `delegate_session` in [odin](odin.md).
2. **Building goes to habitat, via bouwer.** Not in a chat turn, not in a read
   session. Bouwer guards that road; `!dispatch` stays Mark's own command,
   because building is where a mistake is expensive.
3. **Ratatoskr exists for human context**, not to get things done: reading and
   answering across several channels at once. What works there are daily
   standups, escalations, and the judgement of a reviewer, architect or red
   teamer. What does not work there are conversations in which an agent
   explains what it may not do.

That third one is a measure, not a mood. An agent answering "I can't" while a
road exists is a fault in its definition — name the road. A limitation that
lives only in a mandate text and not in the listener is not a limitation but a
misunderstanding that costs money.

## Role contracts (pilot: architect, bouwer, reviewer)

> Mark, 2026-10-22: *"the problem is the overlap, regular hub&spoke isn't
> working superfine."*

The mandates were prose, and two of them claimed the same work. Architect
said "concrete work goes through an OpenSpec change" and bouwer said "turn an
idea into an OpenSpec-change-shaped task". On 2026-10-05 architect then
assigned bouwer to write both `proposal.md` and `design.md`.

The fix is borrowed from the BMAD method: only its role contract, not its
document set. OpenSpec stays the only artifact flow. Each role gets a
`## Contract` section with five fields:

| field | answers |
|---|---|
| **Takes** | which input is mine |
| **Produces** | which artifact I deliver, and where |
| **Done when** | the observable end of my part |
| **Hands off to** | who picks it up next |
| **Not mine** | what looks like mine but is not, and whose it is |

"Not mine" is the field that ends the overlap: an agent knows when to stay
silent and whom to name instead.

The pilot chain, mapped onto OpenSpec:

    architect ──decision──► bouwer ──change on a branch──► (Mark dispatches)
                             │                                  │
                             └──── readiness check ◄────────────┘
                                                                ▼
                                      reviewer ◄── branch/PR with green verify
                                         │
                       go ──► Mark merges · no-go ──► owner per finding

Ratatoskr passes the `## Contract` section into the agent's system prompt, so
the contract reaches the model and not only the reader. The
`role-contracts` change in ratatoskr does this. Other roles get a contract
once the pilot has carried one real change through the chain.

## Guardrails

- **Identity:** the relay is *closed* — only npubs from this registry take part.
- **Definition:** consumers run an agent only as this source describes it; a
  drift gate catches deviation (CI), and this directory falls under CODEOWNERS
  so that "who the agents are" goes past Mark.

## Roles

- [odin](odin.md) — **the hub**: the only agent in #general. Mark talks to odin;
  odin routes to the spokes (route / new agent / extension).
  Was `coordinator`; renamed 2026-09-07 on Mark's decision.
- [bouwer](bouwer.md) — build scoping (chat, #bouw) + habitat `builder` (execution)
- architect — architecture sparring (chat, #architectuur) + habitat plan (execution) *(to follow)*
- assistent — general chat agent (spoke channels), no execution *(to follow)*
- [reviewer](reviewer.md) / [security](security.md) — execution only (habitat)
- [roodteam](roodteam.md) — security/red-team agent (chat, #red-team, #review), no execution
- **seeds/** — canonical execution seeds; the per-spoke `.claude/agents/` are
  derived from these (generator plus drift gate)
