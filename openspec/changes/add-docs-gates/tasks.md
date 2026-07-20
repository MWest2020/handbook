# Tasks: add-docs-gates

## 1. Hub (dit repo)

- [x] 1.1 `scripts/check_contract.py`: `--repo-dir PATH`-modus (hergebruik
      `check_repo()`, geen clone/inventaris; bare output, exit 1 bij schending)
- [x] 1.2 `.github/workflows/docs-gates.yml` (`workflow_call`): inputs
      `code_paths` (globs), `drift_mode` (warn|fail, default fail);
      contract-gate + drift-gate; label-override `docs-drift-ok`
- [x] 1.3 Caller-template vastleggen in de docs (±12 regels, met
      voorbeeld-`code_paths` per spoke-type)

## 2. Testmatrix (habitat als proefspoke)

- [x] 2.1 Live op GitHub Actions bewezen (habitat test-PR #7, gesloten): contract-gate
      groen op geldige docs + rood op ontbrekende front matter; drift-gate rood op
      code-zonder-docs (`dispatch/`) + groen via label `docs-drift-ok`. Twee wiring-
      lessen meegenomen: `handbook_ref` moet mee vóór merge (main mist de scripts nog),
      en de caller triggert ook op `labeled/unlabeled` zodat het label opnieuw evalueert.

## 3. Uitrol naar de spokes (na merge hub-PR; spokes referen `@main`)

- [ ] 3.1 habitat (code_paths: dispatch/, worker/, cage/, report/, orchestrator/)
- [ ] 3.2 homelab
- [ ] 3.3 wordsworth
- [ ] 3.4 zettelkast
- [ ] 3.5 skill-forge
- [ ] 3.6 Per spoke: check verplicht maken op main (branch protection — Mark)

## 4. Afronding

- [x] 4.1 Reference-pagina `docs/reference/docs-gates.md` (wat de gates doen, hoe een
      spoke aanhaakt via de caller-template, wanneer het label gerechtvaardigd is)
- [ ] 4.2 `inventory/repos.json`-notes bijwerken (gate uitgerold per spoke)
