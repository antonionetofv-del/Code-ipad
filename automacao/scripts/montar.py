"""Monta o vídeo final: fundos com movimento, personagem, legenda e som.

    python scripts/montar.py roteiros/meu-video.md
"""

import argparse
from pathlib import Path

from PIL import Image

from comum import (CACHE, FORMATOS, carregar_json, carregar_roteiro, duracao,
                   ffmpeg, pasta_saida, rodar, tem_audio)

VOLUME_TRILHA = 0.07

# Volume do som ambiente vindo dos próprios clipes, antes da compressão.
VOLUME_AMBIENTE = 0.34

# Quanto o fundo é ampliado antes do corte, para sobrar margem de movimento.
AMPLIACAO = 1.14

# Correção de cor aplicada a todo clipe. Filmagem de banco vem de câmeras e
# tratamentos diferentes; sem uma passada comum, um vídeo com oito clipes
# parece oito vídeos colados.
GRADE = "eq=contrast=1.07:saturation=1.06:gamma=0.98"

# A faixa escura atrás da legenda começa nesta fração da altura.
SCRIM_INICIO = 0.62
SCRIM_OPACIDADE = 200       # 0 a 255, no ponto mais escuro (rodapé)


def scrim(largura, altura):
    """Faixa escura em degradê, do meio para o rodapé.

    Legenda branca sobre filmagem real é ilegível quando a cena tem céu,
    parede clara ou monitor aceso. O degradê resolve sem tapar a imagem: no
    topo é totalmente transparente e só escurece onde o texto vive.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    caminho = CACHE / f"scrim_{largura}x{altura}.png"
    if caminho.exists():
        return caminho

    img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    inicio = int(altura * SCRIM_INICIO)
    pixels = img.load()
    for y in range(inicio, altura):
        # Curva quadrática: escurece devagar no começo e fecha no rodapé.
        proporcao = (y - inicio) / (altura - inicio)
        alfa = int(SCRIM_OPACIDADE * proporcao ** 1.6)
        for x in range(largura):
            pixels[x, y] = (0, 0, 0, alfa)
    img.save(caminho)
    return caminho


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
    # A deriva acompanha o ritmo da fala: com narração mais rápida e pausas
    # aparadas, um movimento lento demais faz o corte parecer parado.
    x = f"{folga_x:.1f}+{sx * folga_x * 0.75:.1f}*sin(t*0.34)"
    y = f"{folga_y:.1f}+{sy * folga_y * 0.75:.1f}*sin(t*0.26)"
    return x, y


def normalizar(origem, indice, largura, altura, segundos, destino):
    """Recorta o fundo para o canvas e a duração do bloco, com deriva de câmera.

    O áudio do clipe é preservado. É ele que amarra o som ao que está na tela:
    a rua do motorista, o teclado do escritório, a conversa da reunião. Som
    genérico colado por cima nunca soa do mesmo lugar que a imagem.

    Clipe mudo recebe silêncio, para todas as partes terem as mesmas faixas —
    o concat exige isso.
    """
    x, y = movimento(indice, largura, altura)
    alvo_l, alvo_a = int(largura * AMPLIACAO), int(altura * AMPLIACAO)

    entradas = ["-stream_loop", "-1", "-i", str(origem)]
    if tem_audio(origem):
        mapa_audio = ["-map", "0:a:0"]
    else:
        entradas += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
        mapa_audio = ["-map", "1:a:0"]

    rodar([
        ffmpeg(), "-y", *entradas,
        "-t", f"{segundos:.3f}",
        "-vf", (f"scale={alvo_l}:{alvo_a}:force_original_aspect_ratio=increase,"
                f"crop={largura}:{altura}:x='{x}':y='{y}',{GRADE},fps=30,setsar=1"),
        "-map", "0:v:0", *mapa_audio,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
        str(destino),
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
           "-c", "copy", "../video_base.mp4"], cwd=partes)

    legendas = destino / "legendas.ass"
    final = destino / "video.mp4"
    efeitos = destino / "efeitos.wav"

    entradas = [ffmpeg(), "-y", "-i", str(destino / "video_base.mp4")]
    filtros = []
    proxima = 1

    # Faixa escura atrás da legenda, para o texto continuar legível sobre
    # qualquer cena.
    entradas += ["-i", str(scrim(largura, altura))]
    filtros.append(f"[0:v][{proxima}:v]overlay=0:0[comp]")
    fluxo = "[comp]"
    proxima += 1

    entradas += ["-i", str(destino / "narracao.mp3")]
    indice_narracao = proxima
    proxima += 1

    # A narração é usada duas vezes: como voz e como chave para abaixar o
    # ambiente. Por isso ela é duplicada logo de saída.
    filtros.append(f"[{indice_narracao}:a]asplit=2[voz][chave]")

    # Ambiente do próprio clipe. O corte de graves tira ronco de câmera e
    # vento; o sidechain abaixa o ambiente sozinho quando a voz entra, e
    # devolve nas pausas. É isso que faz o som parecer gravado com a cena em
    # vez de colado depois.
    filtros.append(
        f"[0:a]highpass=f=180,volume={VOLUME_AMBIENTE}[amb];"
        f"[amb][chave]sidechaincompress="
        f"threshold=0.02:ratio=12:attack=15:release=350:makeup=1[ambiente]"
    )
    audios = ["[voz]", "[ambiente]"]
    print("  ambiente dos clipes, abaixado sob a narração")
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
