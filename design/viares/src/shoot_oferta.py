"""Renderiza a peça de oferta em Stories 1080×1920."""

import glob
import pathlib

from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).parent.parent
NAME = 'viares-oferta-mini-ensaio-stories'
W, H = 1080, 1920

_found = glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome')
LAUNCH = {'executable_path': _found[0]} if _found else {}

with sync_playwright() as p:
    browser = p.chromium.launch(**LAUNCH)
    page = browser.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
    page.goto((OUT / f'{NAME}.html').as_uri())
    page.wait_for_timeout(900)
    page.locator('.page').screenshot(path=str(OUT / f'{NAME}-{W}x{H}.png'))
    browser.close()
    print('ok', NAME)
