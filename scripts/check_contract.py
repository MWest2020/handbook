#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Contract-check: valideert per geïmporteerd repo het docs-contract.

Checks per repo (shallow clone):
  1. docs/index.md bestaat
  2. markdown uitsluitend in docs-root, how-to/, reference/, explanation/
     (ADR's onder explanation/adr/); asset-mappen zonder .md zijn vrij
  3. elke pagina heeft front matter met status + last_reviewed, geen owner

Gebruik: check_contract.py [--all | --repo-dir PATH]
  default        : alleen public-ok imports (anonieme clones, CI op elke PR)
  --all          : ook private-only imports (vereist GH_TOKEN met read-scope)
  --repo-dir PATH: check één lokale werkkopie (spoke-PR-gate, geen clone/inventaris)
Exit 1 bij schending. Bare output (CI-script).
"""
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOWED = ("how-to", "reference", "explanation")
FM = re.compile(r"\A---\s*\n(.*?)\n---", re.DOTALL)


def clone(repo: str, dest: pathlib.Path, token: str | None) -> bool:
    auth = f"x-access-token:{token}@" if token else ""
    url = f"https://{auth}github.com/MWest2020/{repo}.git"
    r = subprocess.run(
        ["git", "clone", "--quiet", "--depth", "1", url, str(dest)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"FOUT {repo}: clone mislukt")
        return False
    return True


def check_repo(repo: str, docs: pathlib.Path) -> list[str]:
    errs = []
    if not (docs / "index.md").is_file():
        errs.append("docs/index.md ontbreekt")
    for page in sorted(docs.rglob("*.md")):
        rel = page.relative_to(docs)
        top = rel.parts[0] if len(rel.parts) > 1 else None
        if top is not None and top not in ALLOWED:
            errs.append(f"{rel}: markdown buiten de Diátaxis-mappen ({top}/)")
            continue
        fm_match = FM.match(page.read_text(encoding="utf-8", errors="replace"))
        if not fm_match:
            errs.append(f"{rel}: geen front matter")
            continue
        fm = fm_match.group(1)
        for veld in ("status:", "last_reviewed:"):
            if veld not in fm:
                errs.append(f"{rel}: front matter mist {veld[:-1]}")
        if re.search(r"^owner\s*:", fm, re.MULTILINE):
            errs.append(f"{rel}: owner-veld is niet toegestaan")
    return errs


def check_local(repo_dir: str) -> None:
    """Spoke-PR-gate: valideer één lokale werkkopie, zonder clone of inventaris."""
    root = pathlib.Path(repo_dir)
    name = root.name
    if not (root / "docs").is_dir():
        print(f"OK {name}: geen docs/ (contract n.v.t.)")
        return
    errs = check_repo(name, root / "docs")
    if errs:
        for e in errs:
            print(f"SCHENDING {name}: {e}")
        sys.exit(1)
    print(f"OK {name}: docs-contract voldaan")


def main() -> None:
    if "--repo-dir" in sys.argv:
        i = sys.argv.index("--repo-dir")
        if i + 1 >= len(sys.argv):
            sys.exit("--repo-dir vereist een pad")
        check_local(sys.argv[i + 1])
        return
    include_private = "--all" in sys.argv
    token = os.environ.get("GH_TOKEN")
    rows = json.loads((ROOT / "inventory" / "repos.json").read_text())
    rows = [r for r in rows if r["handbook_import"] == "yes" and r.get("contract_applied") == "yes"]
    if not include_private:
        rows = [r for r in rows if r["sensitivity"] == "public-ok"]
    elif not token:
        sys.exit("--all vereist GH_TOKEN voor private clones")

    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        for r in sorted(rows, key=lambda r: r["repo"].lower()):
            repo = r["repo"]
            dest = pathlib.Path(tmp) / repo
            use_token = token if r["sensitivity"] == "private-only" else None
            if not clone(repo, dest, use_token):
                failures += 1
                continue
            errs = check_repo(repo, dest / "docs")
            if errs:
                failures += 1
                for e in errs:
                    print(f"SCHENDING {repo}: {e}")
            else:
                print(f"OK {repo}")
    if failures:
        sys.exit(1)
    print("contract: alle geïmporteerde repos voldoen")


if __name__ == "__main__":
    main()
