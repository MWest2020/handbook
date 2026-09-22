#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Drift gate: ties code changes to docs changes in a spoke pull request.

Reads the changed files (one path per line on stdin) and fails when the pull
request touches configured code paths without anything under docs/ moving with
it. Purely path-based and deterministic — no content analysis.

Usage: git diff --name-only BASE HEAD | check_drift.py \\
             --code-paths "dispatch/,worker/,cage/" [--mode warn|fail] [--override]
  --code-paths : comma- or newline-separated globs/prefixes (dir/ = prefix)
  --mode       : fail (default) or warn
  --override   : the PR carries the label docs-drift-ok → always green, still reported
Exit 1 only on drift AND mode=fail AND no override. Bare output.
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
        sys.exit("--code-paths is required")
    # Where this spoke's documentation lives. `docs/` by default, because that is
    # the contract — but not every spoke keeps it there. homelab writes its
    # runbooks in `docusaurus/docs/` and also had a `docs/` that had stood still
    # since August. The gate therefore pointed at the dead tree: unsatisfiable by
    # writing real documentation, only by touching the wrong directory or using
    # the label. A gate you cannot pass honestly teaches people to route around
    # it.
    docs_patterns = parse_paths(docs_paths or "docs/")

    changed = [ln.strip() for ln in sys.stdin if ln.strip()]
    code_hits = [f for f in changed if matches(f, patterns)]
    docs_touched = any(matches(f, docs_patterns) for f in changed)

    if not code_hits:
        print("drift gate: no configured code paths touched — not applicable")
        return
    if docs_touched:
        print(f"drift gate: code and {docs_paths or 'docs/'} move together — OK")
        return

    print(f"drift gate: code paths changed without a change in {docs_paths or 'docs/'}:")
    for f in code_hits:
        print(f"  - {f}")
    print("Afspraak: wie code wijzigt, werkt docs/ in dezelfde PR bij "
          "(zie de meebeweeg-conventie in README/AGENTS.md).")
    if override:
        print("drift gate: label docs-drift-ok present — deliberate exception, green.")
        return
    if mode == "warn":
        print("drift gate: mode=warn — a warning, not a gate.")
        return
    print("Add docs changes, or put the label docs-drift-ok on the pull request.")
    sys.exit(1)


if __name__ == "__main__":
    main()
