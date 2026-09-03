#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Contract-gate: elk niet-leeg facet van een agent-definitie declareert tools
(allow/deny) en skills, en de executie-allowlist komt overeen met de seed.

Checks per `docs/agents/<naam>.md` met een `agent:`-front-matter (index.md en de
seeds/ vallen buiten):
  1. elk niet-leeg facet (chat/executie) heeft `tools.allow`, `tools.deny` en
     `skills` (lijsten; deny/skills mogen leeg zijn);
  2. `allow` en `deny` overlappen niet;
  3. voor een executie-facet met `seed:` is `executie.tools.allow` gelijk aan de
     `tools:`-regel van die seed (de allowlist die habitat uitvoert).

Gebruik: check_agent_tools.py        (exit 1 bij schending; bare output, CI-script)
"""
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
AGENTS = ROOT / "docs" / "agents"


def front_matter(path: pathlib.Path):
    txt = path.read_text()
    if not txt.startswith("---"):
        return None
    try:
        return yaml.safe_load(txt.split("---", 2)[1])
    except yaml.YAMLError as e:
        raise SystemExit(f"{path.relative_to(ROOT)}: front matter is geen geldige YAML: {e}")


def seed_tools(seed_rel: str) -> list[str]:
    """De `tools:`-regel van een seed als lijst (seed-formaat: 'A, B, C')."""
    fm = front_matter(ROOT / seed_rel)
    raw = (fm or {}).get("tools", "")
    if isinstance(raw, list):
        return [str(t).strip() for t in raw]
    return [t.strip() for t in str(raw).split(",") if t.strip()]


def seed_for(f: dict) -> str | None:
    """Het seed-pad van een executie-facet: expliciet `seed:`, anders per conventie
    `docs/agents/seeds/<habitat_rol>.md`. Zo wordt de consistentiecheck NIET stil
    overgeslagen als iemand `seed:` vergeet terwijl de seed wél bestaat."""
    if f.get("seed"):
        return f["seed"]
    rol = f.get("habitat_rol")
    cand = f"docs/agents/seeds/{rol}.md" if rol else None
    return cand if cand and (ROOT / cand).exists() else None


def check_facet(rel: str, facet: str, f: dict, errs: list):
    tools = f.get("tools")
    tools_ok = isinstance(tools, dict) and "allow" in tools and "deny" in tools
    if not tools_ok:
        errs.append(f"{rel}/{facet}: mist `tools.allow`/`tools.deny`")
    if "skills" not in f:
        errs.append(f"{rel}/{facet}: mist `skills` (gebruik `[]` als er geen zijn)")
    if not tools_ok:
        return  # zonder tools-blok geen zin in overlap-/seed-check (dubbele fout)
    allow, deny = tools.get("allow") or [], tools.get("deny") or []
    for key, val in (("allow", tools.get("allow")), ("deny", tools.get("deny")), ("skills", f.get("skills"))):
        if val is not None and not isinstance(val, list):
            errs.append(f"{rel}/{facet}: `{key}` moet een lijst zijn")
    overlap = sorted(set(allow) & set(deny))
    if overlap:
        errs.append(f"{rel}/{facet}: allow en deny overlappen: {overlap}")
    if facet == "executie":
        seed = seed_for(f)
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
        if not isinstance(fm, dict) or "agent" not in fm:
            continue  # index.md e.d. — geen agent-def
        checked += 1
        rel = str(path.relative_to(ROOT))
        for facet in ("chat", "executie"):
            f = fm["agent"].get(facet)
            if isinstance(f, dict):
                check_facet(rel, facet, f, errs)
    if errs:
        print("FAIL — agent-tool/skill-contract geschonden:", file=sys.stderr)
        for e in errs:
            print("  " + e, file=sys.stderr)
        return 1
    print(f"agent-tool/skill-contract ok ({checked} definities)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
