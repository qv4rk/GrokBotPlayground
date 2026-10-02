#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import hashlib, random
root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)
NAMES = [
 '01-yabad-cave.jpg','02-haifa-funeral.jpg','03-april-strike.jpg','04-white-paper.jpg',
 '05-irgun-lehi.jpg','06-king-david.jpg','07-haganah-council.jpg','08-un-referral.jpg']
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
 d.line([(x,y+h//5),(x-h//5,y+h//3)],fill=ink,width=2)
 d.line([(x,y+h//5),(x+h//5,y+h//3)],fill=ink,width=2)
def synth(name):
 W,H=1728,1152; rng=random.Random(int(hashlib.md5(name.encode()).hexdigest()[:8],16))
 im=Image.new('RGB',(W,H),(237,228,212)); d=ImageDraw.Draw(im); px=im.load()
 for _ in range(8000):
  x,y=rng.randrange(W),rng.randrange(H); v=rng.randint(-12,8); r,g,b=px[x,y]
  px[x,y]=(max(0,min(255,r+v)),max(0,min(255,g+v)),max(0,min(255,b+v)))
 ink,rust,mid=(42,34,24),(107,58,42),(90,70,50); n=name[:2]
 if n=='01':
  d.ellipse([180,220,900,980],fill=(55,48,38),outline=ink,width=5)
  d.ellipse([280,340,780,860],fill=(35,30,24),outline=ink,width=3)
  fig(d,480,620,180,mid); fig(d,580,640,160,ink); fig(d,680,630,170,mid)
  for i in range(6): fig(d,1050+i*90,700,200,rust if i%2==0 else mid,rng.randint(-6,6))
  d.polygon([(100,980),(400,700),(700,980)],outline=ink,width=2)
 elif n=='02':
  d.rectangle([0,0,W,420],fill=(190,175,150)); d.rectangle([0,420,W,H],fill=(160,145,120))
  d.rectangle([600,380,1120,520],fill=(70,55,40),outline=ink,width=4)
  for i in range(18):
   fig(d,120+i*90,560+rng.randint(-20,40),180+rng.randint(-20,40),mid if i%3 else ink,rng.randint(-10,10))
  for i in range(10):
   fig(d,200+i*140,780,160,rust if i%2==0 else mid,rng.randint(-8,8))
 elif n=='03':
  d.rectangle([40,40,W-40,H-40],outline=ink,width=4)
  for i in range(5):
   x=80+i*320
   d.rectangle([x,180,x+280,700],outline=ink,width=3)
   d.rectangle([x+40,280,x+240,520],fill=(120,100,80),outline=ink,width=2)
   d.line([(x+40,400),(x+240,400)],fill=rust,width=3)
  for i in range(8): fig(d,200+i*180,820,180,mid,rng.randint(-8,8))
 elif n=='04':
  d.rectangle([60,60,W-60,H-60],outline=ink,width=5)
  for i in range(10):
   fig(d,120+i*70,620,220,mid if i%2 else ink,0)
  d.rectangle([900,200,1580,700],outline=rust,width=4)
  d.rectangle([980,280,1500,620],fill=(220,210,190),outline=ink,width=2)
  for i in range(5): d.rectangle([1040,320+i*50,1440,350+i*50],outline=mid,width=1)
  fig(d,1240,780,200,rust)
 elif n=='05':
  d.rectangle([0,0,W,500],fill=(70,60,50)); d.rectangle([0,500,W,H],fill=(100,90,75))
  d.rectangle([200,280,700,900],outline=ink,width=4)
  d.rectangle([350,500,550,900],fill=(40,35,28),outline=ink,width=3)
  fig(d,900,620,240,ink); fig(d,1050,640,220,mid); fig(d,1200,610,250,rust)
  d.ellipse([1400,180,1550,320],outline=(200,185,150),width=2)
 elif n=='06':
  d.rectangle([100,150,1400,750],outline=ink,width=5)
  for i in range(4):
   d.rectangle([180+i*280,220,400+i*280,450],outline=mid,width=2)
  d.polygon([(900,750),(1400,750),(1400,400),(1100,750)],fill=(90,75,60),outline=ink,width=3)
  for i in range(3):
   x=250+i*120; d.ellipse([x,820,x+80,980],outline=rust,width=3)
  fig(d,600,880,140,mid); fig(d,750,870,150,ink)
 elif n=='07':
  d.rectangle([80,80,W-80,H-80],outline=ink,width=5)
  d.rectangle([300,500,1420,720],fill=(150,130,105),outline=ink,width=3)
  for i in range(6):
   fig(d,400+i*160,420,200,mid if i!=2 else rust)
  d.rectangle([860,540,1060,700],outline=rust,width=2)
  fig(d,500,780,180,ink); fig(d,1200,780,180,ink)
 else:
  d.rectangle([60,60,W-60,H-60],outline=ink,width=5)
  d.rectangle([200,250,1520,450],fill=(80,65,50),outline=ink,width=4)
  for i in range(14): fig(d,260+i*95,300,120,mid)
  d.rectangle([500,600,1220,950],outline=rust,width=4)
  d.rectangle([560,660,1160,880],fill=(215,205,185),outline=ink,width=2)
  for i in range(4): d.rectangle([620,700+i*40,1100,725+i*40],outline=mid,width=1)
  fig(d,860,980,100,ink)
 for i in range(0,W,14): d.line([(i,0),(i-200,H)],fill=(200,185,165),width=1)
 return grade(im.filter(ImageFilter.SMOOTH_MORE))
for name in NAMES:
 path=root/name
 if path.exists() and path.stat().st_size>80000: print('keep',path,path.stat().st_size); continue
 synth(name).save(path,'JPEG',quality=85,optimize=True); print('synth',path,path.stat().st_size)
print('ch26 panels done')
