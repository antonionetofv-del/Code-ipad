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
        grupo = palavras[indice:indice + PALAVRAS_POR_LEGENDA]
        texto = " ".join(p["texto"] for p in grupo).strip()
        if not texto:
            continue
        # O respiro de 10ms evita dois cues ativos no mesmo quadro — quando
        # isso acontece o libass empilha um em cima do outro.
        fim = max(grupo[-1]["fim"] - 0.01, grupo[0]["inicio"] + 0.05)
        linhas.append(f"Dialogue: 0,{marcador(grupo[0]['inicio'])},{marcador(fim)},"
                      f"Legenda,,0,0,0,,{texto.upper()}")

    Path(destino).write_text("\n".join(linhas) + "\n", encoding="utf-8")


async def principal(caminho_roteiro):
    meta, blocos = carregar_roteiro(caminho_roteiro)
    destino = pasta_saida(meta)
    audios = destino / "audio"
    audios.mkdir(exist_ok=True)

    print(f"Narrando {len(blocos)} blocos com a voz {meta['voz']}")

    deslocamento = 0.0
    todas_palavras = []
    for indice, bloco in enumerate(blocos):
        arquivo = audios / f"bloco_{indice:02d}.mp3"
        palavras = await sintetizar(bloco["texto"], meta["voz"], meta["ritmo"], arquivo)

        bloco["audio"] = str(arquivo.relative_to(destino))
        bloco["duracao"] = duracao(arquivo)
        for palavra in palavras:
            palavra["inicio"] += deslocamento
            palavra["fim"] += deslocamento
        todas_palavras.extend(palavras)
        deslocamento += bloco["duracao"]

        print(f"  bloco {indice:02d}  {bloco['duracao']:5.1f}s  {bloco['texto'][:50]}...")

    # Junta os blocos numa narração única.
    lista = audios / "lista.txt"
    lista.write_text("".join(f"file '{Path(b['audio']).name}'\n" for b in blocos), encoding="utf-8")
    rodar([ffmpeg(), "-y", "-f", "concat", "-safe", "0", "-i", "lista.txt",
           "-c", "copy", "../narracao.mp3"], cwd=audios)

    montar_ass(todas_palavras, meta["formato"], destino / "legendas.ass")
    salvar_json(destino / "blocos.json", {"meta": meta, "blocos": blocos})

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
