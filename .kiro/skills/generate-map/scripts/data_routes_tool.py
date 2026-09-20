#!/usr/bin/env python3
"""
data_routes_tool.py — Mise à jour des routes dans les fichiers data_*.js

Réutilise les fonctions BRouter de brouter_tool.py (fetch_route, route_to_js)
mais cible la structure 'staticRoutes:[...]' des fichiers data_*.js au lieu
du bloc 'var staticRoutes = [...]' des fichiers HTML.

Usage :
    # Lister les routes
    python data_routes_tool.py list --data data/data_c3.js

    # Remplacer une route par index
    python data_routes_tool.py replace --data data/data_c3.js --index 5 \
        --profile fastbike --waypoints "lat1,lng1|lat2,lng2" --period 5

    # Insérer une route à la fin
    python data_routes_tool.py insert --data data/data_c3.js \
        --profile fastbike --waypoints "lat1,lng1|lat2,lng2" --period 5

    # Supprimer une route
    python data_routes_tool.py delete --data data/data_c3.js --index 5

Exemple WP intermédiaire (pont historique) :
    --waypoints "47.1781,14.7109|47.17058,14.66396|47.17431,14.66452"
"""

import sys
import re
import argparse
from pathlib import Path

# ── Importer les fonctions BRouter depuis brouter_tool.py ──────────────────
_here = Path(__file__).parent
sys.path.insert(0, str(_here))
from brouter_tool import fetch_route, route_to_js


# ── Parser pour la structure data_*.js ─────────────────────────────────────

def _find_static_routes_data(src: str):
    """Trouve le bloc staticRoutes:[...] dans un fichier data_*.js.
    
    Retourne (start, end, inner) :
      start : index du début du mot 'staticRoutes'
      end   : index après le ']' fermant (avant la virgule éventuelle)
      inner : contenu entre les crochets [ et ]
    """
    m = re.search(r'\bstaticRoutes\s*:\s*\[', src)
    if not m:
        raise ValueError("Bloc 'staticRoutes:[' non trouvé dans le fichier")

    start = m.start()
    bracket_start = m.end() - 1  # position du [

    depth = 0
    i = bracket_start
    while i < len(src):
        if src[i] == '[':
            depth += 1
        elif src[i] == ']':
            depth -= 1
            if depth == 0:
                break
        i += 1

    bracket_end = i  # position du ] fermant
    end = bracket_end + 1

    inner = src[bracket_start + 1:bracket_end]
    return start, end, inner


def _parse_entries(inner: str):
    """Parse le contenu intérieur du tableau en liste d'entrées (strings)."""
    entries = []
    depth = 0
    current_start = None

    for i, ch in enumerate(inner):
        if ch == '{' and depth == 0:
            current_start = i
            depth = 1
        elif ch == '{':
            depth += 1
        elif ch == '}' and depth == 1:
            depth = 0
            if current_start is not None:
                entries.append(inner[current_start:i + 1])
                current_start = None
        elif ch == '}':
            depth -= 1

    return entries


def _rebuild_array(entries: list, src: str, start: int, end: int) -> str:
    """Reconstruit staticRoutes:[...] et retourne le fichier complet."""
    if not entries:
        new_block = 'staticRoutes:[]'
    else:
        lines = []
        for i, entry in enumerate(entries):
            suffix = ',' if i < len(entries) - 1 else ''
            lines.append(entry + suffix)
        new_block = 'staticRoutes:[\n' + '\n'.join(lines) + '\n]'

    return src[:start] + new_block + src[end:]


# ── Commandes ───────────────────────────────────────────────────────────────

def cmd_list(data_path: str):
    src = Path(data_path).read_text(encoding='utf-8')
    _, _, inner = _find_static_routes_data(src)
    entries = _parse_entries(inner)

    print(f"Fichier : {data_path}")
    print(f"Nombre de routes : {len(entries)}")
    print()
    for i, entry in enumerate(entries):
        p_m = re.search(r'p:(\d+)', entry)
        da_m = re.search(r'da:(\d+)', entry)
        dist_m = re.search(r'distKm:([\d.]+)', entry)
        pts = entry.count('],[') + 1 if 'coords:' in entry else 0
        p = p_m.group(1) if p_m else '?'
        da = 'pointillé' if da_m and da_m.group(1) == '1' else 'plein'
        dist = dist_m.group(1) if dist_m else '?'
        # first and last coord
        coords_m = re.search(r'coords:\[(\[[\d.,]+\])', entry)
        last_m = re.search(r',(\[[\d.,]+\])\]', entry[::-1])
        first = coords_m.group(1) if coords_m else ''
        last = last_m.group(1)[::-1] if last_m else ''
        print(f"  [{i:2d}] p={p} {da:10s} {dist:5s} km  {pts:4d} pts  {first} -> {last}")


def cmd_replace(data_path: str, index: int, waypoints: str, profile: str,
                period: int, dashed: bool):
    src = Path(data_path).read_text(encoding='utf-8')
    start, end, inner = _find_static_routes_data(src)
    entries = _parse_entries(inner)

    if index < 0 or index >= len(entries):
        raise ValueError(f"Index {index} hors limites (0–{len(entries)-1})")

    route = fetch_route(waypoints, profile=profile, dashed=dashed)
    route_js = route_to_js(route, period)
    entries[index] = route_js

    new_src = _rebuild_array(entries, src, start, end)
    Path(data_path).write_text(new_src, encoding='utf-8')
    print(f"Route [{index}] remplacée — {route['distKm']} km, {len(route['coords'])} pts",
          file=sys.stderr)


def cmd_insert(data_path: str, waypoints: str, profile: str,
               period: int, dashed: bool):
    src = Path(data_path).read_text(encoding='utf-8')
    start, end, inner = _find_static_routes_data(src)
    entries = _parse_entries(inner)

    route = fetch_route(waypoints, profile=profile, dashed=dashed)
    route_js = route_to_js(route, period)
    entries.append(route_js)

    new_src = _rebuild_array(entries, src, start, end)
    Path(data_path).write_text(new_src, encoding='utf-8')
    print(f"Route insérée à l'index {len(entries)-1} — {route['distKm']} km",
          file=sys.stderr)


def cmd_delete(data_path: str, index: int):
    src = Path(data_path).read_text(encoding='utf-8')
    start, end, inner = _find_static_routes_data(src)
    entries = _parse_entries(inner)

    if index < 0 or index >= len(entries):
        raise ValueError(f"Index {index} hors limites (0–{len(entries)-1})")

    removed = entries.pop(index)
    new_src = _rebuild_array(entries, src, start, end)
    Path(data_path).write_text(new_src, encoding='utf-8')
    dist_m = re.search(r'distKm:([\d.]+)', removed)
    print(f"Route [{index}] supprimée ({dist_m.group(1) if dist_m else '?'} km)",
          file=sys.stderr)


# ── main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Gestion des routes dans data_*.js')
    sub = parser.add_subparsers(dest='cmd', required=True)

    # list
    p_list = sub.add_parser('list', help='Lister les routes')
    p_list.add_argument('--data', required=True, help='Chemin vers data_*.js')

    # replace
    p_rep = sub.add_parser('replace', help='Remplacer une route')
    p_rep.add_argument('--data', required=True)
    p_rep.add_argument('--index', type=int, required=True)
    p_rep.add_argument('--waypoints', required=True,
                       help='"lat,lng|lat,lng|..." (préfixe s: = ligne droite)')
    p_rep.add_argument('--profile', default='fastbike')
    p_rep.add_argument('--period', type=int, required=True)
    p_rep.add_argument('--dashed', action='store_true')

    # insert
    p_ins = sub.add_parser('insert', help='Insérer une route à la fin')
    p_ins.add_argument('--data', required=True)
    p_ins.add_argument('--waypoints', required=True)
    p_ins.add_argument('--profile', default='fastbike')
    p_ins.add_argument('--period', type=int, required=True)
    p_ins.add_argument('--dashed', action='store_true')

    # delete
    p_del = sub.add_parser('delete', help='Supprimer une route')
    p_del.add_argument('--data', required=True)
    p_del.add_argument('--index', type=int, required=True)

    args = parser.parse_args()

    if args.cmd == 'list':
        cmd_list(args.data)
    elif args.cmd == 'replace':
        cmd_replace(args.data, args.index, args.waypoints,
                    args.profile, args.period, args.dashed)
    elif args.cmd == 'insert':
        cmd_insert(args.data, args.waypoints, args.profile,
                   args.period, args.dashed)
    elif args.cmd == 'delete':
        cmd_delete(args.data, args.index)


if __name__ == '__main__':
    main()
