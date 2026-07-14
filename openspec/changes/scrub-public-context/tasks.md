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

## 2. Repo-bestanden (na scope-besluit Mark)

- [ ] 2.1 `inventory/repos.json` + `repos.md`: financieringstrajecten uit
      de notes; koppeling repo↔traject naar een private overlay
      (gitignored bestand of buiten dit repo). Validatievelden
      (`handbook_import`, `sensitivity`) blijven ongemoeid.
- [ ] 2.2 Besluit: blijft `mkdocs.private.yml` (met private import-URLs)
      in dit publieke repo, of verhuist de private build-config naar de
      interne beheer-host?
- [ ] 2.3 `openspec/archive/` en `prep/seeds/`: trajectvermeldingen
      scrubben of accepteren als historisch (besluit Mark).
- [ ] 2.4 Besluit git-history: oude index/inventaris blijven in de
      publieke historie staan. Opties: laten staan, history rewrite
      (force push, vereist expliciete bevestiging), of repo private
      (breekt gratis GitHub Pages).

## 3. Sluitstuk

- [ ] 3.1 Spec-delta mergen in de vastgestelde specs en change archiveren
      conform propose→apply→archive.
- [ ] 3.2 Westmarch-spec-repo synchroon houden (delta staat daar al,
      commit 2026-07-14).
