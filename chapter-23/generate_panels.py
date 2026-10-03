#!/usr/bin/env python3
"""Chapter 23 panels. Idempotent: keep a jpg already over 80kb."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib, random

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
NAMES = [
    "01-haifa-quay.jpg",
    "02-inspector-kit.jpg",
    "03-baton-lane.jpg",
    "04-dismissal-desk.jpg",
    "05-swollen-yard.jpg",
    "06-telegram-house.jpg",
    "07-screen-alley.jpg",
    "08-mandate-gate.jpg",
]
INK = (42, 34, 24)
RUST = (107, 58, 42)
MID = (90, 70, 50)
SOOT = (55, 46, 38)
PAPER = (237, 228, 212)
OCHRE = (186, 154, 104)
STONE = (168, 150, 124)


def grain(im, rng):
    px = im.load()
    w, h = im.size
    for _ in range(140000):
        x, y = rng.randrange(w), rng.randrange(h)
        v = rng.randint(-22, 16)
        r, g, b = px[x, y]
        px[x, y] = (
            max(0, min(255, r + v)),
            max(0, min(255, g + v // 2)),
            max(0, min(255, b + v // 3)),
        )


def fig(d, x, y, h, ink, lean=0):
    r = max(7, h // 9)
    d.ellipse([x - r, y - 2 * r, x + r, y], outline=ink, width=2)
    d.line([(x, y), (x + lean, y + h // 2)], fill=ink, width=3)
    d.line([(x + lean, y + h // 2), (x - h // 6, y + h)], fill=ink, width=2)
    d.line([(x + lean, y + h // 2), (x + h // 6, y + h)], fill=ink, width=2)
    d.line([(x, y + h // 5), (x - h // 5, y + h // 3)], fill=ink, width=2)
    d.line([(x, y + h // 5), (x + h // 5, y + h // 3)], fill=ink, width=2)


def sheet(d, box, ink=INK, rows=7):
    d.rectangle(box, fill=(224, 214, 196), outline=ink, width=2)
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0 - 36)
    for i in range(rows):
        yy = y0 + 18 + i * (span / max(1, rows))
        d.line([(x0 + 14, yy), (x1 - 14, yy)], fill=MID, width=1)


def arch(d, x, y, w, h, ink=INK, width=4):
    d.arc([x, y, x + w, y + h], 180, 360, fill=ink, width=width)
    d.line([(x, y + h // 2), (x, y + h)], fill=ink, width=width)
    d.line([(x + w, y + h // 2), (x + w, y + h)], fill=ink, width=width)


def scene_01(d, rng):
    d.rectangle([0, 0, 1728, 620], fill=(196, 168, 122))
    d.rectangle([0, 620, 1728, 1152], fill=(78, 92, 98))
    d.polygon([(180, 640), (1480, 560), (1560, 760), (220, 820)], fill=(62, 54, 46), outline=INK)
    d.rectangle([980, 300, 1080, 580], fill=SOOT, outline=INK, width=3)
    d.line([(1080, 340), (1280, 250)], fill=MID, width=2)
    d.line([(220, 780), (80, 980)], fill=OCHRE, width=4)
    d.line([(420, 800), (260, 1020)], fill=OCHRE, width=3)
    d.rectangle([0, 900, 1728, 1152], fill=(126, 112, 90))
    for i in range(5):
        fig(d, 360 + i * 150, 860, 170, INK if i == 2 else MID, lean=8)
    d.ellipse([80, 80, 220, 220], outline=RUST, width=3)


def scene_02(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(150, 132, 110))
    arch(d, 180, 80, 520, 700, INK, 6)
    d.rectangle([220, 420, 660, 760], fill=(196, 176, 148))
    d.rectangle([900, 620, 1580, 900], fill=(112, 92, 70), outline=INK, width=5)
    fig(d, 1180, 340, 300, INK, lean=0)
    d.line([(1260, 500), (1500, 820)], fill=RUST, width=8)
    d.ellipse([1460, 780, 1540, 860], outline=RUST, width=4)
    cx, cy = 1040, 760
    for k in range(5):
        rr = 18 + k * 16
        d.arc([cx - rr, cy - rr // 2, cx + rr, cy + rr // 2], 200, 520, fill=INK, width=3)
    d.ellipse([980, 700, 1120, 780], fill=SOOT)


def scene_03(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(176, 156, 128))
    d.polygon([(0, 0), (520, 0), (700, 1152), (0, 1152)], fill=(120, 104, 84))
    d.polygon([(1100, 0), (1728, 0), (1728, 1152), (900, 1152)], fill=(132, 114, 92))
    for col in range(4):
        for row in range(8):
            x0 = 30 + col * 120 + (20 if row % 2 else 0)
            y0 = 40 + row * 140
            d.rectangle([x0, y0, x0 + 90, y0 + 100], outline=SOOT, width=2)
            x1 = 1240 + col * 110
            d.rectangle([x1, y0 + 20, x1 + 80, y0 + 120], outline=SOOT, width=2)
    fig(d, 860, 420, 420, INK, lean=12)
    d.line([(980, 620), (1180, 980)], fill=RUST, width=8)
    d.ellipse([1148, 940, 1220, 1010], outline=RUST, width=4)
    d.rectangle([0, 1000, 1728, 1152], fill=(96, 82, 64))


def scene_04(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(210, 196, 170))
    d.rectangle([160, 280, 1100, 860], fill=(128, 108, 86), outline=INK, width=6)
    sheet(d, (280, 380, 980, 760), rows=8)
    d.rectangle([1180, 300, 1500, 980], outline=INK, width=5)
    d.arc([1180, 180, 1500, 520], 200, 340, fill=INK, width=5)
    d.line([(1240, 300), (1240, 860)], fill=RUST, width=6)
    d.rectangle([1560, 360, 1700, 980], fill=SOOT)
    fig(d, 1630, 520, 200, OCHRE, lean=10)


def scene_05(d, rng):
    d.rectangle([0, 0, 1728, 460], fill=(188, 160, 112))
    d.rectangle([0, 460, 1728, 1152], fill=(138, 122, 92))
    for i in range(4):
        x = 40 + i * 420
        d.polygon([(x, 300), (x + 180, 120), (x + 360, 300)], fill=(110, 92, 72), outline=INK)
        d.rectangle([x, 300, x + 360, 430], outline=INK, width=3)
    d.line([(0, 500), (1728, 500)], fill=INK, width=3)
    for row in range(3):
        for i in range(8):
            lean = -4 if row == 1 else 6
            fig(d, 140 + i * 190, 540 + row * 180, 140, INK if (i + row) % 3 == 0 else MID, lean=lean)


def scene_06(d, rng):
    d.rectangle([0, 0, 860, 1152], fill=(214, 202, 182))
    d.rectangle([860, 0, 1728, 1152], fill=(92, 78, 62))
    d.line([(860, 0), (860, 1152)], fill=RUST, width=6)
    sheet(d, (120, 180, 740, 980), rows=14)
    d.ellipse([300, 60, 420, 150], outline=OCHRE, width=3)
    d.polygon([(980, 860), (1120, 420), (1280, 860)], fill=(70, 58, 46), outline=OCHRE)
    d.rectangle([1040, 620, 1220, 860], fill=(40, 32, 26))
    d.rectangle([1100, 280, 1680, 860], outline=OCHRE, width=4)
    d.polygon([(1100, 280), (1390, 80), (1680, 280)], outline=OCHRE, width=4)
    d.rectangle([1320, 520, 1500, 860], fill=(28, 22, 18))
    d.rectangle([900, 900, 1728, 1152], fill=(48, 40, 32))


def scene_07(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(176, 154, 120))
    d.rectangle([0, 80, 1728, 560], fill=(120, 104, 84), outline=INK, width=4)
    for col in range(12):
        for row in range(4):
            x = col * 150 + (40 if row % 2 else 0)
            y = 100 + row * 110
            d.rectangle([x, y, x + 120, y + 90], outline=(70, 58, 46), width=2)
    d.rectangle([620, 470, 900, 860], fill=(224, 214, 196), outline=INK, width=4)
    d.line([(620, 600), (900, 600)], fill=MID, width=2)
    d.line([(620, 730), (900, 730)], fill=MID, width=2)
    for i in range(4):
        fig(d, 220 + i * 100, 700, 200, INK if i % 2 == 0 else RUST, lean=0)
    d.polygon([(1180, 560), (1728, 640), (1728, 1152), (1280, 1152)], fill=(206, 184, 140))
    d.rectangle([0, 980, 1180, 1152], fill=(110, 96, 78))


def scene_08(d, rng):
    d.rectangle([0, 0, 1728, 720], fill=(172, 156, 132))
    d.rectangle([0, 720, 1728, 1152], fill=(196, 176, 140))
    arch(d, 360, 80, 1000, 900, INK, 10)
    d.rectangle([700, 420, 1020, 1000], fill=(48, 40, 32))
    for i in range(6):
        fig(d, 180 + i * 90, 780, 160, MID, lean=-8)
        d.line([(210 + i * 90, 900), (250 + i * 90, 1040)], fill=RUST, width=4)
    d.rectangle([1180, 860, 1680, 1040], fill=(210, 196, 168), outline=INK, width=2)
    d.line([(1220, 980), (1640, 900)], fill=OCHRE, width=3)


SCENES = {
    "01": scene_01,
    "02": scene_02,
    "03": scene_03,
    "04": scene_04,
    "05": scene_05,
    "06": scene_06,
    "07": scene_07,
    "08": scene_08,
}


def synth(name):
    rng = random.Random(int(hashlib.md5(name.encode()).hexdigest()[:8], 16))
    im = Image.new("RGB", (1728, 1152), PAPER)
    d = ImageDraw.Draw(im)
    SCENES[name[:2]](d, rng)
    for i in range(0, 1728, 19):
        d.line([(i, 0), (i - 160, 1152)], fill=(206, 190, 168), width=1)
    grain(im, rng)
    return im.filter(ImageFilter.SMOOTH)


def main():
    for name in NAMES:
        path = root / name
        if path.exists() and path.stat().st_size > 80000:
            print("keep", path, path.stat().st_size)
            continue
        synth(name).save(path, "JPEG", quality=86, optimize=True)
        print("synth", path, path.stat().st_size)


if __name__ == "__main__":
    main()
