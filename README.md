# Centre for Technology and Society — website

Static site built with [Eleventy](https://www.11ty.dev/), edited through
[Sveltia CMS](https://sveltiacms.app/), hosted free on Cloudflare Pages.

Running cost: the domain only (~£10/year). Everything else is on free tiers.

---

## For collaborators: how to edit the site

Go to **`https://techandsociety.org/admin`** and click *Sign in with GitHub*.

You'll see three sections in the sidebar:

| Section | What it controls |
|---|---|
| **People** | The team grid on the homepage |

News and Events are built but parked. `src/admin/config.yml` explains how to
switch them back on when there's enough happening to justify them.

Fill in the form, click **Save**. The site rebuilds and your change is live in
about a minute. You never touch HTML, and you can't break the layout — the
fields are the only things that change.

Every save is recorded, so any edit can be undone.

---

## Setup

**To go live now on GitHub Pages, follow LAUNCH.md instead** — no domain
purchase, no waiting. The Cloudflare instructions below remain valid if you
prefer that route or want a private repository.

## Setup on Cloudflare Pages (one time, ~45 minutes)

### 1. Put this repository on GitHub

```bash
git init
git add .
git commit -m "Initial site"
gh repo create cts-website --private --source=. --push
```

### 2. Buy the domain

[Cloudflare Registrar](https://www.cloudflare.com/products/registrar/) sells at
cost, around £10/year. [Porkbun](https://porkbun.com/) is a good alternative.

Edit `src/CNAME` and `src/_data/site.json` if you pick a different domain from
`techandsociety.org`.

### 3. Deploy on Cloudflare Pages

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** →
   **Connect to Git**, and select this repository.
2. Build settings:
   - Build command: `npm run build`
   - Output directory: `_site`
3. Deploy. You'll get a `*.pages.dev` URL immediately.
4. **Custom domains** → add your domain. DNS is automatic if the domain is
   registered with Cloudflare.

Every push to `main` now redeploys automatically.

### 4. Point the CMS at your repository

In `src/admin/config.yml`, replace:

```yaml
repo: YOUR-GITHUB-USERNAME/YOUR-REPO-NAME
```

You can now sign in at `/admin` using **Sign in with Token** and a GitHub
personal access token. That's enough for you alone. For collaborators, do step 5.

### 5. Add one-click GitHub sign-in (needed for collaborators)

This removes the need for anyone to generate tokens.

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
   - `ALLOWED_DOMAINS` — set to `techandsociety.org` so nobody else's site can
     use your authenticator.
4. In `src/admin/config.yml`, uncomment and set:
   ```yaml
   base_url: https://sveltia-cms-auth.YOUR-SUBDOMAIN.workers.dev
   ```

### 6. Add your collaborators

GitHub repository → **Settings → Collaborators → Add people**. Give them
**Write** access. They log in at `/admin` with their GitHub account.

---

## Working locally

```bash
npm install
npm run serve     # http://localhost:8080, live reload
npm run build     # writes to _site/
```

## Where things live

```
src/
  index.njk                        Homepage — all the one-page sections
  working-papers.njk               Working Paper Series listing
  sanjaya-lall-professorship.njk   Visiting Professorship page
  privacy.md              Placeholder — needs real wording
  accessibility.md        Placeholder — needs real wording
  _includes/layouts/      Page templates
  _data/site.json         Site name, URL, address, contact email
  content/
    people/               One Markdown file per person
  _data/
    papers.json           Working Paper Series entries
    holders.json          Visiting Professorship holders
  assets/papers/          Working paper PDFs
tools/
  make_cover.py           Generates the branded WP cover page
  assets/
    css/style.css         All styling; design tokens at the top
    img/                  Logo, hero illustration, uploads/
  admin/
    index.html            Loads the CMS
    config.yml            Defines the editing forms
```

## Still to do before launch

- [ ] Verify the Sanjaya Lall events archive (src/_data/lallevents.json) — dates
      and details were compiled from the Department of Economics website, Oxford
      Podcasts, event posters, and Wikipedia. 2022 is omitted — sources conflict
      on whether Stiglitz held the chair in 2022 or 2023, and the poster evidence
      points to 2023. The 2014 Krugman podcast link points to a keyword listing
      rather than the episode page.
- [ ] Confirm rights to republish the event posters (2013, 2014, 2018, 2023, 2024)

- [ ] Add Tom Robinson's CTS role and title (currently affiliation only)
- [ ] Decide whether Walter Mattli joins the People section, and with what role
- [ ] Confirm reproduction rights for the Sanjaya Lall portrait before launch
- [ ] Confirm reproduction permission for the eleven holder portraits before
      the site goes public, and record any required photographer credit in the
      `credit` field in src/_data/holders.json (it renders under each card).
- [ ] Add a portrait photo for each person (square images work best)
- [ ] Verify the Visiting Professorship years — Wikipedia and the Department of
      Economics disagree on whether Stiglitz held it in 2022 or 2023
- [ ] Confirm with AIGI how the Centre should be described and credited, and
      that using the AIGI logo in the footer is approved
- [ ] Replace the AIGI logo JPEG with a vector version if AIGI can supply one
- [ ] Have the privacy notice checked by the University Information Compliance
      Team, and the accessibility statement independently audited

---

## Working Paper Series

### Adding a paper

1. Generate the branded cover and merge it onto the paper:
   ```bash
   cd tools
   cp wp-2026-01.json wp-2026-02.json     # edit: number, title, authors, date, abstract
   python3 make_cover.py --config wp-2026-02.json \
                         --paper ~/Downloads/my-paper.pdf \
                         --out ../src/assets/papers/CTS-WP-2026-02.pdf
   ```
   Omit `--paper` to produce the cover on its own.
   Requires `pip install reportlab pypdf`.

2. Add an entry to `src/_data/papers.json`, setting `pdf` to
   `/assets/papers/CTS-WP-2026-02.pdf`.

3. Commit. The paper appears on `/working-papers/` and the newest one is
   featured in the Research section of the homepage.

### Numbering

`WP YYYY-NN` — year, then sequence within that year. WP 2026-01 is the first.

### A note on file size

PDFs live in the Git repository and are served by Cloudflare Pages. A 90-page
text PDF is typically 2–8 MB, which is fine. Keep an eye on two limits:
GitHub warns above 50 MB per file, and Cloudflare Pages caps a single
deployment at 25 MB per file. If a paper exceeds that — usually because of
high-resolution figures — either compress it:
```bash
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=small.pdf big.pdf
```
or leave `pdf` blank in papers.json and rely on the `preprint` link instead.
