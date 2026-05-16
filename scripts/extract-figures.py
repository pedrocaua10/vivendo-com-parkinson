# -*- coding: utf-8 -*-
"""
Extrai figuras recortadas do manual com logica por pagina.
Usa bbox das imagens embutidas como guia de corte.
"""

import sys
import os
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:
    import fitz

PDF = Path.home() / "Downloads" / "ManualPARKINSON_2ed.pdf"
OUT = Path(__file__).parent.parent / "public" / "assets" / "figuras"
OUT.mkdir(parents=True, exist_ok=True)

DPI_RENDER = 200   # DPI para render vetorial (maior = mais nitido)
PADDING_PT = 20    # padding em pontos PDF ao redor do bbox


def rect_with_padding(r, page, pad=PADDING_PT):
    """Expande rect com padding, respeitando limites da pagina."""
    pr = page.rect
    return fitz.Rect(
        max(0,      r.x0 - pad),
        max(0,      r.y0 - pad),
        min(pr.x1,  r.x1 + pad),
        min(pr.y1,  r.y1 + pad),
    )


def render_clip(page, clip_rect, dpi=DPI_RENDER):
    """Renderiza uma regiao da pagina em alta resolucao."""
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, clip=clip_rect, alpha=False)
    return pix


def extract_by_image_bbox(page, xref, pad=PADDING_PT, dpi=DPI_RENDER):
    """Renderiza a regiao da pagina onde a imagem esta, com labels vetoriais."""
    rects = page.get_image_rects(xref)
    if not rects:
        return None
    combined = fitz.Rect()
    for r in rects:
        combined |= r
    clip = rect_with_padding(combined, page, pad)
    return render_clip(page, clip, dpi)


def find_content_bbox(page, dpi=50):
    """
    Renderiza em DPI baixo e encontra bounding box do conteudo nao-branco.
    Usa analise de linhas horizontais para detectar regioes com conteudo.
    """
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    width, height = pix.width, pix.height
    samples = pix.samples  # bytes: R,G,B por pixel

    # Converte para lista de medias por linha
    row_means = []
    for y in range(height):
        row_sum = 0
        for x in range(width):
            idx = (y * width + x) * 3
            r, g, b = samples[idx], samples[idx+1], samples[idx+2]
            row_means.append((r + g + b) / 3)
            row_sum += (r + g + b) / 3
        # substituir por media da linha

    # Re-calcula: media por linha
    line_means = []
    for y in range(height):
        total = 0
        for x in range(width):
            idx = (y * width + x) * 3
            r, g, b = samples[idx], samples[idx+1], samples[idx+2]
            total += (r + g + b) / 3
        line_means.append(total / width)

    # Encontra linhas com conteudo (media < 245 = tem algo nao-branco)
    content_rows = [i for i, m in enumerate(line_means) if m < 245]
    if not content_rows:
        return page.rect

    # Converte de pixels (50dpi) de volta para pontos PDF
    scale = 72.0 / dpi
    top_px = content_rows[0]
    bot_px = content_rows[-1]

    # Faz o mesmo para colunas
    col_means = []
    for x in range(width):
        total = 0
        for y in range(height):
            idx = (y * width + x) * 3
            r, g, b = samples[idx], samples[idx+1], samples[idx+2]
            total += (r + g + b) / 3
        col_means.append(total / height)

    content_cols = [i for i, m in enumerate(col_means) if m < 245]
    if not content_cols:
        left_px, right_px = 0, width
    else:
        left_px, right_px = content_cols[0], content_cols[-1]

    pr = page.rect
    return fitz.Rect(
        max(0,     left_px  * scale - PADDING_PT),
        max(0,     top_px   * scale - PADDING_PT),
        min(pr.x1, right_px * scale + PADDING_PT),
        min(pr.y1, bot_px   * scale + PADDING_PT),
    )


def pix_to_png(pix, out_path):
    pix.save(str(out_path))
    kb = out_path.stat().st_size // 1024
    return pix.width, pix.height, kb


def process(doc, page_1idx, out_name, strategy):
    page = doc[page_1idx - 1]
    out_path = OUT / out_name
    strategy_desc = ""

    if strategy == "image_bbox":
        imgs = page.get_images(full=True)
        # Pega a maior imagem embutida (maior area)
        best = None
        best_area = 0
        for img in imgs:
            xref = img[0]
            info = doc.extract_image(xref)
            area = info["width"] * info["height"]
            if area > best_area:
                best_area = area
                best = xref
        if best is None:
            strategy = "content_bbox"
        else:
            pix = extract_by_image_bbox(page, best, pad=PADDING_PT)
            if pix is None:
                strategy = "content_bbox"
            else:
                strategy_desc = f"image_bbox xref={best}"

    if strategy == "content_bbox" or not strategy_desc:
        bbox = find_content_bbox(page)
        pix = render_clip(page, bbox)
        strategy_desc = f"content_bbox {bbox}"

    w, h, kb = pix_to_png(pix, out_path)
    return w, h, kb, strategy_desc


# Configuracao por pagina
# strategy: "image_bbox" = usa bbox da imagem embutida; "content_bbox" = analise de pixels
JOBS = [
    (9,  "neuronio-dopaminergico.png",  "image_bbox"),
    (16, "postura-parkinsoniana.png",    "image_bbox"),
    (15, "alteracoes-sensoriais.png",   "content_bbox"),
    (17, "alteracoes-autonomicas.png",  "image_bbox"),
    (36, "heimlich-sozinho.png",        "content_bbox"),
    (37, "heimlich-com-ajuda.png",      "content_bbox"),
    (50, "apb-atividades.png",          "content_bbox"),
]


def main():
    if not PDF.exists():
        print("ERRO: PDF nao encontrado em", PDF)
        sys.exit(1)

    print("Carregando:", PDF)
    doc = fitz.open(str(PDF))
    print("Paginas:", doc.page_count, "\n")

    rows = []
    for pn, fname, strategy in JOBS:
        print(f"  p{pn:02d} {fname} [{strategy}] ... ", end="", flush=True)
        try:
            w, h, kb, desc = process(doc, pn, fname, strategy)
            print(f"OK  {w}x{h}  {kb}KB  ({desc})")
            rows.append((fname, w, h, kb, desc, True))
        except Exception as e:
            print(f"ERRO: {e}")
            rows.append((fname, 0, 0, 0, str(e), False))

    doc.close()

    ok = sum(1 for r in rows if r[5])
    print(f"\nSucesso: {ok}/{len(rows)}")
    print("Destino:", OUT)


if __name__ == "__main__":
    main()
