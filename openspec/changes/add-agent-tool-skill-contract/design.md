# Design: add-agent-tool-skill-contract

## Waar de velden staan: in het facet, niet los

De tools/skills horen bij een facet, niet bij de rol als geheel: de chat-listener
en de kooi geven verschillende tools. Daarom komen ze onder `agent.chat` resp.
`agent.executie`, niet op het top-niveau. Een leeg facet (`null`) krijgt ze niet.

```yaml
agent:
  naam: reviewer
  executie:
    habitat_rol: reviewer
    seed: docs/agents/seeds/reviewer.md
    tools:
      allow: [Read, Bash, Grep, Glob]
      deny:  [Write, Edit]        # read-only, nu machine-checkbaar
    skills: []
```

## Waarom een expliciete `deny` naast `allow`

Claude Code's agent-formaat kent alleen een allowlist (`tools:`); "wat mag niet"
is daar het complement. Dat is precies wat onzichtbaar is als je wil garanderen
dat reviewer/security nooit schrijven. Door `deny` expliciet te maken:

- wordt "read-only" een gecontroleerde bewering i.p.v. proza;
- kan habitat 'm later 1-op-1 als `--disallowedTools` doorgeven (defence-in-depth
  bovenop de allowlist);
- ziet een mens in de definitie meteen de grens, zonder de volledige toolset te
  kennen.

`allow` en `deny` mogen niet overlappen (de gate faalt daarop) — anders is de
bedoeling dubbelzinnig.

## Consistentie met de seed = de echte afdwinging

De seed is wat habitat uitvoert. De definitie mag daar niet van afwijken, dus de
gate eist `executie.tools.allow == seed.tools`. Zo is het contract niet louter
documentatie maar gekoppeld aan het artefact-van-record; de bestaande
`gen_agent_seeds`-driftgate bewaakt vervolgens de kopie naar de spokes.

## Skills: intentie nu, consumptie later

`skills` legt vast wélke skills bij een rol relevant zijn (bv. security ↔
`thinking-red-team`). Claude Code kent geen front-matter-`skills:`-veld dat skills
verleent; dit is dus een intentie-/documentatieveld dat de runtime toepast wanneer
'ie skills aanbiedt. Leeg is een geldige, expliciete "geen". De gate eist dat het
veld aanwezig is (ook `[]`), zodat "vergeten" niet als "geen" leest.

## Waarom een gate en geen afspraak

Conform het handbook-uitgangspunt "enforcement, geen afspraak": een los contract
zonder check drift terug. `check_agent_tools.py` draait in `docs-gates` naast de
bestaande contract-/freshness-checks en faalt de PR bij een ontbrekend veld,
allow/deny-overlap of seed-mismatch.

## Verworpen alternatieven

| Optie | Waarom niet |
|---|---|
| Alleen proza netter maken | Blijft oncontroleerbaar; lost Mark's "welke niet" niet structureel op. |
| `deny` weglaten (allowlist volstaat) | Maakt de read-only-garantie onzichtbaar en niet-checkbaar. |
| Skills verplicht niet-leeg | Dwingt verzonnen skills af; `[]` moet een geldige uitkomst zijn. |
| Nieuw top-level `tools:`-blok | Negeert dat chat en kooi verschillende tools hebben. |
