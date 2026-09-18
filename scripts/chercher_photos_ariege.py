"""
chercher_photos_ariege.py
--------------------------
ÉTAPE 1 : Cherche (sans télécharger) des photos domaine public sur Wikimedia Commons
pertinentes pour la carte Alban Rouzaud (Ariège, textile, bergers, orris).

Produit : scripts/candidats_photos.md  — liste commentée pour validation humaine.

Usage :
    python scripts/chercher_photos_ariege.py
"""

import urllib.request
import urllib.parse
import json
import time
import os

REPORT_FILE = os.path.join(os.path.dirname(__file__), "candidats_photos.md")

HEADERS = {
    "User-Agent": "AlbanRouzaudMap/1.0 (educational non-commercial)"
}

REQUETES = [
    # Recherches très ciblées — max 8 résultats chacune
    ("Trutat Ariège village montagne",              "Villages ariégeois – Trutat"),
    ("Trutat berger Pyrénées moutons",              "Bergers pyrénéens – Trutat"),
    ("Trutat vallée Vicdessos Auzat",               "Vallée du Vicdessos – Trutat"),
    ("Tarascon-sur-Ariège ancienne photographie",   "Tarascon-sur-Ariège"),
    ("Lavelanet Ariège carte postale 1910",         "Lavelanet CPA"),
    ("orri cabane pierre berger Pyrénées Ariège",   "Orris Pyrénées"),
    ("filature tissage laine Pyrénées 1900",        "Textile pyrénéen"),
]


def wiki_api_call(url):
    """Appel API avec backoff exponentiel sur 429."""
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            if "429" in str(e) or "Too Many" in str(e):
                wait = 30 * (2 ** attempt)  # 30, 60, 120, 240, 480s
                print(f"  [429] ban temporaire — attente {wait}s…")
                time.sleep(wait)
            else:
                print(f"  Erreur: {e}")
                return None
    return None


def wiki_search(query, limit=8):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": "6",
        "srlimit": limit,
        "format": "json",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    data = wiki_api_call(url)
    if not data:
        return []
    return [h["title"].replace("File:", "") for h in data.get("query", {}).get("search", [])]


def get_imageinfo(filename):
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata",
        "iiextmetadatafilter": "LicenseShortName|ImageDescription|DateTimeOriginal|Artist",
        "format": "json",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    data = wiki_api_call(url)
    if not data:
        return None
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        ii = page.get("imageinfo", [])
        if ii:
            meta = ii[0].get("extmetadata", {})
            return {
                "url":     ii[0].get("url", ""),
                "w":       ii[0].get("width", 0),
                "h":       ii[0].get("height", 0),
                "license": meta.get("LicenseShortName", {}).get("value", "?"),
                "desc":    meta.get("ImageDescription", {}).get("value", "")[:120],
                "date":    meta.get("DateTimeOriginal", {}).get("value", "?"),
                "artist":  meta.get("Artist", {}).get("value", "?")[:80],
            }
    return None


def is_public_domain(license_str):
    lic = license_str.lower()
    return any(k in lic for k in ["public domain", "pd", "cc0", "cc-zero", "no restrictions"])


def main():
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    results = []
    seen = set()

    print("=== Recherche photos Ariège – domaine public ===")
    print("Pause initiale 30s pour éviter le rate-limiting…\n")
    time.sleep(30)

    for (query, label) in REQUETES:
        print(f"\n▶ {label}")
        time.sleep(5)
        files = wiki_search(query)
        print(f"  {len(files)} trouvé(s)")

        for fname in files:
            if fname in seen:
                continue
            seen.add(fname)
            time.sleep(3)

            info = get_imageinfo(fname)
            if not info:
                continue

            # Filtre : domaine public uniquement + taille minimum décente
            if not is_public_domain(info["license"]):
                print(f"  ✗ {info['license']:15s}  {fname[:55]}")
                continue
            if info["w"] < 400 or info["h"] < 400:
                print(f"  ✗ trop petit {info['w']}x{info['h']}  {fname[:50]}")
                continue

            print(f"  ✓ {info['license']:15s}  {fname[:55]}")
            results.append({
                "label":   label,
                "fname":   fname,
                "url":     info["url"],
                "size":    f"{info['w']}×{info['h']}",
                "license": info["license"],
                "date":    info["date"],
                "artist":  info["artist"],
                "desc":    info["desc"],
            })

    # Rapport
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# Candidats photos Ariège – domaine public\n\n")
        f.write(f"**{len(results)} images domaine public trouvées** — valide les lignes à télécharger.\n\n")
        f.write("Pour télécharger une image : note son numéro et dis-le moi.\n\n")

        for i, r in enumerate(results, 1):
            f.write(f"---\n\n")
            f.write(f"### {i}. {r['fname'][:70]}\n\n")
            f.write(f"- **Catégorie** : {r['label']}\n")
            f.write(f"- **Licence** : {r['license']}\n")
            f.write(f"- **Taille** : {r['size']}\n")
            f.write(f"- **Date** : {r['date']}\n")
            f.write(f"- **Auteur** : {r['artist']}\n")
            f.write(f"- **Description** : {r['desc']}\n")
            f.write(f"- **URL** : {r['url']}\n\n")

    print(f"\n=== {len(results)} candidats écrits dans scripts/candidats_photos.md ===")
    print("Ouvre ce fichier, note les numéros qui t'intéressent, je télécharge ensuite.")


if __name__ == "__main__":
    main()
