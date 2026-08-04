"""Gera a foto de perfil do canal.

Foto de perfil é o único elemento da marca que a plataforma exibe a 40 pixels.
Por isso ela não é uma ilustração reduzida: é um monograma desenhado para
sobreviver ao tamanho mínimo, com contraste alto e no máximo duas formas.

    python scripts/perfil.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from comum import RAIZ

LADO = 1024
AZUL_CENTRO = (26, 64, 153)
AZUL_BORDA = (8, 24, 66)
AMARELO = (255, 199, 0)
BRANCO = (255, 255, 255)

FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fundo(lado):
    """Degradê radial: dá profundidade sem competir com as letras."""
    img = Image.new("RGB", (lado, lado), AZUL_BORDA)
    d = ImageDraw.Draw(img)
    passos = 90
    for i in range(passos, 0, -1):
        proporcao = i / passos
        raio = int(lado * 0.78 * proporcao)
        mistura = 1 - proporcao
        cor = tuple(int(AZUL_BORDA[c] + (AZUL_CENTRO[c] - AZUL_BORDA[c]) * mistura)
                    for c in range(3))
        d.ellipse([lado // 2 - raio, lado // 2 - raio,
                   lado // 2 + raio, lado // 2 + raio], fill=cor)
    return img.filter(ImageFilter.GaussianBlur(lado // 40))


def desenhar(lado=LADO):
    img = fundo(lado)
    d = ImageDraw.Draw(img)

    # As letras ocupam o máximo possível: num círculo de 40px, tamanho é tudo.
    # Branco sobre azul escuro já tem contraste de sobra — sombra aqui só
    # acrescentaria um relevo que suja a letra quando a plataforma comprime.
    fonte = ImageFont.truetype(FONTE, int(lado * 0.49))
    texto = "IA"
    caixa = d.textbbox((0, 0), texto, font=fonte)
    largura, altura = caixa[2] - caixa[0], caixa[3] - caixa[1]
    x = (lado - largura) / 2 - caixa[0]
    y = (lado - altura) / 2 - caixa[1] - lado * 0.055
    d.text((x, y), texto, font=fonte, fill=BRANCO)

    # Barra amarela: o único elemento de cor, e o que diferencia de qualquer
    # outro monograma "IA" por aí. Encostada na base das letras, para os dois
    # lerem como um bloco só em vez de dois elementos soltos.
    barra_l = lado * 0.30
    barra_a = lado * 0.055
    barra_y = y + altura + caixa[1] + lado * 0.055
    d.rounded_rectangle([(lado - barra_l) / 2, barra_y,
                         (lado + barra_l) / 2, barra_y + barra_a],
                        radius=barra_a / 2, fill=AMARELO)
    return img


def principal():
    destino = RAIZ.parent / "projeto-canal" / "marca"
    destino.mkdir(parents=True, exist_ok=True)

    img = desenhar()
    caminho = destino / "perfil-1024.png"
    img.save(caminho)

    # Prova real: as plataformas recortam em círculo e exibem pequeno.
    for tamanho in (400, 98, 40):
        img.resize((tamanho, tamanho), Image.LANCZOS).save(destino / f"perfil-{tamanho}.png")

    print(f"Foto de perfil em {destino}")
    return caminho


if __name__ == "__main__":
    principal()
