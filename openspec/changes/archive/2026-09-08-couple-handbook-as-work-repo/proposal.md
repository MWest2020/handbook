# Change: couple-handbook-as-work-repo

## Why

De handbook is de naaf, maar zelf **geen werk-repo**: er kan geen habitat-Job op
draaien. Dat blokkeert alles wat een PR op de handbook nodig heeft — bijvoorbeeld
een nieuwe agent-definitie onder `docs/agents/` (de aanleiding: `@roodteam`).

De blokkade is concreet en te wijzen. De worker-entrypoint van habitat geeft elke
rol deze prompt mee:

> "Je bent de '<rol>'-agent voor deze repository. Volg
> `.claude/agents/<rol>.md` en het project-CLAUDE.md ..."

De handbook heeft **geen** `.claude/agents/` (18 spokes wel, via
`prep/seeds/<spoke>/`). Een builder die hier landt, vindt dus geen rolinstructie
en houdt alleen het hub-mandaat over — en dat opent met *"Coördineren, niet
bouwen"*. Hij zou dus, terecht volgens wat hij leest, niets bouwen.

Dat is geen ontbrekende koppeling in een systeem dat er al is: het is de laatste
spoke die nooit als spoke behandeld is, omdat hij de naaf is.

## What changes

- **`.claude/agents/{builder,reviewer,security}.md`** in de handbook zelf —
  byte-identieke kopieën van de canonieke `docs/agents/seeds/*.md`, want *"een
  builder is overal dezelfde builder"*. Geen handbook-eigen rolvariant.
- **`prep/seeds/handbook/.claude/agents/`** — de handbook doet mee in de
  seed-derivatie, zodat `scripts/gen_agent_seeds.py --check` ook zijn eigen kopie
  bewaakt en er geen stille drift ontstaat.
- **`CLAUDE.md`, één regel verduidelijkt.** "Coördineren, niet bouwen" gaat over
  een *interactieve* sessie die hier start; een gedispatchte habitat-rol volgt
  zijn rolbestand en bouwt wél, binnen zijn change. Zonder die zin is het mandaat
  in tegenspraak met de rol die de worker meegeeft.

## Wat hier bewust NIET gebeurt

- **Geen nieuwe agent toegevoegd.** Deze change koppelt de repo; `@roodteam` (of
  welke agent dan ook) is een aparte change, en een agent die zichzelf in de
  registry zet is precies wat de invarianten verbieden.
- **Geen inventariswijziging.** `inventory/repos.json` houdt voor de handbook
  `contract_applied: no` / `has_mcp_json: no`. Het docs-contract en `.mcp.json`
  zijn een eigen traject; deze change raakt ze niet, en de koppeling hangt er ook
  niet van af (boomhuis staat niet eens in de inventaris en kreeg toch een
  habitat-run).
- **Geen merge-rechten verschoven.** Een rol pusht een branch; mergen blijft
  Mark. Voor de handbook geldt dat te meer: hier liggen de agent-definities.

## Impact

- Een `dispatch.sh <rol> <change> MWest2020/handbook` heeft vanaf nu een
  rolinstructie om te volgen.
- Gates die dit moeten blijven halen: `gen_agent_seeds.py --check` (drift),
  `check_agent_tools.py` (tool/skill-contract), `check_contract.py`,
  `check_drift.py`, `check_freshness.py`.
- Risico dat expliciet aanvaard wordt: een agent kan in de repo werken waar de
  agent-definities liggen. De rem is de rolinstructie zelf ("Never modify
  `CLAUDE.md`, `.claude/agents/`, or CI config") plus de menselijke merge-gate.
