#!/usr/bin/env python3
"""Convertir Markdown a DOCX, PPTX o PDF con la identidad de Hacción.
Solo requiere Python estándar, Pandoc y, para PDF, XeLaTeX.
"""
from pathlib import Path
import argparse, json, os, shutil, subprocess, sys, tempfile
import importlib.util
ROOT = Path(__file__).resolve().parent
DOCS = {'cotizacion', 'recomendacion-tecnica', 'recomendacion-negocio'}
def run(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)
def metadata_value(value):
    if not value: return ''
    if value['t'] == 'MetaString': return value['c']
    if value['t'] == 'MetaInlines':
        return ''.join(x.get('c', '') if x['t'] == 'Str' else ' ' for x in value['c']).strip()
    return ''
def convert(source, formats, outdir, strict):
    source = source.resolve()
    if not source.is_file(): raise ValueError(f'No se encontró: {source}')
    raw = source.read_text(encoding='utf-8')
    if strict and '[' in raw and ']' in raw:
        raise ValueError('Revisar campos entre corchetes antes de emitir. --estricto también detecta enlaces Markdown; omítelo tras revisarlos.')
    parsed = run(['pandoc',str(source),'-f','markdown','-t','json'],capture_output=True,text=True)
    tipo = metadata_value(json.loads(parsed.stdout)['meta'].get('tipo'))
    if tipo not in DOCS | {'presentacion'}: raise ValueError('El YAML debe incluir tipo: cotizacion, recomendacion-tecnica, recomendacion-negocio o presentacion.')
    targets = formats or (['pptx'] if tipo == 'presentacion' else ['docx'])
    if tipo == 'presentacion' and any(x != 'pptx' for x in targets):
        raise ValueError('Las presentaciones se generan en PPTX. Para PDF, exporta el PPTX desde PowerPoint o LibreOffice.')
    if tipo in DOCS and 'pptx' in targets: raise ValueError('Usa tipo: presentacion para exportar PPTX.')
    outdir.mkdir(parents=True, exist_ok=True)
    resources = os.pathsep.join([str(source.parent),str(ROOT),str(ROOT/'assets')])
    base = ['pandoc',str(source),'-f','markdown','--standalone','--resource-path',resources,'--lua-filter',str(ROOT/'plantillas/metadatos.lua'),'--no-highlight']
    for fmt in targets:
        final = outdir / (source.stem+'.'+fmt)
        with tempfile.TemporaryDirectory(prefix='.haccion-', dir=outdir) as temp:
            target=Path(temp)/final.name
            cmd=base.copy()
            if fmt in ['docx','pptx']:
                cmd += ['--reference-doc',str(ROOT/f'plantillas/haccion.{fmt}')]
                if fmt == 'pptx':cmd += ['--slide-level=2']
            else:
                cmd += ['--template',str(ROOT/'plantillas/haccion.tex')]
                if fmt == 'pdf':
                    if not shutil.which('xelatex'):raise ValueError('Para PDF instala XeLaTeX (TeX Live o MiKTeX).')
                    cmd += ['--pdf-engine=xelatex']
                else:cmd += ['-t','latex']
            cmd += ['-o',str(target)]
            run(cmd,cwd=ROOT)
            if fmt in ['docx','pptx']:
                spec=importlib.util.spec_from_file_location('ajustar_office', ROOT/'plantillas/ajustar_office.py')
                module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
                if fmt == 'pptx':module.fix_pptx(target, ROOT/'plantillas/haccion.pptx')
                else:module.fix_docx(target)
            os.replace(target, final)
        print(final)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archivo',nargs='?',type=Path)
    p.add_argument('--todos',action='store_true',help='Generar los cuatro ejemplos')
    p.add_argument('--formato',help='docx, pdf, tex o pptx; se pueden separar con comas')
    p.add_argument('--salida',type=Path,default=ROOT/'salida')
    p.add_argument('--estricto',action='store_true',help='Avisar si todavía hay campos entre corchetes')
    a=p.parse_args()
    if not shutil.which('pandoc'):p.error('No se encontró Pandoc. Instálalo y vuelve a ejecutar.')
    if a.todos and a.archivo:p.error('Usa un archivo o --todos, no ambos.')
    if a.todos and a.formato:p.error('--todos usa el formato natural de cada ejemplo; para otros formatos indica un archivo.')
    if not a.todos and not a.archivo:p.error('Indica un .md o --todos.')
    formats=a.formato.split(',') if a.formato else None
    if formats and any(f not in ['docx','pdf','tex','pptx'] for f in formats):p.error('Formato no válido.')
    sources=sorted((ROOT/'ejemplos').glob('*.md')) if a.todos else [a.archivo]
    for source in sources:convert(source,formats,a.salida.resolve(),a.estricto)
if __name__ == '__main__':
    try:main()
    except (ValueError,subprocess.CalledProcessError,OSError) as e:
        print(f'No se pudo generar: {e}',file=sys.stderr);sys.exit(1)
