# Troubleshooting & Référence

## Erreurs courantes

### "Image exceeds 5 MB maximum"
Le script de préparation redimensionne à 4.5 MB. Si un sub-agent échoue malgré tout, relancer le script sur cette image avec `MAX_SIZE_BYTES = 3_000_000` dans le script, ou manuellement :
```python
from PIL import Image
img = Image.open("page_large.png")
img = img.resize((img.width // 3, img.height // 3), Image.LANCZOS)
img.convert('RGB').save("page_small.jpg", "JPEG", quality=70)
```

### pdf2image échoue
pdf2image nécessite poppler-utils (outil système) :
- Windows : télécharger depuis https://github.com/oschwartz10612/poppler-windows/releases, ajouter `bin/` au PATH
- Mac : `brew install poppler`
- Linux : `sudo apt install poppler-utils`

Alternative : convertir le PDF manuellement et fournir un dossier d'images.

### Sub-agent qui retourne un fichier vide
Relancer une fois. Si le résultat est toujours vide, l'image est probablement une page blanche ou une couverture. Marquer `[Page blanche]`.

### Qualité de transcription douteuse
Lancer un second sub-agent sur la même page pour comparaison. Fournir plus de contexte dans le prompt (noms de personnages, lieux, vocabulaire spécifique).

## Formats d'entrée

| Format | Extensions | Notes |
|--------|-----------|-------|
| PDF | .pdf | Scans multi-pages, 200-300 DPI recommandé |
| PNG | .png | Meilleure qualité, fichiers lourds |
| JPEG | .jpg, .jpeg | Bon compromis qualité/taille |
| TIFF | .tiff, .tif | Scans professionnels |
| BMP | .bmp | Supporté mais déconseillé (très lourd) |
| WebP | .webp | Supporté |

Les images doivent être nommées avec un padding numérique pour le tri : `page_001.png`, `scan_01.jpg`, `001.png`.

## Limites techniques

| Contrainte | Valeur |
|-----------|--------|
| Taille max image par sub-agent | 5 MB |
| Sub-agents parallèles par vague | 14 |
| Taille après redimensionnement | ~0.3-0.6 MB |
| Résolution après redimensionnement | ~1240x1754 px |

## Estimation de durée

Pour un document de 90 pages : ~15-20 minutes (vs 2-3h en séquentiel).
- Préparation : ~30s
- Transcription (6 vagues de 14) : ~10-15 min
- Consolidation : ~30s
