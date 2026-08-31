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
SOBREP_V = 0.22         # quanto cada fileira sobe sobre a anterior
FOLGA_H = 1.20          # largura extra da fileira, consumida na sobreposicao
ESVANECE = 260          # px de esvaecimento no pe da composicao
ESVANECE_FILEIRA = 150  # idem no pe de cada fileira

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


def dissolve_pe(im, altura):
    """Apaga o corte reto do pe da imagem, dissolvendo-o no fundo."""
    altura = min(altura, im.height)
    rampa = Image.new("L", (1, altura))
    for i in range(altura):
        rampa.putpixel((0, i), round(255 * (1 - i / altura) ** 1.6))
    alpha = im.getchannel("A")
    y = im.height - altura
    alpha.paste(rampa.resize((im.width, altura)), (0, y),
                alpha.crop((0, y, im.width, im.height)))
    im.putalpha(alpha)
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

    # as fotos sempre se sobrepoem: sem isso, as bordas do recorte de cada uma
    # ficam a mostra contra o fundo verde
    total = sum(i.width for i in ims)
    f = largura * FOLGA_H / total
    ims = [i.resize((max(1, round(i.width * f)), max(1, round(i.height * f))),
                    Image.LANCZOS) for i in ims]
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
    return dissolve_pe(fileira.crop((0, 0, largura, alt)), ESVANECE_FILEIRA)


fileiras = [monta_fileira(f, LARGURA, ALTURA_FILEIRA) for f in FILEIRAS]
tops, y = [], 0.0
for f in fileiras:
    tops.append(round(y)); y += f.height * (1 - SOBREP_V)
elenco = Image.new("RGBA", (LARGURA, round(tops[-1] + fileiras[-1].height)), (0, 0, 0, 0))
for f, t in zip(fileiras, tops):
    elenco.alpha_composite(f, (0, t))

# o pe da composicao nao tem nada na frente: dissolve mais longo
elenco = dissolve_pe(elenco, ESVANECE)

elenco.save(OUT)
print("%s  %s px  (%.0f x %.0f mm na peca)"
      % (OUT.name, elenco.size, 480, 480 * elenco.height / elenco.width))
