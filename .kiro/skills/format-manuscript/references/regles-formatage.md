# Règles de formatage DOCX

## Structure

- **Page de titre** : titre, auteur, dates centrés. Saut de page après.
- **Marqueurs `--- Page N ---`** : retirés du DOCX.
- **En-tête du .txt** (titre + `====`) : retiré, remplacé par la page de titre.

## Paragraphes

- Chaque ligne non vide du .txt → un paragraphe DOCX. Lignes vides ignorées.
- **Coupures de page** : si un paragraphe ne se termine pas par une ponctuation de fin (`. ! ? »`) et que le paragraphe suivant commence par une minuscule, les fusionner. Ce sont des phrases coupées entre deux pages du manuscrit qui doivent être recollées dans le DOCX. Après fusion, recalculer l'alignement du paragraphe résultant selon les règles ci-dessous (dialogue → gauche, sinon → justifié).
- Espacement entre paragraphes : 2pt. Pas de paragraphes vides.
- **Titres collés au texte** : si `^\d+[re]+ [Jj]ournée\s*:?\s*(.+)` matche, séparer en deux paragraphes (titre en gras, texte en normal).

## Alignement

- Texte narratif : justifié.
- OVERRIDE : lignes commençant par un tiret de dialogue (—, –, -) → alignées à gauche, jamais justifiées.
- Titres de section : gauche, gras.
- Titre du document, "Page(s) manquante(s)", séparateurs : centrés.

## Typographie

- Guillemets droits (`"`) → guillemets français (`«` et `»`) avec espace insécable. Détecter le sens par position : `"` précédé d'un espace ou en début de ligne → `« `, sinon → ` »`.
- Un seul espace entre les mots.

## Police

- Corps : 14pt (ou celle du DOCX modèle si fourni).
- Titres de section : 15pt, gras.
- Page de titre : 16-18pt, gras.
- Tout le reste : normal (le gras est réservé aux titres et à la page de titre).

## Sauts de page

- Avant chaque titre de section (Journées, sections datées, en-têtes nommés).
- Avant "Page(s) manquante(s)". Après aussi, sauf si l'élément suivant déclenche déjà un saut (éviter les pages blanches).

## Numéros de page (footer)

Si un DOCX modèle est fourni, copier l'intégralité de son footer XML (`deepcopy` de chaque enfant de `footer._element`). Les champs PAGE ne sont pas visibles via `.text` sur les paragraphes du footer — inspecter le XML brut pour confirmer leur présence.

Sans template : créer un champ `PAGE \* MERGEFORMAT` dans un paragraphe du footer aligné à droite, via `fldChar` (begin/separate/end) et `instrText`.


---

## Annotations (mode annoté uniquement)

Lorsqu'un `_rapport.md` est fourni, le script annoté ajoute surlignage et commentaires Word sur les zones signalées.

### Source des annotations

Le rapport est parsé par ses sections `## ` :

| Section du rapport | Catégorie |
|---|---|
| Lectures ambiguës | AMBIGU |
| Lectures incertaines | INCERTAIN |
| Passages illisibles | ILLISIBLE |
| Sens douteux | SENS_DOUTEUX |

Chaque section contient une table Markdown. Les lignes d'en-tête et de séparation sont ignorées. Les colonnes varient par section — le script attend le format produit par le skill `transcribe-manuscript` (voir `rapport-format.md`).

### Surlignage

Chaque passage trouvé reçoit un surlignage Word par catégorie :

| Catégorie | Couleur |
|---|---|
| AMBIGU | Jaune |
| INCERTAIN | Turquoise |
| ILLISIBLE | Rose |
| SENS_DOUTEUX | Vert vif |

### Commentaires Word

Chaque passage surligné reçoit un commentaire Word natif contenant la note du rapport. L'auteur du commentaire reprend la catégorie (ex : `Revue [AMBIGU]`). Les notes de plus de 500 caractères sont tronquées.

Les commentaires sont visibles dans le volet « Révision > Commentaires » de Word.

Requiert python-docx >= 1.2.0 pour `document.add_comment()`. Si le script échoue avec une `AttributeError` sur `add_comment`, c'est que la version est trop ancienne.

### Recherche des passages

Pour chaque annotation le mot/passage est cherché dans le texte de la page correspondante :

1. Recherche exacte insensible à la casse
2. Repli sur les 3 premiers mots
3. Repli sur les 2 premiers mots
4. Sinon ignorée (comptée dans les statistiques)

Les chevauchements sont éliminés par ordre de position.

### Légende

Une légende est insérée en page de titre avec un carré coloré par catégorie.
