#!/usr/bin/env python3
"""Télécharge les cahiers DOCX depuis Google Drive (Google Docs exportés) vers docs/.

Les 4 cahiers d'Alban Rouzaud sont hébergés comme Google Docs partagés en lecture
publique. Chaque doc s'exporte en DOCX sans authentification via l'endpoint:
    https://docs.google.com/document/d/<ID>/export?format=docx

Le nom de fichier est lu dans l'en-tête Content-Disposition renvoyé par Google,
donc il n'est pas codé en dur ici — si un titre change côté Drive, le fichier
suit automatiquement.

Usage:
    python fetch_gdrive_docx.py                 # tous les cahiers -> docs/ (écrase)
    python fetch_gdrive_docx.py --dest <dir>    # dossier de destination
    python fetch_gdrive_docx.py --dry-run       # affiche sans écrire
    python fetch_gdrive_docx.py 3               # un seul cahier (par numéro)

Écrase les fichiers existants de même nom (comportement voulu: Drive fait foi).
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# Numéro de cahier -> ID Google Docs. Source: README.md du repo.
CAHIERS: dict[str, str] = {
    "1": "1cuSB04MSC8-Fyp5qBXDpXo0cc8VR9cs4",  # La Guerre (1939-1940)
    "2": "1CJ_H8KuLxS6C2K5QgyMGPXW4mBOQLGyT",  # Journal non écrit d'un fantassin
    "3": "1LlsB4U3KwqlwQ5cNaj8wKaccrTnL7hu0",  # L'Évasion
    "4": "12HeGY9vhKJKc71NK3ajLXALOVU3sg5kk",  # Captivité, récits et réflexions
}

EXPORT_URL = "https://docs.google.com/document/d/{id}/export?format=docx"


def _filename_from_disposition(disposition: str | None, fallback: str) -> str:
    """Extrait le nom de fichier propre de l'en-tête Content-Disposition.

    Préfère le paramètre RFC 5987 filename*=UTF-8''... (avec espaces/accents),
    sinon retombe sur filename="...", sinon sur le fallback.
    """
    if not disposition:
        return fallback
    # filename*=UTF-8''NOM%20PERCENT%20ENCODE  (prioritaire: conserve espaces/accents)
    m = re.search(r"filename\*\s*=\s*[^']*''([^;\r\n]+)", disposition, re.IGNORECASE)
    if m:
        return urllib.parse.unquote(m.group(1).strip())
    # filename="..."  (fallback: Google y met une version sans espaces)
    m = re.search(r'filename\s*=\s*"([^"]+)"', disposition, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return fallback


def fetch_one(num: str, doc_id: str, dest: Path, dry_run: bool) -> Path:
    url = EXPORT_URL.format(id=doc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "fetch-gdrive-docx/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        if resp.status != 200:
            raise RuntimeError(f"cahier {num}: HTTP {resp.status} (doc non public ?)")
        name = _filename_from_disposition(
            resp.headers.get("Content-Disposition"), f"cahier_{num}.docx"
        )
        target = dest / name
        if dry_run:
            print(f"[dry-run] cahier {num} -> {target}")
            return target
        data = resp.read()
    if len(data) < 1000:
        raise RuntimeError(f"cahier {num}: réponse trop courte ({len(data)} o), doc privé ?")
    dest.mkdir(parents=True, exist_ok=True)
    existed = target.exists()
    target.write_bytes(data)
    verb = "écrasé" if existed else "créé"
    print(f"cahier {num}: {verb} {target} ({len(data):,} o)")
    return target


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cahier", nargs="?", choices=sorted(CAHIERS), help="numéro d'un seul cahier (défaut: tous)")
    p.add_argument("--dest", default="docs", help="dossier de destination (défaut: docs)")
    p.add_argument("--dry-run", action="store_true", help="affiche sans écrire")
    args = p.parse_args(argv)

    dest = Path(args.dest)
    items = {args.cahier: CAHIERS[args.cahier]} if args.cahier else CAHIERS

    failures = 0
    for num, doc_id in items.items():
        try:
            fetch_one(num, doc_id, dest, args.dry_run)
        except Exception as exc:  # noqa: BLE001
            print(f"ERREUR cahier {num}: {exc}", file=sys.stderr)
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
