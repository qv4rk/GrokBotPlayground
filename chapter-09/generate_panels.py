#!/usr/bin/env python3
"""Chapter 09 panels. Idempotent: keep an existing jpg over 80kb."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import hashlib, math, random

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
NAMES = [
    "01-glasnevin-beds.jpg",
    "02-berkeley-specimens.jpg",
    "03-half-crop.jpg",
    "04-relief-table.jpg",
    "05-corn-landing.jpg",
    "06-cabinet-chairs.jpg",
    "07-same-night.jpg",
    "08-treasury-handoff.jpg",
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
    px = im.load()
    w, h = im.size
    for _ in range(n):
        x, y = rng.randrange(w), rng.randrange(h)
        r, g, b = px[x, y]
        v = rng.randint(-18, 12)
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))


def hatch(d, box, step=14, color=(196, 180, 156), width=1):
    x0, y0, x1, y1 = box
    span = y1 - y0
    for i in range(x0 - span, x1 + span, step):
        d.line([(i, y0), (i + span, y1)], fill=color, width=width)


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
    else:
        d.line([hip, (x - h // 6, y + h)], fill=ink, width=2)
        d.line([hip, (x + h // 6, y + h)], fill=ink, width=2)
    d.line([(x, y + h // 6), (x - h // 5, y + h // 3)], fill=ink, width=2)
    d.line([(x, y + h // 6), (x + h // 5 + lean // 2, y + h // 3)], fill=ink, width=2)


def squiggle(d, x, y, n, color=MID, amp=3, step=7):
    pts = [(x + i * step, y + ((i % 3) - 1) * amp) for i in range(n)]
    if len(pts) > 1:
        d.line(pts, fill=color, width=1)


def grade(im):
    g = ImageOps.grayscale(im.convert("RGB"))
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


def scene_garden(im, d, rng):
    # walled botanic garden, blighted beds, one curator
    d.rectangle([0, 0, 1728, 420], fill=(168, 178, 176))
    d.rectangle([0, 420, 1728, 1152], fill=(118, 112, 78))
    d.rectangle([40, 80, 1680, 1080], outline=INK, width=10)
    d.rectangle([70, 140, 420, 520], fill=(186, 198, 196), outline=INK, width=4)
    for i in range(5):
        d.rectangle([90 + i * 60, 180, 130 + i * 60, 480], outline=MID, width=2)
    d.polygon([(70, 140), (245, 40), (420, 140)], fill=(150, 168, 166), outline=INK)
    for row in range(4):
        y = 560 + row * 120
        d.rectangle([120, y, 1100, y + 90], fill=(96, 108, 64), outline=INK, width=2)
        for i in range(14):
            x = 150 + i * 66
            sick = (row + i) % 3 == 0
            col = (70, 62, 40) if sick else (60, 90, 48)
            d.polygon([(x, y + 70), (x + 18, y + 10), (x + 36, y + 70)], fill=col, outline=INK)
            if sick:
                d.ellipse([x + 8, y + 28, x + 28, y + 48], fill=SOOT)
    fig(d, 1280, 780, 240, INK, -8)
    d.ellipse([1360, 860, 1420, 910], outline=RUST, width=3)
    d.line([(1390, 880), (1460, 940)], fill=RUST, width=2)
    d.polygon([(1480, 980), (1600, 1000), (1560, 1080)], outline=INK)
    for i in range(6):
        d.ellipse([1460 + (i % 3) * 28, 990 + i * 8, 1478 + (i % 3) * 28, 1006 + i * 8], fill=(80, 60, 36))


def scene_specimens(im, d, rng):
    # calm correspondence desk, pressed leaves, no readable script
    d.rectangle([0, 0, 1728, 1152], fill=(92, 74, 58))
    d.rectangle([80, 160, 1640, 980], fill=(176, 148, 112), outline=INK, width=6)
    d.rectangle([140, 240, 820, 860], fill=(228, 218, 198), outline=INK, width=4)
    for i in range(8):
        squiggle(d, 190, 300 + i * 60, 36, MID, 2, 8)
    d.rectangle([200, 700, 520, 820], outline=RUST, width=3)
    d.ellipse([560, 300, 760, 520], outline=INK, width=4)
    d.polygon([(620, 480), (700, 340), (740, 470)], fill=(70, 80, 46), outline=SOOT)
    d.ellipse([640, 400, 680, 440], fill=SOOT)
    d.rectangle([900, 260, 1520, 700], fill=(210, 200, 180), outline=INK, width=3)
    for i in range(5):
        d.rectangle([960, 310 + i * 70, 1460, 360 + i * 70], outline=MID)
        d.polygon([(980, 350 + i * 70), (1040, 318 + i * 70), (1100, 352 + i * 70)], fill=(50, 62, 36), outline=INK)
    fig(d, 400, 900, 160, INK, 4)
    fig(d, 1280, 860, 180, RUST, -6)
    d.rectangle([1100, 760, 1500, 920], outline=INK, width=2)
    for i in range(4):
        squiggle(d, 1140, 790 + i * 28, 22, MID, 2, 7)


def scene_halfcrop(im, d, rng):
    # inspectors over a clamped field, half the rows gone black
    d.rectangle([0, 0, 1728, 380], fill=(120, 124, 118))
    d.polygon([(0, 380), (400, 260), (900, 340), (1400, 220), (1728, 360), (1728, 520), (0, 560)], fill=(100, 108, 86))
    d.rectangle([0, 500, 1728, 1152], fill=(110, 96, 70))
    for row in range(6):
        y = 560 + row * 90
        dead = row >= 3
        d.rectangle([40, y, 1680, y + 70], fill=(60, 52, 40) if dead else (78, 96, 52), outline=INK)
        for i in range(22):
            x = 70 + i * 74
            if dead:
                d.line([(x, y + 60), (x + 10, y + 8)], fill=SOOT, width=3)
                d.ellipse([x, y + 20, x + 22, y + 40], fill=(40, 32, 24))
            else:
                d.polygon([(x, y + 60), (x + 16, y + 8), (x + 32, y + 60)], fill=(50, 78, 40), outline=INK)
    for i, x in enumerate((980, 1180, 1380)):
        fig(d, x, 420, 200, INK if i != 1 else RUST, rng.randint(-6, 6))
        d.rectangle([x - 20, 500, x + 30, 560], outline=MID)
    d.ellipse([1040, 620, 1160, 700], fill=(90, 60, 40), outline=INK, width=3)
    d.line([(1100, 620), (1100, 700)], fill=SOOT, width=2)


def scene_relief(im, d, rng):
    # small Dublin commission room, not a parliament
    d.rectangle([0, 0, 1728, 1152], fill=(150, 138, 118))
    d.rectangle([60, 40, 700, 620], fill=(176, 190, 188), outline=INK, width=6)
    for i in range(4):
        d.rectangle([100 + i * 140, 80, 200 + i * 140, 280], outline=INK, width=3)
        d.polygon([(100 + i * 140, 280), (150 + i * 140, 200), (200 + i * 140, 360)], outline=MID)
    d.rectangle([0, 700, 1728, 1152], fill=(100, 82, 64))
    d.polygon([(200, 820), (1500, 760), (1560, 1040), (160, 1080)], fill=(120, 90, 64), outline=INK, width=4)
    for i in range(6):
        fig(d, 360 + i * 180, 620, 200, INK if i % 2 == 0 else MID, 0)
    d.rectangle([480, 880, 1240, 1000], fill=PAPER, outline=RUST, width=3)
    for i in range(4):
        squiggle(d, 520, 900 + i * 22, 40, MID, 2, 8)
    d.ellipse([1380, 200, 1580, 360], outline=OCHRE, width=4)


def scene_landing(im, d, rng):
    # dusk quay, sailing ship, unmarked sacks, few hands
    d.rectangle([0, 0, 1728, 520], fill=(70, 74, 92))
    d.rectangle([0, 520, 1728, 780], fill=(48, 62, 74))
    d.rectangle([0, 780, 1728, 1152], fill=(90, 78, 62))
    d.polygon([(80, 640), (420, 200), (460, 640)], fill=(40, 42, 48), outline=INK)
    d.line([(420, 200), (420, 700)], fill=INK, width=4)
    d.polygon([(460, 420), (900, 360), (920, 620), (480, 660)], fill=(36, 38, 44), outline=INK)
    d.polygon([(200, 280), (400, 180), (410, 420)], fill=(210, 206, 190), outline=INK)
    d.polygon([(500, 300), (780, 250), (760, 460)], fill=(200, 196, 180), outline=INK)
    d.rectangle([980, 620, 1680, 1000], fill=(70, 58, 46), outline=INK, width=5)
    d.polygon([(960, 620), (1330, 480), (1700, 620)], fill=(58, 48, 40), outline=INK)
    for i in range(8):
        x = 1040 + (i % 4) * 140
        y = 700 + (i // 4) * 120
        d.ellipse([x, y, x + 100, y + 70], fill=(150, 124, 86), outline=INK, width=3)
    for i, x in enumerate((700, 860, 1180)):
        fig(d, x, 860, 180, PAPER if i == 2 else INK, 6)
    d.ellipse([40, 60, 160, 180], outline=(200, 190, 160), width=3)
    hatch(d, (0, 520, 1728, 780), 22, (40, 52, 62))


def scene_cabinet(im, d, rng):
    # long cabinet table, chairs shoved back, one man left with a sheet
    d.rectangle([0, 0, 1728, 1152], fill=(78, 64, 52))
    d.rectangle([80, 60, 1640, 400], fill=(120, 100, 80), outline=INK, width=4)
    for i in range(7):
        d.rectangle([140 + i * 200, 100, 280 + i * 200, 280], fill=(160, 170, 168), outline=INK, width=2)
    d.polygon([(200, 780), (1520, 700), (1580, 980), (160, 1040)], fill=(132, 104, 76), outline=INK, width=5)
    d.rectangle([520, 800, 1200, 940], fill=PAPER, outline=RUST, width=4)
    for i in range(3):
        squiggle(d, 580, 830 + i * 30, 34, MID, 2, 8)
    fig(d, 860, 560, 240, INK, 0)
    for i, x in enumerate((240, 420, 1280, 1480)):
        # empty chairs tipped
        d.polygon([(x, 860), (x + 70, 820), (x + 80, 980), (x - 10, 1000)], outline=OCHRE, width=3)
        d.line([(x + 20, 980), (x - 30, 1080)], fill=OCHRE, width=3)
        d.line([(x + 50, 980), (x + 110, 1060)], fill=OCHRE, width=3)
    d.rectangle([80, 1040, 400, 1120], fill=(50, 40, 32))


def scene_samenight(im, d, rng):
    # two chambers divided by a wall: peers standing, a sheet left on the other floor
    d.rectangle([0, 0, 860, 1152], fill=(88, 70, 56))
    d.rectangle([868, 0, 1728, 1152], fill=(56, 58, 70))
    d.rectangle([830, 0, 900, 1152], fill=SOOT)
    d.polygon([(120, 700), (740, 660), (760, 900), (100, 940)], fill=(140, 112, 80), outline=INK, width=4)
    fig(d, 420, 480, 220, INK, 4)
    for i, x in enumerate((180, 300, 560, 680)):
        fig(d, x, 820, 160, MID, 0)
    d.rectangle([300, 760, 540, 860], fill=PAPER, outline=RUST, width=3)
    # other room: sheet on the floor, figures leaving toward a door
    d.rectangle([1100, 80, 1600, 420], fill=(30, 32, 40))
    d.polygon([(1180, 80), (1520, 80), (1480, 200)], fill=(20, 22, 28))
    d.rectangle([1000, 860, 1400, 1040], fill=PAPER, outline=OCHRE, width=4)
    for i in range(5):
        squiggle(d, 1040, 900 + i * 24, 28, MID, 2, 7)
    for i, x in enumerate((1480, 1600, 1680)):
        fig(d, x, 700, 200, (210, 200, 180), 16)
    d.line([(900, 200), (900, 900)], fill=RUST, width=2)


def scene_handoff(im, d, rng):
    # treasury desk receives folders and one sack; a coat leaves by the door
    d.rectangle([0, 0, 1728, 1152], fill=(186, 174, 154))
    d.rectangle([0, 0, 420, 1152], fill=(70, 60, 50))
    d.rectangle([80, 180, 340, 900], fill=(40, 34, 28))
    d.polygon([(160, 240), (260, 220), (250, 520), (150, 540)], fill=SOOT, outline=INK)
    d.rectangle([480, 360, 1500, 860], fill=(120, 92, 68), outline=INK, width=6)
    for i in range(4):
        d.rectangle([560 + i * 20, 420 - i * 16, 980 + i * 10, 700 - i * 8], fill=PAPER, outline=INK, width=2)
        for k in range(3):
            squiggle(d, 600 + i * 16, 470 + k * 36 - i * 8, 20, MID, 2, 7)
    d.ellipse([1100, 520, 1320, 700], fill=(150, 124, 86), outline=INK, width=4)
    fig(d, 1380, 480, 260, RUST, -4)
    fig(d, 700, 880, 180, INK, 10)
    d.rectangle([200, 960, 380, 1100], outline=OCHRE, width=3)
    d.line([(260, 960), (300, 880)], fill=OCHRE, width=3)


SCENES = {
    "01": scene_garden,
    "02": scene_specimens,
    "03": scene_halfcrop,
    "04": scene_relief,
    "05": scene_landing,
    "06": scene_cabinet,
    "07": scene_samenight,
    "08": scene_handoff,
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
