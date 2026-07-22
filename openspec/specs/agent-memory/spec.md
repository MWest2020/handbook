# agent-memory Specification

## Purpose
Het geheugen van de coördinerende sessie duurzaam, versiebeheerd en lekvrij
bewaren: privaat geback-upt en op gevoeligheid gesplitst, nooit naar een
publiek repo.
## Requirements
### Requirement: Agent-geheugen wordt privaat en op gevoeligheid gesplitst geback-upt

Het geheugen van de coördinerende sessie SHALL versiebeheerd worden geback-upt
naar uitsluitend `private-only` repo's, gesplitst op gevoeligheid: gevoelige
homelab-/topologie-context naar `zettelkast`, werkwijze-/voorkeuren naar
`dotfiles`. Het SHALL nooit naar een publiek repo gaan. De canonieke bron blijft
de lokale memory-map; de repo-kopieën zijn de backup.

#### Scenario: Nieuw, niet-geclassificeerd geheugenbestand

- WHEN een geheugenbestand niet op de expliciete voorkeuren-allowlist staat
- THEN gaat het naar het gevoelige repo (`zettelkast`), niet naar `dotfiles`
  (fail-closed: onbekend telt als gevoelig)

#### Scenario: Doelrepo is niet privaat

- WHEN een sync-doel geen `PRIVATE`-zichtbaarheid heeft
- THEN breekt de sync af zonder te pushen (geen geheugen naar een publiek repo)

#### Scenario: Geen wijziging sinds de vorige sync

- WHEN het canonieke geheugen niet is gewijzigd t.o.v. de backup
- THEN pusht de sync niets (idempotent)

