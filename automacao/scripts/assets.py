"""Baixa o vídeo de fundo de cada bloco no Pexels (gratuito).

Se não houver PEXELS_API_KEY definida, gera um fundo em degradê animado no
lugar. O pipeline continua funcionando — só fica menos bonito.

    python scripts/assets.py roteiros/meu-video.md
"""

import argparse
import hashlib
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

from comum import (CACHE, FORMATOS, carregar_json, carregar_roteiro, ffmpeg,
                   pasta_saida, rodar, salvar_json)

CHAVE = os.environ.get("PEXELS_API_KEY", "").strip()
BUSCA = "https://api.pexels.com/videos/search"

# Cores dos degradês de reserva, usadas quando não há banco de imagens.
PALETA = ["0f2b75", "1a1a2e", "2d1b4e", "0d3b2e", "3b1f1f", "16324f"]


def buscar_no_pexels(termo, orientacao):
    """Devolve a URL do melhor arquivo de vídeo para o termo, ou None."""
    consulta = urllib.parse.urlencode({
        "query": termo, "orientation": orientacao, "per_page": 5, "size": "medium",
    })
    requisicao = urllib.request.Request(f"{BUSCA}?{consulta}", headers={"Authorization": CHAVE})
    try:
        with urllib.request.urlopen(requisicao, timeout=30) as resposta:
            dados = json.load(resposta)
    except Exception as erro:
        print(f"    Pexels falhou ({erro}); usando degradê")
        return None

    for video in dados.get("videos", []):
        # Prefere o menor arquivo que ainda tenha resolução suficiente.
        arquivos = sorted((a for a in video["video_files"] if (a.get("width") or 0) >= 1080),
                          key=lambda a: a["width"])
        if arquivos:
            return arquivos[0]["link"]
    return None


def baixar(url, destino):
    if destino.exists():
        return destino
    print(f"    baixando {destino.name}")
    requisicao = urllib.request.Request(url, headers={"User-Agent": "projeto-canal/1.0"})
    with urllib.request.urlopen(requisicao, timeout=120) as resposta:
        destino.write_bytes(resposta.read())
    return destino


def degrade(indice, largura, altura, segundos, destino):
    """Gera um fundo em degradê com leve movimento, sem depender de rede."""
    cor = PALETA[indice % len(PALETA)]
    rodar([
        ffmpeg(), "-y",
        "-f", "lavfi", "-i", f"color=c=0x{cor}:s={largura}x{altura}:d={segundos:.2f}:r=30",
        "-f", "lavfi", "-i", f"color=c=0x{cor}:s={largura}x{altura}:d={segundos:.2f}:r=30",
        "-filter_complex",
        # Vinheta suave + zoom lento, para o fundo não ficar completamente parado.
        f"[0:v]format=yuv420p,vignette=PI/4,"
        f"zoompan=z='min(zoom+0.0004,1.15)':d=1:s={largura}x{altura}:fps=30[v]",
        "-map", "[v]", "-t", f"{segundos:.2f}", "-c:v", "libx264", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", str(destino),
    ])
    return destino


def principal(caminho_roteiro):
    meta, _ = carregar_roteiro(caminho_roteiro)
    destino = pasta_saida(meta)
    dados = carregar_json(destino / "blocos.json")
    blocos = dados["blocos"]

    largura, altura = FORMATOS[meta["formato"]]
    orientacao = "portrait" if altura > largura else "landscape"
    CACHE.mkdir(parents=True, exist_ok=True)
    fundos = destino / "fundos"
    fundos.mkdir(exist_ok=True)

    if not CHAVE:
        print("PEXELS_API_KEY não definida — usando degradês gerados localmente.")

    for indice, bloco in enumerate(blocos):
        print(f"  bloco {indice:02d}")
        saida = fundos / f"fundo_{indice:02d}.mp4"

        if bloco.get("arquivo"):
            # Captura de tela local informada no roteiro.
            local = Path(caminho_roteiro).parent / bloco["arquivo"]
            if not local.exists():
                local = Path(bloco["arquivo"])
            if local.exists():
                bloco["fundo"] = str(local.resolve())
                print(f"    arquivo local: {local.name}")
                continue
            print(f"    arquivo {bloco['arquivo']} não encontrado; caindo para o degradê")

        url = buscar_no_pexels(bloco["busca"], orientacao) if (CHAVE and bloco.get("busca")) else None
        if url:
            nome = hashlib.sha1(url.encode()).hexdigest()[:16] + ".mp4"
            bloco["fundo"] = str(baixar(url, CACHE / nome).resolve())
        else:
            bloco["fundo"] = str(degrade(indice, largura, altura,
                                         bloco["duracao"] + 0.5, saida).resolve())

    salvar_json(destino / "blocos.json", dados)
    print(f"Fundos prontos em {fundos}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roteiro")
    principal(parser.parse_args().roteiro)
