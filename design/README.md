# Ferro Velho Alkimin — post "Boa semana"

Post 1080×1350 (Instagram 4:5) construído a partir da referência visual do cliente:
mesmo fundo cinza texturizado, logo na mesma posição, mesmo bloco de horário de
funcionamento. A frase principal foi trocada por uma mensagem de início de semana
e os textos principais passaram para branco.

## Arquivos

| Arquivo | Descrição |
| --- | --- |
| `alkimin-boa-semana.html` | Design final, autocontido (imagens e fontes embutidas em base64). É este arquivo que o Canva importa. |
| `alkimin-boa-semana-1080x1350.png` | Export final para publicação. |
| `src/build.py` | Gera o HTML a partir dos assets abaixo. |
| `src/bg.jpg` | Textura de concreto cinza gerada proceduralmente. |
| `src/logo.png` | Logo recortado da referência, fundo removido. |
| `src/recycle.svg`, `src/recycle_paths.txt` | Símbolo de reciclagem usado nas marcas d'água. |
| `src/*.woff2` | Anton e Poppins (subset latin, SIL Open Font License). |

## Paleta

| Cor | Hex | Uso |
| --- | --- | --- |
| Azul | `#0F2B75` | Logo, rótulo de horário, caixas |
| Verde | `#3D823B` | Filetes, chevrons, marcas d'água |
| Cinza (topo) | `#B8B8BA` | Fundo |
| Cinza (base) | `#959595` | Fundo |
| Branco | `#FFFFFF` | Frase principal e apoio |

## Regenerar

```bash
pip install pillow numpy playwright
python3 src/build.py          # gera alkimin-boa-semana.html
```
