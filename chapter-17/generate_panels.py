#!/usr/bin/env python3
"""Chapter 17 panels. Idempotent: keep an existing jpg above 80kb."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random

ROOT = Path(__file__).resolve().parent / "panels"
ROOT.mkdir(parents=True, exist_ok=True)
W, H = 1728, 1152
NAMES = [
    "01-brunswick-door.jpg",
    "02-secret-wall.jpg",
    "03-candle-files.jpg",
    "04-stone-window.jpg",
    "05-capel-library.jpg",
    "06-alley-warning.jpg",
    "07-empty-branch.jpg",
    "08-pearse-head.jpg",
]
PAPER = (237, 228, 212)
INK = (42, 34, 24)
SOOT = (28, 24, 20)
OCHRE = (168, 122, 72)
RUST = (107, 58, 42)
MID = (92, 74, 54)
WASH = (214, 196, 168)


def rng_for(name):
    return random.Random(sum(ord(c) * (i + 3) for i, c in enumerate(name)) + 17)


def grain(im, rng, n=14000):
    px = im.load()
    for _ in range(n):
        x, y = rng.randrange(W), rng.randrange(H)
        r, g, b = px[x, y]
        v = rng.randint(-18, 10)
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v - 2)))


def figure(d, x, y, h, ink=INK, lean=0):
    """Coat mass. No face, no caricature."""
    r = max(10, h // 10)
    d.ellipse([x - r + lean // 5, y - 2 * r, x + r + lean // 5, y], fill=ink)
    sy = y + h // 12
    hem = y + int(h * 0.62)
    d.polygon(
        [(x - h // 5, sy), (x + h // 5, sy), (x + h // 7 + lean, hem), (x - h // 7 + lean, hem)],
        fill=ink,
    )
    d.polygon(
        [(x - h // 11 + lean, hem), (x - 1 + lean, hem), (x - h // 8, y + h), (x - h // 5, y + h)],
        fill=ink,
    )
    d.polygon(
        [(x + 1 + lean, hem), (x + h // 11 + lean, hem), (x + h // 5, y + h), (x + h // 8, y + h)],
        fill=ink,
    )
    d.polygon(
        [(x - h // 5, sy + 4), (x - h // 3, sy + h // 5), (x - h // 4, sy + h // 3), (x - h // 8, sy + h // 6)],
        fill=ink,
    )


def window(d, x, y, w, h, lit=False):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3)
    d.line([(x + w // 2, y), (x + w // 2, y + h)], fill=INK, width=2)
    d.line([(x, y + h // 2), (x + w, y + h // 2)], fill=INK, width=2)
    if lit:
        d.rectangle([x + 4, y + 4, x + w // 2 - 2, y + h // 2 - 2], fill=OCHRE)


def hatch(d, box, step=11, color=(120, 100, 78)):
    x0, y0, x1, y1 = box
    span = (x1 - x0) + (y1 - y0)
    x = x0 - (y1 - y0)
    while x < x1 + span:
        d.line([(x, y1), (x + (y1 - y0), y0)], fill=color, width=1)
        x += step


def base():
    return Image.new("RGB", (W, H), PAPER)


def p_door(rng):
    im = base()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 780], fill=(48, 42, 36))
    d.rectangle([0, 780, W, H], fill=(36, 32, 28))
    d.rectangle([80, 90, 1640, 820], outline=(70, 60, 48), width=6)
    for i, x in enumerate((140, 520, 980)):
        d.rectangle([x, 160, x + 340, 760], outline=(90, 76, 58), width=3)
        for row in range(3):
            window(d, x + 40, 210 + row * 160, 90, 120, lit=(i == 1 and row == 1))
            window(d, x + 190, 210 + row * 160, 90, 120, lit=False)
    d.rectangle([690, 470, 910, 800], fill=(22, 18, 16), outline=OCHRE, width=4)
    d.polygon([(690, 470), (800, 420), (910, 470)], outline=OCHRE)
    d.ellipse([860, 620, 878, 638], fill=OCHRE)
    d.line([(1040, 180), (1040, 300)], fill=OCHRE, width=3)
    d.polygon([(990, 300), (1090, 300), (1070, 360), (1010, 360)], fill=OCHRE)
    d.ellipse([980, 360, 1100, 520], fill=(90, 62, 30))
    figure(d, 620, 620, 200, (18, 16, 14), lean=-6)
    figure(d, 760, 600, 210, (24, 20, 16), lean=4)
    figure(d, 900, 630, 190, (16, 14, 12), lean=8)
    grain(im, rng, 9000)
    return im


def p_wall(rng):
    im = base()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=(62, 52, 42))
    d.rectangle([80, 70, 1640, 1060], fill=(88, 74, 58), outline=INK, width=4)
    d.polygon([(980, 160), (1500, 200), (1480, 920), (960, 860)], fill=(120, 100, 78), outline=INK)
    d.line([(980, 160), (1500, 200)], fill=OCHRE, width=3)
    for col in range(4):
        for row in range(6):
            x = 220 + col * 160
            y = 180 + row * 120
            d.rectangle([x, y, x + 130, y + 100], fill=(210, 198, 176), outline=INK, width=2)
            d.rectangle([x + 12, y + 16, x + 118, y + 28], fill=RUST)
            d.rectangle([x + 12, y + 40, x + 90, y + 50], fill=MID)
    for cx in (700, 820):
        d.rectangle([cx, 780, cx + 16, 900], fill=OCHRE)
        d.polygon([(cx - 6, 780), (cx + 8, 740), (cx + 22, 780)], fill=(220, 170, 80))
    figure(d, 1280, 640, 220, SOOT, lean=10)
    d.rectangle([1500, 500, 1680, 980], fill=(20, 16, 14))
    grain(im, rng, 7000)
    return im


def p_candles(rng):
    im = base()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=(32, 28, 24))
    d.rectangle([120, 620, 1500, 980], fill=(54, 44, 34), outline=INK, width=4)
    for i in range(7):
        x = 180 + i * 170
        d.polygon([(x, 700), (x + 140, 680), (x + 150, 900), (x + 10, 920)], fill=(226, 214, 190), outline=INK)
        for k in range(5):
            d.line([(x + 20, 740 + k * 28), (x + 120, 728 + k * 28)], fill=RUST, width=2)
    d.rectangle([620, 40, 1080, 280], fill=(150, 140, 128), outline=INK, width=4)
    d.rectangle([640, 60, 840, 260], fill=(186, 168, 140))
    figure(d, 480, 560, 240, (16, 14, 12), lean=20)
    figure(d, 980, 540, 250, (20, 16, 14), lean=-16)
    d.ellipse([400, 860, 520, 940], fill=(120, 80, 36))
    d.ellipse([900, 850, 1040, 940], fill=(130, 86, 40))
    grain(im, rng, 6000)
    return im


def p_stone(rng):
    im = base()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=(40, 36, 32))
    d.polygon([(200, 80), (1500, 40), (1560, 900), (140, 980)], outline=OCHRE, width=8)
    hatch(d, (220, 120, 1480, 860), 16, (70, 60, 50))
    shards = [(640, 420), (780, 360), (900, 500), (720, 560), (1040, 440)]
    for i, (sx, sy) in enumerate(shards):
        d.polygon(
            [(sx, sy), (sx + 80 + i * 10, sy + 30), (sx + 20, sy + 110), (sx - 40, sy + 50)],
            fill=(190, 186, 176),
            outline=INK,
        )
    d.rectangle([0, 900, W, H], fill=(78, 62, 46))
    for i in range(12):
        d.line([(0, 920 + i * 18), (W, 910 + i * 18)], fill=(60, 48, 36), width=2)
    d.ellipse([860, 930, 1040, 1080], fill=(50, 48, 46), outline=INK, width=3)
    figure(d, 180, 860, 90, SOOT)
    figure(d, 260, 870, 80, MID)
    grain(im, rng, 5000)
    return im


def p_library(rng):
    im = base()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 900], fill=(196, 176, 146))
    d.rectangle([0, 900, W, H], fill=(120, 96, 70))
    for i in range(6):
        x = 60 + i * 150
        d.rectangle([x, 80, x + 120, 820], fill=(92, 64, 42), outline=INK, width=3)
        for row in range(14):
            y = 100 + row * 48
            d.rectangle([x + 8, y, x + 112, y + 36], fill=(150 + (row % 3) * 15, 110, 70), outline=SOOT)
    d.rectangle([980, 620, 1660, 860], fill=(70, 52, 36), outline=INK, width=4)
    d.rectangle([1180, 520, 1420, 680], fill=(230, 220, 198), outline=INK, width=3)
    for k in range(4):
        d.line([(1210, 560 + k * 22), (1380, 560 + k * 22)], fill=RUST, width=2)
    figure(d, 1080, 560, 240, (40, 30, 22), lean=6)
    figure(d, 1500, 540, 250, SOOT, lean=-8)
    d.rectangle([1500, 80, 1680, 420], fill=(210, 196, 160), outline=INK, width=3)
    grain(im, rng, 6000)
    return im


def p_alley(rng):
    im = base()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=(34, 32, 30))
    d.polygon([(0, 0), (620, 1040), (0, H)], fill=(22, 20, 18))
    d.polygon([(W, 0), (1100, 1040), (W, H)], fill=(26, 22, 20))
    d.polygon([(520, 1040), (1200, 1040), (980, H), (740, H)], fill=(48, 44, 38))
    d.polygon([(700, 1080), (760, 1060), (1040, 1120), (900, 1140)], fill=(60, 58, 52))
    figure(d, 760, 620, 280, (14, 12, 10), lean=-12)
    figure(d, 980, 600, 300, (18, 16, 14), lean=14)
    figure(d, 1180, 680, 220, (70, 58, 46), lean=-4)
    figure(d, 860, 430, 120, (20, 18, 16))
    figure(d, 960, 440, 110, (80, 66, 50))
    grain(im, rng, 5000)
    return im


def p_empty(rng):
    im = base()
    d = ImageDraw.Draw(im)
    d.rectangle([40, 40, W - 40, H - 40], fill=(176, 160, 136), outline=INK, width=5)
    d.rectangle([120, 700, 1500, 860], fill=(96, 74, 52), outline=INK, width=4)
    for i in range(6):
        x = 180 + i * 210
        d.rectangle([x, 500, x + 70, 700], outline=INK, width=3)
        d.arc([x - 10, 620, x + 80, 760], 200, 340, fill=INK, width=3)
    for col in range(8):
        for row in range(3):
            x = 160 + col * 180
            y = 120 + row * 110
            fill = (210, 198, 176) if (col + row) % 3 else (120, 100, 80)
            d.rectangle([x, y, x + 150, y + 90], fill=fill, outline=INK, width=2)
    for i, x in enumerate((200, 340, 1500)):
        d.line([(x, 430), (x, 470)], fill=INK, width=3)
        d.polygon([(x - 28, 470), (x + 28, 470), (x + 36, 620), (x - 36, 620)], fill=SOOT if i != 1 else RUST)
    d.rectangle([1180, 200, 1560, 460], fill=(24, 22, 20), outline=INK, width=4)
    grain(im, rng, 7000)
    return im


def p_head(rng):
    im = base()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=(176, 158, 132))
    for row in range(10):
        for col in range(9):
            x = 20 + col * 190 + (28 if row % 2 else 0)
            y = 16 + row * 114
            tone = 168 + ((row * 3 + col) % 5) * 6
            d.rectangle([x, y, x + 170, y + 96], fill=(tone, tone - 16, tone - 36), outline=(96, 78, 58), width=2)
    d.polygon(
        [(640, 420), (980, 360), (1120, 470), (1080, 760), (760, 820), (620, 640)],
        fill=(132, 112, 88),
        outline=INK,
    )
    d.polygon([(980, 360), (1180, 430), (1120, 470)], fill=(110, 90, 70), outline=INK)
    d.arc([860, 470, 1080, 700], 250, 40, fill=INK, width=4)
    d.line([(1000, 540), (1088, 590)], fill=INK, width=3)
    d.line([(980, 640), (1060, 650)], fill=INK, width=2)
    d.rectangle([760, 900, 980, 1140], fill=(36, 30, 26), outline=INK, width=4)
    d.rectangle([700, 860, 1040, 910], fill=(150, 128, 102), outline=INK, width=3)
    grain(im, rng, 6000)
    return im


DRAW = {
    "01": p_door,
    "02": p_wall,
    "03": p_candles,
    "04": p_stone,
    "05": p_library,
    "06": p_alley,
    "07": p_empty,
    "08": p_head,
}


def finish(im, rng):
    px = im.load()
    for y in range(0, H, 2):
        row = rng.randint(-8, 6)
        for x in range(0, W, 2):
            v = row + rng.randint(-16, 12)
            r, g, b = px[x, y]
            px[x, y] = (
                max(0, min(255, r + v)),
                max(0, min(255, g + v - 1)),
                max(0, min(255, b + v - 3)),
            )
    d = ImageDraw.Draw(im)
    for i in range(0, W, 9):
        d.line([(i, 0), (i - 260, H)], fill=(198, 182, 158), width=1)
    return im.filter(ImageFilter.SMOOTH)


def main():
    for name in NAMES:
        path = ROOT / name
        if path.exists() and path.stat().st_size > 80000:
            print("keep", path, path.stat().st_size)
            continue
        seed = rng_for(name)
        im = finish(DRAW[name[:2]](seed), seed)
        im.save(path, "JPEG", quality=86, optimize=True)
        print("synth", path, path.stat().st_size)


if __name__ == "__main__":
    main()
