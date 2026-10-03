#!/usr/bin/env python3
"""Chapter 20 panels. Idempotent: keep a jpg already over 80kb."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib, random

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
NAMES = [
    "01-whitehall-sheet.jpg",
    "02-tudor-corridor.jpg",
    "03-disbanded-steps.jpg",
    "04-haifa-landing.jpg",
    "05-quay-word.jpg",
    "06-compound-before.jpg",
    "07-folded-in.jpg",
    "08-district-desk.jpg",
]
INK = (42, 34, 24)
RUST = (107, 58, 42)
MID = (90, 70, 50)
SOOT = (55, 46, 38)
PAPER = (237, 228, 212)
OCHRE = (186, 154, 104)


def grain(im, rng):
    px = im.load()
    w, h = im.size
    for _ in range(160000):
        x, y = rng.randrange(w), rng.randrange(h)
        v = rng.randint(-20, 14)
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


def seated(d, x, y, h, ink):
    r = max(8, h // 8)
    d.ellipse([x - r, y - 2 * r, x + r, y], outline=ink, width=2)
    d.line([(x, y), (x, y + h // 2)], fill=ink, width=3)
    d.line([(x, y + h // 5), (x + h // 3, y + h // 4)], fill=ink, width=2)
    d.line([(x, y + h // 2), (x + h // 3, y + h // 2)], fill=ink, width=2)
    d.line([(x + h // 3, y + h // 2), (x + h // 3, y + h)], fill=ink, width=2)
    d.line([(x, y + h // 2), (x - h // 8, y + h)], fill=ink, width=2)


def sheet(d, box, ink=INK):
    d.rectangle(box, fill=(224, 214, 196), outline=ink, width=2)
    x0, y0, x1, y1 = box
    for i in range(6):
        yy = y0 + 18 + i * ((y1 - y0 - 36) / 6)
        d.line([(x0 + 16, yy), (x1 - 16, yy)], fill=MID, width=1)


def scene_01(d, rng):
    d.rectangle([0, 0, 1728, 420], fill=(168, 150, 124))
    d.polygon([(80, 420), (80, 80), (520, 80), (520, 420)], outline=INK, width=4)
    for i in range(4):
        d.rectangle([120 + i * 90, 140, 190 + i * 90, 360], outline=INK, width=2)
    d.rectangle([0, 700, 1728, 1152], fill=(150, 132, 108))
    d.polygon([(380, 760), (1500, 820), (1560, 1080), (280, 1040)], fill=(120, 100, 78), outline=INK)
    sheet(d, (620, 860, 1180, 1040))
    seated(d, 980, 780, 200, INK)
    d.ellipse([1280, 740, 1360, 820], outline=RUST, width=3)


def scene_02(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(176, 160, 136))
    d.polygon([(860, 80), (80, 1070), (1648, 1070)], outline=INK)
    for i in range(6):
        y = 200 + i * 140
        span = 80 + i * 90
        d.line([(860 - span, y), (860 + span, y)], fill=MID, width=2)
    fig(d, 860, 620, 280, INK, lean=12)
    d.polygon([(980, 760), (1120, 760), (1100, 900), (960, 900)], fill=(224, 214, 196), outline=RUST, width=3)


def scene_03(d, rng):
    d.rectangle([0, 0, 1728, 640], fill=(188, 176, 156))
    d.rectangle([0, 640, 1728, 1152], fill=(130, 114, 92))
    d.rectangle([60, 180, 980, 700], outline=INK, width=5)
    for i in range(8):
        d.line([(100, 240 + i * 40), (160, 240 + i * 40)], fill=INK, width=3)
    d.rectangle([1040, 260, 1660, 700], outline=INK, width=4)
    d.polygon([(1040, 260), (1350, 120), (1660, 260)], outline=INK, width=3)
    for i in range(7):
        fig(d, 180 + i * 110, 760, 180 + (i % 3) * 16, MID if i % 2 else INK, lean=rng.randint(-4, 4))
    for i in range(4):
        d.ellipse([1180 + i * 90, 820, 1250 + i * 90, 900], outline=RUST, width=2)


def scene_04(d, rng):
    d.rectangle([0, 0, 1728, 620], fill=(196, 176, 146))
    d.rectangle([0, 620, 1728, 1152], fill=(92, 86, 74))
    d.polygon([(80, 700), (980, 640), (1040, 860), (60, 900)], fill=(70, 62, 52), outline=INK, width=4)
    d.rectangle([200, 480, 280, 700], fill=SOOT, outline=INK, width=2)
    d.line([(160, 700), (700, 980)], fill=INK, width=4)
    for i in range(14):
        fig(d, 220 + i * 36, 760 + (i % 4) * 18, 90, INK if i % 3 else RUST, lean=8)
    d.rectangle([1100, 860, 1680, 1040], fill=(140, 122, 98), outline=INK, width=3)


def scene_05(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(210, 190, 156))
    for i in range(5):
        x = 40 + i * 340
        h = 420 + (i % 3) * 80
        d.rectangle([x, 180, x + 300, 180 + h], outline=INK, width=4)
        d.arc([x + 40, 280, x + 260, 520], 0, 180, fill=RUST, width=3)
        d.rectangle([x + 90, 400, x + 210, 180 + h], fill=(150, 120, 90), outline=INK, width=2)
    for i in range(9):
        fig(d, 200 + i * 160, 860, 170, INK if i < 5 else MID, lean=-6)


def scene_06(d, rng):
    d.rectangle([40, 40, 1688, 1112], outline=INK, width=8)
    d.rectangle([80, 80, 1648, 1072], fill=(198, 180, 150))
    d.rectangle([720, 860, 1000, 1072], fill=SOOT, outline=INK, width=4)
    for row in range(3):
        for col in range(8):
            fig(d, 180 + col * 170, 220 + row * 220, 120, INK if (row + col) % 2 == 0 else MID, lean=0)
    d.line([(120, 140), (1600, 140)], fill=RUST, width=2)


def scene_07(d, rng):
    d.rectangle([0, 0, 700, 1152], fill=(170, 154, 130))
    d.rectangle([700, 0, 1728, 1152], fill=(120, 104, 86))
    d.rectangle([760, 280, 1120, 1040], fill=(40, 34, 28), outline=INK, width=5)
    for i in range(8):
        fig(d, 160 + i * 60, 640, 200, RUST if i % 2 == 0 else INK, lean=18)
    for i in range(5):
        fig(d, 1240 + i * 80, 700, 180, MID, lean=0)
    d.rectangle([1180, 180, 1600, 420], outline=INK, width=3)


def scene_08(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(48, 40, 32))
    d.rectangle([120, 80, 900, 700], outline=OCHRE, width=3)
    d.polygon([(200, 620), (300, 200), (480, 260), (620, 180), (760, 420), (500, 640)], outline=OCHRE, width=2)
    d.rectangle([980, 620, 1600, 1000], fill=(70, 58, 46), outline=OCHRE, width=3)
    sheet(d, (1060, 700, 1500, 920), ink=OCHRE)
    fig(d, 1280, 480, 220, OCHRE, lean=-8)
    d.ellipse([200, 140, 280, 220], outline=OCHRE, width=2)


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
    for i in range(0, 1728, 17):
        d.line([(i, 0), (i - 180, 1152)], fill=(206, 190, 168), width=1)
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
