# Launch checklist — Shyam Public School website

The site is presentable as it stands: nothing on the public pages is unverified,
and there is no development scaffolding on screen. What remains is to confirm
the facts the school has not yet supplied, and to wire up the plumbing.

---

## 1. Must be done before the site is public

### 1.1 Confirm the contact details
The phone number, email address and contact person were taken from a supplied
contact screenshot and have **not** been confirmed by the school. They appear on
every page, in the mobile action bar, in the WhatsApp links and in the
structured data.

- [ ] Phone — `+91 89520 21550` — confirmed by the school
- [ ] Email — `sharma.rakesh3488@gmail.com` — confirmed, and someone checks it
- [ ] Contact person — `Rakesh Sharma` — confirmed, with the correct designation
- [ ] WhatsApp actually answers on that number (test it yourself)

To change them, search and replace across the project:

| Find | Appears in |
|---|---|
| `918952021550` | `tel:` and `wa.me` links |
| `+91 89520 21550` | visible text |
| `sharma.rakesh3488@gmail.com` | `mailto:` links, JS, structured data |
| `Rakesh Sharma` | header, footer, about, admissions, contact |

The number is also set in the `SCHOOL` object at the top of
`assets/js/main.js` — update it there too.

### 1.2 Fill in the facts the school confirms
Twenty facts are still open. **None of them are asserted anywhere on the public
pages** — the copy is written so that it reads correctly without them, and each
is marked by an HTML comment at the point where it belongs.

- [ ] Work through `docs/content-checklist.md`
- [ ] Add each confirmed fact to the page and delete its `CONFIRM` comment
- [ ] Re-run `python tools/make-checklist.py`

The important ones, in order of how much a parent cares:

1. **Classes offered** and the highest class the school runs
2. **Fees** — admission, tuition, transport, books and uniform
3. **School timings**, summer and winter
4. **Transport routes**, if any
5. **Medium of instruction**
6. **Examination board or affiliation** — and the recognition number if the
   school wishes to publish it

On the last point: do not put an affiliation claim on the site until someone
has checked the paperwork. It is the one mistake a school website cannot afford.

### 1.3 Decide on the logo
The current mark is a **temporary typographic lockup** — the letters "SPS" in a
maroon tile beside the school's name set in type. It is deliberately not a crest.

- [ ] Either supply the official logo — replace it in the `.wordmark` block in
      `index.html` and in `assets/img/brand/favicon.svg` — or
- [ ] Approve the wordmark as the permanent mark

### 1.4 Connect the enquiry form
A submitted form currently opens WhatsApp with the details filled in, and offers
a pre-filled email as a fallback. That works, but nothing is recorded if the
parent closes the WhatsApp screen.

- [ ] Point the form at an endpoint (Formspree, Web3Forms, Google Forms, or a
      small script on the host)
- [ ] Keep the WhatsApp route as well — locally it converts better than email
- [ ] Test an end-to-end submission and confirm the enquiry arrives

The handler is `initForms()` in `assets/js/main.js`.

### 1.5 Photographs
The five campus exterior photographs are the school's own and are in use.

- [ ] Collect the interior and activity photographs listed under *gallery.html*
      in `docs/content-checklist.md`
- [ ] Get **written parental consent** before publishing any photograph that
      shows a child
- [ ] Add each new photograph to `gallery.html` with a caption that matches what
      it actually shows

Never substitute a stock or computer-generated image for a campus facility, a
classroom or a student. Where there is no real photograph, the site shows no
photograph — that is deliberate, and it is why the pages still look finished.

### 1.6 Replace the domain placeholders
- [ ] `robots.txt` — delete `Disallow: /` and set the real sitemap URL
- [ ] `sitemap.xml` — replace `https://example.com/`
- [ ] Each page's `<link rel="canonical">`, and make `og:image` an absolute URL

---

## 2. Worth doing at launch

- [ ] Create a **Google Business Profile** for the school. For a local school
      this brings more enquiries than the website does, and it fixes the map pin
- [ ] Replace the village-centred map on `contact.html` with the exact pin
- [ ] Compress the five JPEGs — they are 120–250 KB each and around 60 KB is
      achievable; add WebP versions if the host supports it
- [ ] Point the host's 404 route at `404.html`
- [ ] Add analytics if the school wants enquiry numbers

## 3. Later

- [ ] A Hindi version, or at least a Hindi admissions page
- [ ] Downloadable admission form (PDF)
- [ ] Notices page for parents
- [ ] Real parent testimonials, collected with written permission. There is no
      testimonials section on the site today precisely because there is nothing
      genuine to put in it

---

## Rebuilding

Interior pages are assembled from `index.html`'s head, header and footer, plus
the page bodies in `tools/bodies/`:

```
python tools/build-pages.py      # about / academics / admissions / gallery / contact / 404
python tools/make-checklist.py   # refresh docs/content-checklist.md
```

Edit shared chrome in `index.html` only, then rebuild — otherwise the pages
drift apart. Page content is edited in `tools/bodies/<page>.html`.
