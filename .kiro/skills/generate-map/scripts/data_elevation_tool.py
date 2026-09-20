#!/usr/bin/env python3
"""
data_elevation_tool.py — Profil d'altitude pour les fichiers data_*.js

Adapte elevation_tool.py pour cibler la structure des data files :
  - staticRoutes:[...]  au lieu de  var staticRoutes = [...];
  - elevProfile:[...]   au lieu de  var elevProfile = [...];

Usage :
    python data_elevation_tool.py build --data data/data_c3.js
    python data_elevation_tool.py build --data data/data_c3.js --only-phases 5
    python data_elevation_tool.py build --data data/data_c3.js --force-refetch
"""

import sys
import re
import json
import argparse
from pathlib import Path

# Réutiliser les fonctions non-IO de elevation_tool
_here = Path(__file__).parent
sys.path.insert(0, str(_here))
from elevation_tool import (
    haversine, _parse_routes, chain_routes, sample_chain,
    fetch_elevations, _coord_key, load_existing_profile
)


# ── Parser data_*.js ────────────────────────────────────────────────────────

def _find_static_routes_data(src):
    """Trouve staticRoutes:[...] dans un data_*.js.
    Retourne (start, end, inner)."""
    m = re.search(r'\bstaticRoutes\s*:\s*\[', src)
    if not m:
        raise ValueError("Bloc 'staticRoutes:[' non trouve dans le fichier")
    start = m.start()
    bracket_start = m.end() - 1
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
    end = i + 1
    return start, end, src[bracket_start + 1:i]


def _load_elevation_cache_data(src):
    """Lit l'elevProfile existant dans un data_*.js et retourne {(lat,lng): alt}."""
    # Trouver elevProfile:[ en cherchant le crochet ouvrant et en comptant la profondeur
    m = re.search(r'\belevProfile\s*:\s*\[', src)
    if not m:
        return {}
    bracket_start = m.end() - 1
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
    try:
        profile = json.loads(src[bracket_start:i + 1])
    except json.JSONDecodeError:
        return {}
    cache = {}
    for seg in profile:
        for pt in seg.get('pts', []):
            if len(pt) >= 4 and pt[1] is not None:
                cache[_coord_key(pt[2], pt[3])] = pt[1]
    return cache


def _inject_data(src, segments):
    """Injecte/remplace elevProfile:[...] dans le data_*.js."""
    js_value = json.dumps(segments, separators=(',', ':'))
    new_block = f'elevProfile:{js_value}'

    # Trouver et remplacer l'existant en comptant les crochets
    m = re.search(r'\belevProfile\s*:\s*\[', src)
    if m:
        bracket_start = m.end() - 1
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
        return src[:m.start()] + new_block + src[i + 1:]

    # Insérer avant la fermeture de l'objet principal
    insert_pos = src.rfind('\n};')
    if insert_pos >= 0:
        return src[:insert_pos] + ',\n  ' + new_block + src[insert_pos:]

    # Fallback : après staticRoutes
    _, end, _ = _find_static_routes_data(src)
    return src[:end] + ',\n  ' + new_block + src[end:]


# ── Commande build ──────────────────────────────────────────────────────────

def build(args):
    src = Path(args.data).read_text(encoding='utf-8')

    only_phases = None
    if args.only_phases:
        only_phases = {int(x) for x in args.only_phases.split(',') if x.strip()}

    _, _, inner = _find_static_routes_data(src)
    routes = _parse_routes(inner)
    chain = chain_routes(routes, include_dashed=args.include_dashed,
                         max_gap=args.max_chain_gap)

    n_solid = sum(1 for r in routes if not r['replaced']
                  and (args.include_dashed or r['da'] == 0))
    print(f"Segments chaines : {len(chain)} / {n_solid} eligibles", file=sys.stderr)

    segments, total_km = sample_chain(chain, step_m=args.sample)
    n_pts = sum(len(s['pts']) for s in segments)
    print(f"Points echantillonnes : {n_pts} | distance totale : {total_km:.1f} km",
          file=sys.stderr)

    # Rapport stop/distance pour calibrer NIGHT_STOPS
    print("\n--- Distances cumulees par phase (pour NIGHT_STOPS) ---", file=sys.stderr)
    for seg in segments:
        if seg['pts']:
            first = seg['pts'][0]
            last  = seg['pts'][-1]
            print(f"  p={seg['p']}  {first[0]:.1f}km -> {last[0]:.1f}km"
                  f"  lat {first[2]:.4f} -> {last[2]:.4f}", file=sys.stderr)

    # Cache altitudes existantes
    cache = {} if args.force_refetch else _load_elevation_cache_data(src)
    if cache:
        print(f"\nCache : {len(cache)} points connus", file=sys.stderr)

    latlngs = []
    index = []
    hits = 0
    for si, seg in enumerate(segments):
        restrict = only_phases is not None and seg['p'] not in only_phases
        for pi, pt in enumerate(seg['pts']):
            cached = cache.get(_coord_key(pt[2], pt[3]))
            if cached is not None:
                pt[1] = cached
                hits += 1
            elif restrict:
                pt[1] = None
            else:
                latlngs.append([pt[2], pt[3]])
                index.append((si, pi))

    print(f"Cache hits : {hits} | a interroger : {len(latlngs)}", file=sys.stderr)

    if latlngs:
        alts = fetch_elevations(latlngs, provider=args.provider,
                                batch=args.batch, pause=args.pause)
        for (si, pi), alt in zip(index, alts):
            segments[si]['pts'][pi][1] = alt
    else:
        print("  aucune requete reseau necessaire", file=sys.stderr)

    src = _inject_data(src, segments)
    Path(args.data).write_text(src, encoding='utf-8')
    print(f"\nelevProfile injecte : {len(segments)} segments, {n_pts} points",
          file=sys.stderr)

    # Afficher les distances aux stops p5 pour calibrage NIGHT_STOPS
    print("\n--- Stops p5 et distances approximatives ---", file=sys.stderr)
    p5_segs = [s for s in segments if s['p'] == 5]
    for seg in p5_segs:
        if seg['pts']:
            f = seg['pts'][0]
            l = seg['pts'][-1]
            print(f"  p5  {f[0]:.1f}km -> {l[0]:.1f}km  "
                  f"({f[2]:.4f},{f[3]:.4f}) -> ({l[2]:.4f},{l[3]:.4f})",
                  file=sys.stderr)


# ── main ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Profil altitude pour data_*.js")
    sub = ap.add_subparsers(dest='command', required=True)

    b = sub.add_parser('build', help='Construire/actualiser elevProfile')
    b.add_argument('--data', required=True, help='Chemin vers data_*.js')
    b.add_argument('--sample', type=float, default=150.0,
                   help='Distance (m) entre points echantillonnes')
    b.add_argument('--max-chain-gap', type=float, default=3000.0,
                   help='Ecart max (m) pour chainer deux traces')
    b.add_argument('--include-dashed', action='store_true')
    b.add_argument('--only-phases', default=None,
                   help="Phases a (re)traiter, ex: '5'")
    b.add_argument('--force-refetch', action='store_true',
                   help='Ignorer le cache')
    b.add_argument('--provider', default='opentopodata',
                   choices=['opentopodata', 'opentopodata-aster'])
    b.add_argument('--batch', type=int, default=100)
    b.add_argument('--pause', type=float, default=1.1)

    args = ap.parse_args()
    if args.command == 'build':
        build(args)


if __name__ == '__main__':
    main()
