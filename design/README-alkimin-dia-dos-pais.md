# Ferro Velho Alkimin — Dia dos Pais, Stories 1080×1920

Publicação comemorativa de Dia dos Pais para o Ferro Velho Alkimin, empresa de segunda
geração. Não é peça de venda: não fala em preço, serviço nem sucata comprada.

Duas versões da mesma peça, geradas pelo mesmo build:

- **`moldura`** — retângulo verde atrás, foto de cantos arredondados por cima, card do
  texto por cima de tudo.
- **`polaroid`** — a foto montada como polaroide, moldura branca com a borda de baixo mais
  larga, levemente girada.

Fundo de concreto (`src/bg_story.jpg`), card azul, Anton + Poppins e a paleta continuam
sendo os do sistema da marca. Os elementos soltos de reciclagem saíram, a pedido; a logo
ficou, em azul.

## O texto

> **De pai para filho**
>
> A todos os pais que ensinam
> com conselhos ou sem perceber:
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
| `alkimin-dia-dos-pais-moldura.html` · `-1080x1920.png` | Versão com retângulo verde e foto arredondada. |
| `alkimin-dia-dos-pais-polaroid.html` · `-1080x1920.png` | Versão polaroide. |
| `src/build_alkimin_pais.py` | Gera as duas. Todo o texto está no topo do arquivo. |
| `src/render.py` | Exporta o HTML para PNG via Chromium. |
| `src/foto_alkimin.jpg` | Foto de campanha (Adobe Stock, ver crédito abaixo). |
| `src/foto_grade.jpg` | A mesma foto já graduada (sai do build). |

**Origem da imagem:** fornecida pelo cliente. Guardada reduzida para 2400 px de largura
(o build renderiza a 960).

**O tratamento é leve de propósito: `DESSAT = 0.12` mais um ganho quente
(`[1.035, 1.000, 0.945]`).** Uma versão anterior
desta peça usava uma foto de banco fria e industrial, e ali dessaturar 55% e puxar para o
azul não custava nada. Esta é quente e humana, e é a temperatura que faz ela funcionar num
Dia dos Pais — o tratamento pesado a deixava cinza e sem vida. A dessaturação sobrou só
para tirar o excesso do xadrez vermelho ao lado do card azul, e o ganho quente devolve o
dourado da madeira. Contra o concreto neutro, o quente da foto vira o foco da peça.

O enquadramento é `object-position: center 35%`, que dá folga acima da cabeça do pai — em
42% ela encostava na borda superior da moldura.

O fundo `bg_story.jpg` e as fontes são os mesmos já versionados para os outros posts da
Alkimin.

## Grade

O bloco de texto é idêntico nas duas versões — o build calcula as posições a partir de
onde o card começa, então mudar o texto não desalinha nada.

**Moldura** — foto em `x 60–1020, y 130–790`, raio 44. O retângulo verde fica em
`x 100–1060, y 90–750`: sai do eixo em **dois lados vizinhos** (topo e direita), nunca nos
quatro, que é o que faz o deslocamento parecer intencional em vez de erro de alinhamento.
A foto se alinha à margem do card (60 px); quem sai do eixo é o verde. Card em `y 790–1586`.

**Polaroide** — moldura em `x 160–920, y 110–810`, girada −2,4°, com a foto `696×520`
recuada 32 px de três lados e 148 px embaixo. A foto vai **dentro** da div da moldura, não
ao lado dela: assim a rotação é uma só e as duas nunca se desencontram. Sombra única, e não
uma pilha — o importador do Express não lida bem com várias. Card em `y 840–1620`.

**A logo** fica centralizada logo abaixo do card, com 340 px de largura. Ela é azul e por
isso precisa de cinza atrás: sobre o card azul sumiria, e sobre a foto ficaria suja.
Centralizada e nesse tamanho ela fecha a peça como assinatura — foi para caber nela que a
foto encolheu de 560 para 520 px de altura. O build calcula a posição a partir do fim do card e tem um
`assert` que falha se ela cair atrás da barra de resposta do Instagram — assim mexer no
texto nunca empurra a logo para fora da área segura sem avisar.

Os dois cards terminam acima de y=1670, onde começa a barra de resposta do Instagram.

## Regenerar

```bash
pip install pillow numpy playwright
python3 src/build_alkimin_pais.py
python3 src/render.py alkimin-dia-dos-pais.html 1080 1920
```
