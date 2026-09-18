"""
scrape_photos_ariege.py
-----------------------
Cherche et télécharge des photos domaine public pour la carte Alban Rouzaud.

Sources :
  - Wikimedia Commons : fonds Trutat (Ariège, ~1880-1910) + autres catégories
  - Filtre : domaine public uniquement, pertinence Ariège / textile / bergers

Usage :
    python scripts/scrape_photos_ariege.py

Les images sont sauvegardées dans cartes_postales/
Un rapport est écrit dans scripts/rapport_photos.md
"""

import urllib.request
import urllib.parse
import json
import time
import os
import re
import sys

DEST_DIR   = os.path.join(os.path.dirname(__file__), "..", "cartes_postales")
REPORT_FILE = os.path.join(os.path.dirname(__file__), "rapport_photos.md")

HEADERS = {
    "User-Agent": "AlbanRouzaudMap/1.0 (educational non-commercial project; github.com/yorfy/alban-rouzaud)"
}

# ──────────────────────────────────────────────
# Requêtes Wikimedia API
# ──────────────────────────────────────────────

def wiki_api(params):
    """Appel GET à l'API Wikimedia Commons avec gestion du rate-limiting."""
    base = "https://commons.wikimedia.org/w/api.php"
    params["format"] = "json"
    url = base + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            if "429" in str(e) or "Too many" in str(e):
                wait = 10 * (attempt + 1)
                print(f"  [rate limit] attente {wait}s…")
                time.sleep(wait)
            else:
                print(f"  [erreur API] {e}")
                return None
    return None


def get_image_url(filename):
    """Retourne l'URL directe de l'image via l'API imageinfo."""
    data = wiki_api({
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
    })
    if not data:
        return None
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        ii = page.get("imageinfo", [])
        if ii:
            return ii[0].get("url")
    return None


def search_category(category, limit=20):
    """Liste les fichiers d'une catégorie Commons."""
    data = wiki_api({
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmtype": "file",
        "cmlimit": limit,
    })
    if not data:
        return []
    return [m["title"].replace("File:", "") for m in data.get("query", {}).get("categorymembers", [])]


def search_files(query, limit=20):
    """Recherche textuelle dans Commons (espace fichiers)."""
    data = wiki_api({
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": "6",   # namespace File
        "srlimit": limit,
    })
    if not data:
        return []
    return [h["title"].replace("File:", "") for h in data.get("query", {}).get("search", [])]


# ──────────────────────────────────────────────
# Téléchargement
# ──────────────────────────────────────────────

def download_image(url, dest_path):
    """Télécharge une image avec délai et User-Agent. Retourne True si OK."""
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            if len(data) < 5000:
                print(f"  [trop petit] {len(data)} octets — ignoré")
                return False
            with open(dest_path, "wb") as f:
                f.write(data)
            return True
        except Exception as e:
            if "429" in str(e):
                wait = 15 * (attempt + 1)
                print(f"  [rate limit] attente {wait}s…")
                time.sleep(wait)
            else:
                print(f"  [erreur DL] {e}")
                return False
    return False


def safe_filename(title):
    """Transforme un titre Commons en nom de fichier sûr."""
    name = re.sub(r"[^\w\-\.éèêëàâùûüîïôœçæ]", "_", title)
    name = re.sub(r"_+", "_", name).strip("_")
    # Garde l'extension originale
    ext = os.path.splitext(title)[1].lower() or ".jpg"
    if not name.endswith(ext):
        name = os.path.splitext(name)[0] + ext
    return name


# ──────────────────────────────────────────────
# Cibles de recherche
# ──────────────────────────────────────────────

SEARCHES = [
    # (type, requête, description)

    # Trutat – photos Ariège domaine public
    ("search", "Trutat Ariège", "Trutat – photos Ariège"),
    ("search", "Trutat Vicdessos", "Trutat – Vicdessos"),
    ("search", "Trutat berger Pyrénées", "Trutat – bergers Pyrénées"),
    ("search", "Trutat estive Pyrénées", "Trutat – estives"),
    ("search", "Trutat tissage filature", "Trutat – industrie textile"),

    # Catégories pertinentes
    ("category", "Photographs_by_Eugène_Trutat", "Trutat – catégorie générale"),

    # Autres fonds domaine public
    ("search", "Lavelanet 1900 filature", "Lavelanet filature"),
    ("search", "Pays d'Olmes textile Ariège", "Pays d'Olmes textile"),
    ("search", "Ariège berger montagne 1900 1910", "Ariège bergers"),
    ("search", "Tarascon-sur-Ariège ancienne photo", "Tarascon CPA"),
    ("search", "orri cabane berger Pyrénées Ariège", "Orris Ariège"),
    ("search", "Vicdessos vallée montagne Ariège", "Vicdessos"),
    ("search", "Soulcem Auzat Ariège estive", "Soulcem estive"),
]

# Mots-clés qui indiquent une pertinence pour le projet
RELEVANT_KEYWORDS = [
    "ariège", "ariege", "pyrénées", "pyrenees", "lavelanet", "vicdessos",
    "tarascon", "foix", "tissage", "tisserand", "filature", "laine",
    "berger", "estive", "orri", "montagne", "pays d'olmes",
    "trutat",
]

def is_relevant(title):
    """Heuristique simple : le titre contient-il un mot-clé pertinent ?"""
    t = title.lower()
    return any(k in t for k in RELEVANT_KEYWORDS)


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    os.makedirs(DEST_DIR, exist_ok=True)

    downloaded = []
    skipped    = []
    seen       = set()

    print("=== Scraping photos Ariège – domaine public ===\n")

    for (stype, query, label) in SEARCHES:
        print(f"\n▶ {label} [{stype}]")
        time.sleep(2)  # politesse entre requêtes

        if stype == "search":
            files = search_files(query, limit=15)
        else:
            files = search_category(query, limit=30)

        print(f"  {len(files)} résultat(s)")

        for filename in files:
            if filename in seen:
                continue
            seen.add(filename)

            # Filtre de pertinence sur le nom de fichier
            if stype != "category" and not is_relevant(filename):
                print(f"  ✗ non pertinent : {filename[:60]}")
                skipped.append((filename, "non pertinent"))
                continue

            # Nom de fichier local
            local_name = safe_filename(filename)
            dest = os.path.join(DEST_DIR, local_name)

            # Déjà téléchargé ?
            if os.path.exists(dest):
                print(f"  ✓ déjà présent : {local_name}")
                downloaded.append((filename, local_name, "déjà présent"))
                continue

            # Récupère l'URL directe
            print(f"  → {filename[:70]}")
            time.sleep(1)
            url = get_image_url(filename)
            if not url:
                print("    [URL introuvable]")
                skipped.append((filename, "URL introuvable"))
                continue

            # Filtre mime : images seulement
            if not any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif"]):
                print(f"    [format ignoré] {url[-20:]}")
                skipped.append((filename, "format non image"))
                continue

            # Téléchargement
            time.sleep(2)
            ok = download_image(url, dest)
            if ok:
                size_kb = os.path.getsize(dest) // 1024
                print(f"    ✓ téléchargé ({size_kb} KB) → {local_name}")
                downloaded.append((filename, local_name, f"{size_kb} KB"))
            else:
                skipped.append((filename, "échec téléchargement"))
                if os.path.exists(dest):
                    os.remove(dest)  # fichier incomplet

    # ── Rapport ──────────────────────────────
    print(f"\n=== Terminé : {len([d for d in downloaded if d[2] != 'déjà présent'])} nouvelles images ===")

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# Rapport scraping photos Ariège – domaine public\n\n")
        f.write(f"**{len(downloaded)} images téléchargées / déjà présentes**\n\n")
        f.write("## Images récupérées\n\n")
        f.write("| Fichier local | Taille | Source Commons |\n")
        f.write("|---|---|---|\n")
        for (orig, local, info) in downloaded:
            f.write(f"| `{local}` | {info} | {orig} |\n")
        f.write("\n## Ignorées / échecs\n\n")
        for (orig, reason) in skipped:
            f.write(f"- `{orig[:80]}` — {reason}\n")

    print(f"Rapport écrit : scripts/rapport_photos.md")


if __name__ == "__main__":
    main()
