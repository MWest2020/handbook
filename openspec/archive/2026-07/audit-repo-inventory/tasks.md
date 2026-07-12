# Tasks: audit-repo-inventory

Read-only. Geen commits naar bestaande repos. Werkdirectory: lokale scratch.

## 1. Repos ophalen

- [ ] 1.1 Codeberg: haal alle repos op via de Forgejo API:
      `curl -s -H "Authorization: token $CODEBERG_TOKEN" "https://codeberg.org/api/v1/user/repos?limit=50&page=N"`
      (pagineer tot leeg). Leg per repo vast: name, private, archived,
      updated_at, default_branch, description.
- [ ] 1.2 GitHub: idem via `gh repo list MWest2020 --limit 200 --json name,visibility,isArchived,updatedAt,description`.
- [ ] 1.3 Dedupliceer mirrors: als een repo op beide forges staat, bepaal het
      canonieke exemplaar (waar wordt gepusht?) en markeer de ander als
      `notes: mirror`.

## 2. Per repo inspecteren (alleen tier active/maintained-kandidaten)

- [ ] 2.1 Shallow clone (`git clone --depth 1`) of gebruik de contents-API —
      géén volledige clones van grote repos.
- [ ] 2.2 Check: bestaat `/docs`? Zo ja: telt het ≥1 inhoudelijk bestand
      (geen lege index)? → `has_docs: yes/partial/no`.
- [ ] 2.3 Check: `.mcp.json` in root → `has_mcp_json`.
- [ ] 2.4 Check agent-sporen: `.claude/`, `CLAUDE.md`, `openspec/` →
      input voor `needs_mcp_json`.
- [ ] 2.5 Check licentie: LICENSE aanwezig? EUPL-1.2? Afwijking → `notes`.
- [ ] 2.6 Bepaal `sensitivity`: bevat de repo of z'n docs interne hostnames,
      IP's, VPN-/overlay-netwerknamen, secrets-paden of topologie? → `private-only`.
      Bij twijfel: `private-only` (fail closed).

## 3. Homelab-gap

- [ ] 3.1 Vergelijk de repo-lijst met de bekende homelab-inventaris (concrete
      nodes en netwerk-config: zie `openspec/private/homelab-context.md`,
      niet gecommit). Alles wat
      draait maar geen repo heeft: aparte sectie "ongedekt" in repos.md.
      NIET oplossen, alleen benoemen.

## 4. Output

- [ ] 4.1 Schrijf `inventory/repos.md`: één tabel, kolommen exact zoals in
      proposal.md, alfabetisch per forge. Onderaan: sectie "TBD" met open
      vragen, sectie "ongedekt" met homelab-gaps.
- [ ] 4.2 Schrijf `inventory/repos.json` met identieke inhoud (array van
      objecten, veldnamen exact als tabelkolommen).
- [ ] 4.3 STOP. Presenteer de tabel ter review. Change 2 start pas na
      expliciete goedkeuring van de classificatie.
