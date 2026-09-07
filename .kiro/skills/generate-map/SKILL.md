---
name: generate-map
description: >
  Génère ou met à jour une carte HTML interactive du parcours décrit dans un manuscrit transcrit. Utiliser quand l'utilisateur veut créer une carte, ajouter/modifier/supprimer des étapes ou des tracés routiers, ou corriger le positionnement d'un lieu.
metadata:
  author: transcrib
  version: "2.0"
  language: fr
compatibility: >
  Python 3.10+, accès internet (API BRouter). MapLibre GL JS 4.7 chargé via CDN.
---

# Génération de carte interactive

Produit un fichier HTML autonome avec **MapLibre GL JS**, des marqueurs HTML pin teardrop et des tracés routiers pré-calculés via BRouter. Les tracés sont embarqués en statique — pas de requête réseau au chargement sauf tuiles de fond et terrain Re:Earth.

## Template de référence

Le fichier **`ALBAN_ROUZAUD_3_EVASION_MARKERS.html`** est le template de référence actuel. Toute nouvelle carte doit reprendre son architecture :

- MapLibre GL JS 4.7 (CDN unpkg)
- Terrain 3D Re:Earth (CC BY 4.0), hillshade, `maxPitch: 85`
- Fonds raster commutables : OSM / OpenTopoMap / Satellite
- **Marqueurs HTML pin teardrop** (pas de couches symbol WebGL)
- Icônes SVG inline par type de stop (aucun fetch réseau)
- Profil altitude canvas en bas, synchronisé carte ↔ courbe
- Sidebar groupée par phase, collapsible

Pour créer une nouvelle carte, copier ce template et injecter les données via `maplibre_tool.py inject`.

## Étape 1 — Analyser le texte source

Lire la transcription pour extraire :
- les **noms de lieux** traversés ou mentionnés, dans l'ordre chronologique
- la **direction de marche** et les distances relatives entre étapes
- les **éléments de paysage** qui aident à géolocaliser (rivière, clocher, forêt, remblai)

Classifier chaque lieu selon les types définis dans #[[file:references/regles-carte.md]].

**Critère de fin** : la liste ordonnée des lieux est établie avec classification et coordonnées proposées.

## Étape 2 — Géolocaliser les lieux

Pour chaque lieu :
1. Chercher les coordonnées via recherche web ou connaissance
2. Vérifier cohérence avec la direction et les distances du récit
3. Si incertain, proposer une position avec `[?]` dans le nom et une note dans `d:`

L'utilisateur peut corriger en pointant avec la souris (affichage coordonnées intégré dans la carte).

**Critère de fin** : chaque lieu a des coordonnées lat/lng validées ou marquées incertaines.

## Étape 3 — Générer les tracés routiers

Utiliser `brouter_tool.py` pour récupérer les tracés. Choix du profil BRouter selon le terrain :

| Contexte | Profil | Usage |
|----------|--------|-------|
| Route départementale, nationale | `fastbike` | Déplacements militaires, convois |
| Chemin de montagne, sentier | `trekking` | Randonnée, sentiers de contrebande |
| Petite route rurale, chemin carrossable | `mtb` | Compromis route/chemin |

### Commandes brouter_tool.py

```bash
# Lister les routes existantes
python .kiro/skills/generate-map/scripts/brouter_tool.py list --html CARTE.html

# Ajouter une route
python .kiro/skills/generate-map/scripts/brouter_tool.py insert \
    --profile fastbike --waypoints "lat1,lng1|lat2,lng2" \
    --html CARTE.html --period 1

# Remplacer une route existante
python .kiro/skills/generate-map/scripts/brouter_tool.py replace \
    --profile trekking --waypoints "lat1,lng1|lat2,lng2" \
    --html CARTE.html --period 1 --index 0

# Supprimer une route
python .kiro/skills/generate-map/scripts/brouter_tool.py delete --html CARTE.html --index 2

# Route en pointillé (trajet en train, parcours inconnu)
python .kiro/skills/generate-map/scripts/brouter_tool.py insert \
    --profile fastbike --waypoints "..." --html CARTE.html --period 4 --dashed
```

Les waypoints sont en format `lat,lng` séparés par `|`. Le script convertit automatiquement en `lng,lat` pour BRouter.

**Segments en ligne droite** : préfixer un waypoint par `s:` rend **droit** le segment qui **arrive** à ce point.

```bash
# route A->B, LIGNE DROITE B->C, route C->D
python .kiro/skills/generate-map/scripts/brouter_tool.py replace \
    --profile trekking \
    --waypoints "Alat,Alng|Blat,Blng|s:Clat,Clng|Dlat,Dlng" \
    --html CARTE.html --period 2 --index 3
```

**Critère de fin** : chaque segment du parcours a un tracé routier cohérent avec le récit.

## Étape 4 — Assembler le HTML

Partir du template `ALBAN_ROUZAUD_3_EVASION_MARKERS.html` :

1. Copier le template sous le nouveau nom
2. Mettre à jour `<title>`, `<h1>`, `<p>` en-tête et le sous-titre
3. Remplacer les tableaux `PC`, `PN`, `S` par les données du nouveau parcours
4. Ajouter les placeholders dans le HTML copié :
   ```html
   // STATICROUTES_PLACEHOLDER
   // ELEVPROFILE_PLACEHOLDER
   ```
5. Injecter les tracés et le profil via `maplibre_tool.py` :
   ```bash
   python .kiro/skills/generate-map/scripts/maplibre_tool.py inject \
       --src SOURCE_AVEC_DONNEES.html --dst NOUVELLE_CARTE.html
   ```
6. Ajuster `center`, `zoom`, `pitch` initiaux selon le parcours

### Tableau S — structure

```javascript
{
  id: 1,             // identifiant unique entier
  p: 1,              // période/phase (pour couleur et groupement sidebar)
  n: "Nom du lieu",  // nom affiché
  lat: 47.238,       // latitude WGS84
  lng: 15.699,       // longitude WGS84
  date: "20 sept.",  // date ou période (affiché dans popup)
  d: "Description",  // description courte
  q: "Citation",     // citation du texte (optionnel)
  r: "Route info",   // info de route (optionnel)
  type: "bivouac"    // voir types ci-dessous — absent = étape ordinaire
}
```

**Critère de fin** : le HTML s'ouvre dans un navigateur, tous les marqueurs et tracés sont visibles.

## Étape 5 — Profil d'altitude (optionnel)

```bash
python .kiro/skills/generate-map/scripts/elevation_tool.py build --html CARTE.html
```

Options utiles : `--sample 150`, `--max-chain-gap 3000`, `--only-phases 2,3`, `--force-refetch`.

Après tout `brouter_tool.py replace/insert/delete`, relancer `elevation_tool.py build` pour resynchroniser.

**Critère de fin** : la courbe s'affiche en bas, les couleurs correspondent aux phases, le survol synchronise carte et courbe.

## Architecture marqueurs HTML

Les marqueurs utilisent `maplibregl.Marker({ element: el, anchor: 'bottom' })`.

**Règle critique** : les dimensions `width` et `height` doivent être fixées **en CSS inline** sur l'élément wrapper, **avant** l'appel `.addTo(map)`. MapLibre lit `offsetWidth`/`offsetHeight` au moment de l'ajout pour calculer l'ancrage. Un wrapper sans dimensions explicites produit un positionnement erroné.

**Règle hover** : ne jamais appliquer `transform: scale()` sur le wrapper du marqueur. Appliquer le scale sur un élément **enfant** (`.inner`). Sinon MapLibre recalcule l'ancrage et le marqueur saute/disparaît.

```javascript
// ✅ Correct
var el = document.createElement('div');
el.style.cssText = 'width:36px;height:46px;display:block;cursor:pointer;';
var inner = document.createElement('div');
inner.style.cssText = 'width:36px;height:46px;transition:transform .15s;transform-origin:bottom center;';
el.appendChild(inner);
el.addEventListener('mouseenter', function() { inner.style.transform = 'scale(1.25) translateY(-4px)'; });
el.addEventListener('mouseleave', function() { inner.style.transform = ''; });
new maplibregl.Marker({ element: el, anchor: 'bottom' }).setLngLat([lng, lat]).addTo(map);

// ❌ Incorrect — le scale sur el fait sauter le marqueur
el.addEventListener('mouseenter', function() { el.style.transform = 'scale(1.25)'; });
```

**Rotation avec bearing** : les marqueurs HTML ne tournent pas avec la carte (limitation MapLibre). C'est le comportement attendu, identique à Google Maps et Mapbox.

## Configuration carte

```javascript
var map = new maplibregl.Map({
  container: 'map',
  style: STYLES.osm,   // fond raster commutable
  center: [lng, lat],
  zoom: 7,
  pitch: 45,
  bearing: 0,
  maxPitch: 85,        // toujours spécifier — défaut MapLibre 4.x = 60°
  attributionControl: { compact: true }
});
```

`maxPitch: 85` est la limite native de MapLibre GL JS. Au-delà, les tiles de l'horizon ne se chargent pas.
