# Change 3 (add-handbook-portal) — open vragen: BESLIST 2026-07-12

De drie open vragen zijn beantwoord en in de proposal/tasks verwerkt:

## 1. Forge → GitHub `MWest2020` (niet Codeberg)

Besluit Mark: alles personal blijft op GitHub; Codeberg is werkcontext
(werkgever-org) en blijft volledig buiten dit ecosysteem. Het `handbook`-repo
komt dus op GitHub, deploy via GitHub Pages (`mwest2020.github.io/handbook/`,
orphan branch `gh-pages`, alleen CI pusht).

## 2. CI → GitHub Actions

Zelfde workflow-syntax als het oorspronkelijke Forgejo Actions-voorstel, op de
forge waar alles al staat; het habitat-worker-image bouwt er al. Nightly
rebuild als cron in dezelfde workflow.

## 3. Private build → on-demand eerst

`uv run mkdocs build -f mkdocs.private.yml` als gedocumenteerd commando;
automatisering op de interne beheer-host pas als de private sectie stabiel
is (herzien na een maand). Private imports via read-only token, alleen in de
private build — nooit in de publieke Pages-workflow.

## Kanttekening bij hergebruik contract-check (tasks 3.5)

De optie "bestaand contract-check-script hergebruiken" verwijst naar
werkcontext-tooling; buiten bereik. Nieuwbouw is klein (front-matter-parse +
mappenlijst-check, ±80 regels).
