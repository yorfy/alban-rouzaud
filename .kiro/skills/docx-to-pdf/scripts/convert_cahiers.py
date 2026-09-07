"""
Régénère les 4 PDFs des Écrits de Guerre depuis leurs DOCX dans docs/.

Usage :
    python .kiro/skills/docx-to-pdf/scripts/convert_cahiers.py

Passe par subprocess pour contourner le blocage PowerShell de Kiro
(le script convert.py ouvre Word via COM, ce qui peut bloquer le terminal).
"""

import subprocess
import sys
import os

DOCX_FILES = [
    "docs/ALBAN ROUZAUD_1_LA GUERRE.docx",
    "docs/ALBAN ROUZAUD_2_JOURNAL NON ECRIT D'UN FANTASSIN EN REPLIS STRATEGIQUE.docx",
    "docs/ALBAN ROUZAUD_3_L'EVASION.docx",
    "docs/ALBAN ROUZAUD_4_CAPTIVITE, RECITS ET REFLEXIONS.docx",
]

CONVERT_SCRIPT = r'.kiro/skills/docx-to-pdf/scripts/convert.py'
OUTPUT_DIR = 'docs'


def main():
    # S'assurer qu'on est à la racine du repo
    root = os.path.dirname(os.path.abspath(__file__))
    # Remonter jusqu'à la racine (scripts/ -> docx-to-pdf/ -> skills/ -> .kiro/ -> root)
    for _ in range(4):
        root = os.path.dirname(root)
    os.chdir(root)

    result = subprocess.run(
        [sys.executable, CONVERT_SCRIPT] + DOCX_FILES + ['--output', OUTPUT_DIR],
        capture_output=True,
        text=True,
        timeout=300,
    )
    print(result.stdout)
    if result.stderr:
        print('STDERR:', result.stderr)
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
