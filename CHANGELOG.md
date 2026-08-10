# Changelog

## 2026-08-10 (spoke-status: zettelkast + habitat)

Coördinatie-update, geen hub-code gewijzigd — alleen inventaris-notes
(`inventory/repos.json`) bijgewerkt met de afgeronde spoke-changes.

- **zettelkast — telefoon→vault-clipping werkt.** `phone-intake-v1` en
  `url-intake-v1` afgerond en gearchiveerd. Clippen is bewezen via de
  telefoon-share-tekstroute (eerste inhoudelijke clip 2026-08-04,
  MCP-architectuur); de dispatch-shortcut is niet geïnstalleerd, maar de
  dispatch-keten zelf is groen bewezen. Besluit Mark 2026-08-10: niet langer
  op de dispatch-route wachten → `url-intake-v1` afgerond via de tekst-route
  (3.3/3.4 met notitie). Geen open openspec-changes meer op zettelkast.
- **habitat — rol-architectuur gebouwd, twee changes gearchiveerd.**
  `add-role-architecture` (PR #11, 2× PASS reviewer+security, gemerged
  14351b8): architect/reviewer/security naast de builder, per-rol
  deny-by-default allowlists, schema-output, PreToolUse/Stop-hooks.
  `add-worker-image` gearchiveerd (besluit Mark 2026-08-10, "route B": image
  blijft privé via het `ghcr-pull`-pull-secret i.p.v. publieke
  package-visibility; nieuwe specs `worker-execution` + `worker-image-build`).
  `add-run-output` gearchiveerd (agent-eind-uitvoer als
  `.habitat/run-output-<id>.md` op de branch).
- **Openstaand (buiten deze machine):** `add-role-architecture` blijft open —
  de cluster-livetests (3.1–3.3) vereisen `kubectl` op een orchestrator-host.
  Paste-klaar runbook toegevoegd in habitat `docs/reference/dispatch.md`.
- **Signaal:** `inventory/repos.md` (de leesbare tabel) loopt achter op
  `repos.json` sinds ±2026-07-13 (o.a. habitat-visibility/notes). `repos.json`
  is de waarheid; `repos.md` is niet bijgewerkt om bestaande drift niet half
  te repareren — kandidaat om te regenereren uit `repos.json`.

## 2026-07-22 (mcp-hub-self-read)

- handbook-mcp ontsluit nu ook de hub zelf: `list_repos` toont `handbook`,
  `list_docs`/`read_doc` lezen zijn `docs/**/*.md` — code-exceptie in
  `_imports()`; de inventarisvlaggen blijven site-semantiek en de site
  importeert zichzelf nog steeds niet (`handbook_import: no`).
- Aanleiding: agents (o.a. zettelkast-sessies) konden elk spoke-repo lezen
  maar niet de hub-docs die het ecosysteem beschrijven; besluit Mark
  2026-07-22.
- `scripts/test_mcp.py` dekt het nieuwe gedrag (hub verplicht in de lijst +
  leescheck op `handbook docs/index.md`); hub-notes in
  `inventory/repos.json` vermelden de uitzondering; spec-delta op
  `handbook-mcp` "Eén waarheid" onder `openspec/changes/mcp-hub-self-read/`.

## 2026-07-14 (scrub-public-context)

- Nieuwe openspec-change `scrub-public-context` na review van de live
  publieke homepage: hub-eigen pagina's en repo-bestanden in dit publieke
  repo mogen geen financieringstrajecten, private repo-namen of
  redactie-metadata bevatten (twee nieuwe requirements op
  `handbook-portal`).
- Directe herstelactie: `docs/index.md` (trajectlabels weg,
  private-sectie-alinea → één verwijzingszin) en
  `docs/homelab/herstel.md` (private repo-namen en redactie-datum weg).
- Scope-besluiten Mark (2026-07-14) uitgevoerd:
  - Inventaris-notes gescrubd (financieringstrajecten en
    gevoelige-pointer-notes uit `inventory/repos.json`/`repos.md`);
    verplaatst naar een private overlay in de gitignored
    `openspec/private/`.
  - `mkdocs.private.yml` ge-untrackt + gitignored (private build-config
    hoort op de beheer-host); `scripts/gen_imports.py` slaat een afwezige
    private config over. README en conventies bijgewerkt.
  - `openspec/archive/`, `prep/seeds/` en `openspec/project.md` ontdaan
    van trajectvermeldingen; repo-namen blijven staan.
  - Git-history blijft staan (geen rewrite, geen visibility-wijziging).

## 2026-07-12 (scherpstelling na diff-review)

- Spec `docs-contract` aangescherpt: (1) structuureis geldt alleen voor
  markdown-dragende mappen — assets-/afbeeldingsmappen zijn geen schending
  (nieuw scenario); (2) front matter is "minimaal status + last_reviewed"
  i.p.v. "exact" (extra velden zoals `title` toegestaan; `owner` blijft
  verboden); (3) migratieregel ontdubbelzinnigd: draft krijgt
  `last_reviewed` = migratiedatum, pas echte review zet `current` + verse
  datum (spec-scenario en taak 2.3 gelijkgetrokken).

## 2026-07-12

- Northstar-sectie toegevoegd aan `openspec/project.md` (bewezen docs/code-
  sync vóór elke push, handbook als enige MCP-ingang voor agents,
  dichtgetimmerde agent-operaties met autonomieniveaus) plus roadmap met
  vier geplande changes (`add-drift-gates`, `add-hub-mcp`,
  `add-agent-guardrails`, `add-docs-claims`).
- Spec-reparaties uit review 2026-07-11:
  - Spec-delta's toegevoegd voor `docs-contract` en `handbook-portal`
    (SHALL-requirements met scenario's); change 1 gemotiveerd zonder delta
    (read-only audit).
  - Contract-check-script als taak 3.5 in change 3 (PR-gate + sha-gepinde
    pre-push hook voor spokes; hergebruik Conduction-script als optie).
  - Pages-mechaniek gecorrigeerd in change 3: `pages`-BRANCH in het
    handbook-repo (subpad `/handbook`) i.p.v. een apart `pages`-repo (dat
    zou de root claimen); proposal en taken 1.2/3.2 aangepast.
  - PROMPT.md: token-scopes per change gespecificeerd (read-only voor de
    audit, minimale write/PR-scopes per forge voor change 2).
  - Inventaris-verversregel toegevoegd (change 2, taak 4.3): repos.json
    herijken bij elk archiefmoment.
  - "Alleen additief" in change 2 herformuleerd tot "geen verplaatsingen
    buiten taak 2.2".
  - README vervangen door één beschrijvende alinea (dubbele koppen weg).

## 2026-07-11

- Openspec-specs voor het personal-handbook-ecosysteem toegevoegd
  (`personal-handbook-openspec/`): project-context, PROMPT, en drie changes
  (`audit-repo-inventory` → `add-docs-contract` → `add-handbook-portal`).
- Concrete homelab-identifiers (hostnamen, VPN-product, GPU-fix) uit de specs
  gestript omdat dit repo publiek is; verplaatst naar het gitignorede
  `personal-handbook-openspec/openspec/private/homelab-context.md`, conform
  het fail-closed-principe uit de specs zelf.
- `.gitignore` toegevoegd die de private map uitsluit.
- Lokale `main` gereconcilieerd met `origin/main` (histories waren ongerelateerd;
  lokale first commit was een subset van de remote en is komen te vervallen).
