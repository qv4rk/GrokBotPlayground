#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import hashlib, random
root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)
NAMES = [
 '01-cabin-refused.jpg','02-steerage-huddled.jpg','03-fever-berths.jpg','04-open-barge-transfer.jpg',
 '05-grosse-ile-anchorage.jpg','06-quarantine-island.jpg','07-ontario-nursing.jpg','08-lords-and-committee.jpg']
def grade(im):
 im=im.convert('RGB').resize((1728,1152), Image.Resampling.LANCZOS)
 g=ImageOps.grayscale(im)
 sep=Image.merge('RGB',(g.point(lambda x:min(255,int(x*1.05+20))),g.point(lambda x:min(255,int(x*0.9+10))),g.point(lambda x:min(255,int(x*0.7)))))
 return ImageEnhance.Contrast(sep).enhance(1.15)
def fig(d,x,y,h,ink,lean=0):
 r=max(8,h//8); d.ellipse([x-r,y-2*r,x+r,y],outline=ink,width=2)
 d.line([(x,y),(x+lean,y+h//2)],fill=ink,width=3)
 d.line([(x+lean,y+h//2),(x-h//6,y+h)],fill=ink,width=2)
 d.line([(x+lean,y+h//2),(x+h//6,y+h)],fill=ink,width=2)
def synth(name):
 W,H=1728,1152; rng=random.Random(int(hashlib.md5(name.encode()).hexdigest()[:8],16))
 im=Image.new('RGB',(W,H),(237,228,212)); d=ImageDraw.Draw(im); px=im.load()
 for _ in range(8000):
  x,y=rng.randrange(W),rng.randrange(H); v=rng.randint(-12,8); r,g,b=px[x,y]
  px[x,y]=(max(0,min(255,r+v)),max(0,min(255,g+v)),max(0,min(255,b+v)))
 ink,rust,mid=(42,34,24),(107,58,42),(90,70,50); n=name[:2]
 if n=='01':
  d.rectangle([80,80,1640,1080],outline=ink,width=5); d.rectangle([200,200,700,950],outline=ink,width=3)
  fig(d,980,500,400,ink); d.rectangle([1100,500,1400,700],outline=rust,width=2)
 elif n=='02':
  d.rectangle([40,40,1688,1112],outline=ink,width=4)
  for row in range(4):
   y0=120+row*230; d.rectangle([100,y0,1620,y0+180],outline=ink,width=2)
   for col in range(6): fig(d,180+col*250,y0+80,100,mid)
  d.ellipse([800,80,920,200],outline=rust,width=2)
 elif n=='03':
  d.rectangle([60,60,1660,1090],outline=ink,width=4)
  for i in range(3):
   x0=120+i*520; d.rectangle([x0,280,x0+460,900],outline=ink,width=3)
   fig(d,x0+120,420,200,mid,10); fig(d,x0+300,450,180,mid,-8)
  d.ellipse([760,920,960,1050],outline=rust,width=3)
 elif n=='04':
  d.rectangle([0,0,W,520],fill=(210,195,170)); d.rectangle([0,700,W,H],fill=(160,145,120))
  for sx,sy,sc in [(200,380,.9),(1200,350,1.1)]:
   d.polygon([(sx,sy+80),(sx+int(180*sc),sy),(sx+int(360*sc),sy+80),(sx+int(320*sc),sy+160),(sx+40,sy+160)],outline=ink,width=3)
   d.line([(sx+int(180*sc),sy),(sx+int(180*sc),sy-int(220*sc))],fill=ink,width=2)
  d.polygon([(420,780),(500,640),(1200,650),(1300,800),(1150,920),(480,910)],outline=ink,width=4)
  for i in range(10): fig(d,540+i*70,720,140,ink,rng.randint(-8,8))
 elif n=='05':
  d.rectangle([0,0,W,520],fill=(200,185,160)); d.rectangle([0,520,W,H],fill=(150,140,120))
  d.ellipse([700,480,1100,620],fill=(120,100,70),outline=ink)
  d.polygon([(750,520),(820,400),(900,520),(980,380),(1050,520)],fill=(90,80,55),outline=ink)
  for i in range(20):
   x=80+(i%10)*160+rng.randint(-20,20); y=560+(i//10)*180+rng.randint(-30,30)
   d.polygon([(x,y),(x+25,y-70),(x+50,y)],outline=ink,width=2); d.line([(x+25,y-70),(x+25,y+40)],fill=ink,width=1)
 elif n=='06':
  d.rectangle([80,200,500,700],outline=ink,width=4); d.rectangle([220,400,360,700],fill=(60,50,40),outline=ink)
  d.rectangle([600,250,1000,720],outline=ink,width=3); d.rectangle([720,420,880,720],fill=(60,50,40),outline=ink)
  for i in range(8): fig(d,1140+(i%4)*120,560+(i//4)*160,120,mid)
  fig(d,485,820,160,rust)
 elif n=='07':
  d.rectangle([60,60,1660,1090],outline=ink,width=4)
  for i in range(4):
   x0=120+i*380; d.rectangle([x0,400,x0+320,700],outline=ink,width=2); d.ellipse([x0+100,320,x0+200,400],outline=mid,width=2)
  fig(d,860,620,280,rust)
 else:
  d.rectangle([100,100,1620,1050],outline=ink,width=5)
  for row in range(5): d.arc([200,350+row*120,1520,530+row*120],200,340,fill=ink,width=2)
  d.rectangle([700,200,1020,360],outline=rust,width=3); fig(d,860,200,160,ink)
  for i in range(4): d.rectangle([1100+i*8,220+i*6,1350+i*8,320+i*6],outline=mid,width=1)
 for i in range(0,W,14): d.line([(i,0),(i-200,H)],fill=(200,185,165),width=1)
 return grade(im.filter(ImageFilter.SMOOTH_MORE))
for name in NAMES:
 path=root/name
 if path.exists() and path.stat().st_size>80000: print('keep',path,path.stat().st_size); continue
 synth(name).save(path,'JPEG',quality=85,optimize=True); print('synth',path,path.stat().st_size)
print('ch14 panels done')
