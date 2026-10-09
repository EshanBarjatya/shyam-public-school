# Putting the site live on Hostinger

This is a plain static site — HTML, CSS, JavaScript and images. No database, no
PHP, no build tools on the server. Hostinger's cheapest shared plan runs it
comfortably, and the whole upload is about **1.7 MB**.

---

## Before you upload

### 1. Build the deploy folder

Do not upload the project folder as it stands. Three things in it are
development settings, and one of them would hide the school from Google.

```bash
python tools/build-pages.py
python tools/prepare-deploy.py --domain yourdomain.com
```

That creates `dist/`, which is what you upload. It:

- replaces every `https://example.com/` placeholder with your real domain
- makes the social-preview image an absolute URL, so WhatsApp and Facebook
  previews show the school building
- **rewrites `robots.txt` to allow crawling** — the development copy says
  `Disallow: /`, which tells Google to ignore the entire site
- writes an `.htaccess` for the 404 page, HTTPS, compression and caching
- leaves out `tools/` and `docs/`, which are internal and should not be public

Re-run both commands any time you change the site.

### 2. Settle the content first

Twenty facts are still unconfirmed — see `docs/content-checklist.md` — and the
phone number and email came from a screenshot that the school has not verified.
None of it is wrong on the page today, because nothing unverified is claimed.
But a live site that says "call us for the fee structure" needs someone
actually answering that number.

---

## Uploading

### Option A — File Manager (easiest, no extra software)

1. Zip the **contents** of `dist/`, not the folder itself. You should be able
   to see `index.html` at the top level when you open the zip.
2. hPanel → **Files** → **File Manager**.
3. Open **`public_html`**. Delete whatever is already there — Hostinger puts a
   `default.php` or placeholder `index.html` in new accounts, and it will take
   priority over yours.
4. Upload the zip, then right-click it → **Extract**.
5. Delete the zip afterwards.
6. Turn on **Settings → Show hidden files** so you can confirm `.htaccess`
   arrived. Files starting with a dot are hidden by default and it is easy to
   miss that it did not upload.

### Option B — FTP (better if you will update often)

1. hPanel → **Files** → **FTP Accounts**. Note the host, username and port.
2. Connect with FileZilla.
3. Upload everything inside `dist/` into `public_html`.

### Option C — Git

hPanel → **Advanced** → **GIT**, if you put the project on GitHub later. You
would need to commit the `dist/` output, or build on your machine and push only
that. Not worth it for a site this size unless you are updating weekly.

---

## After uploading

### 1. Turn on SSL — do this before anything else

hPanel → **Security** → **SSL** → install the free Let's Encrypt certificate.
It usually takes a few minutes.

**The `.htaccess` forces HTTPS.** If you upload it before the certificate is
active, the site will redirect visitors to an address that does not work yet.
If that happens, open `.htaccess` in File Manager and comment out the
`RewriteRule` line until the certificate is ready.

Once SSL is active, also switch on **Force HTTPS** in hPanel if it is offered.

### 2. Check it actually works

On a phone, not just a desktop browser:

- [ ] Home page loads and the photographs appear
- [ ] The menu button opens and closes
- [ ] **Call** and **WhatsApp** in the bottom bar open the right apps
- [ ] The enquiry form opens WhatsApp with the details filled in
- [ ] Visit `yourdomain.com/no-such-page` — you should get the styled 404,
      not Hostinger's default error page. If you get Hostinger's, `.htaccess`
      did not upload.
- [ ] Footer links to **Fees & documents** and **Common questions** land on the
      right section

### 3. Get it found

This matters more than the website for a village school:

1. **Google Business Profile** — create a listing for Shyam Public School at
   Nagal Rajawatn. A parent searching "school near Nagal Rajawatn" finds the
   map listing long before they find a website. It is free, and it also gives
   you the exact map pin to drop into `contact.html`.
2. **Google Search Console** — add the domain, verify it, submit
   `https://yourdomain.com/sitemap.xml`.
3. Put the web address on the school gate board, the uniform circular and any
   WhatsApp broadcast.

---

## The enquiry form

Right now a submitted form opens WhatsApp with everything filled in, with a
pre-filled email as a fallback. That works and needs no server — but if the
parent closes WhatsApp before sending, the enquiry is lost and you never know
it happened.

Hostinger runs PHP, so there are two ways to capture every enquiry:

- **A small PHP handler** on the host that emails the school and logs each
  submission. Free, but mail sent from shared hosting often lands in spam
  unless it goes out through a proper mailbox — use a Hostinger email account
  with SMTP rather than bare `mail()`.
- **A form service** such as Formspree or Web3Forms. Free tiers cover a school's
  volume, nothing to maintain, and the submissions sit in a dashboard.

Keep the WhatsApp button either way. In this area it converts better than
email, and parents reply on it.

---

## Things that will catch you out

| Symptom | Cause |
|---|---|
| Site not on Google after weeks | `robots.txt` with `Disallow: /` — you uploaded the project folder instead of `dist/` |
| Hostinger's error page instead of yours | `.htaccess` missing; it is hidden in File Manager by default |
| "Too many redirects" | HTTPS forced before the SSL certificate was active |
| Old version still showing | Browser cache. Hard-refresh, or check you uploaded into `public_html` and not a subfolder |
| WhatsApp link preview has no image | `og:image` left relative — `prepare-deploy.py` fixes this, so you skipped it |
| Default Hostinger page still loads | Their placeholder `index.html` or `default.php` is still in `public_html` |

---

## Updating later

```bash
# edit tools/bodies/<page>.html, or index.html for the home page
python tools/build-pages.py
python tools/prepare-deploy.py --domain yourdomain.com
# upload the changed files from dist/ over the old ones
```

For a one-line text change you can also edit the file directly in Hostinger's
File Manager — but then make the same edit in the project folder, or the next
deploy will overwrite it.
