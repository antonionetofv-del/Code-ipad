import base64, pathlib
from PIL import Image, ImageFilter, ImageDraw
import numpy as np

D = pathlib.Path(__file__).parent
W, H = 1080, 1920

GREEN = '#376E2B'
BLUE  = '#1E2967'

# ------------------------------------------------- light paper-gray background
rng = np.random.default_rng(23)
top = np.array([0xE6, 0xE6, 0xE6], np.float32)
bot = np.array([0xC4, 0xC4, 0xC6], np.float32)
t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None] ** 1.35
base = np.repeat(top[None, None, :] * (1 - t) + bot[None, None, :] * t, W, axis=1)

def octave(scale, amp):
    small = rng.normal(0, 1, (max(2, H // scale), max(2, W // scale))).astype(np.float32)
    n = (small - small.min()) / (np.ptp(small) + 1e-6) * 255
    img = Image.fromarray(n.astype(np.uint8)).resize((W, H), Image.BICUBIC)
    arr = np.asarray(img.filter(ImageFilter.GaussianBlur(scale * 0.4))).astype(np.float32)
    return (arr - arr.mean()) / (arr.std() + 1e-6) * amp

mott = octave(120, 2.0) + octave(44, 1.6) + octave(16, 1.0)
grain = rng.normal(0, 2.6, (H, W)).astype(np.float32)

scr = Image.new('L', (W, H), 0)
d = ImageDraw.Draw(scr)
for _ in range(340):
    x0, y0 = rng.uniform(-60, W), rng.uniform(-60, H)
    ang = rng.normal(-0.55, 0.8)
    ln = abs(rng.normal(0, 165)) + 20
    d.line([x0, y0, x0 + np.cos(ang) * ln, y0 + np.sin(ang) * ln],
           fill=int(rng.uniform(12, 40)), width=1)
s = np.asarray(scr.filter(ImageFilter.GaussianBlur(0.9))).astype(np.float32)
s = (s - s.mean()) * 0.7

Image.fromarray(np.clip(base + (mott + grain + s)[:, :, None], 0, 255).astype(np.uint8)) \
     .save(D / 'bg_curio.jpg', quality=94)

# ------------------------------------------------------------------- assets
def b64(name):
    return base64.b64encode((D / name).read_bytes()).decode()

def font_face(family, weight, file):
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{b64(file)}) format('woff2');}}")

vb, *paths = (D / 'recycle_paths.txt').read_text().strip().split('\n')
recycle = ('<svg viewBox="%s" xmlns="http://www.w3.org/2000/svg">%s</svg>'
           % (vb, ''.join(f'<path d="{p}" fill="#4F8F44"/>' for p in paths)))
recycle_uri = 'data:image/svg+xml;utf8,' + recycle.replace('"', "'").replace('#', '%23')

html = f"""<meta name="hz:slide-selector" content=".page">
<title>Ferro Velho Alkimin — Curiosidade rápida</title>
<style>
{font_face('Poppins', 400, 'poppins400.woff2')}
{font_face('Poppins', 600, 'poppins600.woff2')}
{font_face('Poppins', 700, 'poppins700.woff2')}
html,body{{margin:0;padding:0;background:#2A2A2E;}}
body{{display:flex;justify-content:center;align-items:flex-start;}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
      font-family:'Poppins',sans-serif;}}
.page > *{{position:absolute;}}
.bg{{left:0;top:0;width:{W}px;height:{H}px;}}
.wm{{opacity:.30;}}
.wm-tr{{left:836px;top:36px;width:230px;}}
.wm-bl{{left:-74px;top:1592px;width:300px;}}

.logo{{left:56px;top:48px;width:380px;}}

.g{{color:{GREEN};}} .b{{color:{BLUE};}}
.tagline{{left:60px;top:300px;width:980px;
         font-weight:700;font-size:56px;line-height:1.14;color:{GREEN};}}
.kicker{{left:60px;top:468px;width:980px;
        font-weight:700;font-size:70px;line-height:1.10;color:{GREEN};}}
.rule{{left:62px;top:674px;width:440px;height:7px;background:{GREEN};border-radius:4px;}}

.shadow{{left:70px;top:1508px;width:930px;height:96px;
        background:radial-gradient(ellipse at 50% 50%, rgba(38,38,44,.34) 0%,
                                    rgba(38,38,44,.16) 42%, rgba(38,38,44,0) 72%);}}
.truck{{left:25px;top:700px;width:1030px;}}

.fact{{left:60px;top:1640px;width:990px;
      font-weight:700;font-size:53px;line-height:1.18;color:{GREEN};}}
</style>

<div class="page" data-document-role="page" data-label="Curiosidade rápida"
     data-canvas-width="{W}" data-canvas-height="{H}">
  <img class="bg" src="data:image/jpeg;base64,{b64('bg_curio.jpg')}" alt="Fundo cinza texturizado">
  <img class="wm wm-tr" src="{recycle_uri}" alt="">
  <img class="wm wm-bl" src="{recycle_uri}" alt="">
  <img class="logo" src="data:image/png;base64,{b64('logo.png')}" alt="Ferro Velho Alkimin">

  <div class="tagline">Tradição e confiança<br>há mais de <span class="b">25 anos</span></div>
  <div class="kicker">Curiosidade rápida<br>sobre <span class="b">FERRO VELHO</span></div>
  <div class="rule"></div>

  <div class="shadow"></div>
  <img class="truck" src="data:image/png;base64,{b64('truck.png')}" alt="Caminhão Ferro Velho Alkimin">

  <div class="fact"><span class="b">O BRASIL</span> recicla <span class="b">97%</span> das<br>latas de alumínio e lidera<br>o ranking mundial há <span class="b">16 anos</span></div>
</div>
"""

(D / 'design_curio.html').write_text(html, encoding='utf-8')
print('written', len(html))
