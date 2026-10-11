import docx, copy, re
SRC='/workspace/book/22-narrative.docx'; MD='/workspace/book/13-narrative.md'; OUT='/workspace/book/13-narrative.docx'
d=docx.Document(SRC); ps=d.paragraphs
proto={'label':ps[0],'title':ps[1],'places':ps[2],'body':ps[3],'image':ps[8],'sep':ps[9],'scene':ps[10],
       'blank':ps[155],'h2':ps[156],'note':ps[157],'bullet':ps[158],'small':ps[170]}
proto={k:copy.deepcopy(v._p) for k,v in proto.items()}
body=d.element.body
sect=body[-1] if body[-1].tag.endswith('sectPr') else None
for el in list(body):
    if el is not sect: body.remove(el)
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def add(kind,text,force_italic=None,raw=False):
    p=copy.deepcopy(proto[kind])
    runs=p.findall(W+'r')
    rpr=runs[0].find(W+'rPr') if runs else None
    for r in runs: p.remove(r)
    if text:
        parts=[text] if raw else re.split(r'(\*[^*]+\*)',text)
        for part in parts:
            if not part: continue
            it = (not raw) and part.startswith('*') and part.endswith('*') and len(part)>2
            t=part[1:-1] if it else part
            r=d.element.makeelement(W+'r',{})
            nr=copy.deepcopy(rpr) if rpr is not None else d.element.makeelement(W+'rPr',{})
            ital = force_italic if force_italic is not None else it
            if force_italic is not None and it: ital = not force_italic
            for i_el in nr.findall(W+'i'): nr.remove(i_el)
            i_el=d.element.makeelement(W+'i',{W+'val':'1' if ital else '0'})
            nr.append(i_el)
            r.append(nr)
            te=d.element.makeelement(W+'t',{'{http://www.w3.org/XML/1998/namespace}space':'preserve'})
            te.text=t; r.append(te); p.append(r)
    if sect is not None: sect.addprevious(p)
    else: body.append(p)
md=open(MD).read()
md=md.split('---',2)[2].strip('\n')
lines=[l for l in md.split('\n')]
add('label','Chapter 13')
mode='prose'
for l in lines:
    s=l.strip()
    if not s: continue
    if s.startswith('# '): add('title',s[2:]); continue
    if s=='## Sources': add('blank',''); add('h2','Sources'); mode='sources'; continue
    if s=='## Corrections to the original': add('blank',''); add('h2','Corrections to the original'); mode='corr'; continue
    if s=='* * *': add('sep','* * *',raw=True); continue
    if re.fullmatch(r'\[\[IMAGE \d\]\]',s): add('image',s); continue
    if mode=='prose':
        if s.startswith('*') and s.endswith('*') and s.count('*')==2:
            # places line (first) or scene heading
            kind='places' if not any(True for _ in []) and 'places_done' not in globals() else 'scene'
            if 'places_done' not in globals():
                globals()['places_done']=True; add('places',s[1:-1],force_italic=True)
            else: add('scene',s[1:-1],force_italic=True)
            continue
        add('body',s); continue
    # sources/corrections
    if s.startswith('- '): add('bullet','•  '+s[2:]); continue
    if s.startswith('First-person passages'): add('note',s,force_italic=True); continue
    add('small',s)
d.save(OUT); print('saved')
