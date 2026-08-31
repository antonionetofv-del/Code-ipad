#!/usr/bin/env python3
"""Recorta o fundo das fotos de artistas com o modelo u2net."""
import pathlib
from PIL import Image
from rembg import new_session, remove

Image.MAX_IMAGE_PIXELS = None
BASE = pathlib.Path(__file__).parent
sess = new_session("u2net")

# fotos que chegaram com fundo; as demais ja vieram recortadas
COM_FUNDO = [
    "b-chapeu-marrom-xadrez", "b-chapeu-palha-preta", "b-chapeu-branco-palco",
    "b-jaqueta-bracos-cruzados", "b-camisa-branca-noturna",
    "evandro-do-acordeon", "gleyk-e-gleyson",
]

for nome in COM_FUNDO:
    src = BASE / (nome + ".jpg")
    if not src.exists():
        print(nome, "-> arquivo ausente"); continue
    im = Image.open(src)
    # fotos muito grandes atrasam o modelo sem ganho visivel na lona
    if max(im.size) > 2200:
        f = 2200 / max(im.size)
        im = im.resize((round(im.width*f), round(im.height*f)), Image.LANCZOS)
    out = remove(im, session=sess, post_process_mask=True)
    out = out.crop(out.getbbox())
    out.save(BASE / (nome + ".png"))
    print(f"{nome:26s} {out.size}")
