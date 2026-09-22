#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Generate or validate the mkdocs import lists from inventory/repos.json.

The inventory is the single source of truth about which repos take part
(northstar: site and agents read exactly the same list). This script writes the
blocks between the BEGIN/END markers in mkdocs.yml (public) and
mkdocs.private.yml (private; untracked, existing only where the private build
runs) — or validates with --check that they have not drifted (CI). An absent
mkdocs.private.yml is skipped.

Criteria:
  public  : handbook_import=yes  sensitivity=public-ok    has_docs=yes
  private : handbook_import=yes  sensitivity=private-only  has_docs=yes

Gebruik: gen_imports.py [--check]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BEGIN = "        # BEGIN IMPORTS (beheerd door scripts/gen_imports.py)"
END = "        # END IMPORTS"


def import_lines(rows: list[dict]) -> str:
    lines = [BEGIN]
    for r in sorted(rows, key=lambda r: r["repo"].lower()):
        lines.append(f"        - section: {r['repo']}")
        lines.append(
            f"          import_url: 'https://github.com/MWest2020/{r['repo']}"
            f"?branch=main&docs_dir=docs/*'"
        )
    lines.append(END)
    return "\n".join(lines)


def replace_block(text: str, block: str, path: str) -> str:
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(text):
        sys.exit(f"{path}: markers missing")
    return pattern.sub(block, text)


def main() -> None:
    check = "--check" in sys.argv
    rows = json.loads((ROOT / "inventory" / "repos.json").read_text())
    rows = [r for r in rows if r["handbook_import"] == "yes" and r.get("contract_applied") == "yes"]
    pub = [r for r in rows if r["sensitivity"] == "public-ok"]
    priv = [r for r in rows if r["sensitivity"] == "private-only"]

    drift = False
    # privaat = alles (publiek + private-only); publiek = alleen public-ok
    for path, subset in (("mkdocs.yml", pub), ("mkdocs.private.yml", pub + priv)):
        f = ROOT / path
        if not f.exists():
            # mkdocs.private.yml is untracked (it lives on the administration host);
            # in CI and fresh clones it is absent and there is nothing to validate.
            print(f"{path}: absent, skipped")
            continue
        old = f.read_text()
        new = replace_block(old, import_lines(subset), path)
        if old != new:
            drift = True
            if check:
                print(f"DRIFT: {path} is out of sync with inventory/repos.json")
            else:
                f.write_text(new)
                print(f"{path}: import block updated ({len(subset)} repos)")
        else:
            print(f"{path}: in sync ({len(subset)} repos)")
    if check and drift:
        sys.exit(1)


if __name__ == "__main__":
    main()
