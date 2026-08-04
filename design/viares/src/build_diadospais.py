"""Ensaio de Dia dos Pais — Instagram Stories 1080×1920.

Mesma filosofia da peça de oferta (../FILOSOFIA-luz-medida.md): campo escuro,
serifada de contraste alto no monumento, monoespaçada em corpo mínimo na
anotação, filetes de 1px dividindo as regiões.

A diferença é que aqui a data manda. Dia dos Pais 2026 cai em 09/08 — a peça
é construída em torno desse prazo, não em torno do serviço.

Os três quadros são ENCAIXES DE FOTO: ficam com marcas de corte e cruz de
registro (a linguagem da folha de contato) para que a peça se sustente antes
das imagens entrarem. No Canva, basta arrastar a foto sobre cada quadro.

    python3 src/build_diadospais.py   # gera o HTML
    python3 src/shoot_diadospais.py   # renderiza o PNG
"""

import base64
import pathlib

import numpy as np
from PIL import Image, ImageFilter

D = pathlib.Path(__file__).parent
OUT = D.parent
FONTS = pathlib.Path('/root/.claude/skills/canvas-design/canvas-fonts')

W, H = 1080, 1920
M = 96
CW = W - 2 * M            # 888

# ----------------------------------------------------------------- editáveis
DATA_PAIS = '09 DE AGOSTO'
VAGAS = '05'
MINUTOS = '30'
FOTOS = '15'
PRECO = '250'
PALAVRA = 'PAI'           # palavra-chave da campanha, pedida no direct
HANDLE = '@viaresfotografia'
LEGENDAS = ['PAI & FILHOS', 'RETRATO', 'FAMÍLIA']

# ------------------------------------------------------------------- paleta
INK = '#12100C'
BONE = '#F4EFE7'
GOLD = '#BE9A62'
FAINT = 'rgba(244,239,231,.42)'
HAIR = 'rgba(190,154,98,.34)'

# --------------------------------------------------- ritmo vertical do campo
# Área segura do Stories: 250px no topo, 250px na base.
Y_HEAD, Y_HEADRULE = 280, 338
Y_KICKER, Y_HERO = 396, 458
Y_MARK, Y_SUB = 656, 692
Y_SLOTS = 748
Y_SLOTRULE = 1168
Y_FIGS = 1214
Y_CTA = 1410
Y_HANDLE = 1546

# --------------------------------------------------------- encaixes de foto
COLS = 3
SGAP = 30
SW = (CW - SGAP * (COLS - 1)) // COLS      # 276
SH = round(SW * 1.25)                       # 345 — proporção 4:5


def field():
    """Campo escuro com grão fino e vinheta — a luz concentrada no centro."""
    rng = np.random.default_rng(19)
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

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * .72)) ** 2 + ((yy - H / 2) / (H * .78)) ** 2)
    vig = np.clip(1 - r ** 2 * .55, .58, 1.0)

    grain = octave(150, 1.5) + octave(40, 1.0) + rng.normal(0, 1.5, (H, W)).astype(np.float32)
    Image.fromarray(np.clip(base * vig[:, :, None] + grain[:, :, None], 0, 255).astype(np.uint8)) \
         .save(D / 'bg_field_pais.jpg', quality=95)
    return 'bg_field_pais.jpg'


def b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def face(family, weight, path):
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"src:url(data:font/ttf;base64,{b64(path)}) format('truetype');}}")


def slots(top):
    """Três encaixes com marcas de corte e cruz de registro."""
    out = []
    for i, legenda in enumerate(LEGENDAS):
        x = M + i * (SW + SGAP)
        a = 0.045 + i * 0.035                       # densidade levemente crescente
        out.append(
            f'<div class="slot" data-slot="{i + 1}" '
            f'style="left:{x}px;top:{top}px;background:rgba(244,239,231,{a:.3f});">'
            '<i class="c tl"></i><i class="c tr"></i><i class="c bl"></i><i class="c br"></i>'
            '<i class="reg rh"></i><i class="reg rv"></i>'
            '</div>'
            f'<div class="sl" style="left:{x}px;top:{top + SH + 12}px;">{legenda}</div>')
    return '\n  '.join(out)


bg = field()
SLOTS = slots(Y_SLOTS)
COLW = CW // 3

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

.lbl{{font-size:19px;font-weight:400;letter-spacing:.34em;color:{FAINT};
     text-transform:uppercase;}}
.lbl.g{{color:{GOLD};}}
.rule{{left:{M}px;width:{CW}px;height:1px;background:{HAIR};}}
.hero{{left:{M}px;width:{CW}px;font-family:'Italiana',serif;color:{BONE};
      font-size:160px;line-height:1;letter-spacing:.005em;}}

/* --- encaixes de foto: marcas de corte + cruz de registro --------------- */
.slot{{position:absolute;width:{SW}px;height:{SH}px;
      border:1px solid rgba(190,154,98,.46);}}
.slot i{{position:absolute;display:block;}}
.c{{width:20px;height:20px;border:0 solid rgba(190,154,98,.75);}}
.tl{{left:11px;top:11px;border-top-width:1px;border-left-width:1px;}}
.tr{{right:11px;top:11px;border-top-width:1px;border-right-width:1px;}}
.bl{{left:11px;bottom:11px;border-bottom-width:1px;border-left-width:1px;}}
.br{{right:11px;bottom:11px;border-bottom-width:1px;border-right-width:1px;}}
.reg{{background:rgba(190,154,98,.42);}}
.rh{{left:50%;top:50%;width:26px;height:1px;transform:translate(-50%,-50%);}}
.rv{{left:50%;top:50%;width:1px;height:26px;transform:translate(-50%,-50%);}}
.sl{{position:absolute;width:{SW}px;text-align:center;font-size:15px;
    letter-spacing:.22em;color:rgba(244,239,231,.40);text-transform:uppercase;}}

/* --- números medidos ---------------------------------------------------- */
.col{{position:absolute;top:{Y_FIGS}px;width:{COLW}px;text-align:center;}}
.fig{{font-family:'Italiana',serif;font-size:82px;line-height:.92;color:{BONE};}}
/* A Italiana não traz o cifrão — as unidades vão na monoespaçada. */
.fig .u{{font-family:'PlexMono',monospace;font-size:24px;letter-spacing:.10em;
        color:{GOLD};}}
.cap{{font-size:16px;letter-spacing:.26em;color:{FAINT};text-transform:uppercase;
     margin-top:20px;}}
.vdiv{{position:absolute;top:{Y_FIGS - 6}px;width:1px;height:128px;background:{HAIR};}}

/* --- chamada ------------------------------------------------------------ */
.cta{{left:{(W - 660) // 2}px;top:{Y_CTA}px;width:660px;height:98px;background:{GOLD};}}
.ctat{{left:{(W - 660) // 2}px;top:{Y_CTA + 36}px;width:660px;text-align:center;
      font-size:24px;font-weight:700;letter-spacing:.20em;color:{INK};}}
.handle{{left:0;top:{Y_HANDLE}px;width:{W}px;text-align:center;font-size:18px;
        letter-spacing:.30em;color:rgba(244,239,231,.40);}}
"""

body = f"""  <img class="bg" src="data:image/jpeg;base64,{b64(D / bg)}" alt="">

  <div class="lbl" style="left:{M}px;top:{Y_HEAD}px;">VIARES FOTOGRAFIA</div>
  <div class="lbl" style="left:{M}px;top:{Y_HEAD}px;width:{CW}px;text-align:right;">PARAGOMINAS · PA</div>
  <div class="rule" style="top:{Y_HEADRULE}px;"></div>

  <div class="lbl g" style="left:{M}px;top:{Y_KICKER}px;">ENSAIO EXPRESSO — {VAGAS} VAGAS</div>
  <div class="hero" style="top:{Y_HERO}px;">dia dos pais</div>
  <div class="rule" style="top:{Y_MARK}px;width:120px;background:{GOLD};height:2px;"></div>
  <div class="lbl" style="left:{M}px;top:{Y_SUB}px;">AGENDA ABERTA ATÉ {DATA_PAIS}</div>

  {SLOTS}

  <div class="rule" style="top:{Y_SLOTRULE}px;"></div>

  <div class="col" style="left:{M}px;">
    <div class="fig">{MINUTOS}<span class="u"> MIN</span></div>
    <div class="cap">de sessão</div>
  </div>
  <div class="vdiv" style="left:{M + COLW}px;"></div>
  <div class="col" style="left:{M + COLW}px;">
    <div class="fig">{FOTOS}</div>
    <div class="cap">fotos tratadas</div>
  </div>
  <div class="vdiv" style="left:{M + COLW * 2}px;"></div>
  <div class="col" style="left:{M + COLW * 2}px;">
    <div class="fig"><span class="u">R$ </span>{PRECO}</div>
    <div class="cap">à vista</div>
  </div>

  <div class="cta"></div>
  <div class="ctat">MANDA {PALAVRA} NO DIRECT</div>
  <div class="handle">{HANDLE}</div>"""

html = f"""<meta name="hz:slide-selector" content=".page">
<title>Viares — Dia dos Pais · Stories</title>
<style>{css}</style>

<div class="page" data-document-role="page" data-label="Dia dos Pais · Stories"
     data-canvas-width="{W}" data-canvas-height="{H}">
{body}
</div>
"""

(OUT / 'viares-diadospais-stories.html').write_text(html, encoding='utf-8')
print(f'ok — encaixes {SW}x{SH}, terminam em y = {Y_SLOTS + SH + 12 + 20}')
