"""Baixa o vídeo de fundo de cada bloco no Pexels (gratuito).

Se não houver PEXELS_API_KEY definida, gera um fundo em degradê animado no
lugar. O pipeline continua funcionando — só fica menos bonito.

    python scripts/assets.py roteiros/meu-video.md
"""

import argparse
import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from comum import (CACHE, FORMATOS, carregar_json, carregar_roteiro, ffmpeg,
                   pasta_saida, rodar, salvar_json)

CHAVE = os.environ.get("PEXELS_API_KEY", "").strip()
BUSCA = "https://api.pexels.com/videos/search"

# Paletas dos degradês de reserva, por clima. O fundo acompanha o que o bloco
# está dizendo em vez de trocar de cor a esmo.
CLIMAS = {
    "alerta": ["4a1220", "3b1f1f", "4d1a0d"],     # aviso, erro, risco
    "positivo": ["0d3b2e", "134d3a", "16404a"],   # resolvido, economia, ganho
    "destaque": ["2d1b4e", "3a2260", "241a52"],   # passo a passo, instrução
    "neutro": ["0f2b75", "16324f", "1a1a2e"],     # explicação, contexto
}

# Palavras que denunciam o clima do bloco. A ordem importa: o primeiro clima
# que casar vence, e "alerta" vem antes porque é o mais específico.
#
# O sufixo "*" marca radical (casa qualquer terminação); sem ele a pista só
# casa como palavra inteira. Isso não é preciosismo: "mente" como substring
# casaria dentro de "exatamente", "realmente" e "novamente", e pintaria de
# vermelho metade dos blocos explicativos.
PISTAS = [
    ("alerta", ("nunca", "cuidado", "erro", "erros", "mente", "golpe", "golpes",
                "risco", "riscos", "perigo", "desconfie", "problema",
                "confidencial", "senha", "senhas", "perdeu", "invent*")),
    ("positivo", ("pronto", "pronta", "economiz*", "resolvid*", "ganha", "sobra",
                  "organizad*", "funciona", "volta")),
    ("destaque", ("passo", "primeira", "segunda", "terceira", "quarta", "quinta",
                  "peça", "escreve", "manda", "liste")),
]

_REGEX = {
    clima: re.compile(
        "|".join(rf"\b{re.escape(p[:-1])}\w*" if p.endswith("*") else rf"\b{re.escape(p)}\b"
                 for p in pistas)
    )
    for clima, pistas in PISTAS
}


def detectar_clima(texto):
    """Escolhe o clima do bloco a partir do que o texto diz."""
    minusculo = texto.lower()
    for clima, _ in PISTAS:
        if _REGEX[clima].search(minusculo):
            return clima
    return "neutro"


def _consultar(termo, orientacao):
    parametros = {"query": termo, "per_page": 12, "size": "medium"}
    if orientacao:
        parametros["orientation"] = orientacao
    requisicao = urllib.request.Request(f"{BUSCA}?{urllib.parse.urlencode(parametros)}",
                                        headers={"Authorization": CHAVE})
    try:
        with urllib.request.urlopen(requisicao, timeout=30) as resposta:
            return json.load(resposta).get("videos", [])
    except urllib.error.HTTPError as erro:
        # 401/403 é a chave sendo recusada, não falta de resultado. Insistir só
        # gasta minutos de máquina para entregar vídeos sem filmagem nenhuma,
        # então paramos na primeira ocorrência.
        if erro.code in (401, 403):
            raise SystemExit(
                f"\n  {'!' * 66}\n"
                f"  O Pexels RECUSOU a chave (HTTP {erro.code}).\n"
                f"  O secret existe e chegou até aqui, mas o valor não é aceito.\n"
                f"  Causas usuais: a chave foi copiada com espaço ou incompleta,\n"
                f"  ou foi gerada uma chave nova (o que invalida a anterior).\n"
                f"  Confira em pexels.com/api e salve de novo em\n"
                f"  Settings -> Secrets and variables -> Actions -> PEXELS_API_KEY\n"
                f"  {'!' * 66}"
            )
        if erro.code == 429:
            print("    Pexels: limite de requisições atingido; usando degradê")
        else:
            print(f"    Pexels falhou (HTTP {erro.code})")
        return []
    except Exception as erro:
        print(f"    Pexels falhou ({erro})")
        return []


def buscar_no_pexels(termo, orientacao, usados):
    """Melhor arquivo de vídeo para o termo, sem repetir o que já foi usado.

    O acervo vertical do Pexels é bem menor que o horizontal, então quando a
    busca em retrato não rende, repetimos sem restrição de orientação — o
    recorte para o canvas acontece de qualquer forma na montagem.
    """
    videos = _consultar(termo, orientacao)
    if len(videos) < 3:
        videos += _consultar(termo, None)

    for video in videos:
        # Clipe curto demais fica repetindo em loop e denuncia o truque.
        if (video.get("duration") or 0) < 5:
            continue
        # Prefere o menor arquivo que ainda tenha resolução suficiente.
        arquivos = sorted((a for a in video["video_files"] if (a.get("width") or 0) >= 1080),
                          key=lambda a: a["width"])
        if arquivos and arquivos[0]["link"] not in usados:
            usados.add(arquivos[0]["link"])
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


def degrade(indice, clima, largura, altura, segundos, destino):
    """Gera um fundo em degradê no clima do bloco, sem depender de rede."""
    paleta = CLIMAS[clima]
    cor = paleta[indice % len(paleta)]
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

    usados = set()
    if not CHAVE:
        print("  " + "!" * 66)
        print("  PEXELS_API_KEY não definida. Os vídeos vão sair só com degradê,")
        print("  sem nenhuma filmagem de pessoa. Crie a chave gratuita em")
        print("  pexels.com/api e salve como secret do repositório.")
        print("  " + "!" * 66)

    for indice, bloco in enumerate(blocos):
        clima = bloco.get("clima") or detectar_clima(bloco["texto"])
        bloco["clima"] = clima
        print(f"  bloco {indice:02d}  [{clima}]")
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

        url = (buscar_no_pexels(bloco["busca"], orientacao, usados)
               if (CHAVE and bloco.get("busca")) else None)
        if url:
            nome = hashlib.sha1(url.encode()).hexdigest()[:16] + ".mp4"
            bloco["fundo"] = str(baixar(url, CACHE / nome).resolve())
        else:
            bloco["fundo"] = str(degrade(indice, clima, largura, altura,
                                         bloco["duracao"] + 0.5, saida).resolve())

    salvar_json(destino / "blocos.json", dados)
    print(f"Fundos prontos em {fundos}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roteiro")
    principal(parser.parse_args().roteiro)
