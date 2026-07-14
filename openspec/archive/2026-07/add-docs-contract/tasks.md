# Tasks: add-docs-contract

Vereist: door Mark vastgestelde `inventory/repos.json` uit change 1.

## 1. Volgorde bepalen

- [ ] 1.1 Sorteer repos met `needs_docs: yes` op prioriteit:
      (1) kernset-repos (zeef, openanonymiser, wanderer, estafette),
      (2) homelab-infra, (3) overige active, (4) maintained.
      Rationale: deze repos hebben externe docs-lezers; daar zit de deadline-druk.

## 2. Per repo (herhaal, één PR per repo)

- [ ] 2.1 Branch `docs/contract` vanaf default branch.
- [ ] 2.2 Leg `docs/`-structuur aan volgens het contract. Migreer bestaande
      losse docs (bv. `ARCHITECTURE.md`, `docs/*.md` zonder structuur) naar de
      juiste Diátaxis-map; laat een stub met verwijzing achter op de oude plek
      als er externe links naartoe kunnen bestaan.
- [ ] 2.3 Vul front matter aan op elke pagina; `last_reviewed` = datum van
      daadwerkelijke review, niet blind vandaag. Niet gereviewde gemigreerde
      pagina's krijgen `status: draft` met `last_reviewed` = migratiedatum;
      een echte review zet later `current` + een verse datum.
- [ ] 2.4 Indien `needs_mcp_json: yes`: voeg `.mcp.json` toe volgens template.
      Handbook-URL als placeholder `TODO-change-3` laten staan.
- [ ] 2.5 Schrijf/actualiseer `docs/index.md`: één alinea wat het project is,
      status, link naar README, link naar de drie secties.
- [ ] 2.6 Open PR met vaste titel `docs: apply handbook docs contract` en
      een body die per punt uit het contract afvinkt wat is toegepast.
- [ ] 2.7 STOP per repo: PR's worden door Mark gemerged, niet door de agent.

## 3. Homelab-specifiek

- [ ] 3.1 Voor repos met `sensitivity: private-only`: expliciet in
      `docs/index.md` vermelden dat deze docs NIET in de publieke handbook-
      import gaan (zie change 3, private sectie).
- [ ] 3.2 Homelab-reference minimaal: node-overzicht (alle nodes en de
      beheer-VM; concrete namen: zie `openspec/private/homelab-context.md`,
      niet gecommit), netwerkmodel op conceptueel niveau, herstelvolgorde
      (cold start). Bekende fixes als how-to vastleggen — begin met de
      terugkerende (zie private context).

## 4. Afsluiting

- [ ] 4.1 Update `inventory/repos.json`: `has_docs` en `has_mcp_json`
      bijwerken naar de nieuwe werkelijkheid na merge.
- [ ] 4.2 Rapporteer: welke repos klaar, welke PR's open, welke geweigerd.
- [ ] 4.3 Verversregel: bij elk archiefmoment (een change gaat naar
      `openspec/archive/`) wordt `inventory/repos.json` herijkt tegen de
      forges, zodat de inventaris niet stilzwijgend veroudert.
