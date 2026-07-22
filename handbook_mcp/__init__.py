# SPDX-License-Identifier: EUPL-1.2
"""handbook-mcp — read-only MCP-server op de contentlaag van het handbook.

Leest exact dezelfde importlijst als de site (inventory/repos.json op main)
en ontsluit uitsluitend docs/**/*.md van geïmporteerde repos én van de
hub zelf (expliciete uitzondering; de site importeert zichzelf niet). Stdio-server;
spokes starten hem via `uvx --from git+https://github.com/MWest2020/handbook
handbook-mcp`. Optioneel GH_TOKEN in de omgeving voor private repos —
tokens verschijnen nooit in output of foutmeldingen.
"""
import json
import os
import posixpath
import urllib.error
import urllib.request

from mcp.server.fastmcp import FastMCP

OWNER = "MWest2020"
HANDBOOK = "handbook"
RAW = "https://raw.githubusercontent.com"
API = "https://api.github.com"

mcp = FastMCP("handbook")


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(url)
    token = os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        # Token-hygiëne: alleen status + pad, nooit headers of URL-parameters.
        raise RuntimeError(f"fetch mislukt (HTTP {e.code}): {url.split('?')[0]}") from None


def _imports() -> dict[str, dict]:
    raw = _fetch(f"{RAW}/{OWNER}/{HANDBOOK}/main/inventory/repos.json")
    rows = json.loads(raw)
    return {
        r["repo"]: r
        for r in rows
        # Hub-uitzondering (mcp-hub-self-read): de vlaggen zijn site-semantiek;
        # de hub-docs zijn via MCP altijd leesbaar, de site importeert zichzelf niet.
        if r["repo"] == HANDBOOK
        or (r.get("handbook_import") == "yes" and r.get("contract_applied") == "yes")
    }


def _guard_repo(repo: str) -> dict:
    imports = _imports()
    if repo not in imports:
        raise ValueError("onbekend of niet-geïmporteerd repo")
    return imports[repo]


def _guard_path(path: str) -> str:
    norm = posixpath.normpath(path)
    if norm.startswith(("/", "..")) or "\\" in path:
        raise ValueError("pad geweigerd (buiten docs/)")
    if not norm.startswith("docs/") or not norm.endswith(".md"):
        raise ValueError("pad geweigerd: alleen docs/**/*.md")
    return norm


@mcp.tool()
def list_repos() -> list[dict]:
    """Alle geïmporteerde repos (dezelfde lijst als de handbook-site) plus
    de hub zelf, met tier, visibility, sensitivity en notes uit de inventaris."""
    velden = ("repo", "tier", "visibility", "sensitivity", "notes")
    return [{k: r.get(k) for k in velden} for r in _imports().values()]


@mcp.tool()
def list_docs(repo: str) -> list[str]:
    """Markdown-pagina's onder docs/ van een geïmporteerd repo."""
    _guard_repo(repo)
    raw = _fetch(f"{API}/repos/{OWNER}/{repo}/git/trees/main?recursive=1")
    tree = json.loads(raw)["tree"]
    return sorted(
        e["path"] for e in tree
        if e["type"] == "blob" and e["path"].startswith("docs/") and e["path"].endswith(".md")
    )


@mcp.tool()
def read_doc(repo: str, path: str) -> str:
    """Inhoud van één docs-pagina (pad relatief aan de repo-root,
    bv. 'docs/index.md')."""
    _guard_repo(repo)
    norm = _guard_path(path)
    return _fetch(f"{RAW}/{OWNER}/{repo}/main/{norm}").decode("utf-8", errors="replace")


def main() -> None:
    mcp.run()
