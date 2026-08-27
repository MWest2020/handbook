#!/usr/bin/env python3
"""Genereer/verifieer de per-spoke agent-seeds uit de canonieke bron.

De executie-rollen leven canoniek in `docs/agents/seeds/<rol>.md`. Elke spoke
die seeds heeft (`prep/seeds/<spoke>/.claude/agents/<rol>.md`) krijgt daarvan
een exacte kopie. Zo is een builder overal dezelfde builder.

Gebruik:
  uv run scripts/gen_agent_seeds.py            # (her)genereer de seeds
  uv run scripts/gen_agent_seeds.py --check    # drift-gate: exit 1 bij afwijking
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
        print("geen canonieke seeds in docs/agents/seeds/", file=sys.stderr)
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
            print("DRIFT — deze seeds wijken af van de canonieke bron:", file=sys.stderr)
            for d in drift:
                print("  " + d, file=sys.stderr)
            print("herstel met: uv run scripts/gen_agent_seeds.py", file=sys.stderr)
            return 1
        print("seeds komen overeen met de canonieke bron")
        return 0
    print(f"seeds gegenereerd/bijgewerkt: {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
