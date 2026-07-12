#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""Freshness-check: waarschuw over pagina's met last_reviewed > 180 dagen.

Warning, geen hard fail (één eigenaar; een fail zou alleen jezelf blokkeren).
`status: deprecated` is uitgesloten. Bare output, geen ANSI (CI-script).

Gebruik: check_freshness.py [dir ...]   (default: docs)
Exit: altijd 0; het aantal verouderde pagina's staat in de output.
"""
import datetime
import pathlib
import re
import sys

MAX_AGE_DAYS = 180
FM = re.compile(r"\A---\s*\n(.*?)\n---", re.DOTALL)


def front_matter(text: str) -> dict:
    m = FM.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip("'\"")
    return out


def main() -> None:
    dirs = [pathlib.Path(d) for d in (sys.argv[1:] or ["docs"])]
    today = datetime.date.today()
    stale = missing = 0
    for d in dirs:
        for page in sorted(d.rglob("*.md")):
            fm = front_matter(page.read_text(encoding="utf-8", errors="replace"))
            if fm.get("status") == "deprecated":
                continue
            raw = fm.get("last_reviewed", "")
            try:
                reviewed = datetime.date.fromisoformat(raw)
            except ValueError:
                print(f"WAARSCHUWING {page}: geen geldige last_reviewed ({raw!r})")
                missing += 1
                continue
            age = (today - reviewed).days
            if age > MAX_AGE_DAYS:
                print(f"WAARSCHUWING {page}: {age} dagen niet gereviewd")
                stale += 1
    print(f"freshness: {stale} verouderd, {missing} zonder geldige datum "
          f"(grens {MAX_AGE_DAYS} dagen)")


if __name__ == "__main__":
    main()
