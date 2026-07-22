# handbook-portal Specification

## Purpose
De publieke hub-build lekt geen private of financiële context: hub-eigen
pagina's én niet-gerenderde repo-bestanden blijven vrij van
financieringstrajecten, private repo-namen en homelab-details.
## Requirements
### Requirement: Hub-eigen pagina's lekken geen private of financiële context

Hub-eigen pagina's in de publieke build (index, conventies, homelab-verwijzing) SHALL geen van de onderstaande drie categorieën bevatten.

1. subsidie- of financieringstrajecten — welk programma, fonds of
   aanvraagtraject dan ook; niet als label bij een repo, niet als
   lopende tekst;
2. namen van `private-only` repos of een opsomming van wat de private
   build aggregeert;
3. homelab-/infradetails, inclusief meta-informatie over wat er
   geredigeerd is en sinds wanneer.

Vermelding van de private sectie SHALL beperkt blijven tot het kale
bestaan ervan (één verwijzingszin), zonder inhoudsopgave. Beschrijvingen
van publieke repos SHALL beperkt blijven tot wat het repo zelf al publiek
documenteert. Dit is nodig omdat de repo-splitsing (fail closed) alleen
imports dekt; hub-eigen pagina's delen hun bron tussen publieke en private
build en vallen daar buiten.

#### Scenario: Subsidietraject op de publieke index

- WHEN een hub-eigen pagina in de publieke build een repo aanduidt met
  zijn subsidie- of financieringstraject
- THEN wordt dat bij review geweigerd en verwijderd vóór deploy

#### Scenario: Private repos opgesomd op de publieke index

- WHEN een hub-eigen pagina in de publieke build `private-only` repos bij
  naam noemt of de inhoud van de private sectie beschrijft
- THEN wordt de passage teruggebracht tot maximaal één verwijzingszin
  zonder repo-namen, of verplaatst naar een pagina die alleen in
  `mkdocs.private.yml` genavigeerd wordt

### Requirement: Repo-bestanden van de publieke hub lekken geen private of financiële context

Het verbod hierboven SHALL ook gelden voor niet-gerenderde bestanden in
het publieke hub-repo (inventaris-notes, configs, seeds, gearchiveerde
changes): het repo zelf is publiek, dus alles daarin is publicatie —
niet alleen wat mkdocs rendert.

#### Scenario: Financieringstraject in inventaris-notes

- WHEN een `notes`-veld in `inventory/repos.json`/`repos.md` een repo
  koppelt aan een subsidie- of financieringstraject
- THEN verhuist die koppeling naar een private overlay (gitignored of
  buiten dit repo) en blijft in de publieke inventaris alleen de
  functionele informatie staan

