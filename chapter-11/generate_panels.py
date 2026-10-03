#!/usr/bin/env python3
"""Chapter 11 panels. Idempotent: keep an existing jpg over 80kb. No gore."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import hashlib, random

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
NAMES = [
    "01-whitehall-letter.jpg",
    "02-mount-trenchard.jpg",
    "03-south-reen-doors.jpg",
    "04-times-sheet.jpg",
    "05-gregory-clause.jpg",
    "06-surrender-signed.jpg",
    "07-crowbar-eaves.jpg",
    "08-walls-down.jpg",
]
INK = (42, 34, 24)
RUST = (107, 58, 42)
SOOT = (28, 24, 20)
OCHRE = (176, 148, 96)
PAPER = (237, 228, 212)
MID = (90, 70, 50)

def rng_for(name):
    return random.Random(int(hashlib.md5(name.encode()).hexdigest()[:8], 16))

def grain(im, rng, n=48000):
    px = im.load(); w, h = im.size
    for _ in range(n):
        x, y = rng.randrange(w), rng.randrange(h)
        r, g, b = px[x, y]; v = rng.randint(-18, 12)
        px[x, y] = (max(0, min(255, r+v)), max(0, min(255, g+v)), max(0, min(255, b+v)))

def squiggle(d, x, y, n, color=MID, amp=3, step=7):
    pts = [(x + i*step, y + ((i % 3)-1)*amp) for i in range(n)]
    if len(pts) > 1:
        d.line(pts, fill=color, width=1)

def fig(d, x, y, h, ink=INK, lean=0):
    r = max(7, h//9)
    d.ellipse([x-r, y-2*r, x+r, y], outline=ink, width=2)
    d.line([(x, y), (x+lean, y+int(h*0.42))], fill=ink, width=3)
    hip = y+int(h*0.42)
    d.line([(x+lean, hip), (x-h//6, y+h)], fill=ink, width=2)
    d.line([(x+lean, hip), (x+h//6, y+h)], fill=ink, width=2)
    d.line([(x, y+h//6), (x-h//5, y+h//3)], fill=ink, width=2)
    d.line([(x, y+h//6), (x+h//5, y+h//3)], fill=ink, width=2)

def grade(im):
    g = ImageOps.grayscale(im.convert("RGB"))
    sep = Image.merge("RGB", (
        g.point(lambda x: min(255, int(x*1.04+18))),
        g.point(lambda x: min(255, int(x*0.90+8))),
        g.point(lambda x: min(255, int(x*0.68))),
    ))
    return ImageEnhance.Contrast(sep).enhance(1.18)

def base(name):
    rng = rng_for(name)
    im = Image.new("RGB", (1728, 1152), PAPER)
    return im, ImageDraw.Draw(im), rng

def scene_letter(im, d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(78, 66, 54))
    d.rectangle([80, 60, 700, 500], fill=(150, 162, 166), outline=INK, width=5)
    for i in range(3):
        d.rectangle([120+i*180, 100, 260+i*180, 280], outline=INK, width=2)
    d.rectangle([200, 520, 1500, 1000], fill=(120, 92, 68), outline=INK, width=6)
    d.rectangle([420, 600, 1180, 920], fill=PAPER, outline=RUST, width=4)
    for i in range(8):
        squiggle(d, 480, 660+i*28, 40, MID, 2, 8)
    fig(d, 1320, 640, 260, INK, -6)
    d.line([(1180, 780), (1280, 820)], fill=RUST, width=3)

def scene_estate(im, d, rng):
    d.rectangle([0, 0, 1728, 480], fill=(168, 176, 168))
    d.rectangle([0, 480, 1728, 1152], fill=(110, 118, 78))
    d.rectangle([180, 220, 980, 780], fill=(150, 128, 100), outline=INK, width=6)
    d.polygon([(140, 240), (580, 40), (1020, 240)], fill=(80, 58, 46), outline=INK)
    for wx, wy in ((260, 320), (460, 320), (700, 320), (280, 500), (680, 500)):
        d.rectangle([wx, wy, wx+90, wy+120], fill=(180, 196, 196), outline=INK, width=2)
    d.rectangle([500, 560, 660, 780], fill=(40, 32, 26))
    d.ellipse([1180, 700, 1560, 900], fill=(90, 70, 48), outline=INK)
    fig(d, 1280, 620, 200, INK, 8)
    d.rectangle([1360, 760, 1500, 860], fill=PAPER, outline=RUST, width=3)
    for i in range(3):
        squiggle(d, 1380, 790+i*18, 10, MID, 2, 6)

def scene_doors(im, d, rng):
    # closed doors, bread baskets, no interiors
    d.rectangle([0, 0, 1728, 420], fill=(120, 128, 132))
    d.polygon([(0, 500), (400, 360), (900, 460), (1400, 320), (1728, 480), (1728, 640), (0, 700)], fill=(90, 100, 78))
    d.rectangle([0, 640, 1728, 1152], fill=(100, 86, 68))
    d.polygon([(40, 620), (900, 700), (1728, 560)], outline=(70, 90, 100))
    for i in range(5):
        x = 80 + i*300
        d.rectangle([x, 360, x+220, 820], fill=(130, 108, 84), outline=INK, width=4)
        d.polygon([(x-10, 360), (x+110, 240), (x+230, 360)], fill=(70, 54, 42), outline=INK)
        d.rectangle([x+70, 560, x+150, 820], fill=SOOT)
        d.line([(x+70, 560), (x+150, 820)], fill=INK, width=3)
        d.line([(x+150, 560), (x+70, 820)], fill=INK, width=3)
    fig(d, 200, 860, 180, INK, 4)
    for i in range(3):
        d.ellipse([280+i*70, 980, 360+i*70, 1060], outline=OCHRE, width=3)
        d.ellipse([300+i*70, 1000, 340+i*70, 1040], fill=(150, 110, 70))

def scene_times(im, d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(90, 86, 80))
    d.rectangle([160, 80, 1560, 1040], fill=(214, 204, 184), outline=INK, width=6)
    d.line([(860, 120), (860, 980)], fill=MID, width=2)
    for col, x in ((0, 220), (1, 940)):
        d.rectangle([x, 160, x+520, 240], fill=SOOT)
        for i in range(10):
            squiggle(d, x+20, 280+i*60, 28, MID, 2, 8)
    fig(d, 400, 900, 80, INK, 0)
    d.rectangle([200, 980, 700, 1080], fill=(70, 60, 50))

def scene_clause(im, d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(70, 58, 48))
    d.polygon([(160, 780), (1560, 700), (1600, 980), (140, 1040)], fill=(130, 104, 76), outline=INK, width=4)
    d.rectangle([520, 760, 1200, 940], fill=PAPER, outline=RUST, width=5)
    for i in range(4):
        squiggle(d, 580, 800+i*28, 34, MID, 2, 8)
    d.rectangle([560, 800, 700, 900], outline=RUST, width=3)
    for i in range(9):
        fig(d, 220+i*160, 520, 160, INK if i % 2 == 0 else MID, 0)
    d.rectangle([80, 80, 1640, 280], fill=(100, 80, 62), outline=INK, width=3)

def scene_surrender(im, d, rng):
    d.rectangle([0, 700, 1728, 1152], fill=(108, 92, 70))
    d.rectangle([0, 0, 900, 700], fill=(160, 148, 124))
    d.rectangle([900, 0, 1728, 700], fill=(126, 140, 86))
    for i in range(6):
        d.rectangle([980, 80+i*90, 1660, 150+i*90], outline=(80, 100, 60))
    d.rectangle([180, 420, 820, 900], fill=(120, 92, 68), outline=INK, width=5)
    d.rectangle([260, 520, 700, 760], fill=PAPER, outline=INK, width=3)
    for i in range(5):
        squiggle(d, 300, 560+i*32, 22, MID, 2, 7)
    fig(d, 360, 240, 200, INK, 4)
    fig(d, 620, 260, 190, RUST, -4)
    d.line([(520, 400), (600, 560)], fill=INK, width=2)

def scene_crowbar(im, d, rng):
    d.rectangle([0, 0, 1728, 500], fill=(170, 168, 150))
    d.rectangle([0, 700, 1728, 1152], fill=(120, 108, 80))
    d.rectangle([200, 280, 900, 860], fill=(140, 116, 88), outline=INK, width=5)
    d.polygon([(160, 300), (550, 80), (960, 300)], fill=(90, 70, 48), outline=INK)
    # thatch lifting
    d.polygon([(200, 300), (420, 140), (500, 300)], fill=(160, 130, 80), outline=RUST)
    for i, x in enumerate((300, 480, 660)):
        fig(d, x, 520, 180, SOOT, 6)
        d.line([(x+40, 560), (x+120, 300)], fill=INK, width=4)
        d.line([(x+120, 300), (x+160, 280)], fill=INK, width=5)
    for i, x in enumerate((1100, 1280, 1460)):
        fig(d, x, 780, 200, INK, 14)
        d.ellipse([x-20, 860, x+40, 920], outline=MID)
    d.line([(1000, 1000), (1700, 920)], fill=(80, 64, 46), width=6)

def scene_walls(im, d, rng):
    d.rectangle([0, 0, 1728, 620], fill=(90, 86, 96))
    d.rectangle([0, 620, 1728, 1152], fill=(70, 60, 48))
    d.polygon([(200, 800), (360, 420), (420, 800)], fill=(100, 84, 66), outline=INK)
    d.polygon([(480, 860), (700, 500), (760, 880)], outline=INK, width=4)
    d.rectangle([800, 640, 1100, 900], outline=INK, width=4)
    d.line([(800, 640), (1100, 900)], fill=SOOT, width=3)
    d.rectangle([1180, 760, 1500, 900], fill=PAPER, outline=OCHRE, width=3)
    for i in range(3):
        squiggle(d, 1220, 800+i*24, 16, MID, 2, 7)
    fig(d, 200, 860, 140, INK, -10)
    d.ellipse([40, 80, 140, 180], outline=(200, 190, 160), width=2)

SCENES = {
    "01": scene_letter, "02": scene_estate, "03": scene_doors, "04": scene_times,
    "05": scene_clause, "06": scene_surrender, "07": scene_crowbar, "08": scene_walls,
}

def synth(name):
    im, d, rng = base(name)
    SCENES[name[:2]](im, d, rng)
    grain(im, rng)
    return grade(im)

def main():
    for name in NAMES:
        path = root / name
        if path.exists() and path.stat().st_size > 80000:
            print("keep", path, path.stat().st_size)
            continue
        synth(name).save(path, "JPEG", quality=92, optimize=False)
        print("synth", path, path.stat().st_size)

if __name__ == "__main__":
    main()
