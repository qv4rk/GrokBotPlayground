import sys
from bs4 import BeautifulSoup
s=BeautifulSoup(open(sys.argv[1]).read(),'html.parser')
m=s.find(id='content') or s
for t in m.find_all(['a']):
    if t.get('class') and 'permalink' in t.get('class'): t.decompose()
out=[]
for el in m.find_all(['p','h1','h2','h3','h4','blockquote','cite']):
    if el.name=='p' and el.find_parent('blockquote'): continue
    tx=el.get_text(' ',strip=True)
    if tx: out.append(tx)
print('\n\n'.join(out))
