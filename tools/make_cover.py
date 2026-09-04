#!/usr/bin/env python3
"""
CTS Working Paper cover page generator.

Usage:
    python make_cover.py --config paper.json --out cover.pdf
    python make_cover.py --config paper.json --paper body.pdf --out CTS-WP-2026-01.pdf

With --paper, the cover is prepended to the existing PDF and the metadata
(title, author, subject) is written into the merged file.
"""
import argparse, json, math, random, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import simpleSplit

W, H = A4
NAVY   = HexColor("#002147")
GOLD   = HexColor("#F0B429")
SLATE  = HexColor("#4A5B6B")
RULE   = HexColor("#D8E0E8")

SPECTRUM = ["#F0B429","#F08A3C","#E8604C","#C9518C","#7B5EA7","#3E7FC1","#2E9E8F","#5FBF7F"]

def _lerp(c1, c2, t):
    a = tuple(int(c1[i:i+2],16) for i in (1,3,5))
    b = tuple(int(c2[i:i+2],16) for i in (1,3,5))
    return "#%02x%02x%02x" % tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def spectrum(t):
    t = max(0.0, min(0.999, t)); n = len(SPECTRUM)-1
    i = int(t*n); f = t*n - i
    return HexColor(_lerp(SPECTRUM[i], SPECTRUM[i+1], f))

def draw_mark(c, x, y, size):
    """The CTS constellation, drawn to scale in spectrum colours."""
    nodes = [(0.10,0.42,.055),(0.24,0.20,.049),(0.26,0.66,.049),(0.44,0.40,.046),
             (0.46,0.80,.043),(0.42,0.06,.040),(0.63,0.22,.040),(0.65,0.58,.037),
             (0.83,0.38,.034),(0.86,0.74,.031),(0.80,0.06,.031)]
    edges = [(0,1),(0,2),(1,3),(2,3),(1,5),(3,4),(2,4),(3,6),(3,7),(5,6),(4,7),(6,8),(7,8),(7,9),(6,10)]
    pts = [(x+nx*size, y+size-ny*size) for nx,ny,_ in nodes]
    c.saveState()
    c.setLineWidth(size*0.014)
    for i,j in edges:
        c.setStrokeColor(spectrum((nodes[i][0]+nodes[j][0])/2))
        c.setLineCap(1)
        c.line(pts[i][0], pts[i][1], pts[j][0], pts[j][1])
    for (px,py),(nx,_,r) in zip(pts, nodes):
        c.setFillColor(spectrum(nx))
        c.circle(px, py, r*size, stroke=0, fill=1)
    c.restoreState()

def wrapped(c, text, font, size, maxw):
    c.setFont(font, size)
    return simpleSplit(text, font, size, maxw)

def build_cover(path, cfg):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle(cfg["title"]); c.setAuthor(", ".join(cfg["authors"]))
    c.setSubject(f'CTS Working Paper {cfg["number"]}')

    ML, MR = 28*mm, 28*mm
    tw = W - ML - MR

    # --- Top band -----------------------------------------------------
    c.setFillColor(NAVY)
    c.rect(0, H-46*mm, W, 46*mm, stroke=0, fill=1)
    draw_mark(c, ML, H-34*mm, 17*mm)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Times-Bold", 27)
    c.drawString(ML+24*mm, H-24*mm, "CTS")
    c.setFont("Times-Roman", 12.5)
    c.drawString(ML+24*mm, H-30.5*mm, "Centre for Technology and Society")
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor("#9FB6CC"))
    c.drawString(ML+24*mm, H-35.5*mm, "UNIVERSITY OF OXFORD")
    # series label, right aligned
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(W-MR, H-24*mm, "WORKING PAPER SERIES")
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Times-Bold", 20)
    c.drawRightString(W-MR, H-33*mm, cfg["number"])

    # --- Spectrum hairline --------------------------------------------
    y = H-46*mm
    seg = W/48
    for i in range(48):
        c.setFillColor(spectrum(i/47))
        c.rect(i*seg, y-2.2*mm, seg+0.6, 2.2*mm, stroke=0, fill=1)

    # --- Title --------------------------------------------------------
    yy = H - 78*mm
    for ln in wrapped(c, cfg["title"], "Times-Bold", 24, tw):
        c.setFillColor(NAVY); c.setFont("Times-Bold", 24)
        c.drawString(ML, yy, ln); yy -= 11.4*mm

    # --- Authors ------------------------------------------------------
    yy -= 3*mm
    for a in cfg["authors"]:
        c.setFillColor(NAVY); c.setFont("Times-Roman", 13.5)
        c.drawString(ML, yy, a); yy -= 6*mm
        if cfg.get("affiliations", {}).get(a):
            c.setFillColor(SLATE); c.setFont("Helvetica", 9)
            c.drawString(ML, yy, cfg["affiliations"][a]); yy -= 7*mm

    # --- Date ---------------------------------------------------------
    yy -= 2*mm
    c.setFillColor(SLATE); c.setFont("Helvetica", 9.5)
    c.drawString(ML, yy, cfg["date"])
    yy -= 9*mm
    c.setStrokeColor(RULE); c.setLineWidth(0.7)
    c.line(ML, yy, W-MR, yy)
    yy -= 10*mm

    # --- Abstract -----------------------------------------------------
    if cfg.get("abstract"):
        c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 8)
        c.drawString(ML, yy, "A B S T R A C T"); yy -= 7*mm
        c.setFillColor(HexColor("#14202B"))
        for ln in wrapped(c, cfg["abstract"], "Times-Roman", 11, tw):
            if yy < 62*mm: break
            c.setFont("Times-Roman", 11)
            c.drawString(ML, yy, ln); yy -= 5.5*mm

    # --- Keywords / JEL -----------------------------------------------
    if cfg.get("keywords"):
        yy -= 4*mm
        c.setFillColor(SLATE); c.setFont("Helvetica-Oblique", 8.5)
        for ln in wrapped(c, "Keywords: " + "; ".join(cfg["keywords"]), "Helvetica-Oblique", 8.5, tw):
            c.drawString(ML, yy, ln); yy -= 4.6*mm

    # --- Footer -------------------------------------------------------
    c.setStrokeColor(RULE); c.setLineWidth(0.7)
    c.line(ML, 34*mm, W-MR, 34*mm)
    c.setFillColor(SLATE); c.setFont("Helvetica", 7.6)
    lines = [
        f'CTS Working Paper {cfg["number"]} · Centre for Technology and Society, University of Oxford',
        cfg.get("series_note",
                "Part of the Oxford Martin AI Governance Initiative. Working papers are circulated for discussion "
                "and comment; they have not been peer reviewed. Views expressed are those of the authors."),
    ]
    fy = 28*mm
    for ln in lines:
        for w in wrapped(c, ln, "Helvetica", 7.6, tw):
            c.setFont("Helvetica", 7.6)
            c.drawString(ML, fy, w); fy -= 3.9*mm
    if cfg.get("url"):
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 7.6)
        c.drawString(ML, fy-1*mm, cfg["url"])

    c.showPage(); c.save()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--paper", help="existing PDF to prepend the cover to")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cfg = json.load(open(a.config))

    if not a.paper:
        build_cover(a.out, cfg); print("cover ->", a.out); return

    from pypdf import PdfReader, PdfWriter
    build_cover("_cover_tmp.pdf", cfg)
    w = PdfWriter()
    for p in PdfReader("_cover_tmp.pdf").pages: w.add_page(p)
    for p in PdfReader(a.paper).pages: w.add_page(p)
    w.add_metadata({"/Title": cfg["title"],
                    "/Author": ", ".join(cfg["authors"]),
                    "/Subject": f'CTS Working Paper {cfg["number"]}'})
    with open(a.out, "wb") as f: w.write(f)
    print("merged ->", a.out)

if __name__ == "__main__":
    main()
