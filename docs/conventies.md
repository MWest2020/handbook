---
status: current
last_reviewed: 2026-07-12
---

# Conventies

## Docs-contract (Diátaxis-light)

Elk deelnemend repo heeft `docs/` met `index.md` in de root en markdown
uitsluitend in de root of in `how-to/`, `reference/` en `explanation/`
(ADR's onder `explanation/adr/NNNN-titel.md`). Elke pagina draagt front
matter met `status` (current | draft | deprecated) en `last_reviewed`
(ISO-datum); een `owner`-veld is verboden. Minimum viable: `index.md` +
één reference-pagina. Eén taal per repo: Engels voor publieke repos,
Nederlands toegestaan voor private/homelab-repos.

De volledige specificatie staat in
[`openspec/archive/2026-07/add-docs-contract/`](https://github.com/MWest2020/handbook/tree/main/openspec/archive/2026-07/add-docs-contract);
`scripts/check_contract.py` dwingt het contract af in CI.

## Importlijst

`inventory/repos.json` is de enige waarheid over welke repos meedoen.
`scripts/gen_imports.py` genereert de mkdocs-importblokken eruit; CI faalt
bij drift. Agents (MCP, gepland) lezen dezelfde lijst — er bestaat geen
tweede waarheid.

## Licenties en tooling

- **EUPL-1.2** voor publieke content, tenzij een repo al anders
  gelicenseerd is (afwijkingen staan in de inventaris-notes).
- **Python via `uv`**, nooit pip direct.
- Boring and auditable: standaard tooling, expliciete configuratie, elke
  beslissing herleidbaar in een proposal of ADR.

## Publiek/privaat

Gescheiden op gevoeligheid, niet op onderwerp, en op repo-niveau: een repo
is public-ok of private-only; per-pagina filters bestaan niet. De private
build (`mkdocs.private.yml`, niet getrackt in dit repo) draait op de
beheer-host en gaat nooit naar Pages.
