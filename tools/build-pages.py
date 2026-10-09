#!/usr/bin/env python3
"""
Assemble the interior pages of the Shyam Public School site.

index.html is the source of truth for the shared chrome (head, header, nav,
footer, mobile action bar). This script lifts that chrome, drops in each page
body from tools/bodies/, and writes the finished static HTML to the project
root.

Run it after editing index.html's header/footer, or after editing any body:

    python tools/build-pages.py

The output files are ordinary static HTML — the site does not need this script
to run, only to be rebuilt consistently.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BODIES = ROOT / "tools" / "bodies"

PAGES = {
    "about.html": {
        "title": "About Shyam Public School — Nagal Rajawatn, Dausa",
        "desc": "Who we are, what we hold to, and the school information parents ask for. "
                "Shyam Public School, Nagal Rajawatn, Dausa, Rajasthan.",
        "og_title": "About Shyam Public School",
        "og_desc": "A school built for Nagal Rajawatn, by people from it.",
        "og_image": "assets/img/photos/campus-side-elevation.jpg",
    },
    "academics.html": {
        "title": "Academics — Shyam Public School, Nagal Rajawatn, Dausa",
        "desc": "Pre-primary to senior classes at Shyam Public School: subjects, how we teach, "
                "activities beyond the classroom, and how progress is reported to parents.",
        "og_title": "Academics at Shyam Public School",
        "og_desc": "Taught carefully, revised often, finished on time.",
        "og_image": "assets/img/photos/campus-front-wide.jpg",
    },
    "admissions.html": {
        "title": "Admissions — Shyam Public School, Nagal Rajawatn, Dausa",
        "desc": "How to take admission at Shyam Public School, Nagal Rajawatn, Dausa: the four "
                "steps, documents needed, age criteria, questions parents ask, and the enquiry form.",
        "og_title": "Admissions — Shyam Public School",
        "og_desc": "A seat for your child, without the runaround. Enquiries welcome.",
        "og_image": "assets/img/photos/campus-entrance-portico.jpg",
    },
    "gallery.html": {
        "title": "Gallery — Shyam Public School, Nagal Rajawatn, Dausa",
        "desc": "Photographs of the Shyam Public School campus at Nagal Rajawatn, Dausa, "
                "supplied by the school.",
        "og_title": "Gallery — Shyam Public School",
        "og_desc": "The school, as it actually looks.",
        "og_image": "assets/img/photos/campus-front-wide.jpg",
    },
    "contact.html": {
        "title": "Contact Shyam Public School — Nagal Rajawatn, Dausa – 303505",
        "desc": "Phone, WhatsApp, email and directions for Shyam Public School, Nagal Rajawatn, "
                "Dausa, Rajasthan – 303505. Speak to Rakesh Sharma.",
        "og_title": "Contact Shyam Public School",
        "og_desc": "Call, message, or simply come by. Nagal Rajawatn, Dausa – 303505.",
        "og_image": "assets/img/photos/campus-entrance-portico.jpg",
    },
    "404.html": {
        "title": "Page not found — Shyam Public School",
        "desc": "That page is not here. Links back to admissions, academics and contact.",
        "og_title": "Page not found — Shyam Public School",
        "og_desc": "That page is not here.",
        "og_image": "assets/img/photos/campus-front-wide.jpg",
    },
}

OPEN_MAIN = '<main id="main">'
CLOSE_MAIN = "</main>"


def sub_once(pattern, repl, text, label):
    """Replace exactly one match, or fail loudly — silent no-ops hide breakage."""
    new, count = re.subn(pattern, lambda _m: repl, text, count=1, flags=re.S)
    if count != 1:
        sys.exit(f"build-pages: expected one match for {label}, found {count}")
    return new


def main():
    index = (ROOT / "index.html").read_text(encoding="utf-8")

    start = index.index(OPEN_MAIN) + len(OPEN_MAIN)
    end = index.rindex(CLOSE_MAIN)
    head = index[:start]
    tail = index[end:]

    for filename, meta in PAGES.items():
        body_file = BODIES / filename
        if not body_file.exists():
            sys.exit(f"build-pages: missing body file {body_file}")
        body = body_file.read_text(encoding="utf-8").rstrip()

        page_head = head

        page_head = sub_once(r"<title>.*?</title>",
                             f"<title>{meta['title']}</title>",
                             page_head, "<title>")
        page_head = sub_once(r'<meta name="description" content=".*?">',
                             f'<meta name="description" content="{meta["desc"]}">',
                             page_head, "meta description")
        page_head = sub_once(r'<meta property="og:title" content=".*?">',
                             f'<meta property="og:title" content="{meta["og_title"]}">',
                             page_head, "og:title")
        page_head = sub_once(r'<meta property="og:description" content=".*?">',
                             f'<meta property="og:description" content="{meta["og_desc"]}">',
                             page_head, "og:description")
        page_head = sub_once(r'<meta property="og:image" content=".*?">',
                             f'<meta property="og:image" content="{meta["og_image"]}">',
                             page_head, "og:image")
        page_head = sub_once(r'<link rel="canonical" href=".*?">',
                             f'<link rel="canonical" href="https://example.com/{filename}">',
                             page_head, "canonical")

        # Only the home page carries the School structured data block.
        page_head = re.sub(
            r'<!-- Structured data.*?</script>\n', "", page_head, count=1, flags=re.S)

        # Move the nav's current-page marker.
        page_head = page_head.replace(' aria-current="page"', "")
        if filename != "404.html":
            page_head = sub_once(rf'<li><a href="{re.escape(filename)}">',
                                 f'<li><a href="{filename}" aria-current="page">',
                                 page_head, f"nav link for {filename}")

        out = f"{page_head}\n\n{body}\n\n{tail}"
        (ROOT / filename).write_text(out, encoding="utf-8")
        print(f"built {filename}  ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
