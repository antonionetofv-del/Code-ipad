"""Prepara a foto de campanha a partir do print de tela enviado pelo cliente.

O arquivo original e um screenshot de Stories: tem barra de status, tarja preta
em cima e embaixo, e a copy da campanha da Hope gravada na imagem. Este script
recorta o quadro util e remove o texto por inpainting.

O texto fica todo entre y 235 e 629 do quadro recortado; as pessoas so comecam
em y 795. Como a area do texto e fundo liso, o inpainting reconstroi sem deixar
rastro. A mascara e limitada a essa faixa justamente para nao tocar em ninguem.

    python3 src/preparar_foto.py <print.png>
"""
import pathlib, sys
import cv2
import numpy as np
from PIL import Image

D = pathlib.Path(__file__).parent

CARTAO = (0, 141, 1170, 2222)   # quadro util dentro do screenshot
TEXTO_Y = (200, 680)            # faixa onde vive a copy gravada
LIMIAR = 165                    # a partir daqui o pixel e considerado texto
FOLGA = 11                      # dilatacao da mascara, para pegar o antialias

origem = pathlib.Path(sys.argv[1])
cartao = Image.open(origem).convert('RGB').crop(CARTAO)
arr = np.asarray(cartao)

mascara = np.zeros(arr.shape[:2], np.uint8)
faixa = slice(*TEXTO_Y)
mascara[faixa] = (arr[faixa].mean(2) > LIMIAR).astype(np.uint8) * 255
mascara = cv2.dilate(mascara, np.ones((FOLGA, FOLGA), np.uint8))

limpo = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), mascara, 14, cv2.INPAINT_TELEA)

# o fundo ali e um degrade liso: uma passada de suavizacao so dentro da mascara
# apaga qualquer estria que o inpainting tenha deixado
suave = cv2.GaussianBlur(limpo, (0, 0), 9)
peso = cv2.GaussianBlur(cv2.dilate(mascara, np.ones((25, 25), np.uint8)),
                        (0, 0), 12).astype(np.float32)[:, :, None] / 255.0
limpo = (limpo * (1 - peso) + suave * peso).astype(np.uint8)

# PNG, nao JPEG: o print ja veio comprimido pelo Instagram, e cada gravacao
# em JPEG a mais soma artefato sobre artefato.
Image.fromarray(cv2.cvtColor(limpo, cv2.COLOR_BGR2RGB)).save(D / 'foto.png')
print(f'foto.png {cartao.size} | pixels tratados: {int((mascara > 0).sum()):,}')
