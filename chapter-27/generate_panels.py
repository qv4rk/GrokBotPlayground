#!/usr/bin/env python3
"""Chapter 27 panels. Idempotent: keep a jpg already over 80kb."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib, random

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
NAMES = [
    "01-manshiyya-balcony.jpg",
    "02-canal-offices.jpg",
    "03-tanker-cut.jpg",
    "04-sevres-villa.jpg",
    "05-kept-receipt.jpg",
    "06-port-said-drop.jpg",
    "07-scuttled-ditch.jpg",
    "08-washington-desk.jpg",
]
INK = (42, 34, 24)
RUST = (107, 58, 42)
MID = (90, 70, 50)
SOOT = (55, 46, 38)
PAPER = (237, 228, 212)
OCHRE = (186, 154, 104)
STONE = (168, 150, 124)
PALE = (224, 214, 196)


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


def seated(d, x, y, h, ink):
    r = max(8, h // 8)
    d.ellipse([x - r, y - 2 * r, x + r, y], outline=ink, width=2)
    d.line([(x, y), (x, y + h // 2)], fill=ink, width=3)
    d.line([(x, y + h // 5), (x + h // 3, y + h // 4)], fill=ink, width=2)
    d.line([(x, y + h // 2), (x + h // 4, y + int(h * 0.55))], fill=ink, width=2)
    d.line([(x + h // 4, y + int(h * 0.55)), (x + h // 3, y + h)], fill=ink, width=2)
    d.line([(x, y + h // 2), (x - h // 7, y + h)], fill=ink, width=2)


def sheet(d, box, rows=6, fill=PALE):
    d.rectangle(box, fill=fill, outline=INK, width=2)
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0 - 24)
    for i in range(rows):
        yy = y0 + 14 + i * (span / max(1, rows))
        d.line([(x0 + 10, yy), (x1 - 10, yy)], fill=MID, width=1)


def scene_01(d, rng):
    d.rectangle([0, 0, 1728, 480], fill=(196, 168, 120))
    d.rectangle([0, 480, 1728, 1152], fill=(150, 132, 108))
    d.rectangle([40, 200, 520, 980], fill=STONE, outline=INK, width=6)
    for i in range(4):
        d.rectangle([80 + i * 100, 280, 150 + i * 100, 460], outline=INK, width=3)
    d.rectangle([40, 620, 560, 700], fill=(120, 100, 80), outline=INK, width=4)
    fig(d, 280, 500, 160, INK, lean=0)
    d.ellipse([80, 60, 220, 200], outline=RUST, width=4)
    for i in range(16):
        fig(d, 640 + (i % 8) * 130, 620 + (i // 8) * 200, 90, SOOT if i % 2 == 0 else MID, lean=rng.randint(-6, 6))


def scene_02(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(36, 32, 28))
    d.rectangle([60, 280, 480, 1000], fill=(70, 60, 50), outline=OCHRE, width=4)
    d.rectangle([180, 760, 300, 1000], fill=(20, 18, 16))
    fig(d, 240, 680, 140, OCHRE, lean=0)
    d.rectangle([560, 120, 900, 1000], fill=(90, 74, 58), outline=PALE, width=4)
    d.rectangle([680, 700, 800, 1000], fill=(20, 18, 16))
    fig(d, 740, 600, 160, PALE, lean=4)
    d.rectangle([1040, 420, 1640, 1000], fill=(60, 52, 44), outline=RUST, width=4)
    d.polygon([(1040, 420), (1340, 220), (1640, 420)], outline=RUST, width=4)
    d.rectangle([1280, 720, 1420, 1000], fill=(20, 18, 16))
    fig(d, 1350, 620, 150, OCHRE, lean=-4)
    d.ellipse([200, 80, 280, 160], outline=OCHRE, width=2)


def scene_03(d, rng):
    d.rectangle([0, 0, 1728, 360], fill=(186, 154, 104))
    d.rectangle([0, 800, 1728, 1152], fill=(176, 148, 100))
    d.rectangle([0, 360, 1728, 800], fill=(70, 90, 96))
    for i in range(3):
        y = 400 + i * 120
        d.polygon([(80, y), (1500, y - 20), (1520, y + 50), (100, y + 70)], fill=SOOT, outline=INK)
        d.rectangle([1180, y - 50, 1260, y + 10], fill=RUST)
    d.ellipse([200, 80, 340, 220], outline=INK, width=3)


def scene_04(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(168, 176, 140))
    d.ellipse([80, 200, 280, 500], fill=(90, 110, 70), outline=INK, width=3)
    d.ellipse([1500, 180, 1680, 460], fill=(90, 110, 70), outline=INK, width=3)
    d.polygon([(360, 420), (860, 140), (1360, 420)], fill=(120, 90, 70), outline=INK)
    d.rectangle([360, 420, 1360, 980], fill=(196, 180, 154), outline=INK, width=5)
    d.rectangle([460, 500, 620, 700], fill=(48, 60, 70), outline=INK, width=3)
    d.rectangle([1100, 500, 1260, 700], fill=(48, 60, 70), outline=INK, width=3)
    d.rectangle([520, 740, 1200, 960], fill=(96, 80, 62), outline=INK, width=4)
    sheet(d, (740, 780, 980, 920), rows=4)
    for i, x in enumerate((580, 720, 900, 1080)):
        seated(d, x, 620, 140, INK)
    for i, x in enumerate((640, 860, 1080)):
        fig(d, x, 860, 80, RUST, lean=0)


def scene_05(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(140, 126, 108))
    d.line([(576, 40), (576, 1110)], fill=INK, width=3)
    d.line([(1152, 40), (1152, 1110)], fill=INK, width=3)
    fig(d, 280, 360, 420, INK, lean=0)
    d.polygon([(180, 620), (400, 600), (420, 860), (160, 900)], fill=SOOT, outline=INK)
    sheet(d, (240, 700, 360, 820), rows=3)
    d.rectangle([700, 420, 1040, 860], fill=(40, 34, 30), outline=OCHRE, width=6)
    fig(d, 860, 280, 200, OCHRE, lean=0)
    sheet(d, (1280, 240, 1560, 420), rows=4)
    sheet(d, (1320, 400, 1600, 580), rows=4, fill=(210, 196, 170))
    fig(d, 1400, 620, 320, RUST, lean=-8)


def scene_06(d, rng):
    d.rectangle([0, 0, 1728, 780], fill=(176, 164, 140))
    d.rectangle([0, 780, 1728, 1152], fill=(90, 78, 64))
    for i, x in enumerate((180, 460, 780, 1100, 1420)):
        d.arc([x, 80 + (i % 2) * 40, x + 220, 360 + (i % 2) * 40], 200, 340, fill=OCHRE, width=5)
        d.line([(x + 20, 220), (x + 110, 700)], fill=INK, width=2)
        d.line([(x + 200, 220), (x + 110, 700)], fill=INK, width=2)
        fig(d, x + 110, 680, 70, INK, lean=0)
    for i in range(4):
        d.rectangle([200 + i * 360, 860, 420 + i * 360, 1080], outline=SOOT, width=4)
    d.polygon([(900, 900), (980, 620), (1060, 900)], fill=(70, 60, 52))


def scene_07(d, rng):
    d.rectangle([0, 0, 1728, 280], fill=(186, 154, 104))
    d.rectangle([0, 860, 1728, 1152], fill=(160, 132, 90))
    d.rectangle([0, 280, 1728, 860], fill=(48, 62, 68))
    d.polygon([(120, 420), (700, 300), (760, 520), (180, 700)], fill=SOOT, outline=INK)
    d.polygon([(820, 500), (1400, 360), (1480, 640), (900, 780)], fill=(30, 28, 26), outline=RUST)
    d.polygon([(200, 240), (900, 200), (980, 360), (40, 520)], outline=INK, width=6)
    d.line([(200, 240), (40, 520)], fill=INK, width=4)
    d.line([(900, 200), (980, 360)], fill=INK, width=4)
    for i in range(6):
        d.line([(220 + i * 110, 230), (80 + i * 140, 500)], fill=MID, width=2)


def scene_08(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(214, 204, 186))
    d.rectangle([80, 60, 700, 520], fill=(168, 186, 190), outline=INK, width=6)
    d.line([(390, 60), (390, 520)], fill=INK, width=4)
    d.rectangle([180, 700, 980, 1080], fill=(96, 80, 62), outline=INK, width=6)
    seated(d, 420, 560, 240, INK)
    d.rectangle([620, 760, 900, 860], fill=SOOT, outline=OCHRE, width=3)
    d.arc([680, 700, 820, 820], 200, 20, fill=OCHRE, width=4)
    d.line([(760, 760), (860, 700)], fill=OCHRE, width=4)
    d.rectangle([1120, 640, 1600, 1080], fill=(70, 62, 54), outline=INK, width=4)
    d.rectangle([1280, 480, 1460, 760], outline=RUST, width=5)
    sheet(d, (1180, 760, 1520, 980), rows=5, fill=(200, 190, 170))


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
    rng = random.Random(int(hashlib.md5(("ch27-" + name).encode()).hexdigest()[:8], 16))
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
