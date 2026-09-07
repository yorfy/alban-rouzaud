---
name: transcribe-manuscript
description: >
  Transcrit des manuscrits scannés (PDF ou images) en texte structuré.
  Utiliser quand l'utilisateur veut transcrire un manuscrit, un document
  ancien, un journal ou des lettres scannées.
metadata:
  author: transcrib
  version: "4.1"
  language: fr
compatibility: >
  Python 3.10+ avec Pillow. Pour les PDF : pymupdf ou pdf2image + poppler.
---

# Transcription de manuscrits scannés

Six phases séquentielles. Convention de nommage : à partir du fichier source `X.pdf`, le dossier de travail est `X/` (images, pages), la transcription `X.txt`, le rapport `X_rapport.md`.

## Phase 1 — Préparer

Collecter auprès de l'utilisateur : source, langue (défaut : français), contexte (époque, auteur, sujet).

```
python .kiro/skills/transcribe-manuscript/scripts/prepare_images.py <source.pdf>
python .kiro/skills/transcribe-manuscript/scripts/prepare_images.py --images-dir <X>/images
```

Voir `references/troubleshooting.md` en cas d'échec.

**Critère de fin** : `<X>/images_small/` contient des images triées par numéro, chacune sous 4.5 MB.

## Phase 2 — Transcrire

OVERRIDE : exactement **un sub-agent `general-task-execution` par page**. Plusieurs images par sub-agent saturent le contexte — interdit.

Prompt template (adapter langue et contexte) :

```
Transcris cette page manuscrite en [LANGUE]. [CONTEXTE]

1. Lis l'image : [CHEMIN]
2. Produis un texte propre structuré en paragraphes :
   - Rassemble les mots coupés par un tiret en fin de ligne.
   - Fusionne les lignes d'un même paragraphe en bloc continu.
   - Chaque changement de paragraphe, tiret de dialogue (—),
     ou espace volontaire large de l'auteur devient un saut de ligne.
   - Conserve la ponctuation et l'orthographe de l'auteur.
   - Un seul espace entre les mots.
   - Mot illisible → [illisible].
3. Vérifie ta transcription :
   - Caractères ambigus : observe l'écriture de cet auteur, identifie
     les lettres qu'il forme de manière similaire. Pour chaque mot
     contenant ces lettres, vérifie le sens de la phrase.
   - Majuscules : les majuscules manuscrites ont souvent une forme
     très différente des minuscules et peuvent être confondues avec
     des chiffres ou d'autres lettres. En début de phrase, vérifie
     que la première lettre est bien une majuscule plausible.
   - Cohérence sémantique : relis chaque phrase. Si un mot produit
     une phrase absurde, retourne à l'image.
   - Noms propres inhabituels : signale-les (lecture incertaine).
4. Crée <X>/pages/page_[NNN].txt avec le texte transcrit.
5. Après une ligne "---NOTES---", liste les points d'attention :
   - [AMBIGU] "mot" ou "alternative" (contexte)
   - [INCERTAIN] "nom propre" (lecture incertaine)
   - [ILLISIBLE] description du passage
   - [SENS DOUTEUX] "phrase" — le texte est lisible mais le sens
     reste obscur (mot possiblement manquant, coupure de page,
     ou lecture exacte qui pourrait être un autre mot donnant
     un meilleur sens). Proposer une interprétation si possible.
   Si aucune note, écrire "---NOTES---" suivi de "Aucune."
```

Vagues de 14 sub-agents maximum. Un retry par échec, puis `[TRANSCRIPTION ÉCHOUÉE]`.

**Critère de fin** : un fichier .txt par page.

## Phase 3 — Assembler

Lire les fichiers .txt dans l'ordre. Séparer texte et notes (séparateur `---NOTES---`). Assembler le texte avec marqueurs `--- Page N ---` et en-tête. Collecter toutes les notes pour le rapport (phase 5). Chaque paragraphe est séparé par un simple retour à la ligne — pas de lignes vides entre les paragraphes.

Seule transformation : fusionner les mots coupés entre pages (`mot-` en fin de page + minuscule en début de la suivante).

**Critère de fin** : fichier `<X>.txt` créé.

## Phase 4 — Valider l'ordre

Lire le document et vérifier la continuité narrative entre pages. Si une page interrompt le récit, la déplacer à sa position logique. Marqueur de traçabilité :
```
--- Page Xbis (page M du PDF, repositionnée) ---
```
Consigner chaque déplacement pour le rapport.

**Critère de fin** : le document est narrativement cohérent.

## Phase 5 — Rapport

Générer `<X>_rapport.md` en suivant le format décrit dans `references/rapport-format.md`. Le rapport agrège les notes des sub-agents (phase 2), les déplacements (phase 4), et les statistiques.

**Critère de fin** : le fichier rapport existe à côté de la transcription.

## Phase 6 — Nettoyer

Supprimer `<X>/images_small/`. Conserver `<X>/images/` et `<X>/pages/` par défaut.

**Critère de fin** : `images_small/` supprimé.
