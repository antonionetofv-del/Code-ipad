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
    """Gera os textos de publicação, separados por plataforma.

    O arquivo de vídeo é o mesmo nos dois lugares (1080x1920), mas o texto não:
    o Shorts usa título curto + descrição longa e indexa por busca, enquanto o
    TikTok usa uma legenda única e curta, onde as hashtags fazem o trabalho.
    """
    meta, blocos = carregar_roteiro(caminho)
    destino = pasta_saida(meta)

    descricao = meta.get("descricao") or " ".join(b["texto"] for b in blocos[:2])
    hashtags = meta.get("hashtags", "")
    titulo_yt = meta.get("titulo_youtube", meta["titulo"])
    legenda_tt = meta.get("legenda_tiktok", meta["titulo"])
    cta = meta.get("cta", "")

    if len(titulo_yt) > 100:
        print(f"    AVISO: título do YouTube tem {len(titulo_yt)} caracteres (limite 100)")

    texto = f"""=== YOUTUBE SHORTS ===

TÍTULO ({len(titulo_yt)}/100)
{titulo_yt}

DESCRIÇÃO
{descricao}

{cta}

{hashtags} #Shorts


=== TIKTOK ===

LEGENDA ({len(legenda_tt)} caracteres — o ideal fica abaixo de 150)
{legenda_tt}

{hashtags}


=== LEMBRETES ===
- Conta do TikTok precisa ser PESSOAL para entrar no Creator Rewards
- Publique o mesmo arquivo nos dois; não republique com marca d'água
- Responda os comentários nas 2 primeiras horas
"""
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
