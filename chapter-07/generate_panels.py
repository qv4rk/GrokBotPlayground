#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import hashlib, random
root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)
NAMES = [
 '01-caisse-ledger.jpg','02-alexandria-forts.jpg','03-grand-square.jpg','04-tel-el-kebir.jpg',
 '05-adviser-veto.jpg','06-ric-blueprint.jpg','07-black-turban.jpg','08-gendarmerie.jpg']
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
  d.rectangle([160,140,1280,980],fill=(222,212,194),outline=ink,width=6)
  for i in range(12):
   d.line([(240,240+i*52),(1100,240+i*52)],fill=mid,width=2)
  for i in range(4):
   fig(d,1380,300+i*180,150,rust if i%2==0 else ink)
  d.rectangle([260,860,700,960],outline=rust,width=3)
  d.rectangle([760,860,1100,960],outline=ink,width=3)
 elif n=='02':
  d.rectangle([0,0,W,620],fill=(176,164,142))
  d.rectangle([0,620,W,H],fill=(58,72,84))
  for i in range(3):
   x=180+i*420
   d.polygon([(x,620),(x+80,360),(x+200,360),(x+280,620)],fill=(110,90,72),outline=ink)
  for i in range(4):
   x=200+i*380
   d.polygon([(x,860),(x+260,780),(x+300,900),(x+40,960)],fill=(32,30,28),outline=ink)
   d.line([(x+140,780),(x+120,680)],fill=ink,width=3)
 elif n=='03':
  d.rectangle([0,700,W,H],fill=(150,132,108))
  for i in range(7):
   x=80+i*230
   d.rectangle([x,280,x+180,720],outline=ink,width=3)
   d.polygon([(x,280),(x+90,180),(x+180,280)],outline=ink)
   d.polygon([(x+40,400),(x+140,360),(x+150,520)],fill=(70,58,48))
  d.rectangle([40,860,900,1040],fill=(90,74,60),outline=ink,width=3)
  d.rectangle([1180,200,1680,1040],fill=(62,78,90))
  d.line([(1180,200),(1180,1040)],fill=ink,width=4)
 elif n=='04':
  d.rectangle([0,0,W,520],fill=(48,42,38))
  d.rectangle([0,520,W,H],fill=(120,104,84))
  d.line([(0,500),(W,460)],fill=(180,150,110),width=3)
  for i in range(6):
   x=120+i*260
   d.rectangle([x,640,x+180,820],outline=ink,width=2)
  fig(d,300,900,140,mid,-8); fig(d,480,920,130,ink,6)
  fig(d,1400,880,160,rust,10)
 elif n=='05':
  d.rectangle([200,180,1100,900],fill=(226,216,198),outline=ink,width=5)
  for i in range(9):
   d.rectangle([280,280+i*60,980,320+i*60],outline=mid,width=1)
  d.rectangle([820,520,980,600],outline=rust,width=4)
  d.rectangle([1180,300,1560,700],fill=(210,198,176),outline=ink,width=3)
  fig(d,1360,780,200,ink)
 elif n=='06':
  d.rectangle([60,160,820,980],fill=(130,110,90),outline=ink,width=6)
  for i in range(5):
   fig(d,180+i*120,620,240,ink if i%2==0 else rust,0)
   d.line([(200+i*120,700),(230+i*120,760)],fill=ink,width=4)
  d.rectangle([980,200,1660,980],fill=(200,188,166),outline=ink,width=3)
  fig(d,1300,640,280,mid)
  d.ellipse([1460,180,1600,300],outline=(190,170,130),width=3)
 elif n=='07':
  d.rectangle([0,640,W,H],fill=(140,124,100))
  for i in range(6):
   x=40+i*280
   d.rectangle([x,220,x+240,660],outline=ink,width=3)
   d.rectangle([x+40,320,x+100,420],outline=mid,width=2)
  for i in range(7):
   x=160+i*210
   fig(d,x,860,200,mid,rng.randint(-6,6))
   d.ellipse([x-22,640,x+22,690],fill=(30,26,22))
 else:
  d.rectangle([0,760,W,H],fill=(100,112,120))
  d.polygon([(80,780),(360,700),(400,860),(60,900)],fill=(36,32,28),outline=ink)
  d.rectangle([200,280,720,620],fill=(224,214,196),outline=ink,width=4)
  for i in range(5):
   d.line([(250,340+i*40),(660,340+i*40)],fill=mid,width=2)
  for i in range(8):
   fig(d,860+i*100,780,200,rust if i%3==0 else ink,rng.randint(-8,8))
   d.line([(840+i*100,860),(870+i*100,920)],fill=ink,width=3)
 for i in range(0,W,14): d.line([(i,0),(i-200,H)],fill=(200,185,165),width=1)
 return grade(im.filter(ImageFilter.SMOOTH_MORE))
for name in NAMES:
 path=root/name
 if path.exists() and path.stat().st_size>80000: print('keep',path,path.stat().st_size); continue
 synth(name).save(path,'JPEG',quality=85,optimize=True); print('synth',path,path.stat().st_size)
print('ch07 panels done')
