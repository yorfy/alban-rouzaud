"""
convert.py — Convertit des fichiers DOCX en PDF via l'API COM de Microsoft Word.

Usage:
    python convert.py <source> [<source2> ...] [--output <dossier>]

<source> peut être :
    - un fichier .docx
    - un dossier (convertit tous les .docx qu'il contient)

--output : dossier de destination (défaut : même dossier que la source)
"""

import argparse
import os
import sys


def convert_docx_to_pdf(docx_path: str, output_dir: str) -> str:
    """Convertit un fichier DOCX en PDF. Retourne le chemin du PDF produit."""
    try:
        import win32com.client
    except ImportError:
        print("ERREUR : pywin32 non installé. Exécuter :")
        print("  venv\\Scripts\\python.exe -m pip install pywin32")
        sys.exit(1)

    docx_path = os.path.abspath(docx_path)
    basename = os.path.splitext(os.path.basename(docx_path))[0]
    pdf_path = os.path.join(os.path.abspath(output_dir), basename + ".pdf")

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(docx_path)
        # Désactiver l'impression des commentaires dans le PDF
        try:
            word.Options.PrintComments = False
        except Exception:
            pass
        # ExportAsFixedFormat avec CreateBookmarks=1 (wdExportCreateHeadingBookmarks)
        # pour inclure les signets PDF générés depuis les styles Titre1/Titre2
        doc.ExportAsFixedFormat(
            OutputFileName=pdf_path,
            ExportFormat=17,          # wdExportFormatPDF
            OpenAfterExport=False,
            OptimizeFor=0,            # wdExportOptimizeForPrint
            Range=0,                  # wdExportAllDocument
            From=1,
            To=1,
            Item=0,                   # wdExportDocumentContent
            IncludeDocProps=True,
            KeepIRM=True,
            CreateBookmarks=1,        # wdExportCreateHeadingBookmarks
            DocStructureTags=True,
            BitmapMissingFonts=True,
            UseISO19005_1=False,
        )
        doc.Close(SaveChanges=False)
    finally:
        word.Quit()

    return pdf_path


def collect_docx_files(sources: list[str]) -> list[str]:
    """Collecte les fichiers .docx depuis une liste de chemins (fichiers ou dossiers)."""
    result = []
    for source in sources:
        source = os.path.abspath(source)
        if os.path.isdir(source):
            for f in sorted(os.listdir(source)):
                if f.lower().endswith(".docx"):
                    result.append(os.path.join(source, f))
        elif os.path.isfile(source) and source.lower().endswith(".docx"):
            result.append(source)
        else:
            print(f"AVERTISSEMENT : ignoré (non trouvé ou non .docx) : {source}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Convertit des DOCX en PDF via Word COM.")
    parser.add_argument("sources", nargs="+", help="Fichiers .docx ou dossiers source")
    parser.add_argument("--output", "-o", default=None, help="Dossier de sortie (défaut : même dossier que la source)")
    args = parser.parse_args()

    files = collect_docx_files(args.sources)
    if not files:
        print("Aucun fichier .docx trouvé.")
        sys.exit(1)

    print(f"{len(files)} fichier(s) à convertir.")

    errors = []
    for docx_path in files:
        output_dir = args.output if args.output else os.path.dirname(docx_path)
        os.makedirs(output_dir, exist_ok=True)
        print(f"Conversion : {os.path.basename(docx_path)}")
        try:
            pdf_path = convert_docx_to_pdf(docx_path, output_dir)
            size = os.path.getsize(pdf_path)
            print(f"  -> {os.path.basename(pdf_path)} ({size:,} octets)")
        except Exception as e:
            print(f"  ERREUR : {e}")
            errors.append(docx_path)

    print()
    if errors:
        print(f"Terminé avec {len(errors)} erreur(s) :")
        for f in errors:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"Terminé. {len(files)} PDF(s) produit(s).")


if __name__ == "__main__":
    main()
