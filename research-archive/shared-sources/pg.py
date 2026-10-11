import re,sys
f=sys.argv[1]; lines=open(f,errors='ignore').read().split('\n')
hdr=re.compile(r'^\s*(\d{1,3})\s+[A-Z][A-Z\'\-\s,\.]{4,}|[A-Z][A-Z\'\-\s,\.]{4,}\s+(\d{1,3})\s*$')
for a in sys.argv[2:]:
    n=int(a)-1
    prev=nxt=None
    for i in range(n,-1,-1):
        m=hdr.search(lines[i])
        if m and len(lines[i])<70: prev=(i+1,lines[i].strip()); break
    for i in range(n,len(lines)):
        m=hdr.search(lines[i])
        if m and len(lines[i])<70: nxt=(i+1,lines[i].strip()); break
    print(a,'PREV',prev,'NEXT',nxt)
