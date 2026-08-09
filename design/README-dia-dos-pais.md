# Dia dos Pais — Stories 1080×1920 (loja multimarcas)

Arte de campanha para Instagram Stories, direção **editorial minimalista**: ciclorama
warm greige gerado proceduralmente, tipografia geométrica leve em caixa alta e muito
respiro no topo. A referência de linguagem foi um editorial de moda com fundo neutro e
texto fino tracked — mas paleta, tipografia, layout e copy são originais.

## Arquivos

| Arquivo | Descrição |
| --- | --- |
| `dia-dos-pais-stories.html` | Design final, autocontido (fonte e fundo em base64). É este arquivo que o Canva/Express importa. |
| `dia-dos-pais-stories-1080x1920.png` | Export para publicação. |
| `src/build_pais.py` | Gera o fundo de estúdio e o HTML. Todo o texto está no topo do arquivo. |
| `src/render.py` | Exporta qualquer HTML de design para PNG via Chromium. |
| `src/bg_pais.jpg` | Ciclorama gerado (não editar à mão — sai do build). |
| `src/jost-var.woff2` | Jost variable 100–900, subset latin (SIL Open Font License). |
| `src/foto.jpg` | **Opcional.** Foto de campanha. Se existir, entra automaticamente. |

## Sistema

**Tipografia** — Jost (revival de Futura, a geométrica clássica da moda), uma família só:

| Uso | Peso | Corpo | Tracking |
| --- | --- | --- | --- |
| Assinatura da loja (topo) | 300 | 38 px | .40 em |
| Rótulo da campanha | 400 | 21 px | .42 em |
| Título | 250 | 84 px | .010 em, entrelinha 1.02 |
| Linha de assinatura | 300 | 28 px | .14 em |
| @ da loja | 400 | 22 px | .34 em |

**Paleta**

| Cor | Hex | Uso |
| --- | --- | --- |
| Creme | `#F3EFE7` | Título, assinatura da loja |
| Areia | `#B9AC9B` | Rótulos, filetes, @ |
| Ciclorama escuro | `#2A241F` | Topo e vinheta lateral |
| Ciclorama claro | `#ADA08F` | Centro do refletor e piso |

**Grade** — margem lateral 92 px. Assinatura da loja no topo (fora da faixa de UI do
Instagram), título em dois blocos com alinhamentos opostos (esquerda e depois direita),
bloco de assinatura terminando em y=1690 para não cair atrás da barra de resposta.

## Trocar os textos

Tudo fica no topo de `src/build_pais.py`:

```python
MARCA   = 'NOME DA LOJA'
LABEL   = 'Dia dos Pais'
LINHA_A = ['O presente certo', 'não é o mais caro.']
LINHA_B = ['É o mais ele.']
ASSINA  = 'As marcas que ele veste, em um lugar só.'
ARROBA  = '@nomedaloja'
```

## Colocar a foto de campanha

Salve a foto como `src/foto.jpg` e rode o build. Ela entra em sangria, ocupando o terço
inferior, com uma máscara em gradiente que dissolve o topo dentro do ciclorama — por isso
funciona melhor com **foto de estúdio, fundo neutro liso, vertical, sujeito na metade de
baixo do quadro**. O enquadramento se ajusta em `.foto { object-position }`.

## Regenerar

```bash
pip install pillow numpy playwright
python3 src/build_pais.py                              # gera o HTML
python3 src/render.py dia-dos-pais-stories.html 1080 1920   # gera o PNG
```
