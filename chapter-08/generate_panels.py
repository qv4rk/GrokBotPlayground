#!/usr/bin/env python3
"""Chapter 08 panels. Idempotent: keep an existing jpg over 80kb."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import hashlib, random

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
NAMES = [
    "01-lough-mask-ledger.jpg",
    "02-women-on-the-road.jpg",
    "03-staff-walk-off.jpg",
    "04-ballinrobe-shutters.jpg",
    "05-league-hall.jpg",
    "06-rain-from-claremorris.jpg",
    "07-turnips-under-escort.jpg",
    "08-ambulance-and-placards.jpg",
]
INK = (42, 34, 24)
RUST = (107, 58, 42)
SOOT = (28, 24, 20)
OCHRE = (176, 148, 96)
PAPER = (237, 228, 212)
MID = (90, 70, 50)


def rng_for(name):
    return random.Random(int(hashlib.md5(name.encode()).hexdigest()[:8], 16))


def grain(im, rng, n=42000):
    px = im.load()
    w, h = im.size
    for _ in range(n):
        x, y = rng.randrange(w), rng.randrange(h)
        r, g, b = px[x, y]
        v = rng.randint(-18, 12)
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))


def hatch(d, box, step=11, color=(196, 180, 156), width=1):
    x0, y0, x1, y1 = box
    for i in range(x0 - (y1 - y0), x1, step):
        d.line([(i, y0), (i + (y1 - y0), y1)], fill=color, width=width)


def fig(d, x, y, h, ink=INK, lean=0, skirt=False):
    r = max(7, h // 9)
    d.ellipse([x - r, y - 2 * r, x + r, y], outline=ink, width=2)
    d.line([(x, y), (x + lean, y + int(h * 0.42))], fill=ink, width=3)
    hip = (x + lean, y + int(h * 0.42))
    if skirt:
        d.polygon([
            (hip[0] - h // 5, hip[1]),
            (hip[0] + h // 5, hip[1]),
            (x + h // 4, y + h),
            (x - h // 4, y + h),
        ], outline=ink)
        d.line([(hip[0], hip[1]), (x - h // 7, y + h)], fill=ink, width=2)
        d.line([(hip[0], hip[1]), (x + h // 7, y + h)], fill=ink, width=2)
    else:
        d.line([hip, (x - h // 6, y + h)], fill=ink, width=2)
        d.line([hip, (x + h // 6, y + h)], fill=ink, width=2)
    d.line([(x, y + h // 6), (x - h // 5, y + h // 3)], fill=ink, width=2)
    d.line([(x, y + h // 6), (x + h // 5, y + h // 3)], fill=ink, width=2)


def squiggle(d, x, y, n, color=MID, amp=3, step=7):
    pts = []
    for i in range(n):
        pts.append((x + i * step, y + ((i % 3) - 1) * amp))
    if len(pts) > 1:
        d.line(pts, fill=color, width=1)


def grade(im):
    im = im.convert("RGB")
    g = ImageOps.grayscale(im)
    sep = Image.merge("RGB", (
        g.point(lambda x: min(255, int(x * 1.04 + 18))),
        g.point(lambda x: min(255, int(x * 0.90 + 8))),
        g.point(lambda x: min(255, int(x * 0.68))),
    ))
    return ImageEnhance.Contrast(sep).enhance(1.18)


def base(name):
    rng = rng_for(name)
    im = Image.new("RGB", (1728, 1152), PAPER)
    d = ImageDraw.Draw(im)
    return im, d, rng


def scene_ledger(im, d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(214, 204, 186))
    d.rectangle([0, 620, 1728, 1152], fill=(92, 74, 56))
    d.rectangle([1080, 80, 1620, 560], fill=(150, 168, 176), outline=INK, width=8)
    d.rectangle([1120, 120, 1580, 340], fill=(168, 186, 190))
    d.polygon([(1120, 340), (1580, 340), (1580, 500), (1120, 470)], fill=(78, 96, 108))
    d.polygon([(1180, 300), (1460, 250), (1520, 320)], fill=(120, 112, 96), outline=INK)
    d.polygon([(160, 700), (980, 640), (1040, 980), (120, 1040)], fill=(120, 92, 64), outline=INK)
    d.rectangle([220, 360, 900, 760], fill=(232, 222, 204), outline=INK, width=5)
    d.line([(560, 380), (560, 740)], fill=RUST, width=3)
    for i in range(9):
        squiggle(d, 260, 420 + i * 32, 28, MID, 2, 8)
        squiggle(d, 600, 420 + i * 32, 26, MID, 2, 8)
    d.rectangle([640, 620, 820, 700], outline=RUST, width=4)
    fig(d, 980, 820, 220, INK, 6)
    d.rectangle([1180, 780, 1560, 1040], outline=INK, width=3)
    hatch(d, (0, 620, 1728, 1152), 18, (80, 64, 48))


def scene_road(im, d, rng):
    d.rectangle([0, 0, 1728, 520], fill=(186, 176, 150))
    d.polygon([(0, 520), (400, 380), (700, 460), (1100, 340), (1728, 480), (1728, 620), (0, 680)], fill=(110, 122, 78))
    d.polygon([(0, 640), (1728, 560), (1728, 1152), (0, 1152)], fill=(132, 112, 84))
    d.line([(0, 900), (1728, 760)], fill=(90, 74, 52), width=8)
    for i in range(8):
        d.ellipse([40 + i * 210, 430, 180 + i * 210, 560], fill=(70, 82, 48), outline=INK)
    for i, x in enumerate([220, 340, 470, 600, 760]):
        fig(d, x, 780, 250, INK if i % 2 == 0 else RUST, rng.randint(-8, 8), skirt=True)
        d.polygon([(x - 30, 700), (x + 10, 640), (x + 50, 720)], outline=INK)
    fig(d, 1180, 740, 230, SOOT, 18)
    d.polygon([(1280, 860), (1460, 900), (1400, 980)], fill=(226, 214, 196), outline=INK)
    for i in range(4):
        d.polygon([(1240 + i * 40, 980), (1300 + i * 40, 960), (1320 + i * 40, 1040)], fill=PAPER, outline=MID)
        squiggle(d, 1250 + i * 40, 1000, 6, MID, 2, 6)
    for x in (1460, 1600):
        fig(d, x, 700, 260, SOOT, 8)
        d.ellipse([x - 22, 430, x + 22, 490], outline=INK, width=3)
        d.rectangle([x - 16, 500, x + 16, 620], outline=INK, width=2)
    for i in range(12):
        x, y = 1000 + rng.randint(0, 280), 980 + rng.randint(0, 80)
        d.ellipse([x, y, x + 18, y + 12], fill=(70, 56, 40))


def scene_walkoff(im, d, rng):
    d.rectangle([0, 0, 1728, 480], fill=(198, 186, 160))
    d.rectangle([0, 780, 1728, 1152], fill=(120, 100, 76))
    d.rectangle([80, 260, 620, 820], fill=(168, 140, 110), outline=INK, width=5)
    d.polygon([(60, 280), (350, 80), (640, 280)], fill=(90, 62, 48), outline=INK)
    d.rectangle([250, 480, 380, 820], fill=(50, 40, 32))
    for wx, wy in ((140, 360), (460, 360), (160, 560)):
        d.rectangle([wx, wy, wx + 70, wy + 90], fill=(180, 196, 200), outline=INK, width=2)
    d.rectangle([700, 420, 1040, 820], fill=(130, 104, 78), outline=INK, width=4)
    d.rectangle([760, 560, 980, 820], fill=(40, 32, 26))
    d.arc([800, 640, 940, 760], 200, 20, fill=RUST, width=3)
    d.ellipse([1080, 700, 1280, 860], outline=INK, width=3)
    d.ellipse([1240, 720, 1460, 880], outline=INK, width=3)
    for i, x in enumerate([1500, 1380, 1260, 1140, 1580]):
        fig(d, x - i * 10, 860, 180 + (i % 3) * 20, INK, -12)
        d.rectangle([x - 30, 900, x + 10, 940], outline=MID)
    d.line([(900, 1000), (1728, 900)], fill=(80, 64, 46), width=6)


def scene_shutters(im, d, rng):
    d.rectangle([0, 620, 1728, 1152], fill=(110, 96, 78))
    d.rectangle([0, 0, 1728, 280], fill=(170, 176, 168))
    for i in range(5):
        x = 40 + i * 330
        d.rectangle([x, 180, x + 300, 760], fill=(150, 128, 102), outline=INK, width=4)
        d.polygon([(x, 180), (x + 150, 60), (x + 300, 180)], outline=INK)
        for s in range(6):
            d.rectangle([x + 30, 260 + s * 70, x + 270, 310 + s * 70], fill=(70, 56, 44), outline=SOOT)
        d.rectangle([x + 90, 560, x + 210, 760], outline=INK, width=3)
    fig(d, 860, 860, 220, INK, 0)
    d.polygon([(780, 980), (900, 960), (920, 1060), (760, 1070)], outline=RUST, width=3)
    d.rectangle([1400, 480, 1660, 900], fill=(40, 32, 28))
    fig(d, 1520, 700, 160, PAPER, 0)
    d.rectangle([1390, 470, 1480, 900], fill=(100, 80, 60))


def scene_hall(im, d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(70, 58, 48))
    d.rectangle([80, 80, 1640, 1070], fill=(196, 180, 154), outline=INK, width=6)
    for x in (200, 500, 860, 1200, 1500):
        d.line([(x, 80), (x, 1070)], fill=(120, 90, 64), width=8)
    for row in range(4):
        y = 780 - row * 140
        d.rectangle([180, y, 1100, y + 36], fill=(110, 82, 58), outline=INK)
        for i in range(7):
            fig(d, 240 + i * 120, y - 10, 110, INK, 0)
    fig(d, 1360, 620, 280, RUST, -4)
    d.rectangle([1240, 200, 1560, 460], fill=PAPER, outline=INK, width=4)
    for i in range(3):
        d.rectangle([1280, 250 + i * 60, 1520, 280 + i * 60], fill=RUST)
    d.ellipse([1480, 120, 1600, 200], outline=OCHRE, width=3)


def scene_rain(im, d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(150, 156, 150))
    d.rectangle([0, 280, 520, 900], fill=(90, 78, 66), outline=INK, width=5)
    d.polygon([(0, 280), (260, 120), (520, 280)], fill=(60, 50, 42), outline=INK)
    d.rectangle([40, 480, 200, 900], fill=(40, 36, 32))
    d.line([(0, 980), (700, 900)], fill=SOOT, width=6)
    d.line([(0, 1040), (760, 940)], fill=SOOT, width=4)
    d.polygon([(560, 820), (860, 780), (900, 900), (540, 940)], fill=(100, 80, 60), outline=INK)
    fig(d, 980, 700, 180, INK, 10)
    d.line([(1040, 760), (1120, 700)], fill=INK, width=3)
    for i in range(6):
        x = 1100 + i * 90
        fig(d, x, 800, 200, SOOT if i % 2 else INK, 14)
        d.ellipse([x + 20, 860, x + 70, 920], outline=MID, width=2)
    for i in range(180):
        x = rng.randrange(1728)
        y = rng.randrange(1000)
        d.line([(x, y), (x - 18, y + 46)], fill=(210, 210, 200), width=1)


def scene_escort(im, d, rng):
    d.rectangle([0, 0, 1728, 420], fill=(168, 186, 188))
    d.polygon([(0, 420), (1728, 360), (1728, 1152), (0, 1152)], fill=(126, 118, 78))
    d.polygon([(0, 500), (600, 460), (900, 520), (0, 640)], fill=(90, 120, 130))
    d.rectangle([80, 560, 280, 760], fill=(100, 78, 60), outline=INK, width=3)
    d.polygon([(70, 560), (180, 470), (290, 560)], fill=(70, 52, 40), outline=INK)
    d.rectangle([300, 500, 520, 740], fill=(140, 112, 82), outline=INK, width=3)
    for i in range(5):
        x = 80 + i * 70
        d.polygon([(x, 860), (x + 40, 800), (x + 90, 860), (x + 50, 900)], outline=INK)
    d.rectangle([700, 620, 1040, 860], fill=(104, 90, 58), outline=RUST, width=3)
    for r in range(5):
        y = 650 + r * 40
        for c in range(8):
            d.ellipse([730 + c * 36, y, 748 + c * 36, y + 16], fill=(150, 90, 60), outline=INK)
    cx, cy, rx, ry = 860, 760, 520, 280
    for i in range(28):
        ang = i / 28 * 6.283
        x = int(cx + rx * __import__("math").cos(ang))
        y = int(cy + ry * __import__("math").sin(ang) * 0.72)
        if 200 < x < 1600 and 430 < y < 1080:
            fig(d, x, y, 70, SOOT if i % 3 else INK, 0)
            d.rectangle([x - 8, y - 28, x + 8, y - 8], outline=INK)


def scene_leave(im, d, rng):
    d.rectangle([0, 0, 1728, 700], fill=(92, 86, 96))
    d.rectangle([0, 700, 1728, 1152], fill=(70, 60, 50))
    d.rectangle([40, 80, 520, 780], fill=(120, 100, 82), outline=INK, width=4)
    for i in range(4):
        d.rectangle([80, 140 + i * 140, 460, 250 + i * 140], fill=PAPER, outline=RUST, width=3)
        for k in range(4):
            squiggle(d, 110, 170 + i * 140 + k * 18, 30, MID, 2, 8)
    d.rectangle([40, 800, 420, 1120], fill=(50, 42, 36))
    for i, x in enumerate([120, 220, 320]):
        fig(d, x, 900, 180, PAPER, 0, skirt=True)
    d.polygon([(620, 860), (1100, 800), (1160, 980), (640, 1040)], fill=(48, 44, 40), outline=INK)
    d.polygon([(700, 820), (1040, 780), (1060, 700), (720, 740)], fill=(70, 64, 58), outline=INK)
    d.ellipse([700, 980, 820, 1100], outline=INK, width=4)
    d.ellipse([980, 940, 1100, 1060], outline=INK, width=4)
    for i, x in enumerate([1280, 1460, 1620]):
        d.ellipse([x - 40, 860, x + 70, 1000], outline=INK, width=3)
        d.line([(x + 50, 900), (x + 90, 820)], fill=INK, width=3)
        fig(d, x, 760, 120, RUST if i == 1 else INK, 4)
        d.polygon([(x - 10, 640), (x + 8, 600), (x + 18, 650)], outline=OCHRE)


SCENES = {
    "01": scene_ledger,
    "02": scene_road,
    "03": scene_walkoff,
    "04": scene_shutters,
    "05": scene_hall,
    "06": scene_rain,
    "07": scene_escort,
    "08": scene_leave,
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
