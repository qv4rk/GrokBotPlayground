#!/usr/bin/env python3
"""Chapter 13 panels. Idempotent: keep a jpg already over 80kb."""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import hashlib, random

root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)

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
    for _ in range(22000):
        x, y = rng.randrange(W), rng.randrange(H)
        v = rng.randint(-16, 10)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))
    ink, rust, mid = (42, 34, 24), (107, 58, 42), (90, 70, 50)
    soot = (55, 46, 36)
    n = name[:2]
    if n == '01':
        d.rectangle([0, 0, W, 520], fill=(48, 42, 36))
        d.rectangle([0, 520, W, H], fill=(32, 36, 40))
        d.polygon([(200, 640), (1480, 560), (1600, 780), (120, 860)], fill=(70, 64, 54), outline=ink)
        d.polygon([(980, 300), (1500, 340), (1500, 560), (1040, 520)], fill=(90, 78, 62), outline=ink)
        d.rectangle([1180, 180, 1220, 340], fill=ink)
        d.rectangle([1080, 400, 1280, 470], fill=(60, 52, 42), outline=ink)
        for i in range(5):
            d.rectangle([260 + i * 90, 700, 330 + i * 90, 780], outline=(200, 180, 150), width=3)
        for i in range(4):
            x = 300 + i * 280
            d.rectangle([x, 820, x + 200, 980], outline=ink, width=4)
            d.ellipse([x + 20, 960, x + 70, 1020], outline=ink, width=3)
            d.ellipse([x + 130, 960, x + 180, 1020], outline=ink, width=3)
        coat(d, 700, 600, 180, rust)
        coat(d, 860, 620, 170, mid)
    elif n == '02':
        d.rectangle([0, 0, W, 400], fill=(176, 160, 132))
        d.rectangle([0, 400, W, H], fill=(140, 124, 98))
        d.rectangle([80, 180, 1640, 980], outline=ink, width=5)
        for i in range(3):
            d.rectangle([140 + i * 500, 220, 520 + i * 500, 460], outline=ink, width=3)
            window(d, 220 + i * 500, 280, 80, 90, ink)
        for i in range(8):
            coat(d, 260 + i * 160, 620, 220, ink if i % 2 == 0 else mid)
        d.rectangle([700, 900, 1040, 1020], outline=rust, width=3)
    elif n == '03':
        d.rectangle([0, 0, W, H], fill=(206, 192, 168))
        d.rectangle([180, 420, 1200, 980], fill=(120, 96, 72), outline=ink, width=6)
        d.rectangle([360, 250, 980, 460], fill=(226, 214, 190), outline=ink, width=4)
        for i in range(6):
            d.line([(420, 300 + i * 22), (900, 300 + i * 22)], fill=mid, width=1)
        d.rectangle([80, 160, 280, 700], outline=ink, width=4)
        window(d, 1320, 120, 280, 360, ink)
        coat(d, 1280, 560, 260, ink)
        d.rectangle([1040, 700, 1160, 900], outline=mid, width=3)
    elif n == '04':
        d.rectangle([0, 0, W, 420], fill=(92, 84, 70))
        d.rectangle([0, 420, W, H], fill=(58, 62, 66))
        for i in range(6):
            y = 480 + i * 90
            d.arc([-200 + i * 40, y, W + 200, y + 220], 200, 340, fill=(150, 140, 120), width=4)
        d.polygon([(700, 620), (1080, 560), (1120, 700), (760, 760)], fill=(150, 132, 108), outline=ink)
        d.line([(900, 300), (900, 620)], fill=ink, width=4)
        d.polygon([(900, 340), (1100, 500), (900, 560)], outline=ink, width=3)
        coat(d, 860, 480, 120, rust)
    elif n == '05':
        d.rectangle([0, 0, W, 480], fill=(196, 178, 146))
        d.rectangle([0, 700, W, H], fill=(150, 132, 108))
        d.rectangle([0, 480, W, 720], fill=(86, 98, 104))
        d.rectangle([80, 620, 1500, 780], fill=(130, 114, 92), outline=ink, width=4)
        d.polygon([(980, 360), (1460, 420), (1460, 680), (1040, 640)], fill=(170, 150, 120), outline=ink, width=4)
        d.line([(1220, 180), (1220, 420)], fill=ink, width=4)
        d.polygon([(1220, 200), (1400, 340), (1220, 400)], fill=(210, 196, 170), outline=ink)
        for i in range(4):
            d.rectangle([200 + i * 80, 640, 260 + i * 80, 720], outline=ink, width=3)
        for i in range(7):
            fig(d, 180 + i * 100, 820, 160, mid if i % 2 else ink)
    elif n == '06':
        d.rectangle([0, 0, W, 500], fill=(180, 164, 136))
        d.polygon([(600, 500), (1100, 500), (1500, H), (200, H)], fill=(122, 108, 82))
        d.rectangle([40, 220, 420, 520], outline=ink, width=4)
        d.polygon([(40, 220), (230, 120), (420, 220)], outline=ink, width=3)
        for i in range(8):
            y = 560 + i * 60
            fig(d, 780, y, 90, ink if i % 2 == 0 else mid)
            d.line([(820, y + 10), (900, y - 20)], fill=soot, width=3)
    elif n == '07':
        d.rectangle([0, 0, W, 360], fill=(168, 152, 124))
        d.rectangle([0, 360, W, H], fill=(118, 104, 84))
        d.rectangle([0, 200, W, 420], fill=(96, 84, 68))
        for i in range(9):
            coat(d, 140 + i * 170, 430, 220, ink)
            d.line([(140 + i * 170, 500), (140 + i * 170, 360)], fill=soot, width=3)
        for i in range(10):
            fig(d, 120 + i * 155, 860, 160, rust if i % 3 == 0 else mid)
        d.line([(0, 760), (W, 760)], fill=ink, width=4)
    else:
        d.rectangle([0, 0, W, 500], fill=(188, 170, 140))
        d.rectangle([0, 500, W, H], fill=(132, 116, 90))
        d.rectangle([200, 220, 420, 700], fill=(110, 92, 72), outline=ink, width=5)
        d.rectangle([1280, 240, 1520, 700], fill=(110, 92, 72), outline=ink, width=5)
        d.line([(420, 460), (200, 460)], fill=ink, width=6)
        d.polygon([(700, 560), (1020, 560), (1280, H), (440, H)], fill=(168, 150, 120))
        d.rectangle([760, 300, 980, 470], outline=mid, width=3)
        d.line([(760, 300), (980, 470)], fill=mid, width=2)
    for i in range(0, W, 18):
        d.line([(i, 0), (i - 240, H)], fill=(200, 186, 166), width=1)
    return grade(im.filter(ImageFilter.SMOOTH_MORE))

NAMES = [
    '01-larne-night.jpg','02-curragh-square.jpg','03-assurance-desk.jpg','04-asgard-storm.jpg',
    '05-howth-morning.jpg','06-volunteer-road.jpg','07-quay-stopped.jpg','08-open-gate.jpg']
for name in NAMES:
    path = root / name
    if path.exists() and path.stat().st_size > 80000:
        print('keep', path.name, path.stat().st_size)
        continue
    synth(name).save(path, 'JPEG', quality=86, optimize=True)
    print('synth', path.name, path.stat().st_size)
print('ch13 panels done')
