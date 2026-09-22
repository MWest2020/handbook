#!/usr/bin/env python3
"""Genereer/verifieer de per-spoke agent-seeds uit de canonieke bron.

The execution roles live canonically in `docs/agents/seeds/<role>.md`. Every
spoke that has seeds (`prep/seeds/<spoke>/.claude/agents/<role>.md`) gets an
exact copy of them. That is how a builder is the same builder everywhere.

Usage:
  uv run scripts/gen_agent_seeds.py            # (re)generate the seeds
  uv run scripts/gen_agent_seeds.py --check    # drift gate: exit 1 on deviation
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "agents" / "seeds"
SEEDS_DIR = ROOT / "prep" / "seeds"


def canonical() -> dict[str, str]:
    return {p.stem: p.read_text() for p in sorted(SRC.glob("*.md"))}


def spoke_targets(role: str):
    for agents_dir in sorted(SEEDS_DIR.glob("*/.claude/agents")):
        yield agents_dir / f"{role}.md"


def main() -> int:
    check = "--check" in sys.argv[1:]
    src = canonical()
    if not src:
        print("no canonical seeds in docs/agents/seeds/", file=sys.stderr)
        return 1
    drift = []
    written = 0
    for role, content in src.items():
        for target in spoke_targets(role):
            if not target.exists() or target.read_text() != content:
                if check:
                    drift.append(str(target.relative_to(ROOT)))
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(content)
                    written += 1
    if check:
        if drift:
            print("DRIFT — these seeds deviate from the canonical source:", file=sys.stderr)
            for d in drift:
                print("  " + d, file=sys.stderr)
            print("fix with: uv run scripts/gen_agent_seeds.py", file=sys.stderr)
            return 1
        print("seeds match the canonical source")
        return 0
    print(f"seeds generated/updated: {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
