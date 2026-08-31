#!/usr/bin/env python3
"""Gera as tres pecas do portico de entrada da II FENAGRO-MR.

Medidas reais:
  - laterais (2x): 0,60 m de largura x 5,00 m de altura
  - testeira:      3,20 m de largura x 0,60 m de altura

O CSS usa milimetros em tamanho real; a resolucao final e definida na
renderizacao. Os recortes graficos vem de ../assets.
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
    "spons_realiza.png", "spons_apoio.png",
    "coopagi.png", "acaitech.png",
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
             "PALESTRAS", "PRA&Ccedil;A DE ALIMENTA&Ccedil;&Atilde;O"]


def bloco_show(dia, semana, nomes):
    linhas = "".join('<div class="sh-name">%s</div>' % n for n in nomes)
    return ('<div class="sh">'
            '<div class="sh-pill">%s <span>&middot; %s</span></div>'
            '<div class="sh-list">%s</div></div>' % (dia, semana, linhas))


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

/* moldura dourada interna */
.moldura {
  position: absolute;
  border: 4mm solid #E3B45A;
}
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
.eyebrow {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  color: #E3B45A;
}
.wordmark {
  font-family: "anton", sans-serif;
  color: #FBF7EB;
  line-height: 1;
  letter-spacing: 0.005em;
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
}
.local {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  color: #FBF7EB;
  line-height: 1.35;
}

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

.regua {
  width: 340mm;
  height: 3.2mm;
  background: #E3B45A;
  margin: 34mm auto;
}

.sec {
  font-family: "anton", sans-serif;
  font-size: 92mm;
  line-height: 1.06;
  color: #FBF7EB;
  letter-spacing: 0.02em;
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

.l-meio {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  padding: 40mm 0;
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
}

.destaques { display: flex; flex-direction: column; gap: 20mm; }
.dest {
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 27mm;
  letter-spacing: 0.12em;
  text-indent: 0.12em;
  color: #FBF7EB;
  border: 1.6mm solid #3C6B4B;
  white-space: nowrap;
  border-radius: 30mm;
  padding: 14mm 20mm;
}

.frase {
  font-family: "anton", sans-serif;
  font-size: 98mm;
  line-height: 1.1;
  color: #E3B45A;
  letter-spacing: 0.01em;
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

.l-selos { display: flex; align-items: flex-end; justify-content: center; gap: 30mm; }
.l-cav { width: 320mm; height: 189mm; display: block; }
.l-nin { width: 185mm; height: 202mm; display: block; }

.patroc {
  background: #FFFFFF;
  border-radius: 10mm;
  width: 100%;
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

.l-rodape { width: 100%; }
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
<meta name="hz:slide-selector" content=".peca">
<link rel="stylesheet" href="https://use.typekit.net/oia8csk.css">
<style>%(css)s</style>
</head>
<body>

<!-- ============ TESTEIRA 3,20 x 0,60 m ============ -->
<div class="peca testeira" id="testeira" data-canvas-width="12094" data-canvas-height="2268">
  <div class="moldura"></div>
  <div class="area">
    <img class="t-logo" src="%(logo)s" width="210" height="210" alt="FENAGRO-MR">
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
      <img class="t-cav" src="%(cav)s" width="200" height="118" alt="XXIII Cavalgada dos Arrojados">
      <img class="t-nin" src="%(nin)s" width="130" height="142" alt="Cia de Rodeio Ninho dos Bons">
    </div>
  </div>
</div>

<!-- ============ LATERAL ESQUERDA 0,60 x 5,00 m ============ -->
<div class="peca lateral" id="lateral-esq" data-canvas-width="2268" data-canvas-height="18898">
  <div class="moldura"></div>
  <div class="area">
    <div>
      <img class="l-logo" src="%(logo)s" width="210" height="210" alt="FENAGRO-MR">
      <div class="wordmark l-word">II FENAGRO-MR</div>
      <div class="tagline l-tag">FEIRA DE NEG&Oacute;CIOS DO AGRO<br>DE M&Atilde;E DO RIO</div>
    </div>
    <div class="l-meio">
      <div>
        <div class="regua"></div>
        <div class="sec">ATRA&Ccedil;&Otilde;ES<br>CONFIRMADAS</div>
        <div class="sec-sub">SHOWS TODAS AS NOITES</div>
      </div>
      %(shows)s
    </div>
    <div class="l-selos">
      <img class="l-cav" src="%(cav)s" width="200" height="118" alt="XXIII Cavalgada dos Arrojados">
      <img class="l-nin" src="%(nin)s" width="130" height="142" alt="Cia de Rodeio Ninho dos Bons">
    </div>
  </div>
</div>

<!-- ============ LATERAL DIREITA 0,60 x 5,00 m ============ -->
<div class="peca lateral" id="lateral-dir" data-canvas-width="2268" data-canvas-height="18898">
  <div class="moldura"></div>
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
      <div class="destaques">%(destaques)s</div>
    </div>
    <div class="l-rodape">
    <div class="ig">@fenagromr</div>
    <div class="patroc">
      <div class="lbl">REALIZA&Ccedil;&Atilde;O</div>
      <img class="p-realiza" src="%(realiza)s" width="150" height="60" alt="FENAGRO-MR e SIPRUMAR">
      <div class="lbl">APOIO</div>
      <img class="p-apoio" src="%(apoio)s" width="470" height="46" alt="Apoio">
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
    "css": CSS,
    "logo": IMG["logo_circ.png"],
    "cav": IMG["cavalgada.png"],
    "nin": IMG["ninho.png"],
    "realiza": IMG["spons_realiza.png"],
    "apoio": IMG["spons_apoio.png"],
    "coopagi": IMG["coopagi.png"],
    "acaitech": IMG["acaitech.png"],
    "shows": "".join(bloco_show(*s) for s in SHOWS),
    "destaques": "".join('<div class="dest">%s</div>' % d for d in DESTAQUES),
}

OUT.write_text(html, encoding="utf-8")
print("%s  (%.0f KB)" % (OUT, OUT.stat().st_size / 1024))
