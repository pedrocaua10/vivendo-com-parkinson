"""
Extrai páginas específicas do manual em PNG usando PyMuPDF.
Uso: python scripts/extract-pdf-images.py
"""

import sys
import os
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:
    import fitz  # fallback para versões antigas

PDF_PATH = Path.home() / "Downloads" / "ManualPARKINSON_2ed.pdf"
OUTPUT_DIR = Path(__file__).parent.parent / "public" / "assets" / "figuras"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# (nome_arquivo, página_1_indexada)
PAGES = [
    ("neuronio-dopaminergico.png",  9),
    ("postura-parkinsoniana.png",  14),
    ("alteracoes-sensoriais.png",  15),
    ("alteracoes-autonomicas.png", 17),
    ("heimlich-sozinho.png",       36),
    ("heimlich-com-ajuda.png",     37),
    ("apb-atividades.png",         50),
]

# DPI: 150 = bom equilíbrio qualidade/tamanho; 200 para Retina
DPI = 150
MAX_WIDTH_PX = 1200

def extract_page(doc, page_num_1indexed, out_path):
    page = doc[page_num_1indexed - 1]  # pymupdf é 0-indexado

    # Calcula scale para atingir ~150 DPI sem exceder MAX_WIDTH_PX
    zoom = DPI / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    # Reduz se passar de MAX_WIDTH_PX
    if pix.width > MAX_WIDTH_PX:
        scale = MAX_WIDTH_PX / pix.width
        mat2 = fitz.Matrix(zoom * scale, zoom * scale)
        pix = page.get_pixmap(matrix=mat2, alpha=False)

    pix.save(str(out_path))
    size_kb = out_path.stat().st_size // 1024
    return pix.width, pix.height, size_kb

def main():
    if not PDF_PATH.exists():
        print(f"ERRO: PDF não encontrado em {PDF_PATH}")
        sys.exit(1)

    print(f"\nCarregando PDF: {PDF_PATH}")
    doc = fitz.open(str(PDF_PATH))
    print(f"Total de páginas: {doc.page_count}\n")

    results = []
    for filename, page_num in PAGES:
        out_path = OUTPUT_DIR / filename
        print(f"  Extraindo p.{page_num:02d} -> {filename} ... ", end="", flush=True)
        try:
            w, h, kb = extract_page(doc, page_num, out_path)
            print(f"OK  {w}×{h}px  {kb} KB")
            results.append((filename, page_num, w, h, kb, True, None))
        except Exception as e:
            print(f"ERRO  ERRO: {e}")
            results.append((filename, page_num, 0, 0, 0, False, str(e)))

    doc.close()

    ok = [r for r in results if r[5]]
    fail = [r for r in results if not r[5]]
    print(f"\n{'─'*50}")
    print(f"Sucesso: {len(ok)}/{len(results)}")
    if fail:
        print("Falhas:")
        for r in fail:
            print(f"  p.{r[1]:02d} {r[0]}: {r[6]}")
    print(f"Destino: {OUTPUT_DIR}\n")

if __name__ == "__main__":
    main()
