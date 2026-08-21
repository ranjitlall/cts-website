#!/usr/bin/env python3
"""
CTS Working Paper cover page generator.

    python3 make_cover.py --config paper.json --out cover.pdf
    python3 make_cover.py --config paper.json --paper body.pdf --out CTS-WP-2026-01.pdf

With --paper, the cover is prepended to the existing PDF and metadata is written
into the merged file.

Fonts are bundled in tools/fonts/ so output is identical on every machine.
Requires: pip install reportlab pypdf
"""
import argparse, json, math, os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

W, H = A4
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

# --- Palette (matches the website) ------------------------------------------
NAVY      = HexColor("#002147")
NAVY_DEEP = HexColor("#001730")
INK       = HexColor("#101F2E")
GOLD      = HexColor("#F5B72E")
GOLD_DEEP = HexColor("#9A6410")
SLATE     = HexColor("#4A5B6B")
MIST      = HexColor("#F4F6F8")
PALE      = HexColor("#9FC4BA")
WHITE     = HexColor("#FFFFFF")

SPECTRUM = ["#F5B72E", "#F2853C", "#E8523C", "#D14E86",
            "#7B5EA7", "#2F7FC4", "#1E9C8A", "#63BF72"]

# --- Fonts -------------------------------------------------------------------
FACES = {
    "Serif":      "SourceSerif4-Regular.ttf",
    "Serif-Bold": "SourceSerif4-Bold.ttf",
    "Serif-Semi": "SourceSerif4-Semibold.ttf",
    "Serif-It":   "SourceSerif4-It.ttf",
    "Sans":       "IBMPlexSans-Regular.ttf",
    "Sans-Semi":  "IBMPlexSans-SemiBold.ttf",
    "Mono":       "IBMPlexMono-Regular.ttf",
    "Mono-Med":   "IBMPlexMono-Medium.ttf",
}
FALLBACK = {"Serif": "Times-Roman", "Serif-Bold": "Times-Bold",
            "Serif-Semi": "Times-Bold", "Serif-It": "Times-Italic",
            "Sans": "Helvetica", "Sans-Semi": "Helvetica-Bold",
            "Mono": "Courier", "Mono-Med": "Courier-Bold"}

def register_fonts():
    names, missing = {}, False
    for key, filename in FACES.items():
        path = os.path.join(FONTS, filename)
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(key, path))
                names[key] = key
                continue
            except Exception:
                pass
        names[key] = FALLBACK[key]; missing = True
    if missing:
        print("note: bundled fonts not found — using built-in substitutes",
              file=sys.stderr)
    return names

F = {}

# --- Helpers -----------------------------------------------------------------
def _lerp(c1, c2, t):
    a = tuple(int(c1[i:i+2], 16) for i in (1, 3, 5))
    b = tuple(int(c2[i:i+2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def spectrum(t):
    t = max(0.0, min(0.999, t)); n = len(SPECTRUM) - 1
    i = int(t*n); f = t*n - i
    return HexColor(_lerp(SPECTRUM[i], SPECTRUM[i+1], f))

def tracked(c, text, x, y, font, size, colour, tracking=0.0):
    c.setFont(font, size); c.setFillColor(colour)
    for ch in text:
        c.drawString(x, y, ch)
        x += pdfmetrics.stringWidth(ch, font, size) + tracking

def tracked_width(text, font, size, tracking=0.0):
    return sum(pdfmetrics.stringWidth(ch, font, size) + tracking for ch in text)

def wrapped(text, font, size, maxw):
    return simpleSplit(text, font, size, maxw)


def split_title(cfg):
    """Main title and subtitle. An explicit `subtitle` in the config wins;
    otherwise split on the first colon, which is where academic titles break."""
    if cfg.get("subtitle"):
        return cfg["title"].strip(), cfg["subtitle"].strip()
    title = cfg["title"]
    if ":" in title:
        head, tail = title.split(":", 1)
        if len(tail.strip()) > 3:
            return head.strip(), tail.strip()
    return title.strip(), ""

def _widths(lines, font, size):
    return [pdfmetrics.stringWidth(l, font, size) for l in lines]

def balanced(text, font, size, k):
    """Break `text` into exactly k lines, minimising the longest line.

    Greedy wrapping fills each line to the margin, which strands short words
    at the end ("...Artificial / Intelligence"). Balancing instead splits near
    the middle, so both lines carry similar weight."""
    words = text.split()
    if k <= 1 or len(words) <= 1:
        return [" ".join(words)]
    if len(words) < k:
        return words + [""] * (k - len(words))

    best, best_key = None, None
    n = len(words)

    def recurse(start, remaining, acc):
        nonlocal best, best_key
        if remaining == 1:
            lines = acc + [" ".join(words[start:])]
            w = _widths(lines, font, size)
            key = (max(w), max(w) - min(w))
            if best_key is None or key < best_key:
                best_key, best = key, lines
            return
        # leave at least one word for each remaining line
        for i in range(start + 1, n - remaining + 2):
            recurse(i, remaining - 1, acc + [" ".join(words[start:i])])

    recurse(0, k, [])
    return best

def fit_lines(text, font, maxw, max_lines, start, floor, step=0.5,
              one_line_floor=None):
    """Set `text` as large as possible within `max_lines`, breaking lines so
    their lengths are balanced.

    If `one_line_floor` is given, a single line is preferred wherever it can be
    set at that size or larger — a title reads better unbroken. Only when it
    would have to shrink below that floor do we fall back to two balanced
    lines at a larger size."""
    if one_line_floor is not None:
        size = start
        while size >= one_line_floor:
            if pdfmetrics.stringWidth(text, font, size) <= maxw:
                return size, [text]
            size -= step

    size = start
    while size > floor:
        for k in range(1, max_lines + 1):
            lines = balanced(text, font, size, k)
            if max(_widths(lines, font, size)) <= maxw:
                return size, lines
        size -= step
    return floor, balanced(text, font, floor, max_lines)

# --- The mark ----------------------------------------------------------------
def draw_mark(c, x, y, size, light=False):
    """Outline triangle enclosing the constellation — the current site logo."""
    stroke = WHITE if light else INK
    cx, cy = x + size*0.50, y + size*0.44
    r = size*0.56
    pts = [(cx + r*math.cos(math.radians(90 + k*120)),
            cy + r*math.sin(math.radians(90 + k*120))) for k in range(3)]
    c.saveState()
    c.setStrokeColor(stroke); c.setLineJoin(1); c.setLineCap(1)
    c.setLineWidth(size*0.032)
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.drawPath(p, stroke=1, fill=0)

    nodes = [(0.12,0.50,.078),(0.28,0.28,.062),(0.29,0.72,.062),(0.50,0.48,.055),
             (0.54,0.80,.050),(0.46,0.22,.050),(0.71,0.32,.046),(0.73,0.66,.046),
             (0.86,0.50,.038)]
    tints = [0.02, 0.16, 0.34, 0.50, 0.62, 0.24, 0.74, 0.86, 0.06]
    edges = [(0,1),(0,2),(1,3),(2,3),(1,5),(3,4),(2,4),(3,6),(3,7),(5,6),(4,7),(6,8),(7,8)]
    P = [(x + nx*size, y + size - ny*size) for nx, ny, _ in nodes]

    c.setLineWidth(size*0.024)
    for i, j in edges:
        c.line(P[i][0], P[i][1], P[j][0], P[j][1])
    for (px, py), (_, _, nr), t in zip(P, nodes, tints):
        c.setFillColor(spectrum(t))
        c.circle(px, py, nr*size, stroke=1, fill=1)
    c.restoreState()

def spectrum_rule(c, y, h, segments=64):
    seg = W / segments
    for i in range(segments):
        c.setFillColor(spectrum(i/(segments-1)))
        c.rect(i*seg, y, seg + 0.7, h, stroke=0, fill=1)

# --- Cover -------------------------------------------------------------------
def build_cover(path, cfg):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle(cfg["title"])
    c.setAuthor(", ".join(cfg["authors"]))
    c.setSubject(f'CTS Working Paper {cfg["number"]}')
    c.setCreator("Centre for Technology and Society, University of Oxford")

    ML, MR = 26*mm, 26*mm
    tw = W - ML - MR

    # ---------- TOP BANNER ----------
    BH = 50*mm
    c.setFillColor(NAVY); c.rect(0, H-BH, W, BH, stroke=0, fill=1)
    draw_mark(c, ML, H-39*mm, 22*mm, light=True)

    tx = ML + 28*mm
    c.setFillColor(WHITE)
    c.setFont(F["Serif-Bold"], 31); c.drawString(tx, H-24.5*mm, "CTS")
    c.setFillColor(GOLD); c.rect(tx+1, H-27.2*mm, 27*mm, 1.2, stroke=0, fill=1)
    c.setFillColor(WHITE); c.setFont(F["Serif-Semi"], 13)
    c.drawString(tx, H-32.5*mm, "Centre for Technology and Society")
    tracked(c, "UNIVERSITY OF OXFORD", tx, H-37.8*mm, F["Sans"], 7.2, PALE, 1.5)

    label = "WORKING PAPER SERIES"
    lw = tracked_width(label, F["Mono-Med"], 8, 1.7)
    tracked(c, label, W-MR-lw, H-23*mm, F["Mono-Med"], 8, GOLD, 1.7)
    c.setFillColor(WHITE); c.setFont(F["Serif-Bold"], 25)
    c.drawRightString(W-MR, H-33.5*mm, cfg["number"])

    spectrum_rule(c, H-BH-2.6*mm, 2.6*mm)

    FB_H = 32*mm          # bottom banner height, needed by the measuring pass

    # ---------- MEASURE ----------
    # Everything between the two banners is measured first, then the leftover
    # space is distributed into the gaps. Without this, short abstracts leave a
    # gulf above the bottom banner and the title sits cramped against the top.
    main, sub = split_title(cfg)

    tsize, tlines = fit_lines(main, F["Serif-Bold"], tw, 2, 28, 17, one_line_floor=18)
    tlead = tsize * 1.16
    h_title = len(tlines) * tlead

    ssize, slines = (0, [])
    h_sub = 0
    if sub:
        ssize, slines = fit_lines(sub, F["Serif-It"], tw, 2, tsize * 0.82, 12,
                                  one_line_floor=13)
        h_sub = len(slines) * ssize * 1.22

    h_authors = 0
    for a in cfg["authors"]:
        h_authors += 5.4*mm
        if cfg.get("affiliations", {}).get(a):
            h_authors += 6.8*mm

    h_date = 4*mm

    abs_lines = wrapped(cfg["abstract"], F["Serif"], 10.5, tw - 14*mm) if cfg.get("abstract") else []
    h_abstract = (14*mm + len(abs_lines) * 5.2*mm) if abs_lines else 0

    kw_rows = 0
    if cfg.get("keywords"):
        x = ML; kw_rows = 1
        for k in cfg["keywords"]:
            wd = pdfmetrics.stringWidth(k, F["Mono"], 7.6) + 8*mm
            if x + wd > W - MR:
                x = ML; kw_rows += 1
            x += wd
    h_keywords = kw_rows * 8*mm

    # Base gaps, then slack shared out by weight
    # title_sub is deliberately near zero: the subtitle belongs to the title and
    # should read as one unit. abs_kw likewise stays tight, so the keywords tuck
    # under the abstract rather than floating between it and the banner.
    g = {"top": 17*mm, "title_sub": 0.4*mm, "sub_auth": 3*mm,
         "auth_date": 0*mm, "date_abs": 8.5*mm, "abs_kw": 6*mm, "bottom": 12*mm}
    weight = {"top": 0.0, "title_sub": 0.0, "sub_auth": 0.06,
              "auth_date": 0.08, "date_abs": 0.14, "abs_kw": 0.0}

    top_limit = H - BH - 2.6*mm
    bottom_limit = FB_H + 2.2*mm
    available = top_limit - bottom_limit
    content = (h_title + h_sub + h_authors + h_date + h_abstract + h_keywords
               + sum(g.values()))
    # Caps stop a short abstract from inflating every gap until the title
    # floats in the middle of the page. Any slack left over simply sits above
    # the bottom banner, which is where empty space is least conspicuous.
    cap = {"top": 0*mm, "title_sub": 0*mm, "sub_auth": 2.5*mm,
           "auth_date": 1.5*mm, "date_abs": 5*mm, "abs_kw": 0*mm}
    slack = available - content
    if slack > 0:
        for key, wgt in weight.items():
            g[key] += min(slack * wgt, cap[key])

    # ---------- DRAW ----------
    yy = top_limit - g["top"]

    c.setFillColor(NAVY)
    for ln in tlines:
        c.setFont(F["Serif-Bold"], tsize); c.drawString(ML, yy, ln); yy -= tlead
    yy -= g["title_sub"]

    if slines:
        c.setFillColor(HexColor("#3D5876"))
        for ln in slines:
            c.setFont(F["Serif-It"], ssize); c.drawString(ML, yy, ln)
            yy -= ssize * 1.22
        yy -= g["sub_auth"]
    else:
        yy -= g["sub_auth"]

    for a in cfg["authors"]:
        c.setFillColor(NAVY); c.setFont(F["Serif-Semi"], 14.5)
        c.drawString(ML, yy, a); yy -= 5.4*mm
        aff = cfg.get("affiliations", {}).get(a)
        if aff:
            c.setFillColor(SLATE); c.setFont(F["Sans"], 9)
            c.drawString(ML, yy, aff); yy -= 6.8*mm
    yy -= g["auth_date"]

    tracked(c, cfg["date"].upper(), ML, yy, F["Mono"], 8, SLATE, 1.2)
    yy -= g["date_abs"]

    if abs_lines:
        top = yy
        c.setFillColor(MIST)
        c.rect(ML - 6*mm, top - h_abstract + 5*mm, tw + 12*mm, h_abstract, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(ML - 6*mm, top - h_abstract + 5*mm, 1.8*mm, h_abstract, stroke=0, fill=1)

        yy = top - 3.5*mm
        tracked(c, "ABSTRACT", ML, yy, F["Mono-Med"], 7.6, GOLD_DEEP, 2.4)
        yy -= 7.8*mm
        c.setFillColor(INK)
        for ln in abs_lines:
            c.setFont(F["Serif"], 10.5); c.drawString(ML, yy, ln); yy -= 5.2*mm
        yy -= g["abs_kw"]

    if cfg.get("keywords"):
        x = ML
        n = max(1, len(cfg["keywords"]) - 1)
        for i, k in enumerate(cfg["keywords"]):
            wd = pdfmetrics.stringWidth(k, F["Mono"], 7.6) + 8*mm
            if x + wd > W - MR:
                x = ML; yy -= 8*mm
            col = spectrum(i/n)
            c.setStrokeColor(col); c.setLineWidth(0.8)
            c.roundRect(x, yy - 2.4*mm, wd - 2.5*mm, 6.4*mm, 3.2*mm, stroke=1, fill=0)
            c.setFillColor(col); c.setFont(F["Mono"], 7.6)
            c.drawString(x + 2.8*mm, yy, k)
            x += wd

    # ---------- BOTTOM BANNER ----------
    FB = FB_H
    c.setFillColor(NAVY_DEEP); c.rect(0, 0, W, FB, stroke=0, fill=1)
    spectrum_rule(c, FB, 2.2*mm)

    c.setFillColor(WHITE); c.setFont(F["Serif-Semi"], 11)
    c.drawString(ML, FB - 10*mm, f'CTS Working Paper {cfg["number"]}')

    note = cfg.get("series_note",
        "Working papers are circulated for discussion and comment; they have not been "
        "peer reviewed. Views expressed are those of the authors.")
    ny = FB - 15.5*mm
    c.setFillColor(HexColor("#93A8BD"))
    for ln in wrapped(note, F["Sans"], 7.3, tw - 52*mm):
        c.setFont(F["Sans"], 7.3); c.drawString(ML, ny, ln); ny -= 3.6*mm

    if cfg.get("url"):
        c.setFillColor(GOLD); c.setFont(F["Sans-Semi"], 8)
        c.drawRightString(W - MR, FB - 10*mm, cfg["url"])
    c.setFillColor(HexColor("#7F97AE")); c.setFont(F["Sans"], 7.3)
    c.drawRightString(W - MR, FB - 15.5*mm, "Oxford Martin AI Governance Initiative")
    c.drawRightString(W - MR, FB - 19.1*mm, "University of Oxford")

    c.showPage(); c.save()

# --- CLI ---------------------------------------------------------------------
def main():
    global F
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--paper", help="existing PDF to prepend the cover to")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    F = register_fonts()
    cfg = json.load(open(a.config))

    out_dir = os.path.dirname(os.path.abspath(a.out))
    os.makedirs(out_dir, exist_ok=True)

    if not a.paper:
        build_cover(a.out, cfg); print("cover ->", a.out); return

    from pypdf import PdfReader, PdfWriter
    tmp = os.path.join(out_dir, "._cover_tmp.pdf")
    build_cover(tmp, cfg)
    w = PdfWriter()
    for p in PdfReader(tmp).pages: w.add_page(p)
    for p in PdfReader(a.paper).pages: w.add_page(p)
    w.add_metadata({"/Title": cfg["title"],
                    "/Author": ", ".join(cfg["authors"]),
                    "/Subject": f'CTS Working Paper {cfg["number"]}'})
    with open(a.out, "wb") as f: w.write(f)
    os.remove(tmp)
    print("merged ->", a.out)

if __name__ == "__main__":
    main()
