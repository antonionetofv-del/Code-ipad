"""Gera as peças de captação da Viares Fotografia.

Cada peça sai como um HTML autocontido (fontes e fundo embutidos em base64),
no mesmo padrão do resto do repositório: o HTML é a fonte da verdade e pode ser
importado no Canva; o PNG é o export para publicação.

    python3 src/build_viares.py     # gera os .html
    python3 src/shoot.py            # renderiza os .png
"""

import base64
import pathlib

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

D = pathlib.Path(__file__).parent
OUT = D.parent

# ----------------------------------------------------------------- editáveis
# Ajuste aqui antes de publicar a peça de oferta.
VAGAS = '5'
DATA_OFERTA = 'SÁBADO · 16 DE AGOSTO'
MES_AGENDA = 'AGENDA · AGOSTO'
HANDLE = '@viaresfotografia'

# ------------------------------------------------------------------- paleta
SAND = (0xEF, 0xE8, 0xDF)   # areia clara — fundo principal
SAND_DK = (0xDE, 0xD3, 0xC6)  # areia, base do degradê
INK = '#17140F'             # preto quente — texto e fundo escuro
INK_RGB = (0x17, 0x14, 0x0F)
INK_DK = (0x0D, 0x0B, 0x08)
GOLD = '#A8814F'            # dourado suave — acento
BONE = '#F6F1EA'            # off-white sobre fundo escuro
MUTED = '#6B6055'           # texto de apoio sobre areia


# --------------------------------------------------------- fundo texturizado
def texture(name, w, h, top, bot, seed, grain=2.4, fibers=True):
    """Papel/linho procedural: degradê vertical + manchas em três oitavas +
    grão fino + fibras finas em diagonal. Mesma técnica dos outros builds."""
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None] ** 1.3
    base = np.repeat(
        np.array(top, np.float32)[None, None, :] * (1 - t)
        + np.array(bot, np.float32)[None, None, :] * t,
        w, axis=1)

    def octave(scale, amp):
        small = rng.normal(0, 1, (max(2, h // scale), max(2, w // scale))).astype(np.float32)
        n = (small - small.min()) / (np.ptp(small) + 1e-6) * 255
        img = Image.fromarray(n.astype(np.uint8)).resize((w, h), Image.BICUBIC)
        arr = np.asarray(img.filter(ImageFilter.GaussianBlur(scale * 0.4))).astype(np.float32)
        return (arr - arr.mean()) / (arr.std() + 1e-6) * amp

    noise = octave(130, 2.2) + octave(46, 1.5) + octave(15, 0.9)
    noise += rng.normal(0, grain, (h, w)).astype(np.float32)

    if fibers:
        scr = Image.new('L', (w, h), 0)
        d = ImageDraw.Draw(scr)
        for _ in range(300):
            x0, y0 = rng.uniform(-60, w), rng.uniform(-60, h)
            ang = rng.normal(-0.5, 0.85)
            ln = abs(rng.normal(0, 150)) + 20
            d.line([x0, y0, x0 + np.cos(ang) * ln, y0 + np.sin(ang) * ln],
                   fill=int(rng.uniform(10, 34)), width=1)
        s = np.asarray(scr.filter(ImageFilter.GaussianBlur(0.9))).astype(np.float32)
        noise += (s - s.mean()) * 0.6

    Image.fromarray(np.clip(base + noise[:, :, None], 0, 255).astype(np.uint8)) \
         .save(D / name, quality=94)
    return name


# ------------------------------------------------------------------- assets
def b64(name):
    return base64.b64encode((D / name).read_bytes()).decode()


def face(family, weight, file):
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{b64(file)}) format('woff2');}}")


def fonts():
    return '\n'.join([
        face('Anton', 400, 'anton.woff2'),
        face('Poppins', 400, 'poppins400.woff2'),
        face('Poppins', 600, 'poppins600.woff2'),
        face('Poppins', 700, 'poppins700.woff2'),
    ])


def shell(title, w, h, label, css, body):
    return f"""<meta name="hz:slide-selector" content=".page">
<title>{title}</title>
<style>
{fonts()}
html,body{{margin:0;padding:0;background:#2A2A2E;}}
body{{display:flex;justify-content:center;align-items:flex-start;}}
.page{{position:relative;width:{w}px;height:{h}px;overflow:hidden;
      font-family:'Poppins',sans-serif;}}
.page > *{{position:absolute;}}
.bg{{left:0;top:0;width:{w}px;height:{h}px;}}
.anton{{font-family:'Anton',sans-serif;font-weight:400;}}
{css}
</style>

<div class="page" data-document-role="page" data-label="{label}"
     data-canvas-width="{w}" data-canvas-height="{h}">
{body}
</div>
"""


# ===========================================================================
# Peça 1 — Lançamento do design gráfico (1080×1350, feed 4:5)
# ===========================================================================
def lancamento():
    W, H = 1080, 1350
    bg = texture('bg_sand_1350.jpg', W, H, SAND, SAND_DK, seed=11)

    css = f"""
.eyebrow{{left:80px;top:96px;font-size:23px;font-weight:600;letter-spacing:.30em;
         color:{MUTED};}}
.eyerule{{left:80px;top:146px;width:920px;height:1px;background:rgba(23,20,15,.22);}}
.tag{{right:80px;top:84px;padding:11px 26px;border:1.5px solid {GOLD};border-radius:999px;
     font-size:20px;font-weight:600;letter-spacing:.20em;color:{GOLD};}}

.head{{left:76px;top:250px;width:940px;font-size:132px;line-height:1.01;
      letter-spacing:-.005em;color:{INK};}}
.gold{{color:{GOLD};}}

.rule{{left:80px;top:706px;width:150px;height:7px;background:{GOLD};border-radius:4px;}}

.sub{{left:80px;top:774px;width:880px;font-size:39px;font-weight:400;line-height:1.44;
     color:{MUTED};}}
.sub b{{font-weight:600;color:{INK};}}

.chips{{left:80px;top:1000px;display:flex;gap:18px;}}
.chip{{padding:15px 40px;border:1.5px solid rgba(23,20,15,.30);border-radius:999px;
      font-size:25px;font-weight:600;letter-spacing:.16em;color:{INK};}}
.chip.on{{background:{INK};border-color:{INK};color:{BONE};}}

.bar{{left:0;top:1158px;width:{W}px;height:192px;background:{INK};}}
.cta{{left:0;top:1218px;width:{W}px;text-align:center;font-size:43px;font-weight:600;
     color:{BONE};}}
.cta em{{font-style:normal;color:{GOLD};font-weight:700;letter-spacing:.06em;}}
.handle{{left:0;top:1284px;width:{W}px;text-align:center;font-size:25px;font-weight:400;
        letter-spacing:.14em;color:rgba(246,241,234,.60);}}
"""

    body = f"""  <img class="bg" src="data:image/jpeg;base64,{b64(bg)}" alt="Fundo areia texturizado">
  <div class="eyebrow">VIARES · PARAGOMINAS-PA</div>
  <div class="eyerule"></div>
  <div class="tag">NOVO SERVIÇO</div>

  <div class="head anton">FOTO BOA<br>EM ARTE RUIM<br><span class="gold">NÃO VENDE.</span></div>
  <div class="rule"></div>

  <div class="sub">Agora a Viares não entrega só a foto.<br>
  Entrega o post pronto para publicar — <b>foto profissional e arte no mesmo pacote.</b></div>

  <div class="chips">
    <div class="chip">FOTO</div>
    <div class="chip">VÍDEO</div>
    <div class="chip on">DESIGN</div>
  </div>

  <div class="bar"></div>
  <div class="cta">Manda <em>DESIGN</em> no direct</div>
  <div class="handle">{HANDLE}</div>"""

    (OUT / 'viares-lancamento-design.html').write_text(
        shell('Viares — Lançamento do design gráfico', W, H, 'Lançamento design', css, body),
        encoding='utf-8')


# ===========================================================================
# Peça 2 — Oferta de entrada / mini-ensaio (1080×1350, feed 4:5)
# ===========================================================================
def oferta():
    W, H = 1080, 1350
    bg = texture('bg_ink_1350.jpg', W, H, INK_RGB, INK_DK, seed=27, grain=1.7, fibers=False)

    css = f"""
.eyebrow{{left:80px;top:96px;font-size:23px;font-weight:600;letter-spacing:.30em;
         color:{GOLD};}}
.eyerule{{left:80px;top:146px;width:920px;height:1px;background:rgba(246,241,234,.20);}}

.vagas{{left:74px;top:206px;font-size:210px;line-height:.92;letter-spacing:-.01em;
       color:{GOLD};}}
.vagas span{{font-size:96px;letter-spacing:.02em;}}

.head{{left:80px;top:470px;width:920px;font-size:104px;line-height:1.04;color:{BONE};}}

.rule{{left:80px;top:718px;width:150px;height:7px;background:{GOLD};border-radius:4px;}}

.list{{left:80px;top:784px;width:900px;font-size:36px;font-weight:400;line-height:2.06;
      color:rgba(246,241,234,.88);}}
.list b{{font-weight:600;color:{BONE};}}
.dot{{display:inline-block;width:9px;height:9px;border-radius:50%;background:{GOLD};
     vertical-align:middle;margin:0 22px 6px 0;}}

.date{{left:80px;top:1032px;font-size:31px;font-weight:600;letter-spacing:.16em;
      color:{GOLD};}}
.limit{{left:80px;top:1084px;font-size:26px;font-weight:400;color:rgba(246,241,234,.55);}}

.bar{{left:0;top:1158px;width:{W}px;height:192px;background:{BONE};}}
.cta{{left:0;top:1218px;width:{W}px;text-align:center;font-size:43px;font-weight:600;
     color:{INK};}}
.cta em{{font-style:normal;color:{GOLD};font-weight:700;letter-spacing:.06em;}}
.handle{{left:0;top:1284px;width:{W}px;text-align:center;font-size:25px;font-weight:400;
        letter-spacing:.14em;color:rgba(23,20,15,.50);}}
"""

    body = f"""  <img class="bg" src="data:image/jpeg;base64,{b64(bg)}" alt="Fundo preto texturizado">
  <div class="eyebrow">{MES_AGENDA} · PARAGOMINAS-PA</div>
  <div class="eyerule"></div>

  <div class="vagas anton">{VAGAS} <span>VAGAS</span></div>
  <div class="head anton">MINI-ENSAIO<br>DE 20 MINUTOS</div>
  <div class="rule"></div>

  <div class="list">
    <span class="dot"></span><b>20 minutos</b> de sessão com direção de pose<br>
    <span class="dot"></span><b>5 fotos</b> tratadas e prontas para o feed<br>
    <span class="dot"></span>Entrega em <b>48 horas</b> por galeria online
  </div>

  <div class="date">{DATA_OFERTA}</div>
  <div class="limit">Quando as vagas acabarem, esse post sai do ar.</div>

  <div class="bar"></div>
  <div class="cta">Manda <em>VAGA</em> no direct</div>
  <div class="handle">{HANDLE}</div>"""

    (OUT / 'viares-oferta-mini-ensaio.html').write_text(
        shell('Viares — Oferta mini-ensaio', W, H, 'Oferta mini-ensaio', css, body),
        encoding='utf-8')


# ===========================================================================
# Peça 3 — Stories de qualificação (1080×1920)
# O miolo entre 1150px e 1560px fica livre de propósito: é onde entra a
# figurinha de enquete do Instagram.
# ===========================================================================
def stories():
    W, H = 1080, 1920
    bg = texture('bg_sand_1920.jpg', W, H, SAND, SAND_DK, seed=41)

    css = f"""
.eyebrow{{left:0;top:172px;width:{W}px;text-align:center;font-size:23px;font-weight:600;
         letter-spacing:.30em;color:{MUTED};}}
.eyerule{{left:390px;top:228px;width:300px;height:1px;background:rgba(23,20,15,.22);}}

.head{{left:0;top:356px;width:{W}px;text-align:center;font-size:108px;line-height:1.07;
      letter-spacing:-.005em;color:{INK};}}
.gold{{color:{GOLD};}}

.sub{{left:120px;top:1000px;width:840px;text-align:center;font-size:36px;font-weight:400;
     line-height:1.48;color:{MUTED};}}

.arrow{{left:0;top:1142px;width:{W}px;text-align:center;font-size:44px;color:{GOLD};}}

.mark{{left:0;top:1668px;width:{W}px;text-align:center;font-size:66px;letter-spacing:.22em;
      color:{INK};}}
.markrule{{left:440px;top:1772px;width:200px;height:5px;background:{GOLD};border-radius:3px;}}
.handle{{left:0;top:1804px;width:{W}px;text-align:center;font-size:27px;font-weight:400;
        letter-spacing:.14em;color:{MUTED};}}
"""

    body = f"""  <img class="bg" src="data:image/jpeg;base64,{b64(bg)}" alt="Fundo areia texturizado">
  <div class="eyebrow">VIARES FOTOGRAFIA · PARAGOMINAS-PA</div>
  <div class="eyerule"></div>

  <div class="head anton">SEU FEED<br>TEM FOTO<br>PROFISSIONAL<br>OU FOTO DE<br><span class="gold">CELULAR?</span></div>

  <div class="sub">Abre o perfil do seu negócio agora<br>e responde com sinceridade</div>
  <div class="arrow">&#8595;</div>

  <div class="mark anton">VIARES</div>
  <div class="markrule"></div>
  <div class="handle">{HANDLE}</div>"""

    (OUT / 'viares-stories-enquete.html').write_text(
        shell('Viares — Stories de qualificação', W, H, 'Stories enquete', css, body),
        encoding='utf-8')


if __name__ == '__main__':
    lancamento()
    oferta()
    stories()
    print('ok — 3 peças geradas em', OUT)
