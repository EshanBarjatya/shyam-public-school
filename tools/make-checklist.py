#!/usr/bin/env python3
"""
Generate docs/content-checklist.md from the CONFIRM comments in the HTML.

Nothing unverified is asserted on the public pages. Where a fact is missing,
the copy is written so that it reads correctly without it, and an HTML comment
marks the spot:

    <!-- CONFIRM: the highest class the school runs -->

This script collects those comments so the school can work through them in one
list, and so nobody has to grep the markup to find out what is still open.

    python tools/make-checklist.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "about.html", "academics.html",
         "admissions.html", "gallery.html", "contact.html"]

MARKER = re.compile(r"<!--\s*(CONFIRM(?:\s*/\s*STILL TO COME)?\s*[:.].*?)-->", re.S | re.I)


def parse(block):
    """Return (headline, [bullets]) for one CONFIRM comment."""
    body = re.sub(r"^CONFIRM(\s*/\s*STILL TO COME)?\s*[:.]\s*", "",
                  block.strip(), flags=re.I)
    raw = [ln.strip() for ln in body.splitlines() if ln.strip()]

    bullets = []
    prose = []
    for line in raw:
        if line.startswith("·"):
            bullets += [p.strip() for p in line.split("·") if p.strip()]
        else:
            prose.append(line)

    headline = re.sub(r"\s+", " ", " ".join(prose)).strip()
    return headline or "See the comment in the markup", bullets


def main():
    lines = [
        "# Content still to be confirmed",
        "",
        "Auto-generated from the `CONFIRM` comments in the HTML — regenerate with",
        "`python tools/make-checklist.py` after any content change.",
        "",
        "**None of these facts are stated anywhere on the public pages.** The copy is",
        "written so that it reads correctly without them, and each one is marked with",
        "an HTML comment at the point where it belongs. As the school confirms a fact,",
        "add it to the page and delete the comment.",
        "",
    ]

    total = 0
    for name in PAGES:
        source = (ROOT / name).read_text(encoding="utf-8")
        hits = MARKER.findall(source)
        if not hits:
            continue

        lines.append(f"## {name} — {len(hits)} item{'s' if len(hits) != 1 else ''}")
        lines.append("")
        for hit in hits:
            headline, bullets = parse(hit)
            lines.append(f"- [ ] {headline}")
            for bullet in bullets:
                lines.append(f"  - [ ] {bullet}")
            total += 1
        lines.append("")

    lines += [
        "---",
        "",
        f"**Total open items: {total}**",
        "",
        "## Also required before launch",
        "",
        "- [ ] Confirm the phone number, email address and contact person taken from",
        "      the supplied screenshot. They appear on every page, in the WhatsApp",
        "      links, in `assets/js/main.js` and in the structured data.",
        "- [ ] Supply the official school logo, or approve the temporary text wordmark.",
        "- [ ] Supply interior and activity photographs for the gallery.",
        "- [ ] Collect written parental consent for any photograph showing a child.",
        "- [ ] Connect a form endpoint so abandoned enquiries are still captured.",
        "",
    ]

    out = ROOT / "docs" / "content-checklist.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote docs/content-checklist.md - {total} open items")


if __name__ == "__main__":
    main()
