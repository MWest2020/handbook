---
status: current
last_reviewed: 2026-09-24
---

# Operating agreements

Operational agreements that apply when running the ecosystem but live neither
in code nor in a spec. Short, one per subject; an agent that starts here
abides by them.

This page is canonical. An agent's local memory may point here but does not
override it (spec `agent-memory`). Each rule came out of a concrete incident;
the incident is kept in one line because it is what makes the rule
recognisable the next time.

## Wordsworth — VC reveal gate: never `REQUIRED` with a test or public issuer

Wordsworth can optionally gate a reveal behind a verifiable credential
(EUDI-aligned, see wordsworth `ADR-0003`): with
`WORDSWORTH_VC_REQUIRED=true` a valid credential becomes mandatory for every
reveal.

**Never turn `WORDSWORTH_VC_REQUIRED=true` on while the VC issuer is a test
issuer or otherwise public** — for instance when a valid test credential is
embedded in a public repo.

The reason: if a valid credential is publicly available, anyone can satisfy the
"VC required" check, so enforcing it buys no additional certainty. Real
enforcement needs a **non-public issuer** *and* **holder binding**
(proof-of-possession: key binding plus audience/nonce).

Until that exists the gate stays **additive** (`REQUIRED=false`): a presented
credential can only **narrow** a reveal (the intersection with the grant),
never widen it. That way the gate gives defence in depth without becoming a
single point of trust.

## Skill register — refreshing the mirror

`inventory/skills-register.yml` is a **mirror** of skill-forge's catalogue of
promoted skills (the source is skill-forge, not the handbook). The agent
tool/skill gate validates every `skills:` entry in an agent definition against
it.

Refresh after a `promote` or `demote` in skill-forge:

    # in skill-forge:
    uv run forge register
    # copy the output into the handbook mirror:
    cp ~/skill-forge/register.yml ~/handbook/inventory/skills-register.yml

Commit the mirror in the handbook. A declared skill that is no longer in the
register makes the gate fail — which is the point: no phantom skills.
Refreshing automatically plus a drift gate against skill-forge's live output
(like the seed drift gate) is deferred work.

## How we work

### Work on main and finish the job

On the personal repos, work directly on `main`: no feature branches, no PRs
to ask for approval. "Finish" means the whole chain up to "it runs and it is
proven": merge, tag, deploy, run the end-to-end check, archive the openspec
change, and fix follow-up failures found on the way. Report afterwards *that*
it happened, with the measurement, instead of asking whether it may.

Exceptions, deliberately small:

- `docs/agents/` and `.claude/agents/` in the handbook (CODEOWNERS): the
  owner merges who the agents are.
- A command the auto-mode classifier blocks for the agent (for example a
  self-approving `gh pr merge`, or ratatoskr's `orchestrator/add-member.py`):
  hand it over as a ready-to-run command, not as a question.
- A genuine fork — two defensible directions with different outcomes: one
  short question with a recommendation.
- **wordsworth goes through pull requests.** Its docs-gates (a code change
  must move `docs/` with it) only run on pull requests, so pushing straight to
  `main` would skip them. Branch, open the PR, merge it yourself once every
  check passes — still no asking. Decided by Mark, 2026-09-26.

Before every push: `git fetch` and rebase if origin moved; never force-push
over someone else's work.

When the work goes through a pull request anyway — because a gate only runs on
pull requests, like wordsworth's docs-gates — read its checks before merging.
`gh pr merge` does not wait for them, and without branch protection nothing
stops a red merge: on 2026-09-26 wordsworth #170 went in with its docs gate
failing, fixed afterwards by #171. Merge in the same step that checks every
result is `pass`, never in a command that merges regardless.

### Prefer habitat where a repo is set up for it

For wordsworth and internetnl-cli, build through the habitat chain
(architect → builder → reviewer → security) when that is practical. It is a
preference, not a gate (owner, 2026-09-24): when habitat cannot run the work
(expired credentials, a blocked dependency, a fix too small to dispatch),
build directly and follow the rest of these agreements.

The same holds for curation in skill-forge: a curation decision preferably goes
through a PR with a decision document under `docs/` that also records the
rejections and why, so the owner can review it. Drafts are gitignored, so the
document is the reviewable trail.

### Reads need no permission

Run read-only inspection (`git log/status/diff/show`, `openspec list`, a
project's `ls`-style commands) without asking and without announcing it; show
the result when it matters. Anything that writes — including commands that
look like reads but record state, such as `forge judge` — still gets care.

### Public actions on someone else's repo are the owner's call

Opening an issue or PR on a third-party repository speaks for the owner in
public. Prepare the text and let the owner confirm or post it. The auto-mode
classifier enforces this for `gh issue create`; a comment on an existing issue
passes, but the same judgement applies.

### No branch protection

Do not propose branch protection, protected branches or rulesets — not as a
suggestion, not as an open item. The gate is `verify.sh` in CI plus the local
pre-push guard. If a change or review asks for it, strike it with the reason
"decided". Rejected four times.

### Dispatch long work, stay reachable

For work that takes more than a few minutes (a build, a migration, a research
question), start a named tmux session in its own worktree, or a subagent;
report that it started and stay available. Quick, decisive work stays inline.
Waiting on something external (CI, a deploy, a cron result)? Use `/loop` or a
monitor rather than polling by hand.

Gotchas: interactive prompts do not survive a pipe; `pgrep -f` matches your
own command line (it once killed the owner's tmux session — match an exact
`/proc/*/cmdline` instead); piping `claude` through `tee` in tmux produces
nothing, because the TUI needs a terminal.

### Clear open work

Standing order: do not wait until each item is named. Open openspec changes,
open PRs, handover batons and explicitly deferred follow-ups ("later") are
open work. At the end of a task, check the backlog and take the next item.
Something the owner rejected is not open work.

### One working tree per session

Git does not isolate two actors in one working tree. On a shared checkout,
another session switched the branch mid-session: two commits landed on their
branch, `git push origin main` pushed nothing and exited 0, and `git add -A`
swept their uncommitted rename into our commit. Another time a SOPS
re-encrypt entangled a second session's `identities.yml` work.

- For a long session with many commits: `git worktree add <scratch>/<task>
  origin/main` and work there.
- Before writing in a repo that is not explicitly yours, check for live
  sessions (`tmux ls`; `readlink /proc/<pid>/cwd` of running `claude`
  processes). If one is there, do not write; report.
- In a shared tree anyway: `git branch --show-current` before each commit,
  `git log --oneline origin/main -1` after each push — a push that did nothing
  looks exactly like one that succeeded.

### Check before you claim

A statement about state (merged, open, deployed, left to do) needs a command
in the same turn that produces it — never recite it from an earlier message.
Specifics that bit:

- **A PR's base.** When stacking, re-check that the base is still unmerged;
  GitHub does not always retarget. One merge landed a whole change on a dead
  branch.
- **A status field is not the state.** ArgoCD reported `Synced` while the pod
  ran the old digest. Verify the artefact, not the tool's opinion of itself.
- **The working directory.** `cd` does not always persist between tool calls;
  use absolute paths.
- **A value has more than one source.** Env comes from `env:` *and*
  `envFrom:`; check the running process, not one of its inputs.

## Testing and evidence

### Smoke the real artefact before merge

Unit and integration tests in isolation are not enough. Before calling
something ready, run the externally observable artefact: boot the binary
against a real database and hit an endpoint, run the MCP exchange over stdio,
open the page. If that is not possible, say so and label the work "needs live
verification", not "tested".

### Test from the cold side

Smoke the route of someone arriving without a key, and ask of each response
not "is this correct?" but "can a human continue from here?". A correct 401
can still be a dead end: a console smoked green while the URL handed to its
user returned a bare JSON error with no way to the login page.

- A browser navigation (`Accept: text/html`) always lands on a page that
  exists; a client that does not ask for HTML keeps the API error. Never
  redirect to a route that itself 404s.
- Validate input before setting state on it.
- After the first real run of a new write path (import, feed), look at the
  screen a human opens. A new kind of row became "the latest scan" of four
  domains and the fleet screen showed 0/0.

### A reassurance needs a test

A sentence saying something is safe, limited or closed stops readers from
looking — which makes it worse than the gap. Every serious finding in one
security review had this shape: a comment promising rate limiting on a path
with no limiter; a doc pointing at the configuration where a binding silently
fell away; a docstring claiming "a caller from the API always passes one" when
no such caller existed.

- Write such a sentence only with a test that fails when it is untrue;
  otherwise write that it is *not* covered.
- Run every new test once with the fix removed. If it still passes, it guards
  nothing.
- With two implementations of one thing (an in-memory index beside the real
  one), test what goes out the door, not the model.
- A reassurance about a caller needs the caller to exist: grep before writing.

### An empty measurement is not a refutation

When a measurement shows no difference, first ask whether the case could
exist at that moment. A filter placement measured identical in production
while all vectors sat in one large dossier; two days later, with small
dossiers, one placement returned zero hits at `k=10`. Write down which case
you could and could not make; seek the extreme (smallest dossier, longest
transaction, empty list); if the case does not exist, create it temporarily.

### A threshold is not a property

A constant in code is almost always a property of the one case you looked at.
A fixed clustering cut-off of 0.45 put 78% of the first real corpus in one
group. Write the property ("no group is the whole dossier"), let the data pick
the number, and put the number in the output. Check every pair of thresholds
on small input: "at most 25%" and "at least 3 members" together allow no
group at all in a ten-document dossier.

### A baseline is not a state

Before putting "before" beside "after", check that "before" is one state. A
corpus built over months was processed by whatever code ran at the time; the
difference then measures two periods, not your change. Look for the evidence
in the data (a type absent from all old records is a code change you are
measuring), prefer a number measured within one run, or run the new code with
the old setting first: two runs, one difference.

## OpenSpec

Deltas live at `openspec/changes/<id>/specs/<capability>/spec.md`. A delta at
the change root is not read as a delta (older CLI versions dropped it
silently; 1.12 fails validation). After writing a change, run
`openspec show <id> --json --deltas-only` and confirm every capability from
the proposal appears. Some repos (skill-forge) deliberately use plain-prose
specs; follow that repo's `openspec/AGENTS.md`.

## Design and code

### Keep it simple

CRAP-style judgement: complexity times missing coverage. A flat function with
early returns over a nested switch (≤ 8 cyclomatic complexity as a rough
guide); one new column over a satellite table; no service, manager or
coordinator type until a second concrete consumer exists; unit tests written
next to the function while the design is fresh. "Configurable / pluggable"
without a second use case is dead weight. Architecture and tooling picks
follow the conventions' "boring and auditable"; lock a non-obvious choice in
a `design.md`.

### LLM features: subscription first

In personal projects, an LLM call goes through `claude -p` (subscription auth)
with a JSON-only prompt and a tolerant parser, as in skill-forge's
`ClaudeCodeProvider`. Keep a provider seam so the API-key route stays
available for SDK-only needs (forced tool use, streaming, batch, cache
tuning); use `ANTHROPIC_API_KEY` first only when asked.

## Writing

### Language

English everywhere (see `AGENTS.md`). Existing Dutch in a repo moves over in
one separate change, never gradually. When an artefact *is* Dutch — a
deliverable for a Dutch government reader — write natural Dutch: no calques
("routineus", "malicious", "quarantaineert" → "zet in quarantaine"), no
English verbs with `-eert`. Jargon without a Dutch equivalent (repo, commit,
lockfile) and English quotations stay. When correcting, fix every similar
case in the document, not just the one pointed out.

### No personal credits

No person is named as source, inspiration or credit in code, docs, README,
commit or blog unless the owner asks for it — and do not propose it. Citing a
public standard or organisation that is already the public source (an RFC,
internet.nl) is fine.
