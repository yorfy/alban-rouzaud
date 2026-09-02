"""
Génère un DOCX mis en page à partir d'un .txt transcrit.

Usage :
  python generate_docx.py source.txt --title "Titre" --author "Auteur" --dates "1939-1941"
  python generate_docx.py source.txt --template modele.docx

Les règles de formatage sont décrites dans references/regles-formatage.md.
"""

import argparse
import re
from pathlib import Path
from copy import deepcopy
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


def add_page_number_footer(section, template_doc=None):
    """Ajoute un numéro de page dans le footer."""
    footer = section.footer
    footer.is_linked_to_previous = False

    if template_doc:
        # Copier le footer du template
        tmpl_footer = template_doc.sections[0].footer._element
        for child in list(footer._element):
            footer._element.remove(child)
        for child in tmpl_footer:
            footer._element.append(deepcopy(child))
    else:
        # Créer un numéro de page aligné à droite
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for tag in ('begin', None, 'separate', None, 'end'):
            run = p.add_run()
            if tag in ('begin', 'separate', 'end'):
                fld = run._r.makeelement(qn('w:fldChar'),
                                         {qn('w:fldCharType'): tag})
                run._r.append(fld)
            elif tag is None and not p._element.findall('.//' + qn('w:instrText')):
                instr = run._r.makeelement(qn('w:instrText'), {})
                instr.text = " PAGE  \\* MERGEFORMAT"
                run._r.append(instr)


def is_titre(line):
    """Détecte les titres de section (Journées, dates, en-têtes)."""
    patterns = [
        r"^\d+[re]+ [Jj]ournée",
        r"^[2-7]e journée",
    ]
    return any(re.match(p, line) for p in patterns)


def is_section_header(line):
    """Détecte les en-têtes de section centrés."""
    headers = ("— La fin première —", "Page(s) manquante(s)", "———")
    return line in headers or line.startswith("Vingt mois après")


def is_dialogue(line):
    """Détecte les lignes de dialogue."""
    return line.startswith(("—", "– ", "- "))


def needs_page_break(line):
    """Détermine si un saut de page est nécessaire avant cette ligne."""
    triggers = [
        "Journal non écrit",
        "1re Journée", "2e journée", "3e Journée", "4e journée",
        "5e journée", "6e journée", "7e Journée",
        "— La fin première —", "Vingt mois après",
        "Page(s) manquante(s)",
    ]
    return any(line.startswith(t) for t in triggers)


def split_titre_text(line):
    """Sépare un titre collé au texte : '7e Journée On murmure' → deux lignes."""
    m = re.match(r"^(\d+[re]+ [Jj]ournée\s*:?\s*)(.*\S.+)", line)
    if m and len(m.group(2).strip()) > 5:
        return [m.group(1).strip(), m.group(2).strip()]
    return [line]


def generate(txt_path, title, author, dates, template_path=None):
    txt = Path(txt_path).read_text(encoding="utf-8")

    # Retirer l'en-tête du .txt
    txt = re.sub(r"^.*?\n=+\n*", "", txt, count=1, flags=re.DOTALL)
    txt = txt.strip()

    # Charger le template si fourni
    template_doc = Document(str(template_path)) if template_path else None

    doc = Document()
    sec = doc.sections[0]

    if template_doc:
        tmpl_sec = template_doc.sections[0]
        sec.page_width = tmpl_sec.page_width
        sec.page_height = tmpl_sec.page_height
        sec.top_margin = tmpl_sec.top_margin
        sec.bottom_margin = tmpl_sec.bottom_margin
        sec.left_margin = tmpl_sec.left_margin
        sec.right_margin = tmpl_sec.right_margin
        sec.header_distance = tmpl_sec.header_distance
        sec.footer_distance = tmpl_sec.footer_distance
    else:
        # Format A5 par défaut
        sec.page_width = Cm(14.80)
        sec.page_height = Cm(21.00)
        sec.top_margin = Cm(0.75)
        sec.bottom_margin = Cm(0.50)
        sec.left_margin = Cm(1.27)
        sec.right_margin = Cm(1.27)
        sec.header_distance = Cm(1.27)
        sec.footer_distance = Cm(0.00)

    # Numéros de page
    add_page_number_footer(sec, template_doc)

    # Style par défaut
    default_size = Pt(14)
    if template_doc:
        for p in template_doc.paragraphs:
            if p.runs and p.text.strip() and len(p.text) > 50:
                if p.runs[0].font.size:
                    default_size = p.runs[0].font.size
                break

    style = doc.styles['Normal']
    style.font.size = default_size
    style.paragraph_format.space_after = Pt(2)
    style.paragraph_format.space_before = Pt(0)

    # Page de titre
    title_lines = title.split("\\n") if "\\n" in title else [title]
    for text_line, size, bold in [
        (author, 16, True), ("", 12, False),
        ("ÉCRITS DE GUERRE", 18, True),
        (dates, 16, False),
        ("", 12, False), ("", 12, False),
    ] + [(t, 18, True) for t in title_lines]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        if text_line:
            run = p.add_run(text_line)
            run.font.size = Pt(size)
            run.bold = bold

    doc.add_page_break()

    # Pré-traiter les lignes
    raw_lines = txt.split("\n")
    lines = []
    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^--- Page \d+", stripped):
            continue
        for part in split_titre_text(stripped):
            lines.append(part)

    # Fusionner les paragraphes coupés entre pages :
    # si une ligne ne finit pas par .!?» et la suivante commence par une minuscule,
    # c'est une phrase coupée — recoller.
    merged = []
    for line in lines:
        if (merged
            and line and line[0].islower()
            and not line.startswith(("—", "–", "-"))
            and merged[-1] and merged[-1][-1] not in ".!?\u00bb\""):
            merged[-1] = merged[-1] + " " + line
        else:
            merged.append(line)
    lines = merged

    # Typographie : guillemets droits → chevrons, doubles espaces
    final_lines = []
    for line in lines:
        line = re.sub(r" {2,}", " ", line)  # doubles espaces
        line = re.sub(r'(?:^|(?<=\s))"', '\u00ab\u00a0', line)  # " ouvrant → «
        line = re.sub(r'"(?=[\s.,;:!?\)]|$)', '\u00a0\u00bb', line)  # " fermant → »
        line = line.replace('"', '\u00a0\u00bb')  # restants → »
        final_lines.append(line)
    lines = final_lines

    # Générer le corps
    first_body = True
    for i, line in enumerate(lines):
        prev_line = lines[i - 1] if i > 0 else ""

        # Saut de page
        need_break = needs_page_break(line) and not first_body
        is_after_manquante = prev_line == "Page(s) manquante(s)"

        if is_after_manquante and need_break:
            # Un seul saut suffit (éviter page blanche)
            doc.add_page_break()
        elif is_after_manquante:
            doc.add_page_break()
        elif need_break:
            doc.add_page_break()

        first_body = False
        p = doc.add_paragraph()

        if line.startswith("Journal non écrit") or line.startswith("JOURNAL NON"):
            run = p.add_run(line)
            run.bold = True
            run.font.size = Pt(16)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(12)
        elif is_titre(line):
            run = p.add_run(line)
            run.bold = True
            run.font.size = Pt(default_size.pt + 1) if hasattr(default_size, 'pt') else Pt(15)
            p.paragraph_format.space_before = Pt(14)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        elif is_section_header(line):
            run = p.add_run(line)
            run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(14)
        elif is_dialogue(line):
            p.add_run(line)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        else:
            p.add_run(line)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Sauvegarder
    out_path = Path(txt_path).with_suffix('.docx')
    # Remplacer les espaces par des underscores pour le nom du fichier
    out_name = out_path.stem.replace(' ', '_') + '.docx'
    out_path = out_path.parent / out_name
    doc.save(str(out_path))
    print(f"Créé : {out_path} ({len(doc.paragraphs)} paragraphes)")
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Génère un DOCX mis en page à partir d'un .txt transcrit."
    )
    parser.add_argument("txt", help="Fichier .txt source")
    parser.add_argument("--title", required=True, help="Titre du document (\\n pour multi-ligne)")
    parser.add_argument("--author", default="", help="Auteur")
    parser.add_argument("--dates", default="", help="Dates")
    parser.add_argument("--template", help="DOCX modèle (optionnel)")

    args = parser.parse_args()
    generate(args.txt, args.title, args.author, args.dates,
             Path(args.template) if args.template else None)


if __name__ == "__main__":
    main()
