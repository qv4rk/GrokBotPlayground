import re,html,subprocess,sys
base,name,pages=sys.argv[1],sys.argv[2],int(sys.argv[3])
out=[]
for p in range(1,pages+1):
    s=subprocess.run(['curl','-sL',f'{base}?page={p}'],capture_output=True,text=True).stdout
    s=re.sub(r'<script.*?</script>','',s,flags=re.S); s=re.sub(r'<style.*?</style>','',s,flags=re.S)
    t=html.unescape(re.sub(r'<[^>]+>','\n',s)); t=re.sub(r'\n\s*\n+','\n',t)
    i=t.find('Leaf'); j=t.find('Search in work')
    if i<0: break
    seg=t[i:j]
    seg=re.sub(r'This page is incomplete\nEdit this page\nLast edit[^\n]*\n[^\n]*\n','',seg)
    out.append(seg)
    if f'of \n' in t and 'Next' not in t: break
open(name,'w').write('\n'.join(out))
