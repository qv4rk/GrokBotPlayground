#!/usr/bin/env python3
"""Chapter 21 panels. Idempotent: keep a jpg already over 80kb."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib, random

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
NAMES = [
    "01-smyths-door.jpg",
    "02-clonard-night.jpg",
    "03-fields-nightclothes.jpg",
    "04-commons-paper.jpg",
    "05-patrick-street.jpg",
    "06-dublin-doors.jpg",
    "07-croke-stands.jpg",
    "08-closed-street.jpg",
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
    d.rectangle([0, 0, 1728, 520], fill=(176, 148, 112))
    d.rectangle([0, 520, 1728, 1152], fill=(110, 96, 78))
    d.rectangle([520, 180, 1200, 980], outline=INK, width=6)
    d.polygon([(520, 180), (860, 40), (1200, 180)], outline=INK, width=4)
    d.rectangle([760, 560, 980, 980], fill=(62, 50, 40), outline=INK, width=4)
    d.ellipse([700, 300, 1020, 460], outline=RUST, width=3)
    fig(d, 360, 700, 240, INK, lean=6)
    fig(d, 1380, 720, 230, MID, lean=-8)

def scene_02(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(42, 36, 30))
    for i in range(6):
        x=40+i*280
        d.rectangle([x, 220, x+240, 780], outline=OCHRE, width=3)
        d.polygon([(x, 220), (x+120, 120), (x+240, 220)], outline=OCHRE, width=2)
        d.ellipse([x+70, 80, x+150, 150], outline=OCHRE, width=2)
    for i in range(3):
        d.rectangle([180+i*460, 860, 520+i*460, 1040], fill=(70, 60, 48), outline=OCHRE, width=3)
    d.rectangle([0, 1000, 1728, 1152], fill=(28, 24, 20))

def scene_03(d, rng):
    d.rectangle([0, 0, 1728, 640], fill=(168, 176, 168))
    d.rectangle([0, 640, 1728, 1152], fill=(120, 132, 96))
    for i in range(5):
        d.arc([80+i*340, 700, 360+i*340, 1100], 200, 340, fill=INK, width=3)
    for i in range(8):
        fig(d, 160+i*190, 620, 200+(i%3)*20, INK if i%2==0 else MID, lean=rng.randint(-6,6))
    d.ellipse([1400, 80, 1560, 240], outline=MID, width=2)

def scene_04(d, rng):
    d.rectangle([0, 80, 1728, 400], fill=(150, 132, 108))
    for row in range(4):
        y=180+row*180
        d.arc([80, y, 1640, y+220], 200, 340, fill=INK, width=4)
        for i in range(12):
            fig(d, 180+i*120, y+40, 90, MID, lean=0)
    sheet(d, (700, 860, 1040, 1080))
    fig(d, 860, 700, 180, RUST, lean=0)

def scene_05(d, rng):
    d.rectangle([0, 0, 1728, 420], fill=(150, 140, 124))
    d.rectangle([0, 420, 1728, 1152], fill=(100, 90, 76))
    for i in range(7):
        x=30+i*245
        d.rectangle([x, 160, x+210, 760], outline=INK, width=4)
        for k in range(4):
            d.line([(x+20, 300+k*80), (x+190, 300+k*80)], fill=RUST, width=3)
    d.line([(200, 900), (900, 980)], fill=INK, width=8)
    d.line([(900, 980), (860, 1040)], fill=INK, width=6)
    d.ellipse([1100, 80, 1500, 280], outline=MID, width=2)

def scene_06(d, rng):
    d.rectangle([0, 0, 1728, 700], fill=(214, 196, 168))
    d.rectangle([0, 700, 1728, 1152], fill=(160, 144, 120))
    for i in range(8):
        x=60+i*205
        d.rectangle([x, 120, x+180, 860], outline=INK, width=4)
        d.rectangle([x+50, 520, x+130, 860], fill=(70, 58, 46), outline=INK, width=3)
        d.rectangle([x+40, 200, x+140, 360], outline=MID, width=2)
    d.ellipse([1480, 60, 1640, 220], outline=RUST, width=3)

def scene_07(d, rng):
    d.ellipse([200, 620, 1520, 1100], outline=INK, width=5)
    d.ellipse([360, 700, 1360, 1040], fill=(150, 140, 100), outline=MID, width=3)
    d.ellipse([820, 840, 860, 880], fill=RUST, outline=INK)
    for row in range(3):
        for i in range(16):
            fig(d, 140+i*95, 180+row*140, 80, INK if (i+row)%2==0 else MID, lean=0)
    d.arc([40, 40, 1680, 520], 0, 180, fill=INK, width=4)

def scene_08(d, rng):
    d.rectangle([0, 0, 1728, 1152], fill=(186, 170, 146))
    d.rectangle([200, 80, 1520, 620], outline=INK, width=8)
    d.rectangle([700, 360, 1020, 620], fill=SOOT, outline=INK, width=5)
    d.line([(760, 360), (960, 620)], fill=OCHRE, width=4)
    d.line([(960, 360), (760, 620)], fill=OCHRE, width=4)
    for i in range(14):
        fig(d, 260+i*90, 160, 70, MID, lean=0)
    d.rectangle([0, 780, 1728, 1152], fill=(120, 108, 90))
    for i in range(4):
        d.rectangle([180+i*380, 860, 420+i*380, 1080], outline=INK, width=3)

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
