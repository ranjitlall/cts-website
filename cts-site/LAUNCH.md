# Launching on GitHub Pages

This gets the site live at `https://<your-username>.github.io/cts-website/` with
no domain purchase and no waiting on anyone. Roughly 30 minutes.

The Oxford domain, if granted, is added later without rebuilding anything.

---

## 1. Create the repository

From the project folder:

```bash
git init
git add .
git commit -m "Initial site"
```

Then create the repo on GitHub. Either use the web interface, or:

```bash
gh repo create cts-website --public --source=. --push
```

**Public or private?** GitHub Pages on a free account requires a **public**
repository. That means the source (and the working paper PDF) is publicly
readable. If you'd rather keep it private until launch, either use Cloudflare
Pages instead — which serves private repos on the free tier — or keep the repo
private now and make it public on the day you launch.

## 2. Adjust two settings for the subpath

A project site lives at `/cts-website/`, not at the domain root, so Eleventy
needs to know that. In `eleventy.config.js`, add a path prefix to the returned
config:

```js
  return {
    pathPrefix: "/cts-website/",
    dir: { ... }
  };
```

and in `src/_data/site.json` set:

```json
"url": "https://YOUR-USERNAME.github.io/cts-website"
```

Delete `src/CNAME` for now — it belongs to a custom domain, not to github.io.
Keep a copy; you'll want it back at step 6.

> When the Oxford domain arrives, both of these revert: `pathPrefix` goes away
> and `url` becomes the real address.

## 3. Add the build workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy site
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx @11ty/eleventy
      - uses: actions/upload-pages-artifact@v3
        with:
          path: _site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Commit and push it.

## 4. Turn on Pages

Repository → **Settings** → **Pages** → under *Build and deployment*, set
**Source** to **GitHub Actions**.

Push anything (or re-run the workflow from the Actions tab). In about a minute
the site is live at the URL shown on that settings page.

## 5. Point the CMS at the repository

In `src/admin/config.yml`, set:

```yaml
repo: YOUR-USERNAME/cts-website
```

You can then sign in at `/cts-website/admin/` with a GitHub personal access
token. For collaborators, deploy the Sveltia authenticator Worker as described
in README step 5 — that part is unchanged.

## 6. Later: adding the Oxford domain

When `cts.ox.ac.uk` (or whatever they grant) is approved, IT Services will ask
where to point it. Give them:

```
YOUR-USERNAME.github.io
```

as a CNAME target. Then on your side:

1. Repository → Settings → Pages → **Custom domain** → enter the hostname.
   This recreates the `CNAME` file automatically.
2. Remove `pathPrefix` from `eleventy.config.js`.
3. Set `url` in `src/_data/site.json` to `https://cts.ox.ac.uk`.
4. Tick **Enforce HTTPS** once the certificate is issued (a few minutes).

The `github.io` address keeps working and redirects to the new one, so nothing
you have circulated in the meantime breaks.

---

## What to tell Oxford IT Services

When you write to `domains@it.ox.ac.uk` (with your Head of Department's
approval), the detail they care about is where the hostname points. Something
like:

> The Centre for Technology and Society, within the Oxford Martin AI Governance
> Initiative, requests the hostname `cts.ox.ac.uk`. The site is a static site
> with no server-side code, built and hosted via GitHub Pages, with all content
> held in a repository controlled by the Centre. We would point the hostname at
> `YOUR-USERNAME.github.io` by CNAME. The site is currently live at
> `https://YOUR-USERNAME.github.io/cts-website/` for review.

The phrase "held in a repository controlled by the Centre" is the one that
matters — external hosting needs an exception, and retained departmental
control is the stated condition for granting it.
