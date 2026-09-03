#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Contract-gate: elk niet-leeg facet van een agent-definitie declareert tools
(allow/deny) en skills, en de executie-allowlist komt overeen met de seed.

Stdlib-only (geen yaml-dep — conform de andere hub-scripts). Het front-matter-
formaat is gecontroleerd: `tools: { allow: [...], deny: [...] }` en `skills: [...]`
inline per facet. Checks per `docs/agents/<naam>.md` met een `agent:`-front-matter
(index.md en de seeds/ vallen buiten):
  1. elk niet-leeg facet (chat/executie) heeft `tools.allow`, `tools.deny` en
     `skills` (lijsten; deny/skills mogen leeg zijn);
  2. `allow` en `deny` overlappen niet;
  3. voor een executie-facet met een seed (expliciet `seed:` of per conventie
     `docs/agents/seeds/<habitat_rol>.md`) is `executie.tools.allow` gelijk aan de
     `tools:`-regel van die seed — de allowlist die habitat uitvoert.

Gebruik: check_agent_tools.py        (exit 1 bij schending; bare output, CI-script)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
AGENTS = ROOT / "docs" / "agents"


def front_matter(path: pathlib.Path) -> str:
    txt = path.read_text()
    if not txt.startswith("---"):
        return ""
    return txt.split("---", 2)[1]


def _list(inner: str) -> list[str]:
    return [x.strip() for x in inner.split(",") if x.strip()]


def facet_block(fm: str, facet: str):
    """(aanwezig, is_null, blok-tekst) voor een facet op 2-spatie-indent."""
    lines = fm.splitlines()
    hdr = next((i for i, ln in enumerate(lines) if re.match(rf"^  {facet}:", ln)), None)
    if hdr is None:
        return (False, False, "")
    rest = re.match(rf"^  {facet}:\s*(\S.*)?$", lines[hdr]).group(1) or ""
    if rest.split("#")[0].strip() == "null":
        return (True, True, "")
    body = []
    for ln in lines[hdr + 1:]:
        if ln.strip() == "":
            continue
        if len(ln) - len(ln.lstrip()) <= 2:
            break
        body.append(ln)
    return (True, False, "\n".join(body))


def seed_tools(seed_rel: str) -> list[str]:
    m = re.search(r"^tools:\s*(.*)$", front_matter(ROOT / seed_rel), re.M)
    return _list(m.group(1)) if m else []


def check_facet(rel: str, facet: str, block: str, errs: list):
    mt = re.search(r"^\s*tools:\s*(.*)$", block, re.M)
    ma = re.search(r"allow:\s*\[([^\]]*)\]", mt.group(1)) if mt else None
    md = re.search(r"deny:\s*\[([^\]]*)\]", mt.group(1)) if mt else None
    if not (mt and ma and md):
        errs.append(f"{rel}/{facet}: mist `tools.allow`/`tools.deny` als inline-lijsten")
        return  # zonder geldig tools-blok geen overlap-/seed-check (dubbele fout vermeden)
    ms = re.search(r"^\s*skills:\s*(.*)$", block, re.M)
    msl = re.search(r"^\s*\[([^\]]*)\]\s*$", ms.group(1)) if ms else None
    if not ms:
        errs.append(f"{rel}/{facet}: mist `skills` (gebruik `[]` als er geen zijn)")
    elif not msl:
        errs.append(f"{rel}/{facet}: `skills` moet een lijst zijn (`[...]`)")

    allow, deny = _list(ma.group(1)), _list(md.group(1))
    overlap = sorted(set(allow) & set(deny))
    if overlap:
        errs.append(f"{rel}/{facet}: allow en deny overlappen: {overlap}")

    if facet == "executie":
        mseed = re.search(r"^\s*seed:\s*(\S+)", block, re.M)
        mrol = re.search(r"^\s*habitat_rol:\s*([^\s#]+)", block, re.M)
        seed = mseed.group(1) if mseed else None
        if not seed and mrol:
            cand = f"docs/agents/seeds/{mrol.group(1)}.md"
            seed = cand if (ROOT / cand).exists() else None
        if seed and not (ROOT / seed).exists():
            errs.append(f"{rel}/executie: `seed:` wijst naar niet-bestaand pad {seed}")
        elif seed:
            st = seed_tools(seed)
            if set(allow) != set(st):
                errs.append(f"{rel}/executie: `tools.allow` {sorted(allow)} wijkt af van "
                            f"seed {seed} tools {sorted(st)}")


def main() -> int:
    errs: list[str] = []
    checked = 0
    for path in sorted(AGENTS.glob("*.md")):
        fm = front_matter(path)
        if not re.search(r"^agent:", fm, re.M):
            continue  # index.md e.d. — geen agent-def
        checked += 1
        rel = str(path.relative_to(ROOT))
        for facet in ("chat", "executie"):
            present, is_null, block = facet_block(fm, facet)
            if present and not is_null:
                check_facet(rel, facet, block, errs)
    if errs:
        print("FAIL — agent-tool/skill-contract geschonden:", file=sys.stderr)
        for e in errs:
            print("  " + e, file=sys.stderr)
        return 1
    print(f"agent-tool/skill-contract ok ({checked} definities)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
