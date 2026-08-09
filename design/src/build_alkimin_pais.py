"""Ferro Velho Alkimin — Dia dos Pais, Stories 1080x1920.

Monta a peca dentro do sistema visual que a marca ja tem no repositorio:
mesmo fundo de concreto, mesmo logo, mesmas marcas d'agua de reciclagem e
chevrons, mesma dupla Anton + Poppins, mesma paleta. O card azul continua
sendo o elemento de assinatura; o que muda dentro dele e o conteudo.

    python3 src/build_alkimin_pais.py
"""
import base64, pathlib

D = pathlib.Path(__file__).parent
W, H = 1080, 1920

# ------------------------------------------------------------------ conteudo
TITULO = ['De pai', 'para filho']
# Quebras manuais: o texto e o argumento da peca, entao o rio dele nao pode
# ficar a cargo do navegador.
MENSAGEM = ['A todos os pais que ensinam sem perceber:',
            'o que vocês começaram segue firme.',
            'Não foi sorte, foi exemplo honesto.',
            'E a gente aprendeu a fazer igual.']
ASSINA = 'Feliz Dia dos Pais'

# ------------------------------------------------------------------- paleta
CARD  = '#121B6E'   # azul do card
GREEN = '#74C96A'   # verde clareado, para ler sobre o navy
WHITE = '#FFFFFF'

# ------------------------------------------------------------------- assets
def b64(name):
    return base64.b64encode((D / name).read_bytes()).decode()


def font_face(family, weight, file):
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{b64(file)}) format('woff2');}}")


vb, *paths = (D / 'recycle_paths.txt').read_text().strip().split('\n')
recycle = ('<svg viewBox="%s" xmlns="http://www.w3.org/2000/svg">%s</svg>'
           % (vb, ''.join(f'<path d="{p}" fill="#3D823B"/>' for p in paths)))
recycle_uri = 'data:image/svg+xml;utf8,' + recycle.replace('"', "'").replace('#', '%23')

BR = '<br>'
html = f"""<meta name="hz:slide-selector" content=".page">
<meta name="hz:canvas-width" content="{W}">
<meta name="hz:canvas-height" content="{H}">
<title>Ferro Velho Alkimin — Dia dos Pais (Stories)</title>
<style>
{font_face('Anton', 400, 'anton.woff2')}
{font_face('Poppins', 400, 'poppins400.woff2')}
{font_face('Poppins', 600, 'poppins600.woff2')}
{font_face('Poppins', 700, 'poppins700.woff2')}
html,body{{margin:0;padding:0;background:#2A2A2E;}}
body{{display:flex;justify-content:center;align-items:flex-start;}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
      font-family:'Poppins',sans-serif;}}
.page > *{{position:absolute;}}
.bg{{left:0;top:0;width:{W}px;height:{H}px;}}

.wm{{opacity:.41;width:217px;}}
.wm-tl{{left:-34px;top:64px;}}
.wm-bl{{left:0px;top:1680px;}}
.wm-br{{left:863px;top:1680px;}}
.chev{{left:648px;top:70px;width:452px;height:330px;}}
.logo{{left:70px;top:300px;width:380px;}}

.card{{left:60px;top:620px;width:960px;height:785px;
      background:{CARD};border-radius:53px;}}

.titulo{{left:124px;top:690px;width:812px;
        font-family:'Anton',sans-serif;font-weight:400;font-size:104px;
        line-height:1.02;color:{WHITE};letter-spacing:-0.5px;}}
.rule{{left:124px;top:942px;width:176px;height:4px;background:{GREEN};}}

.msg{{left:124px;top:1002px;width:812px;
     font-weight:400;font-size:34px;line-height:1.52;color:{WHITE};}}

.assina{{left:124px;top:1280px;width:812px;
        font-weight:700;font-size:40px;color:{GREEN};letter-spacing:.5px;}}
</style>

<div class="page" data-document-role="page" data-label="Dia dos Pais - Stories"
     data-canvas-width="{W}" data-canvas-height="{H}">
  <img class="bg" src="data:image/jpeg;base64,{b64('bg_story.jpg')}" alt="Fundo cinza texturizado">
  <img class="wm wm-tl" src="{recycle_uri}" alt="">
  <img class="wm wm-bl" src="{recycle_uri}" alt="">
  <img class="wm wm-br" src="{recycle_uri}" alt="">
  <svg class="chev" viewBox="0 0 452 330" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g stroke="#3D823B" stroke-width="4" opacity=".52">
      <path d="M104 262 L262 40 L330 40 L172 262 Z"/>
      <path d="M212 262 L370 40 L438 40 L280 262 Z"/>
      <path d="M-4 262 L154 40 L222 40 L64 262 Z"/>
    </g>
  </svg>
  <img class="logo" src="data:image/png;base64,{b64('logo.png')}" alt="Ferro Velho Alkimin">

  <div class="card"></div>
  <div class="titulo">{BR.join(TITULO)}</div>
  <div class="rule"></div>
  <div class="msg">{BR.join(MENSAGEM)}</div>
  <div class="assina">{ASSINA}</div>
</div>
"""

out = D.parent / 'alkimin-dia-dos-pais.html'
out.write_text(html, encoding='utf-8')
print(f'{out.name}: {len(html):,} bytes')
