#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import hashlib, random
root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)
NAMES = [
 '01-dadni-field.jpg','02-patna-factory.jpg','03-calcutta-hammer.jpg','04-canton-exchange.jpg',
 '05-hong-surety.jpg','06-humen-lime.jpg','07-commons-division.jpg','08-pearl-gunboats.jpg']
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
def chest(d,x,y,w,h,ink,fill):
 d.polygon([(x,y+h//5),(x+w//2,y),(x+w,y+h//5),(x+w,y+h),(x,y+h)],outline=ink,fill=fill)
 d.line([(x,y+h//5),(x+w,y+h//5)],fill=ink,width=2)
 d.line([(x+w//2,y),(x+w//2,y+h//5)],fill=ink,width=2)
def synth(name):
 W,H=1728,1152; rng=random.Random(int(hashlib.md5(name.encode()).hexdigest()[:8],16))
 im=Image.new('RGB',(W,H),(237,228,212)); d=ImageDraw.Draw(im); px=im.load()
 for _ in range(8000):
  x,y=rng.randrange(W),rng.randrange(H); v=rng.randint(-12,8); r,g,b=px[x,y]
  px[x,y]=(max(0,min(255,r+v)),max(0,min(255,g+v)),max(0,min(255,b+v)))
 ink,rust,mid=(42,34,24),(107,58,42),(90,70,50); n=name[:2]
 if n=='01':
  d.rectangle([0,620,W,H],fill=(168,150,118))
  for row in range(7):
   y=680+row*62
   d.line([(40,y),(W-40,y)],fill=(120,98,70),width=2)
   for i in range(28):
    x=70+i*58+ (row%2)*20
    d.ellipse([x,y-28,x+16,y-8],fill=rust if (i+row)%4==0 else mid)
  fig(d,280,560,220,ink)
  d.rectangle([210,430,360,500],fill=(230,222,205),outline=ink,width=3)
  for i in range(3): d.line([(230,448+i*14),(340,448+i*14)],fill=mid,width=1)
  d.ellipse([1480,180,1640,300],outline=(200,170,120),width=3)
 elif n=='02':
  d.rectangle([80,160,1100,980],fill=(130,108,88),outline=ink,width=6)
  for i in range(6):
   d.rectangle([140+i*150,220,250+i*150,420],outline=(60,48,38),width=3)
  d.ellipse([200,520,420,700],outline=ink,width=4)
  d.ellipse([460,540,700,740],outline=rust,width=3)
  for i in range(8):
   d.ellipse([180+i*90,760,250+i*90,830],outline=ink,width=2)
  for i in range(4):
   chest(d,1180,220+i*210,420,180,ink,(150,128,100))
  fig(d,360,860,160,mid); fig(d,620,870,150,ink)
 elif n=='03':
  d.rectangle([0,0,W,280],fill=(92,74,58))
  d.polygon([(760,120),(820,40),(880,120)],fill=rust)
  d.line([(820,40),(900,220)],fill=ink,width=6)
  for i in range(5):
   for j in range(3):
    chest(d,160+i*200,360+j*220,160,140,ink,(160,140,112))
  for i in range(9):
   fig(d,180+i*160,980,140,mid if i%2 else ink, rng.randint(-8,8))
 elif n=='04':
  d.rectangle([0,520,W,H],fill=(70,88,98))
  d.rectangle([0,0,W,520],fill=(186,170,146))
  for i in range(8):
   x=80+i*200
   h=280+ (i%3)*70
   d.rectangle([x,520-h,x+150,540],fill=(110,90,70),outline=ink,width=3)
   d.rectangle([x+30,520-h+40,x+70,520-h+90],outline=(210,196,170),width=2)
   d.rectangle([x+85,520-h+40,x+125,520-h+90],outline=(210,196,170),width=2)
  d.polygon([(200,780),(520,700),(560,860),(180,920)],outline=(40,36,30),fill=(48,44,38))
  for i in range(6):
   d.rectangle([980+ (i%3)*180, 640+(i//3)*160, 1120+(i%3)*180, 740+(i//3)*160], fill=(190,175,145), outline=ink, width=2)
  for i in range(5):
   chest(d,200+i*90,980,70,80,ink,(120,90,60))
 elif n=='05':
  d.rectangle([120,140,1600,1000],fill=(214,204,186),outline=ink,width=5)
  for i in range(14):
   d.line([(220,240+i*46),(1280,240+i*46)],fill=mid,width=2)
  d.rectangle([220,220,420,300],outline=rust,width=3)
  fig(d,1420,620,280,ink)
  d.rectangle([1340,360,1560,520],fill=(186,168,140),outline=ink,width=3)
  for i in range(4): d.line([(1360,390+i*24),(1540,390+i*24)],fill=mid,width=1)
 elif n=='06':
  d.rectangle([0,700,W,H],fill=(150,142,120))
  d.polygon([(0,700),(400,520),(900,640),(1400,480),(W,620),(W,700)],fill=(120,108,86))
  for i in range(6):
   x=180+i*240
   d.ellipse([x,760,x+200,980],fill=(214,206,170),outline=ink,width=3)
   chest(d,x+40,700,120,110,ink,(100,78,58))
  fig(d,240,560,180,ink); fig(d,1480,540,200,rust)
  d.rectangle([1280,220,1620,480],fill=(226,216,196),outline=ink,width=3)
  for i in range(5): d.line([(1320,270+i*32),(1560,270+i*32)],fill=mid,width=1)
 elif n=='07':
  d.pieslice([200,180,1520,2100],start=200,end=340,fill=(168,150,128),outline=ink,width=4)
  for i in range(11):
   d.arc([260+i*18,200+i*8,1460-i*18,1900],start=210,end=330,fill=ink,width=2)
  d.rectangle([760,860,960,1040],fill=(90,70,55),outline=ink,width=4)
  fig(d,500,720,200,mid); fig(d,620,700,210,ink)
  fig(d,1120,700,210,rust); fig(d,1240,720,200,mid)
  d.rectangle([180,180,460,320],outline=rust,width=3)
  d.rectangle([1260,180,1560,340],outline=ink,width=3)
 else:
  d.rectangle([0,640,W,H],fill=(62,78,90))
  d.rectangle([0,0,W,640],fill=(176,164,140))
  d.polygon([(40,640),(220,520),(520,640)],fill=(100,86,68),outline=ink)
  for i in range(4):
   x=180+i*380
   d.polygon([(x,700),(x+280,640),(x+300,820),(x+40,860)],fill=(36,32,28),outline=ink)
   d.line([(x+140,640),(x+120,520)],fill=ink,width=3)
   d.polygon([(x+90,520),(x+150,470),(x+180,530)],fill=(70,62,52))
  d.ellipse([1460,80,1660,240],outline=(200,186,150),width=2)
 for i in range(0,W,14): d.line([(i,0),(i-200,H)],fill=(200,185,165),width=1)
 return grade(im.filter(ImageFilter.SMOOTH_MORE))
for name in NAMES:
 path=root/name
 if path.exists() and path.stat().st_size>80000: print('keep',path,path.stat().st_size); continue
 synth(name).save(path,'JPEG',quality=85,optimize=True); print('synth',path,path.stat().st_size)
print('ch05 panels done')
