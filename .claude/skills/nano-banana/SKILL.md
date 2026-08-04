---
name: nano-banana
description: Gera imagens com o Nano Banana (modelos de imagem do Gemini) para o canal — thumbnail, foto de perfil, capa, arte de fundo. Use quando o pedido for criar ou variar uma imagem do projeto. Requer GEMINI_API_KEY.
---

# Nano Banana — geração de imagem

## O que esta skill é, e o que ela não é

Ela é a instrução de **como** chamar a API de imagem do Gemini neste projeto.
Ela **não** dá acesso ao modelo — quem dá é a `GEMINI_API_KEY`. Sem a chave,
nada aqui funciona.

## Verificar antes de qualquer coisa

```bash
echo "${GEMINI_API_KEY:+chave presente}"
```

Se não imprimir nada, pare e peça a chave ao usuário (aistudio.google.com).
Não tente gerar sem ela e não invente que a imagem foi criada.

## Uso

```bash
python automacao/scripts/imagem.py "PROMPT EM INGLÊS" --saida caminho/arquivo.png
python automacao/scripts/imagem.py "..." --modelo pro --proporcao 16:9
```

| Modelo | Id da API | Quando usar |
|---|---|---|
| `lite` (padrão) | `gemini-3.1-flash-lite-image` | Rascunho, variação, teste. Mais barato. |
| `pro` | `gemini-3-pro-image-preview` | Entrega final, texto dentro da imagem, 4K. |

Proporções úteis: `1:1` perfil, `9:16` story e Shorts, `16:9` capa e thumbnail.

## Regras deste projeto

1. **Escreva o prompt em inglês.** O modelo responde bem melhor.
2. **Use a paleta da marca** (ver `projeto-canal/09-identidade.md`): azul
   `#0F2B75`, amarelo `#FFC700` só como acento. Cite os hex no prompt.
3. **Nunca gere foto de perfil por IA.** O avatar aparece a ~40px em círculo,
   onde ilustração vira borrão. Perfil é monograma, e já existe:
   `automacao/scripts/perfil.py`. Use o Nano Banana para thumbnail, capa e
   arte de fundo — onde a imagem é vista grande.
4. **Sempre olhe o resultado** com a ferramenta de leitura de imagem antes de
   entregar. Modelo de imagem erra texto, mão e simetria com frequência.
5. **Reduza para o tamanho real de exibição e olhe de novo.** Thumbnail que não
   funciona em miniatura não funciona.

## Custo

Cada chamada é paga. Ordem de grandeza: `lite` ~US$ 0,03 por imagem; `pro`
~US$ 0,13 em 1K/2K e ~US$ 0,24 em 4K. Gere rascunho em `lite` e só suba para
`pro` quando a composição estiver decidida — não itere no modelo caro.

## Onde guardar a chave

- **Uso pontual nesta sessão:** o usuário exporta `GEMINI_API_KEY` no ambiente.
- **Uso no pipeline:** secret do repositório, igual ao `PEXELS_API_KEY`, e o
  workflow passa por `env:`.

A chave **nunca** entra em arquivo versionado — o repositório é público.
