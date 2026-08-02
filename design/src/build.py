import base64, pathlib

D = pathlib.Path(__file__).parent

def b64(name):
    return base64.b64encode((D / name).read_bytes()).decode()

def font_face(family, weight, file):
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{b64(file)}) format('woff2');}}")

vb, *paths = (D / 'recycle_paths.txt').read_text().strip().split('\n')
recycle = ('<svg viewBox="%s" xmlns="http://www.w3.org/2000/svg">%s</svg>'
           % (vb, ''.join(f'<path d="{p}" fill="%233D823B"/>' for p in paths)))
recycle_uri = 'data:image/svg+xml;utf8,' + recycle.replace('"', "'").replace('#', '%23')

BLUE = '#0F2B75'
GREEN = '#3D823B'

HEADLINE = ['Comece a semana', 'enxergando valor', 'onde ninguém vê']
SUB = ('Boa semana! Aqui a gente transforma em recomeço<br>'
       'o que muitos já tinham dado por perdido &mdash;<br>'
       'com a sua semana não vai ser diferente.')

html = f"""<meta name="hz:slide-selector" content=".page">
<title>Ferro Velho Alkimin — Boa semana</title>
<style>
{font_face('Anton', 400, 'anton.woff2')}
{font_face('Poppins', 400, 'poppins400.woff2')}
{font_face('Poppins', 600, 'poppins600.woff2')}
{font_face('Poppins', 700, 'poppins700.woff2')}
html,body{{margin:0;padding:0;background:#2A2A2E;}}
body{{display:flex;justify-content:center;align-items:flex-start;}}
.page{{position:relative;width:1080px;height:1350px;overflow:hidden;
      font-family:'Poppins',sans-serif;}}
.page > *{{position:absolute;}}
.bg{{left:0;top:0;width:1080px;height:1350px;}}
.scrim{{left:0;top:120px;width:1080px;height:800px;
       background:linear-gradient(180deg,rgba(26,26,30,0) 0%,rgba(26,26,30,.06) 18%,
                                          rgba(26,26,30,.12) 45%,rgba(26,26,30,.10) 72%,
                                          rgba(26,26,30,0) 100%);}}
.wm{{opacity:.34;}}
.wm-l{{left:-188px;top:1074px;width:530px;}}
.wm-r{{left:896px;top:838px;width:452px;}}
.chev{{left:648px;top:8px;width:452px;height:330px;}}
.logo{{left:88px;top:48px;width:420px;}}

.headline{{left:94px;top:304px;width:920px;
          font-family:'Anton',sans-serif;font-weight:400;font-size:88px;line-height:0.97;
          color:#FFFFFF;letter-spacing:-0.5px;
          text-shadow:0 4px 20px rgba(16,16,22,.55);}}
.sub{{left:96px;top:582px;width:880px;
     font-family:'Poppins',sans-serif;font-weight:600;font-size:30px;line-height:1.40;
     color:#FFFFFF;text-shadow:0 2px 12px rgba(16,16,22,.50);}}

.rule{{top:793px;height:3px;background:{GREEN};}}
.rule-l{{left:100px;width:198px;}}
.rule-r{{left:782px;width:198px;}}
.hlabel{{left:290px;top:776px;width:500px;text-align:center;
        font-family:'Poppins',sans-serif;font-weight:700;font-size:27px;
        letter-spacing:1.4px;color:{BLUE};}}

.box-out{{left:243px;top:850px;width:588px;height:226px;
         border:3px solid {BLUE};border-radius:38px;}}
.box-in{{left:243px;top:850px;width:594px;height:128px;
        background:{BLUE};border-radius:38px;}}
.b-day{{left:243px;top:866px;width:594px;text-align:center;
       font-weight:700;font-size:34px;color:#FFFFFF;}}
.b-time{{left:243px;top:914px;width:594px;text-align:center;
        font-weight:700;font-size:33px;color:#FFFFFF;}}
.s-day{{left:243px;top:988px;width:588px;text-align:center;
       font-weight:700;font-size:31px;color:{BLUE};}}
.s-time{{left:243px;top:1029px;width:588px;text-align:center;
        font-weight:700;font-size:33px;color:{BLUE};}}
</style>

<div class="page" data-document-role="page" data-label="Boa semana"
     data-canvas-width="1080" data-canvas-height="1350">
  <img class="bg" src="data:image/jpeg;base64,{b64('bg.jpg')}" alt="Fundo cinza texturizado">
  <div class="scrim"></div>
  <img class="wm wm-l" src="{recycle_uri}" alt="">
  <img class="wm wm-r" src="{recycle_uri}" alt="">
  <svg class="chev" viewBox="0 0 452 330" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g stroke="{GREEN}" stroke-width="4" opacity=".52">
      <path d="M104 262 L262 40 L330 40 L172 262 Z"/>
      <path d="M212 262 L370 40 L438 40 L280 262 Z"/>
      <path d="M-4 262 L154 40 L222 40 L64 262 Z"/>
    </g>
  </svg>
  <img class="logo" src="data:image/png;base64,{b64('logo.png')}" alt="Ferro Velho Alkimin">

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

(D / 'design.html').write_text(html, encoding='utf-8')
print('written', len(html), 'bytes')
