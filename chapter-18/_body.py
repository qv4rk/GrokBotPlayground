#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import hashlib, random
root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)
NAMES = [
 '01-talk-down-looters.jpg','02-portobello-bridge-arrest.jpg','03-human-shield-raid.jpg','04-barracks-yard-wall.jpg',
 '05-vane-to-london.jpg','06-private-court-martial.jpg','07-gpo-and-liffey.jpg','08-hanna-refuses.jpg']
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
  d.rectangle([40,40,W-40,H-40],outline=ink,width=4)
  for i in range(4):
   x0=80+i*400; d.rectangle([x0,120,x0+340,620],outline=ink,width=3)
   d.line([(x0+40,200),(x0+300,280)],fill=mid,width=2); d.line([(x0+60,300),(x0+280,220)],fill=mid,width=2)
  for row in range(6):
   y=680+row*70
   for col in range(14):
    x=60+col*120+(row%2)*40; d.ellipse([x,y,x+90,y+40],outline=mid,width=1)
  fig(d,720,640,280,rust)
  for i,lx in enumerate([420,540,980,1120,1280]):
   fig(d,lx,700+(i%2)*20,200,mid,rng.randint(-10,10)); d.rectangle([lx-40,860,lx+40,920],outline=ink,width=2)
 elif n=='02':
  d.rectangle([0,0,W,420],fill=(200,185,160)); d.rectangle([0,700,W,H],fill=(150,140,120))
  d.rectangle([0,520,W,700],fill=(120,110,95))
  d.polygon([(80,520),(200,380),(1520,380),(1640,520),(1640,580),(80,580)],outline=ink,width=4)
  d.line([(200,380),(200,280)],fill=ink,width=3); d.line([(1520,380),(1520,280)],fill=ink,width=3)
  d.arc([200,480,1520,720],200,340,fill=ink,width=3)
  d.line([(860,280),(860,200)],fill=ink,width=2); d.ellipse([830,160,890,220],outline=rust,width=3)
  fig(d,780,400,220,rust); fig(d,920,390,240,ink); fig(d,1040,400,230,ink); fig(d,660,410,210,mid)
 elif n=='03':
  d.rectangle([0,0,W,H],fill=(210,198,178))
  d.rectangle([0,0,420,H],fill=(160,145,120),outline=ink,width=3)
  d.rectangle([1300,0,W,H],fill=(160,145,120),outline=ink,width=3)
  for y in range(80,H,160):
   d.rectangle([80,y,280,y+100],outline=ink,width=2); d.rectangle([1420,y,1620,y+100],fill=(50,45,35),outline=ink,width=2)
  d.rectangle([420,900,1300,H],fill=(170,155,130)); fig(d,700,620,300,rust)
  for i,sx in enumerate([880,1000,1120,1220]):
   fig(d,sx,600+i*8,280,ink,5); d.line([(sx+20,680),(sx+120,620)],fill=ink,width=2)
 elif n=='04':
  d.rectangle([0,0,W,380],fill=(195,180,155)); d.rectangle([0,380,W,H],fill=(175,160,135))
  d.rectangle([80,200,1640,720],fill=(150,130,105),outline=ink,width=5)
  for row in range(8):
   for col in range(18):
    x=100+col*85+(row%2)*40; y=220+row*60; d.rectangle([x,y,x+75,y+50],outline=mid,width=1)
  for cx in (520,860,1200): fig(d,cx,520,260,rust)
  for sx in (300,480,660,840,1020,1200,1380):
   fig(d,sx,820,200,ink); d.line([(sx,880),(sx,780)],fill=ink,width=2)
 elif n=='05':
  d.rectangle([60,60,W-60,H-60],outline=ink,width=5)
  d.polygon([(200,200),(780,280),(780,900),(200,1000)],outline=ink,width=3)
  d.polygon([(1520,200),(940,280),(940,900),(1520,1000)],outline=ink,width=3)
  d.rectangle([780,280,940,900],fill=(70,55,40),outline=ink,width=4)
  d.ellipse([900,560,930,600],outline=rust,width=2); fig(d,860,620,280,rust)
  d.rectangle([700,700,820,820],outline=ink,width=2)
  for y in (350,550,750): d.rectangle([250,y,400,y+140],outline=mid,width=2)
 elif n=='06':
  d.rectangle([40,40,W-40,H-40],outline=ink,width=5)
  d.rectangle([120,120,480,480],outline=ink,width=3); d.line([(300,120),(300,480)],fill=ink,width=2)
  d.rectangle([1240,120,1600,480],outline=ink,width=3); d.line([(1420,120),(1420,480)],fill=ink,width=2)
  d.rectangle([200,560,1520,780],fill=(160,140,110),outline=ink,width=4)
  for i in range(6): fig(d,320+i*200,480,180,ink)
  d.rectangle([780,820,940,1020],outline=rust,width=3); d.line([(780,860),(940,860)],fill=rust,width=2)
  d.rectangle([700,600,900,700],outline=mid,width=2); d.ellipse([820,640,860,680],outline=rust,width=2)
 elif n=='07':
  d.rectangle([0,0,W,500],fill=(195,180,155)); d.rectangle([0,500,W,700],fill=(130,120,100)); d.rectangle([0,700,W,H],fill=(160,145,120))
  d.rectangle([200,180,1200,620],fill=(175,160,135),outline=ink,width=4)
  for i in range(6):
   x=260+i*150; d.rectangle([x,280,x+80,520],fill=(60,50,40),outline=ink,width=2); d.line([(x+10,300),(x+70,400)],fill=mid,width=2)
  for i in range(4):
   x=320+i*200; d.rectangle([x,400,x+40,620],outline=ink,width=2)
  d.polygon([(200,180),(700,80),(1200,180)],outline=ink,width=3)
  for sx,sy in [(500,60),(700,40),(900,70)]: d.ellipse([sx,sy,sx+120,sy+80],outline=mid,width=2)
  d.polygon([(1280,580),(1580,560),(1620,600),(1560,640),(1300,640)],fill=(50,45,35),outline=ink)
  d.rectangle([1450,500,1480,580],fill=(50,45,35))
  for cx in (300,420,1400): fig(d,cx,780,180,mid)
 else:
  d.rectangle([60,60,W-60,H-60],outline=ink,width=5)
  d.rectangle([200,200,700,900],outline=ink,width=3); d.line([(450,200),(450,900)],fill=mid,width=2)
  d.rectangle([1100,250,1500,850],fill=(70,55,40),outline=ink,width=4); d.ellipse([1420,520,1460,560],outline=rust,width=2)
  d.rectangle([500,700,1100,900],fill=(150,130,105),outline=ink,width=4)
  d.rectangle([520,720,700,820],outline=ink,width=2); d.ellipse([600,750,640,790],outline=rust,width=2)
  fig(d,900,520,320,rust); d.line([(900,600),(720,740)],fill=rust,width=3)
 for i in range(0,W,14): d.line([(i,0),(i-200,H)],fill=(200,185,165),width=1)
 return grade(im.filter(ImageFilter.SMOOTH_MORE))
for name in NAMES:
 path=root/name
 if path.exists() and path.stat().st_size>80000: print('keep',path,path.stat().st_size); continue
 synth(name).save(path,'JPEG',quality=85,optimize=True); print('synth',path,path.stat().st_size)
print('ch18 panels done')
