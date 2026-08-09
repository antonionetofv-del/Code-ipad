"""Converte o HTML final na versao que o Adobe Express importa.

Duas diferencas em relacao ao arquivo de producao:

1. **Fonte.** O design usa Jost embutida em base64. O Express so aceita fontes
   da Adobe Fonts, e a conta da loja nao tem direito a nenhuma geometrica da
   linhagem da Futura — Futura PT, Arboria, Soleil, Basic Sans e Proxima Nova
   voltaram todas como `not_entitled`. Montserrat Light esta liberada e e a
   geometrica mais proxima entre as disponiveis, entao e ela que vai. O PNG de
   producao continua em Jost; a troca vale so para o arquivo editavel.

2. **Metadados de canvas** no cabecalho, que o importador le para dimensionar
   a prancha.

    python3 src/preparar_express.py
"""
import pathlib
import re

D = pathlib.Path(__file__).parent
ORIGEM = D.parent / 'dia-dos-pais-stories.html'
DESTINO = D.parent / 'dia-dos-pais-stories-Express-export.html'

KIT = 'https://use.typekit.net/krr5tsm.css'   # Montserrat Light + Regular
PILHA = '"montserrat",sans-serif'

t = ORIGEM.read_text(encoding='utf-8')

# Jost embutida sai, kit da Adobe Fonts entra
t = re.sub(r"@font-face\{font-family:'Jost';[^}]*\}\n?", '', t, flags=re.S)
t = t.replace('<style>', f'<link rel="stylesheet" href="{KIT}">\n<style>', 1)
t = t.replace("font-family:'Jost',sans-serif;", f'font-family:{PILHA};')

t = t.replace('<meta name="hz:slide-selector" content=".page">',
              '<meta name="hz:slide-selector" content=".page">\n'
              '<meta name="hz:canvas-width" content="1080">\n'
              '<meta name="hz:canvas-height" content="1920">')

# o importador le estilo computado por elemento: a fonte precisa estar
# declarada em cada bloco de texto, nao so no container
for classe in ('.msg', '.assina', '.arroba'):
    t = t.replace(f'{classe}{{left:', f'{classe}{{font-family:{PILHA};left:')

DESTINO.write_text(t, encoding='utf-8')
assert 'Jost' not in t, 'sobrou referencia a Jost'
print(f'{DESTINO.name} {len(t.encode()):,} bytes')
