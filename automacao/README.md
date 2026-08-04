# Automação de produção de vídeo

Pipeline que transforma um roteiro em texto num vídeo pronto para publicar:
narração, fundos, legenda queimada sincronizada e trilha. Custo R$ 0.

A explicação do porquê de cada decisão está em
[`../projeto-canal/08-automacao.md`](../projeto-canal/08-automacao.md).

## Uso pelo iPad (recomendado) — nada para instalar

1. Crie ou edite um arquivo em `roteiros/`, seguindo o formato abaixo
2. Faça o commit
3. O GitHub Actions produz o vídeo sozinho
4. Vá em **Actions → Produzir vídeo → Artifacts** e baixe `videos.zip`

Para rodar sem commitar (produzir um roteiro específico), use
**Actions → Produzir vídeo → Run workflow** e informe o caminho do roteiro.

## Uso num computador

```bash
pip install -r requirements.txt

python scripts/produzir.py roteiros/exemplo-nota-fiscal.md   # um roteiro
python scripts/produzir.py --todos                            # todos
python scripts/produzir.py --todos --trilha trilhas/fundo.mp3 # com música
```

O resultado fica em `saida/<slug-do-titulo>/video.mp4`.

## Formato do roteiro

```markdown
---
titulo: Foto da nota vira planilha em 30 segundos
voz: pt-BR-AntonioNeural
ritmo: -3%
formato: vertical
hashtags: "#ia #produtividade #mei"
descricao: "Texto que vai na descrição da publicação."
---

[busca: person typing on keyboard paperwork]
Se você ainda digita nota fiscal numa planilha, para tudo.

[arquivo: minha-captura-de-tela.mp4]
Esse bloco usa um vídeo local em vez do banco de imagens.
```

- Cada parágrafo é **um bloco**: uma frase narrada e um fundo próprio
- `[busca: ...]` é o termo procurado no Pexels — **escreva em inglês**, o acervo
  responde muito melhor
- `[arquivo: ...]` usa um vídeo seu (captura de tela, por exemplo)
- Sem chave do Pexels, o pipeline gera um fundo em degradê e continua rodando

### Campos do cabeçalho

| Campo | Padrão | Observação |
|---|---|---|
| `titulo` | nome do arquivo | Vira o nome da pasta de saída |
| `voz` | `pt-BR-AntonioNeural` | Escolha uma e nunca mais mude |
| `ritmo` | `+0%` | `-5%` deixa mais didático, `+10%` mais dinâmico |
| `formato` | `vertical` | `vertical`, `horizontal` ou `quadrado` |
| `hashtags` | — | Copiadas para `publicar.txt` |
| `descricao` | 2 primeiros blocos | Copiada para `publicar.txt` |

### Vozes brasileiras disponíveis

```bash
edge-tts --list-voices | grep pt-BR
```

São 15 vozes neurais. `AntonioNeural` (masculina) e `FranciscaNeural`
(feminina) são as mais naturais para narração longa.

## Scripts

| Script | O que faz |
|---|---|
| `produzir.py` | Roda tudo. É o único que você precisa chamar. |
| `narrar.py` | Roteiro → narração `.mp3` + legenda `.ass` sincronizada |
| `assets.py` | Baixa os fundos no Pexels (ou gera degradê) |
| `montar.py` | Fundos + narração + legenda + trilha → `video.mp4` |
| `cortar.py` | Recorta um vídeo longo em verticais com fundo desfocado |
| `comum.py` | Leitura do roteiro e utilidades compartilhadas |

### Recortar um vídeo longo

```bash
python scripts/cortar.py saida/meu-video/video.mp4 --cortes "0:15-1:25,3:40-4:55"
```

Cada trecho vira um 1080x1920 com o vídeo original centralizado e fundo
desfocado. É assim que 1 vídeo longo vira 3 curtos.

## Chave do Pexels (opcional, mas recomendada)

Sem ela o vídeo sai com fundo em degradê — funciona, mas fica pobre.

1. Crie uma conta gratuita em `pexels.com/api` e copie a chave
2. No GitHub: **Settings → Secrets and variables → Actions → New repository secret**
3. Nome: `PEXELS_API_KEY`, valor: sua chave

Localmente: `export PEXELS_API_KEY=sua-chave`.

## Trilha sonora

Coloque um `.mp3` em `trilhas/` (Biblioteca de Áudio do YouTube ou Pixabay
Music — confira sempre a licença). O Actions usa a primeira que encontrar,
em volume 7%, baixo o suficiente para não competir com a narração.

## Detalhes de implementação que importam

**A legenda vem de graça e perfeitamente sincronizada.** O Edge TTS devolve
eventos `WordBoundary` com o instante de cada palavra. Como nós sintetizamos a
voz, já sabemos os tempos — não é preciso reconhecimento de fala.

**A legenda é `.ass`, não `.srt`.** Para legenda SRT o libass assume uma tela
de 384×288 e interpreta corpo de fonte e margem nessa escala, o que joga o
texto para fora do lugar. O `.ass` carrega `PlayResX`/`PlayResY` iguais ao
canvas, então os valores são pixels reais.

**Curtos abaixo de 61 segundos disparam aviso.** O TikTok Creator Rewards só
considera vídeos acima de 1 minuto.

## Desempenho medido

Primeira execução real no GitHub Actions, 7 vídeos verticais:

| Etapa | Tempo |
|---|---|
| Instalar ffmpeg e fontes | 50s |
| Instalar dependências | 6s |
| Produzir os 7 vídeos | 8min51s |
| **Total** | **~10 min** |

Isso dá cerca de 76 segundos de máquina por vídeo — bem dentro dos 2.000
minutos mensais gratuitos.

O grosso desse tempo é a geração dos degradês de reserva, que usam `zoompan` em
1080x1920 e é caro. **Com a chave do Pexels configurada esse passo some**, e a
produção fica mais rápida além de ficar mais bonita.

## Limites conhecidos

- **Publicação é manual.** A API do TikTok exige aprovação comercial; a do
  YouTube exige OAuth com projeto no Google Cloud. Ver arquivo 08.
- **Thumbnail é manual.** Feita no Canva.
- **O `cortar.py` não legenda** o que recorta — o corte herda a legenda que já
  estiver queimada no vídeo de origem.
- **O Edge TTS depende do serviço da Microsoft.** É gratuito e não pede chave,
  mas é um serviço externo e pode ficar indisponível.
