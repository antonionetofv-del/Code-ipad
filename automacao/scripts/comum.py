"""Utilidades compartilhadas pelo pipeline de produção."""

import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "saida"
CACHE = RAIZ / "cache_assets"

# Padrões de canvas por formato de vídeo.
FORMATOS = {
    "vertical": (1080, 1920),
    "horizontal": (1920, 1080),
    "quadrado": (1080, 1080),
}

VOZ_PADRAO = "pt-BR-AntonioNeural"


def ffmpeg():
    """Caminho do ffmpeg: o do sistema, ou o binário estático do imageio."""
    if caminho := shutil.which("ffmpeg"):
        return caminho
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg não encontrado. Instale o ffmpeg ou o pacote imageio-ffmpeg.")


def rodar(cmd, **kwargs):
    """Executa um comando e aborta com a saída de erro se ele falhar."""
    proc = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if proc.returncode != 0:
        sys.exit(f"Comando falhou: {' '.join(str(c) for c in cmd)}\n{proc.stderr[-2000:]}")
    return proc


def duracao(caminho):
    """Duração de um arquivo de mídia em segundos."""
    if ffprobe := shutil.which("ffprobe"):
        proc = rodar([ffprobe, "-v", "error", "-show_entries", "format=duration",
                      "-of", "default=nw=1:nk=1", str(caminho)])
        return float(proc.stdout.strip())
    # Sem ffprobe: decodifica descartando a saída e lê o último timestamp.
    proc = subprocess.run([ffmpeg(), "-i", str(caminho), "-f", "null", "-"],
                          capture_output=True, text=True)
    tempos = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", proc.stderr)
    if not tempos:
        sys.exit(f"Não consegui medir a duração de {caminho}")
    h, m, s = tempos[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


def tem_audio(caminho):
    """Diz se o arquivo tem faixa de áudio.

    Clipe de banco às vezes vem mudo. Sem essa checagem o grafo de filtros
    referencia uma entrada que não existe e a montagem inteira quebra.
    """
    if ffprobe := shutil.which("ffprobe"):
        proc = subprocess.run(
            [ffprobe, "-v", "error", "-select_streams", "a", "-show_entries",
             "stream=index", "-of", "csv=p=0", str(caminho)],
            capture_output=True, text=True)
        return bool(proc.stdout.strip())
    proc = subprocess.run([ffmpeg(), "-i", str(caminho)], capture_output=True, text=True)
    return "Audio:" in proc.stderr


def slug(texto):
    """Transforma um título em nome de pasta seguro."""
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", texto.lower())).strip("-")[:60]


def carregar_roteiro(caminho):
    """Lê um roteiro .md e devolve os metadados e os blocos.

    Formato esperado:

        ---
        titulo: Título do vídeo
        voz: pt-BR-AntonioNeural
        formato: vertical
        ---

        [busca: person typing on laptop]
        Texto que será narrado neste bloco.

        [arquivo: minha-captura.mp4]
        Outro bloco, usando um vídeo local em vez de banco de imagens.
    """
    bruto = Path(caminho).read_text(encoding="utf-8")

    meta = {}
    if bruto.startswith("---"):
        _, cabecalho, bruto = bruto.split("---", 2)
        for linha in cabecalho.strip().splitlines():
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                meta[chave.strip()] = valor.strip().strip("\"'")

    meta.setdefault("titulo", Path(caminho).stem)
    meta.setdefault("voz", VOZ_PADRAO)
    meta.setdefault("formato", "vertical")
    # +8% é o ritmo aprovado do canal. A locução padrão do TTS soa arrastada
    # para vídeo curto, e o roteiro que nasce sem `ritmo` deve já sair certo.
    meta.setdefault("ritmo", "+8%")

    if meta["formato"] not in FORMATOS:
        sys.exit(f"Formato '{meta['formato']}' inválido. Use: {', '.join(FORMATOS)}")

    blocos = []
    for pedaco in re.split(r"\n\s*\n", bruto.strip()):
        pedaco = pedaco.strip()
        if not pedaco or pedaco.startswith("#"):
            continue

        bloco = {"busca": None, "arquivo": None}
        def capturar(m):
            bloco[m.group(1)] = m.group(2).strip()
            return ""

        texto = re.sub(r"\[(busca|arquivo):([^\]]+)\]", capturar, pedaco).strip()
        texto = " ".join(texto.split())
        if texto:
            bloco["texto"] = texto
            blocos.append(bloco)

    if not blocos:
        sys.exit(f"Nenhum bloco de narração encontrado em {caminho}")

    return meta, blocos


def pasta_saida(meta, criar=True):
    destino = SAIDA / slug(meta["titulo"])
    if criar:
        destino.mkdir(parents=True, exist_ok=True)
    return destino


def salvar_json(caminho, dados):
    Path(caminho).write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


def carregar_json(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))
