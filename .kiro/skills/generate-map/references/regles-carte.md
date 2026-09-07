# Conventions de carte

## Structure du tableau S (stops)

```javascript
{
  id: 1,             // identifiant unique entier
  p: 1,              // période/phase (1-N, pour couleur et groupement sidebar)
  n: "Nom du lieu",  // nom affiché dans marqueur et sidebar
  lat: 49.123,       // latitude WGS84
  lng: 5.456,        // longitude WGS84
  date: "20 sept.",  // date ou fourchette de dates (affiché dans popup)
  d: "Description",  // description courte (contexte narratif)
  q: "Citation",     // citation directe du texte (optionnel)
  r: "Route info",   // indication de route ou lieu-dit (optionnel)
  type: "bivouac"    // type de stop — voir table ci-dessous (absent = étape ordinaire)
}
```

## Types de stops

| `type` | Marqueur | Icône | Usage |
|--------|----------|-------|-------|
| *(absent)* | pin numéroté | chiffre blanc | Étape ordinaire traversée physiquement |
| `"mention"` | pin petit | ⓘ (info) | Lieu signalé sans y passer, non numéroté |
| `"bivouac"` | pin | tente △ | Nuit passée en plein air ou dans une grange |
| `"frontiere"` | pin | drapeau | Passage de frontière |
| `"capture"` | pin | cadenas 🔒 | Arrestation, capture, internement |
| `"kommando"` | pin | grille ⛔ | Camp de travail, Kommando |
| `"ferme"` | pin | maison 🏠 | Ferme, habitation où l'on est hébergé |
| `"retour"` | pin | locomotive 🚂 | Retour en captivité (train, escorte) |

Les types `"mention"` utilisent un pin plus petit (26×32 px vs 36×46 px pour les autres).

## Numérotation

Les étapes sont numérotées séquentiellement (1, 2, 3…) en excluant les stops typés (`mention`, `bivouac`, `frontiere`, `capture`, `kommando`, `ferme`, `retour`). Seuls les stops sans `type` ou avec un `type` non reconnu reçoivent un numéro.

## Noms incertains

Quand un toponyme du manuscrit ne correspond pas à un lieu identifié avec certitude :
- Ajouter `[?]` dans le nom : `"Village au carrefour [?]"`
- Expliquer l'hypothèse dans le champ `d`
- Citer le texte original dans `q`

## Tableaux couleurs et noms de phases

```javascript
var PC = {1:'#e94560', 2:'#f5a623', 3:'#2ecc71', 4:'#3498db', ...};
// Clé = numéro de phase (entier), valeur = couleur CSS hex
// Utiliser des couleurs bien contrastées sur fond sombre (#16213e)

var PN = {1:'I — Titre phase 1', 2:'II — Titre phase 2', ...};
// Clé = numéro de phase, valeur = nom affiché dans la sidebar
```

## Tracés (staticRoutes)

```javascript
{p: 1, da: 0, distKm: 17.4, coords: [[lat,lng], [lat,lng], ...]}
```

- `p` : phase (pour la couleur via `PC`)
- `da` : `0` = trait plein (à pied, à vélo), `1` = pointillé (train, parcours inconnu)
- `distKm` : distance totale du segment en km
- `coords` : tableau `[lat, lng]` en WGS84 (ordre lat/lng, pas lng/lat)

## Fonds de carte disponibles

```javascript
var STYLES = {
  osm:       // OpenStreetMap — défaut, bon équilibre
  topo:      // OpenTopoMap — relief détaillé, idéal pour zones montagneuses
  satellite: // Esri World Imagery — vue aérienne
};
```

Commutable via les boutons radio dans la sidebar.

## Terrain 3D

Toujours inclure le terrain Re:Earth avec hillshade :

```javascript
map.addSource('dem', {
  type: 'raster-dem',
  url: 'https://terrain.reearth.land/mapbox/elevation/tilejson.json',
  tileSize: 256, maxzoom: 15,
  attribution: 'Re:Earth Terrain · Mapterhorn (CC BY 4.0)'
});
map.setTerrain({ source: 'dem', exaggeration: 1.0 });
```

`maxPitch: 85` doit être spécifié dans les options `Map` (le défaut MapLibre 4.x est 60°).

## Profil altitude

Format injecté dans le HTML :
```javascript
var elevProfile = [ {p: 1, pts: [[distKm, alt, lat, lng], ...]}, ... ];
```

- `distKm` : distance cumulée depuis le début du parcours (km)
- `alt` : altitude SRTM 30m (mètres)
- `lat`, `lng` : coordonnées pour la synchronisation carte ↔ courbe

## Affichage des coordonnées

Toujours inclure un affichage lat/lng du curseur pour permettre de pointer des positions exactes :

```javascript
map.on('mousemove', function(e) {
  document.getElementById('coords').textContent =
    'lat: ' + e.lngLat.lat.toFixed(5) + '   lng: ' + e.lngLat.lng.toFixed(5);
});
```
