"""Ferro Velho Alkimin — Dia dos Pais, Stories 1080x1920.

Monta a peca dentro do sistema visual que a marca ja tem no repositorio:
mesmo fundo de concreto, mesmo logo, mesmas marcas d'agua de reciclagem e
chevrons, mesma dupla Anton + Poppins, mesma paleta. O card azul continua
sendo o elemento de assinatura; o que muda dentro dele e o conteudo.

    python3 src/build_alkimin_pais.py
"""
import base64, pathlib
from PIL import Image
import numpy as np

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

# -------------------------------------------------------------------- foto
# A foto entra como faixa no topo e derrete no concreto por um degrade, para
# nao criar uma linha reta cortando a peca. Fica dessaturada e puxada para o
# frio: o assunto e o trabalho, nao a foto.
FOTO_H, FOTO_FUSAO = 760, 140

fundo = Image.open(D / 'bg_story.jpg').convert('RGB')
base = np.asarray(fundo).astype(np.float32)

ph = Image.open(D / 'foto_alkimin.jpg').convert('RGB')
escala = max(W / ph.width, FOTO_H / ph.height)
ph = ph.resize((round(ph.width * escala), round(ph.height * escala)), Image.LANCZOS)
esq = (ph.width - W) // 2
faixa = np.asarray(ph.crop((esq, 0, esq + W, FOTO_H))).astype(np.float32)

cinza = faixa @ np.array([0.299, 0.587, 0.114], np.float32)
faixa = faixa * 0.45 + cinza[:, :, None] * 0.55          # dessatura
faixa *= np.array([0.94, 0.97, 1.04], np.float32)         # esfria de leve

# escurece o topo: da superficie para o logo branco e afunda o quadro
veu = np.clip((300 - np.arange(FOTO_H)) / 300, 0, 1).astype(np.float32) ** 1.4
faixa *= (1 - 0.52 * veu)[:, None, None]

alfa = np.clip((FOTO_H - np.arange(FOTO_H)) / FOTO_FUSAO, 0, 1).astype(np.float32)
alfa = (alfa * alfa * (3 - 2 * alfa))[:, None, None]
base[:FOTO_H] = base[:FOTO_H] * (1 - alfa) + faixa * alfa
Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).save(D / 'bg_pais_alkimin.jpg', quality=94)

# logo em branco, para ler sobre a foto
lg = np.asarray(Image.open(D / 'logo.png').convert('RGBA')).astype(np.float32)
branco = np.zeros(lg.shape, np.uint8)
branco[:, :, :3] = 255
branco[:, :, 3] = lg[:, :, 3].astype(np.uint8)
Image.fromarray(branco, 'RGBA').save(D / 'logo_branco.png')

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
.logo{{left:680px;top:96px;width:330px;}}   /* sobre a maquina escura, longe dos rostos */

.card{{left:60px;top:800px;width:960px;height:785px;
      background:{CARD};border-radius:53px;}}

.titulo{{left:124px;top:870px;width:812px;
        font-family:'Anton',sans-serif;font-weight:400;font-size:104px;
        line-height:1.02;color:{WHITE};letter-spacing:-0.5px;}}
.rule{{left:124px;top:1122px;width:176px;height:4px;background:{GREEN};}}

.msg{{left:124px;top:1182px;width:812px;
     font-weight:400;font-size:34px;line-height:1.52;color:{WHITE};}}

.assina{{left:124px;top:1460px;width:812px;
        font-weight:700;font-size:40px;color:{GREEN};letter-spacing:.5px;}}
</style>

<div class="page" data-document-role="page" data-label="Dia dos Pais - Stories"
     data-canvas-width="{W}" data-canvas-height="{H}">
  <img class="bg" src="data:image/jpeg;base64,{b64('bg_pais_alkimin.jpg')}" alt="Pai e filho no trabalho">
  <img class="wm wm-bl" src="{recycle_uri}" alt="">
  <img class="wm wm-br" src="{recycle_uri}" alt="">
  <img class="logo" src="data:image/png;base64,{b64('logo_branco.png')}" alt="Ferro Velho Alkimin">

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
