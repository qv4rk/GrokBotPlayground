#!/usr/bin/env python3
"""Chapter 19 panels. Idempotent: keep an existing jpg above 80kb."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random

ROOT = Path(__file__).resolve().parent / "panels"
ROOT.mkdir(parents=True, exist_ok=True)
W, H = 1728, 1152
NAMES = [
    "01-acre-ships.jpg",
    "02-porte-desk.jpg",
    "03-tapu-square.jpg",
    "04-musha-strips.jpg",
    "05-notable-ink.jpg",
    "06-salam-debt.jpg",
    "07-jezreel-beirut.jpg",
    "08-afuleh-deed.jpg",
]
PAPER = (237, 228, 212)
INK = (42, 34, 24)
SOOT = (28, 24, 20)
OCHRE = (168, 122, 72)
RUST = (107, 58, 42)
MID = (92, 74, 54)
WASH = (214, 196, 168)

def rng_for(name):
    return random.Random(sum(ord(c) * (i + 3) for i, c in enumerate(name)) + 19)

def grain(im, rng, n=14000):
    px = im.load()
    for _ in range(n):
        x, y = rng.randrange(W), rng.randrange(H)
        r, g, b = px[x, y]
        v = rng.randint(-18, 10)
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v - 2)))

def figure(d, x, y, h, ink=INK, lean=0):
    r = max(10, h // 10)
    d.ellipse([x - r + lean // 5, y - 2 * r, x + r + lean // 5, y], fill=ink)
    sy = y + h // 12
    hem = y + int(h * 0.62)
    d.polygon([(x - h // 5, sy), (x + h // 5, sy), (x + h // 7 + lean, hem), (x - h // 7 + lean, hem)], fill=ink)
    d.polygon([(x - h // 11 + lean, hem), (x - 1 + lean, hem), (x - h // 8, y + h), (x - h // 5, y + h)], fill=ink)
    d.polygon([(x + 1 + lean, hem), (x + h // 11 + lean, hem), (x + h // 5, y + h), (x + h // 8, y + h)], fill=ink)
    d.polygon([(x - h // 5, sy + 4), (x - h // 3, sy + h // 5), (x - h // 4, sy + h // 3), (x - h // 8, sy + h // 6)], fill=ink)

def base():
    return Image.new("RGB", (W, H), PAPER)

def p_ships(rng):
    im = base(); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,620], fill=(70,78,82))
    d.rectangle([0,620,W,H], fill=(48,62,70))
    d.polygon([(40,520),(280,480),(420,560),(380,700),(80,740)], fill=(120,100,78), outline=INK)
    d.polygon([(300,500),(520,430),(560,640),(340,700)], fill=(90,72,54), outline=INK)
    d.rectangle([180,360,260,520], fill=(70,56,42), outline=INK)
    d.polygon([(160,360),(220,280),(280,360)], fill=(60,48,36))
    for i,x in enumerate((700,980,1260,1500)):
        y = 430 + (i%2)*40
        d.polygon([(x,y+80),(x+160,y+70),(x+150,y+140),(x+20,y+150)], fill=(36,30,26), outline=OCHRE)
        d.line([(x+80,y+80),(x+70,y)], fill=OCHRE, width=3)
        d.polygon([(x+70,y),(x+110,y+30),(x+40,y+36)], fill=(150,130,100))
    grain(im, rng, 7000); return im

def p_desk(rng):
    im = base(); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,H], fill=(92,74,56))
    d.rectangle([160,520,1500,980], fill=(62,46,32), outline=INK, width=5)
    d.rectangle([420,280,1180,760], fill=(230,220,200), outline=INK, width=4)
    d.rectangle([460,320,1140,720], outline=RUST, width=2)
    for k in range(6):
        d.line([(520,400+k*40),(1080,400+k*40)], fill=(180,150,120), width=2)
    d.ellipse([980,640,1220,820], fill=(160,140,110))
    figure(d, 1320, 460, 280, SOOT, lean=-8)
    d.rectangle([80,180,360,420], fill=(40,32,26), outline=OCHRE, width=3)
    grain(im, rng, 6000); return im

def p_square(rng):
    im = base(); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,420], fill=(186,160,120))
    d.rectangle([0,420,W,H], fill=(140,112,78))
    for i,x in enumerate((40,260,1480)):
        d.polygon([(x,420),(x+80,280),(x+180,300),(x+200,420)], fill=(110,86,62), outline=INK)
    d.rectangle([760,640,1040,860], fill=(70,54,40), outline=INK, width=3)
    d.polygon([(820,560),(980,520),(1000,700),(800,720)], fill=(226,214,190), outline=INK)
    figure(d, 900, 500, 240, SOOT, lean=4)
    for i,x in enumerate((180,340,500,1200,1360,1520)):
        figure(d, x, 620, 200+ (i%3)*20, (40,32,26) if i%2==0 else (80,62,44), lean=(-6 if i<3 else 6))
    grain(im, rng, 6000); return im

def p_strips(rng):
    im = base(); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,280], fill=(176,168,140))
    colors = [(150,120,70),(120,100,60),(168,140,80),(100,86,54),(140,110,64),(90,78,48)]
    for i in range(9):
        y0 = 260 + i*90
        d.polygon([(0,y0),(W,y0-40),(W,y0+50),(0,y0+90)], fill=colors[i%len(colors)])
    for i,x in enumerate((80,260,440)):
        d.rectangle([x,80,x+120,240], fill=(100,78,56), outline=INK, width=2)
        figure(d, x+60, 200, 90, SOOT)
    d.ellipse([1200,40,1600,240], outline=OCHRE, width=3)
    grain(im, rng, 5000); return im

def p_notable(rng):
    im = base(); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,H], fill=(70,58,46))
    d.rectangle([860,120,1620,1000], fill=(130,108,84), outline=INK, width=5)
    d.rectangle([1080,620,1280,1000], fill=(28,22,18))
    for row in range(3):
        d.rectangle([980,200+row*140,1140,300+row*140], outline=INK, width=3)
        d.rectangle([1360,200+row*140,1520,300+row*140], outline=INK, width=3)
    figure(d, 1180, 480, 200, SOOT)
    d.rectangle([1240,560,1480,700], fill=(226,216,196), outline=RUST, width=3)
    for i,x in enumerate((120,280,440,600)):
        figure(d, x, 640, 220, (36,28,22), lean=8)
    grain(im, rng, 6000); return im

def p_salam(rng):
    im = base(); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,H], fill=(88,70,52))
    for i in range(8):
        d.ellipse([80+i*70,700,150+i*70,770], fill=OCHRE, outline=INK, width=2)
    for i in range(4):
        d.polygon([(80+i*140,400),(160+i*140,360),(240+i*140,400),(220+i*140,620),(100+i*140,620)], fill=(150,120,70), outline=INK)
    d.rectangle([1100,280,1560,860], fill=(228,216,196), outline=INK, width=4)
    for k in range(7):
        d.line([(1160,360+k*50),(1500,360+k*50)], fill=RUST, width=2)
    figure(d, 980, 520, 260, SOOT, lean=12)
    grain(im, rng, 6000); return im

def p_plain(rng):
    im = base(); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,360], fill=(186,174,148))
    d.rectangle([0,360,W,H], fill=(130,112,70))
    for i in range(14):
        y = 400+i*48
        d.line([(0,y),(W-420,y+12)], fill=(100,82,48), width=3)
    for x in (200,520,860):
        d.polygon([(x,520),(x+40,460),(x+90,470),(x+100,540)], fill=(90,70,50), outline=INK)
    d.rectangle([1380,160,1660,520], fill=(150,130,100), outline=INK, width=4)
    d.polygon([(1360,160),(1520,60),(1680,160)], fill=(80,60,44))
    d.line([(1100,700),(1400,480)], fill=(70,56,40), width=6)
    figure(d, 1240, 560, 140, SOOT, lean=10)
    grain(im, rng, 5000); return im

def p_leave(rng):
    im = base(); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,H], fill=(168,150,122))
    for i,x in enumerate((60,240,420)):
        d.rectangle([x,360,x+160,640], fill=(110,86,64), outline=INK, width=3)
        d.polygon([(x-10,360),(x+80,260),(x+170,360)], fill=(70,52,38))
    d.rectangle([980,180,1560,820], fill=(230,220,200), outline=INK, width=5)
    d.rectangle([1040,240,1500,760], outline=RUST, width=3)
    for k in range(8):
        d.line([(1100,320+k*46),(1460,320+k*46)], fill=(150,110,90), width=2)
    figure(d, 860, 520, 240, (30,26,22))
    figure(d, 760, 560, 200, (50,40,32))
    for i,x in enumerate((180,320,470)):
        figure(d, x, 760, 180, SOOT, lean=-12)
        d.ellipse([x+20,860,x+70,910], fill=(80,60,40), outline=INK)
    grain(im, rng, 6000); return im

DRAW = {
    "01": p_ships, "02": p_desk, "03": p_square, "04": p_strips,
    "05": p_notable, "06": p_salam, "07": p_plain, "08": p_leave,
}

def finish(im, rng):
    px = im.load()
    for y in range(0, H, 2):
        row = rng.randint(-8, 6)
        for x in range(0, W, 2):
            v = row + rng.randint(-16, 12)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r+v)), max(0, min(255, g+v-1)), max(0, min(255, b+v-3)))
    d = ImageDraw.Draw(im)
    for i in range(0, W, 9):
        d.line([(i, 0), (i-260, H)], fill=(198, 182, 158), width=1)
    return im.filter(ImageFilter.SMOOTH)

def main():
    for name in NAMES:
        path = ROOT / name
        if path.exists() and path.stat().st_size > 80000:
            print("keep", path, path.stat().st_size); continue
        seed = rng_for(name)
        im = finish(DRAW[name[:2]](seed), seed)
        im.save(path, "JPEG", quality=86, optimize=True)
        print("synth", path, path.stat().st_size)

if __name__ == "__main__":
    main()
