# Format du rapport de transcription

Nom du fichier : `<X>_rapport.md`, à côté de `<X>.txt`.

```markdown
# Rapport de transcription — [TITRE]

## Résumé
- Source : [fichier]
- Pages transcrites : [N]
- Caractères : [N]
- Mots : [N]

## Lectures ambiguës
| Page | Mot transcrit | Alternative | Contexte |
|------|--------------|-------------|----------|

## Lectures incertaines
| Page | Mot/passage | Note |
|------|------------|------|

## Passages illisibles
| Page | Description |
|------|------------|

## Sens douteux
Phrases correctement lues lettre par lettre mais dont le sens reste obscur :
mot possiblement manquant (coupure de page, numérisation tronquée),
lecture exacte qui pourrait être une autre lecture donnant un meilleur sens,
ou phrase de l'auteur volontairement elliptique.

| Page | Passage transcrit | Problème | Interprétation possible |
|------|------------------|----------|------------------------|

## Pages déplacées
| Page PDF | Ancienne position | Nouvelle position | Raison |
|----------|------------------|-------------------|--------|

## Pages spéciales
- Pages blanches : [liste]
- Pages de titre : [liste]
- Transcriptions échouées : [liste]
```

Les sections sans contenu portent la mention "Aucun." sous l'en-tête de tableau.
