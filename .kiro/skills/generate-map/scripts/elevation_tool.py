"""
Génère (ou régénère) le profil d'altitude d'une carte HTML.

Lit le tableau `staticRoutes` du HTML, chaîne les tracés PLEINS (da=0) dans
l'ordre du parcours à pied, échantillonne les points, interroge un service
d'élévation (OpenTopoData SRTM30m par défaut), puis injecte/actualise un
tableau JS `elevProfile` dans le HTML.

Format injecté :
    var elevProfile = [ {p: <phase>, pts: [[distKm, alt, lat, lng], ...]}, ... ];
- distKm : distance cumulée depuis le début du parcours (km)
- alt    : altitude en mètres
- lat,lng: coordonnées du point (pour l'interaction carte <-> courbe)

Le rendu graphique (canvas + interactions) est ajouté séparément dans le HTML ;
ce script ne s'occupe QUE des données. Relancer après toute modification des
tracés met simplement le profil à jour.

Mise à jour incrémentale :
    Par défaut, les altitudes déjà présentes dans le `elevProfile` existant sont
    réutilisées (cache par coordonnée). Seuls les points nouveaux (issus d'un
    tracé modifié/ajouté) déclenchent une requête réseau. Le chaînage et les
    distances cumulées sont toujours recalculés localement, donc le profil reste
    cohérent même quand un segment change de longueur. Utiliser --force-refetch
    pour tout recalculer via le réseau.

Usage :
    python elevation_tool.py build --html CARTE.html
    python elevation_tool.py build --html CARTE.html --sample 150 --max-chain-gap 3000
    python elevation_tool.py build --html CARTE.html --include-dashed   # inclure aussi les pointillés
    python elevation_tool.py build --html CARTE.html --only-phases 2,3  # limiter à certaines phases
    python elevation_tool.py build --html CARTE.html --force-refetch    # tout re-interroger

Options :
    --sample N          distance (m) entre points échantillonnés (défaut 150)
    --max-chain-gap M   écart max (m) entre extrémités pour chaîner deux tracés (défaut 3000)
    --include-dashed    inclure aussi les tracés pointillés (da=1) dans le profil
    --only-phases LIST  ne (re)traiter que ces phases (ex: "2,3") ; les autres
                        segments du profil existant sont conservés tels quels
    --force-refetch     ignorer le cache et re-interroger toutes les altitudes
    --provider P        service d'élévation : opentopodata (défaut) | opentopodata-aster
    --batch N           taille de lot pour les requêtes (défaut 100)
    --pause S           pause (s) entre requêtes (défaut 1.1, requis par le service public)
"""

import argparse
import json
import math
import re
import sys
import time
import urllib.parse
import urllib.request


# --------- Géométrie ---------

def haversine(a, b):
    """Distance en mètres entre a=[lat,lng] et b=[lat,lng]."""
    R = 6371000.0
    rad = math.pi / 180.0
    dlat = (b[0] - a[0]) * rad
    dlng = (b[1] - a[1]) * rad
    la1 = a[0] * rad
    la2 = b[0] * rad
    h = math.sin(dlat / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dlng / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


# --------- Lecture du HTML ---------

def _find_array(html, varname):
    """Retourne (start, end, inner) du tableau `var <varname> = [ ... ];`."""
    m = re.search(r"var\s+" + re.escape(varname) + r"\s*=\s*\[", html)
    if not m:
        raise ValueError(f"Bloc 'var {varname} = [' non trouvé")
    bracket_start = m.end() - 1
    depth = 0
    i = bracket_start
    while i < len(html):
        if html[i] == "[":
            depth += 1
        elif html[i] == "]":
            depth -= 1
            if depth == 0:
                break
        i += 1
    bracket_end = i
    end = bracket_end + 1
    while end < len(html) and html[end] in " \t\n\r":
        end += 1
    if end < len(html) and html[end] == ";":
        end += 1
    return m.start(), end, html[bracket_start + 1:bracket_end]


def _parse_routes(inner):
    """Parse le contenu de staticRoutes en liste de dicts {p, da, coords}."""
    routes = []
    depth = 0
    start = None
    for i, ch in enumerate(inner):
        if ch == "{" and depth == 0:
            start = i
            depth = 1
        elif ch == "{":
            depth += 1
        elif ch == "}" and depth == 1:
            depth = 0
            entry = inner[start:i + 1]
            routes.append(_parse_one_route(entry))
    return routes


def _parse_one_route(entry):
    p = re.search(r"\bp:\s*(\d+)", entry)
    da = re.search(r"\bda:\s*(\d+)", entry)
    repl = re.search(r"__replaced\s*:\s*true", entry)
    cm = re.search(r"coords:\s*(\[\[.*?\]\])", entry, re.S)
    coords = json.loads(cm.group(1)) if cm else []
    return {
        "p": int(p.group(1)) if p else 0,
        "da": int(da.group(1)) if da else 0,
        "replaced": bool(repl),
        "coords": coords,
    }


# --------- Chaînage des tracés ---------

def chain_routes(routes, include_dashed=False, max_gap=3000.0):
    """Chaîne les tracés dans l'ordre du parcours en partant de la phase la plus
    basse, en reliant à chaque étape le tracé dont une extrémité est la plus
    proche de la fin courante. Retourne une liste de dicts {p, coords}."""
    pool = [
        {"p": r["p"], "coords": [list(c) for c in r["coords"]]}
        for r in routes
        if not r["replaced"] and (include_dashed or r["da"] == 0) and len(r["coords"]) >= 2
    ]
    if not pool:
        return []

    # Point de départ : tracé de la plus petite phase
    min_p = min(r["p"] for r in pool)
    start = next(r for r in pool if r["p"] == min_p)
    used = {id(start)}
    chain = [start]
    tail = start["coords"][-1]

    while True:
        best = None
        best_d = float("inf")
        best_rev = False
        for r in pool:
            if id(r) in used:
                continue
            h = r["coords"][0]
            t = r["coords"][-1]
            dh = haversine(tail, h)
            dt = haversine(tail, t)
            if dh < best_d:
                best_d, best, best_rev = dh, r, False
            if dt < best_d:
                best_d, best, best_rev = dt, r, True
        if best is None or best_d > max_gap:
            break
        used.add(id(best))
        if best_rev:
            best["coords"].reverse()
        chain.append(best)
        tail = best["coords"][-1]

    return chain


# --------- Échantillonnage ---------

def sample_chain(chain, step_m=150.0):
    """Retourne (segments, samples) où :
    - segments = [{p, pts:[[distKm, None(alt), lat, lng], ...]}]
    - samples  = [(seg_index, pt_index, lat, lng)]  pour requêtes d'élévation
    La distance cumulée est globale (continue d'un segment au suivant)."""
    segments = []
    samples = []
    cum = 0.0
    prev = None

    for seg in chain:
        co = seg["coords"]
        sampled = [co[0]]
        acc = 0.0
        for k in range(1, len(co)):
            acc += haversine(co[k - 1], co[k])
            if acc >= step_m or k == len(co) - 1:
                sampled.append(co[k])
                acc = 0.0
        seg_obj = {"p": seg["p"], "pts": []}
        for pt in sampled:
            if prev is not None:
                cum += haversine(prev, pt)
            prev = pt
            samples.append((len(segments), len(seg_obj["pts"]), pt[0], pt[1]))
            seg_obj["pts"].append([round(cum / 1000, 3), None,
                                   round(pt[0], 5), round(pt[1], 5)])
        segments.append(seg_obj)

    return segments, cum / 1000.0


# --------- Service d'élévation ---------

def fetch_elevations(latlngs, provider="opentopodata", batch=100, pause=1.1):
    """Retourne la liste des altitudes (m) pour latlngs=[[lat,lng], ...]."""
    dataset = {"opentopodata": "srtm30m", "opentopodata-aster": "aster30m"}.get(provider, "srtm30m")
    out = []
    total = (len(latlngs) + batch - 1) // batch
    for bi in range(0, len(latlngs), batch):
        chunk = latlngs[bi:bi + batch]
        locs = "|".join(f"{lat:.5f},{lng:.5f}" for lat, lng in chunk)
        data = urllib.parse.urlencode({"locations": locs}).encode()
        url = f"https://api.opentopodata.org/v1/{dataset}"
        req = urllib.request.Request(url, data=data,
                                     headers={"User-Agent": "elevation-tool/1.0"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    j = json.loads(resp.read())
                if j.get("status") != "OK":
                    raise RuntimeError(j.get("error", j.get("status")))
                out.extend(r["elevation"] for r in j["results"])
                break
            except Exception as e:
                if attempt == 3:
                    raise
                print(f"    retry ({e})", file=sys.stderr)
                time.sleep(2 + attempt)
        print(f"  batch {bi // batch + 1}/{total} ok", file=sys.stderr)
        time.sleep(pause)
    return out


# --------- Cache d'altitudes (profil existant) ---------

def _coord_key(lat, lng):
    """Clé de cache stable sur 5 décimales (≈1 m), cohérente avec l'arrondi
    utilisé lors de l'échantillonnage."""
    return (round(lat, 5), round(lng, 5))


def load_elevation_cache(html):
    """Lit le `elevProfile` existant et retourne {(lat,lng): alt} pour réutiliser
    les altitudes déjà calculées. Retourne {} si aucun profil n'existe."""
    m = re.search(r"var\s+elevProfile\s*=\s*(\[.*?\]);", html, re.S)
    if not m:
        return {}
    try:
        profile = json.loads(m.group(1))
    except json.JSONDecodeError:
        return {}
    cache = {}
    for seg in profile:
        for pt in seg.get("pts", []):
            # pt = [distKm, alt, lat, lng]
            if len(pt) >= 4 and pt[1] is not None:
                cache[_coord_key(pt[2], pt[3])] = pt[1]
    return cache


def load_existing_profile(html):
    """Retourne le `elevProfile` existant (liste de segments) ou None."""
    m = re.search(r"var\s+elevProfile\s*=\s*(\[.*?\]);", html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


# --------- Injection dans le HTML ---------

def inject(html, segments):
    js = "var elevProfile = " + json.dumps(segments, separators=(",", ":")) + ";"
    if re.search(r"var\s+elevProfile\s*=", html):
        return re.sub(r"var\s+elevProfile\s*=\s*\[.*?\];", js, html, count=1, flags=re.S)
    # sinon, insérer juste après staticRoutes = [...];
    _, end, _ = _find_array(html, "staticRoutes")
    return html[:end] + "\n" + js + html[end:]


# --------- CLI ---------

def build(args):
    with open(args.html, "r", encoding="utf-8") as f:
        html = f.read()

    only_phases = None
    if args.only_phases:
        only_phases = {int(x) for x in args.only_phases.split(",") if x.strip()}

    _, _, inner = _find_array(html, "staticRoutes")
    routes = _parse_routes(inner)
    chain = chain_routes(routes, include_dashed=args.include_dashed,
                         max_gap=args.max_chain_gap)
    n_solid = sum(1 for r in routes if not r["replaced"]
                  and (args.include_dashed or r["da"] == 0))
    print(f"Segments chaînés : {len(chain)} / {n_solid} éligibles", file=sys.stderr)

    segments, total_km = sample_chain(chain, step_m=args.sample)
    n_pts = sum(len(s["pts"]) for s in segments)
    print(f"Points échantillonnés : {n_pts} | distance totale : {total_km:.1f} km",
          file=sys.stderr)

    # Cache d'altitudes issu du profil existant (sauf si --force-refetch)
    cache = {} if args.force_refetch else load_elevation_cache(html)
    if cache:
        print(f"Cache d'altitudes : {len(cache)} points connus", file=sys.stderr)

    # Remplir depuis le cache ; ne collecter que les points manquants
    latlngs = []
    index = []
    hits = 0
    for si, seg in enumerate(segments):
        # Si on limite à certaines phases, on ne (re)fetch pas les autres :
        # on essaie de les remplir par le cache, sinon on laisse tel quel.
        restrict = only_phases is not None and seg["p"] not in only_phases
        for pi, pt in enumerate(seg["pts"]):
            cached = cache.get(_coord_key(pt[2], pt[3]))
            if cached is not None:
                pt[1] = cached
                hits += 1
            elif restrict:
                # Phase hors périmètre et absente du cache : altitude inconnue,
                # laissée à None (le rendu ignore les points None).
                pt[1] = None
            else:
                latlngs.append([pt[2], pt[3]])
                index.append((si, pi))

    print(f"Réutilisés depuis le cache : {hits} | à interroger : {len(latlngs)}",
          file=sys.stderr)

    if latlngs:
        alts = fetch_elevations(latlngs, provider=args.provider,
                                batch=args.batch, pause=args.pause)
        for (si, pi), alt in zip(index, alts):
            segments[si]["pts"][pi][1] = alt
    else:
        print("  aucune requête réseau nécessaire", file=sys.stderr)

    html = inject(html, segments)
    with open(args.html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"elevProfile injecté : {len(segments)} segments, {n_pts} points",
          file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Profil d'altitude pour cartes HTML")
    sub = ap.add_subparsers(dest="command", required=True)

    b = sub.add_parser("build", help="Construire/actualiser elevProfile")
    b.add_argument("--html", required=True)
    b.add_argument("--sample", type=float, default=150.0,
                   help="Distance (m) entre points échantillonnés")
    b.add_argument("--max-chain-gap", type=float, default=3000.0,
                   help="Écart max (m) pour chaîner deux tracés")
    b.add_argument("--include-dashed", action="store_true",
                   help="Inclure aussi les tracés pointillés")
    b.add_argument("--only-phases", default=None,
                   help="Ne (re)traiter que ces phases, ex: '2,3'")
    b.add_argument("--force-refetch", action="store_true",
                   help="Ignorer le cache et re-interroger toutes les altitudes")
    b.add_argument("--provider", default="opentopodata",
                   choices=["opentopodata", "opentopodata-aster"])
    b.add_argument("--batch", type=int, default=100)
    b.add_argument("--pause", type=float, default=1.1)

    args = ap.parse_args()
    if args.command == "build":
        build(args)


if __name__ == "__main__":
    main()
