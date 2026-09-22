---
status: current
last_reviewed: 2026-09-22
---

# Test gate (verify check per spoke)

The test half of "do not merge without green tests *and* up-to-date docs" (the
docs half is [docs-gates](docs-gates.md)). Every imported spoke has a PR check
called **`verify`**; what it runs depends on the kind of repo. There is
deliberately **no central test runner** — tests are not uniform the way the
docs contract is (one needs service containers, another validates infra). The
hub provides templates and counts the coverage (`verify_gate` in
`inventory/repos.json`); the spoke owns its own workflow.

Enforcement is a signal, not a block: a red X, no branch protection on the solo
repos (see [docs-gates](docs-gates.md#wiring-it-up-caller-template)).

## Template — Python (uv + pytest)

For spokes with a `pyproject.toml` and a `tests/` directory (skill-forge,
wordsworth, and the like):

```yaml
name: verify
on:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --frozen
      - run: uv run pytest -q
```

If your suite needs service containers (Postgres, OpenSearch, …), use
`services:` the way wordsworth already does in its `ci.yml` — that counts as
the verify.

## Template — shell + manifests (habitat)

No unit suite; validate what is there. `--severity=warning` lets deliberate
informational noise through (SC2016 on an envsubst `$VAR`, for example), and
envsubst templates are not parsed as static YAML (they validate server-side
after rendering):

```yaml
name: verify
on:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: shellcheck
        run: |
          sudo apt-get update -qq && sudo apt-get install -y shellcheck >/dev/null
          find . -name '*.sh' -not -path './openspec/changes/archive/*' -print0 \
            | xargs -0 -r shellcheck --severity=warning
      - name: yaml-syntax
        run: |
          python3 - <<'PY'
          import glob, yaml, sys
          bad = 0
          for f in glob.glob('**/*.yml', recursive=True) + glob.glob('**/*.yaml', recursive=True):
              if '/archive/' in f or 'job-template' in f:   # envsubst template, not static YAML
                  continue
              try:
                  list(yaml.safe_load_all(open(f)))
              except Exception as e:
                  print(f'YAML ERROR {f}: {e}'); bad = 1
          sys.exit(bad)
          PY
```

## Template — infra (homelab)

Cheap, and without credentials or `init` (a signal gate, not a deploy):

```yaml
name: verify
on:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - name: terraform fmt
        run: terraform fmt -check -recursive
      - name: yaml-syntax
        run: |
          python3 - <<'PY'
          import glob, yaml, sys
          bad = 0
          for f in glob.glob('**/*.yml', recursive=True) + glob.glob('**/*.yaml', recursive=True):
              try:
                  list(yaml.safe_load_all(open(f)))
              except Exception as e:
                  print(f'YAML ERROR {f}: {e}'); bad = 1
          sys.exit(bad)
          PY
```

## Coverage

`inventory/repos.json` carries `verify_gate` per imported spoke:

- `yes` — a `verify` check runs on pull requests;
- `n/a` — no meaningful verify is possible (an explicit decision; no fake
  suite);
- `no` — still to do.
