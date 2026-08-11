# Changelog

## 2026-08-11 (OpenAnonymiser-fork: strip-to-text-only)

- `strip-to-text-only` uitgevoerd op de MWest2020-fork. Bevinding: de fork was al
  gestript (geen document/DB/crypto/PDF/transformers-laag; die files bestonden hier
  niet, base-deps schoon, geen `charts/`). De change was tegen de zwaardere upstream
  geschreven. **Effectieve wijziging:** de default plugin-config (`plugins.yaml`)
  draaide GLiNER (torch) met de regex-recognizers uit, waardoor de slanke build niet
  startte (`ImportError: GLiNER is not installed`) — nu de text-only default (SpaCy
  NER + alle regex-recognizers, geen GLiNER/torch); GLiNER/GPU blijft in
  `plugins.gpu.yaml` (`Dockerfile.gpu`). Live geverifieerd: `/health`, `/analyze`
  (BSN/PERSON/PHONE/IBAN via SpaCy+regex), `/anonymize`. `Dockerfile.classic` al
  text-only (statisch geverifieerd; docker build/run niet mogelijk in de agent-omgeving
  — geen daemon-toegang). Spec `text-only-api` naar delta-format + gearchiveerd.
  `split-into-3-flavors` blijft open (niet gevraagd).

## 2026-08-11 (zeef: 4 gereconcilieerd + gearchiveerd; bm25 hand-rolled)

- Op beslissing Mark de zeef-4 spec-owner-reconciliatie gedaan: criteria-scoring,
  converge-ranking, structured-llm-score, topic-clustering archiveerden niet
  doordat hun MODIFIED-deltas op hernoemde/gesuperseded requirement-headers
  mikten. Per requirement op inhoud gemerged in dependency-volgorde (export
  "Inventory export" → base "Excel inventory of the selection" + motivatie/doc_type
  als superset; retrieve-rerank LLM-scoring gemerged tot converge's side-score-
  invariant + structured-output, stale top-K-demotie verwijderd). Niets uit
  al-gearchiveerde changes overschreven; eindspecs zonder dubbele headers. Alle
  vier gearchiveerd. **bm25-reuse afgevoerd** (beslissing Mark: hand-rolled BM25
  behouden — de rank_bm25-swap brak ordening-equivalentie op kleine corpora).
  zeef heeft nu geen open changes meer behalve het cross-repo `apply-docs-contract`.

## 2026-08-11 (ecosysteem-sweep: open punten "graph style" opgeruimd)

- Graph-style aanpak: eerst een read-only triage-workflow (7 thuislabrepos, 1
  lezer per repo), daarna gericht uitvoeren. **Gearchiveerd (af, alleen
  bookkeeping):** zeef-eval 3, Billbird 4 (plan-command's live-deploy-taken als
  operator-deferred), zeef 6, Wanderer 1 (research-high-signal-observability, op
  beslissing Mark; design-principe naar project-hygiene gemerged). **Gecommit:**
  homelab CrowdSec A.2 (live-infra-merge, 21 remote-commits, CHANGELOG-union).
  **Gebouwd:** estafette `submission-v1` — PR-submissie + crawl/harvester
  (poc.yaml, publiccode-fallback), verse reviewer+security PASS incl. hardening
  (https-only fetch/redirects, `assessment`-strip op geharvestte entries,
  slug-guard), 17 tests, gearchiveerd.
- **Eerlijke muren (spec-owner/omgeving, niet geforceerd):** zeef `bm25-reuse`
  (rank_bm25-swap breekt ordening-equivalentie op kleine corpora → semantiek-
  keuze); zeef ×4 (criteria-scoring/converge-ranking/structured-llm-score/
  topic-clustering: stale/gesuperseded spec-deltas vs gedreven base →
  reconciliatie); ash-nazg `wire-dosbox-engine` (vereist docker + NC/AppAPI-stack);
  OpenAnonymiser ×2 (breaking refactors op de MWest2020-fork — groot/richting).
- OpenAnonymiser_light lokaal omgehangen naar de MWest2020-fork (weg van de
  Conduction/Codeberg-remote) zodat het in-mandate bewerkbaar is.
- Buiten scope/geblokkeerd: Conduction-repos (hard geblokkeerd). `apply-docs-contract`
  blijft in meerdere repos open (delta-loze cross-repo docs-change, vers remote-werk).

## 2026-08-11 (habitat: run-artefacten gehard — N1 + N3)

- Vervolg op `reproducible-diff-hash`: de twee lage security-residuen (round 3)
  netjes afgerond in `harden-run-artifacts`. **N1** — `.habitat/run-output-<id>.md`
  werd alleen geschreven bij een `result` in de `claude -p`-JSON; nu schrijft
  `habitat_report.py` dit **altijd** (placeholder zonder result), ná de diff-hash
  en per exacte naam uitgesloten, zodat habitat het artefact bezit en een agent er
  geen eigen versie voor kan smokkelen. **N3** — een beschadigde `audit.jsonl`-regel
  liet het rapport crashen; nu fail-closed (`prev_hash=""`) en onleesbare regels
  worden als expliciet gebroken rij getoond i.p.v. stil weggelaten (security-F1),
  zodat de keten niet "opgeschoond" kan worden. Reviewer + security **PASS**;
  nieuwe image (`e5dcfac`); cluster-sanity groen (run-output habitat-geschreven,
  `diff_hash` reproduceerbaar). Direct naar `main` (thuislab, geen PR).
  Gearchiveerd; habitat zonder open changes.

## 2026-08-10 (habitat: reproduceerbare diff_hash, geen .habitat/-smokkelkanaal)

- Een livetest-reviewer signaleerde dat `run-report.json` **2** bestanden meldde
  terwijl de commit er **6** bevatte: de `diff_hash` werd op report-tijd berekend
  (vóór de habitat-artefacten gecommit werden), dus niet reproduceerbaar vanaf de
  gepushte branch — precies het punt van de audit-keten. `reproducible-diff-hash`
  sluit nu **exact de run-artefacten** uit (vaste naam + dispatch-run-id,
  `literal`-pathspec, géén wildcard): `.habitat/audit.jsonl`,
  `.habitat/run-report-<id>.html`, `.habitat/run-output-<id>.md`,
  `run-report.json`. Security-review ging **3 rondes**: grove `.habitat/`-exclusie
  (round 1) en naam-wildcard (round 2, `*` matcht ook `/`) waren allebei
  agent-noembare smokkelkanalen → exacte run-id-exclusie sluit ze; élk ander
  bestand dat de agent onder `.habitat/` schrijft blijft nu in de hash. Nieuwe
  worker-image (`084f9db`); cluster-sanity groen: de opgeslagen `diff_hash`
  reproduceert exact vanaf de branch via het `diff_hash_scope`-commando. Eerste
  change **direct naar `main`** gemerged (thuislab, geen PR); reviews + gates als
  kwaliteitscheck vóór de merge. Gearchiveerd; habitat zonder open changes.

## 2026-08-10 (habitat-testrepo: livetest-fixture 2.1)

- De `add-greeting`-fixture op `habitat-testrepo` liet de rol-keten struikelen:
  taak 2.1 eiste de exitcode van `scripts/verify.sh`, die niemand produceert
  (de builder mag geen `bash` draaien), dus 2.1 bleef onafgevinkt → reviewer-FAIL.
  Herschreven zodat de builder 2.1 kan afvinken via inspectie (Read), met de
  builder-Stop-hook als uitvoeringsbewijs (groene Job = verify gedraaid+geslaagd).
  Testrepo-only (wegwerp-fixture), geen platform-code. Her-geverifieerd met
  `chain.sh`: **hele keten groen** — architect/builder/reviewer/security alle vier
  `AFGEROND`; reviewer flipte van `failed` naar `ok` (reviewer+security read-only,
  leeg-hash diff).

## 2026-08-10 (habitat: robuuste dispatch-wait)

- `dispatch.sh` wachtte te kort (~180s) → een cold image-pull of lange run
  eindigde ten onrechte als "onbekend" (exit 2), wat de exit-code onbetrouwbaar
  maakte (ook voor `chain.sh`). `robust-dispatch-wait` (PR #15): één lus die
  wacht op een terminale Job-conditie met timeout `ACTIVE_DEADLINE_SECONDS+600`.
  Dispatch-only (geen image). Reviewer PASS; cluster-sanity: `AFGEROND` + exit 0.
  Gearchiveerd. Habitat blijft zonder open openspec-changes.

## 2026-08-10 (habitat: run-unieke branches + chain.sh)

- Vervolg op de rol-architectuur-livetest: de worker pushte niet-deterministisch
  (`habitat/<rol>/<change>` met `-<run_id>`-fallback), wat de reviewer/security-
  lookup na een builder-retry brak. `run-unique-branches` (PR #14): branch is nu
  **altijd** `habitat/<rol>/<change>-<run_id>` (niet-destructief, geen force,
  elke run bewaard), en nieuw `dispatch/chain.sh` draait de volle keten en geeft
  de builder-branch door aan reviewer/security. Besluit Mark: niet force-pushen,
  wél run-uniek + threading.
- Cluster-geverifieerd (image 4b11c83): run-unieke namen, `chain.sh`-threading en
  keten-gate (stopt bij rol-FAIL) werken. 2 reviewrondes (reviewer+security PASS;
  fix: chain stopt nu op de dispatch-exit i.p.v. die te negeren).
- Gearchiveerd. Habitat blijft **zonder open openspec-changes**.

## 2026-08-10 (habitat: rol-architectuur live-bewezen)

- **Cluster-livetests van `add-role-architecture` groen** (image 232583a) op
  `habitat-testrepo`: architect/reviewer/security aantoonbaar read-only
  (diff_hash = leeg-hash), builder door de Stop-hook geverifieerd, idempotentie
  (identieke diff_hash bij herhaling), end-to-end keten met verdict-propagatie
  (rol-FAIL → Job Failed), en de Stop-hook blokkeert een falende verify.
- **Bug gevonden én gefixt via de eigen keten:** de PreToolUse-guard blokkeerde
  élk `.claude/`-pad, terwijl de worker elke rol opdraagt `.claude/agents/<rol>.md`
  te lezen → architect faalde. Fix `fix-guard-role-definition` (PR #13): Read-
  uitzondering voor rol-definities, symlink-hardening (component-walk), 2 review-
  rondes (reviewer+security, ronde 1 FAIL op symlink-bypass → ronde 2 beide PASS).
- **Deploy-fix:** de `role-architect`-ServiceAccount ontbrak op het cluster →
  `cage/rbac.yaml` toegepast.
- **Beide changes gearchiveerd** (`add-role-architecture`,
  `fix-guard-role-definition`). Habitat heeft nu **geen open openspec-changes**.
- Follow-ups genoteerd (niet-blokkerend): `Glob`/`Grep` buiten de guard,
  hardlink-vector, interpreter-exfil — pre-existing.

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
