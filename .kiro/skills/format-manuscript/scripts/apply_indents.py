"""
Applique un retrait de première ligne aux paragraphes qui débutent un vrai
paragraphe typographique dans un DOCX existant (sans régénérer le document).

Règle stricte « début de paragraphe » :
  - Premier paragraphe du corps (après la page de titre)
  - Paragraphe qui suit directement un saut de page
  - Paragraphe qui suit directement un titre de section

Tous les autres paragraphes narratifs NE reçoivent PAS de retrait.
Cela permet une revue manuelle : tu ajoutes le retrait dans Word
sur les vrais débuts de paragraphe que tu identifies toi-même.

Exclusions (jamais de retrait) :
  - Lignes de dialogue (commençant par —, –, -)
  - Titres de section (gras, taille > normale)
  - Page de titre (paragraphes centrés avant le premier saut de page)
  - Paragraphes vides

Usage :
  python apply_indents.py <fichier.docx> [--indent 0.5] [--dry-run]

  --indent  Retrait en cm (défaut : 0.5)
  --dry-run Affiche les paragraphes qui recevraient un retrait sans modifier le fichier
"""

import argparse
from pathlib import Path
from docx import Document
from docx.shared import Cm
from docx.oxml.ns import qn


DIALOGUE_STARTS = ('—', '–', '- ', '– ')


def is_dialogue(text):
    return any(text.startswith(s) for s in DIALOGUE_STARTS)


def is_title_para(para):
    """Détecte les titres : style Heading, ou gras ET taille supérieure à la normale."""
    if not para.text.strip():
        return False
    # Style Heading (Heading 1, Heading 2, etc.)
    if para.style and para.style.name.startswith('Heading'):
        return True
    # Gras ET grande taille (inline)
    for run in para.runs:
        if run.bold and run.font.size and run.font.size.pt >= 15:
            return True
    return False


def is_section_header(para):
    """Détecte les en-têtes de section centrés (séparateurs, titres de chapitres)."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    text = para.text.strip()
    if not text:
        return False
    headers = ("— La fin première —", "Page(s) manquante(s)", "———")
    if text in headers or text.startswith("Vingt mois après"):
        return True
    # Titre centré en gras
    if para.alignment == WD_ALIGN_PARAGRAPH.CENTER:
        for run in para.runs:
            if run.bold:
                return True
    return False


def has_page_break_before(para):
    """Vérifie si un saut de page précède ce paragraphe."""
    # Cherche w:pageBreakBefore dans pPr
    pPr = para._element.find(qn('w:pPr'))
    if pPr is not None:
        pbr = pPr.find(qn('w:pageBreakBefore'))
        if pbr is not None and pbr.get(qn('w:val'), 'true') not in ('false', '0'):
            return True
    # Cherche w:br type=page dans le paragraphe précédent (dans les runs)
    return False


def prev_para_has_page_break(para, all_paras, idx):
    """Vérifie si le paragraphe précédent contient un saut de page."""
    if idx == 0:
        return False
    prev = all_paras[idx - 1]
    for br in prev._element.findall('.//' + qn('w:br')):
        if br.get(qn('w:type')) == 'page':
            return True
    return False


def classify_paragraphs(doc, indent_cm):
    """
    Retourne une liste de (para, should_indent, reason) pour tous les paragraphes du corps.
    La page de titre est détectée comme les paragraphes avant le premier saut de page.
    """
    all_paras = doc.paragraphs
    results = []

    # Trouver le premier saut de page (fin de page de titre)
    title_page_end = 0
    for i, p in enumerate(all_paras):
        for br in p._element.findall('.//' + qn('w:br')):
            if br.get(qn('w:type')) == 'page':
                title_page_end = i
                break
        if title_page_end:
            break

    in_body = False
    prev_text = ''
    prev_is_title = False
    prev_is_section = False
    first_body = True

    for i, para in enumerate(all_paras):
        text = para.text.strip()

        # Page de titre : tout avant le premier saut de page
        if i <= title_page_end:
            results.append((para, False, 'titre-page'))
            continue

        in_body = True

        if not text:
            results.append((para, False, 'vide'))
            prev_text = ''
            continue

        # Dialogue : jamais de retrait
        if is_dialogue(text):
            results.append((para, False, 'dialogue'))
            prev_text = text
            prev_is_title = False
            prev_is_section = False
            continue

        # Titre ou section header : pas de retrait, mais marque pour le suivant
        if is_title_para(para) or is_section_header(para):
            results.append((para, False, 'titre'))
            prev_text = text
            prev_is_title = True
            prev_is_section = True
            continue

        # Déterminer si c'est un début de paragraphe
        after_page_break = prev_para_has_page_break(para, all_paras, i)
        after_title = prev_is_title or prev_is_section

        if first_body:
            reason = 'premier-corps'
            indent = True
        elif after_page_break:
            reason = 'apres-saut-page'
            indent = True
        elif after_title:
            reason = 'apres-titre'
            indent = True
        else:
            reason = 'continuation'
            indent = False

        results.append((para, indent, reason))
        prev_text = text
        prev_is_title = False
        prev_is_section = False
        first_body = False

    return results


def apply_indents(docx_path, indent_cm=0.5, dry_run=False):
    doc = Document(str(docx_path))
    indent = Cm(indent_cm)

    classifications = classify_paragraphs(doc, indent_cm)

    n_indent = 0
    n_continuation = 0
    n_skip = 0

    for para, should_indent, reason in classifications:
        text = para.text.strip()
        if not text:
            continue

        if should_indent:
            n_indent += 1
            if dry_run:
                print(f'  [RETRAIT] ({reason}) {text[:80]}')
            else:
                para.paragraph_format.first_line_indent = indent
                # Vérification immédiate
                written = para.paragraph_format.first_line_indent
                if written is None:
                    # Forcer via XML direct
                    from docx.oxml import OxmlElement
                    pPr = para._element.find(qn('w:pPr'))
                    if pPr is None:
                        pPr = OxmlElement('w:pPr')
                        para._element.insert(0, pPr)
                    ind = pPr.find(qn('w:ind'))
                    if ind is None:
                        ind = OxmlElement('w:ind')
                        pPr.append(ind)
                    # Cm(0.5) = 720 twips
                    twips = str(int(indent.pt * 20))
                    ind.set(qn('w:firstLine'), twips)
        elif reason in ('continuation',):
            n_continuation += 1
            if dry_run:
                print(f'  [suite  ] ({reason}) {text[:80]}')
        else:
            n_skip += 1

    print(f'\n--- Résultat ---')
    print(f'  Début de paragraphe (retrait) : {n_indent}')
    print(f'  Continuation (pas de retrait) : {n_continuation}')
    print(f'  Ignorés (titre/dialogue/vide) : {n_skip}')

    if not dry_run:
        # Sauvegarder avec suffixe _indent pour ne pas écraser l'original
        out_path = docx_path.parent / (docx_path.stem + '_indent.docx')
        doc.save(str(out_path))
        print(f'\nSauvegardé : {out_path}')
    else:
        print(f'\n(dry-run — fichier non modifié)')


def main():
    parser = argparse.ArgumentParser(
        description='Applique un retrait de première ligne aux débuts de paragraphe dans un DOCX existant.'
    )
    parser.add_argument('docx', help='Fichier DOCX à traiter')
    parser.add_argument('--indent', type=float, default=0.5,
                        help='Retrait de première ligne en cm (défaut : 0.5)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Affiche la classification sans modifier le fichier')
    args = parser.parse_args()

    docx_path = Path(args.docx)
    if not docx_path.exists():
        print(f'Erreur : fichier introuvable : {docx_path}')
        return

    apply_indents(docx_path, indent_cm=args.indent, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
