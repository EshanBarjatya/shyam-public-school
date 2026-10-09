# Shyam Public School — website

A mobile-first website for Shyam Public School, Nagal Rajawatn, Dausa,
Rajasthan – 303505. Built to do one job well: give a parent enough confidence
to pick up the phone.

Plain static HTML, CSS and JavaScript. No framework, no dependencies, nothing
to install on the host.

> Before publishing, see [`docs/launch-checklist.md`](docs/launch-checklist.md).
> The contact details still need confirming by the school, and twenty facts are
> waiting to be filled in — none of which are claimed on the pages meanwhile.

---

## Running it

Open `index.html` in a browser, or serve the folder:

```bash
python -m http.server 8000
# http://localhost:8000
```

## Structure

```
index.html              Home — the main admissions funnel
about.html              Story, values, people, school information
academics.html          Stages, subjects, teaching approach, reporting
admissions.html         Process, documents, fees, FAQ, enquiry form
gallery.html            The campus photographs
contact.html            Phone, WhatsApp, email, map, message form
404.html

assets/css/styles.css   The whole design system, in numbered sections
assets/js/main.js       Nav, scroll reveal, FAQ, lightbox, form handling
assets/img/photos/      The school's own photographs — see CREDITS.md
assets/img/brand/       Temporary favicon
assets/img/illustrations/ Clearly labelled editorial artwork — see CREDITS.md

tools/build-pages.py    Assembles interior pages from index.html's chrome
tools/bodies/           Per-page content — the only place to edit page copy
tools/make-checklist.py Regenerates docs/content-checklist.md
tools/prepare-deploy.py Builds dist/ for upload — sets the real domain

docs/launch-checklist.md   What must happen before launch
docs/content-checklist.md  Every unconfirmed fact, auto-generated
docs/hosting-hostinger.md  Step-by-step deploy to Hostinger
```

## Editing

**Shared head, header, navigation and footer** live in `index.html` and are
copied into the other pages by the build script. Edit them there, then:

```bash
python tools/build-pages.py
```

**Page content** lives in `tools/bodies/<page>.html`. Editing a built page like
`about.html` directly works until the next rebuild overwrites it.

**Home page content** is edited in `index.html` itself.

## Design

| | |
|---|---|
| Ground | warm white `#FCFAF6`, cream `#F6F1E8` |
| Type | deep navy `#0E1B33`, body ink `#2E3A52` |
| Accents | maroon `#7A2233`, gold `#B38A42` |
| Fonts | Source Serif 4 for display, Inter for text and UI |

The identity comes from the building itself: the pediment above the school's
entrance is redrawn as a small rule that heads the major sections, and
photographs sit in arch-topped frames that echo the portico. Beyond that the
page is kept quiet — hairline borders rather than heavy shadows, one accent at
a time, and generous space.

Mobile first. Below 1024px a Call / WhatsApp / Enquire bar slides up on scroll,
because most parents will arrive on a phone and the phone is the conversion.

Accessibility: skip link, visible focus rings, labelled fields with inline
errors, keyboard-operable accordion and lightbox, `prefers-reduced-motion`
honoured, alt text on every image.

## Editorial rules this site follows

Deliberate, and worth keeping:

1. **Nothing unverified is asserted.** Where a fact is missing the sentence is
   written so it reads correctly without it, and an HTML `CONFIRM` comment marks
   the spot. No placeholder text reaches the reader.
2. **No invented photographs.** The five exterior shots are the school's own.
   Generated artwork is clearly labelled “Editorial illustration” and is never
   presented as this campus, its staff, students or families.
3. **Captions match content.** A picture of the building is never captioned as a
   classroom, a library or an activity.
4. **No invented testimonials.** There is no parent-quotes section, because
   there are no real parent quotes yet.
5. **Logo status stays clear.** The architecture-and-book crest is an original
   website identity concept, not a claim of an officially registered school mark.
   Replace it if the school supplies an official crest.
