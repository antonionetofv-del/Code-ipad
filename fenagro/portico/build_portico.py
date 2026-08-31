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
import io
import pathlib
import sys

from PIL import Image

BASE = pathlib.Path(__file__).parent
ASSETS = BASE / "assets_hi"
REC = BASE / "recebidos"
OUT = BASE / "portico-fenagro.html"

MIME = {".png": "image/png", ".jpg": "image/jpeg"}


# A versao para o Adobe Express reduz cada imagem ao dobro do tamanho em que ela
# aparece na peca. O arquivo de impressao continua saindo do HTML normal.
EXPRESS = "--express" in sys.argv
MM_PX = 96 / 25.4

# maior lado de cada logo, em mm, como aparece nas pecas
LADO_MM = {"logo-fenagro-mr": 470, "logo-cavalgada-arrojados": 330,
           "logo-ninho-dos-bons": 213}
FOLGA_EXPRESS = 1.25     # folga sobre o tamanho de exibicao das logos


def data_uri(p, lado_mm=None):
    dados = p.read_bytes()
    sufixo = p.suffix
    if EXPRESS and lado_mm:
        limite = round(lado_mm * MM_PX * FOLGA_EXPRESS)
        with Image.open(p) as im:
            if max(im.size) > limite:
                f = limite / max(im.size)
                im = im.resize((max(1, round(im.width * f)),
                                max(1, round(im.height * f))), Image.LANCZOS)
                buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
                dados = buf.getvalue()
    return "data:%s;base64,%s" % (MIME[sufixo], base64.b64encode(dados).decode())



# nomes por dia, como na arte oficial: sem legenda em cada rosto
SHOWS = [
    ("17/09", "", ["ISAIAS SHOW", "DJ REMIX"]),
    ("18/09", "", ["LEOZINHO FORROZEIRO", "JOAO NUNES", "DJ REMIX"]),
    ("19/09", "", ["XERIFE BAR&Atilde;O", "THIAGO ARA&Uacute;JO", "DJ REMIX"]),
    ("20/09", "CAVALGADA DOS ARROJADOS",
     ["ANT&Ocirc;NIO MARCOS", "EVANDRO DO ACORDEON", "MARQUINHOS PAR&Aacute;",
      "GLEYK &amp; GLEYSON", "DEYSE BANDEIRA", "LOCUTOR JUNIOR MIL", "DJ REMIX"]),
]

DESTAQUES = ["SHOWS", "RODEIO", "XXIII CAVALGADA", "PARQUE DE DIVERS&Atilde;O",
             "EXPOSITORES", "PRA&Ccedil;A DE ALIMENTA&Ccedil;&Atilde;O", "E MUITO MAIS!"]

PALESTRAS = [
    ("17/09", ["CACAU"]),
    ("18/09", ["A&Ccedil;A&Iacute;"]),
    ("19/09", ["PISCICULTURA", "BOVINOCULTURA DE CORTE",
               "BOVINO DE LEITE", "ADEPAR&Aacute;"]),
]

# (chave, altura em mm) -- a largura sai da proporcao real do arquivo
REALIZACAO = [("logo-fenagro-mr", 112), ("logo-siprumar", 112)]
APOIO = [
    [("logo-faepa", 62), ("logo-sebrae", 46), ("logo-banpara", 33)],
    [("logo-prefeitura-mae-do-rio", 31), ("logo-governo-para", 86),
     ("logo-amazon-center-park", 70)],
]
PARCEIROS = [("coopagi", 88), ("acaitech", 78)]

def proporcao(chave):
    """Razao largura/altura do arquivo, para dimensionar as logos pela altura."""
    for pasta in (REC, ASSETS):
        f = pasta / (chave + ".png")
        if f.exists():
            with Image.open(f) as im:
                return im.width / im.height
    raise KeyError(chave)


PROPORCAO = {c: proporcao(c) for c, _ in
             REALIZACAO + PARCEIROS + [i for linha in APOIO for i in linha]}


def lado_exibido(chave):
    """Maior lado, em mm, com que a imagem aparece na peca."""
    if chave in LADO_MM:
        return LADO_MM[chave]
    for c, h in REALIZACAO + PARCEIROS + [i for l in APOIO for i in l]:
        if c == chave:
            return max(h, h * PROPORCAO[c])
    return None


# logos e fotos enviados pela organizacao, ja com fundo recortado
IMG = {p.stem: data_uri(p, lado_exibido(p.stem)) for p in sorted(REC.glob("*.png"))
       if not p.stem.startswith("000-")}
IMG.update({n: data_uri(ASSETS / (n + ".png"), lado_exibido(n))
            for n in ("coopagi", "acaitech")})
# o elenco pesa quase tudo: na versao Express entra achatado sobre o proprio
# fundo da peca, o que dispensa o canal alfa e troca o PNG por um JPEG
IMG["elenco"] = data_uri(ASSETS / ("elenco-express.jpg" if EXPRESS else "elenco.png"))


def bloco_show(dia, nota, nomes):
    linhas = "".join('<div class="tj-nome">%s</div>' % n for n in nomes)
    obs = '<div class="tj-nota">%s</div>' % nota if nota else ""
    return ('<div class="tj">'
            '<div class="tj-dia">%s%s</div>'
            '<div class="tj-nomes">%s</div></div>' % (dia, obs, linhas))


def bloco_palestra(dia, temas):
    linhas = "".join('<div class="pa-tema">%s</div>' % t for t in temas)
    return '<div class="pa"><div class="pa-dia">%s</div>%s</div>' % (dia, linhas)


def logo(chave, altura_mm, classe=""):
    larg = round(altura_mm * PROPORCAO[chave], 1)
    return ('<img class="lg %s" src="%s" style="width:%smm;height:%smm" alt="%s">'
            % (classe, IMG[chave], larg, altura_mm, chave.replace("logo-", "")))


def linha_logos(itens, classe="lg-row"):
    return '<div class="%s">%s</div>' % (
        classe, "".join(logo(c, h) for c, h in itens))


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
.t-centro .wordmark { font-size: 176mm; margin-top: 12mm; }
.t-centro .tagline { font-size: 40mm; margin-top: 12mm; letter-spacing: 0.03em; }
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
.t-cav { width: 330mm; height: 201mm; display: block; }
.t-nin { width: 165mm; height: 213mm; display: block; }

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

/* composicao de grupo das atracoes, no padrao da arte oficial */
.elenco { width: 480mm; display: block; margin: 26mm auto 22mm; }

/* tarja com os nomes agrupados por data */
.tarja {
  width: 100%%;
  background: rgba(4,26,11,0.86);
  border: 2.4mm solid #E3B45A;
  border-radius: 10mm;
  padding: 8mm 20mm;
}
.tj {
  display: flex;
  align-items: center;
  gap: 18mm;
  padding: 14mm 0;
  text-align: left;
}
.tj + .tj { border-top: 0.9mm solid rgba(227,180,90,0.42); }
.tj-dia {
  font-family: "anton", sans-serif;
  font-size: 62mm;
  line-height: 1;
  color: #E3B45A;
  width: 132mm;
  flex: none;
}
.tj-nota {
  font-family: "montserrat", sans-serif;
  font-weight: 800;
  font-size: 13mm;
  line-height: 1.2;
  letter-spacing: 0.06em;
  color: #FBF7EB;
  margin-top: 5mm;
}
.tj-nomes { flex: 1; }
.tj-nome {
  font-family: "anton", sans-serif;
  font-size: 33mm;
  line-height: 1.24;
  color: #FBF7EB;
  letter-spacing: 0.01em;
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
.l-cav { width: 320mm; height: 195mm; display: block; }
.l-nin { width: 160mm; height: 207mm; display: block; }

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
.lg { display: block; object-fit: contain; }
.lg-row {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 22mm;
}
/* a marca da prefeitura e em tipografia branca: precisa de fundo escuro */
.chip-escuro {
  background: #0E2A4A;
  border-radius: 5mm;
  padding: 8mm 10mm;
  display: flex;
  align-items: center;
}
.divisor { width: 300mm; height: 0.9mm; background: #D6DCD6; margin: 4mm auto; }

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
        <img class="elenco" src="%(elenco)s" alt="Atra&ccedil;&otilde;es da II FENAGRO-MR">
        <div class="tarja">%(shows)s</div>
      </div>
    </div>
    <div>
      <div class="l-selos">
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
        %(realiza)s
        <div class="divisor"></div>
        <div class="lbl">APOIO</div>
        %(apoio)s
        <div class="divisor"></div>
        <div class="lbl">PARCEIROS DAS PALESTRAS</div>
        %(parceiros)s
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""

apoio_html = "".join(
    linha_logos(linha) if i == 0 else
    '<div class="lg-row">%s</div>' % "".join(
        ('<div class="chip-escuro">%s</div>' % logo(c, h))
        if c == "logo-prefeitura-mae-do-rio" else logo(c, h) for c, h in linha)
    for i, linha in enumerate(APOIO))

html = HTML % {
    "css": CSS % {"luzes_lat": LUZES_LATERAL, "luzes_tes": LUZES_TESTEIRA},
    "logo": IMG["logo-fenagro-mr"],
    "cav": IMG["logo-cavalgada-arrojados"],
    "nin": IMG["logo-ninho-dos-bons"],
    "elenco": IMG["elenco"],
    "realiza": linha_logos(REALIZACAO),
    "apoio": apoio_html,
    "parceiros": linha_logos(PARCEIROS),
    "shows": "".join(bloco_show(*x) for x in SHOWS),
    "palestras": "".join(bloco_palestra(*x) for x in PALESTRAS),
    "destaques": "".join('<div class="dest">%s</div>' % d for d in DESTAQUES),
}

if EXPRESS:
    # kit de fontes Adobe gerado para a conta em uso; mesmos nomes CSS
    html = html.replace("https://use.typekit.net/oia8csk.css",
                        "https://use.typekit.net/iqu0oeo.css")
    # metadados que o importador do Adobe Express le para achar e dimensionar
    # cada peca; o tamanho vai em px a 96 dpi, como o importador espera
    px = lambda mm: int(round(mm * MM_PX))
    html = html.replace("<title>",
        '<meta name="hz:slide-selector" content=".peca">\n'
        '<meta name="hz:canvas-width" content="%d">\n'
        '<meta name="hz:canvas-height" content="%d">\n' % (px(600), px(5000))
        + "<title>", 1)
    for pid, (w, h) in (("testeira", (3200, 600)), ("lateral-esq", (600, 5000)),
                        ("lateral-dir", (600, 5000))):
        html = html.replace('id="%s">' % pid,
                            'id="%s" data-canvas-width="%d" data-canvas-height="%d">'
                            % (pid, px(w), px(h)), 1)
    OUT = BASE / "portico-fenagro-Express-export.html"

OUT.write_text(html, encoding="utf-8")
print("%s  (%.1f MB)" % (OUT, OUT.stat().st_size / 1e6))
