"""Desenha o apresentador do canal e sincroniza a boca com a narração.

O personagem é desenhado por código (Pillow), não baixado de serviço nenhum:
roda igual em toda execução, não depende de conta, não custa por vídeo e não
some se um serviço externo mudar de política.

O lip-sync sai de graça porque o Edge TTS já devolve o instante de cada palavra
falada. A partir dessas marcações montamos a linha do tempo da boca.

    python scripts/personagem.py roteiros/meu-video.md
"""

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw

from comum import (FORMATOS, carregar_json, carregar_roteiro, ffmpeg,
                   pasta_saida, rodar, salvar_json)

# Paleta da identidade (ver projeto-canal/09-identidade.md).
AZUL = (15, 43, 117)
AZUL_CLARO = (32, 74, 176)
AMARELO = (255, 199, 0)
BRANCO = (255, 255, 255)
ESCURO = (10, 22, 56)

LADO = 520          # lado do quadro do personagem, em pixels
QUADROS_POR_SEG = 12  # taxa da animação da boca; acima disso ninguém percebe

# Aberturas de boca. A ordem importa: o índice 0 é a boca fechada.
BOCAS = ["fechada", "pouco", "media", "muito", "sorriso"]


# Geometria do rosto. Olhos e boca ficam DENTRO do visor: além de ser a
# linguagem visual de assistente digital, evita que a boca aberta transborde
# a cabeça nos quadros de maior abertura.
VISOR = (92, 175, 428, 405)
OLHO_Y = 252
BOCA_Y = 341


def desenhar(boca, piscando=False):
    """Gera um quadro do personagem com determinada boca."""
    img = Image.new("RGBA", (LADO, LADO), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = LADO // 2

    # Antena
    d.line([(c, 78), (c, 140)], fill=AZUL_CLARO, width=11)
    d.ellipse([c - 27, 44, c + 27, 98], fill=AMARELO)
    d.ellipse([c - 13, 58, c + 3, 74], fill=BRANCO)

    # Fones laterais, desenhados antes da cabeça para ficarem atrás dela
    for lado in (-1, 1):
        x = c + lado * 196
        d.rounded_rectangle([x - 30, 232, x + 30, 350], radius=28, fill=AZUL_CLARO)

    # Cabeça
    d.rounded_rectangle([60, 130, LADO - 60, 450], radius=84, fill=AZUL,
                        outline=AZUL_CLARO, width=9)

    # Visor
    d.rounded_rectangle(VISOR, radius=58, fill=ESCURO)

    # Olhos
    for dx in (-70, 70):
        if piscando:
            d.rounded_rectangle([c + dx - 33, OLHO_Y - 7, c + dx + 33, OLHO_Y + 7],
                                radius=7, fill=BRANCO)
        else:
            d.ellipse([c + dx - 33, OLHO_Y - 33, c + dx + 33, OLHO_Y + 33], fill=BRANCO)
            d.ellipse([c + dx - 15, OLHO_Y - 15, c + dx + 15, OLHO_Y + 15], fill=AZUL)
            d.ellipse([c + dx - 6, OLHO_Y - 23, c + dx + 6, OLHO_Y - 11], fill=BRANCO)

    # Boca: a abertura é o que muda entre os quadros.
    alturas = {"fechada": 10, "pouco": 28, "media": 50, "muito": 74, "sorriso": 44}
    larguras = {"fechada": 96, "pouco": 80, "media": 92, "muito": 84, "sorriso": 132}
    altura, largura = alturas[boca], larguras[boca]
    x0, x1 = c - largura // 2, c + largura // 2
    y0, y1 = BOCA_Y - altura // 2, BOCA_Y + altura // 2

    if boca == "sorriso":
        # Arco cheio: sorriso aberto, com a borda de baixo arredondada.
        d.chord([x0, y0 - altura, x1, y1], start=0, end=180, fill=AMARELO)
    else:
        d.rounded_rectangle([x0, y0, x1, y1], radius=min(altura // 2, 20), fill=AMARELO)
        if altura > 30:
            # Sombra interna: dá profundidade e tira o aspecto de adesivo chapado.
            d.rounded_rectangle([x0 + 12, y0 + altura // 2, x1 - 12, y1 - 6],
                                radius=min(altura // 4, 12), fill=(122, 92, 0))

    return img


def gerar_quadros(destino):
    """Escreve um PNG por combinação de boca (e a variante piscando)."""
    destino.mkdir(parents=True, exist_ok=True)
    caminhos = {}
    for boca in BOCAS:
        caminho = destino / f"{boca}.png"
        desenhar(boca).save(caminho)
        caminhos[boca] = caminho
    caminho = destino / "piscando.png"
    desenhar("fechada", piscando=True).save(caminho)
    caminhos["piscando"] = caminho
    return caminhos


def linha_do_tempo(palavras, duracao):
    """Converte as marcações de palavra numa sequência de estados de boca.

    Dentro de cada palavra alternamos as aberturas num ritmo de sílaba; entre
    as palavras a boca fecha. É o que dá a leitura de fala, sem precisar de
    análise fonética.
    """
    quadros = []
    passo = 1.0 / QUADROS_POR_SEG
    tempo = 0.0
    indice = 0

    while tempo < duracao:
        # Avança até a palavra que cobre este instante.
        while indice < len(palavras) and palavras[indice]["fim"] < tempo:
            indice += 1

        boca = "fechada"
        if indice < len(palavras):
            palavra = palavras[indice]
            if palavra["inicio"] <= tempo <= palavra["fim"]:
                # Posição relativa dentro da palavra, em "sílabas" de 0,14s.
                passos = max(1, round((palavra["fim"] - palavra["inicio"]) / 0.14))
                fatia = (palavra["fim"] - palavra["inicio"]) / passos
                atual = int((tempo - palavra["inicio"]) / fatia)
                # Alterna entre aberturas para a boca não ficar travada.
                boca = ["media", "pouco", "muito", "pouco"][atual % 4]

        # Pisca a cada ~3,4s, por 2 quadros.
        if boca == "fechada" and (tempo % 3.4) < (2 * passo):
            boca = "piscando"

        quadros.append(boca)
        tempo += passo

    return quadros


def montar_video(quadros, caminhos, duracao, destino):
    """Monta o vídeo do personagem (com transparência) a partir dos estados."""
    lista = destino.parent / "lista_personagem.txt"
    passo = 1.0 / QUADROS_POR_SEG
    linhas = []
    for estado in quadros:
        linhas.append(f"file '{caminhos[estado].resolve()}'\nduration {passo:.4f}\n")
    # O concat demuxer ignora a duração do último item; repetimos para fechar.
    linhas.append(f"file '{caminhos[quadros[-1]].resolve()}'\n")
    lista.write_text("".join(linhas), encoding="utf-8")

    rodar([
        ffmpeg(), "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
        "-t", f"{duracao:.3f}",
        "-vf", f"fps={QUADROS_POR_SEG},format=rgba",
        "-c:v", "qtrle",  # codec com canal alfa, para preservar a transparência
        str(destino),
    ])
    lista.unlink()
    return destino


def principal(caminho_roteiro):
    meta, _ = carregar_roteiro(caminho_roteiro)
    destino = pasta_saida(meta)
    dados = carregar_json(destino / "blocos.json")

    palavras = dados.get("palavras")
    if not palavras:
        raise SystemExit("blocos.json não tem as marcações de palavra. "
                         "Rode narrar.py antes de personagem.py.")

    duracao = sum(b["duracao"] for b in dados["blocos"])
    caminhos = gerar_quadros(destino / "personagem")
    quadros = linha_do_tempo(palavras, duracao)

    falando = sum(1 for q in quadros if q not in ("fechada", "piscando"))
    print(f"  {len(quadros)} quadros a {QUADROS_POR_SEG}fps "
          f"({falando / len(quadros):.0%} com a boca em movimento)")

    saida = montar_video(quadros, caminhos, duracao, destino / "personagem.mov")
    dados["personagem"] = str(saida)
    salvar_json(destino / "blocos.json", dados)
    print(f"  personagem: {saida}")
    return saida


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roteiro")
    principal(parser.parse_args().roteiro)
