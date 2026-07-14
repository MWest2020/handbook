#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Genereer/valideer de mkdocs-importlijsten uit inventory/repos.json.

De inventaris is de enige waarheid over welke repos meedoen (northstar:
site en agents lezen exact dezelfde lijst). Dit script schrijft de blokken
tussen de BEGIN/END-markers in mkdocs.yml (publiek) en mkdocs.private.yml
(privaat; niet getrackt, leeft alleen waar de private build draait) — of
valideert met --check dat ze niet gedrift zijn (CI). Een afwezige
mkdocs.private.yml wordt overgeslagen.

Criteria:
  publiek : handbook_import=yes  sensitivity=public-ok    has_docs=yes
  privaat : handbook_import=yes  sensitivity=private-only  has_docs=yes

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
        sys.exit(f"{path}: markers ontbreken")
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
            # mkdocs.private.yml is niet getrackt (leeft op de beheer-host);
            # in CI/verse clones ontbreekt hij en is er niets te valideren.
            print(f"{path}: afwezig, overgeslagen")
            continue
        old = f.read_text()
        new = replace_block(old, import_lines(subset), path)
        if old != new:
            drift = True
            if check:
                print(f"DRIFT: {path} loopt niet synchroon met inventory/repos.json")
            else:
                f.write_text(new)
                print(f"{path}: importblok bijgewerkt ({len(subset)} repos)")
        else:
            print(f"{path}: synchroon ({len(subset)} repos)")
    if check and drift:
        sys.exit(1)


if __name__ == "__main__":
    main()
