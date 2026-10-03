#!/usr/bin/env python3
"""Chapter 04 — eight beats, not one image per paragraph.
Crotty's house taught a Clare parish not to build anything worth taking.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import hashlib, random

root = Path(__file__).resolve().parent / 'panels'
root.mkdir(parents=True, exist_ok=True)
NAMES = [
 '01-conacre-strip.jpg','02-paving-the-house.jpg','03-onto-the-highway.jpg','04-timber-left-down.jpg',
 '05-kilrush-oath.jpg','06-ennis-counter.jpg','07-quinpool-gate.jpg','08-courthouse-lets-out.jpg']
INK, RUST, SOOT, OCHRE = (42,34,24), (107,58,42), (55,48,40), (168,132,86)
PAPER, MUD, THATCH, LIME = (237,228,212), (122,98,72), (154,120,74), (214,204,184)

def grade(im):
 im=im.convert('RGB').resize((1728,1152), Image.Resampling.LANCZOS)
 g=ImageOps.grayscale(im)
 sep=Image.merge('RGB',(g.point(lambda x:min(255,int(x*1.05+18))),g.point(lambda x:min(255,int(x*0.90+8))),g.point(lambda x:min(255,int(x*0.68)))))
 return ImageEnhance.Contrast(sep).enhance(1.14)

def grain(im, rng):
 px=im.load(); w,h=im.size
 for _ in range(7000):
  x,y=rng.randrange(w),rng.randrange(h); v=rng.randint(-14,10); r,g,b=px[x,y]
  px[x,y]=(max(0,min(255,r+v)),max(0,min(255,g+v)),max(0,min(255,b+v)))

def fig(d,x,y,h,ink=INK,lean=0,coat=None):
 r=max(7,h//9)
 d.ellipse([x-r,y-2*r,x+r,y],outline=ink,width=2)
 d.line([(x,y),(x+lean,y+h//2)],fill=ink,width=3)
 d.line([(x+lean,y+h//2),(x-h//5,y+h)],fill=ink,width=2)
 d.line([(x+lean,y+h//2),(x+h//5,y+h)],fill=ink,width=2)
 d.line([(x,y+h//5),(x-h//4,y+h//3)],fill=ink,width=2)
 d.line([(x,y+h//5),(x+h//4,y+h//3)],fill=ink,width=2)
 if coat:
  d.polygon([(x-r-4,y+4),(x+r+4,y+4),(x+r+10,y+h//2),(x-r-10,y+h//2)],outline=coat,width=2)

def hatch_ridge(d,y,x0,x1,dark=False):
 fill=(112,88,56) if dark else OCHRE
 d.polygon([(x0,y),(x1,y+16),(x1,y+48),(x0,y+32)],fill=fill,outline=INK)
 x=x0+24
 while x<x1-16:
  d.ellipse([x,y+10,x+9,y+22],fill=(62,86,46),outline=SOOT); x+=34

def p_conacre(d,W,H,rng):
 d.rectangle([0,0,W,220],fill=(206,194,168)); d.rectangle([0,220,W,H],fill=(128,104,70))
 d.rectangle([0,240,70,H],fill=(108,100,90),outline=INK,width=4)
 d.rectangle([W-70,260,W,H],fill=(108,100,90),outline=INK,width=4)
 d.ellipse([160,250,460,420],fill=(92,62,40),outline=INK,width=3)
 for i in range(8): hatch_ridge(d,430+i*78,100,W-100,dark=(i%2==0))
 fig(d,280,300,200,INK,8); fig(d,430,330,170,RUST,-6)
 d.line([(700,240),(700,400)],fill=SOOT,width=4)

def p_paving(d,W,H,rng):
 d.rectangle([0,0,W,H],fill=(198,184,156))
 d.polygon([(0,H),(0,780),(W,700),(W,H)],fill=(150,132,104))
 d.rectangle([430,250,1080,760],fill=LIME,outline=INK,width=5)
 d.polygon([(390,250),(755,40),(1120,250)],fill=RUST,outline=INK,width=4)
 d.rectangle([680,470,860,760],fill=(48,40,32),outline=INK,width=3)
 for wx,wy in ((500,340),(920,340),(500,520)):
  d.rectangle([wx,wy,wx+100,wy+90],fill=(226,216,190),outline=INK,width=2)
  d.line([(wx+50,wy),(wx+50,wy+90)],fill=INK,width=2)
 d.line([(1180,500),(1180,200)],fill=SOOT,width=6)
 d.line([(1120,500),(1240,500)],fill=SOOT,width=4); d.line([(1120,360),(1240,360)],fill=SOOT,width=4)
 fig(d,1200,260,150,INK,4)
 d.rectangle([1120,520,1460,800],fill=(186,170,146),outline=INK,width=3)
 d.rectangle([1460,620,1660,800],fill=(170,154,130),outline=INK,width=3)
 fig(d,360,860,120,RUST,20)
 for i in range(6): d.rectangle([180+i*70,980,240+i*70,1040],outline=SOOT,width=2)
 for i in range(7): d.rectangle([200+(i%7)*90,860,280+(i%7)*90,910],outline=INK,width=2)

def p_highway(d,W,H,rng):
 d.rectangle([0,0,780,H],fill=(176,162,140))
 d.rectangle([80,60,700,900],fill=LIME,outline=INK,width=6)
 d.polygon([(60,60),(390,0),(720,80)],fill=(120,72,52))
 d.rectangle([300,380,500,900],fill=(28,24,20),outline=INK,width=6)
 d.ellipse([455,620,478,644],fill=OCHRE)
 d.rectangle([140,200,250,320],fill=(40,36,30),outline=INK,width=2)
 d.rectangle([520,200,630,320],fill=(40,36,30),outline=INK,width=2)
 fig(d,640,560,240,SOOT,-8)
 d.polygon([(760,H),(860,620),(W,700),(W,H)],fill=(158,136,98),outline=INK)
 fig(d,1040,760,220,INK,14); fig(d,1220,800,160,RUST,12); fig(d,1380,840,110,SOOT,10)
 d.polygon([(1120,900),(1168,880),(1155,940),(1105,930)],outline=RUST,width=3)

def p_timber(d,W,H,rng):
 d.rectangle([0,0,W,360],fill=(188,176,152)); d.rectangle([0,360,W,H],fill=(146,124,96))
 def cabin(x,y,w=200):
  d.polygon([(x,y),(x+w//2,y-70),(x+w,y)],fill=THATCH,outline=INK,width=2)
  d.rectangle([x+8,y,x+w-8,y+130],fill=MUD,outline=INK,width=2)
  d.rectangle([x+w//2-16,y+50,x+w//2+16,y+130],fill=SOOT)
 cabin(60,520); cabin(300,560,170); cabin(1280,500,220); cabin(1520,560,160)
 for i in range(5):
  d.polygon([(560,620+i*36),(1180,560+i*36),(1180,584+i*36),(560,644+i*36)],fill=(92,64,42),outline=INK,width=2)
 for i in range(8): d.rectangle([600+i*62,860,650+i*62,980],fill=(120,116,108),outline=INK,width=2)
 for i,x in enumerate((420,1480,250)): fig(d,x,780,200,INK if i!=1 else RUST,-18 if i==0 else 16)

def p_oath(d,W,H,rng):
 d.rectangle([0,0,W,H],fill=(150,132,108))
 d.rectangle([40,40,W-40,H-40],outline=INK,width=8)
 d.rectangle([1260,80,1600,420],fill=(230,220,196),outline=INK,width=4)
 d.line([(1430,80),(1430,420)],fill=INK,width=3); d.line([(1260,250),(1600,250)],fill=INK,width=3)
 d.polygon([(220,520),(1500,430),(1560,700),(280,800)],fill=(112,78,52),outline=INK,width=4)
 for i in range(6):
  fig(d,380+i*170,300,140,SOOT,0)
  d.rectangle([330+i*170,470,450+i*170,520],fill=(70,56,44),outline=INK)
 fig(d,240,640,340,INK,2,coat=RUST)
 for i in range(5): d.rectangle([460+i*150,520,580+i*150,580],fill=LIME,outline=SOOT)

def p_bank(d,W,H,rng):
 d.rectangle([0,0,W,H],fill=(168,156,136)); d.rectangle([0,0,W,180],fill=(96,74,56),outline=INK,width=3)
 for i in range(14): d.line([(80+i*70,180),(80+i*70,520)],fill=INK,width=3)
 d.rectangle([60,500,W-60,680],fill=(120,86,56),outline=INK,width=5)
 d.rectangle([1180,300,1500,480],fill=(70,54,40),outline=OCHRE,width=4)
 fig(d,1320,180,150,SOOT,0); fig(d,520,760,280,INK,0)
 d.line([(430,980),(360,1040)],fill=INK,width=3); d.line([(610,980),(690,1040)],fill=INK,width=3)
 d.ellipse([340,1025,390,1065],outline=INK,width=2); d.ellipse([670,1025,720,1065],outline=INK,width=2)

def p_gate(d,W,H,rng):
 d.rectangle([0,0,W,H],fill=(92,74,58))
 d.ellipse([1200,-140,1720,360],fill=(150,120,86))
 d.ellipse([-40,20,520,620],fill=(48,56,40),outline=INK,width=3)
 d.rectangle([160,460,230,H],fill=(42,34,26))
 d.rectangle([1360,500,1420,1100],fill=SOOT,outline=INK,width=3)
 d.rectangle([1620,540,1680,1100],fill=SOOT,outline=INK,width=3)
 for i in range(5): d.line([(1400,580+i*80),(1640,620+i*80)],fill=INK,width=4)
 fig(d,640,600,400,INK,12); fig(d,1020,620,380,RUST,-14)
 d.line([(820,940),(920,900)],fill=INK,width=4); d.line([(940,910),(860,960)],fill=RUST,width=4)
 for i in range(6): d.ellipse([860+i*22,900,894+i*22,934],outline=OCHRE,width=3)

def p_letsout(d,W,H,rng):
 d.rectangle([0,0,W,420],fill=(214,202,178)); d.rectangle([0,420,W,H],fill=(168,150,118))
 d.rectangle([0,460,W,560],fill=(150,132,100))
 d.polygon([(40,540),(90,500),(140,540)],fill=THATCH,outline=INK)
 d.polygon([(200,545),(250,505),(300,545)],fill=THATCH,outline=INK)
 d.polygon([(1500,530),(1560,490),(1620,530)],fill=THATCH,outline=INK)
 d.rectangle([360,200,1380,760],fill=(186,172,148),outline=INK,width=5)
 for x in (460,700,980,1200):
  d.rectangle([x,260,x+70,760],fill=(160,144,120),outline=INK,width=4)
 d.polygon([(320,200),(860,40),(1420,200)],fill=(110,78,56),outline=INK,width=3)
 d.rectangle([760,480,980,760],fill=(36,30,26),outline=INK,width=4)
 for i in range(5):
  y=760+i*50
  d.rectangle([300-i*30,y,1440+i*16,y+48],fill=(140,124,100),outline=INK,width=2)
 for i in range(7): fig(d,260+i*180,900,130+(i%3)*10,INK if i%2==0 else SOOT,rng.randint(-8,12))

SCENES={'01':p_conacre,'02':p_paving,'03':p_highway,'04':p_timber,'05':p_oath,'06':p_bank,'07':p_gate,'08':p_letsout}

def synth(name):
 W,H=1728,1152
 rng=random.Random(int(hashlib.md5(('ch04-'+name).encode()).hexdigest()[:8],16))
 im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im); grain(im,rng)
 SCENES[name[:2]](d,W,H,rng)
 for i in range(0,W,22): d.line([(i,0),(i-140,H)],fill=(206,190,168),width=1)
 return grade(im.filter(ImageFilter.SMOOTH_MORE))

for name in NAMES:
 path=root/name
 if path.exists() and path.stat().st_size>80000:
  print('keep',path,path.stat().st_size); continue
 synth(name).save(path,'JPEG',quality=85,optimize=True); print('synth',path,path.stat().st_size)
print('ch04 panels done')
