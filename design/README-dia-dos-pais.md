# Dia dos Pais — Stories 1080×1920 — Marca Registrada

Publicação comemorativa de Dia dos Pais (não é peça de venda: não fala em presente,
preço nem produto). Direção **editorial minimalista**: ciclorama warm greige gerado
proceduralmente, foto de campanha composta dentro dele e tipografia geométrica leve em
caixa alta com muito respiro no topo.

**A linha.** `CADA PAI TEM / SUA MARCA REGISTRADA.` — o nome da loja é o desfecho da
frase. "Marca registrada" no sentido do jeito dele, aquilo que só aquele pai faz. Por
isso o topo leva **só o símbolo** do logotipo, sem o lettering: quem diz o nome da marca
na peça é o próprio título, e repetir o wordmark logo acima mataria a virada.

## Arquivos

| Arquivo | Descrição |
| --- | --- |
| `dia-dos-pais-stories.html` | Design final, autocontido (fonte e fundo em base64). É este arquivo que o Canva/Express importa. |
| `dia-dos-pais-stories-1080x1920.png` | Export para publicação. |
| `src/build_pais.py` | Gera o fundo de estúdio e o HTML. Todo o texto está no topo do arquivo. |
| `src/render.py` | Exporta qualquer HTML de design para PNG via Chromium. |
| `src/bg_pais.jpg` | Ciclorama + foto já compostos (não editar à mão — sai do build). |
| `src/jost-var.woff2` | Jost variable 100–900, subset latin (SIL Open Font License). |
| `src/logo_marca_registrada.png` | Logotipo original do cliente, como recebido. |
| `src/simbolo_creme.png` | Símbolo recortado e repintado em creme (sai do build). |
| `src/foto.jpg` | Foto de campanha. Se o arquivo existir, entra automaticamente. |

**Crédito da imagem:** Adobe Stock, asset `639834895` — *"Portrait of happy casual older
bearded man with glasses and gray hair smiling"*, licenciada pela conta Adobe da loja.
Guardada aqui reduzida para 2160 px de largura (o build renderiza em 1080).

## Sistema

**Tipografia** — Jost (revival de Futura, a geométrica clássica da moda), uma família só:

| Uso | Peso | Corpo | Tracking |
| --- | --- | --- | --- |
| Título | 250 | 96 px | .008 em, entrelinha 1.02 |
| Linha de assinatura | 300 | 28 px | .14 em |
| @ da loja | 400 | 22 px | .34 em |

O símbolo do logotipo entra com 240 px de largura, centralizado, a 150 px do topo.

**Paleta**

| Cor | Hex | Uso |
| --- | --- | --- |
| Creme | `#F3EFE7` | Título, assinatura da loja |
| Areia | `#B9AC9B` | Rótulos, filetes, @ |
| Ciclorama escuro | `#2A241F` | Topo e vinheta lateral |
| Ciclorama claro | `#ADA08F` | Centro do refletor e piso |

**Grade** — margem lateral 92 px. Símbolo no topo (fora da faixa de UI do Instagram),
título em dois blocos com alinhamentos opostos (esquerda e depois direita), bloco de
assinatura terminando em y=1646 para não cair atrás da barra de resposta.

## Trocar os textos

Tudo fica no topo de `src/build_pais.py`:

```python
LINHA_A = ['Cada pai tem']              # bloco alinhado à esquerda
LINHA_B = ['sua marca', 'registrada.']  # bloco alinhado à direita
ASSINA  = 'Feliz Dia dos Pais'
ARROBA  = '@marcaregistrada'
```

O `@` está como suposição — confirmar o handle real antes de publicar.

## Trocar a foto de campanha

Salve a nova foto como `src/foto.jpg` e rode o build. Ela não é uma camada por cima do
fundo: o build a compõe *dentro* do ciclorama, em cinco passos —

1. neutraliza o fundo do estúdio da foto, usando o próprio fundo como referência de cinza;
2. aplica o grade da campanha (empurra o neutro para o greige quente);
3. casa a luminância da foto com a do ciclorama exatamente na linha da emenda;
4. prolonga o fundo da foto para cima, para o degradê ter onde acontecer;
5. funde com alfa em *smoothstep*, e só depois joga o grão por cima de tudo.

É o passo 5 que faz a emenda sumir: foto e fundo terminam compartilhando a mesma textura.
Por isso funciona melhor com **foto de estúdio, fundo neutro liso, vertical, sujeito
enquadrado do peito para cima**.

Dois parâmetros controlam o encaixe, no topo do `build_pais.py`:

```python
FOTO_TOPO_CABECA = 0.051   # onde a cabeça começa na foto (fração da altura)
FOTO_CABECA_Y    = 946     # onde a cabeça deve cair no canvas
FOTO_FUSAO       = 360     # altura do degradê de fusão, em px
```

Ao trocar a foto, meça `FOTO_TOPO_CABECA` na imagem nova — é o único valor que costuma
mudar.

## Regenerar

```bash
pip install pillow numpy playwright
python3 src/build_pais.py                              # gera o HTML
python3 src/render.py dia-dos-pais-stories.html 1080 1920   # gera o PNG
```
