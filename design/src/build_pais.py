"""Dia dos Pais — Stories 1080x1920 para a Marca Registrada.

Gera o fundo de estudio (ciclorama warm greige) com a foto de campanha ja
composta dentro dele, recorta o simbolo do logotipo em creme e escreve o
HTML autocontido.
"""
import base64, pathlib
from PIL import Image, ImageFilter
import numpy as np

D = pathlib.Path(__file__).parent
W, H = 1080, 1920

# ------------------------------------------------------------------ conteudo
# Mensagem em caixa alta e baixa: texto longo em versal nao se le. A caixa
# alta tracked fica so na assinatura. As quebras sao manuais, para controlar
# o rio do paragrafo.
MENSAGEM = ['A gente cresce, ganha altura,',
            'aprende a se virar sozinho.',
            'Mas tem dia em que o lugar',
            'mais seguro do mundo',
            'ainda é ao lado dele.']
ASSINA   = 'Feliz Dia dos Pais'
ARROBA   = '@marcaregistrada'

# ------------------------------------------------------------------- paleta
# Tres pontos, nao dois: a sombra puxa levemente para o frio e a luz para o
# quente, entao o fundo ganha profundidade em vez de virar um degrade chapado.
SOMBRA = np.array([0x1E, 0x1C, 0x1C], np.float32)   # cantos, topo
MEIO   = np.array([0x5C, 0x53, 0x48], np.float32)   # meio-tom da parede
LUZ    = np.array([0xB6, 0xA8, 0x94], np.float32)   # centro do refletor
CREME  = '#F3EFE7'
AREIA  = '#B9AC9B'
FUNDO  = '#332E29'   # cor de referencia para os scrims em CSS

# ------------------------------------------------------------------- fundo
rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
u, v = xx / W, yy / H

# refletor gaussiano atras do sujeito: largo, baixo e ao centro
pool = np.exp(-(((u - 0.50) ** 2) / (2 * 0.36 ** 2) + ((v - 0.58) ** 2) / (2 * 0.30 ** 2)))

# encontro da parede com o piso: transicao de luz + a sombra classica na base
horizonte = 1.0 / (1.0 + np.exp(-(v - 0.715) * 30.0))
sombra = -0.13 * np.exp(-((v - 0.682) ** 2) / (2 * 0.030 ** 2))

# queda de luz no topo (onde entra a tipografia) e nas bordas laterais
topo = np.clip((v - 0.02) / 0.34, 0.0, 1.0) ** 0.85
lados = 1.0 - np.clip((np.abs(u - 0.5) - 0.24) / 0.26, 0.0, 1.0) ** 1.3 * 0.45

# vinheta radial: fecha os quatro cantos e sustenta a tipografia no topo.
# Aplicada la embaixo, sobre a arte ja montada, para valer tambem sobre a foto.
r = np.sqrt(((u - 0.5) * 1.05) ** 2 + ((v - 0.52) * 0.80) ** 2) / 0.62
vinheta = (1.0 - 0.38 * np.clip(r, 0, 1) ** 1.9)[:, :, None]

k = np.clip((0.05 + 0.86 * pool * topo + 0.30 * horizonte + sombra) * lados, 0, 1)

# rampa em dois trechos, passando pelo meio-tom
t2 = np.clip(k / 0.5, 0, 1)[:, :, None]
t3 = np.clip((k - 0.5) / 0.5, 0, 1)[:, :, None]
base = (SOMBRA[None, None, :] * (1 - t2) + MEIO[None, None, :] * t2) * (1 - t3) \
     + LUZ[None, None, :] * t3


# ---------------------------------------------------------------- simbolo
# O logotipo do cliente vem preto sobre branco, com o lettering embaixo. Aqui
# so o simbolo e recortado: ele serve duas vezes, como marca em creme no topo
# e como textura gigante no fundo.
SIMBOLO_CAIXA = (150, 0, 952, 620)   # recorte do simbolo no arquivo original

lg = np.asarray(Image.open(D / 'logo_marca_registrada.png').convert('RGBA')
                .crop(SIMBOLO_CAIXA)).astype(np.float32)
cobertura = (1.0 - lg[:, :, :3].mean(2) / 255.0) * (lg[:, :, 3] / 255.0)

simbolo = np.zeros(lg.shape, np.uint8)
simbolo[:, :, 0], simbolo[:, :, 1], simbolo[:, :, 2] = (
    int(CREME[1:3], 16), int(CREME[3:5], 16), int(CREME[5:7], 16))
simbolo[:, :, 3] = np.clip(cobertura * 255, 0, 255).astype(np.uint8)
Image.fromarray(simbolo, 'RGBA').save(D / 'simbolo_creme.png')

SIMBOLO_L = 190                                       # largura na arte, em px
SIMBOLO_A = round(SIMBOLO_L * lg.shape[0] / lg.shape[1])


def octave(scale, amp):
    small = rng.normal(0, 1, (max(2, H // scale), max(2, W // scale))).astype(np.float32)
    n = (small - small.min()) / (np.ptp(small) + 1e-6) * 255
    img = Image.fromarray(n.astype(np.uint8)).resize((W, H), Image.BICUBIC)
    arr = np.asarray(img.filter(ImageFilter.GaussianBlur(scale * 0.4))).astype(np.float32)
    return (arr - arr.mean()) / (arr.std() + 1e-6) * amp


# -------------------------------------------------------------- campanha
# Se existir src/foto.jpg, ela e graduada para a paleta quente, casada em tom
# com o ciclorama na altura da emenda e fundida por um degrade longo. O grao
# entra depois, por cima de tudo, para foto e fundo compartilharem a textura.
FOTO_TOPO_CABECA = 0.382   # onde comeca a cabeca na foto (fracao da altura)
FOTO_CABECA_Y = 800        # onde a cabeca deve cair no canvas
FOTO_FUSAO = 360           # altura do degrade de fusao, em px
FOTO_REF = (0.02, 0.10, 0.05, 0.85)   # retalho de fundo liso, para o cinza de
                                      # referencia: (y0, y1, x0, x1) em fracao

foto_src = D / 'foto.jpg'
tem_foto = foto_src.exists()

if tem_foto:
    ph = Image.open(foto_src).convert('RGB')
    p = np.asarray(ph).astype(np.float32)

    # 1. neutraliza o fundo do estudio usando um retalho dele como referencia
    ry0, ry1, rx0, rx1 = FOTO_REF
    ref = p[int(ry0 * ph.height):int(ry1 * ph.height),
            int(rx0 * ph.width):int(rx1 * ph.width)].reshape(-1, 3).mean(0)
    p *= (ref.mean() / ref)[None, None, :]

    # 2. grade da campanha: puxa o neutro para o greige quente. Comedido de
    #    proposito — passar disso vira sepia e a pele amarela.
    p *= np.array([1.020, 0.968, 0.912], np.float32)[None, None, :]

    alt = int(round(W * ph.height / ph.width))
    p = np.asarray(Image.fromarray(np.clip(p, 0, 255).astype(np.uint8))
                   .resize((W, alt), Image.LANCZOS)).astype(np.float32)

    topo = int(round(FOTO_CABECA_Y - FOTO_TOPO_CABECA * alt))

    # 3. casa a luminancia da foto com a do ciclorama na linha da emenda
    faixa = slice(max(0, topo), min(H, topo + 70))
    alvo = base[faixa].reshape(-1, 3).mean(0)
    p *= np.clip(alvo / p[:70].reshape(-1, 3).mean(0), 0.75, 1.35)[None, None, :]

    # 4. prolonga o fundo da foto para cima, a partir da propria primeira linha,
    #    para o degrade ter onde acontecer sem criar degrau na emenda
    tira = p[0:6].mean(0)[None, :, :]
    p = np.concatenate([np.repeat(tira, FOTO_FUSAO, axis=0), p], axis=0)
    topo -= FOTO_FUSAO

    # 5. recorta na moldura e monta com alfa em smoothstep (derivada zero nas
    #    duas pontas, entao nem o inicio nem o fim do degrade aparecem)
    y0, y1 = max(0, topo), min(H, topo + p.shape[0])
    recorte = p[y0 - topo:y1 - topo]
    t = np.clip((np.arange(y0, y1, dtype=np.float32) - topo) / FOTO_FUSAO, 0, 1)
    alfa = (t * t * (3 - 2 * t))[:, None, None]
    base[y0:y1] = base[y0:y1] * (1 - alfa) + recorte * alfa

base *= vinheta            # fecha os cantos da arte inteira, foto inclusive

mottle = octave(230, 1.1) + octave(60, 1.0)          # manchas do papel infinito
grain = rng.normal(0, 2.0, (H, W)).astype(np.float32)  # grao de filme
textura = (mottle + grain)[:, :, None] * (0.45 + 0.55 * k[:, :, None])

Image.fromarray(np.clip(base + textura, 0, 255).astype(np.uint8)) \
     .save(D / 'bg_pais.jpg', quality=95)

# ------------------------------------------------------------------ assets
def b64(name):
    return base64.b64encode((D / name).read_bytes()).decode()

BR = '<br>'
html = f"""<meta name="hz:slide-selector" content=".page">
<title>Dia dos Pais — Marca Registrada (Stories)</title>
<style>
@font-face{{font-family:'Jost';font-style:normal;font-weight:100 900;
  src:url(data:font/woff2;base64,{b64('jost-var.woff2')}) format('woff2');}}
html,body{{margin:0;padding:0;background:#1A1714;}}
body{{display:flex;justify-content:center;align-items:flex-start;}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
      font-family:'Jost',sans-serif;color:{CREME};
      text-transform:uppercase;font-kerning:normal;}}
.page > *{{position:absolute;}}
.bg{{left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;}}

/* scrim inferior para a assinatura ler sobre a foto */
.scrim{{left:0;top:1330px;width:{W}px;height:590px;
       background:linear-gradient(to bottom,
         rgba(30,26,22,0) 0%, rgba(30,26,22,.42) 42%,
         rgba(30,26,22,.74) 72%, rgba(30,26,22,.88) 100%);}}

/* ---------------------------------------------------------- cabecalho */
.marca{{left:{(W - SIMBOLO_L) // 2}px;top:140px;
       width:{SIMBOLO_L}px;height:{SIMBOLO_A}px;}}

/* ---------------------------------------------------------- titulo */
.msg{{left:92px;top:392px;width:920px;text-align:left;text-transform:none;
      font-weight:300;font-size:46px;line-height:1.36;letter-spacing:.004em;}}

/* ---------------------------------------------------------- assinatura */
.regua2{{left:496px;top:1512px;width:88px;height:1px;
        background:{AREIA};opacity:.45;}}
.assina{{left:140px;top:1550px;width:800px;text-align:center;
        font-weight:300;font-size:28px;line-height:1.35;letter-spacing:.14em;
        text-indent:.14em;}}
.arroba{{left:0;top:1612px;width:{W}px;text-align:center;
        font-weight:400;font-size:22px;letter-spacing:.34em;text-indent:.34em;
        color:{AREIA};text-transform:none;}}
</style>

<div class="page" data-document-role="page" data-label="Dia dos Pais - Stories"
     data-canvas-width="{W}" data-canvas-height="{H}">
  <img class="bg" src="data:image/jpeg;base64,{b64('bg_pais.jpg')}" alt="Fundo de estúdio">
  <div class="scrim"></div>

  <img class="marca" src="data:image/png;base64,{b64('simbolo_creme.png')}"
       alt="Marca Registrada">

  <div class="msg">{BR.join(MENSAGEM)}</div>

  <div class="regua2"></div>
  <div class="assina">{ASSINA}</div>
  <div class="arroba">{ARROBA}</div>
</div>
"""

out = D.parent / 'dia-dos-pais-stories.html'
out.write_text(html, encoding='utf-8')
print(f'{out.name}: {len(html)} bytes | foto de campanha: {"sim" if tem_foto else "nao"}')
