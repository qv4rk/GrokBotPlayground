#!/usr/bin/env python3
"""Generate chapter-10 panels via pollinations + ochre grade."""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw
import io, time, urllib.parse, urllib.request, hashlib

root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)
panels = [
    ("01-lintin-to-crop.jpg", "graphic novel ink line ochre soot, 1839 China coast chests of opium becoming inland crop Yunnan Sichuan valleys poppy fields replacing foreign cargo, period accurate Qing landscape no text no captions"),
    ("02-yunnan-sichuan-earth.jpg", "graphic novel ink ochre soot, two grades inland opium poppy: Yunnan high valley white purple blossom and Sichuan red basin fields, farmers period dress Qing China 1839, dignified no text"),
    ("03-abandon-grain.jpg", "graphic novel ink ochre soot, irrigated Chinese valley floor under white purple poppy blossom instead of rice grain, Qing Southwest 1830s, abandon grain plant smoke, no text no captions"),
    ("04-grain-surplus-reverses.jpg", "graphic novel ink ochre soot, Yangzi corridor rice boats and market, Southwest counties buying grain in after poppy conversion, Qing China 1830s sombre, no text"),
    ("05-slogan-banner.jpg", "graphic novel ink ochre soot, armed syndicate on Sichuan mountain road 1841 meeting imperial troops, cloth banner with illegible brush strokes not readable English, muskets period Qing dress dignified no gore no text captions"),
    ("06-flower-smoke-rooms.jpg", "graphic novel ink ochre soot, Qing gentry flower-smoke room carved opium pipe silver lamp leisure interior 1839 China, dignified faces period furniture no text no captions"),
    ("07-cage-water.jpg", "graphic novel ink ochre soot, porters boatmen coolies drinking dark cup of pipe scrapings cage-water beside carrying poles, Qing China labourers sombre dignified no caricature no text"),
    ("08-likin-and-lin.jpg", "graphic novel ink ochre soot split mood: interior yamen clerk fee schedule coins on desk native drug likin, distant coast implied, Qing China 1839, Lin suppression far away, no readable modern text no captions"),
]

def grade(im):
    im = im.convert('RGB').resize((1728, 1152), Image.Resampling.LANCZOS)
    w, h = im.size
    im = im.crop((0, 0, w, int(h * 0.96))).resize((1728, 1152), Image.Resampling.LANCZOS)
    gray = ImageOps.grayscale(im)
    sep = Image.merge('RGB', (
        gray.point(lambda x: min(255, int(x * 1.05 + 20))),
        gray.point(lambda x: min(255, int(x * 0.9 + 10))),
        gray.point(lambda x: min(255, int(x * 0.7))),
    ))
    return ImageEnhance.Contrast(sep).enhance(1.15)

for name, prompt in panels:
    path = root / name
    if path.exists() and path.stat().st_size > 80000:
        print('keep', path, path.stat().st_size); continue
    ok=False
    for attempt in range(10):
        try:
            q=urllib.parse.quote(prompt)
            seed=int(hashlib.md5((name+str(attempt)).encode()).hexdigest()[:8],16)%100000
            url=f'https://image.pollinations.ai/prompt/{q}?width=1280&height=896&nologo=true&seed={seed}'
            print('fetch', name, attempt, seed, flush=True)
            req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 qv4rk-ch10'})
            with urllib.request.urlopen(req, timeout=180) as r:
                data=r.read()
            if len(data)<8000: raise RuntimeError('tiny')
            grade(Image.open(io.BytesIO(data))).save(path,'JPEG',quality=82,optimize=True)
            print('wrote', path, path.stat().st_size, flush=True)
            ok=True; break
        except Exception as e:
            print('fail', name, e, flush=True); time.sleep(5+attempt*2)
    if not ok:
        im=Image.new('RGB',(1728,1152),(237,228,212)); d=ImageDraw.Draw(im)
        d.rectangle([40,40,1688,1112],outline=(42,34,24),width=4)
        d.text((100,120),'POPPIES INLAND',fill=(42,34,24)); d.text((100,180),name,fill=(107,58,42))
        im.save(path,'JPEG',quality=85); print('synth', path)
print('ch10 panels done')
