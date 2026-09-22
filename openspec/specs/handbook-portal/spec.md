# handbook-portal Specification

## Purpose
The public hub build leaks no private or financial context: hub-owned pages
*and* non-rendered repo files stay free of funding programmes, private repo
names and homelab details.
## Requirements
### Requirement: Hub-owned pages leak no private or financial context

Hub-owned pages in the public build (index, conventions, the homelab pointer)
SHALL contain none of the three categories below.

1. subsidy or funding programmes — whichever programme, fund or application
   track; not as a label on a repo, and not in running text;
2. names of `private-only` repos, or an enumeration of what the private build
   aggregates;
3. homelab or infrastructure details, including meta-information about what has
   been redacted and since when.

Mention of the private section SHALL be limited to the bare fact that it exists
(one pointer sentence), without a table of contents. Descriptions of public
repos SHALL be limited to what the repo already documents publicly itself. This
is necessary because the repo split (fail closed) covers imports only;
hub-owned pages share their source between the public and private build and
fall outside it.

#### Scenario: A funding programme on the public index

- WHEN a hub-owned page in the public build identifies a repo by its subsidy or
  funding programme
- THEN that is refused at review and removed before deploy

#### Scenario: Private repos enumerated on the public index

- WHEN a hub-owned page in the public build names `private-only` repos or
  describes the content of the private section
- THEN the passage is reduced to at most one pointer sentence without repo
  names, or moved to a page navigated only in `mkdocs.private.yml`

### Requirement: Repo files of the public hub leak no private or financial context

The prohibition above SHALL apply equally to non-rendered files in the public
hub repo (inventory notes, configs, seeds, archived changes): the repo itself
is public, so everything in it is publication — not only what mkdocs renders.

#### Scenario: A funding programme in the inventory notes

- WHEN a `notes` field in `inventory/repos.json` or `repos.md` ties a repo to a
  subsidy or funding programme
- THEN that link moves to a private overlay (gitignored, or outside this repo)
  and only the functional information remains in the public inventory
