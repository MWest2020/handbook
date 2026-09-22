#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Contract gate: every non-empty facet of an agent definition declares tools
(allow/deny) and skills, and the execution allowlist matches the seed.

Stdlib only (no yaml dependency — in line with the other hub scripts). The front
matter format is controlled: `tools: { allow: [...], deny: [...] }` and
`skills: [...]` inline per facet. Checked per `docs/agents/<name>.md` that has an
`agent:` front matter (index.md and seeds/ are out of scope):
  1. every non-empty facet (chat/executie) has `tools.allow`, `tools.deny` and
     `skills` (lists; deny and skills may be empty);
  2. `allow` and `deny` do not overlap;
  3. for an execution facet with a seed (an explicit `seed:` or, by convention,
     `docs/agents/seeds/<habitat_rol>.md`) `executie.tools.allow` equals that
     seed's `tools:` line — the allowlist habitat actually runs;
  4. every `skills:` entry exists in the skill register
     (`inventory/skills-register.yml`, a mirror of skill-forge) — an unknown
     skill, or a missing register with a non-empty skills list, is a FAIL.

Note: the front-matter KEYS (`naam`, `chat`, `executie`) stay as they are. They
are parsed here and by ratatoskr's agents/bootstrap.py; renaming one is a
cross-repo change, not a translation.

Usage: check_agent_tools.py      (exit 1 on a violation; bare output, a CI script)
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
    """(present, is_null, block text) for a facet at two-space indent."""
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
    """A seed's `tools:` line as a list, or None when the line is ABSENT.
    (In Claude Code an absent `tools:` means "all tools" — the opposite of an empty
    list — so those two must never be conflated.)"""
    m = re.search(r"^tools:\s*(.*)$", front_matter(ROOT / seed_rel), re.M)
    return _list(m.group(1)) if m else None


SKIP_NO_AGENT = {"index.md"}  # docs/agents/*.md that are NOT agent definitions
REGISTER = ROOT / "inventory" / "skills-register.yml"  # mirror van skill-forge


def register_slugs():
    """The slugs from the skill register (a mirror of skill-forge's `register.yml`),
    or None when the manifest is missing. Stdlib: every skill appears as `- slug: <x>`.
    Zo blijft "welke skills bestaan" één bron (skill-forge), hier alleen gespiegeld."""
    if not REGISTER.exists():
        return None
    return set(re.findall(r"^\s*-\s*slug:\s*(\S+)", REGISTER.read_text(), re.M))


# Toegestane modellen. De def legt de INTENTIE vast (zoeken/denken/uitzondering),
# not an exact model id: that rotates per release and would expire every definition.
# Regel (Mark, 2026-09-06): zoeken = haiku, denken = sonnet, uitzonderlijk = opus.
MODELS = {"haiku", "sonnet", "opus"}


def check_facet(rel: str, facet: str, block: str, errs: list, notices: list, reg):
    # Model: mandatory, and from the fixed set. Without this field an agent runs on
    # whatever the environment happens to default to — exactly what we do not want.
    mm = re.search(r"^\s*model:\s*(\S+)\s*$", block, re.M)
    if not mm:
        errs.append(f"{rel}/{facet}: missing `model` (one of {sorted(MODELS)})")
    elif mm.group(1) not in MODELS:
        errs.append(f"{rel}/{facet}: unknown model {mm.group(1)!r} "
                    f"(allowed: {sorted(MODELS)})")
    # Skills FIRST, independent of the tools block: otherwise a definition that has
    # lost its tools block (the early return below) would only surface an unknown
    # skill on the next run. reg is None = the register is missing; an empty set =
    # the register is broken or empty (main already fails once for that, so no
    # per-skill noise here).
    ms = re.search(r"^\s*skills:\s*(.*)$", block, re.M)
    msl = re.search(r"^\s*\[([^\]]*)\]\s*$", ms.group(1)) if ms else None
    if not ms:
        errs.append(f"{rel}/{facet}: missing `skills` (use `[]` when there are none)")
    elif not msl:
        errs.append(f"{rel}/{facet}: `skills` must be a list (`[...]`)")
    else:
        skills = _list(msl.group(1))
        if skills and reg is None:
            errs.append(f"{rel}/{facet}: skills {skills} but the register "
                        f"({REGISTER.relative_to(ROOT)}) is missing — cannot validate")
        elif skills and reg:
            unknown = sorted(s for s in skills if s not in reg)
            if unknown:
                errs.append(f"{rel}/{facet}: unknown skill(s) {unknown} — not in the "
                            f"skill register (promoted skill-forge skills only)")

    mt = re.search(r"^\s*tools:\s*(.*)$", block, re.M)
    ma = re.search(r"allow:\s*\[([^\]]*)\]", mt.group(1)) if mt else None
    md = re.search(r"deny:\s*\[([^\]]*)\]", mt.group(1)) if mt else None
    if not (mt and ma and md):
        errs.append(f"{rel}/{facet}: missing `tools.allow`/`tools.deny` as inline lists")
        return  # without a valid tools block, no overlap or seed check (avoids a double error)
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
            errs.append(f"{rel}/executie: `seed:` points at a non-existent path {seed}")
        elif seed:
            # Cross-check the model: the worker will read the role file in the target
            # repo, so seed and definition must name the same model — otherwise a run
            # uses something other than what the registry promises.
            sm = re.search(r"^model:\s*(\S+)\s*$", (ROOT / seed).read_text(), re.M)
            if not sm:
                errs.append(f"{rel}/executie: seed {seed} has no `model:` line")
            elif mm and sm.group(1) != mm.group(1):
                errs.append(f"{rel}/executie: model {mm.group(1)!r} differs from "
                            f"seed {seed} model {sm.group(1)!r}")
            st = seed_tools(seed)
            if st is None:
                errs.append(f"{rel}/executie: seed {seed} has no `tools:` line — "
                            f"the allowlist is undetermined (add it to the seed)")
            elif set(allow) != set(st):
                errs.append(f"{rel}/executie: `tools.allow` {sorted(allow)} differs from "
                            f"seed {seed} tools {sorted(st)}")
        else:
            # No seed: `allow` cannot be cross-checked. Say so explicitly (the design
            # promises "no silent ok"), but not as an error — a known, bounded limit.
            notices.append(f"{rel}/executie: no seed — `allow` not cross-checked (intent).")


def check_identity(rel: str, stem: str, fm: str, errs: list, notices: list) -> None:
    """The front-matter contract at identity level (add-agent-registry 1.5): a
    definition names itself and its key. Without this check a definition could lose
    its `naam` or `npub` without anything failing — while the listener compares
    fail-closed on exactly that npub, and a wrong name points an agent at the wrong
    file."""
    m = re.search(r"^  naam:\s*(\S.*)$", fm, re.M)
    if not m:
        errs.append(f"{rel}: missing `naam:` in the front matter")
    elif m.group(1).strip() != stem:
        errs.append(f"{rel}: `naam: {m.group(1).strip()}` differs from the filename "
                    f"{stem!r} — consumers fetch the definition by filename")
    if not re.search(r"^  npub:\s*\S", fm, re.M):
        errs.append(f"{rel}: missing `npub:` — use an explicit `npub: null` when the "
                    f"identity does not exist yet")
    elif re.search(r"^  npub:\s*null\s*(#.*)?$", fm, re.M):
        notices.append(f"{rel}: `npub: null` — the identity does not exist yet "
                       f"(a chat facet cannot run with this).")


def main() -> int:
    errs: list[str] = []
    notices: list[str] = []
    reg = register_slugs()
    if REGISTER.exists() and reg is not None and not reg:
        # The file exists but yields no slugs: a truncated copy, an empty file, or a
        # format change in `forge register`. One clear error instead of striking
        # off every declared skill as "unknown".
        errs.append(f"{REGISTER.relative_to(ROOT)} contains no skill slugs — "
                    f"a broken or truncated mirror? (expected `- slug:` lines)")
    checked = 0
    for path in sorted(AGENTS.glob("*.md")):
        rel = str(path.relative_to(ROOT))
        fm = front_matter(path)
        if not re.search(r"^agent:", fm, re.M):
            # Enforce coverage: a definition that loses its front matter must not slip
            # through silently. Only an explicit allowlist (index.md) is fine.
            if path.name not in SKIP_NO_AGENT:
                errs.append(f"{rel}: no `agent:` front matter — an agent definition should "
                            f"have one (or list it in {sorted(SKIP_NO_AGENT)}).")
            continue
        checked += 1
        check_identity(rel, path.stem, fm, errs, notices)
        for facet in ("chat", "executie"):
            present, is_null, block = facet_block(fm, facet)
            if not present:
                # A wholly missing facet key is ambiguous: "no facet" should be an
                # explicit `null`. This way a definition that loses its tools by
                # dropping the whole key does not slip through silently.
                errs.append(f"{rel}: missing the `{facet}:` key — use a block or an "
                            f"explicit `{facet}: null`")
            elif not is_null:
                check_facet(rel, facet, block, errs, notices, reg)
    for n in notices:
        print("  · " + n)
    if errs:
        print("FAIL — agent-tool/skill contract violated:", file=sys.stderr)
        for e in errs:
            print("  " + e, file=sys.stderr)
        return 1
    print(f"agent-tool/skill contract ok ({checked} definitions)")
    return 0


def _selftest() -> int:
    """Test the gate logic itself (northstar: gates that are themselves tested).
    Runs on constructed facet blocks, no filesystem — pure logic assertions.
    Usage: check_agent_tools.py --selftest

    Every block carries a `model:` line, because `model` is mandatory for a
    non-empty facet. Without it two cases failed on the missing model rather
    than on what they meant to test, and the selftest had been red for that
    reason (found 2026-09-22; it runs in no CI step, which is why nobody saw)."""
    reg = {"thinking-red-team", "no-ai-slop"}
    cases = []

    def run(name, block, want_ok, want_sub="", facet="executie", r=reg):
        errs, notices = [], []
        check_facet("x.md", facet, block, errs, notices, r)
        ok = not errs
        passed = (ok == want_ok) and (want_sub == "" or any(want_sub in e for e in errs))
        cases.append((name, passed, errs))

    MODEL = "model: sonnet"
    OKTOOLS = f"{MODEL}\ntools: {{ allow: [Read, Bash], deny: [Write] }}"
    run("valid skill", f"{OKTOOLS}\nskills: [thinking-red-team]", True)
    run("unknown skill", f"{OKTOOLS}\nskills: [does-not-exist]", False, "unknown skill")
    run("register missing + skills", f"{OKTOOLS}\nskills: [thinking-red-team]",
        False, "is missing", r=None)
    run("empty skills passes", f"{OKTOOLS}\nskills: []", True)
    run("missing skills field", OKTOOLS, False, "missing `skills`")
    run("allow/deny overlap",
        f"{MODEL}\ntools: {{ allow: [Read, Write], deny: [Write] }}\nskills: []",
        False, "overlap")
    run("skills checked even with the tools block gone", f"{MODEL}\nskills: [does-not-exist]",
        False, "unknown skill")

    fails = [(n, e) for n, ok, e in cases if not ok]
    for n, ok, _ in cases:
        print(f"  {'ok ' if ok else 'FAIL'} {n}")
    if fails:
        print(f"SELFTEST FAIL: {[n for n, _ in fails]}", file=sys.stderr)
        return 1
    print(f"selftest ok ({len(cases)} cases)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(_selftest())
    raise SystemExit(main())
