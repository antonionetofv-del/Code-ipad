import base64, pathlib
from PIL import Image, ImageFilter, ImageDraw
import numpy as np

D = pathlib.Path(__file__).parent
W, H = 1080, 1920

# ---------------------------------------------------------------- background
rng = np.random.default_rng(11)
top = np.array([0xB8, 0xB8, 0xBA], np.float32)
bot = np.array([0x93, 0x93, 0x93], np.float32)
t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None] ** 1.2
base = np.repeat(top[None, None, :] * (1 - t) + bot[None, None, :] * t, W, axis=1)

def octave(scale, amp):
    small = rng.normal(0, 1, (max(2, H // scale), max(2, W // scale))).astype(np.float32)
    n = (small - small.min()) / (np.ptp(small) + 1e-6) * 255
    img = Image.fromarray(n.astype(np.uint8)).resize((W, H), Image.BICUBIC)
    arr = np.asarray(img.filter(ImageFilter.GaussianBlur(scale * 0.4))).astype(np.float32)
    return (arr - arr.mean()) / (arr.std() + 1e-6) * amp

mott = octave(110, 2.2) + octave(42, 1.8) + octave(15, 1.1)
grain = rng.normal(0, 2.3, (H, W)).astype(np.float32)

scr = Image.new('L', (W, H), 0)
d = ImageDraw.Draw(scr)
for _ in range(370):
    x0, y0 = rng.uniform(-60, W), rng.uniform(-60, H)
    ang = rng.normal(-0.55, 0.8)
    ln = abs(rng.normal(0, 170)) + 20
    d.line([x0, y0, x0 + np.cos(ang) * ln, y0 + np.sin(ang) * ln],
           fill=int(rng.uniform(14, 46)), width=1)
s = np.asarray(scr.filter(ImageFilter.GaussianBlur(0.9))).astype(np.float32)
s = (s - s.mean()) * 0.75

Image.fromarray(np.clip(base + (mott + grain + s)[:, :, None], 0, 255).astype(np.uint8)) \
     .save(D / 'bg_story.jpg', quality=94)

# ---------------------------------------------------------------- assets
def b64(name):
    return base64.b64encode((D / name).read_bytes()).decode()

def font_face(family, weight, file):
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{b64(file)}) format('woff2');}}")

vb, *paths = (D / 'recycle_paths.txt').read_text().strip().split('\n')
recycle = ('<svg viewBox="%s" xmlns="http://www.w3.org/2000/svg">%s</svg>'
           % (vb, ''.join(f'<path d="{p}" fill="#3D823B"/>' for p in paths)))
recycle_uri = 'data:image/svg+xml;utf8,' + recycle.replace('"', "'").replace('#', '%23')

CARD  = '#121B6E'   # card azul (escolha do usuário)
BLUE  = '#0F2B75'   # azul da marca
GREEN = '#74C96A'   # verde clareado para ler sobre o navy

HEADLINE = ['Comece a semana', 'enxergando valor', 'onde ninguém vê']
SUB = 'Iniciando mais uma semana!'

html = f"""<meta name="hz:slide-selector" content=".page">
<title>Ferro Velho Alkimin — Boa semana (Stories)</title>
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

.card{{left:60px;top:620px;width:960px;height:940px;
      background:{CARD};border-radius:53px;}}

.headline{{left:124px;top:700px;width:812px;
          font-family:'Anton',sans-serif;font-weight:400;font-size:88px;line-height:1.09;
          color:#FFFFFF;letter-spacing:-0.5px;}}
.sub{{left:124px;top:1030px;width:812px;
     font-weight:700;font-size:36px;line-height:1.4;color:#FFFFFF;}}

.rule{{top:1186px;height:4px;background:{GREEN};}}
.rule-l{{left:124px;width:176px;}}
.rule-r{{left:780px;width:176px;}}
.hlabel{{left:290px;top:1170px;width:500px;text-align:center;
        font-weight:700;font-size:27px;letter-spacing:1.4px;color:#FFFFFF;}}

.box-out{{left:243px;top:1258px;width:588px;height:226px;
         border:3px solid #FFFFFF;border-radius:38px;}}
.box-in{{left:243px;top:1258px;width:594px;height:128px;
        background:#FFFFFF;border-radius:38px;}}
.b-day{{left:243px;top:1274px;width:594px;text-align:center;
       font-weight:700;font-size:34px;color:{BLUE};}}
.b-time{{left:243px;top:1322px;width:594px;text-align:center;
        font-weight:700;font-size:33px;color:{BLUE};}}
.s-day{{left:243px;top:1392px;width:588px;text-align:center;
       font-weight:700;font-size:31px;color:#FFFFFF;}}
.s-time{{left:243px;top:1432px;width:588px;text-align:center;
        font-weight:700;font-size:33px;color:#FFFFFF;}}
</style>

<div class="page" data-document-role="page" data-label="Boa semana - Stories"
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
  <div class="headline">{'<br>'.join(HEADLINE)}</div>
  <div class="sub">{SUB}</div>

  <div class="rule rule-l"></div>
  <div class="rule rule-r"></div>
  <div class="hlabel">HORÁRIO DE FUNCIONAMENTO</div>

  <div class="box-out"></div>
  <div class="box-in"></div>
  <div class="b-day">Segunda a Sexta</div>
  <div class="b-time">7:00h às 11:30h / 13:30h às 18:00h</div>
  <div class="s-day">Sábado</div>
  <div class="s-time">7:00h às 11:30h</div>
</div>
"""

(D / 'design_story.html').write_text(html, encoding='utf-8')
print('written', len(html))
