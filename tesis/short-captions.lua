--- short-captions.lua
--- Mueve el atributo short-caption="..." de una imagen al slot nativo
--- ShortCaption de la figura (AST de Pandoc 3), de modo que el writer
--- LaTeX emita \caption[corto]{largo} y la Lista de Figuras use el corto.
--- Uso: pandoc --lua-filter=short-captions.lua ...

function Figure(fig)
  local short = nil
  fig.content:walk({
    Image = function(img)
      if img.attributes['short-caption'] then
        short = img.attributes['short-caption']
      end
    end
  })
  if short then
    local doc = pandoc.read(short, 'markdown')
    fig.caption.short = pandoc.utils.blocks_to_inlines(doc.blocks)
    return fig
  end
end
