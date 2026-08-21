# Working paper tooling

## Where the PDF path comes from

The `pdf` field in `src/_data/papers.json` is simply the file's location inside
the site, so you create the path by putting the file there.

1. **Generate the PDF.** Run the cover script on your machine, telling it where
   to write:

   ```bash
   cd tools
   python3 make_cover.py --config wp-2026-01.json \
                         --paper ~/Downloads/political-economy-of-ai.pdf \
                         --out ../src/assets/papers/CTS-WP-2026-01.pdf
   ```

   The `--paper` file is your existing 90-page PDF. The `--out` file is the new
   one with the cover on the front.

2. **Read off the path.** Everything inside `src/assets/` is served from
   `/assets/`, so a file at:

   ```
   src/assets/papers/CTS-WP-2026-01.pdf
   ```

   is reachable at:

   ```
   /assets/papers/CTS-WP-2026-01.pdf
   ```

   That string is what goes in the `pdf` field. It is already filled in for
   WP 2026-01 — you only need to place the file.

3. **Commit and push.** Cloudflare rebuilds and the download button goes live.

## First time only

```bash
pip install reportlab pypdf
```

## Checking it worked

```bash
npm run serve
```

then open http://localhost:8080/working-papers/ and click the download button.
If you get a 404, the file is not where step 1 put it — check the filename
matches `papers.json` exactly, including capitalisation.
