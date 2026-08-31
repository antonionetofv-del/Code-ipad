#!/usr/bin/env python3
"""Recorta o fundo das tres logos institucionais (SEBRAE, Governo do Para, Prefeitura)."""
import pathlib, sys
import numpy as np
from PIL import Image
from collections import deque

BASE = pathlib.Path(__file__).parent
UP = pathlib.Path("/root/.claude/uploads/967c3446-f3eb-5278-99e6-81cdb852543a")

def flood(im, tol=40):
    """Torna transparente so o fundo alcancavel a partir da borda; preserva contraformas."""
    a = np.asarray(im.convert("RGB"), dtype=np.int16)
    h, w, _ = a.shape
    ref = a[0, 0].astype(np.int16)
    prox = (np.abs(a - ref).sum(axis=2) <= tol)
    visto = np.zeros((h, w), dtype=bool)
    fila = deque()
    for x in range(w):
        for y in (0, h - 1):
            if prox[y, x] and not visto[y, x]:
                visto[y, x] = True; fila.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if prox[y, x] and not visto[y, x]:
                visto[y, x] = True; fila.append((y, x))
    while fila:
        y, x = fila.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and prox[ny, nx] and not visto[ny, nx]:
                visto[ny, nx] = True; fila.append((ny, nx))
    out = im.convert("RGBA")
    alpha = np.asarray(out)[:, :, 3].copy()
    alpha[visto] = 0
    arr = np.asarray(out).copy(); arr[:, :, 3] = alpha
    return Image.fromarray(arr, "RGBA")

def alpha_por_luminancia(im, corte=30, ganho=7):
    """Fundo preto -> alpha proporcional ao brilho (logo de tipografia clara)."""
    a = np.asarray(im.convert("RGB"), dtype=np.float32)
    lum = a.max(axis=2)
    alpha = np.clip((lum - corte) * ganho, 0, 255).astype(np.uint8)
    arr = np.dstack([a.astype(np.uint8), alpha])
    return Image.fromarray(arr, "RGBA")

TRABALHOS = [
    ("ea340f55-image.png", "logo-sebrae",          flood),
    ("f80b810c-image.png", "logo-governo-para",    flood),
    ("35ea5d7b-image.jpg", "logo-prefeitura-mae-do-rio", alpha_por_luminancia),
]

for src, nome, fn in TRABALHOS:
    p = UP / src
    if not p.exists():
        print(nome, "-> ausente"); continue
    im = Image.open(p)
    out = fn(im)
    out = out.crop(out.getbbox())
    out.save(BASE / (nome + ".png"))
    print(f"{nome:30s} {out.size}")
