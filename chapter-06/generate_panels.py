#!/usr/bin/env python3
"""Generate chapter-06 panels on CI (pollinations + ochre grade)."""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw
import io, time, urllib.parse, urllib.request

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
panels = [
    ("01-ibrahim-nizam.jpg", "graphic novel ink line ochre soot paper 1830s Ottoman Syria Ibrahim Pasha nizam soldiers entering city gate dignified faces no text no captions"),
    ("02-jerusalem-summons.jpg", "graphic novel ink line ochre soot paper 1834 Jerusalem interior council table Ibrahim Pasha facing Palestinian notables mufti sheikhs dignified faces period dress no text no captions"),
    ("03-self-mutilation.jpg", "graphic novel ink ochre soot village youths rendering themselves unfit for musket conscription lime near eye sombre dignified no gore no text"),
    ("04-dung-gate.jpg", "graphic novel ink line ochre soot rebels crawling from ancient sewer under Jerusalem stone Dung Gate Bab al-Maghariba peasants with spears streaming into city 1834 no text no captions"),
    ("05-safed-looting.jpg", "graphic novel ink ochre soot Safed Jewish quarter aftermath wrecked Hebrew press torn Torah scrolls smoke 1834 dignified no gore no text"),
    ("06-ein-al-zeitun.jpg", "graphic novel ink line ochre soot Galilee Arab village courtyard olive trees unnamed sheikh sheltering twelve-year-old Jewish boy Jacob Saphir 1834 dignified faces no text no captions"),
    ("07-hebron-sack.jpg", "graphic novel ink ochre soot Egyptian troops entering Hebron closed Jewish doorway street 1834 sombre no gore no text"),
    ("08-earthquake-safed.jpg", "graphic novel ink line ochre soot Safed hillside town rubble after 1837 earthquake vineyards and olive groves still tended in valley distant travellers dust no text no captions"),
]

def grade(im):
    im = im.convert("RGB").resize((1728, 1152), Image.Resampling.LANCZOS)
    w, h = im.size
    im = im.crop((0, 0, w, int(h * 0.96))).resize((1728, 1152), Image.Resampling.LANCZOS)
    gray = ImageOps.grayscale(im)
    sep = Image.merge("RGB", (
        gray.point(lambda x: min(255, int(x * 1.05 + 20))),
        gray.point(lambda x: min(255, int(x * 0.9 + 10))),
        gray.point(lambda x: min(255, int(x * 0.7))),
    ))
    sep = ImageEnhance.Contrast(sep).enhance(1.15)
    sep = ImageEnhance.Color(sep).enhance(0.85)
    return sep

for name, prompt in panels:
    path = root / name
    # regenerate weak synth fallbacks (<60KB) and missing files
    if path.exists() and path.stat().st_size > 60000:
        print("keep", path, path.stat().st_size)
        continue
    if path.exists():
        path.unlink()
    ok = False
    for attempt in range(6):
        try:
            q = urllib.parse.quote(prompt)
            seed = (abs(hash(name)) + attempt * 9973) % 100000
            url = f"https://image.pollinations.ai/prompt/{q}?width=1280&height=896&nologo=true&seed={seed}"
            print("fetch", name, attempt, seed, flush=True)
            req = urllib.request.Request(url, headers={"User-Agent": "qv4rk-ch06-bot"})
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            if len(data) < 5000:
                raise RuntimeError(f"tiny response {len(data)}")
            im = Image.open(io.BytesIO(data))
            grade(im).save(path, "JPEG", quality=82, optimize=True)
            print("wrote", path, path.stat().st_size, flush=True)
            ok = True
            break
        except Exception as e:
            print("fail", name, e, flush=True)
            time.sleep(5 + attempt * 3)
    if not ok:
        im = Image.new("RGB", (1728, 1152), (237, 228, 212))
        d = ImageDraw.Draw(im)
        d.rectangle([40, 40, 1688, 1112], outline=(42, 34, 24), width=4)
        d.rectangle([80, 80, 1648, 280], fill=(210, 180, 140))
        d.text((100, 120), "THE LEDGER AND THE MOB", fill=(42, 34, 24))
        d.text((100, 180), name, fill=(107, 58, 42))
        im.save(path, "JPEG", quality=85)
        print("synth", path, flush=True)
