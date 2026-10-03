#!/usr/bin/env python3
"""Chapter 15 panels. Idempotent: keep a jpg already over 80kb."""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import hashlib, random

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

def hull(d, x, y, w, h, ink, fill):
    d.polygon([(x, y), (x + w, y + h // 5), (x + w - 30, y + h), (x + 40, y + h)], fill=fill, outline=ink)

def synth(name):
    W, H = 1728, 1152
    rng = random.Random(int(hashlib.md5(name.encode()).hexdigest()[:8], 16))
    im = Image.new('RGB', (W, H), (237, 228, 212))
    d = ImageDraw.Draw(im)
    px = im.load()
    for _ in range(28000):
        x, y = rng.randrange(W), rng.randrange(H)
        v = rng.randint(-18, 12)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))
    ink, rust, mid = (42, 34, 24), (107, 58, 42), (90, 70, 50)
    soot = (55, 46, 36)
    n = name[:2]
    if n == '01':
        d.rectangle([0, 0, W, 620], fill=(168, 150, 122))
        d.rectangle([0, 620, W, H], fill=(78, 88, 92))
        for i in range(5):
            y = 680 + i * 70
            d.arc([-300, y, W + 200, y + 180], 200, 340, fill=(140, 150, 148), width=3)
        d.polygon([(620, 860), (1180, 820), (1120, 980), (700, 1000)], fill=(120, 96, 72), outline=ink)
        d.line([(900, 280), (900, 860)], fill=ink, width=5)
        d.line([(980, 340), (980, 820)], fill=ink, width=4)
        d.polygon([(900, 300), (1280, 520), (900, 640)], fill=(214, 198, 168), outline=ink)
        d.polygon([(980, 360), (1320, 560), (980, 700)], fill=(200, 180, 150), outline=ink)
        d.polygon([(820, 420), (900, 480), (900, 700)], fill=(190, 170, 140), outline=ink)
        fig(d, 860, 700, 90, rust)
    elif n == '02':
        d.rectangle([0, 0, W, 480], fill=(150, 136, 112))
        d.polygon([(900, 80), (1680, 40), (1728, 900), (1100, 980), (860, 420)], fill=(132, 108, 78), outline=ink)
        d.rectangle([0, 700, 1100, H], fill=(70, 78, 82))
        hull(d, 80, 620, 780, 220, ink, (96, 78, 60))
        d.rectangle([260, 420, 340, 640], fill=soot)
        d.rectangle([460, 460, 530, 640], fill=soot)
        d.ellipse([180, 300, 420, 520], outline=(80, 72, 64), width=8)
        d.polygon([(200, 780), (520, 760), (500, 900), (220, 920)], fill=(40, 36, 32))
        for i in range(6):
            d.ellipse([240 + i * 48, 800, 280 + i * 48, 860], fill=(30, 28, 26))
    elif n == '03':
        d.rectangle([0, 0, W, H], fill=(186, 154, 108))
        d.polygon([(760, 0), (980, 0), (1180, H), (520, H)], fill=(150, 118, 78))
        d.polygon([(820, 40), (920, 40), (1040, H), (680, H)], fill=(96, 110, 114))
        for i in range(7):
            x = 160 + (i % 4) * 80
            y = 180 + i * 120
            d.polygon([(x, y), (x + 50, y + 20), (x + 20, y + 70)], outline=ink)
            d.line([(x + 10, y + 30), (x - 30, y + 10)], fill=ink, width=3)
        for i in range(4):
            d.polygon([(1280, 200 + i * 180), (1480, 140 + i * 180), (1560, 280 + i * 180), (1320, 320 + i * 180)], outline=ink, width=3)
        for i in range(5):
            fig(d, 240 + i * 70, 860, 110, mid if i % 2 else ink, lean=-6)
        d.ellipse([400, 980, 470, 1040], outline=rust, width=3)
        d.ellipse([500, 990, 560, 1050], outline=ink, width=2)
    elif n == '04':
        d.rectangle([0, 0, W, 500], fill=(120, 96, 78))
        d.rectangle([0, 500, W, H], fill=(86, 104, 108))
        for i in range(18):
            x, y = 80 + (i * 97) % 1600, 80 + (i * 53) % 360
            d.line([(x, y), (x + 8, y + 28)], fill=(220, 190, 120), width=2)
        d.polygon([(180, 620), (620, 560), (680, 760), (240, 820)], fill=(170, 150, 120), outline=ink)
        d.line([(400, 280), (400, 600)], fill=ink, width=4)
        d.polygon([(400, 300), (620, 480), (400, 540)], fill=(220, 206, 180), outline=ink)
        for i in range(5):
            x = 760 + i * 170
            d.polygon([(x, 700 + i * 12), (x + 140, 680 + i * 8), (x + 150, 800), (x + 20, 820)], fill=(140, 122, 100), outline=ink)
        fig(d, 360, 500, 80, rust)
        fig(d, 480, 520, 70, mid)
    elif n == '05':
        d.rectangle([0, 0, 280, H], fill=(168, 140, 96))
        d.rectangle([1440, 0, W, H], fill=(160, 132, 90))
        d.rectangle([280, 0, 1440, H], fill=(72, 86, 90))
        for i in range(6):
            y = 40 + i * 180
            d.polygon([(340, y + 40), (900, y), (980, y + 70), (400, y + 110)], fill=(110, 92, 70), outline=ink)
            d.rectangle([460, y - 50, 500, y + 30], fill=soot)
            d.rectangle([620, y - 70, 670, y + 10], fill=soot)
            d.ellipse([500, y - 140, 640, y - 40], outline=(90, 82, 72), width=6)
        d.rectangle([0, 200, 200, 420], outline=ink, width=4)
        d.rectangle([1500, 640, 1700, 900], outline=ink, width=4)
    elif n == '06':
        d.rectangle([0, 0, W, H], fill=(196, 180, 154))
        d.rectangle([80, 80, 1640, 1040], outline=ink, width=8)
        for i in range(8):
            d.rectangle([140 + i * 190, 120, 300 + i * 190, 520], outline=mid, width=3)
        d.rectangle([360, 600, 1280, 1000], fill=(118, 92, 68), outline=ink, width=6)
        d.rectangle([520, 460, 1040, 680], fill=(230, 220, 198), outline=ink, width=4)
        for i in range(5):
            d.line([(580, 510 + i * 24), (980, 510 + i * 24)], fill=mid, width=1)
        d.rectangle([1100, 760, 1240, 960], outline=soot, width=5)
        d.rectangle([200, 780, 340, 980], outline=ink, width=4)
        fig(d, 1480, 640, 240, ink)
    elif n == '07':
        d.rectangle([0, 0, W, H], fill=(176, 148, 112))
        for i in range(3):
            x = 180 + i * 500
            d.arc([x, 80, x + 420, 700], 200, 340, fill=ink, width=8)
            d.rectangle([x + 40, 380, x + 380, 980], outline=ink, width=4)
        d.rectangle([620, 520, 1100, 900], fill=(210, 196, 168), outline=rust, width=4)
        for i in range(9):
            d.rectangle([660, 560 + i * 28, 1040, 582 + i * 28], outline=mid, width=1)
        d.polygon([(240, 860), (480, 820), (500, 1040), (220, 1060)], outline=ink, width=5)
        d.line([(240, 860), (500, 1040)], fill=ink, width=2)
        d.rectangle([1280, 700, 1560, 1040], outline=soot, width=6)
    else:
        d.rectangle([0, 0, W, H], fill=(48, 42, 36))
        d.polygon([(0, 280), (420, 220), (760, 360), (980, 180), (1280, 300), (1728, 160), (1728, 820), (0, 900)], fill=(92, 74, 52))
        d.polygon([(0, 700), (500, 640), (900, 760), (1400, 680), (1728, 820), (1728, H), (0, H)], fill=(36, 48, 52))
        lights = [(120, 340), (300, 260), (560, 400), (860, 240), (1120, 360), (1400, 250), (1600, 420)]
        for x, y in lights:
            d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(210, 170, 90))
            d.rectangle([x - 16, y + 8, x + 16, y + 36], outline=(180, 150, 100), width=2)
        d.rectangle([700, 480, 980, 700], outline=(190, 160, 110), width=4)
        d.polygon([(700, 480), (840, 400), (980, 480)], outline=(190, 160, 110), width=3)
        d.rectangle([760, 560, 920, 700], fill=(70, 58, 44))
        for i in range(4):
            fig(d, 620 + i * 50, 760, 80, (200, 170, 130))
    for i in range(0, W, 21):
        d.line([(i, 0), (i - 180, H)], fill=(200, 186, 166), width=1)
    return grade(im.filter(ImageFilter.SMOOTH_MORE))

NAMES = [
    '01-cape-clipper.jpg',
    '02-fat-steam.jpg',
    '03-desert-cut.jpg',
    '04-bitter-lakes.jpg',
    '05-traffic-slot.jpg',
    '06-new-court.jpg',
    '07-empty-treasury.jpg',
    '08-staging-post.jpg',
]
root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)
for name in NAMES:
    path = root / name
    if path.exists() and path.stat().st_size > 80000:
        print('keep', path.name, path.stat().st_size)
        continue
    synth(name).save(path, 'JPEG', quality=86, optimize=True)
    print('synth', path.name, path.stat().st_size)
print('ch15 panels done')
