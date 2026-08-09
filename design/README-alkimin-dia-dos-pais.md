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
> A todos os pais que ensinam sem perceber:
> o que vocês começaram segue firme.
> Não foi sorte, foi exemplo honesto.
> E a gente aprendeu a fazer igual.
>
> **Feliz Dia dos Pais**

A mensagem fala **com** os pais, não *sobre* um pai — daí o "vocês". Para um Stories que o
cliente vê, endereçar funciona melhor do que narrar.

O desejo é a última linha da copy, mas entra na peça como a assinatura verde, em corpo
maior. Assim ele aparece uma vez só e ainda ganha destaque.

Escrito na voz do ofício — concreto e direto, vocabulário simples. O registro editorial e
econômico usado na peça da Marca Registrada (`README-dia-dos-pais.md`) soaria falso aqui:
são clientes com públicos e tons opostos, ainda que a data seja a mesma.

Nada de "sucata", "ferro velho" ou "segunda geração" no texto: o legado aparece por dentro
("o que vocês começaram segue firme"), não anunciado. Persistência e exemplo estão ditos
sem virar palavra de ordem.

## Arquivos

| Arquivo | Descrição |
| --- | --- |
| `alkimin-dia-dos-pais.html` | Design final, autocontido. É este arquivo que o Canva/Express importa. |
| `alkimin-dia-dos-pais-1080x1920.png` | Export para publicação. |
| `src/build_alkimin_pais.py` | Gera o HTML. Todo o texto está no topo do arquivo. |
| `src/render.py` | Exporta o HTML para PNG via Chromium. |
| `src/foto_alkimin.jpg` | Foto de campanha (Adobe Stock, ver crédito abaixo). |
| `src/bg_pais_alkimin.jpg` | Concreto + foto já compostos (sai do build). |
| `src/logo_branco.png` | Logo repintado em branco para ler sobre a foto (sai do build). |

**Crédito da imagem:** Adobe Stock `676335764` — *"Instructor teaching the trade to a metal
industrial factory worker"*, licenciada pela conta Adobe da loja. Guardada reduzida para
2400 px de largura.

Escolhida entre quatro licenciadas porque é a única em que a diferença de gerações se lê:
o mais velho opera a máquina, o mais novo observa. De lado, máquina real, ninguém posando
para a câmera — e os uniformes azuis caem na cor da marca por acaso feliz. As descartadas:
`1390913255` (três gerações em marcenaria, mas com criança), `447723348` (pátio de sucata
real, porém um trabalhador só, de frente e sorrindo) e `616200017` (dois homens da mesma
idade, sem leitura de gerações).

Os assets (`bg_story.jpg`, `logo.png`, `recycle_paths.txt`, fontes) são os mesmos já
versionados para os outros posts da Alkimin — nada de novo foi criado.

## Grade

| Elemento | Posição |
| --- | --- |
| Faixa da foto | y 0 a 760, sangrando nas laterais |
| Logo (branco) | x 680, y 96, largura 330 |
| Card azul | x 60, y 800, 960×785, raio 53 |
| Título (Anton 104 px) | x 124, y 870 |
| Filete verde | x 124, y 1122, 176×4 |
| Mensagem (Poppins 400, 34 px) | x 124, y 1182 |
| Assinatura (Poppins 700, 40 px) | x 124, y 1460 |

O card termina em y=1585, acima da barra de resposta do Instagram. As marcas d'água
inferiores (y=1680) ficam atrás dela de propósito — são textura, não informação.

**A faixa da foto** não é uma imagem colada por cima: o build a compõe dentro do fundo de
concreto, com um degradê em *smoothstep* nos últimos 140 px, para não deixar uma linha reta
cortando a peça. A foto entra dessaturada em 55% e levemente esfriada — o assunto é o
trabalho, não a fotografia. Os 300 px do topo levam um véu escuro que dá superfície ao logo
branco.

O logo foi para a direita, sobre a máquina escura: à esquerda ele caía em cima do rosto do
trabalhador mais novo. Os chevrons verdes e a marca d'água superior saíram — com a foto no
topo, virariam ruído.

## Regenerar

```bash
pip install pillow numpy playwright
python3 src/build_alkimin_pais.py
python3 src/render.py alkimin-dia-dos-pais.html 1080 1920
```
