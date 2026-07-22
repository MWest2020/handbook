#!/usr/bin/env bash
# SPDX-License-Identifier: EUPL-1.2
# Bouwt de PRIVATE handbook-build op de beheer-host. Output → site-private/
# (gitignored). NOOIT naar GitHub Pages publiceren.
#
# Vereist, en alleen aanwezig op de beheer-host:
#   - mkdocs.private.yml   (gitignored; erft mkdocs.yml, heft exclude_docs op)
#   - docs/private/        (gitignored; symlink naar openspec/private/)
#   - een read-only GH_TOKEN voor het clonen van de private repos
#
# Let op: `uv run mkdocs` hapert op de spawn in deze omgeving; draai mkdocs als
# module (`python -m mkdocs`). Vandaar de aanroep hieronder.
set -euo pipefail

cd "$(dirname "$0")/.."

# Token uit de omgeving, anders van de gh-CLI.
: "${GH_TOKEN:=$(gh auth token 2>/dev/null || true)}"
if [ -z "${GH_TOKEN:-}" ]; then
  echo "FOUT: geen GH_TOKEN (nodig voor de private repo-clones)." >&2
  exit 1
fi
export GH_TOKEN

if [ ! -f mkdocs.private.yml ]; then
  echo "FOUT: mkdocs.private.yml ontbreekt — dit hoort de beheer-host te zijn." >&2
  exit 1
fi

echo "[build-private] private build → site-private/ (niet publiceren)"
exec uv run python -m mkdocs build -f mkdocs.private.yml -d site-private "$@"
