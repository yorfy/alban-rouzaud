---
name: format-manuscript
description: >
  Génère un DOCX mis en page à partir d'une transcription .txt. Utiliser quand l'utilisateur veut mettre en page un manuscrit transcrit, formater un texte en document Word, ou produire un DOCX de lecture. Supporte un mode annoté qui ajoute surlignage et commentaires Word à partir d'un rapport de transcription (_rapport.md).
metadata:
  author: transcrib
  version: "2.1"
  language: fr
compatibility: >
  Python 3.10+ avec python-docx >= 1.2.0.
---

# Mise en page DOCX

Deux modes : **simple** et **annoté**. Le mode annoté est déclenché quand un `_rapport.md` est fourni ou quand l'utilisateur demande des annotations sur les zones ambiguës.

## Étape 1 — Collecter les entrées

Rassembler :
- le .txt source (préférer `_revue.txt` si une revue a été faite)
- titre, auteur, dates — inférer depuis l'en-tête du .txt si non fournis
- un DOCX modèle (optionnel — marges, police, footer copiés)
- un `_rapport.md` (optionnel — active le mode annoté)

**Critère de fin** : le .txt existe, les métadonnées sont déterminées, le mode (simple ou annoté) est tranché.

## Étape 2 — Générer le DOCX

### Mode simple

```
python .kiro/skills/format-manuscript/scripts/generate_docx.py <source.txt> \
  --title "..." --author "..." --dates "..." [--template modele.docx]
```

### Mode annoté

```
python .kiro/skills/format-manuscript/scripts/generate_docx_annotated.py <source.txt> \
  --rapport <rapport.md> --title "..." --author "..." --dates "..." [--template modele.docx]
```

Le script annoté applique les mêmes règles de formatage puis ajoute surlignage coloré et commentaires Word natifs à partir du rapport. Voir `#[[file:references/regles-formatage.md]]` section « Annotations » pour le détail des couleurs, la recherche des passages et le format des commentaires.

**Critère de fin** : le .docx existe, le script s'est terminé sans erreur, le nombre d'annotations appliquées est affiché. Demander à l'utilisateur d'ouvrir le fichier et de vérifier dans le volet Révision de Word.
