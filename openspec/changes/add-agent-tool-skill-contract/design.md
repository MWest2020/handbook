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
    tools: { allow: [Read, Bash, Grep, Glob], deny: [Write, Edit] }  # read-only, machine-checkbaar
    skills: []
```

De inline flow-vorm (`tools: { allow: [...], deny: [...] }`, `skills: [...]`) is de
vorm die alle defs gebruiken én die de gate verwacht — één regel per veld, geen
blok-YAML, zodat de stdlib-gate 'm zonder yaml-parser betrouwbaar leest.

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

## Betekenis van een lege `allow`

`allow: []` betekent: **dit facet verleent geen tools** — een puur conversatie-
facet. Alle chat-facetten krijgen `[]` omdat de boomhuis-`claude -p`-listener
vandaag geen tools uitdeelt (de agents adviseren, voeren niet uit; zie de
mandaten). Zodra de listener wél tools verleent (fase 2, aparte consumptie-change)
worden die hier ingevuld en leest de listener ze. `[]` is dus een expliciete,
geldige keuze — niet "onbekend".

## Consistentie met de seed = de echte afdwinging

De seed is wat habitat uitvoert. De definitie mag daar niet van afwijken, dus de
gate eist `executie.tools.allow == seed.tools`. Zo is het contract niet louter
documentatie maar gekoppeld aan het artefact-van-record; de bestaande
`gen_agent_seeds`-driftgate bewaakt vervolgens de kopie naar de spokes.

## Skills: het veld nu leeg, gevuld zodra er een skill-bron is

`skills` legt vast wélke skills bij een rol relevant zijn. Claude Code kent geen
front-matter-`skills:`-veld dat skills verleent; dit is een intentie-/
documentatieveld. De velden staan nu bewust op `[]`: een niet-lege waarde zou een
skill-naam claimen die nergens in het ecosysteem als bestaand te controleren is,
en de gate zou 'm — anders dan een `seed:`-pad — niet tegen een artefact kunnen
kruisen. Daarom eerst het contract (veld verplicht aanwezig, ook `[]`), en het
vullen + een existentie-check tegen een skill-register (bv. skill-forge) als
vervolg-change — net zoals `seed:` nu wél tegen een bestaand bestand wordt
gekruist. `[]` is een geldige, expliciete "geen".

## Executie-facetten zonder seed (architect)

Niet elke executie-rol heeft (nog) een canonieke seed: `docs/agents/seeds/` bevat
`builder/reviewer/security`, maar geen `architect`. Voor architect kan de gate
`executie.tools.allow` dus tegen niets kruisen — de declaratie staat er als
intentie, ongecontroleerd, tot architect een seed krijgt (samen met
`add-seed-derivation`-vervolg). De gate slaat de seed-check dan expliciet over
(geen stille "ok"): dit is een bekende, begrensde beperking, geen gat zoals de
r1-bouwer (die wél een seed had maar 'm niet declareerde).

## Verhouding tot "seeds zijn afgeleid" (agent-registry)

`agent-registry` eist dat seeds worden *afgeleid* van het executie-facet. Deze
change zet de tools nog op twee plekken (def-front-matter + seed) en bewaakt hun
gelijkheid met de gate — een interim-guard, geen eindstation. De eindvorm is dat
`gen_agent_seeds` de seed-`tools:` uit `executie.tools.allow` *genereert* (één
bron); dat is een vervolg op `add-seed-derivation`. Tot dan is de gate wat "gelijk
blijven" afdwingt i.p.v. hoopt.

## Waarom een gate en geen afspraak

Conform het handbook-uitgangspunt "enforcement, geen afspraak": een los contract
zonder check drift terug. `check_agent_tools.py` faalt bij een ontbrekend veld,
allow/deny-overlap of seed-mismatch. De CI-stap die 'm in de handbook-pipeline
(`handbook.yml`) draait, naast de bestaande seed-drift-/contract-checks, voegt Mark
met de hand toe (CI-config is een human-gate; deze change raakt CI niet).
(`docs-gates.yml` is bewust NIET de plek: dat is de reusable workflow die
hub-checkers tegen een spoke draait, en een spoke heeft geen `docs/agents/`.)

## Verworpen alternatieven

| Optie | Waarom niet |
|---|---|
| Alleen proza netter maken | Blijft oncontroleerbaar; lost Mark's "welke niet" niet structureel op. |
| `deny` weglaten (allowlist volstaat) | Maakt de read-only-garantie onzichtbaar en niet-checkbaar. |
| Skills verplicht niet-leeg | Dwingt verzonnen skills af; `[]` moet een geldige uitkomst zijn. |
| Nieuw top-level `tools:`-blok | Negeert dat chat en kooi verschillende tools hebben. |
