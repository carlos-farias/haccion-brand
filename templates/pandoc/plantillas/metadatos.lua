-- Metadata is prepended as a compact paragraph for Word and LaTeX.
function Pandoc(doc)
  if FORMAT == 'pptx' then
    if doc.meta.date then
      doc.meta.author = pandoc.MetaString(pandoc.utils.stringify(doc.meta.author or '') .. ' · ' .. pandoc.utils.stringify(doc.meta.date))
      doc.meta.date = nil
    end
    return doc
  end
  if FORMAT:match('latex') then
    if not doc.meta['cover-label'] then
      local tipo = pandoc.utils.stringify(doc.meta.tipo or '')
      local labels = {
        ['cotizacion'] = 'Cotización',
        ['recomendacion-tecnica'] = 'Recomendación técnica',
        ['recomendacion-negocio'] = 'Recomendación de negocio'
      }
      doc.meta['cover-label'] = pandoc.MetaString(labels[tipo] or 'Documento')
    end
    return doc
  end
  local groups = {{{'cliente','Cliente'}},{{'codigo','Código'},{'version','Versión'}},{{'contacto','Contacto'},{'responsable','Responsable'}},{{'moneda','Moneda'},{'validez','Validez'}}}
  local inlines = pandoc.List()
  for _, group in ipairs(groups) do
    local line = pandoc.List()
    for _, f in ipairs(group) do
      if doc.meta[f[1]] then
        if #line > 0 then line:insert(pandoc.Str('  ·  ')) end
        line:insert(pandoc.Strong({pandoc.Str(f[2] .. ':')}))
        line:insert(pandoc.Space())
        line:insert(pandoc.Str(pandoc.utils.stringify(doc.meta[f[1]])))
      end
    end
    if #line > 0 then
      if #inlines > 0 then inlines:insert(pandoc.LineBreak()) end
      inlines:extend(line)
    end
  end
  if #inlines > 0 then doc.blocks:insert(1,pandoc.Para(inlines)) end
  return doc
end
function Div(el)
  if el.classes:includes('salto') then
    if FORMAT:match('latex') then return pandoc.RawBlock('latex', '\\newpage')
    elseif FORMAT == 'docx' then return pandoc.RawBlock('openxml','<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
    else return {} end
  end
end
