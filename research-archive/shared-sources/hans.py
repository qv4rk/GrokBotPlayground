import sys,re,html,subprocess
url=sys.argv[1]
base,anchor=url.split('#')
t=subprocess.run(['curl','-sL','-m','40','https://api.parliament.uk'+base],capture_output=True,text=True).stdout
title=re.findall(r'<title>(.*?)</title>',t)
print('TITLE',title)
i=t.find('id="'+anchor+'"')
seg=t[i:]
# end at next member contribution div
m=re.search(r'<div class="hentry member_contribution" id="',seg[10:])
seg=seg[:m.start()+10] if m else seg[:20000]
s=html.unescape(re.sub(r'<[^>]+>',' ',seg))
s=re.sub(r'[ \t]+',' ',s)
s=re.sub(r'\n\s*\n+','\n',s)
print(s[:int(sys.argv[2]) if len(sys.argv)>2 else 6000])
