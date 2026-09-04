---
inclusion: always
---

# Carte ALBAN_ROUZAUD_3_EVASION_MARKERS.html — Conventions

## Référence aux points

Toujours désigner les points par leur **numéro affiché dans la sidebar** (1, 2, 3…), jamais par leur `id` interne JavaScript.

Les mentions (type `mention`) et les gares (type `gare`) ont un préfixe spécial dans la sidebar (⊙ ou 🚉) mais sont quand même comptées dans le stepN séquentiel — elles ont donc un numéro, même si ce numéro n'est pas affiché visuellement sur le marqueur.

## Table des points actuels (ordre séquentiel dans S[])

| N° sidebar | id JS | Nom court |
|-----------|-------|-----------|
| 1 | 32 | Ferme Grabner |
| 2 | 1 | Kommando Hohenilz |
| 3 | 2 | Weiz |
| 4 | 3 | Forêt NO Weiz |
| 5 | 27 | Pancarte Arbeits Kommando ⊙ |
| 6 | 25 | Bivouac nuit 1 |
| 7 | 4 | Raabklamm |
| 8 | 5 | Bivouac nuit 2 |
| 9 | 23 | Cascade |
| 10 | 28 | Village traversé ⊙ |
| 11 | 29 | Pentes abruptes ⊙ |
| 12 | 6 | Pont Frohnleiten |
| 13 | 26 | Bivouac nuit 3 |
| 14 | 7 | Montagnes (abreuvoirs) |
| 15 | 30 | Grange à foin |
| 16 | 31 | Village carrefour ⊙ |
| 17 | 8 | Bords de la Mur ⊙ |
| 18 | 9 | Forêt le long de la Mur |
| 19 | 10 | Judenburg (gare) |
| 20 | 43 | Grange après Judenburg |
| 21 | 35 | Tentative escalade — raidillon ⊙ |
| 22 | 34 | Bord de la Mur — Dimanche de pêcheurs |
| 23 | 11 | Auto-strade — accident de vélo |
| 24 | 12 | Tunnel gardé |
| 25 | 13 | St. Veit an der Glan |
| 26 | 14 | Lac d'Ossiach |
| 27 | 15 | Villach |
| 28 | 16 | Dernier bivouac Autriche |
| 29 | 17 | Frontière |
| 30 | 33 | Baraque en lisière ⊙ |
| 31 | 18 | Versant italien |
| 32 | 19 | Arrestation |
| 33 | 20 | Tarvisio |
| 34 | 21 | Udine |
| 35 | 22 | Stalag XVIII D — Marburg |

## Notes
- Les numéros peuvent changer si des stops sont ajoutés ou supprimés. Mettre à jour cette table après chaque modification.
- Tous les stops ont un numéro séquentiel, affiché dans la sidebar et sur le marqueur de la carte.
- `type: "mention"` et `type: "gare"` ne changent plus le style visuel — ils ont le même badge numéro que les autres.
