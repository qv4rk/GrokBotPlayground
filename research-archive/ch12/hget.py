import sys,re,html,urllib.request,time,os
def get(url):
    for i in range(5):
        try:
            s=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read().decode('utf8'); break
        except Exception as e:
            time.sleep(3); s=None
    if s is None: return 'FAILED'
    t=re.sub(r'<script.*?</script>','',s,flags=re.S)
    t=re.sub(r'<(br|p|div|h\d|li|blockquote)[^>]*>','\n',t)
    t=re.sub(r'<[^>]+>','',t); t=html.unescape(t)
    t=re.sub(r'Search Help.*?(Commons|Lords) Sitting','',t,flags=re.S)
    t=re.sub(r'Noticed a typo.*','',t,flags=re.S)
    t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    return t
for u in sys.argv[1:]:
    fn='hans/'+u.split('historic-hansard/')[1].replace('/','_')+'.txt'
    if os.path.exists(fn) and os.path.getsize(fn)>200: continue
    open(fn,'w').write(get(u))
