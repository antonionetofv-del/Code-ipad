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

[busca: small business owner stressed with paperwork at desk]
Se você ainda digita nota fiscal numa planilha, para tudo.

[arquivo: minha-captura-de-tela.mp4]
Esse bloco usa um vídeo local em vez do banco de imagens.
```

Os roteiros já produzidos ficam em `roteiros-semana1/`. O `--todos` só varre
`roteiros/`, então arquivar a semana anterior evita reproduzir tudo de novo.

- Cada parágrafo é **um bloco**: uma frase narrada e um fundo próprio
- `[busca: ...]` é o termo procurado no Pexels — **escreva em inglês**, o acervo
  responde muito melhor
- `[arquivo: ...]` usa um vídeo seu (captura de tela, por exemplo)
- **Varie o termo do bloco de CTA entre os roteiros.** Todos terminam com
  "comenta aí", e repetir `person reading comments on smartphone` em sete
  roteiros esgota os resultados: o último bloco é justamente o que mais cai no
  degradê. Use ângulos diferentes — pessoa rindo do celular, grupo de amigos
  vendo a tela, mão digitando resposta
- Sem chave do Pexels não há filmagem: o pipeline cai para degradê e continua rodando

### Campos do cabeçalho

| Campo | Padrão | Observação |
|---|---|---|
| `titulo` | nome do arquivo | Vira o nome da pasta de saída |
| `voz` | `pt-BR-AntonioNeural` | Escolha uma e nunca mais mude |
| `ritmo` | `+8%` | Ritmo aprovado do canal. `+12%` acelera mais, `+5%` acalma |
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
| `narrar.py` | Roteiro → narração `.mp3` + legenda `.ass` animada |
| `assets.py` | Busca a filmagem no Pexels (ou gera degradê no clima do bloco) |
| `sons.py` | Sintetiza os efeitos e monta a trilha de transições |
| `montar.py` | Junta tudo em `video.mp4` |
| `cortar.py` | Recorta um vídeo longo em verticais com fundo desfocado |
| `comum.py` | Leitura do roteiro e utilidades compartilhadas |

## As quatro camadas do vídeo

**1. Filmagem real de pessoas.** Cada bloco puxa um clipe do Pexels a partir do
seu `[busca:]`. **A chave do Pexels é obrigatória para esse formato** — sem ela
não existe pessoa nenhuma, só degradê.

Como não há lip-sync, os termos de busca são escritos de propósito para plano
médio, mãos e over-the-shoulder, nunca para close de rosto falando: rosto em
close com a boca fora de sincronia é a coisa que mais denuncia um vídeo montado.
O mesmo clipe nunca se repete dentro de um vídeo, e clipes com menos de 5
segundos são descartados porque ficariam em loop visível.

O acervo vertical do Pexels é bem menor que o horizontal, então quando a busca
em retrato rende pouco, a busca é refeita sem restrição de orientação — o
recorte para o canvas acontece de qualquer forma na montagem.

**2. Legenda viva e legível.** O grupo de 3 palavras fica na tela e só a palavra
sendo falada acende em amarelo. Atrás dela vai uma faixa escura em degradê: sem
isso, legenda branca some sobre parede clara, céu ou monitor aceso.

**3. Coerência visual.** Todo clipe passa pela mesma correção de cor. Filmagem
de banco vem de câmeras e tratamentos diferentes; sem uma passada comum, um
vídeo com oito clipes parece oito vídeos colados. Quando não há filmagem, o
degradê de reserva muda de família de cor conforme o que o texto diz: vermelho
em alerta, verde em resultado positivo, roxo em instrução, azul em explicação —
`assets.py` tem a tabela de pistas e aceita `[clima: alerta]` para forçar.

**4. Movimento e som.** Cada bloco tem deriva lenta de câmera, com a direção
alternada para o vídeo não parecer deslizar sempre para o mesmo lado, e cada
corte leva um whoosh sintetizado pelo próprio ffmpeg — sem arquivo baixado, sem
dúvida de licença. O áudio final é normalizado em **-14 LUFS**, que é o alvo do
TikTok e do YouTube: sem isso cada vídeo sobe num nível diferente e o canal soa
irregular.

### Recortar um vídeo longo

```bash
python scripts/cortar.py saida/meu-video/video.mp4 --cortes "0:15-1:25,3:40-4:55"
```

Cada trecho vira um 1080x1920 com o vídeo original centralizado e fundo
desfocado. É assim que 1 vídeo longo vira 3 curtos.

## Chave do Pexels (obrigatória)

**Sem ela não existe filmagem de pessoa nenhuma** — o vídeo sai só com degradê.

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

**O silêncio das pontas é aparado em cada bloco.** O TTS devolve cada fala com
silêncio antes e depois; emendar onze blocos empilharia onze desses silêncios, e
é isso que faz um vídeo parecer arrastado mesmo com o texto bom. O corte usa a
própria marcação de palavra — a primeira começa onde a fala começa — então não
precisa de detector de silêncio, e as legendas são deslocadas junto. No lugar
entra um respiro fixo e curto de 0,12s.

**Ritmo `+8%` com pausas aparadas encurta o vídeo em torno de 15%.** Se você
acelerar sem acrescentar texto, o curto cai abaixo dos 61 segundos e perde o
Creator Rewards. A conta prática: cerca de 2,9 palavras por segundo no ritmo
`+8%`, mais 0,12s por bloco.

**Curtos abaixo de 61 segundos disparam aviso.** O TikTok Creator Rewards só
considera vídeos acima de 1 minuto.

**As chamadas ao Pexels mandam um `User-Agent` de verdade.** Sem ele o urllib
se identifica como `Python-urllib/3.x` e o WAF na frente da API recusa tudo com
**403**. É uma pegadinha cruel porque 403 parece chave inválida — mas chave
inválida devolve **401**. Se um dia voltar a dar 403 com a chave certa, olhe o
cabeçalho antes de trocar a credencial.

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
