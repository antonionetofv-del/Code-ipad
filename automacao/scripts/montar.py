"""Monta o vídeo final: fundos + narração + legenda queimada + trilha.

    python scripts/montar.py roteiros/meu-video.md
"""

import argparse
from pathlib import Path

from comum import (FORMATOS, RAIZ, carregar_json, carregar_roteiro, duracao,
                   ffmpeg, pasta_saida, rodar)

VOLUME_TRILHA = 0.07


def normalizar(origem, largura, altura, segundos, destino):
    """Recorta e ajusta um fundo para o canvas e a duração exatos do bloco."""
    rodar([
        ffmpeg(), "-y",
        # Repete o clipe se ele for mais curto que a narração do bloco.
        "-stream_loop", "-1", "-i", str(origem),
        "-t", f"{segundos:.3f}",
        "-vf", (f"scale={largura}:{altura}:force_original_aspect_ratio=increase,"
                f"crop={largura}:{altura},fps=30,setsar=1"),
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-pix_fmt", "yuv420p", str(destino),
    ])
    return destino


def principal(caminho_roteiro, trilha=None):
    meta, _ = carregar_roteiro(caminho_roteiro)
    destino = pasta_saida(meta)
    blocos = carregar_json(destino / "blocos.json")["blocos"]
    largura, altura = FORMATOS[meta["formato"]]

    partes = destino / "partes"
    partes.mkdir(exist_ok=True)

    print(f"Normalizando {len(blocos)} blocos para {largura}x{altura}")
    for indice, bloco in enumerate(blocos):
        normalizar(bloco["fundo"], largura, altura, bloco["duracao"],
                   partes / f"parte_{indice:02d}.mp4")

    lista = partes / "lista.txt"
    lista.write_text("".join(f"file 'parte_{i:02d}.mp4'\n" for i in range(len(blocos))),
                     encoding="utf-8")
    rodar([ffmpeg(), "-y", "-f", "concat", "-safe", "0", "-i", "lista.txt",
           "-c", "copy", "../video_mudo.mp4"], cwd=partes)

    narracao = destino / "narracao.mp3"
    legendas = destino / "legendas.ass"
    final = destino / "video.mp4"

    entradas = [ffmpeg(), "-y", "-i", str(destino / "video_mudo.mp4"), "-i", str(narracao)]
    # O caminho da legenda é escapado porque vai dentro do grafo de filtros.
    # O estilo já vem no cabeçalho do .ass, com PlayRes igual ao canvas.
    escapado = str(legendas).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
    filtro = f"[0:v]ass='{escapado}'[v]"

    if trilha and Path(trilha).exists():
        print(f"Aplicando trilha: {Path(trilha).name}")
        entradas += ["-stream_loop", "-1", "-i", str(trilha)]
        filtro += (f";[2:a]volume={VOLUME_TRILHA}[t];"
                   f"[1:a][t]amix=inputs=2:duration=first:dropout_transition=0[a]")
        mapa_audio = "[a]"
    else:
        mapa_audio = "1:a"

    rodar(entradas + [
        "-filter_complex", filtro,
        "-map", "[v]", "-map", mapa_audio,
        "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
        str(final),
    ])

    print(f"\nPronto: {final}")
    print(f"Duração: {duracao(final):.1f}s")
    return final


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roteiro")
    parser.add_argument("--trilha", help="mp3 de fundo (pasta trilhas/)")
    args = parser.parse_args()
    principal(args.roteiro, args.trilha)
