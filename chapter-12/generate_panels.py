#!/usr/bin/env python3
"""Chapter 12 panels. Idempotent: keep a jpg already over 80kb."""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import hashlib, random

root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)
NAMES = [
    '01-hayes-billiard.jpg',
    '02-league-room.jpg',
    '03-thurles-walkout.jpg',
    '04-hurling-sideline.jpg',
    '05-language-class.jpg',
    '06-organizer-road.jpg',
    '07-dundalk-resignation.jpg',
    '08-keating-after.jpg',
]

def grade(im):
    im = im.convert('RGB').resize((1728, 1152), Image.Resampling.LANCZOS)
    g = ImageOps.grayscale(im)
    sep = Image.merge('RGB', (
        g.point(lambda x: min(255, int(x * 1.05 + 18))),
        g.point(lambda x: min(255, int(x * 0.88 + 8))),
        g.point(lambda x: min(255, int(x * 0.68))),
    ))
    return ImageEnhance.Contrast(sep).enhance(1.12)

def fig(d, x, y, h, ink, lean=0):
    r = max(8, h // 8)
    d.ellipse([x - r, y - 2 * r, x + r, y], outline=ink, width=2)
    d.line([(x, y), (x + lean, y + h // 2)], fill=ink, width=3)
    d.line([(x + lean, y + h // 2), (x - h // 6, y + h)], fill=ink, width=2)
    d.line([(x + lean, y + h // 2), (x + h // 6, y + h)], fill=ink, width=2)
    d.line([(x, y + h // 5), (x - h // 5, y + h // 3)], fill=ink, width=2)
    d.line([(x, y + h // 5), (x + h // 5, y + h // 3)], fill=ink, width=2)

def coat(d, x, y, h, ink):
    fig(d, x, y, h, ink, 0)
    d.line([(x - h // 7, y + h // 6), (x - h // 5, y + h // 2)], fill=ink, width=2)
    d.line([(x + h // 7, y + h // 6), (x + h // 5, y + h // 2)], fill=ink, width=2)

def lamp(d, x, y, ink, glow):
    d.line([(x, y), (x, y + 70)], fill=ink, width=3)
    d.polygon([(x - 28, y), (x + 28, y), (x + 14, y - 36), (x - 14, y - 36)], outline=ink)
    d.ellipse([x - 18, y - 22, x + 18, y + 8], outline=glow, width=2)

def window(d, x, y, w, h, ink):
    d.rectangle([x, y, x + w, y + h], outline=ink, width=3)
    d.line([(x + w // 2, y), (x + w // 2, y + h)], fill=ink, width=2)
    d.line([(x, y + h // 2), (x + w, y + h // 2)], fill=ink, width=2)

def synth(name):
    W, H = 1728, 1152
    rng = random.Random(int(hashlib.md5(name.encode()).hexdigest()[:8], 16))
    im = Image.new('RGB', (W, H), (237, 228, 212))
    d = ImageDraw.Draw(im)
    px = im.load()
    for _ in range(24000):
        x, y = rng.randrange(W), rng.randrange(H)
        v = rng.randint(-18, 10)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))
    ink, rust, mid = (42, 34, 24), (107, 58, 42), (90, 70, 50)
    soot = (55, 46, 36)
    n = name[:2]
    if n == '01':
        d.rectangle([0, 0, W, H], fill=(214, 198, 172))
        d.rectangle([0, 0, W, 160], fill=(70, 58, 46))
        d.rectangle([80, 860, W - 80, H], fill=(96, 78, 58))
        d.rectangle([220, 430, 1500, 860], fill=(62, 78, 48), outline=ink, width=6)
        d.rectangle([280, 490, 1440, 800], outline=(120, 140, 90), width=3)
        for i in range(6):
            d.ellipse([360 + i * 170, 620, 420 + i * 170, 680], outline=(30, 40, 24), width=2)
        d.line([(200, 640), (520, 520)], fill=ink, width=4)
        d.line([(1500, 700), (1200, 500)], fill=ink, width=4)
        lamp(d, 360, 280, ink, rust)
        lamp(d, 1360, 280, ink, rust)
        coat(d, 260, 360, 220, ink)
        coat(d, 520, 340, 200, mid)
        coat(d, 1240, 350, 210, ink)
        coat(d, 1480, 380, 190, rust)
        d.rectangle([40, 200, 160, 780], outline=ink, width=3)
        d.rectangle([1560, 200, 1680, 780], outline=ink, width=3)
    elif n == '02':
        d.rectangle([0, 780, W, H], fill=(150, 132, 108))
        d.rectangle([40, 80, 520, 900], outline=ink, width=5)
        for row in range(8):
            y = 120 + row * 90
            d.line([(60, y), (500, y)], fill=mid, width=2)
            for k in range(9):
                bh = 28 + (k * 17 + row * 5) % 40
                d.rectangle([80 + k * 46, y - bh, 112 + k * 46, y - 4], fill=soot if k % 2 == 0 else rust, outline=ink)
        d.rectangle([700, 620, 1280, 760], fill=(186, 168, 142), outline=ink, width=4)
        d.rectangle([760, 560, 860, 620], outline=ink, width=2)
        d.rectangle([880, 540, 1000, 620], outline=mid, width=2)
        d.rectangle([1020, 570, 1100, 620], outline=ink, width=2)
        window(d, 1360, 120, 280, 360, ink)
        fig(d, 980, 500, 160, ink)
        coat(d, 640, 420, 240, mid)
        coat(d, 1380, 460, 220, rust)
    elif n == '03':
        d.rectangle([60, 80, 1280, 1040], outline=ink, width=6)
        d.rectangle([80, 140, 1240, 280], fill=(120, 100, 78), outline=ink, width=3)
        for i in range(22):
            fig(d, 140 + (i % 11) * 100, 340 + (i // 11) * 200, 150, mid if i % 3 else ink, rng.randint(-4, 4))
        d.polygon([(1280, 480), (1680, 360), (1680, 980), (1280, 860)], fill=(196, 180, 156), outline=ink)
        d.rectangle([1280, 500, 1360, 840], fill=(40, 34, 28))
        for i in range(9):
            fig(d, 1420 + (i % 3) * 80, 520 + (i // 3) * 140, 110, rust if i % 2 == 0 else mid, 8)
        d.rectangle([200, 900, 1100, 980], fill=(90, 74, 56), outline=ink, width=2)
    elif n == '04':
        d.rectangle([0, 0, W, 460], fill=(186, 168, 138))
        d.rectangle([0, 460, W, H], fill=(104, 112, 72))
        d.line([(0, 460), (W, 448)], fill=ink, width=3)
        d.rectangle([140, 160, 168, 700], fill=ink)
        d.rectangle([520, 160, 548, 700], fill=ink)
        d.rectangle([140, 160, 548, 188], fill=ink)
        for i in range(6):
            x = 700 + i * 130
            fig(d, x, 620, 200, mid if i % 2 else ink, rng.randint(-5, 5))
            d.line([(x + 10, 700), (x + 70, 860)], fill=soot, width=5)
        coat(d, 1280, 560, 280, ink)
        coat(d, 1520, 580, 260, rust)
        d.line([(1360, 780), (1480, 900)], fill=ink, width=5)
        d.ellipse([1180, 900, 1230, 940], outline=ink, width=3)
    elif n == '05':
        d.rectangle([0, 0, W, H], fill=(214, 200, 176))
        d.rectangle([360, 70, 1360, 460], fill=(78, 66, 52), outline=ink, width=6)
        for i in range(26):
            x0 = 420 + rng.randint(0, 860)
            y0 = 110 + rng.randint(0, 280)
            h = 30 + rng.randint(0, 70)
            d.line([(x0, y0), (x0 + rng.randint(-6, 6), y0 + h)], fill=(214, 198, 170), width=2)
        d.rectangle([180, 780, 1540, 860], fill=(120, 96, 70), outline=ink, width=4)
        for i in range(6):
            fig(d, 300 + i * 200, 560, 200, mid if i % 2 else ink)
        coat(d, 860, 300, 180, rust)
        d.rectangle([80, 620, 200, 700], outline=ink, width=3)
        d.ellipse([110, 560, 170, 620], outline=rust, width=3)
    elif n == '06':
        d.rectangle([0, 0, W, 480], fill=(176, 158, 128))
        d.rectangle([0, 480, W, H], fill=(150, 132, 104))
        d.polygon([(760, 500), (968, 500), (1280, H), (448, H)], fill=(196, 176, 146))
        d.line([(760, 500), (448, H)], fill=ink, width=3)
        d.line([(968, 500), (1280, H)], fill=ink, width=3)
        for i in range(5):
            y = 560 + i * 100
            d.rectangle([200, y, 520, y + 28], outline=soot, width=2)
            d.rectangle([1200, y + 20, 1560, y + 48], outline=soot, width=2)
        d.rectangle([120, 250, 420, 500], fill=(132, 114, 92), outline=ink, width=4)
        d.polygon([(110, 250), (270, 150), (430, 250)], fill=(100, 82, 64), outline=ink)
        window(d, 180, 320, 80, 90, ink)
        d.rectangle([1280, 230, 1600, 500], fill=(124, 106, 86), outline=ink, width=4)
        d.polygon([(1270, 230), (1440, 120), (1610, 230)], fill=(90, 74, 58), outline=ink)
        window(d, 1360, 300, 80, 100, ink)
        coat(d, 860, 620, 260, ink)
        d.rectangle([900, 760, 960, 840], outline=rust, width=3)
    elif n == '07':
        d.rectangle([0, 0, W, 560], fill=(214, 196, 170))
        d.rectangle([0, 560, W, H], fill=(122, 104, 84))
        d.rectangle([140, 160, 980, 560], fill=(72, 60, 48), outline=ink, width=5)
        light = (214, 198, 172)
        d.line([(520, 250), (520, 500)], fill=light, width=4)
        d.line([(520, 250), (560, 250)], fill=light, width=4)
        d.line([(560, 250), (560, 360)], fill=light, width=4)
        d.line([(520, 360), (640, 360)], fill=light, width=4)
        d.line([(640, 360), (640, 500)], fill=light, width=4)
        for i in range(4):
            d.line([(1000, 500 + i * 28), (1220, 500 + i * 28)], fill=ink, width=5)
        coat(d, 1100, 430, 240, rust)
        for i in range(11):
            fig(d, 120 + i * 145, 860, 150, mid if i % 2 else ink)
            if i % 3 == 0:
                d.line([(120 + i * 145, 820), (150 + i * 145, 760)], fill=rust, width=3)
    else:
        d.rectangle([0, 0, W, H], fill=(36, 30, 26))
        d.rectangle([70, 70, W - 70, H - 70], fill=(210, 196, 172), outline=ink, width=4)
        d.rectangle([120, 120, 360, 420], fill=(22, 26, 40), outline=ink, width=4)
        d.line([(240, 120), (240, 420)], fill=ink, width=2)
        d.line([(120, 270), (360, 270)], fill=ink, width=2)
        for i in range(4):
            x = 140 + i * 150
            d.rectangle([x, 860, x + 90, 940], outline=mid, width=3)
            d.line([(x + 10, 860), (x + 10, 780)], fill=mid, width=3)
            d.line([(x + 80, 860), (x + 80, 780)], fill=mid, width=3)
            d.line([(x + 10, 780), (x + 80, 780)], fill=mid, width=3)
        coat(d, 720, 460, 250, ink)
        coat(d, 900, 430, 270, rust)
        coat(d, 1080, 450, 250, mid)
        coat(d, 1260, 470, 240, ink)
        coat(d, 1440, 500, 210, soot)
        d.ellipse([980, 780, 1060, 860], outline=rust, width=3)
    for i in range(0, W, 18):
        d.line([(i, 0), (i - 240, H)], fill=(200, 186, 166), width=1)
    return grade(im.filter(ImageFilter.SMOOTH_MORE))

for name in NAMES:
    path = root / name
    if path.exists() and path.stat().st_size > 80000:
        print('keep', path, path.stat().st_size)
        continue
    synth(name).save(path, 'JPEG', quality=86, optimize=True)
    print('synth', path, path.stat().st_size)
print('ch12 panels done')
