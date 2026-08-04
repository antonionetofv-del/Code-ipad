"""Renderiza os HTMLs das peças da Viares em PNG na resolução exata."""

import glob
import pathlib

from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).parent.parent

# O ambiente pode ter um Chromium pré-instalado com build diferente do que o
# pacote playwright espera; nesse caso apontamos direto para o executável.
_found = glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome')
LAUNCH = {'executable_path': _found[0]} if _found else {}

PIECES = [
    ('viares-lancamento-design',  1080, 1350),
    ('viares-oferta-mini-ensaio', 1080, 1350),
    ('viares-stories-enquete',    1080, 1920),
]

with sync_playwright() as p:
    browser = p.chromium.launch(**LAUNCH)
    for name, w, h in PIECES:
        page = browser.new_page(viewport={'width': w, 'height': h},
                                device_scale_factor=1)
        page.goto((OUT / f'{name}.html').as_uri())
        page.wait_for_timeout(700)
        page.locator('.page').screenshot(path=str(OUT / f'{name}-{w}x{h}.png'))
        page.close()
        print('ok', name)
    browser.close()
