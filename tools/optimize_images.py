#!/usr/bin/env python3
"""
Gera as imagens otimizadas do site (assets/img) a partir de uma pasta de originais.

Uso:
    python3 tools/optimize_images.py originais/ assets/img/

Os arquivos de entrada devem ter o mesmo nome (sem extensão) dos ids do site
(g1, c3, e1, gabriel...). Aceita JPG, PNG, WEBP, TIFF.
Para cada imagem gera:  <id>.webp  (até 2000 px, qualidade alta)
                        <id>-th.webp (miniatura de 1000 px para a galeria)
"""
import sys, os
from PIL import Image, ImageFilter, ImageOps

FULL, THUMB, MAXUP = 2000, 1000, 2.0

def process(src, out_dir):
    name = os.path.splitext(os.path.basename(src))[0]
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    L = max(im.size)
    if L < FULL:  # fonte pequena: amplia com Lanczos (limitado a 2x)
        k = min(MAXUP, FULL / L)
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))
    elif L > FULL:  # original grande: reduz
        k = FULL / L
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    im.save(os.path.join(out_dir, name + ".webp"), "WEBP", quality=90, method=6)
    k = THUMB / max(im.size)
    th = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    th.save(os.path.join(out_dir, name + "-th.webp"), "WEBP", quality=85, method=6)
    return name, im.size

if __name__ == "__main__":
    src_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    for f in sorted(os.listdir(src_dir)):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff")):
            print(*process(os.path.join(src_dir, f), out_dir))
