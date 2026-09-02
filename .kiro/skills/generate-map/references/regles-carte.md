# Conventions de carte

## Structure du tableau stops

Chaque entrée du tableau `stops` (ou `S` en version compacte) :

```javascript
{
    id: 1,           // identifiant unique
    day: 1,          // journée (cahier 2) ou p: 1 (période, cahier 1)
    name: "Nom",     // nom affiché
    lat: 49.123,     // latitude WGS84
    lng: 5.456,      // longitude WGS84
    desc: "...",     // description courte
    quote: "...",    // citation du texte (optionnel)
    route: "...",    // indication de route (optionnel)
    type: "mention"  // "depart", "capture", "mention", ou absent (étape normale)
}
```

## Marqueurs

- **Étape** (pas de type) : cercle numéroté, couleur du jour/période
- **Mention** (`type: "mention"`) : symbole ⊙, pas numérotée — lieu signalé mais non traversé
- **Départ** (`type: "depart"`) : étoile ★
- **Capture/Fin** (`type: "capture"`) : carré ■

## Numérotation

Les étapes sont numérotées séquentiellement (1, 2, 3...) en excluant les mentions, départs et captures. Si deux étapes successives sont au même endroit (< 500m), elles partagent le même numéro.

## Noms incertains

Quand un toponyme du manuscrit ne correspond pas à un lieu connu :
- Ajouter `[NomProposé ?]` dans le nom : `"Grantham [Avocourt ?]"`
- Expliquer l'hypothèse dans la description
- Citer le texte original entre guillemets

## Tracés (staticRoutes)

Chaque entrée :
```javascript
{p: 1, da: 0, distKm: 17.4, coords: [[lat,lng], [lat,lng], ...]}
```

- `p` : période/jour (pour la couleur)
- `da` : 0 = trait plein, 1 = pointillé (train, parcours inconnu)
- `distKm` : distance en km
- `coords` : tableau de [lat, lng] en WGS84

## Fonds de carte

Trois couches disponibles :
1. **OpenTopoMap** (moderne, par défaut)
2. **Carte IGN 1950** — la plus proche de l'époque des récits
3. **Carte d'État-Major** (1820-1866) — utile pour identifier les anciens toponymes

## Affichage des coordonnées

Toujours inclure un div en bas à droite affichant lat/lng du curseur pour permettre à l'utilisateur de pointer des positions exactes.
