# Tasks: add-docs-gates

## 1. Hub (dit repo)

- [ ] 1.1 `scripts/check_contract.py`: `--repo-dir PATH`-modus (hergebruik
      `check_repo()`, geen clone/inventaris; bare output, exit 1 bij schending)
- [ ] 1.2 `.github/workflows/docs-gates.yml` (`workflow_call`): inputs
      `code_paths` (globs), `drift_mode` (warn|fail, default fail);
      contract-gate + drift-gate; label-override `docs-drift-ok`
- [ ] 1.3 Caller-template vastleggen in de docs (±12 regels, met
      voorbeeld-`code_paths` per spoke-type)

## 2. Testmatrix (habitat als proefspoke)

- [ ] 2.1 Contractbreuk → rood; drift → rood; label-override → groen;
      code+docs → groen (vier PR-varianten, resultaat vastleggen in de PR's)

## 3. Uitrol naar de spokes (habitat-builder-Jobs)

- [ ] 3.1 habitat (code_paths: dispatch/, worker/, cage/, report/, orchestrator/)
- [ ] 3.2 homelab
- [ ] 3.3 wordsworth
- [ ] 3.4 zettelkast
- [ ] 3.5 skill-forge
- [ ] 3.6 Per spoke: check verplicht maken op main (branch protection — Mark)

## 4. Afronding

- [ ] 4.1 Reference-pagina in `docs/` van dit repo (wat de gates doen, hoe een
      spoke aanhaakt, wanneer het label gerechtvaardigd is)
- [ ] 4.2 `inventory/repos.json`-notes bijwerken (gate uitgerold per spoke)
