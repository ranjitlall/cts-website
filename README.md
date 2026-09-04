# Centre for Technology and Society — website

Static site built with [Eleventy](https://www.11ty.dev/), edited through
[Sveltia CMS](https://sveltiacms.app/), hosted free on GitHub Pages.

**Live at:** <https://ranjitlall.github.io/cts-website/>
**Repository:** `ranjitlall/cts-website` (public)

Running cost: nothing. Everything is on free tiers. An `ox.ac.uk` hostname, if
granted, is added later without rebuilding anything — see LAUNCH.md.

---

## For collaborators: how to edit the site

Go to **`https://ranjitlall.github.io/cts-website/admin/`**.

| Section | What it controls |
|---|---|
| **People** | The team grid on the homepage |

News and Events are built but parked. `src/admin/config.yml` explains how to
switch them back on when there's enough happening to justify them.

Fill in the form, click **Save**. The site rebuilds and your change is live in
about a minute. You never touch HTML, and you can't break the layout — the
fields are the only things that change. Every save is recorded, so any edit can
be undone.

**Signing in.** The one-click *Sign in with GitHub* button needs an
authenticator Worker that isn't deployed yet, so for now sign in with **Sign in
with Token** using a GitHub personal access token. To open it up to
colleagues, follow "Adding one-click sign-in" below.

---

## Deployment

Every push to `main` triggers `.github/workflows/deploy.yml`, which builds the
site and publishes it to GitHub Pages. Nothing else needs doing.

The build passes `--pathprefix="/cts-website/"` so that links resolve under the
repository subpath. Every internal link in the templates runs through Eleventy's
`url` filter, so the same source works unchanged at a domain root later.

Repository → **Settings** → **Pages** is set to **Source: GitHub Actions**.

## Working locally

```bash
npm install
npm run serve     # http://localhost:8080, live reload
npm run build     # writes to _site/
```

`npm run serve` builds without the `/cts-website/` prefix, which is what you
want locally.

## Where things live

```
src/
  index.njk                        Homepage — all the one-page sections
  working-papers.njk               Working Paper Series listing
  sanjaya-lall-professorship.njk   Visiting Professorship page
  privacy.md                       Privacy notice
  accessibility.md                 Accessibility statement
  sitemap.njk                      Generates /sitemap.xml
  robots.txt
  _includes/layouts/               Page templates
  _data/
    site.json                      Site name, URL, address, contact email
    papers.json                    Working Paper Series entries
    outputs.json                   News & commentary items
    holders.json                   Visiting Professorship holders
    lallevents.json                Professorship events archive, by year
  content/
    people/                        One Markdown file per person
  assets/
    css/style.css                  All styling; design tokens at the top
    img/                           Logos, portraits, posters, uploads/
    papers/                        Working paper PDFs
  admin/
    index.html                     Loads the CMS
    config.yml                     Defines the editing forms
tools/
  make_cover.py                    Generates the branded WP cover page
  fonts/                           Bundled fonts for the cover
```

There is no `src/CNAME` while the site is on `github.io`. When a custom domain
is granted, recreate it — LAUNCH.md, section 6, has the steps.

---

## Adding one-click sign-in for collaborators

This removes the need for anyone to generate a token.

1. Deploy the authenticator:
   <https://github.com/sveltia/sveltia-cms-auth> — it has a one-click
   "Deploy to Cloudflare Workers" button. Note the resulting Worker URL.
2. On GitHub: **Settings → Developer settings → OAuth Apps → New OAuth App**
   - Homepage URL: your Worker URL
   - Authorization callback URL: `<your-worker-url>/callback`
   - Generate a client secret.
3. In the Cloudflare Worker's **Settings → Variables**, add:
   - `GITHUB_CLIENT_ID`
   - `GITHUB_CLIENT_SECRET` (as a secret)
   - `ALLOWED_DOMAINS` — set to `ranjitlall.github.io` so nobody else's site can
     use your authenticator.
4. In `src/admin/config.yml`, uncomment and set:
   ```yaml
   base_url: https://sveltia-cms-auth.YOUR-SUBDOMAIN.workers.dev
   ```
5. Repository → **Settings → Collaborators → Add people**, with **Write**
   access. They then log in at `/admin/` with their GitHub account.

## Alternative host: Cloudflare Pages

Not in use, but the site builds there unchanged, and Cloudflare serves private
repositories on the free tier if the repo ever needs to stop being public.
Connect the repository under **Workers & Pages → Create → Pages**, with build
command `npm run build` and output directory `_site`, and drop the
`--pathprefix` from the build if serving at a domain root.

---

## Still to do

**Permissions and sign-off**

- [ ] Confirm reproduction rights for the event posters (2013, 2014, 2018,
      2023, 2024) and the twelve holder portraits before wide publicity, and
      record any required photographer credit in the `credit` field in
      `src/_data/holders.json` (it renders under each card).
- [ ] Confirm reproduction rights for the Sanjaya Lall portrait.
- [ ] Confirm rights to reproduce the twelve book-cover images on the Sanjaya
      Lall page (`src/assets/img/books/`) — publishers usually permit covers in
      this biographical/review context, but it has not been confirmed.
- [ ] Have the privacy notice checked by the University's Information
      Compliance Team. The accessibility statement is a self-assessment, not an
      independent audit.
- [ ] Confirm with AIGI how the Centre should be described and credited, and
      that using the AIGI logo in the top strip is approved.

**Branding**

- [ ] Ask the Oxford Martin School and AIGI for approved reversed (white)
      versions of their logos. Both marks are navy-on-white, so each currently
      sits in a white tile on the navy strip. Do not recolour their artwork
      without their approved variant.
- [ ] Replace `src/assets/img/logo-aigi.jpeg` with a vector or
      transparent-PNG version if AIGI can supply one.
- [ ] The Martin School may want programmes branded "Oxford Martin …", which
      would affect the logo and the working paper covers.

**Content**

- [ ] Verify the Sanjaya Lall events archive (`src/_data/lallevents.json`) —
      dates and details were compiled from the Department of Economics website,
      Oxford Podcasts, event posters, and Wikipedia.
- [ ] Resolve the Stiglitz year. `holders.json` records him as the 2022 holder
      while `lallevents.json` places his lectures in 2023 alongside Raj Chetty,
      so the two currently disagree. Sources conflict; the poster evidence
      points to 2023. 2022 has no events entry either way.
- [ ] The 2014 Krugman podcast link points to a keyword listing rather than the
      episode page.
- [ ] Confirm Tom Robinson's CTS position — currently listed as Faculty
      Affiliate, chosen to match the harmonised set.
- [ ] Jean-Paul Carvalho was removed from the People section in August 2026.
      His portrait remains at `src/assets/img/people/jean-paul-carvalho.jpg`
      in case he is reinstated; delete it if not.
- [ ] Add portrait photos for anyone still missing one (square images work
      best; they render as circles).

**Domain**

- [ ] `cts.aigi.ox.ac.uk` — needs backing from AIGI or the Oxford Martin School,
      then a request to `domains@it.ox.ac.uk` including an exception for hosting
      outside the University network. LAUNCH.md has the wording.

---

## Working Paper Series

### Adding a paper

1. Generate the branded cover and merge it onto the paper:
   ```bash
   cd tools
   cp wp-2026-01.json wp-2026-03.json     # edit: number, title, authors, date, abstract
   python3 make_cover.py --config wp-2026-03.json \
                         --paper ~/Downloads/my-paper.pdf \
                         --out ../src/assets/papers/CTS-WP-2026-03.pdf
   ```
   Omit `--paper` to produce the cover on its own.
   Requires `pip install reportlab pypdf`.

2. Add an entry to `src/_data/papers.json`, setting `pdf` to
   `/assets/papers/CTS-WP-2026-03.pdf`.

3. Commit. The paper appears on `/working-papers/` and the newest one is
   featured in the Research section of the homepage.

### Numbering

`WP YYYY-NN` — year, then sequence within that year. WP 2026-01 is the first.

### A note on file size

PDFs live in the Git repository. A 90-page text PDF is typically 2–8 MB, which
is fine. GitHub warns above 50 MB per file. If a paper exceeds that — usually
because of high-resolution figures — either compress it:
```bash
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=small.pdf big.pdf
```
or leave `pdf` blank in papers.json and rely on the `preprint` link instead.
