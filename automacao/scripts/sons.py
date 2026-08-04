"""Gera os efeitos sonoros e monta a trilha de efeitos do vídeo.

Os sons são sintetizados pelo próprio ffmpeg — nada é baixado. Isso evita
qualquer dúvida de licença, que é o problema número um de canal que usa
biblioteca de efeito achada na internet.

    python scripts/sons.py roteiros/meu-video.md
"""

import argparse
from pathlib import Path

from comum import CACHE, carregar_json, carregar_roteiro, ffmpeg, pasta_saida, rodar

VOLUME_EFEITO = 0.22


def whoosh(destino, duracao=0.42):
    """Transição: ruído filtrado com envelope rápido. Marca o corte sem cansar."""
    rodar([
        ffmpeg(), "-y",
        "-f", "lavfi", "-i", f"anoisesrc=d={duracao}:c=pink:a=0.9:r=44100",
        "-af", (f"highpass=f=380,lowpass=f=5200,"
                f"afade=t=in:st=0:d=0.06,afade=t=out:st=0.10:d={duracao - 0.10:.2f},"
                f"volume=1.4"),
        "-ac", "2", str(destino),
    ])
    return destino


def pop(destino, duracao=0.14):
    """Acento curto, para o primeiro quadro e para momentos de ênfase."""
    rodar([
        ffmpeg(), "-y",
        "-f", "lavfi", "-i", f"sine=frequency=760:duration={duracao}:sample_rate=44100",
        "-af", (f"afade=t=out:st=0.02:d={duracao - 0.02:.2f},"
                f"aecho=0.7:0.6:22:0.3,volume=0.7"),
        "-ac", "2", str(destino),
    ])
    return destino


def trilha_de_efeitos(marcas, duracao_total, destino):
    """Posiciona um whoosh em cada corte e devolve uma faixa única.

    Cada efeito entra como uma entrada atrasada e todas são somadas. Como
    `amix` divide o volume pelo número de entradas, usamos normalize=0 para
    manter o nível de cada efeito.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    som = CACHE / "whoosh.wav"
    if not som.exists():
        whoosh(som)

    if not marcas:
        return None

    entradas, filtros, rotulos = [], [], []
    for indice, instante in enumerate(marcas):
        entradas += ["-i", str(som)]
        atraso = max(0, int(instante * 1000))
        filtros.append(f"[{indice}:a]adelay={atraso}|{atraso},volume={VOLUME_EFEITO}[e{indice}]")
        rotulos.append(f"[e{indice}]")

    if len(rotulos) == 1:
        grafo = filtros[0] + f";{rotulos[0]}apad[saida]"
    else:
        grafo = (";".join(filtros) + ";" + "".join(rotulos) +
                 f"amix=inputs={len(rotulos)}:normalize=0[saida]")

    rodar([ffmpeg(), "-y"] + entradas + [
        "-filter_complex", grafo, "-map", "[saida]",
        "-t", f"{duracao_total:.3f}", "-ac", "2", "-ar", "44100", str(destino),
    ])
    return destino


def principal(caminho_roteiro):
    meta, _ = carregar_roteiro(caminho_roteiro)
    destino = pasta_saida(meta)
    dados = carregar_json(destino / "blocos.json")
    blocos = dados["blocos"]

    # Um whoosh no início de cada bloco a partir do segundo — ou seja, no corte.
    marcas, acumulado = [], 0.0
    for bloco in blocos[:-1]:
        acumulado += bloco["duracao"]
        marcas.append(acumulado)

    total = sum(b["duracao"] for b in blocos)
    saida = trilha_de_efeitos(marcas, total, destino / "efeitos.wav")
    if saida:
        dados["efeitos"] = str(saida)
        from comum import salvar_json
        salvar_json(destino / "blocos.json", dados)
        print(f"  {len(marcas)} efeitos de transição em {saida.name}")
    return saida


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roteiro")
    principal(parser.parse_args().roteiro)
