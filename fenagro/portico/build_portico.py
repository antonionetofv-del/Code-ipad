#!/usr/bin/env python3
"""Gera as tres pecas do portico de entrada da II FENAGRO-MR.

Medidas reais:
  - laterais (2x): 0,60 m de largura x 5,00 m de altura
  - testeira:      3,20 m de largura x 0,60 m de altura

O CSS usa milimetros em tamanho real; a resolucao final e definida na
renderizacao. As luzes do fundo sao gradientes, nao imagem, para nao depender
da resolucao dos recortes.
"""
import base64
import pathlib

BASE = pathlib.Path(__file__).parent
ASSETS = BASE / "assets_hi"
OUT = BASE / "portico-fenagro.html"

MIME = {".png": "image/png", ".jpg": "image/jpeg"}


def data_uri(name):
    p = ASSETS / name
    return "data:%s;base64,%s" % (MIME[p.suffix], base64.b64encode(p.read_bytes()).decode())


IMG = {n: data_uri(n) for n in (
    "logo_circ.png", "cavalgada.png", "ninho.png",
    "spons_realiza.png", "spons_apoio.png", "coopagi.png", "acaitech.png",
    "art_a.jpg", "art_b.jpg", "art_c.jpg", "art_d.jpg",
)}

SHOWS = [
    ("17/09", "QUINTA", ["Isa&iacute;as Show"]),
    ("18/09", "SEXTA", ["Leozinho Forrozeiro", "Jo&atilde;o Nunes"]),
    ("19/09", "S&Aacute;BADO", ["Xerife Bar&atilde;o", "Thiago Ara&uacute;jo"]),
    ("20/09", "DOMINGO", ["Ant&ocirc;nio Marcos", "Gleyk &amp; Gleyson",
                          "Evandro do Acordeon", "Marquinhos Par&aacute;",
                          "Deyse Bandeira"]),
]

DESTAQUES = ["SHOWS", "RODEIO", "XXIII CAVALGADA", "PARQUE DE DIVERS&Atilde;O",
             "EXPOSITORES", "PRA&Ccedil;A DE ALIMENTA&Ccedil;&Atilde;O", "E MUITO MAIS!"]

PALESTRAS = [
    ("17/09", ["CACAU"]),
    ("18/09", ["A&Ccedil;A&Iacute;"]),
    ("19/09", ["PISCICULTURA", "BOVINOCULTURA DE CORTE",
               "BOVINO DE LEITE", "ADEPAR&Aacute;"]),
]

MOSAICO = [("art_a.jpg", 560, 290), ("art_b.jpg", 560, 290),
           ("art_c.jpg", 560, 250), ("art_d.jpg", 560, 250)]


def bloco_show(dia, semana, nomes):
    linhas = "".join('<div class="sh-name">%s</div>' % n for n in nomes)
    return ('<div class="sh">'
            '<div class="sh-pill">%s <span>&middot; %s</span></div>'
            '<div class="sh-list">%s</div></div>' % (dia, semana, linhas))


def bloco_palestra(dia, temas):
    linhas = "".join('<div class="pa-tema">%s</div>' % t for t in temas)
    return '<div class="pa"><div class="pa-dia">%s</div>%s</div>' % (dia, linhas)


def bloco_foto(nome, w, h):
    alt = round(480 * h / w, 1)          # 480 mm de largura util na lateral
    return ('<img class="foto" src="%s" width="%d" height="%d" '
            'style="height:%smm" alt="Atra&ccedil;&otilde;es da II FENAGRO-MR">'
            % (IMG[nome], w, h, alt))


# luzes do fundo, no espirito da moldura de lampadas da marca
def luzes(pontos):
    return ",\n    ".join(
        "radial-gradient(circle %dmm at %s, rgba(227,180,90,%s) 0%%, "
        "rgba(227,180,90,0) 70%%)" % (r, pos, op) for pos, r, op in pontos)


LUZES_LATERAL = luzes([
    ("12% 6%", 70, ".25"), ("88% 13%", 58, ".21"), ("18% 21%", 52, ".19"),
    ("82% 30%", 74, ".23"), ("10% 39%", 60, ".20"), ("90% 47%", 54, ".19"),
    ("20% 56%", 68, ".22"), ("84% 64%", 58, ".20"), ("12% 73%", 62, ".21"),
    ("88% 81%", 70, ".22"), ("22% 90%", 54, ".19"), ("80% 96%", 60, ".20"),
])
LUZES_TESTEIRA = luzes([
    ("6% 20%", 60, ".23"), ("18% 78%", 48, ".20"), ("32% 26%", 56, ".21"),
    ("48% 80%", 50, ".20"), ("62% 22%", 58, ".22"), ("76% 76%", 46, ".19"),
    ("92% 30%", 62, ".23"),
])

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: #555;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40mm;
  padding: 40mm 0;
  font-family: "montserrat", sans-serif;
}

/* ---------- pecas ---------- */
.peca { position: relative; overflow: hidden; background: #01270E; }
.lateral { width: 600mm;  height: 5000mm; }
.testeira { width: 3200mm; height: 600mm; }

.luz { position: absolute; left: 0; top: 0; right: 0; bottom: 0; }
.lateral .luz { background-image: %(luzes_lat)s; }
.testeira .luz { background-image: %(luzes_tes)s; }

/* escurece as bordas e segura a leitura do texto */
.veu {
  position: absolute;
  left: 0; top: 0; right: 0; bottom: 0;
  background: radial-gradient(ellipse at center,
              rgba(1,39,14,0.14) 0%%, rgba(1,39,14,0.74) 100%%);
}

.moldura { position: absolute; border: 4mm solid #E3B45A; }
.lateral .moldura { left: 26mm; top: 26mm; right: 26mm; bottom: 26mm; }
.testeira .moldura { left: 22mm; top: 22mm; right: 22mm; bottom: 22mm; }

.area { position: absolute; display: flex; }
.lateral .area {
  left: 60mm; top: 60mm; right: 60mm; bottom: 60mm;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  text-align: center;
}
.testeira .area {
  left: 56mm; top: 46mm; right: 56mm; bottom: 46mm;
  align-items: center;
  justify-content: space-between;
}

/* ---------- tipografia ---------- */
.eyebrow { font-family: "montserrat", sans-serif; font-weight: 700; color: #E3B45A; }
.wordmark {
  font-family: "anton", sans-serif;
  color: #FBF7EB;
  line-height: 1;
  letter-spacing: 0.005em;
  text-shadow: 0 3mm 8mm rgba(0,0,0,0.45);
}
.tagline {
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  color: #E3B45A;
  line-height: 1.24;
}
.datao {
  font-family: "anton", sans-serif;
  color: #E3B45A;
  line-height: 1;
  letter-spacing: 0.02em;
  text-shadow: 0 3mm 8mm rgba(0,0,0,0.45);
}
.local { font-family: "montserrat", sans-serif; font-weight: 700; color: #FBF7EB; line-height: 1.35; }

/* ---------- testeira ---------- */
.t-logo { width: 450mm; height: 450mm; display: block; }
.t-centro { text-align: center; }
.t-centro .eyebrow { font-size: 24mm; letter-spacing: 0.42em; text-indent: 0.42em; }
.t-centro .wordmark { font-size: 142mm; margin-top: 12mm; }
.t-centro .tagline { font-size: 30mm; margin-top: 10mm; letter-spacing: 0.03em; }
.t-dir { text-align: center; }
.t-dir .datao { font-size: 116mm; }
.t-dir .sub {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 27mm;
  letter-spacing: 0.2em;
  text-indent: 0.2em;
  color: #FBF7EB;
  margin-top: 8mm;
}
.t-dir .local { font-size: 25mm; margin-top: 12mm; }
.t-selos { display: flex; align-items: center; gap: 26mm; }
.t-cav { width: 300mm; height: 177mm; display: block; }
.t-nin { width: 172mm; height: 188mm; display: block; }

/* ---------- laterais ---------- */
.l-logo { width: 470mm; height: 470mm; display: block; }
.l-word { font-size: 80mm; white-space: nowrap; margin-top: 22mm; }
.l-tag { font-size: 27mm; margin-top: 12mm; letter-spacing: 0.04em; }

.regua { width: 340mm; height: 3.2mm; background: #E3B45A; margin: 30mm auto; }

.sec {
  font-family: "anton", sans-serif;
  font-size: 92mm;
  line-height: 1.06;
  color: #FBF7EB;
  letter-spacing: 0.02em;
  text-shadow: 0 3mm 8mm rgba(0,0,0,0.45);
}
.sec-sub {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 26mm;
  letter-spacing: 0.28em;
  text-indent: 0.28em;
  color: #E3B45A;
  margin-top: 12mm;
}

/* mosaico das atracoes */
.mosaico { display: flex; flex-direction: column; gap: 6mm; margin: 30mm 0; }
.foto {
  width: 480mm;
  display: block;
  object-fit: cover;
  border: 2.4mm solid #E3B45A;
  border-radius: 8mm;
}

.sh { margin-top: 0; }
.sh-pill {
  display: inline-block;
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 28mm;
  letter-spacing: 0.1em;
  color: #01270E;
  background: #E3B45A;
  border-radius: 40mm;
  padding: 12mm 38mm;
}
.sh-pill span { font-weight: 700; color: #3A4A20; }
.sh-name {
  font-family: "anton", sans-serif;
  font-size: 76mm;
  line-height: 1.07;
  color: #FBF7EB;
  margin-top: 16mm;
  text-shadow: 0 2mm 6mm rgba(0,0,0,0.45);
}

.locutor {
  border-top: 2mm solid #3C6B4B;
  border-bottom: 2mm solid #3C6B4B;
  padding: 18mm 0;
  width: 100%%;
}
.locutor .lb {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 20mm;
  letter-spacing: 0.3em;
  text-indent: 0.3em;
  color: #E3B45A;
}
.locutor .nm {
  font-family: "anton", sans-serif;
  font-size: 62mm;
  line-height: 1.1;
  color: #FBF7EB;
  margin-top: 8mm;
}

.palestras { margin-top: 26mm; display: flex; flex-direction: column; gap: 18mm; }
.pa-dia {
  display: inline-block;
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 24mm;
  letter-spacing: 0.1em;
  color: #01270E;
  background: #E3B45A;
  border-radius: 40mm;
  padding: 8mm 28mm;
}
.pa-tema {
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 28mm;
  line-height: 1.24;
  color: #FBF7EB;
  margin-top: 9mm;
}

.destaques { display: flex; flex-direction: column; gap: 18mm; }
.dest {
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 27mm;
  letter-spacing: 0.12em;
  text-indent: 0.12em;
  color: #FBF7EB;
  border: 1.6mm solid #3C6B4B;
  border-radius: 30mm;
  white-space: nowrap;
  padding: 14mm 20mm;
}

.frase {
  font-family: "anton", sans-serif;
  font-size: 98mm;
  line-height: 1.1;
  color: #E3B45A;
  letter-spacing: 0.01em;
  text-shadow: 0 3mm 8mm rgba(0,0,0,0.45);
}

.l-datao { font-size: 132mm; white-space: nowrap; }
.l-datasub {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 36mm;
  letter-spacing: 0.24em;
  text-indent: 0.24em;
  color: #FBF7EB;
  margin-top: 10mm;
}
.l-local { font-size: 40mm; margin-top: 30mm; }
.l-local span { display: block; font-weight: 500; font-size: 32mm; color: #CFE0D2; }

.l-meio {
  flex: 1;
  width: 100%%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  padding: 30mm 0;
}

.l-selos { display: flex; align-items: flex-end; justify-content: center; gap: 30mm; }
.l-cav { width: 320mm; height: 189mm; display: block; }
.l-nin { width: 185mm; height: 202mm; display: block; }

.l-rodape { width: 100%%; }
.patroc {
  background: #FFFFFF;
  border-radius: 10mm;
  width: 100%%;
  padding: 22mm 18mm;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12mm;
}
.patroc .lbl {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 21mm;
  letter-spacing: 0.28em;
  text-indent: 0.28em;
  color: #4A5A4C;
}
.p-realiza { width: 380mm; height: 152mm; display: block; }
.p-apoio { width: 480mm; height: 47mm; display: block; }
.parceiros-row { display: flex; align-items: center; justify-content: center; gap: 26mm; }
.lg-coop { width: 170mm; height: 169mm; display: block; }
.lg-acai { width: 182mm; height: 156mm; display: block; }

.ig {
  margin-bottom: 40mm;
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 46mm;
  color: #E3B45A;
  letter-spacing: 0.04em;
}
"""

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>P&oacute;rtico II FENAGRO-MR</title>
<link rel="stylesheet" href="https://use.typekit.net/oia8csk.css">
<style>%(css)s</style>
</head>
<body>

<!-- ============ TESTEIRA 3,20 x 0,60 m ============ -->
<div class="peca testeira" id="testeira">
  <div class="luz"></div><div class="veu"></div><div class="moldura"></div>
  <div class="area">
    <img class="t-logo" src="%(logo)s" width="247" height="247" alt="FENAGRO-MR">
    <div class="t-centro">
      <div class="eyebrow">2&ordf; EDI&Ccedil;&Atilde;O</div>
      <div class="wordmark">II FENAGRO-MR</div>
      <div class="tagline">FEIRA DE NEG&Oacute;CIOS DO AGRO DE M&Atilde;E DO RIO</div>
    </div>
    <div class="t-dir">
      <div class="datao">17 A 20</div>
      <div class="sub">DE SETEMBRO</div>
      <div class="local">ESPA&Ccedil;O CUIA &middot; M&Atilde;E DO RIO / PA</div>
    </div>
    <div class="t-selos">
      <img class="t-cav" src="%(cav)s" width="242" height="143" alt="XXIII Cavalgada dos Arrojados">
      <img class="t-nin" src="%(nin)s" width="165" height="177" alt="Cia de Rodeio Ninho dos Bons">
    </div>
  </div>
</div>

<!-- ============ LATERAL ESQUERDA 0,60 x 5,00 m ============ -->
<div class="peca lateral" id="lateral-esq">
  <div class="luz"></div><div class="veu"></div><div class="moldura"></div>
  <div class="area">
    <div>
      <img class="l-logo" src="%(logo)s" width="247" height="247" alt="FENAGRO-MR">
      <div class="wordmark l-word">II FENAGRO-MR</div>
      <div class="tagline l-tag">FEIRA DE NEG&Oacute;CIOS DO AGRO<br>DE M&Atilde;E DO RIO</div>
    </div>
    <div class="l-meio">
      <div>
        <div class="regua"></div>
        <div class="sec">ATRA&Ccedil;&Otilde;ES<br>CONFIRMADAS</div>
        <div class="sec-sub">SHOWS TODAS AS NOITES</div>
        <div class="mosaico">%(mosaico)s</div>
      </div>
      %(shows)s
    </div>
    <div>
      <div class="locutor">
        <div class="lb">LOCUTOR</div>
        <div class="nm">JUNIOR MIL</div>
      </div>
      <div class="l-selos" style="margin-top:40mm">
        <img class="l-cav" src="%(cav)s" width="242" height="143" alt="XXIII Cavalgada dos Arrojados">
        <img class="l-nin" src="%(nin)s" width="165" height="177" alt="Cia de Rodeio Ninho dos Bons">
      </div>
    </div>
  </div>
</div>

<!-- ============ LATERAL DIREITA 0,60 x 5,00 m ============ -->
<div class="peca lateral" id="lateral-dir">
  <div class="luz"></div><div class="veu"></div><div class="moldura"></div>
  <div class="area">
    <div>
      <div class="datao l-datao">17 A 20</div>
      <div class="l-datasub">DE SETEMBRO</div>
      <div class="local l-local">ESPA&Ccedil;O CUIA<span>M&atilde;e do Rio / PA</span></div>
    </div>
    <div class="l-meio">
      <div>
        <div class="regua"></div>
        <div class="frase">O AGRO QUE<br>MOVIMENTA,<br>CONECTA E<br>TRANSFORMA!</div>
        <div class="regua"></div>
      </div>
      <div>
        <div class="sec" style="font-size:66mm">PALESTRAS</div>
        <div class="sec-sub">A PARTIR DAS 08H</div>
        <div class="palestras">%(palestras)s</div>
      </div>
      <div class="destaques">%(destaques)s</div>
    </div>
    <div class="l-rodape">
      <div class="ig">@fenagromr</div>
      <div class="patroc">
        <div class="lbl">REALIZA&Ccedil;&Atilde;O</div>
        <img class="p-realiza" src="%(realiza)s" width="188" height="80" alt="FENAGRO-MR e SIPRUMAR">
        <div class="lbl">APOIO</div>
        <img class="p-apoio" src="%(apoio)s" width="692" height="68" alt="Apoio">
        <div class="lbl">PARCEIROS DAS PALESTRAS</div>
        <div class="parceiros-row">
          <img class="lg-coop" src="%(coopagi)s" width="1134" height="1128" alt="COOPAGI">
          <img class="lg-acai" src="%(acaitech)s" width="1162" height="996" alt="A&ccedil;a&iacute;Tech">
        </div>
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""

html = HTML % {
    "css": CSS % {"luzes_lat": LUZES_LATERAL, "luzes_tes": LUZES_TESTEIRA},
    "logo": IMG["logo_circ.png"],
    "cav": IMG["cavalgada.png"],
    "nin": IMG["ninho.png"],
    "realiza": IMG["spons_realiza.png"],
    "apoio": IMG["spons_apoio.png"],
    "coopagi": IMG["coopagi.png"],
    "acaitech": IMG["acaitech.png"],
    "mosaico": "".join(bloco_foto(*m) for m in MOSAICO),
    "shows": "".join(bloco_show(*s) for s in SHOWS),
    "palestras": "".join(bloco_palestra(*p) for p in PALESTRAS),
    "destaques": "".join('<div class="dest">%s</div>' % d for d in DESTAQUES),
}

OUT.write_text(html, encoding="utf-8")
print("%s  (%.0f KB)" % (OUT, OUT.stat().st_size / 1024))
