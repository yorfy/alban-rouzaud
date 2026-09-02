"""
Prépare les images pour la transcription par sub-agents.

Usage :
  # À partir d'un PDF (extrait les pages puis redimensionne) :
  python prepare_images.py document.pdf

  # À partir d'un dossier d'images existantes :
  python prepare_images.py --images-dir ./mon_dossier

Convention de sortie :
  document/
  ├── images/        # pages extraites du PDF (ou copie des originaux)
  └── images_small/  # images redimensionnées si nécessaire

Toute image au-dessus de 4.5 MB est redimensionnée (JPEG qualité 85,
résolution ÷ 2) pour respecter la limite de 5 MB des sub-agents.
"""

import argparse
import shutil
import sys
from pathlib import Path

MAX_SIZE_BYTES = 4_500_000
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.webp'}


def convert_pdf_to_images(pdf_path: Path, output_dir: Path, dpi: int = 200) -> list[Path]:
    """Convertit un PDF en images PNG via pymupdf, avec fallback sur pdf2image."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Tenter pymupdf d'abord
    try:
        import pymupdf
        doc = pymupdf.open(str(pdf_path))
        total = len(doc)
        print(f"Conversion de {pdf_path.name} ({total} pages) via pymupdf à {dpi} DPI...")

        paths = []
        zoom = dpi / 72
        mat = pymupdf.Matrix(zoom, zoom)
        for i in range(total):
            out_path = output_dir / f"page_{i + 1:03d}.png"
            pix = doc[i].get_pixmap(matrix=mat)
            pix.save(str(out_path))
            size_mb = out_path.stat().st_size / 1e6
            print(f"  Page {i + 1:3d}/{total} : {pix.width}x{pix.height} px — {size_mb:.1f} MB")
            paths.append(out_path)
        doc.close()
        print(f"\n{total} pages converties dans {output_dir}")
        return paths

    except ImportError:
        pass

    # Fallback sur pdf2image
    try:
        from pdf2image import convert_from_path
        print(f"Conversion de {pdf_path.name} via pdf2image à {dpi} DPI...")
        images = convert_from_path(str(pdf_path), dpi=dpi)

        paths = []
        for i, img in enumerate(images, 1):
            out_path = output_dir / f"page_{i:03d}.png"
            img.save(str(out_path), "PNG")
            size_mb = out_path.stat().st_size / 1e6
            print(f"  Page {i}/{len(images)} : {size_mb:.1f} MB")
            paths.append(out_path)
        print(f"\n{len(images)} pages converties dans {output_dir}")
        return paths

    except ImportError:
        print("ERREUR : ni pymupdf ni pdf2image ne sont installés.")
        print("  pip install pymupdf       (recommandé)")
        print("  pip install pdf2image     (nécessite aussi poppler)")
        sys.exit(1)


def resize_image(src_path: Path, dst_path: Path) -> Path:
    """Redimensionne une image sous MAX_SIZE_BYTES."""
    from PIL import Image

    img = Image.open(src_path)
    w, h = img.size
    new_w, new_h = w // 2, h // 2
    img_resized = img.resize((new_w, new_h), Image.LANCZOS)

    if img_resized.mode in ('RGBA', 'LA', 'P'):
        img_resized = img_resized.convert('RGB')

    jpg_path = dst_path.with_suffix('.jpg')

    for quality in (85, 60):
        img_resized.save(jpg_path, 'JPEG', quality=quality)
        if jpg_path.stat().st_size <= MAX_SIZE_BYTES:
            return jpg_path

    # Dernier recours : réduire encore
    img_resized = img_resized.resize((new_w // 2, new_h // 2), Image.LANCZOS)
    img_resized.save(jpg_path, 'JPEG', quality=75)
    return jpg_path


def prepare_images(images_dir: Path, output_dir: Path) -> dict:
    """Copie ou redimensionne les images dans le dossier de sortie."""
    from PIL import Image  # noqa: F401

    output_dir.mkdir(parents=True, exist_ok=True)

    image_files = sorted(
        f for f in images_dir.iterdir()
        if f.suffix.lower() in IMAGE_EXTENSIONS
    )

    if not image_files:
        print(f"Aucune image trouvée dans {images_dir}")
        sys.exit(1)

    stats = {'total': len(image_files), 'copied': 0, 'resized': 0}

    for img_file in image_files:
        size = img_file.stat().st_size
        out_path = output_dir / img_file.name

        if size <= MAX_SIZE_BYTES:
            shutil.copy2(img_file, out_path)
            stats['copied'] += 1
            print(f"  {img_file.name}: {size / 1e6:.1f} MB -> copié")
        else:
            result_path = resize_image(img_file, out_path)
            new_size = result_path.stat().st_size
            stats['resized'] += 1
            print(f"  {img_file.name}: {size / 1e6:.1f} MB -> {result_path.name}: {new_size / 1e6:.1f} MB")

    print(f"\nRésumé :")
    print(f"  Total          : {stats['total']} images")
    print(f"  Copiées        : {stats['copied']}")
    print(f"  Redimensionnées: {stats['resized']}")
    print(f"  Dossier        : {output_dir}")
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Prépare les images pour la transcription de manuscrits.",
        epilog="Convention : crée <nom_source>/images/ et <nom_source>/images_small/",
    )
    parser.add_argument('pdf', nargs='?', help="Fichier PDF à convertir.")
    parser.add_argument('--images-dir', help="Dossier d'images existantes.")
    parser.add_argument('--dpi', type=int, default=200, help="Résolution (défaut : 200).")

    args = parser.parse_args()

    if args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"ERREUR : fichier introuvable : {args.pdf}")
            sys.exit(1)

        # Convention de dossiers : <nom_sans_extension>/images/ et /images_small/
        work_dir = pdf_path.parent / pdf_path.stem
        images_dir = work_dir / "images"
        images_small_dir = work_dir / "images_small"

        convert_pdf_to_images(pdf_path, images_dir, dpi=args.dpi)
        print(f"\nRedimensionnement...")
        prepare_images(images_dir, images_small_dir)

    elif args.images_dir:
        images_dir = Path(args.images_dir)
        if not images_dir.exists():
            print(f"ERREUR : dossier introuvable : {args.images_dir}")
            sys.exit(1)

        # Créer images_small/ à côté du dossier d'images
        images_small_dir = images_dir.parent / "images_small"
        prepare_images(images_dir, images_small_dir)

    else:
        parser.print_help()
        print("\nFournir un PDF ou --images-dir")
        sys.exit(1)


if __name__ == '__main__':
    main()
