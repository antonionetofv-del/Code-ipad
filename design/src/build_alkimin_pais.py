"""Ferro Velho Alkimin — Dia dos Pais, Stories 1080x1920.

Gera duas versoes a partir do mesmo texto e da mesma foto:

  moldura  — retangulo verde atras, foto de cantos arredondados por cima
             deslocada, e o card do texto por cima de tudo
  polaroid — a foto montada como polaroide, com moldura branca e a borda
             inferior mais larga, levemente girada

Sem os elementos de reciclagem soltos (pedido do cliente). A logo volta em
azul, no concreto abaixo do card — sobre o card ela sumiria e sobre a foto
ficaria suja. O fundo de concreto e o card azul seguem sendo os do sistema
da marca.

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
MENSAGEM = ['A todos os pais que ensinam',
            'com conselhos ou sem perceber:',
            'o que vocês começaram segue firme.',
            'Não foi sorte, foi exemplo honesto.',
            'E a gente aprendeu a fazer igual.']
ASSINA = 'Feliz Dia dos Pais'

# ------------------------------------------------------------------- paleta
CARD  = '#121B6E'   # azul do card
BLUE  = '#0F2B75'   # azul da marca
GREEN = '#3D823B'   # verde da marca, no retangulo de tras
LIME  = '#74C96A'   # verde clareado, para ler sobre o navy
WHITE = '#FFFFFF'

# -------------------------------------------------------------------- foto
# Dessaturacao leve, so para acalmar o xadrez vermelho ao lado do card azul.
# Sem esfriar: a foto e quente e humana, e e essa temperatura que faz ela
# funcionar num Dia dos Pais. Contra o concreto neutro, o quente vira o foco.
DESSAT = 0.12
QUENTE = np.array([1.035, 1.000, 0.945], np.float32)

ph = Image.open(D / 'foto_alkimin.jpg').convert('RGB')
p = np.asarray(ph).astype(np.float32)
cinza = p @ np.array([0.299, 0.587, 0.114], np.float32)
p = p * (1 - DESSAT) + cinza[:, :, None] * DESSAT
p *= QUENTE
Image.fromarray(np.clip(p, 0, 255).astype(np.uint8)).save(D / 'foto_grade.jpg', quality=93)

# ------------------------------------------------------------------- assets
def b64(name):
    return base64.b64encode((D / name).read_bytes()).decode()


def font_face(family, weight, file):
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{b64(file)}) format('woff2');}}")


BR = '<br>'
FONTES = '\n'.join([font_face('Anton', 400, 'anton.woff2'),
                    font_face('Poppins', 400, 'poppins400.woff2'),
                    font_face('Poppins', 700, 'poppins700.woff2')])


def pagina(nome, rotulo, css_extra, corpo, card_y, titulo_px=96, logo_l=340):
    """Monta uma variacao. O bloco de texto e identico nas duas."""
    tit_y = card_y + 70
    rule_y = tit_y + round(titulo_px * 1.02 * 2) + 42
    msg_y = rule_y + 58
    ass_y = msg_y + round(34 * 1.52 * len(MENSAGEM)) + 46
    card_h = ass_y + 52 + 74 - card_y
    # A logo e azul e fica no concreto, abaixo do card: sobre o card azul ela
    # sumiria e sobre a foto ficaria suja. Alinhada em x=124, com o texto.
    logo_a = round(logo_l * 944 / 1607)
    logo_y = card_y + card_h + 44
    assert logo_y + logo_a < 1670, 'logo cairia atras da barra de resposta'

    html = f"""<meta name="hz:slide-selector" content=".page">
<meta name="hz:canvas-width" content="{W}">
<meta name="hz:canvas-height" content="{H}">
<title>Ferro Velho Alkimin — Dia dos Pais ({rotulo})</title>
<style>
{FONTES}
html,body{{margin:0;padding:0;background:#2A2A2E;}}
body{{display:flex;justify-content:center;align-items:flex-start;}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
      font-family:'Poppins',sans-serif;}}
.page > *{{position:absolute;}}
.bg{{left:0;top:0;width:{W}px;height:{H}px;}}
{css_extra}
.card{{left:60px;top:{card_y}px;width:960px;height:{card_h}px;
      background:{CARD};border-radius:53px;}}
.titulo{{left:124px;top:{tit_y}px;width:812px;
        font-family:'Anton',sans-serif;font-weight:400;font-size:{titulo_px}px;
        line-height:1.02;color:{WHITE};letter-spacing:-0.5px;}}
.rule{{left:124px;top:{rule_y}px;width:176px;height:4px;background:{LIME};}}
.msg{{left:124px;top:{msg_y}px;width:812px;
     font-weight:400;font-size:34px;line-height:1.52;color:{WHITE};}}
.assina{{left:124px;top:{ass_y}px;width:812px;
        font-weight:700;font-size:40px;color:{LIME};letter-spacing:.5px;}}
.logo{{left:{(W - logo_l) // 2}px;top:{logo_y}px;width:{logo_l}px;}}
</style>

<div class="page" data-document-role="page" data-label="Dia dos Pais - {rotulo}"
     data-canvas-width="{W}" data-canvas-height="{H}">
  <img class="bg" src="data:image/jpeg;base64,{b64('bg_story.jpg')}" alt="Fundo de concreto">
{corpo}
  <div class="card"></div>
  <div class="titulo">{BR.join(TITULO)}</div>
  <div class="rule"></div>
  <div class="msg">{BR.join(MENSAGEM)}</div>
  <div class="assina">{ASSINA}</div>
  <img class="logo" src="data:image/png;base64,{b64('logo.png')}" alt="Ferro Velho Alkimin">
</div>
"""
    out = D.parent / f'alkimin-dia-dos-pais-{nome}.html'
    out.write_text(html, encoding='utf-8')
    print(f'{out.name}: {len(html):,} bytes | card {card_y}–{card_y + card_h}')


# ---------------------------------------------------------------- moldura
# Retangulo verde atras, deslocado, para a foto ganhar profundidade e a cor
# da marca voltar sem virar enfeite solto.
pagina(
    'moldura', 'Moldura',
    # A foto se alinha a margem do card (60 px); o verde e que sai do eixo,
    # aparecendo em cima e a direita — dois lados vizinhos, nunca quatro.
    f""".bloco{{left:100px;top:50px;width:960px;height:520px;
       background:{GREEN};border-radius:44px;}}
.foto{{left:60px;top:90px;width:960px;height:520px;
      border-radius:44px;object-fit:cover;object-position:center 35%;}}""",
    """  <div class="bloco"></div>
  <img class="foto" src="data:image/jpeg;base64,{FOTO}" alt="Dois trabalhadores em uma máquina">
""".replace('{FOTO}', b64('foto_grade.jpg')),
    card_y=610)

# --------------------------------------------------------------- polaroide
# Moldura branca com a borda de baixo mais larga, girada de leve. A sombra
# e unica e discreta: o importador do Express nao lida bem com pilhas delas.
# A foto vai DENTRO da moldura, nao ao lado: assim a rotacao e uma so e as
# duas nunca saem do lugar uma da outra. Borda de baixo mais larga, como no
# polaroide de verdade. Sombra unica — o importador do Express nao lida bem
# com pilhas delas.
pagina(
    'polaroid', 'Polaroide',
    """.polaroid{left:242px;top:50px;width:597px;height:550px;
          background:#F4F2ED;border-radius:8px;
          box-shadow:0 20px 42px rgba(0,0,0,.32);
          transform:rotate(-2.4deg);}
.polaroid .foto{position:absolute;left:26px;top:26px;width:545px;height:407px;
      object-fit:cover;object-position:center 35%;}""",
    """  <div class="polaroid">
    <img class="foto" src="data:image/jpeg;base64,{FOTO}" alt="Dois trabalhadores em uma máquina">
  </div>
""".replace('{FOTO}', b64('foto_grade.jpg')),
    card_y=630, titulo_px=88)
