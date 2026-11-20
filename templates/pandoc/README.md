# Plantillas Hacción desde Markdown

Este kit convierte contenido Markdown en cotizaciones, recomendaciones técnicas, recomendaciones de negocio y presentaciones con el último logotipo de Hacción y la paleta océano, celeste, blanco y gris azulado.

## Qué incluye

| Modelo para rellenar | Salida principal | Salidas adicionales |
|---|---|---|
| `ejemplos/cotizacion.md` | Word `.docx`, carta | PDF y fuente LaTeX `.tex` |
| `ejemplos/recomendacion-tecnica.md` | Word `.docx`, carta | PDF y fuente LaTeX `.tex` |
| `ejemplos/recomendacion-negocio.md` | Word `.docx`, carta | PDF y fuente LaTeX `.tex` |
| `ejemplos/presentacion.md` | PowerPoint `.pptx`, 16:9 | PDF mediante exportación desde PowerPoint o LibreOffice |

`salida/` contiene ejemplos ya generados. Son plantillas con campos por completar, no propuestas comerciales reales.

Word usa `plantillas/haccion.docx` como referencia de estilos. PowerPoint usa `plantillas/haccion.pptx` como referencia de diseños. LaTeX se usa para la salida PDF, mediante `plantillas/haccion.tex`. LaTeX no es necesario para generar Word o PowerPoint.

## Requisitos

- Python 3.9 o posterior. El generador solo usa la biblioteca estándar; no requiere instalar módulos con pip.
- Pandoc 3.7 o posterior, disponible en el PATH. Probado con Pandoc 3.7.0.2.
- Fuente **Noto Sans** para Word y PowerPoint. Si falta, Office sustituirá la fuente y pueden cambiar los saltos de línea.
- Para PDF: **XeLaTeX** y los paquetes de TeX Live o MiKTeX `fontspec`, `geometry`, `xcolor`, `graphicx`, `longtable`, `booktabs`, `array`, `calc`, `amsmath`, `amssymb`, `hyperref` y `scrlayer-scrpage` (KOMA-Script). La plantilla usa **Noto Sans Mono** cuando está disponible y recurre a **Liberation Mono** como alternativa. Es suficiente una instalación de TeX Live con las colecciones LaTeX recomendadas, fuentes recomendadas y XeTeX.

No requiere Word ni PowerPoint instalados para generar los archivos. Sí conviene revisarlos en la aplicación de destino antes de enviarlos.

## Empezar

Descomprime el kit, abre una terminal en su carpeta y ejecuta:

```bash
python3 generar.py --todos
```

En Windows puedes usar `py` en lugar de `python3`.

Después:

1. Duplica el Markdown que necesites y asígnale el nombre del proyecto.
2. Sustituye los campos entre corchetes, tanto en el bloque inicial YAML como en el cuerpo.
3. Añade o elimina filas, secciones, imágenes o diapositivas.
4. Ejecuta el generador sobre ese archivo.
5. Revisa el resultado en `salida/`.

### Cotización en Word

```bash
python3 generar.py ejemplos/cotizacion.md
```

### Recomendaciones en Word

```bash
python3 generar.py ejemplos/recomendacion-tecnica.md
python3 generar.py ejemplos/recomendacion-negocio.md
```

### Documentos en Word, PDF y LaTeX

```bash
python3 generar.py ejemplos/cotizacion.md --formato docx,pdf,tex
```

También puedes usar `--formato pdf` o `--formato tex` por separado. El PDF y el Word usan la misma identidad, pero sus motores de composición pueden paginar de manera diferente. El PDF incorpora la portada carta oficial de `assets/portada-carta.png`; las páginas interiores llevan el logotipo reducido en el pie, numeración a la derecha y marca de agua.

Para compilar manualmente el `.tex`, ejecuta desde la raíz del kit:

```bash
xelatex -output-directory=salida salida/cotizacion.tex
```

### Presentación

```bash
python3 generar.py ejemplos/presentacion.md
```

El resultado es un `.pptx` con texto y tablas editables, portada blanca con ondas y páginas interiores con marca de agua. Los fondos son imágenes incorporadas; sus fuentes SVG editables están en `assets/`.

### Otro destino

```bash
python3 generar.py "mis documentos/proyecto.md" --salida "entregables/proyecto"
```

Las rutas del archivo de entrada y de `--salida` se interpretan desde la carpeta donde ejecutas el comando. Los recursos del kit se localizan automáticamente. Puedes llamar al script mediante su ruta absoluta desde otra carpeta.

Si ya existe un archivo con el mismo nombre en la salida, se reemplaza solo después de generar correctamente el nuevo. El Markdown original no se modifica.

## Campos del bloque YAML

```yaml
---
tipo: cotizacion
title: "Cotización de servicios"
subtitle: "Nombre del proyecto"
author: "Hacción"
date: "18 de noviembre de 2026"
cliente: "Nombre del cliente"
codigo: "COT-2026-001"
version: "1.0"
contacto: "Persona de contacto"
moneda: "CLP"
validez: "15 días"
---
```

El ejemplo de fecha es ilustrativo; se usa literalmente lo que escribas. No se agrega una fecha automática.

- `tipo` es obligatorio: `cotizacion`, `recomendacion-tecnica`, `recomendacion-negocio` o `presentacion`.
- `title`, `subtitle`, `author` y `date` componen el título.
- `cover-label` permite reemplazar el rótulo pequeño de la portada. Si se omite, el generador usa “Cotización”, “Recomendación técnica” o “Recomendación de negocio” según `tipo`.
- `cliente`, `codigo`, `version`, `contacto`, `responsable`, `moneda` y `validez` se incluyen como datos del documento cuando están presentes.
- Elimina los campos opcionales que no correspondan.
- Usa comillas si un valor contiene dos puntos, símbolos o corchetes.
- En presentación, autor y fecha aparecen juntos en la portada.

Los ejemplos son esqueletos para rellenar. El generador no redacta recomendaciones ni calcula precios, impuestos, márgenes o retorno de inversión. Completa y revisa los importes y supuestos antes de emitirlos. Quita las instrucciones de relleno que no deban aparecer en el documento final.

## Escribir el contenido

### Documentos

- `#` crea una sección; `##` una subsección.
- `**texto**` aplica negrita; `*texto*` cursiva.
- Las tablas Markdown se convierten en tablas editables.
- Usa rutas relativas para imágenes y enlaces; las imágenes se buscan también junto al archivo `.md`.
- Se puede insertar un salto de página explícito:

```markdown
::: {.salto}
:::
```

El salto se admite en DOCX y PDF. Úsalo con moderación y revisa el resultado cuando el contenido crezca.

### Presentaciones

- La portada se genera desde el YAML.
- Cada título `##` abre una diapositiva.
- Usa `###` para un subtítulo dentro de una diapositiva.
- Usa `#` solo si quieres una diapositiva divisoria de sección.
- Limita cada diapositiva a una idea y pocos puntos: el generador no divide automáticamente el contenido que se desborda.
- El ejemplo muestra dos columnas, tablas y notas del presentador.

```markdown
## Título de la diapositiva

- Primer punto.
- Segundo punto.

::: notes
Notas que solo verá quien presenta.
:::
```

Para una imagen:

```markdown
## Esquema de la solución

![Descripción accesible](imagenes/esquema.png){width=70%}
```

## Personalizar el diseño

- **Word:** abre `plantillas/haccion.docx` y modifica los estilos (Title, Subtitle, Heading 1, Heading 2, Normal, Body Text y Table), el encabezado o el pie. El texto de ese archivo es ilustrativo; Pandoc toma sus estilos, no su contenido.
- **PowerPoint:** modifica los diseños en Vista → Patrón de diapositivas de `plantillas/haccion.pptx`. Conserva sus nombres, especialmente `Title Slide`, `Title and Content`, `Two Content`, `Comparison` y `Content with Caption`.
- **Fondos:** los PNG están incorporados en el PPTX de referencia. Si cambias un SVG de `assets/`, exporta un PNG y sustituye el fondo correspondiente en el patrón. Cambiar el SVG externo por sí solo no actualiza el PPTX.
- **LaTeX:** ajusta colores, fuente, márgenes y pie de página en `plantillas/haccion.tex`. La portada PDF usa `assets/portada-carta.png`; su fuente vectorial editable es `assets/portada-carta.svg`.
- **Ajustes de salida:** `plantillas/ajustar_office.py` conserva los fondos al generar PPTX, aplica tamaños de texto y compacta las tablas de Word. Si cambias esos tamaños en el patrón, ajusta también este archivo.

Paleta:

| Nombre | Hexadecimal |
|---|---|
| Océano | `#0284C7` |
| Celeste | `#C9EDFF` |
| Blanco | `#FFFFFF` |
| Gris azulado | `#526575` |
| Sombra | `#173042` |
| Niebla | `#F2F6F9` |

## Comprobaciones y límites

- Los tres ejemplos Word se renderizaron y revisaron en tamaño carta.
- Los tres documentos PDF se generaron mediante XeLaTeX, con portada carta independiente y membrete reducido en el pie de las páginas interiores.
- La presentación se generó y revisó en 16:9; contiene cinco diapositivas.
- Word y PowerPoint mantienen texto y tablas editables. El logotipo se incorpora como imagen de alta resolución; su SVG original está incluido.
- No se ha abierto el resultado en Microsoft Office; la revisión visual se hizo con LibreOffice. Puede haber pequeñas diferencias entre aplicaciones, versiones y fuentes disponibles.
- Después de ampliar contenido, revisa páginas, tablas, saltos de línea y desbordamientos de diapositivas.
- El modo opcional `--estricto` rechaza archivos con corchetes. Es un recordatorio conservador: también puede señalar enlaces Markdown válidos. No sustituye la revisión editorial.
- `--todos` usa DOCX para documentos y PPTX para presentación. Para elegir otros formatos indica un archivo concreto.

El flujo de referencias DOCX/PPTX y la estructura de diapositivas siguen el [manual oficial de Pandoc](https://pandoc.org/MANUAL.html). Las plantillas Office parten de las referencias predeterminadas de Pandoc, personalizadas con la identidad Hacción.
