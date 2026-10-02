#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import hashlib, random
root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)
NAMES = [
 '01-trustees-and-minor.jpg','02-christies-and-debt.jpg','03-wyndham-bonus.jpg','04-athy-meeting.jpg',
 '05-eighteen-under-an-hour.jpg','06-castledermot-after.jpg','07-sale-closes.jpg','08-leinster-terms-spread.jpg']
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
  d.rectangle([60,60,W-60,H-60],outline=ink,width=5)
  d.rectangle([200,200,700,900],outline=ink,width=3); fig(d,450,500,280,mid)
  d.rectangle([900,250,1500,850],fill=(70,55,40),outline=ink,width=4)
  fig(d,1100,500,300,ink); fig(d,1300,520,280,ink)
  d.rectangle([1000,700,1200,820],outline=rust,width=2)
 elif n=='02':
  d.rectangle([80,80,W-80,H-80],outline=ink,width=5)
  for i in range(6):
   x=150+i*250; d.rectangle([x,250,x+200,700],outline=ink,width=3)
   d.ellipse([x+40,320,x+160,480],outline=mid,width=2)
  fig(d,860,780,200,rust)
 elif n=='03':
  d.rectangle([100,100,1620,1050],outline=ink,width=5)
  d.rectangle([400,200,1320,500],outline=rust,width=4)
  for i in range(3): d.rectangle([500,280+i*50,1200,320+i*50],outline=mid,width=1)
  fig(d,860,620,300,ink)
 elif n=='04':
  d.rectangle([40,40,W-40,H-40],outline=ink,width=4)
  d.rectangle([200,400,1520,700],fill=(160,140,110),outline=ink,width=3)
  for i in range(12): fig(d,280+i*110,480,180,mid,rng.randint(-8,8))
  fig(d,860,280,200,rust)
 elif n=='05':
  d.rectangle([60,60,W-60,H-60],outline=ink,width=5)
  d.rectangle([200,500,1520,780],fill=(150,130,105),outline=ink,width=4)
  fig(d,400,400,220,ink)
  for i in range(9): fig(d,600+i*100,520,160,mid)
  d.ellipse([300,200,500,350],outline=rust,width=2)
 elif n=='06':
  d.rectangle([0,0,W,500],fill=(195,180,155)); d.rectangle([0,500,W,H],fill=(150,140,120))
  for i in range(5):
   x=150+i*300; d.polygon([(x,520),(x+80,380),(x+160,520)],outline=ink,width=2)
  for i in range(8): fig(d,300+i*150,700,180,mid,rng.randint(-10,10))
  fig(d,860,650,220,rust)
 elif n=='07':
  d.rectangle([80,80,W-80,H-80],outline=ink,width=5)
  for row in range(4):
   for col in range(6):
    x=150+col*250; y=200+row*200
    d.rectangle([x,y,x+200,y+150],outline=ink,width=2)
  fig(d,860,900,160,rust)
 else:
  d.rectangle([60,60,W-60,H-60],outline=ink,width=5)
  for i in range(3):
   x=200+i*450; d.rectangle([x,250,x+350,700],outline=ink,width=3); fig(d,x+175,500,220,ink)
  d.rectangle([500,800,1200,1000],outline=rust,width=3)
  for i in range(4): d.rectangle([550+i*8,850+i*6,900+i*8,950+i*6],outline=mid,width=1)
 for i in range(0,W,14): d.line([(i,0),(i-200,H)],fill=(200,185,165),width=1)
 return grade(im.filter(ImageFilter.SMOOTH_MORE))
for name in NAMES:
 path=root/name
 if path.exists() and path.stat().st_size>80000: print('keep',path,path.stat().st_size); continue
 synth(name).save(path,'JPEG',quality=85,optimize=True); print('synth',path,path.stat().st_size)
print('ch22 panels done')
