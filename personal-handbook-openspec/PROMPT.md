# PROMPT — start hier (Claude Code)

Plak onderstaande prompt in Claude Code in een lege werkdirectory waar deze
`openspec/`-map naast staat. Zorg dat `CODEBERG_TOKEN` (read-only scope:
repository) en `gh auth status` werken vóór je start.

Tokens per change (minimale scope, apart token per doel):

- **Change 1 (audit, read-only):** `CODEBERG_TOKEN` met alleen
  `read:repository`; GitHub via `gh` met standaard leestoegang. Geen
  write-scopes tijdens de audit.
- **Change 2 (PR's naar eigen repos):** per forge een apart write-token —
  Codeberg/Forgejo: `write:repository` (branch pushen + PR openen), geen
  admin- of org-scopes; GitHub: `gh` met `repo`-scope of een fine-grained
  token met `contents: write` + `pull requests: write`, beperkt tot de
  betrokken repos. Pas aanmaken/gebruiken vanaf change 2.

---

Je werkt aan mijn persoonlijke handbook-ecosysteem. Lees eerst volledig:

1. `openspec/project.md` — context en uitgangspunten
2. `openspec/changes/audit-repo-inventory/proposal.md` en `tasks.md`

Voer daarna UITSLUITEND change `audit-repo-inventory` uit, taak voor taak, in
volgorde. Harde regels:

- Deze change is read-only: geen commits, geen PR's, geen wijzigingen aan
  bestaande repos. Shallow clones of API-calls alleen om te inspecteren.
- Inspecteer de repos zelf op Codeberg (Forgejo API) én GitHub (`gh`) — baseer
  de classificatie op wat je aantreft, niet op aannames. Pagineer volledig;
  een halve lijst is erger dan geen lijst.
- Beslis niet bij twijfel: `tier: TBD` + concrete vraag in `notes`.
  Sensitivity bij twijfel: `private-only`.
- Output exact zoals taak 4 beschrijft: `inventory/repos.md` +
  `inventory/repos.json`, identieke inhoud, veldnamen exact als de
  proposal-tabel.
- Stop na taak 4.3 en presenteer de tabel plus je TBD-vragen. Changes 2 en 3
  starten pas na mijn expliciete goedkeuring van de classificatie — begin er
  niet alvast aan, ook niet "ter voorbereiding".

Stijl: boring and auditable. Bare scripts (geen ANSI, geen banners), elke
classificatiebeslissing die niet triviaal uit de beslistabel volgt krijgt één
regel motivatie in `notes`.

---

Na goedkeuring van de inventaris: zelfde patroon voor
`openspec/changes/add-docs-contract/` (per repo één PR, stop per PR) en
daarna `openspec/changes/add-handbook-portal/` (beantwoord eerst de drie
open vragen in die proposal).
