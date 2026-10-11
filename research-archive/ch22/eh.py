import re,html,sys,subprocess
u=sys.argv[1]
t=subprocess.run(['curl','-sL','-m','40','https://kildarelibraries.ie/ehistory/'+u+'/'],capture_output=True,text=True).stdout
i=t.find('<h1'); t=t[i:]
j=t.find('Articles: '); t=t[:j] if j>0 else t
s=html.unescape(re.sub(r'<[^>]+>','\n',t)); s=re.sub(r'\n\s*\n+','\n',s)
open(u+'.txt','w').write(s); print(len(s))
