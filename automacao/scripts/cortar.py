"""Recorta um vídeo longo em cortes verticais para TikTok, Shorts e Reels.

O vídeo horizontal vira 1080x1920 com fundo desfocado em cima e embaixo —
formato padrão de reaproveitamento, sem perder nada do enquadramento original.

    python scripts/cortar.py saida/meu-video/video.mp4 --cortes "0:15-1:25,3:40-4:55"
"""

import argparse
from pathlib import Path

from comum import FORMATOS, duracao, ffmpeg, rodar


def segundos(marca):
    """Aceita '95', '1:35' ou '1:02:30' e devolve segundos."""
    partes = [float(p) for p in marca.strip().split(":")]
    total = 0.0
    for parte in partes:
        total = total * 60 + parte
    return total


def cortar(origem, inicio, fim, destino, largura=1080, altura=1920):
    """Extrai um trecho e reenquadra em vertical com fundo desfocado."""
    filtro = (
        # Fundo: o próprio vídeo ampliado, cortado e borrado.
        f"[0:v]scale={largura}:{altura}:force_original_aspect_ratio=increase,"
        f"crop={largura}:{altura},gblur=sigma=28,eq=brightness=-0.12[fundo];"
        # Frente: o vídeo inteiro, encaixado na largura.
        f"[0:v]scale={largura}:-2:force_original_aspect_ratio=decrease[frente];"
        f"[fundo][frente]overlay=(W-w)/2:(H-h)/2,fps=30,setsar=1[v]"
    )
    rodar([
        ffmpeg(), "-y", "-ss", f"{inicio:.3f}", "-to", f"{fim:.3f}", "-i", str(origem),
        "-filter_complex", filtro, "-map", "[v]", "-map", "0:a?",
        "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(destino),
    ])
    return destino


def principal(origem, cortes, destino=None):
    origem = Path(origem)
    destino = Path(destino) if destino else origem.parent / "cortes"
    destino.mkdir(parents=True, exist_ok=True)
    total = duracao(origem)

    for indice, trecho in enumerate(cortes.split(","), start=1):
        if "-" not in trecho:
            raise SystemExit(f"Trecho inválido: {trecho!r}. Use o formato 0:15-1:25")
        inicio, fim = (segundos(p) for p in trecho.split("-", 1))
        if fim > total:
            print(f"  corte {indice}: fim {fim:.0f}s passa do vídeo ({total:.0f}s); ajustando")
            fim = total
        if inicio >= fim:
            raise SystemExit(f"Trecho inválido: {trecho!r}. O início vem depois do fim.")

        saida = destino / f"corte_{indice:02d}.mp4"
        print(f"  corte {indice}: {inicio:.0f}s a {fim:.0f}s ({fim - inicio:.0f}s)")
        if fim - inicio < 61:
            print("    AVISO: abaixo de 61s não entra no TikTok Creator Rewards")
        cortar(origem, inicio, fim, saida)

    print(f"\nCortes em {destino}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="vídeo longo de origem")
    parser.add_argument("--cortes", required=True,
                        help='trechos separados por vírgula, ex: "0:15-1:25,3:40-4:55"')
    parser.add_argument("--destino", help="pasta de saída (padrão: cortes/ ao lado do vídeo)")
    args = parser.parse_args()
    principal(args.video, args.cortes, args.destino)
