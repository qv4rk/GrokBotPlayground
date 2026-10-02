#!/usr/bin/env python3
"""Generate chapter-06 panels on CI (pollinations + ochre grade)."""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw
import io, time, urllib.parse, urllib.request

root = Path(__file__).resolve().parent / "panels"
root.mkdir(parents=True, exist_ok=True)
panels = [
    ("01-ibrahim-nizam.jpg", "graphic novel ink line ochre soot paper 1830s Ottoman Syria Ibrahim Pasha nizam soldiers entering city gate dignified faces no text no captions"),
    ("02-jerusalem-summons.jpg", "graphic novel ink ochre soot 1834 Jerusalem council table Ibrahim facing Palestinian notables mufti and sheikhs dignified no text"),
    ("03-self-mutilation.jpg", "graphic novel ink ochre soot village youths rendering themselves unfit for musket conscription lime near eye sombre dignified no gore no text"),
    ("04-dung-gate.jpg", "graphic novel ink ochre soot rebels emerging from sewer under Jerusalem Dung Gate peasants streaming in 1834 no text"),
    ("05-safed-looting.jpg", "graphic novel ink ochre soot Safed Jewish quarter aftermath wrecked Hebrew press torn Torah scrolls smoke 1834 dignified no gore no text"),
    ("06-ein-al-zeitun.jpg", "graphic novel ink ochre soot Arab village sheikh sheltering Jewish boy Jacob Saphir Ein al-Zeitun olive trees dignified no text"),
    ("07-hebron-sack.jpg", "graphic novel ink ochre soot Egyptian troops entering Hebron closed Jewish doorway street 1834 sombre no gore no text"),
    ("08-earthquake-safed.jpg", "graphic novel ink ochre soot Safed rubble after 1837 earthquake vineyards olives tended in valley travellers distant no text"),
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
    if path.exists() and path.stat().st_size > 20000:
        print("keep", path)
        continue
    ok = False
    for attempt in range(5):
        try:
            q = urllib.parse.quote(prompt)
            seed = abs(hash(name)) % 100000
            url = f"https://image.pollinations.ai/prompt/{q}?width=1280&height=896&nologo=true&seed={seed}"
            print("fetch", name, attempt, flush=True)
            req = urllib.request.Request(url, headers={"User-Agent": "qv4rk-ch06-bot"})
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            im = Image.open(io.BytesIO(data))
            grade(im).save(path, "JPEG", quality=82, optimize=True)
            print("wrote", path, path.stat().st_size, flush=True)
            ok = True
            break
        except Exception as e:
            print("fail", name, e, flush=True)
            time.sleep(4 + attempt * 3)
    if not ok:
        im = Image.new("RGB", (1728, 1152), (237, 228, 212))
        d = ImageDraw.Draw(im)
        d.rectangle([40, 40, 1688, 1112], outline=(42, 34, 24), width=4)
        d.text((100, 120), name, fill=(42, 34, 24))
        im.save(path, "JPEG", quality=85)
        print("synth", path, flush=True)
