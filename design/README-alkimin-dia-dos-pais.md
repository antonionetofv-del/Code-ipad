# Ferro Velho Alkimin — Dia dos Pais, Stories 1080×1920

Publicação comemorativa de Dia dos Pais para o Ferro Velho Alkimin, empresa de segunda
geração. Não é peça de venda: não fala em preço, serviço nem sucata comprada.

Montada **dentro do sistema visual que a marca já tem neste repositório** — mesmo fundo
de concreto (`src/bg_story.jpg`), mesmo logo, mesmas marcas d'água de reciclagem e
chevrons, mesma dupla Anton + Poppins, mesma paleta. O card azul continua sendo o
elemento de assinatura; o que muda dentro dele é o conteúdo.

## O texto

> **De pai para filho**
>
> Ele ensinou a enxergar valor onde os outros só veem sucata. E a não largar no meio do
> caminho. Hoje a segunda geração toca o que ele começou.
>
> **Feliz Dia dos Pais** · 2ª geração

Escrito na voz do ofício — concreto e direto. O registro editorial e econômico usado na
peça da Marca Registrada (`README-dia-dos-pais.md`) soaria falso aqui: são clientes com
públicos e tons opostos, ainda que a data seja a mesma.

A frase cobre os três pontos do briefing sem listá-los: **foco** ("enxergar valor onde os
outros só veem sucata"), **persistência** ("não largar no meio do caminho") e **legado**
("a segunda geração toca o que ele começou"). O trocadilho está em *sucata* — a palavra
que descreve o material do negócio é a mesma que descreve o que os outros deixam passar.

## Arquivos

| Arquivo | Descrição |
| --- | --- |
| `alkimin-dia-dos-pais.html` | Design final, autocontido. É este arquivo que o Canva/Express importa. |
| `alkimin-dia-dos-pais-1080x1920.png` | Export para publicação. |
| `src/build_alkimin_pais.py` | Gera o HTML. Todo o texto está no topo do arquivo. |
| `src/render.py` | Exporta o HTML para PNG via Chromium. |

Os assets (`bg_story.jpg`, `logo.png`, `recycle_paths.txt`, fontes) são os mesmos já
versionados para os outros posts da Alkimin — nada de novo foi criado.

## Grade

| Elemento | Posição |
| --- | --- |
| Logo | x 70, y 300, largura 380 |
| Card azul | x 60, y 620, 960×820, raio 53 |
| Título (Anton 104 px) | x 124, y 690 |
| Filete verde | x 124, y 942, 176×4 |
| Mensagem (Poppins 400, 34 px) | x 124, y 1002 |
| Assinatura (Poppins 700, 40 px) | x 124, y 1268 |
| Selo (Poppins 600, 25 px) | x 124, y 1334 |

O card termina em y=1440, bem acima da barra de resposta do Instagram. As marcas d'água
inferiores (y=1680) ficam atrás dela de propósito — são textura, não informação.

## Regenerar

```bash
pip install pillow numpy playwright
python3 src/build_alkimin_pais.py
python3 src/render.py alkimin-dia-dos-pais.html 1080 1920
```
