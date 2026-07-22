#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Sessietest voor handbook-mcp: echte server over stdio, alle tools plus
de weiger-paden uit de spec-delta. Exit 1 bij elke afwijking. Bare output.

Gebruik: uv run python scripts/test_mcp.py
"""
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def die(msg: str) -> None:
    print(f"FOUT: {msg}")
    sys.exit(1)


async def main() -> None:
    params = StdioServerParameters(
        command=sys.executable, args=["-c", "import handbook_mcp; handbook_mcp.main()"]
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            names = sorted(t.name for t in tools.tools)
            if names != ["list_docs", "list_repos", "read_doc"]:
                die(f"onverwachte toolset: {names}")
            print(f"tools: {names}")

            import json

            def items(result):
                # FastMCP levert een lijst als één content-item per element
                out = []
                for c in result.content:
                    try:
                        out.append(json.loads(c.text))
                    except (ValueError, TypeError):
                        out.append(c.text)
                return out

            r = await session.call_tool("list_repos", {})
            if r.isError:
                die("list_repos faalde")
            repo_names = {x["repo"] for x in items(r)}
            if "Wanderer" not in repo_names or "handbook" not in repo_names:
                die(f"importlijst klopt niet: {sorted(repo_names)}")
            print(f"list_repos: {len(repo_names)} repos (incl. hub)")

            r = await session.call_tool("read_doc", {"repo": "handbook", "path": "docs/index.md"})
            if r.isError or "status:" not in r.content[0].text:
                die("read_doc(handbook, docs/index.md) leverde geen front matter (hub-exceptie)")
            print("read_doc(handbook): hub-docs leesbaar (ok)")

            r = await session.call_tool("list_docs", {"repo": "Wanderer"})
            docs = items(r)
            if r.isError or "docs/index.md" not in docs:
                die("list_docs(Wanderer) mist docs/index.md")
            print(f"list_docs(Wanderer): {len(docs)} pagina's")

            r = await session.call_tool("read_doc", {"repo": "Wanderer", "path": "docs/index.md"})
            if r.isError or "status:" not in r.content[0].text:
                die("read_doc(Wanderer, docs/index.md) leverde geen front matter")
            print("read_doc: front matter aanwezig")

            r = await session.call_tool("read_doc", {"repo": "Wanderer", "path": "docs/../.mcp.json"})
            if not r.isError:
                die("pad-traversal werd NIET geweigerd")
            if "token" in r.content[0].text.lower().replace("token-hygi", ""):
                die("foutmelding lekt mogelijk token-context")
            print("read_doc traversal: geweigerd (ok)")

            r = await session.call_tool("list_docs", {"repo": "grapher"})
            if not r.isError:
                die("niet-geïmporteerd repo werd NIET geweigerd")
            print("list_docs(grapher): geweigerd (ok)")

    print("sessietest: alle checks geslaagd")


if __name__ == "__main__":
    asyncio.run(main())
