#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Drift-gate: koppelt code-wijzigingen aan docs-wijzigingen in een spoke-PR.

Leest de gewijzigde bestanden (één pad per regel op stdin) en faalt wanneer de
PR geconfigureerde code-paden raakt zonder dat er iets onder docs/ meebeweegt.
Puur padgebaseerd en deterministisch — geen inhoudsanalyse.

Gebruik: git diff --name-only BASE HEAD | check_drift.py \\
             --code-paths "dispatch/,worker/,cage/" [--mode warn|fail] [--override]
  --code-paths : komma- of newline-gescheiden globs/prefixes (map/ = prefix)
  --mode       : fail (default) of warn
  --override   : PR draagt label docs-drift-ok → altijd groen, wél gemeld
Exit 1 alleen bij drift én mode=fail én geen override. Bare output.
"""
import fnmatch
import sys


def parse_paths(raw: str) -> list[str]:
    return [p.strip() for p in raw.replace("\n", ",").split(",") if p.strip()]


def matches(path: str, patterns: list[str]) -> bool:
    for pat in patterns:
        if pat.endswith("/") and (path == pat[:-1] or path.startswith(pat)):
            return True
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(path, pat.rstrip("/") + "/*"):
            return True
    return False


def main() -> None:
    args = sys.argv[1:]
    code_paths, docs_paths, mode, override = "", "", "fail", False
    i = 0
    while i < len(args):
        if args[i] == "--code-paths":
            code_paths = args[i + 1]; i += 2
        elif args[i] == "--docs-paths":
            docs_paths = args[i + 1]; i += 2
        elif args[i] == "--mode":
            mode = args[i + 1]; i += 2
        elif args[i] == "--override":
            override = True; i += 1
        else:
            sys.exit(f"onbekend argument: {args[i]}")
    patterns = parse_paths(code_paths)
    if not patterns:
        sys.exit("--code-paths is verplicht")
    # Waar de documentatie van deze spoke woont. Standaard `docs/`, want dat is
    # het contract — maar niet elke spoke heeft hem daar. homelab schrijft zijn
    # runbooks in `docusaurus/docs/` en had daarnaast een `docs/` die sinds
    # augustus stilstond. De gate wees dus naar de dode boom: niet te halen door
    # echte documentatie te schrijven, alleen door de verkeerde map aan te raken
    # of het label te gebruiken. Een gate die je niet eerlijk kunt halen, leert
    # mensen hem te omzeilen.
    docs_patterns = parse_paths(docs_paths or "docs/")

    changed = [ln.strip() for ln in sys.stdin if ln.strip()]
    code_hits = [f for f in changed if matches(f, patterns)]
    docs_touched = any(matches(f, docs_patterns) for f in changed)

    if not code_hits:
        print("drift-gate: geen geconfigureerde code-paden geraakt — n.v.t.")
        return
    if docs_touched:
        print(f"drift-gate: code én {docs_paths or 'docs/'} bewegen mee — OK")
        return

    print(f"drift-gate: code-paden gewijzigd zónder wijziging in {docs_paths or 'docs/'}:")
    for f in code_hits:
        print(f"  - {f}")
    print("Afspraak: wie code wijzigt, werkt docs/ in dezelfde PR bij "
          "(zie de meebeweeg-conventie in README/CLAUDE.md).")
    if override:
        print("drift-gate: label docs-drift-ok aanwezig — bewuste uitzondering, groen.")
        return
    if mode == "warn":
        print("drift-gate: mode=warn — waarschuwing, geen gate.")
        return
    print("Voeg docs-wijzigingen toe of zet het label docs-drift-ok op de PR.")
    sys.exit(1)


if __name__ == "__main__":
    main()
