import copy, re, shutil, docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
SRC='/workspace/book/04-narrative.docx'; OUT='/workspace/book/09-narrative.docx'
shutil.copy(SRC, OUT)
d=docx.Document(OUT)
P=d.paragraphs
T={k:copy.deepcopy(P[i]._p) for k,i in dict(label=0,title=1,place=2,first=3,body=4,sep=8,scene=9,afterscene=10,blank=97,srchead=98,srcnote=99,srcnote2=100,bullet=101).items()}
body=d.element.body
for el in list(body):
    if not el.tag.endswith('sectPr'): body.remove(el)
sect=body[-1]
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def add(key,text,center=False):
    p=copy.deepcopy(T[key])
    runs=p.findall(W+'r')
    for r in runs[1:]: p.remove(r)
    if runs:
        r=runs[0]
        for c in list(r):
            if not c.tag.endswith('rPr'): r.remove(c)
        t=r.makeelement(W+'t',{}); t.text=text
        t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); r.append(t)
    sect.addprevious(p)
    para=docx.text.paragraph.Paragraph(p,d._body)
    if center: para.alignment=WD_ALIGN_PARAGRAPH.CENTER
    return para
md=open('/workspace/book/09-narrative.md').read()
fm,rest=md.split('---\n',2)[1:]
lines=[l for l in rest.split('\n')]
anchors=["It described what a grower would see.","We sorted them on the floor by the fire","Mr. H. Burton of Carrigaholt Castle","The sack is twenty stone.","Some of the men on our road were strong at Easter.","The store opened at six in the morning","Father Theobald Mathew made the journey"]
n_img=0; prev=None; insources=False
add('label','Chapter 9')
for l in lines:
    if not l.strip(): continue
    if l.startswith('# '): add('title',l[2:]); prev='title'; continue
    if l.strip()=='* * *': add('sep','* * *'); prev='sep'; continue
    if l.strip()=='---': add('blank',''); insources=True; continue
    if l.startswith('## '): add('srchead',l[3:]); continue
    if insources:
        if l.startswith('- '): add('bullet','\u2022  '+l[2:])
        elif l.startswith('First-person'): add('srcnote',l)
        else: add('srcnote2',l)
        continue
    if l.startswith('*') and l.endswith('*'):
        add('place' if prev=='title' else 'scene', l[1:-1]); prev='placeline'; continue
    add('first' if prev=='placeline' and False else ('afterscene' if prev=='placeline' else 'body'), l)
    prev='body'
    for a in anchors:
        if l.startswith(a):
            n_img+=1; add('body',f'[[IMAGE {n_img}]]',center=True)
d.save(OUT); print('images',n_img)
