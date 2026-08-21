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

## Fonts

`tools/fonts/` holds the typefaces used on the cover — Source Serif 4 (Adobe,
SIL Open Font License) and IBM Plex Sans and Mono (IBM, SIL Open Font License).
They are bundled so covers render identically on any machine. If the folder is
missing, the script falls back to built-in PDF fonts and prints a warning; the
layout still works but looks noticeably plainer.

## How titles are set

The cover splits the title at the first colon: the part before becomes the main
title, the part after becomes an italic subtitle. So

```json
"title": "The Political Economy of Artificial Intelligence: Evidence from Western Europe"
```

sets *The Political Economy of Artificial Intelligence* large, with *Evidence
from Western Europe* beneath it.

The main title is then set on **one line wherever possible**. The script starts
at 28pt and steps down; if the whole title fits on a single line at 18pt or
larger, that is what you get. Only a title too long for that falls back to two
lines, set as large as will fit.

When two lines are unavoidable, the break is **balanced** rather than greedy.
Ordinary wrapping fills the first line to the margin and strands the remainder;
the script instead tries every possible break and picks the one that minimises
the longest line, so both lines carry similar weight.

The subtitle follows the same logic at 82% of the title size, preferring one
line down to 13pt, and sits directly beneath the title with almost no gap so
the two read as a single unit. Every paper therefore gets the same treatment without
hand-tuning.

To control the split yourself — for a title with no colon, or one with several —
add an explicit `subtitle` field, which overrides the automatic split:

```json
"title": "Who Gains from Automation?",
"subtitle": "A Task-Level Analysis of Twenty-Three Advanced Economies"
```

A title with no colon and no `subtitle` simply runs on one or two lines with no
subtitle beneath.

## How the page is spaced

The cover lays itself out in two passes. It first measures every block — title,
subtitle, authors, date, abstract, keywords — then compares the total against
the space between the two banners and shares the leftover out among the gaps,
weighted so it goes between the subtitle and author and above the abstract.
The top margin, the title-to-subtitle gap and the abstract-to-keywords gap are
deliberately excluded, so the block sits high on the page and those pairs stay
tight however much space is available. Any remaining slack collects above the
bottom banner.

The result is that a long abstract and a short one both produce a balanced
page, rather than the short one leaving a gulf above the bottom banner.

Each gap has a ceiling, so a very sparse cover doesn't inflate until the title
floats mid-page; any slack beyond those ceilings sits above the bottom banner,
where empty space is least conspicuous. The weights and caps are the `weight`
and `cap` dictionaries in `build_cover()` if you ever want to retune them.
