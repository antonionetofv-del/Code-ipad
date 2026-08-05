"""Gera a narração e a legenda sincronizada a partir de um roteiro.

Usa o Edge TTS (gratuito, ilimitado, 15 vozes neurais em pt-BR). Os tempos das
legendas vêm dos eventos WordBoundary do próprio serviço, então a sincronia é
exata e não precisa de reconhecimento de fala.

    python scripts/narrar.py roteiros/meu-video.md
"""

import argparse
import asyncio
from pathlib import Path

import edge_tts

from comum import (FORMATOS, carregar_roteiro, duracao, ffmpeg, pasta_saida,
                   rodar, salvar_json)

# Quantas palavras cabem confortavelmente numa linha de legenda queimada.
PALAVRAS_POR_LEGENDA = 3

# Sobra deixada antes da primeira palavra e depois da última, ao aparar o
# silêncio do bloco. Zero cortaria a consoante inicial e o final da frase.
MARGEM_INICIO = 0.06
MARGEM_FIM = 0.18

# Respiro entre blocos. O TTS já devolve cada fala com silêncio nas pontas, e
# emendar nove blocos empilha nove desses silêncios — é isso que faz o vídeo
# parecer arrastado. Aparamos tudo e devolvemos um respiro curto e igual.
PAUSA_ENTRE_BLOCOS = 0.12

# Cabeçalho ASS. Escrevemos .ass em vez de .srt porque o libass assume uma tela
# de 384x288 para legenda SRT — corpo de fonte e margem sairiam na escala errada.
# Com PlayResX/PlayResY explícitos, os valores abaixo são pixels reais.
CABECALHO_ASS = """[Script Info]
ScriptType: v4.00+
PlayResX: {largura}
PlayResY: {altura}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Legenda,DejaVu Sans,{corpo},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,{contorno},0,2,{margem_lado},{margem_lado},{margem_baixo},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# Amarelo da identidade (#FFC700). No ASS a cor vai em BGR, não em RGB.
DESTAQUE = r"{\c&H00C7FF&}"
NORMAL = r"{\c&HFFFFFF&}"


async def sintetizar(texto, voz, ritmo, destino):
    """Sintetiza um bloco e devolve as marcações de palavra (em segundos)."""
    comunicacao = edge_tts.Communicate(texto, voz, rate=ritmo, boundary="WordBoundary")
    palavras = []
    with open(destino, "wb") as saida:
        async for pedaco in comunicacao.stream():
            if pedaco["type"] == "audio":
                saida.write(pedaco["data"])
            elif pedaco["type"] == "WordBoundary":
                # Os offsets vêm em unidades de 100 nanossegundos.
                palavras.append({
                    "inicio": pedaco["offset"] / 1e7,
                    "fim": (pedaco["offset"] + pedaco["duration"]) / 1e7,
                    "texto": pedaco["text"],
                })
    if destino.stat().st_size == 0:
        raise RuntimeError(f"O Edge TTS devolveu áudio vazio para: {texto[:60]!r}")
    return palavras


def marcador(segundos):
    """Timestamp no formato do ASS: H:MM:SS.cc (centésimos)."""
    horas, resto = divmod(max(segundos, 0), 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{int(horas)}:{int(minutos):02d}:{segundos:05.2f}"


def montar_ass(palavras, formato, destino):
    """Agrupa palavras em legendas curtas e escreve o arquivo .ass."""
    largura, altura = FORMATOS[formato]
    corpo = round(altura * 0.034)
    linhas = [CABECALHO_ASS.format(
        largura=largura, altura=altura, corpo=corpo,
        contorno=max(3, round(corpo / 14)),
        margem_lado=round(largura * 0.07),
        # 18% da altura mantém a legenda acima da faixa de botões do TikTok.
        margem_baixo=round(altura * 0.18),
    )]

    for indice in range(0, len(palavras), PALAVRAS_POR_LEGENDA):
        grupo = [p for p in palavras[indice:indice + PALAVRAS_POR_LEGENDA] if p["texto"].strip()]
        if not grupo:
            continue

        # Uma linha por palavra: o grupo inteiro fica na tela e só a palavra
        # que está sendo falada acende em amarelo. É o que dá a sensação de
        # legenda viva, e sai de graça porque já temos o tempo de cada palavra.
        for posicao, palavra in enumerate(grupo):
            texto = " ".join(
                (DESTAQUE + p["texto"].upper() + NORMAL) if i == posicao else p["texto"].upper()
                for i, p in enumerate(grupo)
            )
            # O respiro de 10ms evita dois cues ativos no mesmo quadro — quando
            # isso acontece o libass empilha um em cima do outro.
            fim = max(palavra["fim"] - 0.01, palavra["inicio"] + 0.04)
            linhas.append(f"Dialogue: 0,{marcador(palavra['inicio'])},{marcador(fim)},"
                          f"Legenda,,0,0,0,,{NORMAL}{texto}")

    Path(destino).write_text("\n".join(linhas) + "\n", encoding="utf-8")


async def principal(caminho_roteiro):
    meta, blocos = carregar_roteiro(caminho_roteiro)
    destino = pasta_saida(meta)
    audios = destino / "audio"
    audios.mkdir(exist_ok=True)

    print(f"Narrando {len(blocos)} blocos com a voz {meta['voz']}")

    deslocamento = 0.0
    todas_palavras = []
    aparado_total = 0.0
    for indice, bloco in enumerate(blocos):
        bruto = audios / f"bruto_{indice:02d}.mp3"
        arquivo = audios / f"bloco_{indice:02d}.mp3"
        palavras = await sintetizar(bloco["texto"], meta["voz"], meta["ritmo"], bruto)

        # Apara o silêncio das pontas usando a própria marcação de palavra:
        # a primeira começa onde a fala começa, a última termina onde ela
        # acaba. Não precisa de detector de silêncio.
        recorte = max(0.0, palavras[0]["inicio"] - MARGEM_INICIO)
        fim_fala = palavras[-1]["fim"] + MARGEM_FIM
        rodar([ffmpeg(), "-y", "-i", str(bruto),
               "-af", (f"atrim=start={recorte:.3f}:end={fim_fala:.3f},"
                       f"asetpts=PTS-STARTPTS,apad=pad_dur={PAUSA_ENTRE_BLOCOS}"),
               "-c:a", "libmp3lame", "-b:a", "128k", str(arquivo)])
        aparado_total += recorte + max(0.0, duracao(bruto) - fim_fala)
        bruto.unlink()

        bloco["audio"] = str(arquivo.relative_to(destino))
        bloco["duracao"] = duracao(arquivo)
        for palavra in palavras:
            palavra["inicio"] += deslocamento - recorte
            palavra["fim"] += deslocamento - recorte
        todas_palavras.extend(palavras)
        deslocamento += bloco["duracao"]

        print(f"  bloco {indice:02d}  {bloco['duracao']:5.1f}s  {bloco['texto'][:50]}...")

    print(f"  {aparado_total:.1f}s de silêncio aparado das pontas")

    # Junta os blocos numa narração única.
    lista = audios / "lista.txt"
    lista.write_text("".join(f"file '{Path(b['audio']).name}'\n" for b in blocos), encoding="utf-8")
    rodar([ffmpeg(), "-y", "-f", "concat", "-safe", "0", "-i", "lista.txt",
           "-c", "copy", "../narracao.mp3"], cwd=audios)

    montar_ass(todas_palavras, meta["formato"], destino / "legendas.ass")
    # As marcações de palavra também alimentam o lip-sync do personagem.
    salvar_json(destino / "blocos.json",
                {"meta": meta, "blocos": blocos, "palavras": todas_palavras})

    print(f"\nNarração: {deslocamento:.1f}s no total")
    if meta["formato"] == "vertical" and deslocamento < 61:
        print("  AVISO: menos de 61s. Vídeos curtos abaixo de 1 minuto não entram "
              "no TikTok Creator Rewards. Alongue o roteiro.")
    print(f"Saída em {destino}")
    return destino


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roteiro", help="caminho do arquivo .md do roteiro")
    asyncio.run(principal(parser.parse_args().roteiro))
