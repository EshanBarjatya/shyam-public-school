#!/usr/bin/env python3
"""
Build an upload-ready copy of the site in dist/ for Hostinger (or any host).

    python tools/prepare-deploy.py --domain shyampublicschool.com

What it does that a plain file copy does not:

  * Replaces every https://example.com/ placeholder with the real domain,
    in the canonical links, the Open Graph image and sitemap.xml.
  * Makes og:image an absolute URL — Facebook and WhatsApp ignore relative ones,
    so link previews would otherwise show no picture.
  * Rewrites robots.txt to allow crawling. The development copy carries
    "Disallow: /", which would keep the school out of Google entirely.
  * Writes an .htaccess with the 404 page, HTTPS redirect, compression and
    cache headers (Hostinger runs Apache/LiteSpeed, so .htaccess applies).
  * Leaves out tools/ and docs/ — internal notes that should not be public.

Nothing in the project folder is modified; everything lands in dist/.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
PLACEHOLDER = "https://example.com/"

# Everything the live site needs. tools/ and docs/ are deliberately absent.
INCLUDE_FILES = ["index.html", "about.html", "academics.html", "admissions.html",
                 "gallery.html", "contact.html", "404.html", "sitemap.xml"]
INCLUDE_DIRS = ["assets"]

HTACCESS = """# Shyam Public School — Apache / LiteSpeed configuration
# Hostinger reads this file automatically. Leave it in public_html.

# --- Friendly error page -------------------------------------------------
ErrorDocument 404 /404.html

# --- Force HTTPS ---------------------------------------------------------
# Turn this on only AFTER the SSL certificate is active in hPanel,
# otherwise the site will redirect to an address that does not work yet.
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} !=on
  RewriteCond %{HTTP:X-Forwarded-Proto} !https
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</IfModule>

# --- Compression ---------------------------------------------------------
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml \\
    application/javascript application/json image/svg+xml
</IfModule>

# --- Caching -------------------------------------------------------------
# Photographs and the stylesheet are the bulk of the page weight. A month of
# caching keeps repeat visits fast on a slow mobile connection; HTML stays
# short-lived so content edits appear straight away.
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg      "access plus 1 month"
  ExpiresByType image/png       "access plus 1 month"
  ExpiresByType image/svg+xml   "access plus 1 month"
  ExpiresByType text/css        "access plus 1 week"
  ExpiresByType application/javascript "access plus 1 week"
  ExpiresByType text/html       "access plus 10 minutes"
</IfModule>

# --- Basic hardening -----------------------------------------------------
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
Options -Indexes
"""

ROBOTS = """# Shyam Public School
User-agent: *
Allow: /

Sitemap: {base}sitemap.xml
"""


def normalise(domain: str) -> str:
    """Accept shyampublicschool.com, www...., or a full URL; return https://host/."""
    domain = domain.strip().rstrip("/")
    domain = re.sub(r"^https?://", "", domain)
    if not domain or " " in domain or "." not in domain:
        sys.exit(f"prepare-deploy: '{domain}' does not look like a domain name")
    return f"https://{domain}/"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", required=True,
                    help="the live domain, e.g. shyampublicschool.com")
    ap.add_argument("--out", default=str(DIST), help="output folder (default: dist/)")
    args = ap.parse_args()

    base = normalise(args.domain)
    out = Path(args.out)

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    replaced = 0
    for name in INCLUDE_FILES:
        src = ROOT / name
        if not src.exists():
            sys.exit(f"prepare-deploy: missing {name} — run tools/build-pages.py first")
        text = src.read_text(encoding="utf-8")
        replaced += text.count(PLACEHOLDER)
        text = text.replace(PLACEHOLDER, base)

        # og:image must be absolute or link previews show nothing.
        text = re.sub(
            r'(<meta property="og:image" content=")(?!https?://)([^"]+)(">)',
            lambda m: m.group(1) + base + m.group(2).lstrip("/") + m.group(3),
            text)

        (out / name).write_text(text, encoding="utf-8")

    for name in INCLUDE_DIRS:
        shutil.copytree(ROOT / name, out / name)

    (out / "robots.txt").write_text(ROBOTS.format(base=base), encoding="utf-8")
    (out / ".htaccess").write_text(HTACCESS, encoding="utf-8")

    # Report
    files = [p for p in out.rglob("*") if p.is_file()]
    total = sum(p.stat().st_size for p in files)
    biggest = sorted(files, key=lambda p: p.stat().st_size, reverse=True)[:5]

    print(f"Built {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} for {base}")
    print(f"  {len(files)} files, {total/1024/1024:.2f} MB total")
    print(f"  {replaced} domain placeholders replaced")
    print(f"  robots.txt now allows crawling")
    print(f"  .htaccess written (404 page, HTTPS redirect, caching)")
    print("\n  Largest files:")
    for p in biggest:
        print(f"    {p.stat().st_size/1024:7.0f} KB  {p.relative_to(out)}")

    leftover = [p.name for p in files if PLACEHOLDER in p.read_text(encoding="utf-8", errors="ignore")] \
        if any(p.suffix in {".html", ".xml", ".txt"} for p in files) else []
    if leftover:
        print(f"\n  WARNING: example.com still present in: {leftover}")
    else:
        print("\n  No example.com references remain.")


if __name__ == "__main__":
    main()
