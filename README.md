# Identidad de marca Hacción

Repositorio oficial de la identidad visual y documental de **Hacción**.

La marca parte de una idea simple: hacer visible lo invisible. El símbolo `h` representa lo fundamental que sostiene a los sistemas; la palabra en cursiva expresa acción, avance y transformación. El azul océano aporta confianza y profundidad, mientras que el celeste abre espacio, claridad y cercanía.

## Comenzar

- Consulta [MANUAL-DE-MARCA.md](MANUAL-DE-MARCA.md) antes de crear una pieza nueva.
- Usa los archivos de `assets/logo/` sin redibujar, deformar ni recomponer el logotipo.
- Elige una de las tres familias de `assets/portadas/` según el tono de la comunicación.
- Para generar Word, PDF o PowerPoint desde Markdown, entra en `templates/pandoc/` y sigue su `README.md`.

## Estructura

```text
.
├── MANUAL-DE-MARCA.md       Manual normativo y guía de aplicación
├── assets/
│   ├── logo/                Logotipos, símbolo, BIMI, favicon e iconos
│   ├── paleta/              Muestra editable y vista previa de color
│   ├── portadas/            Tres sistemas en Letter y 16:9
│   ├── papeleria/           Membrete, interior, marca de agua y pies
│   └── previews/            Láminas de referencia rápida
├── templates/pandoc/        Generador y plantillas Markdown → Office/PDF
├── base.md                  Misión y visión resumidas
├── brand-brief.md           Brief original de identidad
└── mision-vision-aplicadas.md
```

## Archivos maestros

Los SVG son los maestros editables. Los PNG e ICO están listos para usos que no admiten vectores. Para impresión, exporta desde SVG y conserva el perfil y la proporción originales.

## Generación de documentos

Desde `templates/pandoc/`:

```bash
python3 generar.py --todos
python3 generar.py ejemplos/cotizacion.md --formato docx,pdf
python3 generar.py ejemplos/presentacion.md
```

Requisitos: Python 3.9 o posterior y Pandoc 3.7 o posterior. La salida PDF requiere XeLaTeX.

## Fuente de verdad

El logotipo aprobado está en `assets/logo/`. Las carpetas de portadas y papelería ya emplean esta versión: `h` inclinada, barra extendida con remate biselado y acento azul océano.

