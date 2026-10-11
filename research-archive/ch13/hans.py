import sys,re,html,urllib.request
def get(url):
    s=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})).read().decode('utf8')
    t=s
    t=re.sub(r'<script.*?</script>','',t,flags=re.S)
    t=re.sub(r'<(br|p|div|h\d|li|blockquote)[^>]*>','\n',t)
    t=re.sub(r'<[^>]+>','',t)
    t=html.unescape(t)
    t=re.sub(r'Search Help.*?(Commons|Lords) Sitting','',t,flags=re.S)
    t=re.sub(r'Noticed a typo.*','',t,flags=re.S)
    t=re.sub(r'[ \t]+',' ',t)
    t=re.sub(r'\n\s*\n+','\n\n',t)
    return t
for u in sys.argv[1:]:
    print('#####',u); print(get(u))
