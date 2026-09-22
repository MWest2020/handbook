#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Regenerate the GitHub table in inventory/repos.md from inventory/repos.json.

repos.json is the single source of truth (see AGENTS.md). This generator writes
the table between two marker comments; all handwritten prose (intro, Codeberg,
Settled, TBD, Not covered) is left alone. Idempotent: run it as often as you like.

Usage: uv run scripts/gen_inventory_md.py  (or: python3 scripts/gen_inventory_md.py)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "inventory" / "repos.json"
MD_PATH = ROOT / "inventory" / "repos.md"

BEGIN = "<!-- BEGIN generated:github-table (from inventory/repos.json; do not edit by hand) -->"
END = "<!-- END generated:github-table -->"

COLUMNS = [
    "repo", "forge", "tier", "visibility", "sensitivity",
    "has_docs", "has_mcp_json", "needs_mcp_json", "needs_docs",
    "handbook_import", "notes",
]


def _cell(value: object) -> str:
    """Eén tabelcel: pipes escapen, newlines platslaan."""
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def build_table(records: list[dict]) -> str:
    github = sorted(
        (r for r in records if r.get("forge") == "github"),
        key=lambda r: r["repo"].lower(),
    )
    lines = [
        "| " + " | ".join(COLUMNS) + " |",
        "|" + "|".join(["---"] * len(COLUMNS)) + "|",
    ]
    for r in github:
        lines.append("| " + " | ".join(_cell(r.get(c)) for c in COLUMNS) + " |")
    return "\n".join(lines)


def splice(md: str, block: str) -> str:
    """Replace the marked block, or — on a first run without markers — the table
    region between '## GitHub' and the next '## ' heading."""
    marked = f"{BEGIN}\n{block}\n{END}"

    if BEGIN in md and END in md:
        pre, rest = md.split(BEGIN, 1)
        _, post = rest.split(END, 1)
        return pre + marked + post

    lines = md.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines) if ln.strip().startswith("## GitHub"))
    except StopIteration:
        sys.exit("heading '## GitHub' not found in repos.md")
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    head = lines[: start + 1]
    tail = lines[end:]
    return "\n".join(head + ["", marked, ""] + tail) + ("\n" if md.endswith("\n") else "")


def main() -> None:
    records = json.loads(JSON_PATH.read_text())
    md = MD_PATH.read_text()
    out = splice(md, build_table(records))
    if not out.endswith("\n"):
        out += "\n"
    MD_PATH.write_text(out)
    n = sum(1 for r in records if r.get("forge") == "github")
    print(f"repos.md updated: {n} GitHub repos in the generated table")


if __name__ == "__main__":
    main()
