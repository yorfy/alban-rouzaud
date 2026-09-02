# Transcription de manuscrits scannés

Transcription automatique de documents manuscrits (PDF ou images) via le skill Kiro `transcribe-manuscript`. Le modèle IA lit directement les images et produit un texte structuré en paragraphes.

## Prérequis

- **Kiro IDE** avec accès aux sub-agents
- **Python 3.10+** avec Pillow (`pip install Pillow`)
- **pymupdf** pour la conversion PDF → images (`pip install pymupdf`)

## Utilisation

Dans Kiro, invoquer le skill :

```
/transcribe-manuscript
```

Ou simplement demander : *"Transcris ce manuscrit"* — Kiro détecte le skill automatiquement.

Le skill demande la source (PDF ou dossier d'images), la langue et le contexte du document, puis exécute 6 phases automatiques : préparation, transcription parallèle, assemblage, validation de l'ordre, rapport et nettoyage.

## Structure du workspace

```
document_source.pdf              ← fichier scanné
document_source.txt              ← transcription finale
document_source_rapport.md       ← rapport (lectures ambiguës, pages déplacées...)
document_source/
├── images/                      ← pages extraites du PDF
├── images_small/                ← redimensionnées (supprimé après)
└── pages/                       ← un .txt par page
```

## Manuscrits transcrits

| Document | Pages | Caractères |
|----------|-------|------------|
| ALBAN ROUZAUD 1 — La Guerre (1939-1940) | 41 | ~44 000 |
| ALBAN ROUZAUD 2 — Journal non écrit d'un fantassin en repli stratégique | 90 | ~70 000 |

## Skill

Le skill se trouve dans `.kiro/skills/transcribe-manuscript/` :
- `SKILL.md` — instructions (6 phases avec critères de fin)
- `scripts/prepare_images.py` — conversion PDF et redimensionnement
- `references/troubleshooting.md` — dépannage et limites techniques
- `references/rapport-format.md` — format du rapport de transcription
