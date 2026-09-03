# Design: add-skills-register-check

## Bron in skill-forge, mirror in de handbook

De catalogus "welke skills bestaan" hoort bij de skill-bibliotheek (skill-forge):
een skill bestaat = skill-forge heeft 'm gepromoveerd. De handbook mag daar geen
tweede bron van maken (tegen "één bron van waarheid"). Daarom is
`inventory/skills-register.yml` een **mirror** van skill-forge's `forge register`-
uitvoer, niet een eigen lijst — precies zoals de agent-seeds een mirror van de
canonieke bron zijn en de importlijst uit de inventaris komt.

## Refresh + drift (interim → gate)

Nu: de mirror wordt ververst door skill-forge's `register.yml` te kopiëren naar
`inventory/skills-register.yml` (na een promote/demote in skill-forge). Dat is de
boring-eerste-stap. De eindvorm is een drift-gate zoals bij de seeds: de nightly
haalt skill-forge's `register.yml` op en faalt als de mirror afwijkt — zodat "de
mirror is vers" afdwingbaar wordt i.p.v. een belofte. Die automatisering is een
vervolg; deze change legt de consumptie + validatie vast.

## Afdwinging via CI (human-gate)

De gate valideert; de CI-stap die 'm draait (`handbook.yml`) voegt Mark met de hand
toe — CI-config is een human-gate en deze change raakt CI niet. Zonder die stap is
de gate lokaal/handmatig draaibaar maar niet PR-blokkerend; dat geldt voor de hele
`check_agent_tools.py` (tools én skills), niet alleen deze uitbreiding.

## Stdlib-parsing

De gate blijft stdlib-only (geen yaml-dep, conform de andere hub-scripts): het
register wordt geparsed via de `- slug: <x>`-regels. Het manifest heeft een
gecontroleerd formaat (gegenereerd door `forge register`), dus regex volstaat en
faalt luid als de vorm verandert.

## Wat deze check WEL en NIET doet

WEL: valideren dat elke gedeclareerde skill een gepromoveerde skill-forge-skill is
(geen phantom-namen, geen typefouten). NIET: de skill aan de uitvoerende agent
leveren. Tools zijn verankerd aan de seed omdat de seed is wat habitat draait
(`--allowedTools`); skills bereiken de seed/kooi vandaag niet. Die asymmetrie is
bewust en zichtbaar: `skills:` is een gevalideerde *declaratie van relevantie*, en
skill-*provisioning* (seed-`skills:` + kooi-mount + een tools-achtige pariteit-check)
is een aparte vervolg-change. Zo levert deze change echte waarde (namen kloppen)
zonder te doen alsof skills al enforced draaien.

## Waarom `security → thinking-red-team` nu wél mag

In de vorige change wees de review `skills: [thinking-red-team]` terecht af: niet
te verifiëren. Nu staat die skill in het register (gepromoveerd in skill-forge),
dus de gate kruist 'm en de claim is hard. Dat is precies het gat dat deze change
dicht.
