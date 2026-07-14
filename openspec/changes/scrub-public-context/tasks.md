# Tasks: scrub-public-context

## 1. Site-pagina's (direct, in deze branch)

- [x] 1.1 `docs/index.md`: trajectlabels weg, koppeling van een publiek
      repo aan een privaat repo weg, private-sectie-alinea vervangen
      door één kale verwijzingszin.
- [x] 1.2 `docs/homelab/herstel.md`: private repo-namen en
      redactie-datum verwijderd; alleen de functionele uitleg blijft.
- [ ] 1.3 Private overzichtspagina toevoegen die alleen in
      `mkdocs.private.yml` genavigeerd wordt (template staat in de
      gitignored `openspec/private/` van het Westmarch-spec-repo).

## 2. Repo-bestanden (scope-besluiten Mark, 2026-07-14)

- [x] 2.1 `inventory/repos.json` + `repos.md`: financieringstrajecten en
      gevoelige-pointer-notes uit de publieke notes; verplaatst naar de
      private overlay in de gitignored `openspec/private/`.
      Validatievelden (`handbook_import`, `sensitivity`) ongemoeid.
- [x] 2.2 BESLOTEN: private build-config verhuist naar de beheer-host.
      `mkdocs.private.yml` ge-untrackt + gitignored (lokale kopie blijft
      voor de private build); `scripts/gen_imports.py` slaat een afwezige
      private config over, getest met en zonder.
- [x] 2.3 BESLOTEN: scrubben. `openspec/archive/`, `prep/seeds/` en
      `openspec/project.md` ontdaan van trajectvermeldingen;
      repo-namen blijven staan (repo-info mag publiek).
- [x] 2.4 BESLOTEN: git-history laten staan. Geen rewrite, geen
      visibility-wijziging; het verbod geldt vanaf nu.

## 3. Sluitstuk

- [ ] 3.1 Spec-delta mergen in de vastgestelde specs en change archiveren
      conform propose→apply→archive.
- [ ] 3.2 Westmarch-spec-repo synchroon houden (delta staat daar al,
      commit 2026-07-14).
