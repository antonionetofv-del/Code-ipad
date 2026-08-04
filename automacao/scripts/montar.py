"""Monta o vídeo final: fundos com movimento, personagem, legenda e som.

    python scripts/montar.py roteiros/meu-video.md
"""

import argparse
from pathlib import Path

from comum import (FORMATOS, carregar_json, carregar_roteiro, duracao,
                   ffmpeg, pasta_saida, rodar)

VOLUME_TRILHA = 0.07

# O personagem fica no alto e à esquerda: longe da legenda (que vive embaixo)
# e longe da coluna de botões do TikTok (que fica à direita).
PERSONAGEM_LADO = 0.44      # fração da largura do canvas
PERSONAGEM_X = 0.035
PERSONAGEM_Y = 0.07
BALANCO = 9                 # amplitude da "respiração", em pixels

# Quanto o fundo é ampliado antes do corte, para sobrar margem de movimento.
AMPLIACAO = 1.14


def movimento(indice, largura, altura):
    """Expressões de corte que fazem a câmera derivar devagar sobre o fundo.

    Alternar a direção por bloco evita que o vídeo inteiro pareça deslizar
    para o mesmo lado. É mais barato que `zoompan`, que reescala quadro a
    quadro e domina o tempo de processamento.
    """
    folga_x = (largura * AMPLIACAO - largura) / 2
    folga_y = (altura * AMPLIACAO - altura) / 2
    # Quatro combinações de direção, revezadas conforme o índice do bloco.
    sx, sy = [(1, 1), (-1, 1), (1, -1), (-1, -1)][indice % 4]
    x = f"{folga_x:.1f}+{sx * folga_x * 0.75:.1f}*sin(t*0.22)"
    y = f"{folga_y:.1f}+{sy * folga_y * 0.75:.1f}*sin(t*0.17)"
    return x, y


def normalizar(origem, indice, largura, altura, segundos, destino):
    """Recorta o fundo para o canvas e a duração do bloco, com deriva de câmera."""
    x, y = movimento(indice, largura, altura)
    alvo_l, alvo_a = int(largura * AMPLIACAO), int(altura * AMPLIACAO)
    rodar([
        ffmpeg(), "-y",
        # Repete o clipe se ele for mais curto que a narração do bloco.
        "-stream_loop", "-1", "-i", str(origem),
        "-t", f"{segundos:.3f}",
        "-vf", (f"scale={alvo_l}:{alvo_a}:force_original_aspect_ratio=increase,"
                f"crop={largura}:{altura}:x='{x}':y='{y}',fps=30,setsar=1"),
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-pix_fmt", "yuv420p", str(destino),
    ])
    return destino


def principal(caminho_roteiro, trilha=None):
    meta, _ = carregar_roteiro(caminho_roteiro)
    destino = pasta_saida(meta)
    dados = carregar_json(destino / "blocos.json")
    blocos = dados["blocos"]
    largura, altura = FORMATOS[meta["formato"]]

    partes = destino / "partes"
    partes.mkdir(exist_ok=True)

    print(f"Normalizando {len(blocos)} blocos para {largura}x{altura}")
    for indice, bloco in enumerate(blocos):
        normalizar(bloco["fundo"], indice, largura, altura, bloco["duracao"],
                   partes / f"parte_{indice:02d}.mp4")

    lista = partes / "lista.txt"
    lista.write_text("".join(f"file 'parte_{i:02d}.mp4'\n" for i in range(len(blocos))),
                     encoding="utf-8")
    rodar([ffmpeg(), "-y", "-f", "concat", "-safe", "0", "-i", "lista.txt",
           "-c", "copy", "../video_mudo.mp4"], cwd=partes)

    legendas = destino / "legendas.ass"
    final = destino / "video.mp4"
    personagem = destino / "personagem.mov"
    efeitos = destino / "efeitos.wav"

    entradas = [ffmpeg(), "-y", "-i", str(destino / "video_mudo.mp4")]
    filtros = []
    fluxo = "[0:v]"
    proxima = 1

    if personagem.exists():
        lado = int(largura * PERSONAGEM_LADO)
        entradas += ["-i", str(personagem)]
        filtros.append(f"[{proxima}:v]scale={lado}:{lado},format=rgba[ch]")
        filtros.append(
            f"{fluxo}[ch]overlay=x={int(largura * PERSONAGEM_X)}"
            f":y='{int(altura * PERSONAGEM_Y)}+sin(t*2.1)*{BALANCO}'"
            f":eof_action=pass[comp]"
        )
        fluxo = "[comp]"
        proxima += 1
        print("  personagem sobreposto")

    entradas += ["-i", str(destino / "narracao.mp3")]
    indice_narracao = proxima
    proxima += 1

    audios = [f"[{indice_narracao}:a]"]
    if trilha and Path(trilha).exists():
        entradas += ["-stream_loop", "-1", "-i", str(trilha)]
        filtros.append(f"[{proxima}:a]volume={VOLUME_TRILHA}[trilha]")
        audios.append("[trilha]")
        proxima += 1
        print(f"  trilha: {Path(trilha).name}")

    if efeitos.exists():
        entradas += ["-i", str(efeitos)]
        audios.append(f"[{proxima}:a]")
        proxima += 1
        print("  efeitos de transição")

    # O caminho da legenda é escapado porque vai dentro do grafo de filtros.
    # O estilo já vem no cabeçalho do .ass, com PlayRes igual ao canvas.
    escapado = str(legendas).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
    filtros.append(f"{fluxo}ass='{escapado}'[v]")

    if len(audios) == 1:
        mistura = audios[0]
    else:
        # normalize=0 mantém a narração no volume cheio: sem isso o `amix`
        # divide o nível pelo número de entradas e a voz some.
        filtros.append("".join(audios) +
                       f"amix=inputs={len(audios)}:duration=first:normalize=0[mix]")
        mistura = "[mix]"

    # TikTok e YouTube normalizam o áudio na entrega. Se cada vídeo sobe num
    # nível diferente, a plataforma corrige de um jeito diferente e o canal
    # soa irregular. Entregar já em -14 LUFS evita isso.
    filtros.append(f"{mistura}loudnorm=I=-14:TP=-1.5:LRA=11[a]")

    rodar(entradas + [
        "-filter_complex", ";".join(filtros),
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "44100",
        "-shortest", "-movflags", "+faststart",
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
