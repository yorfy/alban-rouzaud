"""
Outil pour récupérer des routes BRouter et les insérer dans les cartes HTML.

Usage:
  # Récupérer une route et afficher le JSON compact
  python brouter_tool.py fetch --profile fastbike --waypoints "48.85,7.32|48.80,7.48"

  # Récupérer et insérer dans un fichier HTML (ajoute en fin de staticRoutes)
  python brouter_tool.py insert --profile trekking --waypoints "42.77,1.505|42.604,1.437" \
      --html carte.html --period 1

  # Ligne droite : préfixer un waypoint par 's:' rend DROIT le segment qui y arrive.
  # Ex. route A->B, ligne droite B->C, route C->D :
  python brouter_tool.py replace --profile trekking \
      --waypoints "A_lat,A_lng|B_lat,B_lng|s:C_lat,C_lng|D_lat,D_lng" \
      --html carte.html --period 2 --index 3

  # Remplacer une route existante (par index 0-based dans staticRoutes)
  python brouter_tool.py replace --profile mtb --waypoints "42.94,1.85|42.86,1.94" \
      --html carte.html --period 1 --index 0

  # Supprimer une route par index
  python brouter_tool.py delete --html carte.html --index 2

  # Lister les routes dans un fichier HTML
  python brouter_tool.py list --html carte.html
"""

import argparse
import json
import math
import re
import sys
import time
import urllib.request


def _haversine_m(a, b):
    """Distance en mètres entre a=[lat,lng] et b=[lat,lng]."""
    R = 6371000.0
    rad = 3.141592653589793 / 180.0
    dlat = (b[0] - a[0]) * rad
    dlng = (b[1] - a[1]) * rad
    la1 = a[0] * rad
    la2 = b[0] * rad
    h = math.sin(dlat / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dlng / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def _straight_points(a, b, step_m=30.0):
    """Segment en ligne droite : points interpolés linéairement de a (exclu) à b (inclus)."""
    d = _haversine_m(a, b)
    n = max(1, int(d // step_m))
    pts = []
    for i in range(1, n + 1):
        f = i / n
        pts.append([round(a[0] + (b[0] - a[0]) * f, 5), round(a[1] + (b[1] - a[1]) * f, 5)])
    return pts


def _parse_waypoint(pair):
    """Retourne (lat, lng, straight) où straight=True si le segment ARRIVANT à ce
    point doit être une ligne droite (préfixe 's:')."""
    pair = pair.strip()
    straight = False
    if pair.lower().startswith("s:"):
        straight = True
        pair = pair[2:]
    parts = pair.split(",")
    if len(parts) != 2:
        raise ValueError(f"Waypoint invalide: {pair}")
    return float(parts[0]), float(parts[1]), straight


def _fetch_brouter_segment(seg_pts, profile):
    """Route un tronçon (liste de [lat,lng]) via BRouter, retourne (coords, dist_m)."""
    lonlats = "|".join(f"{lng},{lat}" for lat, lng in seg_pts)
    url = (
        f"https://brouter.de/brouter?profile={profile}"
        f"&alternativeidx=0&format=geojson&lonlats={lonlats}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "brouter-tool/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    feature = data["features"][0]
    raw = feature["geometry"]["coordinates"]
    coords = [[round(c[1], 5), round(c[0], 5)] for c in raw]
    dist_m = float(feature["properties"]["track-length"])
    return coords, dist_m


def fetch_route(waypoints_str: str, profile: str = "fastbike", dashed: bool = False):
    """Récupère une route et retourne un dict {distKm, coords, dashed}.

    Les waypoints sont "lat,lng" séparés par '|'. Un waypoint préfixé par 's:'
    indique que le segment qui y ARRIVE est une LIGNE DROITE (interpolée), au lieu
    d'être routé par BRouter. On peut ainsi mélanger routage et lignes droites :
        "48.1,7.3|48.0,7.2|s:47.9,7.1|47.8,7.0"
    -> route 1->2, droite 2->3, route 3->4.
    """
    wps = [_parse_waypoint(p) for p in waypoints_str.split("|")]
    if len(wps) < 2:
        raise ValueError("Il faut au moins 2 waypoints")

    print(f"  Route ({profile}) : {len(wps)} waypoints "
          f"({sum(1 for w in wps if w[2])} segment(s) droit(s))...", file=sys.stderr)

    coords = [[wps[0][0], wps[0][1]]]
    # On accumule les waypoints routés consécutifs pour minimiser les appels BRouter.
    pending = [[wps[0][0], wps[0][1]]]  # points à router ensemble

    def flush_routed():
        if len(pending) >= 2:
            seg_coords, _ = _fetch_brouter_segment(pending, profile)
            for c in seg_coords:
                if c != coords[-1]:
                    coords.append(c)

    for k in range(1, len(wps)):
        lat, lng, straight = wps[k]
        pt = [lat, lng]
        if straight:
            flush_routed()          # router le tronçon en attente jusqu'ici
            for c in _straight_points(coords[-1], pt):  # puis ligne droite
                if c != coords[-1]:
                    coords.append(c)
            pending[:] = [pt]       # repartir de ce point pour la suite
        else:
            pending.append(pt)
    flush_routed()

    # distance totale mesurée sur la polyligne finale (routage + droites)
    total_m = sum(_haversine_m(coords[i - 1], coords[i]) for i in range(1, len(coords)))
    dist_km = round(total_m / 1000, 1)
    print(f"  -> {len(coords)} points, {dist_km} km", file=sys.stderr)
    return {"distKm": dist_km, "coords": coords, "dashed": dashed}


def route_to_js(route: dict, period: int) -> str:
    """Convertit un dict route en entrée JavaScript pour staticRoutes."""
    da = 1 if route["dashed"] else 0
    coords_str = json.dumps(route["coords"], separators=(",", ":"))
    return f"{{p:{period},da:{da},distKm:{route['distKm']},coords:{coords_str}}}"


# --- Manipulation du HTML ---

def _find_static_routes(html: str):
    """Trouve le bloc var staticRoutes = [...]; et retourne (start, end, contenu)."""
    # Cherche "var staticRoutes = [" puis le "];" correspondant
    m = re.search(r"var\s+staticRoutes\s*=\s*\[", html)
    if not m:
        raise ValueError("Bloc 'var staticRoutes = [' non trouvé dans le HTML")
    
    start = m.start()
    bracket_start = m.end() - 1  # position du [
    
    # Trouver le ] fermant (gestion des crochets imbriqués dans les coords)
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
    
    bracket_end = i  # position du ] fermant
    # Chercher le ; après
    end = bracket_end + 1
    while end < len(html) and html[end] in " \t\n\r":
        end += 1
    if end < len(html) and html[end] == ";":
        end += 1
    
    inner = html[bracket_start + 1:bracket_end]
    return start, end, inner


def _parse_entries(inner: str):
    """Parse le contenu intérieur du tableau staticRoutes en liste d'entrées (strings)."""
    entries = []
    depth = 0
    current_start = None
    
    for i, ch in enumerate(inner):
        if ch == "{" and depth == 0:
            current_start = i
            depth = 1
        elif ch == "{":
            depth += 1
        elif ch == "}" and depth == 1:
            depth = 0
            if current_start is not None:
                entries.append(inner[current_start:i + 1])
                current_start = None
        elif ch == "}":
            depth -= 1
    
    return entries


def _rebuild_array(entries: list) -> str:
    """Reconstruit le bloc var staticRoutes = [...]; à partir d'une liste d'entrées JS."""
    if not entries:
        return "var staticRoutes = [];"
    
    lines = []
    for i, entry in enumerate(entries):
        suffix = "," if i < len(entries) - 1 else ""
        lines.append(entry + suffix)
    
    return "var staticRoutes = [\n" + "\n".join(lines) + "\n];"


def list_routes(html_path: str):
    """Affiche les routes contenues dans le fichier HTML."""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    _, _, inner = _find_static_routes(html)
    entries = _parse_entries(inner)
    
    print(f"Fichier: {html_path}")
    print(f"Nombre de routes: {len(entries)}")
    print()
    
    for i, entry in enumerate(entries):
        # Extraire les métadonnées
        p_match = re.search(r"p:(\d+)", entry)
        da_match = re.search(r"da:(\d+)", entry)
        dist_match = re.search(r"distKm:([\d.]+)", entry)
        # Compter les coordonnées
        coord_count = entry.count("],[") + 1 if "coords:" in entry else 0
        
        p = p_match.group(1) if p_match else "?"
        da = "pointillé" if da_match and da_match.group(1) == "1" else "plein"
        dist = dist_match.group(1) if dist_match else "?"
        
        print(f"  [{i}] période={p}, {da}, {dist} km, {coord_count} points")


def insert_route(html_path: str, route_js: str):
    """Ajoute une route en fin de staticRoutes."""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    start, end, inner = _find_static_routes(html)
    entries = _parse_entries(inner)
    entries.append(route_js)
    
    new_block = _rebuild_array(entries)
    html = html[:start] + new_block + html[end:]
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"  Route ajoutée (index {len(entries) - 1})", file=sys.stderr)


def replace_route(html_path: str, index: int, route_js: str):
    """Remplace une route existante par index."""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    start, end, inner = _find_static_routes(html)
    entries = _parse_entries(inner)
    
    if index < 0 or index >= len(entries):
        raise ValueError(f"Index {index} hors limites (0-{len(entries) - 1})")
    
    entries[index] = route_js
    
    new_block = _rebuild_array(entries)
    html = html[:start] + new_block + html[end:]
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"  Route [{index}] remplacée", file=sys.stderr)


def delete_route(html_path: str, index: int):
    """Supprime une route par index."""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    start, end, inner = _find_static_routes(html)
    entries = _parse_entries(inner)
    
    if index < 0 or index >= len(entries):
        raise ValueError(f"Index {index} hors limites (0-{len(entries) - 1})")
    
    removed = entries.pop(index)
    dist_match = re.search(r"distKm:([\d.]+)", removed)
    dist = dist_match.group(1) if dist_match else "?"
    
    new_block = _rebuild_array(entries)
    html = html[:start] + new_block + html[end:]
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"  Route [{index}] supprimée ({dist} km)", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Outil BRouter pour cartes HTML")
    sub = parser.add_subparsers(dest="command", required=True)

    # fetch
    p_fetch = sub.add_parser("fetch", help="Récupérer une route BRouter")
    p_fetch.add_argument("--profile", default="fastbike", help="Profil BRouter (fastbike, trekking, mtb...)")
    p_fetch.add_argument("--waypoints", required=True, help="Waypoints: lat1,lng1|lat2,lng2|...")
    p_fetch.add_argument("--dashed", action="store_true", help="Tracé pointillé")

    # insert
    p_ins = sub.add_parser("insert", help="Récupérer et insérer une route")
    p_ins.add_argument("--profile", default="fastbike")
    p_ins.add_argument("--waypoints", required=True)
    p_ins.add_argument("--html", required=True, help="Fichier HTML cible")
    p_ins.add_argument("--period", type=int, required=True, help="Numéro de période (couleur)")
    p_ins.add_argument("--dashed", action="store_true")

    # replace
    p_rep = sub.add_parser("replace", help="Récupérer et remplacer une route")
    p_rep.add_argument("--profile", default="fastbike")
    p_rep.add_argument("--waypoints", required=True)
    p_rep.add_argument("--html", required=True)
    p_rep.add_argument("--period", type=int, required=True)
    p_rep.add_argument("--index", type=int, required=True, help="Index de la route à remplacer")
    p_rep.add_argument("--dashed", action="store_true")

    # delete
    p_del = sub.add_parser("delete", help="Supprimer une route")
    p_del.add_argument("--html", required=True)
    p_del.add_argument("--index", type=int, required=True)

    # list
    p_list = sub.add_parser("list", help="Lister les routes")
    p_list.add_argument("--html", required=True)

    args = parser.parse_args()

    if args.command == "fetch":
        route = fetch_route(args.waypoints, args.profile, args.dashed)
        print(json.dumps({"distKm": route["distKm"], "points": len(route["coords"])}))

    elif args.command == "insert":
        route = fetch_route(args.waypoints, args.profile, args.dashed)
        js = route_to_js(route, args.period)
        insert_route(args.html, js)

    elif args.command == "replace":
        route = fetch_route(args.waypoints, args.profile, args.dashed)
        js = route_to_js(route, args.period)
        replace_route(args.html, args.index, js)

    elif args.command == "delete":
        delete_route(args.html, args.index)

    elif args.command == "list":
        list_routes(args.html)


if __name__ == "__main__":
    main()
