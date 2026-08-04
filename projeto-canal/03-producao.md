# 03 — Pipeline de produção (custo R$ 0)

## Stack completo, tudo gratuito

| Etapa | Ferramenta | Observação |
|---|---|---|
| Pauta e pesquisa | Claude Pro | Já disponível |
| Roteiro | Claude Pro + template do arquivo 04 | |
| Narração | **Edge TTS** | 15 vozes neurais PT-BR, ilimitado, grátis |
| Narração (alternativa) | ElevenLabs free | 10.000 caracteres/mês, qualidade superior |
| Narração (alternativa) | CapCut TTS embutido | Mais rápido, qualidade menor |
| Gravação de tela | Gravador nativo do celular / OBS Studio | OBS é gratuito e open source |
| Edição | CapCut | Gratuito, legenda automática em PT-BR |
| Imagens e vídeos | Pexels, Pixabay, Mixkit | Livres para uso comercial |
| Música | Biblioteca de Áudio do YouTube, Pixabay Music | Sempre confira a licença |
| Legenda | CapCut (automática) | Sempre revise — erra nome próprio e número |
| Thumbnail | Canva gratuito | |
| Organização | Planilha do Google | Modelo no arquivo 06 |

**Custo total mensal: R$ 0.**

### Edge TTS — a peça mais importante do stack

O Brasil tem a maior coleção de vozes neurais gratuitas de qualquer idioma
fora do inglês. São 15 vozes PT-BR, sem limite de caracteres, sem marca d'água.

Duas formas de usar:

1. **Sem instalar nada:** abra o Microsoft Edge, use a função "Ler em voz alta"
   e grave a saída de áudio do sistema.
2. **Via script (melhor qualidade, gera arquivo direto):** o pacote `edge-tts`
   roda em Python e exporta MP3.

```bash
pip install edge-tts

# Listar as vozes brasileiras disponíveis
edge-tts --list-voices | grep pt-BR

# Gerar a narração
edge-tts --voice pt-BR-AntonioNeural --file roteiro.txt --write-media narracao.mp3

# Voz feminina, um pouco mais devagar (bom para explicação)
edge-tts --voice pt-BR-FranciscaNeural --rate=-5% --file roteiro.txt --write-media narracao.mp3
```

Escolha **uma voz** e nunca mais mude. A voz é a identidade do canal — trocar
confunde quem já te conhece.

## O fluxo de 3 horas

### Produção em lote (o segredo de manter o ritmo)

Não produza um vídeo por dia. Produza **a semana inteira em dois dias** e
publique aos poucos. Quem produz diariamente desiste no dia 20.

### Domingo — 3h — Bloco de planejamento e roteiro

| Tempo | Tarefa |
|---|---|
| 30 min | Pesquisa de pauta: o que subiu no nicho essa semana, comentários do público |
| 20 min | Escolher 7 pautas e definir a série de cada uma |
| 90 min | Escrever os 7 roteiros com Claude (usando o template do arquivo 04) |
| 40 min | Revisar tudo em voz alta, cortar o que é enrolação |

### Segunda — 3h — Bloco de produção

| Tempo | Tarefa |
|---|---|
| 30 min | Gerar as 7 narrações no Edge TTS |
| 60 min | Gravar as telas e capturas necessárias |
| 60 min | Editar os 7 vídeos no CapCut (mesmo template, só troca conteúdo) |
| 30 min | Thumbnails, títulos, descrições e hashtags |

### Terça a sábado — 20 a 30 min/dia — Bloco de distribuição

| Tempo | Tarefa |
|---|---|
| 5 min | Publicar o vídeo do dia nas duas plataformas |
| 15 min | **Responder todos os comentários** — isso é algoritmo puro |
| 10 min | Anotar as métricas do vídeo de 48h atrás na planilha |

Responder comentário nas primeiras 2 horas é o empurrão mais barato que existe.
Não pule.

## Especificação técnica dos vídeos

### Vídeo curto (TikTok, Shorts, Reels)

| Item | Valor |
|---|---|
| Formato | 1080 × 1920, vertical |
| Duração | **61 a 90 segundos** |
| Legenda | Queimada no vídeo, sempre |
| Gancho | Primeiros 2 segundos definem tudo |
| Corte | Troca de imagem a cada 2–3 segundos |

> **Por que 61 segundos e não 30?** O TikTok Creator Rewards só considera
> vídeos **acima de 1 minuto**. Fazer curto de 40s é jogar fora a monetização
> antes mesmo de destravá-la. Nunca publique curto com menos de 61 segundos.

### Vídeo longo (YouTube)

| Item | Valor |
|---|---|
| Formato | 1920 × 1080, horizontal |
| Duração | 8 a 12 minutos |
| Frequência | 1 por semana, a partir da semana 3 |
| Função | Gerar as 4.000 horas de exibição — Shorts não gera |
| Estrutura | Gancho 15s → promessa → 3 a 5 blocos → recapitulação → CTA |

O vídeo longo é o que paga. O curto é o que traz gente. Você precisa dos dois.

## Reaproveitamento — 1 gravação, 6 publicações

Cada vídeo longo vira:

1. O próprio vídeo no YouTube
2. 3 cortes verticais (um por bloco) → TikTok, Shorts e Reels
3. 1 carrossel de imagens → Instagram
4. 1 post de texto → comunidade do YouTube

Você grava uma vez e publica seis. É assim que 3h/dia viram presença diária em
três plataformas.

## Prompt de roteiro para o Claude

Cole isso e troque o que está entre colchetes:

```
Você é roteirista de um canal faceless em português do Brasil chamado
[NOME DO CANAL]. O canal ensina pessoas que NÃO são da área de tecnologia
a usar IA para resolver tarefas chatas do dia a dia.

Público: 28 a 55 anos, autônomo ou de empresa pequena, usa mais o celular
que o computador, tem pouca paciência com termo técnico.

Escreva um roteiro de vídeo vertical de 75 segundos sobre:
[TEMA]

Regras obrigatórias:
- Gancho nos primeiros 2 segundos que mostre a DOR, não a solução
- Português falado, frase curta, zero jargão técnico
- Um único assunto do começo ao fim, sem desvio
- Mostrar o passo a passo concreto, não falar de forma abstrata
- Terminar com uma pergunta que gere comentário
- Marcar as indicações de imagem entre colchetes a cada 3 segundos
- Máximo de 190 palavras (é o que cabe em 75 segundos de narração)

Formato de saída: tabela com colunas Tempo | Narração | Imagem na tela
```

## Regras de qualidade que evitam desmonetização

O YouTube derruba conteúdo repetitivo e produzido em massa. Para não cair nessa:

- **Sempre acrescente sua análise.** Não leia notícia — teste, mostre a tela, dê veredito.
- **Nunca reposte vídeo de terceiro** sem transformação significativa.
- **Não use a mesma estrutura de roteiro palavra por palavra** em todos os vídeos.
- **Imagem de banco é permitida**, mas o valor tem que estar na narração e na edição.
- **Voz de IA é permitida.** O que não é permitido é conteúdo sem esforço editorial.
