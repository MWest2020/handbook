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
     `tools:`-regel van die seed — de allowlist die habitat uitvoert;
  4. elke `skills:`-entry bestaat in het skill-register (`inventory/skills-register.yml`,
     mirror van skill-forge) — onbekende skill of ontbrekend register bij niet-lege
     skills → FAIL.

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


def seed_tools(seed_rel: str):
    """De `tools:`-regel van een seed als lijst, of None als de regel ONTBREEKT.
    (In Claude Code betekent een afwezige `tools:` "alle tools" — het tegendeel van
    een lege lijst — dus die twee mogen niet samenvallen.)"""
    m = re.search(r"^tools:\s*(.*)$", front_matter(ROOT / seed_rel), re.M)
    return _list(m.group(1)) if m else None


SKIP_NO_AGENT = {"index.md"}  # docs/agents/*.md die géén agent-def zijn
REGISTER = ROOT / "inventory" / "skills-register.yml"  # mirror van skill-forge


def register_slugs():
    """De slugs uit het skill-register (mirror van skill-forge's `register.yml`),
    of None als het manifest ontbreekt. Stdlib: elke skill staat als `- slug: <x>`.
    Zo blijft "welke skills bestaan" één bron (skill-forge), hier alleen gespiegeld."""
    if not REGISTER.exists():
        return None
    return set(re.findall(r"^\s*-\s*slug:\s*(\S+)", REGISTER.read_text(), re.M))


def check_facet(rel: str, facet: str, block: str, errs: list, notices: list, reg):
    # Skills EERST, onafhankelijk van het tools-blok: anders zou een def die z'n
    # tools-blok kwijt is (early return hieronder) een onbekende skill pas volgende
    # run tonen. reg is None = register ontbreekt; lege set = register kapot/leeg
    # (daarvoor faalt main al één keer, hier geen per-skill-ruis).
    ms = re.search(r"^\s*skills:\s*(.*)$", block, re.M)
    msl = re.search(r"^\s*\[([^\]]*)\]\s*$", ms.group(1)) if ms else None
    if not ms:
        errs.append(f"{rel}/{facet}: mist `skills` (gebruik `[]` als er geen zijn)")
    elif not msl:
        errs.append(f"{rel}/{facet}: `skills` moet een lijst zijn (`[...]`)")
    else:
        skills = _list(msl.group(1))
        if skills and reg is None:
            errs.append(f"{rel}/{facet}: skills {skills} maar het register "
                        f"({REGISTER.relative_to(ROOT)}) ontbreekt — kan niet valideren")
        elif skills and reg:
            unknown = sorted(s for s in skills if s not in reg)
            if unknown:
                errs.append(f"{rel}/{facet}: onbekende skill(s) {unknown} — niet in het "
                            f"skill-register (alleen gepromoveerde skill-forge-skills)")

    mt = re.search(r"^\s*tools:\s*(.*)$", block, re.M)
    ma = re.search(r"allow:\s*\[([^\]]*)\]", mt.group(1)) if mt else None
    md = re.search(r"deny:\s*\[([^\]]*)\]", mt.group(1)) if mt else None
    if not (mt and ma and md):
        errs.append(f"{rel}/{facet}: mist `tools.allow`/`tools.deny` als inline-lijsten")
        return  # zonder geldig tools-blok geen overlap-/seed-check (dubbele fout vermeden)
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
            if st is None:
                errs.append(f"{rel}/executie: seed {seed} heeft geen `tools:`-regel — "
                            f"de allowlist is onbepaald (voeg 'm toe aan de seed)")
            elif set(allow) != set(st):
                errs.append(f"{rel}/executie: `tools.allow` {sorted(allow)} wijkt af van "
                            f"seed {seed} tools {sorted(st)}")
        else:
            # Geen seed: allow niet te kruisen. Expliciet melden (design belooft
            # "geen stille ok"), geen fout — een bekende, begrensde beperking.
            notices.append(f"{rel}/executie: geen seed — `allow` niet gekruist (intentie).")


def main() -> int:
    errs: list[str] = []
    notices: list[str] = []
    reg = register_slugs()
    if REGISTER.exists() and reg is not None and not reg:
        # Bestand is er maar levert geen slugs op: afgekapte kopie, leeg bestand of
        # een formaatwijziging in `forge register`. Eén duidelijke fout i.p.v. elke
        # gedeclareerde skill als "onbekend" wegstrepen.
        errs.append(f"{REGISTER.relative_to(ROOT)} bevat geen skill-slugs — "
                    f"kapotte/afgekapte mirror? (verwacht `- slug:`-regels)")
    checked = 0
    for path in sorted(AGENTS.glob("*.md")):
        rel = str(path.relative_to(ROOT))
        fm = front_matter(path)
        if not re.search(r"^agent:", fm, re.M):
            # Dekking afdwingen: een def die z'n front-matter kwijtraakt mag niet
            # stil doorglippen. Alleen een expliciete allowlist (index.md) is oké.
            if path.name not in SKIP_NO_AGENT:
                errs.append(f"{rel}: geen `agent:`-front-matter — een agent-def hoort "
                            f"'m te hebben (of zet 'm in {sorted(SKIP_NO_AGENT)}).")
            continue
        checked += 1
        for facet in ("chat", "executie"):
            present, is_null, block = facet_block(fm, facet)
            if not present:
                # Een volledig ontbrekende facet-sleutel is dubbelzinnig: "geen
                # facet" hoort expliciet `null` te zijn. Zo glipt een def die z'n
                # tools verliest door de hele sleutel te droppen niet stil door.
                errs.append(f"{rel}: mist de `{facet}:`-sleutel — gebruik een blok of "
                            f"expliciet `{facet}: null`")
            elif not is_null:
                check_facet(rel, facet, block, errs, notices, reg)
    for n in notices:
        print("  · " + n)
    if errs:
        print("FAIL — agent-tool/skill-contract geschonden:", file=sys.stderr)
        for e in errs:
            print("  " + e, file=sys.stderr)
        return 1
    print(f"agent-tool/skill-contract ok ({checked} definities)")
    return 0


def _selftest() -> int:
    """Test de gate-logica zelf (northstar: gates die zelf getest zijn). Draait
    op gemaakte facet-blokken, geen filesystem — pure logica-asserties.
    Gebruik: check_agent_tools.py --selftest"""
    reg = {"thinking-red-team", "no-ai-slop"}
    cases = []

    def run(name, block, want_ok, want_sub="", facet="executie", r=reg):
        errs, notices = [], []
        check_facet("x.md", facet, block, errs, notices, r)
        ok = not errs
        passed = (ok == want_ok) and (want_sub == "" or any(want_sub in e for e in errs))
        cases.append((name, passed, errs))

    OKTOOLS = "tools: { allow: [Read, Bash], deny: [Write] }"
    run("geldige skill", f"{OKTOOLS}\nskills: [thinking-red-team]", True)
    run("onbekende skill", f"{OKTOOLS}\nskills: [does-not-exist]", False, "onbekende skill")
    run("register ontbreekt + skills", f"{OKTOOLS}\nskills: [thinking-red-team]",
        False, "ontbreekt", r=None)
    run("lege skills slaagt", f"{OKTOOLS}\nskills: []", True)
    run("mist skills-veld", OKTOOLS, False, "mist `skills`")
    run("allow/deny overlap", "tools: { allow: [Read, Write], deny: [Write] }\nskills: []",
        False, "overlappen")
    run("skills gecheckt ondanks tools-blok weg", "skills: [does-not-exist]",
        False, "onbekende skill")

    fails = [(n, e) for n, ok, e in cases if not ok]
    for n, ok, _ in cases:
        print(f"  {'ok ' if ok else 'FAIL'} {n}")
    if fails:
        print(f"SELFTEST FAIL: {[n for n, _ in fails]}", file=sys.stderr)
        return 1
    print(f"selftest ok ({len(cases)} gevallen)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(_selftest())
    raise SystemExit(main())
