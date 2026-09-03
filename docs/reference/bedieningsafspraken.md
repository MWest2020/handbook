---
status: current
last_reviewed: 2026-08-31
---

# Bedieningsafspraken

Operationele afspraken die gelden bij het draaien van het ecosysteem, maar
niet in code of een spec staan. Kort, per onderwerp; een agent die hier start
houdt zich eraan.

## Wordsworth — VC reveal-gate: nooit `REQUIRED` met een test/publieke issuer

Wordsworth kan de reveal optioneel gaten met een verifiable credential
(EUDI-aligned, zie wordsworth `ADR-0003`): met `WORDSWORTH_VC_REQUIRED=true`
wordt een geldige credential verplicht voor elke reveal.

**Zet `WORDSWORTH_VC_REQUIRED=true` nooit aan zolang de VC-issuer een test- of
anderszins publieke issuer is** — bijvoorbeeld wanneer een geldig
test-credential in een publieke repo is ingebed.

Reden: als een geldige credential publiek beschikbaar is, kan iedereen aan de
"VC-verplicht"-check voldoen, waardoor de afdwinging geen extra zekerheid
oplevert. Echte afdwinging vereist een **niet-publieke issuer** én
**holder-binding** (proof-of-possession: key-binding + audience/nonce).

Tot dat er is blijft de gate **additief** (`REQUIRED=false`): een gepresenteerde
credential kan een reveal alleen **versmallen** (doorsnede met de grant), nooit
verbreden. Zo levert de gate defense-in-depth zonder enkelvoudig steunpunt.

## Skill-register — verversen van de mirror

`inventory/skills-register.yml` is een **mirror** van skill-forge's catalogus van
gepromoveerde skills (bron: skill-forge, niet de handbook). De agent-tool/skill-gate
valideert elke `skills:`-entry in een agent-def hiertegen.

Verversen na een `promote`/`demote` in skill-forge:

    # in skill-forge:
    uv run forge register
    # kopieer de uitvoer naar de handbook-mirror:
    cp ~/skill-forge/register.yml ~/handbook/inventory/skills-register.yml

Commit de mirror in de handbook. Een gedeclareerde skill die niet (meer) in het
register staat laat de gate falen — dat is de bedoeling: geen phantom-skills.
Automatisch verversen + een drift-gate tegen skill-forge's live output (zoals de
seed-drift-gate) is uitgesteld werk.
