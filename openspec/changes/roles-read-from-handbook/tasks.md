## 1. Seeds read, not copied

- [x] 1.1 Add `docs/agents/seeds/architect.md`; point `docs/agents/architect.md`
      `executie.seed` at it. Proof: `check_agent_tools.py` cross-checks the
      architect's `allow` against the seed (no "no seed" note).
- [x] 1.2 Remove `prep/seeds/` and `scripts/gen_agent_seeds.py`, and the CI step
      that runs it. Proof: CI green without the step; no reference left outside
      the archive and the changelog.
- [x] 1.3 Update `docs/agents/index.md`: how habitat reads a role (pinned
      handbook commit, fail closed), and Bash in the cage per role.

## 2. Afterwards (not in this change)

- [ ] 2.1 Set `HABITAT_HANDBOOK_REF` in the factory and roll out habitat's
      worker image `ef0b4ef`.
- [ ] 2.2 Remove the spokes' own `.claude/agents/` copies.
