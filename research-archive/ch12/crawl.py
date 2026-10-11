import re,urllib.request,time,sys
def get(u):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode('utf8')
        except Exception as e: time.sleep(2)
    return ''
B='https://api.parliament.uk'
months=[('1915',m) for m in ['feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']]+[('1916',m) for m in ['jan','feb','mar','apr']]
out=open('hans_index.tsv','w')
for y,m in months:
    s=get(f'{B}/historic-hansard/sittings/{y}/{m}')
    days=sorted(set(re.findall(rf'/historic-hansard/sittings/{y}/{m}/\d+',s)))
    for d in days:
        t=get(B+d)
        for href,title in re.findall(r'<a href="(/historic-hansard/(?:commons|lords|written_answers)/[^"]+)"[^>]*>([^<]+)</a>',t):
            out.write(f'{d.split("/sittings/")[1]}\t{title.strip()}\t{B}{href}\n')
        out.flush()
