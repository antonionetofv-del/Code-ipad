"""Roda o pipeline inteiro para um roteiro (ou para todos de uma vez).

    python scripts/produzir.py roteiros/meu-video.md
    python scripts/produzir.py --todos
"""

import argparse
import asyncio
import sys
from pathlib import Path

import assets
import montar
import narrar
from comum import RAIZ, carregar_roteiro, pasta_saida


def produzir(caminho, trilha=None):
    print(f"\n{'=' * 60}\n{Path(caminho).name}\n{'=' * 60}")
    asyncio.run(narrar.principal(caminho))
    print("\n-- fundos --")
    assets.principal(caminho)
    print("\n-- montagem --")
    return montar.principal(caminho, trilha)


def escrever_metadados(caminho):
    """Gera título, descrição e hashtags prontos para colar na plataforma."""
    meta, blocos = carregar_roteiro(caminho)
    destino = pasta_saida(meta)
    texto = "\n".join([
        meta["titulo"],
        "",
        meta.get("descricao", " ".join(b["texto"] for b in blocos[:2])),
        "",
        meta.get("hashtags", ""),
    ])
    (destino / "publicar.txt").write_text(texto, encoding="utf-8")
    print(f"Metadados: {destino / 'publicar.txt'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roteiro", nargs="?", help="caminho do roteiro .md")
    parser.add_argument("--todos", action="store_true", help="produz todos os roteiros da pasta")
    parser.add_argument("--trilha", help="mp3 de fundo")
    args = parser.parse_args()

    if args.todos:
        roteiros = sorted((RAIZ / "roteiros").glob("*.md"))
        if not roteiros:
            sys.exit("Nenhum roteiro encontrado em roteiros/")
    elif args.roteiro:
        roteiros = [Path(args.roteiro)]
    else:
        parser.error("informe um roteiro ou use --todos")

    for roteiro in roteiros:
        produzir(roteiro, args.trilha)
        escrever_metadados(roteiro)

    print(f"\n{len(roteiros)} vídeo(s) prontos em {RAIZ / 'saida'}")
