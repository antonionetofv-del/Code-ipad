# 08 — Automação: o que dá e o que não dá

## A restrição que define a arquitetura

Você trabalha no iPad. iPad não roda Python nem ffmpeg. Isso elimina a
abordagem óbvia — "instala essas ferramentas no computador e roda o script".

A solução: **o pipeline roda no GitHub Actions**, de graça, na nuvem. Você
escreve o roteiro num arquivo de texto, dá commit, e alguns minutos depois
baixa o vídeo pronto. Nenhum programa instalado no seu aparelho.

```
Você escreve o roteiro (texto)  →  commit no GitHub
                                        ↓
                      GitHub Actions liga uma máquina Linux
                                        ↓
              narração → fundos → montagem → legenda queimada
                                        ↓
                      vídeo.mp4 disponível para download
                                        ↓
                    você baixa no iPad e publica manualmente
```

## As 5 etapas e o que automatiza cada uma

| Etapa | Automatizável? | Como |
|---|---|---|
| 1. Pauta | Parcial | Claude sugere; você escolhe |
| 2. Roteiro | Parcial | Claude escreve com o prompt do arquivo 03; você revisa |
| 3. Narração | **Total** | Edge TTS, gratuito e ilimitado |
| 4. Legenda sincronizada | **Total** | Vem de graça junto com a narração |
| 5. Montagem | **Total** | ffmpeg: fundos, cortes, legenda queimada, trilha |
| 6. Publicação | **Não** | Manual — explico o porquê abaixo |

### A legenda é o truque mais elegante do pipeline

Quase todo mundo legenda com reconhecimento de fala (Whisper), que é pesado,
lento e erra palavra. Aqui não precisa: o Edge TTS devolve, junto com o áudio,
**o instante exato em que cada palavra é falada** (eventos `WordBoundary`).

Como a narração é sintetizada por nós, já sabemos os tempos. A legenda sai
perfeitamente sincronizada, de graça, instantânea, sem erro de transcrição.

### Por que a publicação continua manual

- **TikTok:** a API de publicação exige aprovação de aplicativo comercial. Não
  está disponível para criador individual.
- **YouTube:** a API existe e funciona, mas exige montar um projeto no Google
  Cloud, passar por verificação OAuth e guardar um token de atualização. É
  viável, e vale a pena quando você estiver publicando todo dia. Não vale no
  começo.

Além disso, subir manualmente leva 3 minutos e é onde você escreve o título e
escolhe a thumbnail — as duas coisas que mais afetam o desempenho. Automatizar
essa parte cedo demais economiza pouco e custa qualidade.

## O que NÃO automatizar (e isso é importante)

O YouTube derruba conteúdo produzido em massa sem esforço editorial. Um canal
que gera 50 vídeos por dia com o mesmo molde é exatamente o alvo da política.

O que a automação faz aqui é **tirar de você o trabalho braçal** — sintetizar
voz, cortar clipe, sincronizar legenda, encodar. O que ela **não** faz é
decidir o que dizer. Isso continua sendo seu:

| Automatize | Nunca automatize |
|---|---|
| Narração, montagem, legenda, encode | A escolha da pauta |
| Baixar fundo de banco de imagens | O ângulo e a opinião |
| Gerar título e descrição a partir do roteiro | O teste real da ferramenta |
| Recortar o vídeo longo em verticais | A resposta aos comentários |

Um roteiro que você revisou e um teste que você fez de verdade é o que separa
seu canal dos 97% que não monetizam.

## Fluxo de trabalho semanal, com a automação ligada

| Dia | Tempo | O que você faz |
|---|---|---|
| Domingo | 2h | Escolhe 7 pautas e escreve os 7 roteiros com o Claude |
| Domingo | 5 min | Commita os 7 arquivos `.md` — o Actions produz sozinho |
| Domingo | 15 min | Baixa os 7 vídeos e confere |
| Seg a sáb | 20 min/dia | Publica o do dia e responde comentários |

O gargalo deixa de ser a edição e passa a ser a **decisão do que falar** — que
é exatamente onde seu tempo deveria estar.

## Custo

| Item | Custo |
|---|---|
| GitHub Actions | Gratuito (2.000 min/mês em repositório privado) |
| Edge TTS | Gratuito e ilimitado |
| Pexels API | Gratuito |
| ffmpeg | Gratuito |
| **Total** | **R$ 0** |

Um vídeo de 60s consome de 2 a 4 minutos de Actions. Os 2.000 minutos mensais
dão para algo em torno de 500 vídeos por mês — muito além do necessário.

## Próximos passos possíveis

Quando o canal estiver rodando e o volume justificar:

1. **Upload automático no YouTube** via API (OAuth + token de atualização)
2. **Thumbnail gerada** a partir do título, com o mesmo pipeline do ffmpeg
3. **Planilha de métricas preenchida sozinha** pela YouTube Analytics API
4. **Agendamento** — o Actions produz e publica em horário fixo via `schedule`

Nenhum deles é necessário agora. O que importa nos primeiros 90 dias é publicar
todo dia, e para isso o pipeline atual já basta.
