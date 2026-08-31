#!/usr/bin/env python3
"""Renderiza as pecas do portico em tamanho real e gera os arquivos de impressao.

Cada peca sai em duas versoes:
  <peca>-RGB.png    referencia / aprovacao
  <peca>-CMYK.tif   arquivo de impressao (separacao com GCR, LZW)

Pecas com mais de 16384 px sao capturadas em faixas e emendadas, por causa do
limite de bitmap do navegador.
"""
import glob
import pathlib
import sys

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

Image.MAX_IMAGE_PIXELS = None

BASE = pathlib.Path(__file__).parent
OUT = BASE / "arquivos"
MM = 96 / 25.4          # px CSS por mm
MAX_FAIXA = 12000       # altura maxima de cada captura, em px

PECAS = {                       # id: (largura_mm, altura_mm)
    "testeira": (3200, 600),
    "lateral-esq": (600, 5000),
    "lateral-dir": (600, 5000),
}


def rgb_para_cmyk(im):
    """Separacao RGB -> CMYK com remocao de subcor (GCR).

    A conversao direta do Pillow zera o canal K, o que joga todo o preto para
    CMY e encarece a impressao. Aqui o preto vai para o canal K.
    """
    a = np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
    k = 1.0 - a.max(axis=2)
    d = np.maximum(1.0 - k, 1e-6)
    cmy = (1.0 - a - k[..., None]) / d[..., None]
    cmyk = np.concatenate([cmy, k[..., None]], axis=2)
    cmyk = np.clip(cmyk, 0.0, 1.0)
    cmyk[k >= 1.0] = (0.0, 0.0, 0.0, 1.0)
    return Image.fromarray((cmyk * 255.0 + 0.5).astype(np.uint8), mode="CMYK")


def render(url, dpi=96):
    OUT.mkdir(exist_ok=True)
    escala = dpi / 96.0
    exe = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))[-1]
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=exe, args=["--no-sandbox"])
        for pid, (wmm, hmm) in PECAS.items():
            wcss, hcss = wmm * MM, hmm * MM
            pag = nav.new_page(
                viewport={"width": round(wcss) + 40, "height": min(round(hcss) + 40, 30000)},
                device_scale_factor=escala,
            )
            pag.goto(url)
            # deixa so a peca alvo na pagina, para o recorte usar coordenadas do topo
            pag.evaluate("""(id)=>{document.querySelectorAll('.peca').forEach(e=>{
              if(e.id!==id) e.style.display='none';});
              document.body.style.padding='0'; document.body.style.gap='0';}""", pid)
            pag.wait_for_timeout(3000)
            caixa = pag.query_selector("#" + pid).bounding_box()
            alt_px = round(caixa["height"] * escala)
            n = max(1, -(-alt_px // MAX_FAIXA))          # teto da divisao
            passo = caixa["height"] / n
            faixas = []
            for i in range(n):
                alvo = BASE / f".faixa_{pid}_{i}.png"
                pag.screenshot(path=str(alvo), clip={
                    "x": caixa["x"], "y": caixa["y"] + i * passo,
                    "width": caixa["width"], "height": passo,
                })
                faixas.append(Image.open(alvo))
            larg = max(f.width for f in faixas)
            cheia = Image.new("RGB", (larg, sum(f.height for f in faixas)), "#01270E")
            y = 0
            for f in faixas:
                cheia.paste(f.convert("RGB"), (0, y))
                y += f.height
            cheia.save(OUT / f"{pid}-RGB.png", optimize=True)
            print(f"{pid}: {cheia.size[0]} x {cheia.size[1]} px  ({n} faixa(s), {dpi} dpi)")
            rgb_para_cmyk(cheia).save(OUT / f"{pid}-CMYK.tif", compression="tiff_lzw")
            for f in faixas:
                f.close()
            for i in range(n):
                (BASE / f".faixa_{pid}_{i}.png").unlink(missing_ok=True)
            pag.close()
        nav.close()


if __name__ == "__main__":
    render(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 96)
