"""
maplibre_tool.py — Outil de manipulation des cartes MapLibre HTML.

Opérations disponibles :
  inject     Injecte staticRoutes + elevProfile depuis une carte Leaflet source
  patch-js   Remplace un bloc JS identifié par un marqueur BEGIN/END
  set-style  Change le style de base (osm/topo/satellite)
  info       Affiche les tailles des blocs JS injectés

Usage :
  python maplibre_tool.py inject  --src LEAFLET.html --dst MAPLIBRE.html
  python maplibre_tool.py patch-js --html MAPLIBRE.html --marker addMarkerLayer --file patch.js
  python maplibre_tool.py info   --html MAPLIBRE.html
"""

import argparse
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers HTML
# ---------------------------------------------------------------------------

def read_html(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_html(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")


def extract_js_var(html: str, var_name: str) -> str:
    """Extrait le bloc 'var NAME = [...];' ou 'var NAME = {...};' depuis le HTML."""
    start = html.find(f"var {var_name} = ")
    if start == -1:
        raise ValueError(f"Variable '{var_name}' introuvable dans le HTML.")
    # Trouver la fin : chercher '];' ou '};' après le début
    # On cherche le premier '];' ou '};' à partir de la position du '='
    eq = html.index("=", start) + 1
    bracket_open = html[eq:].lstrip()[0]
    bracket_close = "];" if bracket_open == "[" else "};"
    end = html.find(bracket_close, eq) + len(bracket_close)
    if end < len(bracket_close):
        raise ValueError(f"Fin du bloc '{var_name}' introuvable.")
    return html[start:end]


def replace_js_var(html: str, var_name: str, new_block: str) -> str:
    """Remplace le bloc 'var NAME = ...;' par new_block."""
    old = extract_js_var(html, var_name)
    return html.replace(old, new_block, 1)


def inject_placeholder(html: str, placeholder: str, block: str) -> str:
    """Remplace '// PLACEHOLDER' par block dans le HTML."""
    if placeholder not in html:
        raise ValueError(f"Placeholder '{placeholder}' introuvable.")
    return html.replace(placeholder, block, 1)


# ---------------------------------------------------------------------------
# Commande : inject
# ---------------------------------------------------------------------------

def cmd_inject(args):
    src = read_html(args.src)
    dst = read_html(args.dst)

    changed = False
    for var in ["staticRoutes", "elevProfile"]:
        try:
            block = extract_js_var(src, var)
        except ValueError as e:
            print(f"  SKIP {var}: {e}", file=sys.stderr)
            continue

        placeholder = f"// {var.upper()}_PLACEHOLDER"
        if placeholder in dst:
            dst = inject_placeholder(dst, placeholder, block)
            print(f"  inject {var}: placeholder → {len(block)} chars")
        elif f"var {var} = " in dst:
            dst = replace_js_var(dst, var, block)
            print(f"  inject {var}: replace existing → {len(block)} chars")
        else:
            print(f"  SKIP {var}: ni placeholder ni variable existante trouvés", file=sys.stderr)
            continue
        changed = True

    if changed:
        write_html(args.dst, dst)
        print(f"Écrit : {args.dst}  ({len(dst)} chars)")
    else:
        print("Rien à injecter.", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Commande : patch-js
# ---------------------------------------------------------------------------

def cmd_patch_js(args):
    """Remplace le bloc de code entre les marqueurs
    // BEGIN:<marker> ... // END:<marker> dans le HTML."""
    html = read_html(args.html)
    patch = Path(args.file).read_text(encoding="utf-8")

    begin = f"// BEGIN:{args.marker}"
    end   = f"// END:{args.marker}"

    i_begin = html.find(begin)
    i_end   = html.find(end)
    if i_begin == -1 or i_end == -1:
        raise ValueError(f"Marqueurs BEGIN/END:{args.marker} introuvables.")

    # Inclure les marqueurs dans le remplacement
    i_end += len(end)
    new_block = f"{begin}\n{patch}\n{end}"
    html = html[:i_begin] + new_block + html[i_end:]
    write_html(args.html, html)
    print(f"Patché {args.marker} dans {args.html}")


# ---------------------------------------------------------------------------
# Commande : replace-block
# ---------------------------------------------------------------------------

def cmd_replace_block(args):
    """Remplace la première occurrence de --old par le contenu de --new-file."""
    html = read_html(args.html)
    old  = Path(args.old_file).read_text(encoding="utf-8") if args.old_file else args.old
    new  = Path(args.new_file).read_text(encoding="utf-8")

    if old not in html:
        raise ValueError("Bloc 'old' introuvable dans le HTML.")
    html = html.replace(old, new, 1)
    write_html(args.html, html)
    print(f"Bloc remplacé dans {args.html}  ({len(html)} chars)")


# ---------------------------------------------------------------------------
# Commande : set-style
# ---------------------------------------------------------------------------

BASEMAP_TILES = {
    "osm":       "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    "topo":      "https://tile.opentopomap.org/{z}/{x}/{y}.png",
    "satellite": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
}

def cmd_set_style(args):
    if args.basemap not in BASEMAP_TILES:
        raise ValueError(f"Basemap inconnu : {args.basemap}. Choix : {list(BASEMAP_TILES)}")
    html = read_html(args.html)
    # Remplacer la propriété currentBasemap par défaut dans le JS
    html = re.sub(
        r"var currentBasemap\s*=\s*['\"](\w+)['\"]",
        f"var currentBasemap = '{args.basemap}'",
        html,
    )
    write_html(args.html, html)
    print(f"Style par défaut → {args.basemap}")


# ---------------------------------------------------------------------------
# Commande : info
# ---------------------------------------------------------------------------

def cmd_info(args):
    html = read_html(args.html)
    total = len(html)
    print(f"Fichier : {args.html}")
    print(f"  Taille totale : {total:,} chars  ({total // 1024} KB)")
    for var in ["staticRoutes", "elevProfile", "S", "PC", "PN"]:
        try:
            block = extract_js_var(html, var)
            print(f"  {var:<20} {len(block):>8,} chars")
        except ValueError:
            print(f"  {var:<20}   absent")

    # Compter les couches MapLibre
    n_addlayer = html.count("map.addLayer(")
    n_addsource = html.count("map.addSource(")
    print(f"  map.addLayer()  : {n_addlayer}")
    print(f"  map.addSource() : {n_addsource}")

    # Glyphs
    if "glyphs:" in html:
        m = re.search(r"glyphs:\s*['\"]([^'\"]+)['\"]", html)
        print(f"  glyphs          : {m.group(1) if m else '(trouvé mais non parsé)'}")
    else:
        print("  glyphs          : absent (OK pour file://)")

    # Terrain
    if "setTerrain" in html:
        m = re.search(r"exaggeration:\s*([\d.]+)", html)
        print(f"  terrain         : exaggeration={m.group(1) if m else '?'}")
    else:
        print("  terrain         : absent")


# ---------------------------------------------------------------------------
# Commande : strip-glyphs
# ---------------------------------------------------------------------------

def cmd_strip_glyphs(args):
    """Supprime la ligne glyphs: du style et toute couche symbol qui dépend de text-field."""
    html = read_html(args.html)
    original_len = len(html)

    # 1. Supprimer la ligne glyphs:
    html = re.sub(r"\s*//[^\n]*glyphs[^\n]*\n", "\n", html)
    html = re.sub(r"\s*glyphs:\s*['\"][^'\"]+['\"],?\n", "\n", html)

    # 2. Supprimer les blocs addLayer avec type:'symbol' qui contiennent text-font
    #    Pattern : map.addLayer({ id:'...', type:'symbol', ... text-font ... });
    html = re.sub(
        r"map\.addLayer\(\{[^}]*type\s*:\s*['\"]symbol['\"][^}]*text-font[^}]*\}\s*\)\s*;",
        "/* symbol layer with text-font removed by maplibre_tool strip-glyphs */",
        html,
        flags=re.DOTALL,
    )

    write_html(args.html, html)
    print(f"strip-glyphs : {original_len - len(html):+} chars  → {args.html}")


# ---------------------------------------------------------------------------
# Commande : use-svg-icons
# ---------------------------------------------------------------------------

# Bloc JS de remplacement pour les fonctions de marqueurs Maki SDF
# (remplace SHAPE_DEFS + makeMarkerImageSVG)
_SVG_ICONS_JS = r"""
// ---- MARQUEURS MAKI (SDF) + BADGES NUMÉROTÉS ----
// Icônes Maki open-source (CC0) chargées depuis GitHub raw.
// Mode SDF : la couleur est appliquée via icon-color au runtime — une seule
// image par type, recolorée par phase dans la couche symbol.
// Les étapes numérotées (shape='step') utilisent un badge canvas (cercle + chiffre).

var MAKI_BASE = 'https://raw.githubusercontent.com/mapbox/maki/main/icons/';

// Mapping type → nom d'icône Maki
var MAKI_ICON = {
  bivouac:  'campsite',
  frontiere:'entrance',
  capture:  'prison',
  kommando: 'roadblock',
  ferme:    'farm',
  retour:   'rail',
  mention:  'circle-stroked'
  // 'step' → badge canvas numéroté (pas de Maki)
};

// Charge un SVG depuis GitHub raw, le convertit en ImageData SDF-compatible
// (noir sur fond transparent) pour addImage avec { sdf: true }
function loadMakiSDF(iconName) {
  var url = MAKI_BASE + iconName + '.svg';
  return fetch(url)
    .then(function(r) { return r.text(); })
    .then(function(svgText) {
      // Forcer fill="#000" pour que MapLibre SDF fonctionne
      var colored = svgText.replace(/fill="[^"]*"/g, 'fill="#000"')
                           .replace(/fill:[^;}"']*/g, 'fill:#000');
      var uri = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(colored);
      return new Promise(function(resolve) {
        var img = new Image();
        img.onload = function() {
          var sz = 32;
          var cv = document.createElement('canvas');
          cv.width = cv.height = sz;
          cv.getContext('2d').drawImage(img, 0, 0, sz, sz);
          var id = cv.getContext('2d').getImageData(0, 0, sz, sz);
          resolve({ width: sz, height: sz, data: id.data });
        };
        img.src = uri;
      });
    });
}

// Badge numéroté canvas pour les étapes ordinaires (shape='step')
function makeBadgeImage(label, color) {
  var sz = 28;
  var cv = document.createElement('canvas');
  cv.width = cv.height = sz;
  var ctx = cv.getContext('2d');
  // Cercle plein
  ctx.beginPath();
  ctx.arc(sz/2, sz/2, sz/2 - 2, 0, 2*Math.PI);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.lineWidth = 2.5;
  ctx.strokeStyle = 'rgba(255,255,255,0.92)';
  ctx.stroke();
  // Chiffre
  ctx.fillStyle = '#fff';
  ctx.font = 'bold ' + Math.round(sz * 0.42) + 'px Arial,sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(label, sz/2, sz/2 + 0.5);
  var id = ctx.getImageData(0, 0, sz, sz);
  return { width: sz, height: sz, data: id.data };
}
""".strip()

# Bloc JS de remplacement pour buildMarkersGeoJSON — ajoute iconShape + badgeKey/sdfKey
_BUILD_MARKERS_JS = r"""
function buildMarkersGeoJSON() {
  var SHAPE_FOR_TYPE = {
    bivouac: 'bivouac', frontiere: 'frontiere', capture: 'capture',
    kommando: 'kommando', ferme: 'ferme', retour: 'retour',
    mention: 'mention'
  };
  var stepN = 0;
  var features = [];
  S.forEach(function(s) {
    var isMention = s.type === 'mention';
    var isCapture = s.type === 'capture';
    var label = '';
    if (!isMention && !isCapture) { stepN++; label = String(stepN); }
    else if (isCapture) label = '\u25a0';
    else label = '\u2299';
    var shape = SHAPE_FOR_TYPE[s.type] || 'step';

    features.push({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [s.lng, s.lat] },
      properties: {
        id: s.id, p: s.p, n: s.n, date: s.date || '', d: s.d,
        q: s.q || '', r: s.r || '', type: s.type || 'step',
        label: label,
        color: PC[s.p] || '#888',
        isMention: isMention ? 1 : 0,
        isCapture: isCapture ? 1 : 0,
        iconShape: shape,
        radius: isMention ? 8 : 13,
        strokeW: isMention ? 1 : 2.5
      }
    });
  });
  return { type: 'FeatureCollection', features: features };
}
""".strip()

# Bloc JS de remplacement pour addMarkerLayer — Maki SDF + badges canvas
_ADD_MARKER_LAYER_JS = r"""
function addMarkerLayer() {
  var geojson = buildMarkersGeoJSON();

  // --- 1. Badges canvas (sync) pour les étapes numérotées ---
  var seenBadge = {};
  geojson.features.forEach(function(f) {
    var p = f.properties;
    if (p.iconShape !== 'step') return;
    var key = 'badge-' + p.label + '-' + p.color.replace('#','');
    p.badgeKey = key;
    if (!seenBadge[key] && !map.hasImage(key)) {
      seenBadge[key] = true;
      map.addImage(key, makeBadgeImage(p.label, p.color));
    }
  });

  // --- 2. SDF Maki (async) — une image par type, partagée entre phases ---
  var makiNeeded = {};
  geojson.features.forEach(function(f) {
    var shape = f.properties.iconShape;
    if (shape === 'step') return;
    var iconName = MAKI_ICON[shape];
    if (!iconName) return;
    var sdfKey = 'maki-' + iconName;
    f.properties.sdfKey = sdfKey;
    if (!makiNeeded[sdfKey] && !map.hasImage(sdfKey)) {
      makiNeeded[sdfKey] = iconName;
    }
  });

  var sdfPromises = Object.keys(makiNeeded).map(function(sdfKey) {
    return loadMakiSDF(makiNeeded[sdfKey]).then(function(imgData) {
      if (!map.hasImage(sdfKey)) map.addImage(sdfKey, imgData, { sdf: true });
    });
  });

  Promise.all(sdfPromises).then(function() {
    if (map.getSource('stops')) { map.getSource('stops').setData(geojson); return; }
    map.addSource('stops', { type: 'geojson', data: geojson });

    // Couche 1 : badges numérotés pour les étapes ordinaires
    map.addLayer({ id: 'stops-badge', type: 'symbol', source: 'stops',
      filter: ['==', ['get', 'iconShape'], 'step'],
      layout: {
        'icon-image': ['get', 'badgeKey'],
        'icon-allow-overlap': true,
        'icon-ignore-placement': true,
        'icon-pitch-alignment': 'map',
        'icon-rotation-alignment': 'map',
        'icon-size': 1
      }
    });

    // Couche 2 : icônes Maki SDF pour les types spéciaux
    // icon-color est data-driven → couleur de phase appliquée au runtime
    map.addLayer({ id: 'stops-maki', type: 'symbol', source: 'stops',
      filter: ['!=', ['get', 'iconShape'], 'step'],
      layout: {
        'icon-image': ['get', 'sdfKey'],
        'icon-allow-overlap': true,
        'icon-ignore-placement': true,
        'icon-pitch-alignment': 'map',
        'icon-rotation-alignment': 'map',
        'icon-size': ['case', ['==', ['get', 'iconShape'], 'mention'], 0.7, 1.0]
      },
      paint: {
        'icon-color': ['get', 'color'],
        'icon-halo-color': 'rgba(255,255,255,0.9)',
        'icon-halo-width': 1.5
      }
    });

    // Zone de clic invisible couvrant les deux couches
    map.addLayer({ id: 'stops-hit', type: 'circle', source: 'stops',
      paint: {
        'circle-radius': 18,
        'circle-color': 'rgba(0,0,0,0)',
        'circle-pitch-alignment': 'map'
      }
    });

    // Hover
    map.on('mouseenter', 'stops-hit', function(e) {
      map.getCanvas().style.cursor = 'pointer';
      var id = e.features[0].properties.id;
      map.setLayoutProperty('stops-badge', 'icon-size', ['case', ['==',['get','id'],id], 1.25, 1.0]);
      map.setLayoutProperty('stops-maki',  'icon-size', ['case', ['==',['get','id'],id], 1.25,
        ['case', ['==',['get','iconShape'],'mention'], 0.7, 1.0]]);
    });
    map.on('mouseleave', 'stops-hit', function() {
      map.getCanvas().style.cursor = '';
      map.setLayoutProperty('stops-badge', 'icon-size', 1.0);
      map.setLayoutProperty('stops-maki',  'icon-size', ['case', ['==',['get','iconShape'],'mention'], 0.7, 1.0]);
    });

    // Clic → popup
    map.on('click', 'stops-hit', function(e) {
      var props = e.features[0].properties;
      var s = S.find(function(x){ return x.id === props.id; }) || props;
      var html = '<div class="pt">'+(s.n||props.n)+'</div>'
        + '<div class="pp">'+(s.date||props.date)+' &mdash; '+(PN[s.p||props.p]||'')+'</div>'
        + '<div class="px">'+(s.d||props.d)+'</div>'
        + ((s.q||props.q) ? '<div class="pq">&laquo;&nbsp;'+(s.q||props.q)+'&nbsp;&raquo;</div>' : '')
        + ((s.r||props.r) ? '<div class="px" style="margin-top:4px;color:#667788;font-style:italic">'+(s.r||props.r)+'</div>' : '');
      new maplibregl.Popup({ offset: 16, maxWidth: '310px' })
        .setLngLat(e.lngLat)
        .setHTML(html)
        .addTo(map);
    });
  }); // fin Promise.all
}
""".strip()


def cmd_use_svg_icons(args):
    """Remplace le bloc marqueurs (MAKI_ICON + loadMakiSDF + makeBadgeImage),
    buildMarkersGeoJSON et addMarkerLayer par les versions Maki SDF."""
    html = read_html(args.html)
    original_len = len(html)

    def _repl(text):
        return lambda m: text + '\n\n'

    # --- 1. Remplacer le bloc marqueurs (MARQUEURS NATIFS ou MARQUEURS MAKI) ---
    pat_make = re.compile(
        r'// ---- MARQUEURS (?:NATIFS WebGL|MAKI \(SDF\)).*?(?=\nfunction addMarkerLayer)',
        re.DOTALL,
    )
    if not pat_make.search(html):
        raise ValueError(
            "Bloc '// ---- MARQUEURS …' introuvable. "
            "Vérifiez que la carte est bien une carte MapLibre générée par cet outil."
        )
    html = pat_make.sub(_repl(_SVG_ICONS_JS), html, count=1)
    print("  loadMakiSDF + makeBadgeImage : bloc marqueurs mis à jour")

    # --- 2. Remplacer buildMarkersGeoJSON ---
    pat_build = re.compile(
        r'function buildMarkersGeoJSON\(\).*?(?=\n// =+\n// AJOUT)',
        re.DOTALL,
    )
    if not pat_build.search(html):
        raise ValueError(
            "Fonction buildMarkersGeoJSON() introuvable ou délimiteur '// ==…// AJOUT' manquant."
        )
    html = pat_build.sub(_repl(_BUILD_MARKERS_JS), html, count=1)
    print("  buildMarkersGeoJSON : iconShape conservé")

    # --- 3. Remplacer addMarkerLayer ---
    pat_add = re.compile(
        r'function addMarkerLayer\(\).*?(?=\n// =+\n// SIDEBAR)',
        re.DOTALL,
    )
    if not pat_add.search(html):
        raise ValueError(
            "Fonction addMarkerLayer() introuvable ou délimiteur '// ==…// SIDEBAR' manquant."
        )
    html = pat_add.sub(_repl(_ADD_MARKER_LAYER_JS), html, count=1)
    print("  addMarkerLayer : Maki SDF + badges canvas")

    write_html(args.html, html)
    delta = len(html) - original_len
    print(f"Écrit : {args.html}  ({len(html):,} chars, {delta:+d})")


# ---------------------------------------------------------------------------
# Commande : rebuild
# ---------------------------------------------------------------------------

def cmd_rebuild(args):
    """Reconstruit une carte MapLibre depuis un template HTML et une carte Leaflet source.
    Le template doit contenir // STATICROUTES_PLACEHOLDER et // ELEVPROFILE_PLACEHOLDER."""
    template = read_html(args.template)
    src      = read_html(args.src)
    out      = args.out or args.template.replace(".html", "_rebuilt.html")

    for var, ph in [("staticRoutes", "// STATICROUTES_PLACEHOLDER"),
                    ("elevProfile",  "// ELEVPROFILE_PLACEHOLDER")]:
        try:
            block = extract_js_var(src, var)
        except ValueError:
            print(f"  SKIP {var}", file=sys.stderr)
            continue
        if ph in template:
            template = template.replace(ph, block, 1)
            print(f"  {var}: {len(block):,} chars injectés")
        else:
            print(f"  SKIP {var}: placeholder {ph!r} absent du template", file=sys.stderr)

    write_html(out, template)
    print(f"Reconstruit → {out}  ({len(template):,} chars)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Manipulation des cartes MapLibre HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # inject
    p = sub.add_parser("inject", help="Injecte staticRoutes+elevProfile depuis une carte Leaflet")
    p.add_argument("--src",  required=True, help="Carte Leaflet source (HTML)")
    p.add_argument("--dst",  required=True, help="Carte MapLibre destination (HTML, modifiée en place)")

    # patch-js
    p = sub.add_parser("patch-js", help="Remplace un bloc BEGIN/END dans le HTML")
    p.add_argument("--html",   required=True)
    p.add_argument("--marker", required=True, help="Nom du marqueur BEGIN/END")
    p.add_argument("--file",   required=True, help="Fichier .js contenant le nouveau bloc")

    # replace-block
    p = sub.add_parser("replace-block", help="Remplace un bloc de texte exact")
    p.add_argument("--html",     required=True)
    p.add_argument("--old",      default=None, help="Texte exact à remplacer (alternatif à --old-file)")
    p.add_argument("--old-file", default=None, dest="old_file", help="Fichier contenant le texte à remplacer")
    p.add_argument("--new-file", required=True, dest="new_file", help="Fichier contenant le remplacement")

    # set-style
    p = sub.add_parser("set-style", help="Change le style de base par défaut")
    p.add_argument("--html",    required=True)
    p.add_argument("--basemap", required=True, choices=list(BASEMAP_TILES))

    # info
    p = sub.add_parser("info", help="Affiche les infos d'une carte MapLibre HTML")
    p.add_argument("--html", required=True)

    # strip-glyphs
    p = sub.add_parser("strip-glyphs", help="Supprime glyphs et couches symbol text-font (pour file://)")
    p.add_argument("--html", required=True)

    # use-svg-icons
    p = sub.add_parser("use-svg-icons",
        help="Remplace les marqueurs cercle-numéro par des icônes SVG thématiques "
             "(bivouac=tente, frontiere=drapeau, capture=cadenas, kommando=barbelé, ferme=maison…)")
    p.add_argument("--html", required=True, help="Carte MapLibre HTML à modifier en place")

    # rebuild
    p = sub.add_parser("rebuild", help="Reconstruit depuis template + source Leaflet")
    p.add_argument("--template", required=True, help="Template HTML MapLibre avec placeholders")
    p.add_argument("--src",      required=True, help="Carte Leaflet source pour les données")
    p.add_argument("--out",      default=None,  help="Fichier de sortie (défaut: template_rebuilt.html)")

    args = parser.parse_args()

    dispatch = {
        "inject":        cmd_inject,
        "patch-js":      cmd_patch_js,
        "replace-block": cmd_replace_block,
        "set-style":     cmd_set_style,
        "info":          cmd_info,
        "strip-glyphs":  cmd_strip_glyphs,
        "use-svg-icons": cmd_use_svg_icons,
        "rebuild":       cmd_rebuild,
    }
    try:
        dispatch[args.cmd](args)
    except Exception as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
