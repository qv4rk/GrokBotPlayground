import shutil, re, copy
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
src='/workspace/book/09-narrative.docx'; out='/workspace/book/03-narrative.docx'
shutil.copy(src,out)
d=Document(out)
body=d.element.body
for el in list(body):
    if el.tag!=qn('w:sectPr'): body.remove(el)
for rId,rel in list(d.part.rels.items()):
    if rel.reltype.endswith('/image'): del d.part.rels[rId]
sect=body.find(qn('w:sectPr'))
FONT='Palatino Linotype'
def para(text, *, italic=False, color=None, sz=None, jc=None, before=None, after=None, first0=True, hang=False):
    p=OxmlElement('w:p'); pPr=OxmlElement('w:pPr')
    if before is not None or after is not None:
        s=OxmlElement('w:spacing')
        if before is not None: s.set(qn('w:before'),str(before))
        if after is not None: s.set(qn('w:after'),str(after))
        pPr.append(s)
    ind=OxmlElement('w:ind')
    if hang: ind.set(qn('w:left'),'432'); ind.set(qn('w:hanging'),'432'); pPr.append(ind)
    elif first0: ind.set(qn('w:firstLine'),'0'); pPr.append(ind)
    if jc: j=OxmlElement('w:jc'); j.set(qn('w:val'),jc); pPr.append(j)
    if len(pPr): p.append(pPr)
    r=OxmlElement('w:r'); rPr=OxmlElement('w:rPr')
    f=OxmlElement('w:rFonts')
    for k in ('ascii','hAnsi','cs'): f.set(qn('w:'+k),FONT)
    f.set(qn('w:eastAsia'),'SimSun'); rPr.append(f)
    i=OxmlElement('w:i')
    if not italic: i.set(qn('w:val'),'0')
    rPr.append(i)
    if color: c=OxmlElement('w:color'); c.set(qn('w:val'),color); rPr.append(c)
    if sz: z=OxmlElement('w:sz'); z.set(qn('w:val'),str(sz)); rPr.append(z)
    r.append(rPr); t=OxmlElement('w:t'); t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); t.text=text; r.append(t); p.append(r)
    sect.addprevious(p)
md=open('/workspace/book/03-narrative.md').read()
md=md.split('---\n',2)[2]
blocks=[b.strip() for b in md.split('\n\n') if b.strip()]
anchors=["In the hay season of 1834","A cross-bearer led","Gold. The gold on them.","The chapel was colder than outside.","The stream comes out under the wall","They were packed against the door","In August a long letter came from Connemara."]
used=[]; n=0
para('Chapter 3',color='6B3A2A',sz=24,jc='center',before=1440,after=120)
state='body'; fresh=True
for b in blocks:
    if b.startswith('# '):
        para(b[2:],color='2A2218',sz=44,jc='center',after=200); continue
    if b=='---': state='back'; continue
    if b.startswith('## '):
        para(b[3:],color='2A2218',sz=32,after=200,before=(240 if 'Corrections' in b else None)); continue
    if state=='back':
        if b.startswith('- ') or '\n- ' in b:
            lines=b.split('\n')
            for ln in lines:
                if ln.startswith('- '): para('•  '+ln[2:],sz=20,after=100,hang=True)
                else: para(ln,sz=20,after=100,italic=ln.endswith(':'))
        else:
            para(b,sz=20,after=100,italic=b.startswith('First-person'))
        continue
    if b=='* * *':
        para('* * *',color='6B3A2A',jc='center',before=280,after=280); fresh=True; continue
    if b.startswith('*') and b.endswith('*'):
        txt=b.strip('*')
        if txt.startswith('Castleconnell'): para(txt,italic=True,color='6B3A2A',jc='center',after=240)
        else: para(txt,italic=True,color='6B3A2A',jc='left',after=160)
        fresh=True; continue
    assert '*' not in b, b[:40]
    para(b,first0=fresh); fresh=False
    for a in anchors:
        if b.startswith(a) and a not in used:
            used.append(a); n+=1
            para(f'[[IMAGE {n}]]',jc='center',before=200,after=200); fresh=True
assert n==len(anchors),used
d.save(out)
print('placeholders',n)
