#!/usr/bin/env python3
"""Monta as fotos dos artistas em uma composicao unica de grupo.

Segue a arte-referencia da FENAGRO: fileiras sobrepostas, sem legenda em cada
rosto -- os nomes vao na tarja de datas. Como a lateral do portico e estreita e
alta (0,60 x 5,00 m), as fotos entram em duplas, o que mantem os rostos grandes.
A saida e um PNG com transparencia, usado como bloco unico na lateral.
"""
import pathlib
from PIL import Image, ImageFilter

BASE = pathlib.Path(__file__).parent
REC = BASE / "recebidos"
OUT = BASE / "assets_hi" / "elenco.png"

LARGURA = 1560          # px da composicao; a lateral reserva 480 mm de largura
ALTURA_FILEIRA = 1480   # px; igual em todas, para nao variar a escala dos rostos
SOBREP_V = 0.16         # quanto cada fileira sobe sobre a anterior

# (arquivo, escala) -- a escala equilibra o tamanho das cabecas, ja que as fotos
# chegaram com enquadramentos diferentes (de meio corpo a corpo inteiro).
# As fileiras vao do fundo para a frente.
FILEIRAS = [
    [("b-chapeu-marrom-xadrez", 1.00), ("artista-chapeu-preto", 0.96)],
    [("c-chapeu-marrom-oculos", 0.92), ("b-chapeu-palha-preta", 0.96)],
    [("sanfoneiro", 1.10), ("b-chapeu-branco-palco", 0.86)],
    [("gleyk-e-gleyson", 0.82), ("b-jaqueta-bracos-cruzados", 1.00)],
    [("evandro-do-acordeon", 0.98), ("c-chapeu-branco-camisa-preta", 1.00)],
    [("b-camisa-branca-noturna", 0.94), ("deyse-bandeira", 0.92)],
]


def limpa(nome, im):
    """Retoques nos originais antes da montagem."""
    if nome == "evandro-do-acordeon":
        # o proprio arquivo traz o logotipo do artista; os nomes vao na tarja
        return im.crop((0, 0, im.width, round(im.height * 0.70)))
    return im


def sombra(im):
    """Sombra suave para descolar o recorte do fundo verde escuro."""
    s = Image.new("RGBA", (im.width + 40, im.height + 40), (0, 0, 0, 0))
    s.paste(Image.new("RGBA", im.size, (0, 0, 0, 150)), (20, 27), im)
    return s.filter(ImageFilter.GaussianBlur(15))


def monta_fileira(itens, largura, altura):
    """Escala as fotos a uma altura fixa, alinha pelos pes e fecha a largura."""
    ims = []
    for nome, escala in itens:
        im = limpa(nome, Image.open(REC / (nome + ".png")).convert("RGBA"))
        h = max(1, round(altura * escala))
        ims.append(im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS))

    # fileira estreita demais deixaria buraco no meio: cresce um pouco para fechar
    total = sum(i.width for i in ims)
    if total < largura * 1.06:
        f = min(1.18, largura * 1.06 / total)
        ims = [i.resize((round(i.width * f), round(i.height * f)), Image.LANCZOS)
               for i in ims]
        total = sum(i.width for i in ims)
    passo = (total - largura) / (len(ims) - 1)
    xs, x = [], 0.0
    for i in ims:
        xs.append(round(x)); x += i.width - passo

    alt = max(i.height for i in ims)
    fileira = Image.new("RGBA", (max(total, largura), alt), (0, 0, 0, 0))
    # o rosto central fica na frente: desenha das pontas para o meio
    for k in sorted(range(len(ims)), key=lambda k: -abs(k - (len(ims) - 1) / 2)):
        y = alt - ims[k].height                  # todos apoiados na mesma linha
        fileira.alpha_composite(sombra(ims[k]), (xs[k] - 20, y - 20))
        fileira.alpha_composite(ims[k], (xs[k], y))
    return fileira.crop((0, 0, largura, alt))


fileiras = [monta_fileira(f, LARGURA, ALTURA_FILEIRA) for f in FILEIRAS]
tops, y = [], 0.0
for f in fileiras:
    tops.append(round(y)); y += f.height * (1 - SOBREP_V)
elenco = Image.new("RGBA", (LARGURA, round(tops[-1] + fileiras[-1].height)), (0, 0, 0, 0))
for f, t in zip(fileiras, tops):
    elenco.alpha_composite(f, (0, t))

elenco.save(OUT)
print("%s  %s px  (%.0f x %.0f mm na peca)"
      % (OUT.name, elenco.size, 480, 480 * elenco.height / elenco.width))
