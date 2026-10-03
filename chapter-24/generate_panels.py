#!/usr/bin/env python3
"""Chapter 24 panels. Idempotent: keep a jpg already over 80kb."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib, random

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
NAMES = [
    "01-cairo-letter.jpg",
    "02-hussein-hands.jpg",
    "03-revolt-ridge.jpg",
    "04-london-zones.jpg",
    "05-archive-sheets.jpg",
    "06-balfour-note.jpg",
    "07-cyprus-house.jpg",
    "08-amman-parcels.jpg",
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


def seated(d, x, y, h, ink):
    r = max(8, h // 8)
    d.ellipse([x - r, y - 2 * r, x + r, y], outline=ink, width=2)
    d.line([(x, y), (x, y + h // 2)], fill=ink, width=3)
    d.line([(x, y + h // 5), (x + h // 3, y + h // 4)], fill=ink, width=2)
    d.line([(x, y + h // 2), (x + h // 3, y + h // 2)], fill=ink, width=2)
    d.line([(x + h // 3, y + h // 2), (x + h // 3, y + h)], fill=ink, width=2)
    d.line([(x, y + h // 2), (x - h // 8, y + h)], fill=ink, width=2)


def scene_01(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(168, 148, 118))
    arch(d, 80, 60, 420, 900, INK, 8)
    d.rectangle([140, 400, 440, 900], fill=(196, 176, 146))
    d.rectangle([620, 520, 1500, 980], fill=(112, 94, 74), outline=INK, width=6)
    sheet(d, (760, 250, 1100, 900), rows=16)
    seated(d, 1280, 620, 280, INK)
    d.polygon([(1520, 160), (1660, 220), (1600, 420), (1460, 360), (1480, 240)], outline=RUST, width=3)


def scene_02(d, rng):
    d.rectangle([0, 0, 1728, 420], fill=(186, 154, 104))
    d.rectangle([0, 420, 1728, 1152], fill=(120, 100, 78))
    for i in range(6):
        d.rectangle([40 + i * 280, 80, 260 + i * 280, 520], outline=INK, width=4)
        d.arc([60 + i * 280, 40, 240 + i * 280, 220], 200, 340, fill=INK, width=3)
    d.ellipse([760, 80, 980, 280], outline=OCHRE, width=4)
    d.line([(520, 780), (700, 640)], fill=INK, width=5)
    d.line([(1200, 780), (1020, 640)], fill=INK, width=5)
    fig(d, 420, 620, 280, MID, lean=8)
    fig(d, 1300, 620, 280, INK, lean=-8)
    sheet(d, (680, 560, 1060, 820), rows=5)


def scene_03(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(176, 160, 132))
    d.polygon([(0, 900), (300, 420), (700, 760), (1100, 280), (1500, 640), (1728, 500), (1728, 1152), (0, 1152)], fill=(110, 92, 70))
    d.polygon([(0, 980), (400, 700), (900, 1000), (1400, 620), (1728, 860), (1728, 1152), (0, 1152)], fill=(78, 66, 52))
    for i in range(14):
        fig(d, 80 + i * 115, 520 + (i % 3) * 30, 90, OCHRE if i % 2 == 0 else INK, lean=6)
    d.ellipse([80, 60, 220, 200], outline=MID, width=2)


def scene_04(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(150, 140, 126))
    for i in range(5):
        d.rectangle([80 + i * 320, 40, 360 + i * 320, 280], outline=INK, width=3)
    d.rectangle([160, 360, 1560, 980], fill=(214, 204, 186), outline=INK, width=5)
    d.rectangle([180, 380, 860, 960], fill=(186, 154, 104))
    d.rectangle([860, 380, 1280, 700], fill=(55, 46, 38))
    d.polygon([(1280, 380), (1540, 380), (1540, 960), (1100, 960)], fill=(107, 58, 42))
    d.line([(860, 380), (860, 960)], fill=INK, width=3)
    fig(d, 240, 200, 160, INK, lean=0)
    fig(d, 1480, 200, 170, MID, lean=0)


def scene_05(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(132, 116, 96))
    for i in range(4):
        for k in range(3):
            d.rectangle([80 + i * 200, 80 + k * 160, 240 + i * 200, 210 + k * 160], outline=INK, width=3)
    for i in range(6):
        x = 980 + i * 30
        y = 180 + i * 40
        d.polygon([(x, y), (x + 280, y + 40), (x + 240, y + 380), (x - 40, y + 340)], fill=(224, 214, 196), outline=INK)
    fig(d, 900, 700, 240, INK, lean=-6)
    fig(d, 1400, 740, 220, RUST, lean=8)


def scene_06(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(92, 78, 64))
    d.ellipse([180, 80, 520, 420], outline=OCHRE, width=6)
    d.rectangle([200, 640, 1500, 1040], fill=(120, 100, 78), outline=INK, width=5)
    sheet(d, (760, 700, 1040, 980), rows=4)
    seated(d, 1180, 520, 300, OCHRE)
    d.rectangle([40, 200, 120, 1000], fill=SOOT)
    d.rectangle([1600, 200, 1680, 1000], fill=SOOT)


def scene_07(d, rng):
    d.rectangle([0, 0, 1728, 640], fill=(186, 170, 140))
    d.rectangle([0, 640, 1728, 1152], fill=(78, 98, 108))
    d.rectangle([180, 260, 780, 760], outline=INK, width=6)
    d.polygon([(180, 260), (480, 80), (780, 260)], outline=INK, width=5)
    d.rectangle([400, 460, 560, 760], fill=SOOT)
    fig(d, 480, 500, 120, OCHRE, lean=0)
    d.polygon([(1100, 700), (1500, 640), (1560, 800), (1140, 860)], fill=SOOT, outline=INK)
    d.rectangle([1280, 480, 1360, 680], fill=INK)
    d.ellipse([80, 80, 200, 200], outline=RUST, width=3)


def scene_08(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(196, 180, 154))
    d.rectangle([80, 80, 1100, 700], outline=INK, width=4)
    d.polygon([(140, 180), (320, 140), (380, 320), (180, 360)], outline=RUST, width=3)
    d.polygon([(460, 220), (700, 160), (760, 340), (520, 400)], outline=SOOT, width=3)
    d.polygon([(200, 420), (480, 400), (520, 580), (220, 620)], outline=INK, width=3)
    d.ellipse([820, 200, 1020, 480], outline=MID, width=3)
    d.rectangle([1240, 280, 1560, 980], outline=INK, width=5)
    d.arc([1240, 140, 1560, 520], 200, 340, fill=INK, width=5)
    d.rectangle([0, 860, 1728, 1152], fill=(140, 122, 100))


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
