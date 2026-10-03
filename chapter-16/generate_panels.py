#!/usr/bin/env python3
"""Chapter 16 panels. Idempotent: keep a jpg already over 80kb."""
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
    for _ in range(28000):
        x, y = rng.randrange(W), rng.randrange(H)
        v = rng.randint(-18, 12)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))
    ink, rust, mid = (42, 34, 24), (107, 58, 42), (90, 70, 50)
    soot = (55, 46, 36)
    n = name[:2]
    if n == '01':
        d.rectangle([0, 0, W, 520], fill=(168, 150, 122))
        d.rectangle([0, 700, W, H], fill=(122, 108, 78))
        d.polygon([(0, 520), (600, 460), (1100, 540), (W, 480), (W, 720), (0, 760)], fill=(140, 124, 90))
        d.rectangle([980, 260, 1460, 620], fill=(110, 90, 70), outline=ink, width=5)
        d.polygon([(980, 260), (1220, 120), (1460, 260)], outline=ink, width=4)
        d.rectangle([1080, 360, 1180, 520], fill=(60, 52, 44))
        d.rectangle([1280, 400, 1380, 620], fill=(70, 58, 46))
        d.line([(200, 760), (860, 700)], fill=mid, width=3)
        for i in range(4):
            d.ellipse([180 + i * 160, 820, 280 + i * 160, 900], outline=ink, width=2)
    elif n == '02':
        d.rectangle([0, 0, W, H], fill=(206, 194, 172))
        d.rectangle([260, 280, 1460, 980], fill=(126, 100, 74), outline=ink, width=8)
        d.rectangle([460, 160, 1260, 520], fill=(232, 222, 200), outline=ink, width=4)
        for i in range(8):
            d.line([(540, 220 + i * 28), (1180, 220 + i * 28)], fill=mid, width=1)
        d.rectangle([160, 140, 360, 640], outline=ink, width=4)
        d.line([(160, 140), (360, 640)], fill=mid, width=2)
    elif n == '03':
        d.rectangle([0, 0, W, H], fill=(176, 160, 136))
        d.rectangle([420, 80, 1300, 1080], fill=(150, 128, 100), outline=ink, width=6)
        d.polygon([(420, 80), (860, 10), (1300, 80)], outline=ink)
        for row in range(4):
            for col in range(3):
                window(d, 520 + col * 220, 160 + row * 180, 120, 110, ink)
        d.rectangle([760, 860, 960, 1080], fill=(70, 56, 44), outline=ink, width=4)
        d.rectangle([200, 700, 380, 1040], outline=mid, width=3)
        d.rectangle([1360, 680, 1560, 1040], outline=mid, width=3)
    elif n == '04':
        d.rectangle([0, 0, W, 280], fill=(90, 72, 54))
        d.rectangle([0, 280, W, H], fill=(150, 128, 100))
        for i in range(6):
            d.line([(0, 40 + i * 36), (W, 20 + i * 30)], fill=soot, width=4)
        d.rectangle([180, 520, 1540, 980], fill=(120, 96, 72), outline=ink, width=5)
        for i in range(3):
            x = 420 + i * 320
            d.rectangle([x, 620, x + 180, 860], outline=ink, width=3)
            fig(d, x + 90, 480, 160, ink if i != 1 else rust)
        d.rectangle([80, 360, 280, 700], outline=mid, width=4)
    elif n == '05':
        d.rectangle([0, 0, W, H], fill=(160, 140, 112))
        d.rectangle([80, 80, 1640, 400], fill=(110, 88, 66), outline=ink, width=4)
        d.rectangle([620, 180, 1120, 360], fill=(220, 206, 180), outline=ink, width=3)
        for i in range(14):
            fig(d, 140 + (i % 7) * 220, 520 + (i // 7) * 220, 150, mid if i % 2 else ink)
    elif n == '06':
        d.rectangle([0, 0, W, 480], fill=(150, 138, 114))
        d.rectangle([0, 480, W, H], fill=(70, 82, 86))
        d.polygon([(200, 700), (1400, 620), (1500, 920), (280, 1000)], fill=(110, 86, 62), outline=ink)
        d.line([(980, 220), (980, 680)], fill=ink, width=5)
        d.polygon([(980, 250), (1280, 460), (980, 560)], outline=ink, width=3)
        for i in range(5):
            d.rectangle([360 + i * 40, 640 - i * 18, 900, 760 - i * 10], outline=(40, 32, 24), width=3)
        d.rectangle([1180, 300, 1240, 680], fill=soot)
    elif n == '07':
        d.rectangle([0, 0, W, 460], fill=(170, 154, 126))
        d.rectangle([0, 620, W, H], fill=(124, 108, 82))
        d.polygon([(200, 620), (1500, 620), (1728, H), (0, H)], fill=(140, 122, 96))
        d.rectangle([80, 280, 520, 700], fill=(132, 108, 80), outline=ink, width=5)
        d.polygon([(80, 280), (300, 140), (520, 280)], outline=ink, width=4)
        d.rectangle([220, 460, 340, 700], fill=(50, 42, 34))
        for i in range(5):
            fig(d, 700 + i * 90, 640, 200, ink)
            d.line([(700 + i * 90, 700), (700 + i * 90, 560)], fill=soot, width=3)
        for i in range(4):
            fig(d, 1080 + i * 140, 820, 140, rust, lean=16)
            d.ellipse([1140 + i * 140, 900, 1220 + i * 140, 960], outline=mid, width=2)
    else:
        d.rectangle([0, 0, W, 500], fill=(176, 158, 128))
        d.rectangle([0, 700, W, H], fill=(130, 114, 88))
        d.rectangle([640, 300, 1200, 860], outline=ink, width=6)
        d.line([(640, 300), (920, 140), (1200, 300)], fill=ink, width=4)
        d.rectangle([860, 620, 980, 860], outline=ink, width=3)
        d.rectangle([200, 760, 520, 980], fill=(90, 70, 48), outline=ink, width=4)
        for i in range(4):
            d.rectangle([220, 780 + i * 40, 500, 810 + i * 40], outline=soot, width=2)
        d.polygon([(1280, 820), (1600, 800), (1620, 980), (1300, 1000)], outline=ink, width=4)
        d.ellipse([1320, 960, 1400, 1040], outline=ink, width=3)
        d.ellipse([1500, 960, 1580, 1040], outline=ink, width=3)
        d.rectangle([760, 900, 860, 1040], fill=(160, 140, 110), outline=rust, width=4)
        for i in range(6):
            fig(d, 180 + i * 80, 560, 100, mid)
    for i in range(0, W, 21):
        d.line([(i, 0), (i - 180, H)], fill=(200, 186, 166), width=1)
    return grade(im.filter(ImageFilter.SMOOTH_MORE))

NAMES = [
    '01-galway-house.jpg','02-clear-title.jpg','03-henrietta-front.jpg','04-stable-court.jpg',
    '05-estate-sale.jpg','06-timber-ship.jpg','07-cleared-road.jpg','08-lismanny-stone.jpg',
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
print('ch16 panels done')
