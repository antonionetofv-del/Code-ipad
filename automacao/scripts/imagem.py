"""Gera imagem com o Nano Banana (modelos de imagem do Gemini).

Precisa de GEMINI_API_KEY no ambiente. A chave sai de aistudio.google.com.

    export GEMINI_API_KEY=...
    python scripts/imagem.py "flat vector icon, navy background" --saida capa.png
    python scripts/imagem.py "..." --modelo pro --proporcao 16:9
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

CHAVE = os.environ.get("GEMINI_API_KEY", "").strip()
BASE = "https://generativelanguage.googleapis.com/v1beta/models"

# Os apelidos são o que as pessoas usam; o id é o que a API aceita.
MODELOS = {
    "lite": "gemini-3.1-flash-lite-image",   # "Nano Banana 2 Lite" — mais barato
    "pro": "gemini-3-pro-image-preview",     # "Nano Banana Pro" — melhor qualidade
}


def gerar(prompt, modelo="lite", proporcao=None, destino=Path("imagem.png")):
    if not CHAVE:
        sys.exit("GEMINI_API_KEY não definida. Pegue a chave em aistudio.google.com.")

    corpo = {"contents": [{"parts": [{"text": prompt}]}]}
    if proporcao:
        corpo["generationConfig"] = {"imageConfig": {"aspectRatio": proporcao}}

    identificador = MODELOS.get(modelo, modelo)
    requisicao = urllib.request.Request(
        f"{BASE}/{identificador}:generateContent",
        data=json.dumps(corpo).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": CHAVE},
    )

    try:
        with urllib.request.urlopen(requisicao, timeout=180) as resposta:
            dados = json.load(resposta)
    except urllib.error.HTTPError as erro:
        detalhe = erro.read().decode("utf-8", "replace")[:600]
        sys.exit(f"A API recusou (HTTP {erro.code}):\n{detalhe}")

    # A imagem volta embutida em base64 entre as partes da resposta.
    for candidato in dados.get("candidates", []):
        for parte in candidato.get("content", {}).get("parts", []):
            embutido = parte.get("inlineData") or parte.get("inline_data")
            if embutido and embutido.get("data"):
                destino = Path(destino)
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_bytes(base64.b64decode(embutido["data"]))
                print(f"{destino}  ({destino.stat().st_size // 1024} KB, modelo {identificador})")
                return destino

    # Sem imagem: quase sempre é recusa por política, e o motivo vem no texto.
    texto = json.dumps(dados)[:600]
    sys.exit(f"A resposta não trouxe imagem. Retorno da API:\n{texto}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", help="descrição da imagem, em inglês (responde melhor)")
    parser.add_argument("--modelo", default="lite", choices=list(MODELOS) + ["custom"],
                        help="lite (barato) ou pro (melhor). Padrão: lite")
    parser.add_argument("--proporcao", help="ex: 1:1, 16:9, 9:16")
    parser.add_argument("--saida", default="imagem.png")
    args = parser.parse_args()
    gerar(args.prompt, args.modelo, args.proporcao, Path(args.saida))
