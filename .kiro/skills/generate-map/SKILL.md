---
name: generate-map
description: >
  Génère ou met à jour une carte HTML interactive du parcours décrit dans un manuscrit transcrit. Utiliser quand l'utilisateur veut créer une carte, ajouter/modifier/supprimer des étapes ou des tracés routiers, ou corriger le positionnement d'un lieu.
metadata:
  author: transcrib
  version: "1.0"
  language: fr
compatibility: >
  Python 3.10+, accès internet (API BRouter). Leaflet chargé via CDN dans le HTML.
---

# Génération de carte interactive

Produit un fichier HTML autonome avec Leaflet, des marqueurs d'étapes et des tracés routiers pré-calculés via BRouter. Les tracés sont embarqués en statique : pas de requête réseau au chargement (sauf tuiles de fond).

## Étape 1 — Analyser le texte source

Lire la transcription pour extraire :
- les **noms de lieux** traversés ou mentionnés, dans l'ordre chronologique
- la **direction de marche** et les distances relatives entre étapes
- les **éléments de paysage** qui aident à géolocaliser (rivière, clocher, forêt, remblai)

Classifier chaque lieu :
- **étape** : lieu traversé physiquement, marqueur numéroté
- **mention** : lieu signalé sans y passer (combat au loin, direction non prise), marqueur ⊙
- **départ** ★ et **capture/fin** ■

Consulter #[[file:references/regles-carte.md]] pour les conventions de structuration.

**Critère de fin** : la liste ordonnée des lieux est établie avec classification et coordonnées proposées.

## Étape 2 — Géolocaliser les lieux

Pour chaque lieu :
1. Chercher les coordonnées via recherche web ou connaissance
2. Vérifier sur la carte d'État-Major (couche IGN) si le toponyme existe
3. Si incertain, proposer une position avec `[?]` dans le nom et une note explicative

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

**Segments en ligne droite** : préfixer un waypoint par `s:` rend **droit** (interpolé, non routé) le segment qui **arrive** à ce point. On peut mélanger routage et lignes droites dans un seul appel. Utile quand le récit décrit une traversée hors route (à travers prés, coupe à flanc) là où BRouter forcerait un détour par une route.

```bash
# route A->B, LIGNE DROITE B->C, route C->D
python .kiro/skills/generate-map/scripts/brouter_tool.py replace \
    --profile trekking \
    --waypoints "Alat,Alng|Blat,Blng|s:Clat,Clng|Dlat,Dlng" \
    --html CARTE.html --period 2 --index 3
```

Les points droits sont interpolés tous les ~30 m. Plusieurs `s:` consécutifs enchaînent plusieurs segments droits ; un tracé entièrement droit (2 waypoints, le second en `s:`) ne fait aucun appel réseau.

**Critère de fin** : chaque segment du parcours a un tracé routier cohérent avec le récit, visible sur la carte.

## Étape 4 — Assembler le HTML

La carte HTML contient :
- **En-tête** : titre, sous-titre
- **Sidebar** : étapes groupées par journée/période, numérotées, cliquables
- **Carte Leaflet** : fonds IGN 1950, État-Major, OpenTopoMap
- **Marqueurs** : numérotés (étapes), ⊙ (mentions), ★ (départ), ■ (capture)
- **Tracés** : polylines colorées par jour/période, avec distance en tooltip
- **Coordonnées** : affichage lat/lng du curseur en bas à droite

Le tableau `stops` définit les marqueurs, le tableau `staticRoutes` contient les tracés pré-calculés.

**Critère de fin** : le HTML s'ouvre dans un navigateur, tous les marqueurs et tracés sont visibles et cohérents avec le récit.

## Étape 5 — Profil d'altitude (optionnel)

Ajoute une courbe altitude/distance en bas de la carte, colorée par période, avec interaction bidirectionnelle carte ↔ courbe (survol/clic sur la courbe met un marqueur sur la carte ; clic sur la carte met en avant le point le plus proche sur la courbe). Panneau masquable via un bouton.

### Données : `elevation_tool.py`

Le script chaîne les tracés **pleins** (`da=0`) dans l'ordre du parcours à pied, échantillonne les points, interroge un service d'élévation (OpenTopoData SRTM30m, gratuit, ~1 req/s) et injecte un tableau `elevProfile` dans le HTML.

```bash
# Construire / actualiser le profil d'altitude
python .kiro/skills/generate-map/scripts/elevation_tool.py build --html CARTE.html

# Options utiles
#   --sample 150         distance (m) entre points échantillonnés
#   --max-chain-gap 3000 écart max (m) pour chaîner deux tracés consécutifs
#   --include-dashed     inclure aussi les tracés pointillés (train/escorte)
#   --only-phases 2,3    ne (re)traiter que ces phases (les autres segments conservés)
#   --force-refetch      ignorer le cache et tout re-interroger
```

**Mise à jour incrémentale** : par défaut, les altitudes déjà présentes dans le
`elevProfile` existant sont réutilisées (cache par coordonnée à 5 décimales).
Après un `brouter_tool.py replace/insert`, relancer `build` n'interroge le
service d'élévation **que pour les points nouveaux** du tracé modifié ; le
chaînage et les distances cumulées sont recalculés localement, donc le profil
reste cohérent même quand un segment change de longueur. Utiliser
`--force-refetch` pour forcer un recalcul complet.

Format injecté :
```js
var elevProfile = [ {p:<période>, pts:[[distKm, alt, lat, lng], ...]}, ... ];
```
- `distKm` : distance cumulée depuis le début du parcours
- `alt` : altitude en mètres (SRTM 30 m)
- `lat,lng` : coordonnées du point (interaction carte ↔ courbe)

**IMPORTANT** : après toute modification des tracés (`brouter_tool.py insert/replace/delete`), **relancer `elevation_tool.py build`** pour resynchroniser le profil. Le script est idempotent : il remplace le `elevProfile` existant.

### Rendu (dans le HTML)

Le panneau `#elevpanel` contient un `<canvas id="elevcanvas">` dessiné en JS :
- aire + ligne colorées segment par segment via `PC[p]` (mêmes couleurs que les tracés)
- axes : altitude (m) à gauche, distance (km) en bas
- curseur mobile relié à un `L.circleMarker` sur la carte
- bouton `#elevtoggle` pour afficher/masquer

**Critère de fin** : la courbe s'affiche en bas, les couleurs correspondent aux périodes, et le survol/clic synchronise carte et courbe.
