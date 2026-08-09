"""Exporta um HTML de design para PNG no tamanho do canvas.

    python3 src/render.py dia-dos-pais-stories.html 1080 1920
"""
import glob, pathlib, sys
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve()
w, h = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1080, 1920)
png = html.with_name(f'{html.stem}-{w}x{h}.png')

# usa o Chromium ja instalado na maquina quando a versao nao bate com o pacote
chrome = next(iter(sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))), None)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
    pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
    pg.goto(html.as_uri())
    pg.wait_for_timeout(900)          # garante o webfont carregado
    pg.locator('.page').screenshot(path=str(png))
    b.close()

print('->', png)
