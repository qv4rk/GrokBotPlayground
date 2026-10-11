import sys,re,html,subprocess
url=sys.argv[1]
base,anchor=url.split('#')
t=subprocess.run(['curl','-sL','-m','40','https://api.parliament.uk'+base],capture_output=True,text=True).stdout
print('TITLE',re.findall(r'<title>(.*?)</title>',t))
i=t.find("name='"+anchor+"'")
if i<0: i=t.find(anchor)
seg=t[i:]
m=re.search(r"class='speech-permalink",seg[2000:])
seg=seg[:m.start()+2000] if m else seg[:30000]
# keep column refs
seg=re.sub(r"<a[^>]*class='permalink column-permalink'[^>]*>([^<]*)</a>",r' [col. \1] ',seg)
s=html.unescape(re.sub(r'<[^>]+>',' ',seg))
s=re.sub(r'[ \t]+',' ',s); s=re.sub(r'\n\s*\n+','\n',s)
print(s[:int(sys.argv[2]) if len(sys.argv)>2 else 6000])
