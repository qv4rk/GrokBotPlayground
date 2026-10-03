#!/usr/bin/env python3
"""Chapter 25 panels. Idempotent: keep a jpg already over 80kb."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib, random

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
NAMES = [
    "01-two-letters.jpg",
    "02-euston-train.jpg",
    "03-holyhead-hull.jpg",
    "04-barton-holdout.jpg",
    "05-treaty-lamp.jpg",
    "06-collins-dawn.jpg",
    "07-earlsfort-house.jpg",
    "08-beal-na-blath.jpg",
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


def sheet(d, box, ink=INK, rows=7, fill=PALE):
    d.rectangle(box, fill=fill, outline=ink, width=2)
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0 - 28)
    for i in range(rows):
        yy = y0 + 16 + i * (span / max(1, rows))
        d.line([(x0 + 12, yy), (x1 - 12, yy)], fill=MID, width=1)


def seated(d, x, y, h, ink):
    r = max(8, h // 8)
    d.ellipse([x - r, y - 2 * r, x + r, y], outline=ink, width=2)
    d.line([(x, y), (x, y + h // 2)], fill=ink, width=3)
    d.line([(x, y + h // 5), (x + h // 3, y + h // 4)], fill=ink, width=2)
    d.line([(x, y + h // 2), (x + h // 4, y + int(h * 0.55))], fill=ink, width=2)
    d.line([(x + h // 4, y + int(h * 0.55)), (x + h // 3, y + h)], fill=ink, width=2)
    d.line([(x, y + h // 2), (x - h // 7, y + h)], fill=ink, width=2)


def scene_01(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(78, 66, 54))
    d.rectangle([0, 0, 1728, 180], fill=(48, 40, 34))
    d.rectangle([90, 40, 300, 160], outline=OCHRE, width=3)
    d.rectangle([1420, 36, 1630, 160], outline=OCHRE, width=3)
    fig(d, 160, 260, 300, OCHRE, lean=4)
    for i, x in enumerate((420, 640, 860, 1080, 1300)):
        seated(d, x, 430, 220, INK)
    d.rectangle([200, 760, 1580, 1100], fill=(96, 78, 58), outline=INK, width=6)
    sheet(d, (340, 800, 700, 1060), rows=11, fill=(232, 224, 208))
    d.polygon([(980, 830), (1320, 790), (1380, 1040), (1020, 1070)], fill=(168, 120, 92), outline=RUST)
    d.line([(980, 830), (1180, 960)], fill=RUST, width=4)
    for i in range(4):
        d.line([(1080, 880 + i * 36), (1300, 860 + i * 36)], fill=SOOT, width=2)


def scene_02(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(62, 54, 46))
    for i in range(6):
        x = -40 + i * 310
        d.arc([x, -40, x + 480, 520], 200, 340, fill=OCHRE, width=6)
    d.rectangle([0, 900, 1728, 1152], fill=(110, 96, 78))
    d.rectangle([80, 860, 1728, 910], fill=(48, 40, 34))
    d.rectangle([260, 560, 1180, 820], fill=SOOT, outline=INK, width=5)
    d.rectangle([1040, 400, 1280, 820], fill=(36, 30, 26), outline=INK, width=5)
    d.rectangle([1100, 280, 1200, 420], fill=INK)
    d.ellipse([1080, 140, 1220, 280], fill=(200, 186, 150), outline=OCHRE)
    d.ellipse([1160, 60, 1320, 200], outline=PALE, width=3)
    d.ellipse([340, 760, 500, 920], outline=OCHRE, width=6)
    d.ellipse([620, 760, 780, 920], outline=OCHRE, width=6)
    d.ellipse([900, 760, 1060, 920], outline=OCHRE, width=6)
    for i in range(4):
        fig(d, 80 + i * 50, 740, 110, PALE, lean=0)


def scene_03(d, rng):
    d.rectangle([0, 0, 1728, 420], fill=(150, 132, 108))
    d.rectangle([0, 420, 1728, 1152], fill=(48, 58, 62))
    for i in range(18):
        y = 480 + i * 36
        d.line([(0, y), (1728, y + 8)], fill=(70, 82, 86), width=2)
    d.polygon([(160, 520), (1280, 470), (1360, 620), (200, 680)], fill=SOOT, outline=INK)
    d.rectangle([860, 300, 960, 520], fill=RUST)
    d.line([(420, 280), (420, 520)], fill=INK, width=4)
    d.line([(420, 320), (620, 400)], fill=INK, width=2)
    d.rectangle([80, 560, 160, 980], fill=STONE, outline=INK, width=3)
    d.rectangle([200, 600, 260, 1000], fill=STONE, outline=INK, width=3)
    d.rectangle([300, 640, 360, 1040], fill=STONE, outline=INK, width=3)
    d.rectangle([1380, 300, 1680, 460], fill=STONE, outline=INK, width=4)
    fig(d, 1520, 220, 160, INK, lean=0)
    d.ellipse([120, 60, 260, 200], outline=OCHRE, width=3)


def scene_04(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(120, 104, 86))
    d.ellipse([500, 200, 1220, 980], outline=INK, width=2)
    seated(d, 860, 520, 360, INK)
    fig(d, 380, 400, 440, RUST, lean=28)
    fig(d, 1320, 380, 460, OCHRE, lean=-30)
    d.line([(500, 520), (720, 560)], fill=RUST, width=3)
    d.line([(1180, 520), (980, 560)], fill=OCHRE, width=3)
    d.polygon([(200, 860), (520, 780), (560, 1040), (160, 1100)], fill=PALE, outline=MID)
    d.line([(240, 900), (480, 860)], fill=SOOT, width=2)
    d.line([(250, 960), (470, 930)], fill=SOOT, width=2)


def scene_05(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(28, 24, 20))
    d.ellipse([520, 80, 1220, 780], fill=(186, 154, 104))
    d.ellipse([640, 180, 1100, 640], fill=(210, 186, 140))
    sheet(d, (360, 620, 1380, 980), rows=8, fill=(236, 228, 214))
    d.line([(200, 700), (420, 760)], fill=OCHRE, width=8)
    d.line([(1500, 680), (1280, 760)], fill=OCHRE, width=8)
    d.line([(700, 1100), (820, 900)], fill=PALE, width=7)
    d.ellipse([180, 660, 250, 730], outline=OCHRE, width=3)
    d.ellipse([1470, 640, 1540, 710], outline=OCHRE, width=3)
    d.ellipse([760, 1060, 840, 1140], outline=PALE, width=3)


def scene_06(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(168, 150, 124))
    d.rectangle([1040, 40, 1320, 900], fill=(214, 196, 160), outline=INK, width=8)
    d.line([(1180, 40), (1180, 900)], fill=INK, width=4)
    d.line([(1040, 460), (1320, 460)], fill=INK, width=4)
    for i in range(5):
        d.rectangle([1360, 200 + i * 90, 1680, 260 + i * 90], outline=MID, width=2)
    d.rectangle([140, 720, 900, 1080], fill=(96, 80, 62), outline=INK, width=5)
    seated(d, 360, 520, 280, INK)
    sheet(d, (520, 760, 820, 1000), rows=6, fill=(232, 224, 208))
    d.rectangle([0, 0, 80, 1152], fill=SOOT)


def scene_07(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(150, 136, 116))
    d.rectangle([0, 0, 1728, 280], fill=(70, 58, 48))
    d.line([(0, 280), (1728, 280)], fill=OCHRE, width=6)
    for i in range(22):
        fig(d, 60 + i * 76, 120, 70, OCHRE if i % 3 else PALE, lean=rng.randint(-4, 4))
    d.arc([180, 360, 1400, 1500], 200, 340, fill=INK, width=6)
    d.arc([280, 480, 1300, 1480], 200, 340, fill=MID, width=3)
    for i in range(6):
        fig(d, 260 + i * 70, 620, 150, RUST, lean=0)
    for i in range(8):
        seated(d, 700 + i * 80, 700, 120, INK)
    d.rectangle([1500, 420, 1680, 1000], fill=(40, 34, 28), outline=OCHRE, width=4)
    fig(d, 1560, 640, 160, PALE, lean=8)
    fig(d, 1630, 700, 140, OCHRE, lean=10)


def scene_08(d, rng):
    d.rectangle([0, 0, 1728, 520], fill=(176, 158, 126))
    d.polygon([(0, 520), (400, 260), (900, 480), (1400, 200), (1728, 420), (1728, 1152), (0, 1152)], fill=(120, 104, 80))
    d.polygon([(0, 780), (500, 640), (1100, 820), (1728, 700), (1728, 1152), (0, 1152)], fill=(78, 86, 62))
    d.polygon([(200, 700), (900, 860), (860, 1152), (80, 1152)], fill=STONE)
    for i in range(12):
        d.rectangle([220 + i * 48, 760 + (i % 3) * 8, 260 + i * 48, 900], outline=INK, width=2)
    d.polygon([(1120, 700), (1500, 680), (1540, 820), (1100, 860)], fill=(48, 42, 36), outline=INK)
    d.line([(1180, 700), (1220, 620), (1460, 600), (1500, 680)], fill=INK, width=3)
    d.ellipse([1160, 800, 1280, 900], outline=OCHRE, width=4)
    d.ellipse([1380, 790, 1500, 890], outline=OCHRE, width=4)
    for i in range(4):
        fig(d, 300 + i * 80, 560, 100, SOOT, lean=-6)
    d.ellipse([80, 60, 200, 180], outline=RUST, width=3)


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
