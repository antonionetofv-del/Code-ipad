#!/usr/bin/env python3
"""Gera o folder dobravel (3 dobras, frente e verso) da II FENAGRO-MR.

Os recortes graficos (logo, badge da Cavalgada, faixas de atracoes, logos de
patrocinio, foto da equipe) sao embutidos em base64 para que o HTML seja
autocontido e possa ser importado direto no Adobe Express.
"""
import base64
import pathlib

ASSETS = pathlib.Path(__file__).parent / "assets"
OUT = pathlib.Path(__file__).parent / "folder-fenagro.html"

MIME = {".png": "image/png", ".jpg": "image/jpeg"}


def data_uri(name):
    p = ASSETS / name
    return "data:%s;base64,%s" % (
        MIME[p.suffix],
        base64.b64encode(p.read_bytes()).decode("ascii"),
    )


IMG = {
    n: data_uri(n)
    for n in (
        "logo_circ.png",
        "cavalgada.png",
        "spons_realiza.jpg",
        "coopagi.png",
        "acaitech.png",
        "spons_apoio.jpg",
        "orn_tractor.jpg",
        "orn_rider.png",
        "ninho.png",
    )
}

# ---------------------------------------------------------------- conteudo ---

PROGRAMACAO = [
    ("17/09", "QUINTA-FEIRA", [
        ("08:00", "Abertura Oficial da Feira",
         "Palavra do Presidente do Sindicato e das autoridades de M&atilde;e do Rio"),
        ("08:00", "Palestra", "Cacau: enxertia, poda e nutri&ccedil;&atilde;o"),
        ("14:00", "Neg&oacute;cios e Expositores", "Visita&ccedil;&atilde;o aos estandes"),
        ("18:00", "Abertura Oficial do Rodeio", ""),
        ("20:00", "Shows", "Isa&iacute;as Show &middot; DJ Remix nos intervalos"),
    ]),
    ("18/09", "SEXTA-FEIRA", [
        ("08:00", "Abertura da Feira", ""),
        ("08:00", "Palestra", "A&ccedil;a&iacute; irrigado: efici&ecirc;ncia e lucratividade"),
        ("09:00", "Palestra", "Desafios de produzir a&ccedil;a&iacute; em terra firme"),
        ("14:00", "Neg&oacute;cios e Expositores", "Visita&ccedil;&atilde;o aos estandes"),
        ("18:00", "Rodeio", ""),
        ("20:00", "Shows", "Leozinho Forrozeiro &middot; Jo&atilde;o Nunes &middot; DJ Remix nos intervalos"),
    ]),
    ("19/09", "S&Aacute;BADO", [
        ("08:00", "Abertura da Feira", ""),
        ("08:00", "Ciclo de Palestras",
         "Piscicultura, Bovino de Corte, Bovino de Leite e Adepar&aacute;"),
        ("14:00", "Neg&oacute;cios e Expositores", "Visita&ccedil;&atilde;o aos estandes"),
        ("18:00", "Rodeio", ""),
        ("20:00", "Shows", "Xerife Bar&atilde;o &middot; Gleyk &amp; Gleyson &middot; DJ Remix nos intervalos"),
    ]),
    ("20/09", "DOMINGO", [
        ("08:00", "XXIII Cavalgada dos Arrojados", "Concentra&ccedil;&atilde;o e sa&iacute;da"),
        ("12:00", "Almo&ccedil;o dos Cavaleiros", ""),
        ("14:00", "Entrega das Premia&ccedil;&otilde;es", ""),
        ("19:00", "Encerramento do Rodeio", ""),
        ("20:00", "Encerramento Oficial da Feira", ""),
        ("20:30", "Shows", "Ant&ocirc;nio Marcos &middot; Gleyk &amp; Gleyson &middot; Evandro do Acordeon "
                           "&middot; Marquinhos Par&aacute; &middot; Deyse Bandeira &middot; DJ Remix nos intervalos"),
        ("21:00", "Desfile da Garota FENAGRO", "Passagem da faixa"),
    ]),
]

PALESTRAS = [
    ("17/09", "QUINTA-FEIRA", [
        ("08:00", "CACAU", "Enxertia, poda e nutri&ccedil;&atilde;o no cacau",
         "Adailton Mendes", "T&eacute;cnico em Agropecu&aacute;ria"),
    ]),
    ("18/09", "SEXTA-FEIRA", [
        ("08:00", "A&Ccedil;A&Iacute;",
         "A&ccedil;a&iacute; irrigado: como produzir com efici&ecirc;ncia e lucratividade",
         "Arcidio Ornela Filho", "Especialista na Cultura do A&ccedil;a&iacute;"),
        ("09:00", "A&Ccedil;A&Iacute;", "Desafios de produzir a&ccedil;a&iacute; em terra firme",
         "Emerson Silva de Menezes", "Presidente da COOPAGI"),
    ]),
    ("19/09", "S&Aacute;BADO", [
        ("08:00", "PISCICULTURA", "", "Eryca Maria de Jesus Vieira",
         "T&eacute;cnica em Aquicultura &middot; Secret&aacute;ria Municipal de Agricultura "
         "e Desenvolvimento Econ&ocirc;mico de M&atilde;e do Rio"),
        ("09:00", "BOVINO DE CORTE", "Efici&ecirc;ncia de pastagem",
         "Wemelly Menezes de Oliveira", "Zootecnista"),
        ("10:00", "BOVINO DE LEITE", "", "Tomaz Pina Maia", "M&eacute;dico Veterin&aacute;rio"),
        ("11:00", "ADEPAR&Aacute;", "", "", ""),
    ]),
]

ATRACOES = [
    ("17/09", "QUINTA", ["Isa&iacute;as Show"]),
    ("18/09", "SEXTA", ["Leozinho Forrozeiro", "Jo&atilde;o Nunes"]),
    ("19/09", "S&Aacute;BADO", ["Xerife Bar&atilde;o", "Gleyk &amp; Gleyson"]),
    ("20/09", "DOMINGO", ["Ant&ocirc;nio Marcos", "Gleyk &amp; Gleyson",
                                "Evandro do Acordeon", "Marquinhos Par&aacute;",
                                "Deyse Bandeira"]),
]

DESTAQUES = [
    "Shows", "Rodeio", "XXIII Cavalgada", "Parque de Divers&atilde;o",
    "Palestras", "Pra&ccedil;a de Alimenta&ccedil;&atilde;o", "Neg&oacute;cios e muito mais!",
]

# ----------------------------------------------------------------- helpers ---


def dia_bloco(dia, semana, itens):
    linhas = []
    for hora, titulo, sub in itens:
        sub_html = '<span class="row-sub">%s</span>' % sub if sub else ""
        linhas.append(
            '<div class="row"><span class="row-time">%s</span>'
            '<span class="row-body"><span class="row-title">%s</span>%s</span></div>'
            % (hora, titulo, sub_html)
        )
    return (
        '<div class="day">'
        '<div class="day-pill"><span class="day-date">%s</span>'
        '<span class="day-week">%s</span></div>%s</div>'
        % (dia, semana, "".join(linhas))
    )


def palestra_bloco(dia, semana, itens):
    linhas = []
    for hora, palestra, tema, quem, formacao in itens:
        corpo = ['<span class="talk-title">%s</span>' % palestra]
        if tema:
            corpo.append('<span class="talk-theme">%s</span>' % tema)
        if quem:
            credito = "%s &middot; %s" % (quem, formacao) if formacao else quem
            corpo.append('<span class="talk-who">%s</span>' % credito)
        linhas.append(
            '<div class="talk"><span class="talk-time">%s</span>'
            '<span class="talk-body">%s</span></div>' % (hora, "".join(corpo))
        )
    return (
        '<div class="talk-day">'
        '<div class="day-pill"><span class="day-date">%s</span>'
        '<span class="day-week">%s</span></div>%s</div>'
        % (dia, semana, "".join(linhas))
    )


def atracao_bloco(dia, semana, nomes):
    linhas = "".join('<div class="act-name">%s</div>' % n for n in nomes)
    return (
        '<div class="act">'
        '<div class="act-pill">%s <span>&middot; %s</span></div>'
        '<div class="act-list">%s<div class="act-tag">DJ REMIX NOS INTERVALOS</div></div>'
        "</div>" % (dia, semana, linhas)
    )


IG_SVG = (
    '<svg class="ig" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">'
    '<rect x="2.5" y="2.5" width="19" height="19" rx="5.5" fill="none" '
    'stroke="#E3B45A" stroke-width="2"/>'
    '<circle cx="12" cy="12" r="4.6" fill="none" stroke="#E3B45A" stroke-width="2"/>'
    '<circle cx="17.6" cy="6.4" r="1.5" fill="#E3B45A"/></svg>'
)

ORNAMENTO = (
    '<svg class="orn-rule" viewBox="0 0 200 8" width="200" height="8" '
    'preserveAspectRatio="none" aria-hidden="true">'
    '<line x1="0" y1="4" x2="80" y2="4" stroke="#E3B45A" stroke-width="1"/>'
    '<polygon points="100,0 106,4 100,8 94,4" fill="#E3B45A"/>'
    '<line x1="120" y1="4" x2="200" y2="4" stroke="#E3B45A" stroke-width="1"/></svg>'
)

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: #6a6a6a;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12mm;
  padding: 12mm 0;
  font-family: "montserrat", sans-serif;
}

.panel {
  position: relative;
  width: 303mm;
  height: 216mm;
  overflow: hidden;
  background: #FBF7EB;
}

/* --- colunas (paineis de dobra) --- */
.col { position: absolute; top: 0; height: 216mm; overflow: hidden; }
.col-a { left: 0mm;   width: 100mm; }
.col-b { left: 100mm; width: 100mm; }
.col-c { left: 200mm; width: 103mm; }
.in-a  { left: 0mm;   width: 103mm; }
.in-b  { left: 103mm; width: 100mm; }
.in-c  { left: 203mm; width: 100mm; }

.dark  { background: #01270E; }
.cream { background: #FBF7EB; }

.pad {
  height: 216mm;
  padding: 9mm 8mm;
  display: flex;
  flex-direction: column;
}
.pad > * { flex-shrink: 0; }

/* ---------------- capa ---------------- */
.cover { align-items: center; text-align: center; justify-content: space-between; }

.eyebrow {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 2.9mm;
  letter-spacing: 0.42em;
  color: #E3B45A;
  text-indent: 0.42em;
}

.cover-logo { width: 42mm; height: 42mm; display: block; }

.wordmark {
  font-family: "anton", sans-serif;
  font-weight: 400;
  font-size: 13.4mm;
  line-height: 1.02;
  color: #FBF7EB;
  letter-spacing: 0.005em;
}

.tagline {
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 4.1mm;
  line-height: 1.28;
  letter-spacing: 0.03em;
  color: #E3B45A;
}

.place-rule {
  display: flex;
  align-items: center;
  gap: 3mm;
  font-family: "montserrat", sans-serif;
  font-weight: 600;
  font-size: 2.7mm;
  letter-spacing: 0.3em;
  color: #FBF7EB;
  text-indent: 0.3em;
}
.place-rule::before, .place-rule::after {
  content: "";
  display: block;
  width: 14mm;
  height: 0.4mm;
  background: #E3B45A;
}

.date-big {
  font-family: "anton", sans-serif;
  font-weight: 400;
  font-size: 16mm;
  line-height: 1;
  color: #E3B45A;
  letter-spacing: 0.02em;
}
.date-sub {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 4.4mm;
  letter-spacing: 0.24em;
  color: #FBF7EB;
  text-indent: 0.24em;
  margin-top: 1.5mm;
}
.venue {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 4mm;
  line-height: 1.4;
  color: #FBF7EB;
  margin-top: 5mm;
}
.venue span { display: block; font-weight: 500; font-size: 3.4mm; color: #CFE0D2; }

.seals { display: flex; align-items: flex-end; justify-content: center; gap: 6mm; }
.seal-cav { width: 40mm; height: 23.6mm; display: block; }
.seal-nin { width: 23mm; height: 25.2mm; display: block; }

/* ---------------- contracapa ---------------- */
.back { justify-content: space-between; align-items: center; text-align: center; }

.claim {
  font-family: "anton", sans-serif;
  font-weight: 400;
  font-size: 8.4mm;
  line-height: 1.08;
  color: #E3B45A;
  letter-spacing: 0.01em;
}

.lede {
  font-family: "montserrat", sans-serif;
  font-weight: 400;
  font-size: 3.1mm;
  line-height: 1.62;
  color: #E4EDE5;
}

.kicker {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 2.6mm;
  letter-spacing: 0.3em;
  color: #E3B45A;
  text-indent: 0.3em;
  margin-bottom: 3mm;
}

.tags { display: flex; flex-wrap: wrap; justify-content: center; gap: 1.6mm 2mm; }
.tag {
  font-family: "montserrat", sans-serif;
  font-weight: 600;
  font-size: 2.85mm;
  line-height: 1;
  color: #FBF7EB;
  border: 0.3mm solid #3C6B4B;
  border-radius: 6mm;
  padding: 1.6mm 2.6mm;
}

.when {
  border-top: 0.4mm solid #3C6B4B;
  border-bottom: 0.4mm solid #3C6B4B;
  padding: 4mm 0;
  width: 100%;
}
.when-date {
  font-family: "anton", sans-serif;
  font-size: 7.6mm;
  line-height: 1.05;
  color: #E3B45A;
  letter-spacing: 0.02em;
}
.when-place {
  font-family: "montserrat", sans-serif;
  font-weight: 600;
  font-size: 3.1mm;
  line-height: 1.45;
  color: #FBF7EB;
  margin-top: 1.6mm;
}

.social {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2.2mm;
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 4.2mm;
  color: #E3B45A;
}
.ig { width: 4.6mm; height: 4.6mm; display: block; }

.sponsors {
  background: #FFFFFF;
  border-radius: 2mm;
  width: 100%;
  padding: 3.4mm 3mm;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.6mm;
}
.sponsors .lbl {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 2.1mm;
  letter-spacing: 0.28em;
  color: #4A5A4C;
  text-indent: 0.28em;
}
.sp-realiza { width: 42mm; height: 16.8mm; display: block; }
.sp-apoio { width: 76mm; height: 7.5mm; display: block; }

/* ---------------- atracoes ---------------- */
.acts { gap: 3mm; }
.acts-head { text-align: center; }
.sec-title {
  font-family: "anton", sans-serif;
  font-size: 7.8mm;
  line-height: 1.05;
  color: #01270E;
  letter-spacing: 0.01em;
}
.sec-sub {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 2.5mm;
  letter-spacing: 0.26em;
  color: #14713A;
  text-indent: 0.26em;
  margin-top: 1.6mm;
}

.act { display: flex; flex-direction: column; align-items: center; gap: 1.2mm; }
.acts { justify-content: space-between; }
.act-pill {
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 2.9mm;
  letter-spacing: 0.08em;
  color: #FBF7EB;
  background: #14713A;
  border-radius: 5mm;
  padding: 1.2mm 5mm;
}
.act-pill span { font-weight: 600; color: #BFE0C8; }
.act-list { text-align: center; }
.act-name {
  font-family: "anton", sans-serif;
  font-size: 5.6mm;
  line-height: 1.16;
  color: #01270E;
  letter-spacing: 0.01em;
  margin-top: 2.4mm;
}
.act-tag {
  display: block;
  margin-top: 1.6mm;
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 2.2mm;
  letter-spacing: 0.26em;
  color: #C08A1E;
  text-indent: 0.26em;
  margin-top: 0.6mm;
}

/* ---------------- programacao ---------------- */
.band, .hero {
  background: #01270E;
  flex: none;
  height: 25mm;
  margin: -9mm -8mm 6mm -8mm;
  padding: 0 8mm;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}
.band-title {
  font-family: "anton", sans-serif;
  font-size: 7.4mm;
  line-height: 1.05;
  color: #FBF7EB;
  letter-spacing: 0.05em;
}
.band-sub {
  font-family: "montserrat", sans-serif;
  font-weight: 600;
  font-size: 2.4mm;
  letter-spacing: 0.26em;
  color: #E3B45A;
  text-indent: 0.26em;
  margin-top: 1.4mm;
}

.day { margin-bottom: 3.5mm; }
.day-pill {
  background: #14713A;
  border-radius: 5mm;
  padding: 1.8mm 4mm;
  margin-bottom: 2.2mm;
  display: flex;
  align-items: baseline;
  gap: 2.2mm;
}
.day-date {
  font-family: "anton", sans-serif;
  font-size: 4.6mm;
  color: #FBF7EB;
  letter-spacing: 0.02em;
}
.day-week {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 2.6mm;
  letter-spacing: 0.2em;
  color: #C6E4CF;
  text-indent: 0.2em;
}

.row {
  display: flex;
  gap: 3mm;
  padding: 1mm 0;
  border-bottom: 0.25mm solid #E2DCC4;
}
.row:last-child { border-bottom: 0; }
.row-time {
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 3.1mm;
  line-height: 1.3;
  color: #14713A;
  width: 13mm;
  flex: 0 0 13mm;
}
.row-body { display: block; }
.row-title {
  display: block;
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 3.1mm;
  line-height: 1.3;
  color: #14301B;
}
.row-sub {
  display: block;
  font-family: "montserrat", sans-serif;
  font-weight: 500;
  font-size: 2.6mm;
  line-height: 1.34;
  color: #5B6A5D;
  margin-top: 0.4mm;
}

.orn { margin-top: auto; padding-top: 2mm; text-align: center; }
.orn img { display: block; margin: 0 auto 2.5mm auto; }
.orn-tractor { width: 32mm; height: 13.3mm; }
.orn-rider { width: 17mm; height: 13.7mm; }
.orn-text {
  font-family: "anton", sans-serif;
  font-size: 4.6mm;
  line-height: 1.18;
  color: #14713A;
  letter-spacing: 0.02em;
}

/* ---------------- palestras ---------------- */
.hero-eyebrow {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 2.4mm;
  letter-spacing: 0.3em;
  color: #E3B45A;
  text-indent: 0.3em;
}
.hero-title {
  font-family: "anton", sans-serif;
  font-size: 6.4mm;
  line-height: 1.06;
  color: #FBF7EB;
  letter-spacing: 0.02em;
  margin-top: 1.4mm;
}

.talks { padding-top: 0; }
.talk-day { margin-bottom: 2.4mm; }
.talk {
  display: flex;
  gap: 3mm;
  padding: 1.1mm 0;
  border-bottom: 0.25mm solid #E2DCC4;
}
.talk:last-child { border-bottom: 0; }
.talk-time {
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 3.1mm;
  line-height: 1.3;
  color: #14713A;
  width: 13mm;
  flex: 0 0 13mm;
}
.talk-body { display: block; }
.talk-title {
  display: block;
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 3mm;
  line-height: 1.24;
  color: #14301B;
  letter-spacing: 0.01em;
}
.talk-theme {
  display: block;
  font-family: "montserrat", sans-serif;
  font-weight: 500;
  font-size: 2.5mm;
  line-height: 1.3;
  color: #5B6A5D;
  margin-top: 0.5mm;
}
.talk-who {
  display: block;
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 2.5mm;
  line-height: 1.3;
  color: #C08A1E;
  margin-top: 0.6mm;
}

.parceiros {
  margin-top: auto;
  padding-top: 3mm;
  text-align: center;
}
  /* rotulo dos parceiros */
.parceiros .lbl {
  font-family: "montserrat", sans-serif;
  font-weight: 700;
  font-size: 2.2mm;
  letter-spacing: 0.28em;
  text-indent: 0.28em;
  color: #14713A;
  margin-bottom: 3mm;
}
.parceiros-row { display: flex; align-items: center; justify-content: center; gap: 8mm; }
.lg-coopagi { width: 29mm; height: 28.8mm; display: block; }
.lg-acaitech { width: 31mm; height: 26.6mm; display: block; }

.orn-rule { width: 30mm; height: 1.2mm; display: block; margin: 3.5mm auto; }
"""

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Folder II FENAGRO-MR</title>
<meta name="hz:slide-selector" content=".panel">
<meta name="hz:canvas-width" content="1145">
<meta name="hz:canvas-height" content="816">
<link rel="stylesheet" href="https://use.typekit.net/oia8csk.css">
<style>%(css)s</style>
</head>
<body>

<!-- ============ FACE EXTERNA: atracoes | contracapa | capa ============ -->
<div class="panel" data-canvas-width="1145" data-canvas-height="816">

  <!-- painel que dobra para dentro -->
  <div class="col col-a cream">
    <div class="pad acts">
      <div class="acts-head">
        <div class="sec-title">ATRA&Ccedil;&Otilde;ES<br>CONFIRMADAS</div>
        <div class="sec-sub">SHOWS TODAS AS NOITES</div>
      </div>
      %(atracoes)s
    </div>
  </div>

  <!-- contracapa -->
  <div class="col col-b dark">
    <div class="pad back">
      <div class="claim">O AGRO QUE<br>MOVIMENTA, CONECTA<br>E TRANSFORMA!</div>
      <p class="lede">Venha viver experi&ecirc;ncias, fazer novos contatos,
        conhecer tecnologias e fortalecer o agroneg&oacute;cio da nossa regi&atilde;o.</p>
      <div>
        <div class="kicker">O QUE VOC&Ecirc; ENCONTRA</div>
        <div class="tags">%(tags)s</div>
      </div>
      <div class="when">
        <div class="when-date">17 A 20 DE SETEMBRO</div>
        <div class="when-place">Espa&ccedil;o Cuia<br>M&atilde;e do Rio / PA</div>
      </div>
      <div class="social">%(ig)s @fenagromr</div>
      <div class="sponsors">
        <div class="lbl">REALIZA&Ccedil;&Atilde;O</div>
        <img class="sp-realiza" src="%(realiza)s" width="150" height="60" alt="FENAGRO-MR e SIPRUMAR">
        <div class="lbl">APOIO</div>
        <img class="sp-apoio" src="%(apoio)s" width="470" height="46" alt="Apoio">
      </div>
    </div>
  </div>

  <!-- capa -->
  <div class="col col-c dark">
    <div class="pad cover">
      <div class="eyebrow">2&ordf; EDI&Ccedil;&Atilde;O</div>
      <img class="cover-logo" src="%(logo)s" width="200" height="200" alt="FENAGRO-MR">
      <div>
        <div class="wordmark">II FENAGRO-MR</div>
        <div class="tagline">FEIRA DE NEG&Oacute;CIOS<br>DO AGRO DE M&Atilde;E DO RIO</div>
      </div>
      <div class="place-rule">M&Atilde;E DO RIO - PA</div>
      <div>
        <div class="date-big">17 A 20</div>
        <div class="date-sub">DE SETEMBRO</div>
        <div class="venue">ESPA&Ccedil;O CUIA<span>M&atilde;e do Rio / PA</span></div>
      </div>
      <div class="seals">
        <img class="seal-cav" src="%(badge)s" width="200" height="118" alt="XXIII Cavalgada dos Arrojados">
        <img class="seal-nin" src="%(ninho)s" width="130" height="142" alt="Cia de Rodeio Ninho dos Bons">
      </div>
    </div>
  </div>
</div>

<!-- ============ FACE INTERNA: 17-18 | 19-20 | palestras ============ -->
<div class="panel" data-canvas-width="1145" data-canvas-height="816">

  <div class="col in-a cream">
    <div class="pad">
      <div class="band">
        <div class="band-title">PROGRAMA&Ccedil;&Atilde;O OFICIAL</div>
        <div class="band-sub">II FENAGRO-MR &middot; 2026</div>
      </div>
      %(dia1)s
      %(dia2)s
      <div class="orn">
        <img class="orn-tractor" src="%(tractor)s" width="120" height="50" alt="">
        <div class="orn-text">4 DIAS DE MUITOS NEG&Oacute;CIOS,<br>TRADI&Ccedil;&Atilde;O E DIVERS&Atilde;O!</div>
      </div>
    </div>
  </div>

  <div class="col in-b cream">
    <div class="pad">
      <div class="band">
        <div class="band-title">PROGRAMA&Ccedil;&Atilde;O OFICIAL</div>
        <div class="band-sub">ESPA&Ccedil;O CUIA &middot; M&Atilde;E DO RIO / PA</div>
      </div>
      %(dia3)s
      %(dia4)s
      <div class="orn">
        <img class="orn-rider" src="%(rider)s" width="100" height="80" alt="">
        <div class="orn-text">XXIII CAVALGADA<br>DOS ARROJADOS</div>
      </div>
    </div>
  </div>

  <div class="col in-c cream">
    <div class="pad">
      <div class="hero">
        <div class="hero-eyebrow">2&ordf; FENAGRO-MR</div>
        <div class="hero-title">CRONOGRAMA<br>DE PALESTRAS</div>
      </div>
      <div class="talks">%(palestras)s</div>
      <div class="parceiros">
        <div class="lbl">PARCEIROS DAS PALESTRAS</div>
        <div class="parceiros-row">
          <img class="lg-coopagi" src="%(coopagi)s" width="210" height="209" alt="COOPAGI">
          <img class="lg-acaitech" src="%(acaitech)s" width="210" height="181" alt="A&ccedil;a&iacute;Tech">
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
    "badge": IMG["cavalgada.png"],
    "realiza": IMG["spons_realiza.jpg"],
    "ninho": IMG["ninho.png"],
    "apoio": IMG["spons_apoio.jpg"],
    "tractor": IMG["orn_tractor.jpg"],
    "rider": IMG["orn_rider.png"],
    "ig": IG_SVG,
    "rule": ORNAMENTO,
    "coopagi": IMG["coopagi.png"],
    "acaitech": IMG["acaitech.png"],
    "tags": "".join('<span class="tag">%s</span>' % t for t in DESTAQUES),
    "atracoes": "".join(atracao_bloco(*a) for a in ATRACOES),
    "dia1": dia_bloco(*PROGRAMACAO[0]),
    "dia2": dia_bloco(*PROGRAMACAO[1]),
    "dia3": dia_bloco(*PROGRAMACAO[2]),
    "dia4": dia_bloco(*PROGRAMACAO[3]),
    "palestras": "".join(palestra_bloco(*p) for p in PALESTRAS),
}

OUT.write_text(html, encoding="utf-8")
print("%s  (%.0f KB)" % (OUT, OUT.stat().st_size / 1024))
