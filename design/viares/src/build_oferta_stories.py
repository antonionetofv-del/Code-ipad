"""Oferta de mini-ensaio — Instagram Stories 1080×1920.

Redesenho da peça de oferta segundo a filosofia "Luz Medida"
(ver ../FILOSOFIA-luz-medida.md): a quantidade de fotos não é escrita como
número solto, é desenhada como uma folha de contato de 10 quadros numerados,
com densidade progressiva — inventário e instrumento ao mesmo tempo.

Toda a composição respeita a área segura do Stories (250px no topo, 250px na
base), onde a interface do Instagram cobre o conteúdo.

    python3 src/build_oferta_stories.py   # gera o HTML
    python3 src/shoot_oferta.py           # renderiza o PNG
"""

import base64
import pathlib

import numpy as np
from PIL import Image, ImageFilter

D = pathlib.Path(__file__).parent
OUT = D.parent
FONTS = pathlib.Path('/root/.claude/skills/canvas-design/canvas-fonts')

W, H = 1080, 1920
M = 96                    # margem lateral
CW = W - 2 * M            # largura útil = 888

# ----------------------------------------------------------------- editáveis
VAGAS = '05'
FOTOS = 10
MINUTOS = '20'
PRAZO = '48'
MES = 'AGOSTO'
DATA = 'SÁB · 16 AGO'
HANDLE = '@viaresfotografia'

# ------------------------------------------------------------------- paleta
INK = '#12100C'           # preto quente — campo
BONE = '#F4EFE7'          # osso quente — leitura
GOLD = '#BE9A62'          # dourado envelhecido — medição
FAINT = 'rgba(244,239,231,.42)'
HAIR = 'rgba(190,154,98,.34)'


# ------------------------------------------------- campo escuro com grão fino
def field():
    rng = np.random.default_rng(7)
    top = np.array([0x16, 0x13, 0x0E], np.float32)
    bot = np.array([0x0A, 0x09, 0x07], np.float32)
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None] ** 1.15
    base = np.repeat(top[None, None, :] * (1 - t) + bot[None, None, :] * t, W, axis=1)

    def octave(scale, amp):
        small = rng.normal(0, 1, (max(2, H // scale), max(2, W // scale))).astype(np.float32)
        n = (small - small.min()) / (np.ptp(small) + 1e-6) * 255
        img = Image.fromarray(n.astype(np.uint8)).resize((W, H), Image.BICUBIC)
        arr = np.asarray(img.filter(ImageFilter.GaussianBlur(scale * 0.4))).astype(np.float32)
        return (arr - arr.mean()) / (arr.std() + 1e-6) * amp

    # vinheta suave: concentra a luz no centro do campo
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * .72)) ** 2 + ((yy - H / 2) / (H * .78)) ** 2)
    vig = np.clip(1 - r ** 2 * .55, .58, 1.0)

    grain = octave(150, 1.5) + octave(40, 1.0) + rng.normal(0, 1.5, (H, W)).astype(np.float32)
    out = np.clip(base * vig[:, :, None] + grain[:, :, None], 0, 255)
    Image.fromarray(out.astype(np.uint8)).save(D / 'bg_field.jpg', quality=95)
    return 'bg_field.jpg'


# ------------------------------------------------------------------- assets
def b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def face(family, weight, path):
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"src:url(data:font/ttf;base64,{b64(path)}) format('truetype');}}")


# ------------------------------------------- folha de contato: 10 quadros
# Largura do bloco travada na largura útil, para alinhar com os filetes.
COLS, ROWS = 5, 2
FGAP, RGAP = 37, 42
FW = (CW - FGAP * (COLS - 1)) // COLS          # 148 — o vão fecha a largura útil
FH = round(FW * 1.25)                          # 185 — proporção 4:5, de fotografia
NUMY = 9                                        # respiro entre quadro e índice

# --------------------------------------------------- ritmo vertical do campo
# Toda a composição vive entre 250px e 1670px: fora disso a interface do
# Instagram cobre o conteúdo. Cada valor abaixo foi acertado contra o vizinho.
Y_HEAD = 286
Y_HEADRULE = 338
Y_KICKER = 392
Y_HERO = 452
Y_MARK = 668
Y_SESSION = 700
Y_SHEET = 748
Y_SHEET_RULE = 1232
Y_CAPTION = 1262
Y_FIGS = 1330
Y_CTA = 1508
Y_HANDLE = 1638


def contact_sheet(top):
    """Dez quadros numerados, com densidade progressiva. A escala de degraus
    é o que transforma a contagem em instrumento."""
    cells = []
    for i in range(FOTOS):
        c, r = i % COLS, i // COLS
        x = M + c * (FW + FGAP)
        y = top + r * (FH + RGAP)
        # densidade progressiva de 4,5% a 25% — legível, jamais decorativa
        a = 0.045 + (i / (FOTOS - 1)) * 0.205
        cells.append(
            f'<div class="fr" style="left:{x}px;top:{y}px;'
            f'background:rgba(244,239,231,{a:.3f});"></div>'
            f'<div class="fn" style="left:{x}px;top:{y + FH + NUMY}px;">{i + 1:02d}</div>')
    return '\n  '.join(cells)


SHEET = contact_sheet(Y_SHEET)

bg = field()

css = f"""
{face('Italiana', 400, FONTS / 'Italiana-Regular.ttf')}
{face('PlexMono', 400, FONTS / 'IBMPlexMono-Regular.ttf')}
{face('PlexMono', 700, FONTS / 'IBMPlexMono-Bold.ttf')}

html,body{{margin:0;padding:0;background:#2A2A2E;}}
body{{display:flex;justify-content:center;align-items:flex-start;}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
      font-family:'PlexMono',monospace;background:{INK};}}
.page > *{{position:absolute;}}
.bg{{left:0;top:0;width:{W}px;height:{H}px;}}

/* --- anotação: monoespaçada, corpo mínimo, entreletras abertas ---------- */
.lbl{{font-size:19px;font-weight:400;letter-spacing:.34em;color:{FAINT};
     text-transform:uppercase;}}
.lbl.g{{color:{GOLD};}}

/* --- filetes: 1px, dividem regiões como uma tabela de laboratório ------- */
.rule{{left:{M}px;width:{CW}px;height:1px;background:{HAIR};}}

/* --- monumento: serifada de contraste alto, traço fino ------------------ */
.hero{{left:{M}px;width:{CW}px;font-family:'Italiana',serif;color:{BONE};
      font-size:176px;line-height:1;letter-spacing:.005em;}}

/* --- folha de contato --------------------------------------------------- */
.fr{{width:{FW}px;height:{FH}px;border:1px solid rgba(190,154,98,.50);}}
.fn{{width:{FW}px;font-size:15px;letter-spacing:.22em;color:rgba(244,239,231,.36);
    text-align:center;}}

/* --- números medidos ---------------------------------------------------- */
.fig{{font-family:'Italiana',serif;font-size:92px;line-height:.92;color:{BONE};}}
.fig .u{{font-size:29px;letter-spacing:.10em;color:{GOLD};}}
.cap{{font-size:17px;letter-spacing:.28em;color:{FAINT};text-transform:uppercase;
     margin-top:18px;}}
.col{{position:absolute;top:{Y_FIGS}px;}}
.vdiv{{position:absolute;top:{Y_FIGS - 4}px;width:1px;height:136px;background:{HAIR};}}

/* --- chamada ------------------------------------------------------------ */
.cta{{left:{(W - 660) // 2}px;top:{Y_CTA}px;width:660px;height:98px;background:{GOLD};}}
.ctat{{left:{(W - 660) // 2}px;top:{Y_CTA + 36}px;width:660px;text-align:center;
      font-size:24px;font-weight:700;letter-spacing:.20em;color:{INK};}}
.handle{{left:0;top:{Y_HANDLE}px;width:{W}px;text-align:center;font-size:18px;
        letter-spacing:.30em;color:rgba(244,239,231,.40);}}
"""

body = f"""  <img class="bg" src="data:image/jpeg;base64,{b64(D / bg)}" alt="">

  <!-- cabeçalho -->
  <div class="lbl" style="left:{M}px;top:{Y_HEAD}px;">VIARES FOTOGRAFIA</div>
  <div class="lbl" style="left:{M}px;top:{Y_HEAD}px;width:{CW}px;text-align:right;">PARAGOMINAS · PA</div>
  <div class="rule" style="top:{Y_HEADRULE}px;"></div>

  <!-- monumento -->
  <div class="lbl g" style="left:{M}px;top:{Y_KICKER}px;">AGENDA {MES} — {VAGAS} VAGAS</div>
  <div class="hero" style="top:{Y_HERO}px;">mini-ensaio</div>
  <div class="rule" style="top:{Y_MARK}px;width:120px;background:{GOLD};height:2px;"></div>
  <div class="lbl" style="left:{M}px;top:{Y_SESSION}px;">SESSÃO DE {MINUTOS} MINUTOS · {DATA}</div>

  <!-- folha de contato: a quantidade desenhada, não escrita -->
  {SHEET}

  <div class="rule" style="top:{Y_SHEET_RULE}px;"></div>
  <div class="lbl g" style="left:{M}px;top:{Y_CAPTION}px;width:{CW}px;text-align:center;">
    {FOTOS} FOTOS TRATADAS</div>

  <!-- números medidos -->
  <div class="col" style="left:{M}px;width:{CW // 2 - 1}px;text-align:center;">
    <div class="fig">{MINUTOS}<span class="u"> MIN</span></div>
    <div class="cap">de sessão</div>
  </div>
  <div class="vdiv" style="left:{W // 2}px;"></div>
  <div class="col" style="left:{W // 2 + 1}px;width:{CW // 2 - 1}px;text-align:center;">
    <div class="fig">{PRAZO}<span class="u"> H</span></div>
    <div class="cap">para entrega</div>
  </div>

  <!-- chamada -->
  <div class="cta"></div>
  <div class="ctat">MANDA VAGA NO DIRECT</div>
  <div class="handle">{HANDLE}</div>"""

html = f"""<meta name="hz:slide-selector" content=".page">
<title>Viares — Mini-ensaio · Stories</title>
<style>{css}</style>

<div class="page" data-document-role="page" data-label="Mini-ensaio · Stories"
     data-canvas-width="{W}" data-canvas-height="{H}">
{body}
</div>
"""

(OUT / 'viares-oferta-mini-ensaio-stories.html').write_text(html, encoding='utf-8')
print('ok — folha de contato termina em y =',
      Y_SHEET + ROWS * FH + RGAP * (ROWS - 1) + NUMY + 18)
