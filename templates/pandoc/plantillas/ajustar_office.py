"""Compatibility adjustments after Pandoc. Only Python's standard library."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
import xml.etree.ElementTree as E
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
for pre,uri in NS.items():E.register_namespace(pre,uri)
def tag(s):a,b=s.split(':');return '{'+NS[a]+'}'+b
def child(p,s,**attrs):return E.SubElement(p,tag(s),attrs)
def fix_pptx(path,reference):
    with ZipFile(path) as z:files={n:z.read(n) for n in z.namelist()}
    with ZipFile(reference) as z:
        for n in z.namelist():
            if n.startswith('ppt/media/'):files[n]=z.read(n)
    types=E.fromstring(files['[Content_Types].xml'])
    ct='{http://schemas.openxmlformats.org/package/2006/content-types}'
    E.register_namespace('',ct[1:-1])
    if not any(e.get('Extension')=='png' for e in types):E.SubElement(types,ct+'Default',Extension='png',ContentType='image/png')
    files['[Content_Types].xml']=E.tostring(types,encoding='utf-8',xml_declaration=True)
    for n in list(files):
        if not(n.startswith('ppt/slides/slide') and n.endswith('.xml')):continue
        r=E.fromstring(files[n])
        for shape in r.findall('.//p:sp',NS):
            ph=shape.find('.//p:ph',NS)
            typ=ph.get('type','obj') if ph is not None else 'obj'
            size='3000' if typ in ['title','ctrTitle'] else ('1700' if typ=='subTitle' else '1900')
            body=shape.find('p:txBody/a:bodyPr',NS)
            if body is not None:body.set('anchor','t')
            for p in shape.findall('p:txBody/a:p',NS):
                pp=p.find('a:pPr',NS)
                if pp is None:pp=E.Element(tag('a:pPr'));p.insert(0,pp)
                pp.set('algn','l')
                dr=pp.find('a:defRPr',NS)
                if dr is None:dr=child(pp,'a:defRPr')
                dr.set('sz',size)
                for run in p.findall('a:r',NS):
                    rp=run.find('a:rPr',NS)
                    if rp is None:rp=E.Element(tag('a:rPr'));run.insert(0,rp)
                    rp.set('sz',size);rp.set('lang','es-CL')
        # Native table text stays editable.
        for e in r.findall('.//a:tc//a:rPr',NS):e.set('sz','1700')
        files[n]=E.tostring(r,encoding='utf-8',xml_declaration=True)
    with ZipFile(path,'w',ZIP_DEFLATED) as z:
        for n,data in files.items():z.writestr(n,data)

def fix_docx(path):
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    E.register_namespace('w',w[1:-1])
    with ZipFile(path) as z:files={n:z.read(n) for n in z.namelist()}
    r=E.fromstring(files['word/document.xml'])
    for table in r.iter(w+'tbl'):
        pr=table.find(w+'tblPr')
        if pr is None:pr=E.SubElement(table,w+'tblPr')
        width=pr.find(w+'tblW')
        if width is None:width=E.SubElement(pr,w+'tblW')
        width.set(w+'type','pct');width.set(w+'w','5000')
        for p in table.iter(w+'p'):
            pp=p.find(w+'pPr')
            if pp is None:pp=E.Element(w+'pPr');p.insert(0,pp)
            spacing=pp.find(w+'spacing')
            if spacing is None:spacing=E.SubElement(pp,w+'spacing')
            for key,val in [('before','0'),('after','0'),('line','240'),('lineRule','auto')]:spacing.set(w+key,val)
        for run in table.iter(w+'r'):
            rp=run.find(w+'rPr')
            if rp is None:rp=E.Element(w+'rPr');run.insert(0,rp)
            sz=rp.find(w+'sz')
            if sz is None:sz=E.SubElement(rp,w+'sz')
            sz.set(w+'val','19')
    files['word/document.xml']=E.tostring(r,encoding='utf-8',xml_declaration=True)
    with ZipFile(path,'w',ZIP_DEFLATED) as z:
        for n,data in files.items():z.writestr(n,data)
