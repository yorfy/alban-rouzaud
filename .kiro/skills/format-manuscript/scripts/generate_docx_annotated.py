"""
Génère un DOCX mis en page à partir d'un .txt transcrit,
avec surlignage jaune et commentaires sur les zones ambiguës.

Usage :
  python generate_docx_annotated.py source_revue.txt --rapport rapport.md \
      --title "Titre" --author "Auteur" --dates "1939-1941"

Les annotations sont extraites du rapport _rapport.md (sections Lectures ambiguës,
Lectures incertaines, Passages illisibles, Sens douteux).
"""

import argparse
import re
from pathlib import Path
from copy import deepcopy
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml.ns import qn


# ---------------------------------------------------------------------------
# Annotation data model
# ---------------------------------------------------------------------------

class Annotation:
    """A single annotation tied to a word/passage in the text."""
    def __init__(self, page: int, word: str, note: str, category: str):
        self.page = page
        self.word = word        # text to highlight
        self.note = note        # comment text
        self.category = category  # AMBIGU, INCERTAIN, ILLISIBLE, SENS_DOUTEUX
        self.used = False

    def __repr__(self):
        return f"<Ann p{self.page} '{self.word[:30]}' [{self.category}]>"


# ---------------------------------------------------------------------------
# Parse the rapport.md to extract annotations
# ---------------------------------------------------------------------------

def parse_rapport(rapport_path: str) -> list[Annotation]:
    """Parse the rapport markdown and return a list of Annotations."""
    text = Path(rapport_path).read_text(encoding="utf-8")
    annotations = []

    # Split into sections
    sections = re.split(r"^## ", text, flags=re.MULTILINE)

    for section in sections:
        lines = section.strip().split("\n")
        if not lines:
            continue
        header = lines[0].strip()

        if header.startswith("Lectures ambiguës") or header.startswith("Lectures ambigu"):
            annotations.extend(_parse_ambiguous_table(lines, "AMBIGU"))
        elif header.startswith("Lectures incertaines"):
            annotations.extend(_parse_uncertain_table(lines, "INCERTAIN"))
        elif header.startswith("Passages illisibles"):
            annotations.extend(_parse_illisible_table(lines, "ILLISIBLE"))
        elif header.startswith("Sens douteux"):
            annotations.extend(_parse_sens_douteux_table(lines, "SENS_DOUTEUX"))

    print(f"  Annotations extraites : {len(annotations)}")
    cats = {}
    for a in annotations:
        cats[a.category] = cats.get(a.category, 0) + 1
    for c, n in sorted(cats.items()):
        print(f"    {c}: {n}")
    return annotations


def _clean_cell(cell: str) -> str:
    """Remove surrounding quotes and whitespace from a table cell."""
    cell = cell.strip()
    if cell.startswith('"') and cell.endswith('"'):
        cell = cell[1:-1]
    return cell.strip()


def _parse_page(page_str: str) -> int:
    """Extract the first integer from a page string like '14' or '32-35'."""
    m = re.search(r"\d+", page_str)
    return int(m.group()) if m else 0


def _parse_ambiguous_table(lines: list[str], category: str) -> list[Annotation]:
    """Parse | Page | Mot transcrit | Alternative | Contexte |"""
    annotations = []
    for line in lines:
        if not line.startswith("|") or line.startswith("|-") or "Page" in line:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 4:
            continue
        page = _parse_page(cells[0])
        word = _clean_cell(cells[1])
        alt = _clean_cell(cells[2])
        ctx = _clean_cell(cells[3])
        if not page or not word:
            continue
        # Build comment
        comment = f"[AMBIGU] {word}"
        if alt:
            comment += f" → alternative : {alt}"
        if ctx:
            comment += f" — {ctx}"
        annotations.append(Annotation(page, word, comment, category))
    return annotations


def _parse_uncertain_table(lines: list[str], category: str) -> list[Annotation]:
    """Parse | Page | Mot/passage | Note |"""
    annotations = []
    for line in lines:
        if not line.startswith("|") or line.startswith("|-") or "Page" in line:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 3:
            continue
        page = _parse_page(cells[0])
        word = _clean_cell(cells[1])
        note = _clean_cell(cells[2])
        if not page or not word:
            continue
        comment = f"[INCERTAIN] {word} — {note}"
        annotations.append(Annotation(page, word, comment, category))
    return annotations


def _parse_illisible_table(lines: list[str], category: str) -> list[Annotation]:
    """Parse | Page | Description |"""
    annotations = []
    for line in lines:
        if not line.startswith("|") or line.startswith("|-") or "Page" in line:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 2:
            continue
        page = _parse_page(cells[0])
        desc = _clean_cell(cells[1])
        if not page:
            continue
        # The word to highlight is [illisible] or [tampon]
        annotations.append(Annotation(page, "[illisible]", f"[ILLISIBLE] {desc}", category))
    return annotations


def _parse_sens_douteux_table(lines: list[str], category: str) -> list[Annotation]:
    """Parse | Page | Passage transcrit | Problème | Interprétation possible |"""
    annotations = []
    for line in lines:
        if not line.startswith("|") or line.startswith("|-") or "Page" in line:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 4:
            continue
        page = _parse_page(cells[0])
        passage = _clean_cell(cells[1])
        problem = _clean_cell(cells[2])
        interp = _clean_cell(cells[3])
        if not page or not passage:
            continue
        comment = f"[SENS DOUTEUX] {passage}"
        if problem:
            comment += f" — {problem}"
        if interp:
            comment += f" | {interp}"
        # Use first 4+ words of passage as search key
        word = passage
        annotations.append(Annotation(page, word, comment, category))
    return annotations


# ---------------------------------------------------------------------------
# Highlight color helpers
# ---------------------------------------------------------------------------

HIGHLIGHT_COLORS = {
    "AMBIGU": WD_COLOR_INDEX.YELLOW,
    "INCERTAIN": WD_COLOR_INDEX.TURQUOISE,
    "ILLISIBLE": WD_COLOR_INDEX.PINK,
    "SENS_DOUTEUX": WD_COLOR_INDEX.BRIGHT_GREEN,
}


# ---------------------------------------------------------------------------
# Text processing (adapted from generate_docx.py)
# ---------------------------------------------------------------------------

def is_titre_section(line):
    """Detect section titles across all manuscripts."""
    title_patterns = [
        # --- Cahier 2 : Journal non écrit (Journées de repli) ---
        r'^\d+[re]+ [Jj]ournée',
        r'^[2-7]e journée',
        r'^Journal non écrit',
        r'^JOURNAL NON',
        r'^— La fin première —',
        r'^Vingt mois après',
        # --- Cahier 4 : Captivité ---
        r'^« Histoire de Pages »',
        r'^« PAGES d\'HISTOIRE »',
        r'^« Quelques Réflexions »',
        r'^Le Rappel de Quelques Souvenirs',
        r'^« Les Chleuhs',
        r'^« Passe-temps idiot »',
        r'^« Colloque Santi-mental »',
        r'^« Arbeits Kommando »',
        r'^« Stalag »',
        r'^Capitale des',
        r'^« Petites Scènes de la vie de Captivité »',
        r'^« Les Gendarmes »',
        r'^« Miaou »',
        r'^« Démangeaisons »',
        r'^« Les jeux sont faits',
        r'^« Les Sauvages »',
        r'^« Tel que',
        r'^« Parfums »',
        r'^« Gueuletons »',
        r'^« Chiffres »',
        r'^« Leçon',
        r'^« Prêtés et Rendus »',
        r'^Tabac\.\.\. à la noix',
        r'^« Babioles »',
        r'^— Babioles —',
        r'^« Benedicte »',
        r'^« Au bureau de tabac »',
        r'^« Regain »',
        r'^« Ballade des Noëls',
        r'^Envoi :',
        r'^« Revue de Noël »',
        r'^« Pour mémoire »',
        r'^Noël 1941',
        # Dates standalone
        r'^Marburg\s+\d',
        r'^— Épinal —',
        r'^— Güssing —',
        r'^Épinal —',
        r'^Kaiserstenbrück',
        r'^Bains-les-Bains',
        r'^Gisseng',
        r'^P\.cc\.',
    ]
    for pattern in title_patterns:
        if re.match(pattern, line):
            return True
    return False


def is_date_line(line):
    """Detect standalone date lines."""
    return bool(re.match(r'^(Marburg|— Épinal|Épinal|Kaiserstenbrück|Bains-les-Bains|Gisseng|— Güssing|P\.cc\.)', line))


def is_dialogue(line):
    return line.startswith(("—", "– ", "- "))


def needs_page_break(line):
    """Section titles that merit a page break."""
    triggers = [
        # Cahier 2
        "Journal non écrit",
        "1re Journée", "2e journée", "3e Journée", "4e journée",
        "5e journée", "6e journée", "7e Journée",
        "— La fin première —", "Vingt mois après",
        "Page(s) manquante(s)",
        # Cahier 4
        "« PAGES d'HISTOIRE »",
        "Le Rappel de Quelques Souvenirs",
        "« Les Chleuhs",
        "« Passe-temps idiot »",
        "« Arbeits Kommando »",
        "« Stalag »",
        "« Petites Scènes",
        "« Revue de Noël »",
        "Noël 1941",
    ]
    return any(line.startswith(t) for t in triggers)


def split_titre_text(line):
    """Sépare un titre collé au texte : '7e Journée On murmure' → deux lignes."""
    m = re.match(r"^(\d+[re]+ [Jj]ournée\s*:?\s*)(.*\S.+)", line)
    if m and len(m.group(2).strip()) > 5:
        return [m.group(1).strip(), m.group(2).strip()]
    return [line]


# ---------------------------------------------------------------------------
# Core generation
# ---------------------------------------------------------------------------

def generate(txt_path, rapport_path, title, author, dates, template_path=None):
    # Load text
    txt = Path(txt_path).read_text(encoding="utf-8")

    # Parse annotations from rapport
    annotations = parse_rapport(rapport_path) if rapport_path else []

    # Build page→annotations index
    ann_by_page = {}
    for ann in annotations:
        ann_by_page.setdefault(ann.page, []).append(ann)

    # Load template
    template_doc = Document(str(template_path)) if template_path else None

    doc = Document()
    sec = doc.sections[0]

    if template_doc:
        tmpl_sec = template_doc.sections[0]
        for attr in ('page_width', 'page_height', 'top_margin', 'bottom_margin',
                      'left_margin', 'right_margin', 'header_distance', 'footer_distance'):
            setattr(sec, attr, getattr(tmpl_sec, attr))
    else:
        sec.page_width = Cm(14.80)
        sec.page_height = Cm(21.00)
        sec.top_margin = Cm(0.75)
        sec.bottom_margin = Cm(0.50)
        sec.left_margin = Cm(1.27)
        sec.right_margin = Cm(1.27)
        sec.header_distance = Cm(1.27)
        sec.footer_distance = Cm(0.00)

    # Footer with page numbers
    _add_page_number_footer(sec, template_doc)

    # Default font
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

    # ---- Page de titre ----
    for text_line, size, bold in [
        (author, 16, True), ("", 12, False),
        ("ÉCRITS DE GUERRE ET DE CAPTIVITÉ", 18, True),
        (dates, 16, False),
        ("", 12, False), ("", 12, False),
        (title, 18, True),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        if text_line:
            run = p.add_run(text_line)
            run.font.size = Pt(size)
            run.bold = bold

    # Legend for highlighting
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(24)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("Légende des annotations :")
    run.bold = True
    run.font.size = Pt(11)

    for color, label in [
        (WD_COLOR_INDEX.YELLOW, "Jaune = lecture ambiguë"),
        (WD_COLOR_INDEX.TURQUOISE, "Turquoise = lecture incertaine"),
        (WD_COLOR_INDEX.PINK, "Rose = passage illisible"),
        (WD_COLOR_INDEX.BRIGHT_GREEN, "Vert = sens douteux"),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(f"  ■ {label}")
        run.font.size = Pt(10)
        run.font.highlight_color = color

    doc.add_page_break()

    # ---- Process text lines ----
    raw_lines = txt.split("\n")
    # Track page numbers from markers
    processed = []  # list of (line_text, page_number)
    current_page = 0

    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            continue
        m = re.match(r"^--- Page (\d+) ---$", stripped)
        if m:
            current_page = int(m.group(1))
            continue
        # Remove header lines (top of .txt before ====)
        if stripped.startswith("ALBAN ROUZAUD") or stripped.startswith("ÉCRITS DE GUERRE") or stripped.startswith("====="):
            continue
        if stripped in ("Captivité, Récits et Réflexions",):
            continue
        # Split titre collé au texte (ex: "7e Journée On murmure")
        for part in split_titre_text(stripped):
            processed.append((part, current_page))

    # Merge split paragraphs (phrase coupée entre pages)
    merged = []
    for line_text, page_num in processed:
        if (merged
            and line_text and line_text[0].islower()
            and not line_text.startswith(("—", "–", "-"))
            and merged[-1][0] and merged[-1][0][-1] not in ".!?\u00bb\""):
            merged[-1] = (merged[-1][0] + " " + line_text, merged[-1][1])
        else:
            merged.append((line_text, page_num))
    processed = merged

    # ---- Generate body with annotations ----
    first_body = True
    for i, (line, page) in enumerate(processed):
        # Page break before section titles
        if needs_page_break(line) and not first_body:
            doc.add_page_break()
        first_body = False

        p = doc.add_paragraph()

        # Determine style
        is_title = is_titre_section(line)
        is_date = is_date_line(line)
        is_dial = is_dialogue(line)

        if is_title and not is_date:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(12)
        elif is_date:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p.paragraph_format.space_before = Pt(6)
        elif is_dial:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        # Get annotations for this page
        page_anns = ann_by_page.get(page, [])

        if not page_anns:
            # No annotations — simple run
            run = p.add_run(line)
            if is_title and not is_date:
                run.bold = True
                run.font.size = Pt(default_size.pt + 1) if hasattr(default_size, 'pt') else Pt(15)
            elif is_date:
                run.font.size = Pt(default_size.pt - 1) if hasattr(default_size, 'pt') else Pt(13)
                run.italic = True
        else:
            # Try to match and highlight annotations in the text
            _add_annotated_line(doc, p, line, page_anns, is_title, is_date, default_size)

    # Save
    out_path = Path(txt_path).with_name(
        Path(txt_path).stem.replace("_revue", "") + ".docx"
    )
    doc.save(str(out_path))
    print(f"\nCréé : {out_path} ({len(doc.paragraphs)} paragraphes)")

    # Stats
    used = sum(1 for a in annotations if a.used)
    print(f"Annotations appliquées : {used}/{len(annotations)}")

    return out_path


def _add_annotated_line(document, paragraph, text: str, annotations: list[Annotation],
                         is_title: bool, is_date: bool, default_size):
    """Add text to paragraph with highlighted annotations and Word comments."""
    # Build list of (start, end, annotation) matches
    matches = []
    for ann in annotations:
        if ann.used:
            continue
        # Clean the search word
        search = ann.word.strip('"\'')
        if not search or len(search) < 2:
            continue
        # For SENS_DOUTEUX, use first significant words (up to 40 chars)
        if ann.category == "SENS_DOUTEUX" and len(search) > 40:
            search = search[:40]

        # Find in text (case-insensitive)
        idx = text.lower().find(search.lower())
        if idx >= 0:
            matches.append((idx, idx + len(search), ann))
            ann.used = True
        else:
            # Try shorter match (first 3 words)
            words = search.split()
            if len(words) >= 3:
                short = " ".join(words[:3])
                idx = text.lower().find(short.lower())
                if idx >= 0:
                    matches.append((idx, idx + len(short), ann))
                    ann.used = True
            elif len(words) >= 2:
                short = " ".join(words[:2])
                idx = text.lower().find(short.lower())
                if idx >= 0:
                    matches.append((idx, idx + len(short), ann))
                    ann.used = True

    if not matches:
        # No matches found — plain text
        run = paragraph.add_run(text)
        if is_title and not is_date:
            run.bold = True
            run.font.size = Pt(default_size.pt + 1) if hasattr(default_size, 'pt') else Pt(15)
        elif is_date:
            run.font.size = Pt(default_size.pt - 1) if hasattr(default_size, 'pt') else Pt(13)
            run.italic = True
        return

    # Sort matches by position and remove overlaps
    matches.sort(key=lambda m: m[0])
    non_overlapping = []
    last_end = 0
    for start, end, ann in matches:
        if start >= last_end:
            non_overlapping.append((start, end, ann))
            last_end = end
    matches = non_overlapping

    # Collect runs that need comments (apply comments after all runs are added)
    pending_comments = []  # list of (run, annotation)

    # Build runs: alternating plain and highlighted
    pos = 0
    for start, end, ann in matches:
        if start > pos:
            # Plain text before this match
            run = paragraph.add_run(text[pos:start])
            if is_title and not is_date:
                run.bold = True
                run.font.size = Pt(default_size.pt + 1) if hasattr(default_size, 'pt') else Pt(15)
            elif is_date:
                run.font.size = Pt(default_size.pt - 1) if hasattr(default_size, 'pt') else Pt(13)
                run.italic = True

        # Highlighted run
        highlighted_text = text[start:end]
        run = paragraph.add_run(highlighted_text)
        color = HIGHLIGHT_COLORS.get(ann.category, WD_COLOR_INDEX.YELLOW)
        run.font.highlight_color = color
        if is_title and not is_date:
            run.bold = True
            run.font.size = Pt(default_size.pt + 1) if hasattr(default_size, 'pt') else Pt(15)
        elif is_date:
            run.font.size = Pt(default_size.pt - 1) if hasattr(default_size, 'pt') else Pt(13)
            run.italic = True

        pending_comments.append((run, ann))
        pos = end

    # Remaining text after last match
    if pos < len(text):
        run = paragraph.add_run(text[pos:])
        if is_title and not is_date:
            run.bold = True
            run.font.size = Pt(default_size.pt + 1) if hasattr(default_size, 'pt') else Pt(15)
        elif is_date:
            run.font.size = Pt(default_size.pt - 1) if hasattr(default_size, 'pt') else Pt(13)
            run.italic = True

    # Now add Word comments using the native document.add_comment() API
    CATEGORY_INITIALS = {
        "AMBIGU": "AM",
        "INCERTAIN": "IN",
        "ILLISIBLE": "IL",
        "SENS_DOUTEUX": "SD",
    }
    for run, ann in pending_comments:
        note_text = ann.note
        if len(note_text) > 500:
            note_text = note_text[:497] + "…"
        cat_author = f"Revue [{ann.category}]"
        cat_initials = CATEGORY_INITIALS.get(ann.category, "RV")
        try:
            document.add_comment(
                runs=[run],
                text=note_text,
                author=cat_author,
                initials=cat_initials,
            )
        except Exception as e:
            print(f"  WARN: comment failed for p{ann.page} '{ann.word[:20]}': {e}")


def _add_page_number_footer(section, template_doc=None):
    """Add page number to footer."""
    footer = section.footer
    footer.is_linked_to_previous = False

    if template_doc:
        tmpl_footer = template_doc.sections[0].footer._element
        for child in list(footer._element):
            footer._element.remove(child)
        for child in tmpl_footer:
            footer._element.append(deepcopy(child))
    else:
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


def main():
    parser = argparse.ArgumentParser(
        description="Génère un DOCX annoté à partir d'un .txt transcrit et d'un rapport."
    )
    parser.add_argument("txt", help="Fichier .txt source (de préférence _revue.txt)")
    parser.add_argument("--rapport", required=True, help="Fichier _rapport.md avec les annotations")
    parser.add_argument("--title", required=True, help="Titre du document")
    parser.add_argument("--author", default="", help="Auteur")
    parser.add_argument("--dates", default="", help="Dates")
    parser.add_argument("--template", help="DOCX modèle (optionnel)")

    args = parser.parse_args()
    generate(args.txt, args.rapport, args.title, args.author, args.dates,
             Path(args.template) if args.template else None)


if __name__ == "__main__":
    main()
