"""Dia dos Pais — Stories 1080x1920 para loja multimarcas.

Gera o fundo de estudio (ciclorama warm greige) e o HTML autocontido.
Se existir `src/foto.jpg`, a foto de campanha entra em sangria no terco
inferior, dissolvida no fundo por uma mascara em gradiente.
"""
import base64, pathlib
from PIL import Image, ImageFilter
import numpy as np

D = pathlib.Path(__file__).parent
W, H = 1080, 1920

# ------------------------------------------------------------------ conteudo
MARCA    = 'NOME DA LOJA'
LABEL    = 'Dia dos Pais'
LINHA_A  = ['O presente certo', 'não é o mais caro.']
LINHA_B  = ['É o mais ele.']
ASSINA   = 'As marcas que ele veste, em um lugar só.'
ARROBA   = '@nomedaloja'

# ------------------------------------------------------------------- paleta
ESCURO = np.array([0x2A, 0x24, 0x1F], np.float32)   # topo / vinheta lateral
CLARO  = np.array([0xAD, 0xA0, 0x8F], np.float32)   # centro do refletor
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

k = np.clip((0.05 + 0.86 * pool * topo + 0.30 * horizonte + sombra) * lados, 0, 1)
base = ESCURO[None, None, :] * (1 - k[:, :, None]) + CLARO[None, None, :] * k[:, :, None]


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
FOTO_TOPO_CABECA = 0.051   # onde comeca a cabeca no original (fracao da altura)
FOTO_CABECA_Y = 946        # onde a cabeca deve cair no canvas
FOTO_FUSAO = 360           # altura do degrade de fusao, em px

foto_src = D / 'foto.jpg'
tem_foto = foto_src.exists()

if tem_foto:
    ph = Image.open(foto_src).convert('RGB')
    p = np.asarray(ph).astype(np.float32)

    # 1. neutraliza o fundo do estudio (cinza-azulado) usando-o como referencia
    ref = p[200:900, 150:900].reshape(-1, 3).mean(0)
    p *= (ref.mean() / ref)[None, None, :]

    # 2. grade da campanha: puxa o neutro para o greige quente
    p *= np.array([1.03, 0.945, 0.855], np.float32)[None, None, :]

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
<title>Dia dos Pais — {MARCA} (Stories)</title>
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
.marca{{left:0;top:150px;width:{W}px;text-align:center;
       font-weight:300;font-size:38px;letter-spacing:.40em;text-indent:.40em;}}
.regua{{left:496px;top:232px;width:88px;height:1px;
       background:{AREIA};opacity:.55;}}

/* ---------------------------------------------------------- titulo */
.label{{left:92px;top:352px;font-weight:400;font-size:21px;
       letter-spacing:.42em;color:{AREIA};}}
.tracinho{{left:92px;top:398px;width:44px;height:1px;background:{AREIA};opacity:.7;}}

.tit-a{{left:92px;top:440px;width:900px;text-align:left;
       font-weight:250;font-size:84px;line-height:1.02;letter-spacing:.010em;}}
.tit-b{{right:92px;top:694px;width:900px;text-align:right;
       font-weight:250;font-size:84px;line-height:1.02;letter-spacing:.010em;}}

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

  <div class="marca">{MARCA}</div>
  <div class="regua"></div>

  <div class="label">{LABEL}</div>
  <div class="tracinho"></div>
  <div class="tit-a">{BR.join(LINHA_A)}</div>
  <div class="tit-b">{BR.join(LINHA_B)}</div>

  <div class="regua2"></div>
  <div class="assina">{ASSINA}</div>
  <div class="arroba">{ARROBA}</div>
</div>
"""

out = D.parent / 'dia-dos-pais-stories.html'
out.write_text(html, encoding='utf-8')
print(f'{out.name}: {len(html)} bytes | foto de campanha: {"sim" if tem_foto else "nao"}')
